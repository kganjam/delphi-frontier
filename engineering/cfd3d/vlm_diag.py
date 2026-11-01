"""Analytic-planform control for the VLM's rigid-CL refinement behaviour (contract: vlm_diag_contract.json).

    python -I engineering/cfd3d/vlm_diag.py OUTDIR [--deadline S] [--extended] [--repair] [--arms ID,ID] [--panels PATH]
    python -I engineering/cfd3d/vlm_diag.py merge OUT.json RESULTS_DIR [RESULTS_DIR ...]

Runs the frozen arms in order on the unchanged vlm.py, writes OUTDIR/results.json atomically after every solve,
and classifies each refinement family by the contract's rules. Inputs are checked by sha256 and refused on a
mismatch. Nothing here changes vlm.py; the local-velocity Kutta-Joukowski lift is a labelled diagnostic only.
--repair runs the post-hoc REPAIR variant of vlm_diag_addendum_repair.json (panel-consistent collocation, only C
moved); merge combines result directories and adds the addendum's D_colloc against the core variant.
"""
from __future__ import annotations

import os

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("vlm", HERE / "vlm.py")
vlm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vlm)
CONTRACT = json.loads((HERE / "vlm_diag_contract.json").read_text())
ADDENDUM = json.loads((HERE / "vlm_diag_addendum_repair.json").read_text())
ALPHA = 4.0
TOL_ROUND = 1e-12


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def helm(a: float) -> float:
    return 2 * math.pi * a / (2 + math.sqrt(a * a + 4))


def shoelace(poly: np.ndarray) -> float:
    x, y = poly[:, 0], poly[:, 1]
    return 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


PLANAR = (np.zeros(3), np.array([0, 1.0, 0]), np.array([1.0, 0, 0]), np.array([0, 0, 1.0]))


def ellipse_poly(ar: float, k: int) -> np.ndarray:
    """vlm.elliptic's outline (span 1, straight quarter-chord line) with k uniform-in-span points per edge."""
    c0 = 4.0 / (math.pi * ar)
    y = np.linspace(-0.5, 0.5, k)
    c = c0 * np.sqrt(np.clip(1 - (2 * y) ** 2, 0, 1))
    return np.vstack([np.c_[y, -c / 4], np.c_[y[::-1], 3 * c[::-1] / 4]])


RECT = np.array([[-0.5, 0.0], [0.5, 0.0], [0.5, 0.25], [-0.5, 0.25]])
U_STEP = -0.5 + 1 / math.pi
NOTCH = np.array([[-0.5, 0.0], [0.5, 0.0], [0.5, 0.125], [U_STEP, 0.125], [U_STEP, 0.25], [-0.5, 0.25]])


def repair_colloc(lat: dict, origin, e_u, e_w, f: float = 0.75) -> dict:
    """REPAIR (addendum): collocation at the 3/4 point of the panel's own corners, averaged over its two strip
    edges, instead of the chord at the strip midpoint. Only C changes."""
    uw = lat["uw"]                    # corners: edge i front, edge i+1 front, edge i+1 rear, edge i rear
    um = 0.5 * (uw[:, 0, 0] + uw[:, 1, 0])
    wc = 0.5 * ((uw[:, 0, 1] + f * (uw[:, 3, 1] - uw[:, 0, 1])) + (uw[:, 1, 1] + f * (uw[:, 2, 1] - uw[:, 1, 1])))
    return {**lat, "C": origin + um[:, None] * e_u + wc[:, None] * e_w}


def builders(fins: dict, repair: bool = False) -> dict:
    """arm id -> f(ns, nc) returning (lattice, S_ref, owners-or-None, per-owner reference areas)."""
    def fix(lat, origin, e_u, e_w):
        return repair_colloc(lat, origin, e_u, e_w) if repair else lat

    def poly_arm(poly):
        return lambda ns, nc: (fix(vlm.lattice(poly, *PLANAR, ns, nc), *PLANAR[:3]), shoelace(poly), None, None)

    def fin_one(f, ns, nc):
        lat, geo = vlm.fin_setup(fins[f], ns, nc)
        return fix(lat, geo["origin"], geo["eu"], geo["ew"])

    def fin_arm(names):
        def build(ns, nc):
            lats = {f: fin_one(f, ns, nc) for f in names}
            areas = {f: float(fins[f]["area_flat_m2"]) for f in names}
            lat = vlm.combine(lats) if len(names) > 1 else lats[names[0]]
            return lat, sum(areas.values()), (lat["owner"] if len(names) > 1 else None), areas
        return build

    def ell(ar, colloc=0.75):
        def build(ns, nc):
            lat, s = vlm.elliptic(ar, ns, nc, colloc=colloc)
            return fix(lat, *PLANAR[:3]), s, None, None
        return build

    return {
        "R0_reproduce_owner07": fin_arm(list(vlm.PAIRED)),
        "N1_mutant_collocation_quarter_chord": ell(6, colloc=0.25),
        "A1_elliptic_AR6_dense": ell(6),
        "A2_elliptic_AR4_dense": ell(4),
        "A3_rectangle_AR4": poly_arm(RECT),
        "A4_elliptic_AR4_coarse7": poly_arm(ellipse_poly(4, 7)),
        "A4_elliptic_AR4_coarse16": poly_arm(ellipse_poly(4, 16)),
        "N2_notched_rectangle": poly_arm(NOTCH),
        "F1_pectoral_L_isolated": fin_arm(["pectoral_L"]),
        "F2_pelvic_L_isolated": fin_arm(["pelvic_L"]),
        "F3_four_fins_combined": fin_arm(list(vlm.PAIRED)),
    }


def measure(lat, S: float, owners, areas) -> dict:
    """CL on S_ref from the unchanged vlm.solve, plus the labelled local-velocity KJ diagnostic."""
    t0 = time.perf_counter()
    g, F, _, V = vlm.solve(lat, ALPHA)
    t_solve = time.perf_counter() - t0
    a = math.radians(ALPHA)
    ldir = np.array([-math.sin(a), 0, math.cos(a)])
    lift = float(F.sum(axis=0) @ ldir)
    out = {"CL": lift / (0.5 * S), "panels": len(g), "area_ratio": float(lat["area"].sum() / S), "solve_s": t_solve}
    # local-velocity KJ: same horseshoes and far legs as vlm.solve, evaluated at each bound-segment midpoint
    A, B = lat["A"], lat["B"]
    span = max(np.ptp(np.vstack([A, B]), axis=0).max(), 1e-9)
    xhat = np.array([1.0, 0.0, 0.0])
    Af, Bf = A + vlm.FAR * span * xhat, B + vlm.FAR * span * xhat
    mid = 0.5 * (A + B)
    Vloc = np.empty_like(mid)
    for i in range(0, len(mid), 256):
        sl = slice(i, i + 256)
        v = vlm.seg_vel(mid[sl], Af, A) + vlm.seg_vel(mid[sl], A, B) + vlm.seg_vel(mid[sl], B, Bf)
        Vloc[sl] = V + np.einsum("nmk,m->nk", v, g)
    Floc = g[:, None] * np.cross(Vloc, B - A)
    out["KJ_local_over_freestream_lift_minus_1"] = float(Floc.sum(axis=0) @ ldir) / lift - 1
    if owners is not None:
        o = np.array(owners)
        out["per_fin_CL"] = {f: float(F[o == f].sum(axis=0) @ ldir) / (0.5 * ar) for f, ar in areas.items()}
    out["wall_s"] = time.perf_counter() - t0
    return out


# ---------------------------------------------------------------- classification (contract "classification")
def triple(f1: float, f2: float, f3: float) -> dict:
    e21, e32 = f2 - f1, f3 - f2
    tol = TOL_ROUND * abs(f3)
    if abs(e21) <= tol and abs(e32) <= tol:
        return {"status": "converged_roundoff", "eps21": e21, "eps32": e32}
    if e21 == 0:
        return {"status": "divergent", "R": None, "eps21": e21, "eps32": e32}
    R = e32 / e21
    st = "monotone_convergent" if 0 < R < 1 else "oscillatory_convergent" if -1 < R < 0 else "divergent"
    out = {"status": st, "R": R, "eps21": e21, "eps32": e32}
    if st == "monotone_convergent":
        out["p"] = math.log(1 / R) / math.log(2)
    return out


def family(vals: dict[int, float], triples: list, decisive: list, tail: list) -> dict:
    need = sorted({n for t in triples + decisive for n in t} | set(tail))
    missing = [n for n in need if n not in vals]
    out = {"values": {str(n): vals[n] for n in sorted(vals)}, "missing": missing}
    out["triples"] = {"-".join(map(str, t)): triple(*(vals[n] for n in t)) for t in triples if all(n in vals for n in t)}
    if missing:
        out["verdict"] = "incomplete"
        return out
    ok = ("monotone_convergent", "converged_roundoff")
    dec = {"-".join(map(str, t)): triple(*(vals[n] for n in t)) for t in decisive}
    d = [vals[b] - vals[a] for a, b in itertools.pairwise(tail)]
    tol = TOL_ROUND * abs(vals[tail[-1]])
    same = all(x > 0 for x in d) or all(x < 0 for x in d) or all(abs(x) <= tol for x in d)
    out.update(decisive=dec, tail=tail, tail_differences=d, tail_same_sign=same)
    out["verdict"] = "regular" if same and all(v["status"] in ok for v in dec.values()) else "irregular"
    return out


def families_spec(extended: bool) -> dict:
    f = CONTRACT["families"]
    span, chord = list(f["span"]["ns"]), list(f["chord"]["nc"])
    spec = {"span": {"members": span, "triples": f["triples_r2"]["span"], "decisive": f["decisive_triples"]["span"], "tail": f["tail"]["span"]},
            "chord": {"members": chord, "triples": f["triples_r2"]["chord"], "decisive": f["decisive_triples"]["chord"], "tail": f["tail"]["chord"]}}
    if extended:
        e = CONTRACT["execution"]["extended"]["families"]
        spec["span_extended"] = {"members": span + e["span"]["ns_add"], "triples": f["triples_r2"]["span"] + e["span"]["decisive_triples"],
                                 "decisive": e["span"]["decisive_triples"], "tail": e["span"]["tail"]}
        spec["chord_extended"] = {"members": chord + e["chord"]["nc_add"], "triples": f["triples_r2"]["chord"] + e["chord"]["decisive_triples"],
                                  "decisive": e["chord"]["decisive_triples"], "tail": e["chord"]["tail"]}
    return spec


def points(extended: bool) -> list[tuple[int, int]]:
    """(ns, nc) solve list for a family arm: span family at nc 8, then chord family at ns 32; no duplicates."""
    s = families_spec(extended)
    span = s["span_extended" if extended else "span"]["members"]
    chord = s["chord_extended" if extended else "chord"]["members"]
    nc0, ns0 = CONTRACT["families"]["span"]["nc"], CONTRACT["families"]["chord"]["ns"]
    pts = [(n, nc0) for n in span] + [(ns0, n) for n in chord]
    return list(dict.fromkeys(pts))


def classify_arm(solves: dict, extended: bool) -> dict:
    nc0, ns0 = CONTRACT["families"]["span"]["nc"], CONTRACT["families"]["chord"]["ns"]
    span = {ns: r["CL"] for (ns, nc), r in solves.items() if nc == nc0 and "CL" in r}
    chord = {nc: r["CL"] for (ns, nc), r in solves.items() if ns == ns0 and "CL" in r}
    s = families_spec(extended)
    out = {k: family(span if k.startswith("span") else chord, v["triples"], v["decisive"], v["tail"]) for k, v in s.items()}
    for tag, keys in (("core", ("span", "chord")), ("extended", ("span_extended", "chord_extended"))):
        if all(k in out for k in keys):
            v = [out[k]["verdict"] for k in keys]
            out[f"arm_{tag}"] = "incomplete" if "incomplete" in v else "regular" if all(x == "regular" for x in v) else "irregular"
    return out


def law_check(solves: dict) -> dict:
    """Helmbold A = 6 at the finest core member of each family (contract reference.law_check)."""
    ref = helm(6)
    fam = CONTRACT["families"]
    at = [(fam["span"]["ns"][-1], fam["span"]["nc"]), (fam["chord"]["ns"], fam["chord"]["nc"][-1])]
    rows = {}
    for p in at:
        r = solves.get(p, {})
        if "CL" in r:
            cla = r["CL"] / math.radians(ALPHA)
            rows[f"{p[0]}x{p[1]}"] = {"CL_alpha": cla, "rel_err": cla / ref - 1}
    tol = json.loads((HERE / "gates_vlm.json").read_text())["controls"]["V1_elliptic_AR6"]["pass"]["rel_err_max"]
    done = len(rows) == len(at)
    return {"reference_helmbold_A6": ref, "tolerance": tol, "at": rows,
            "pass": (all(abs(v["rel_err"]) <= tol for v in rows.values()) if done else None)}


def decide(arms: dict, extended: bool) -> dict:
    key = "arm_extended" if extended else "arm_core"

    def v(a):
        c = arms.get(a, {}).get("classification", {})
        return c.get(key) or c.get("arm_core") or "incomplete"

    r0 = arms.get("R0_reproduce_owner07", {}).get("reproduced")
    if r0 is not True:
        return {"precondition_R0": r0, "all": "invalid" if r0 is False else "unknown"}
    a1 = arms.get("A1_elliptic_AR6_dense", {})
    n1 = arms.get("N1_mutant_collocation_quarter_chord", {})
    n1_law = (n1.get("law_check") or {}).get("pass")
    n1_flag = v("N1_mutant_collocation_quarter_chord") == "irregular" or n1_law is False
    n2_flag = v("N2_notched_rectangle") == "irregular"
    smooth = [v(a) for a in ("A1_elliptic_AR6_dense", "A2_elliptic_AR4_dense", "A3_rectangle_AR4")]
    samp = {a: v(a) for a in ("A4_elliptic_AR4_coarse7", "A4_elliptic_AR4_coarse16", "F1_pectoral_L_isolated", "F2_pelvic_L_isolated")}
    f3 = v("F3_four_fins_combined")
    d = {"precondition_R0": True, "N1_flagged": n1_flag, "N2_flagged": n2_flag}
    if "irregular" in smooth:
        d["D_scheme"] = "indicated"
    elif all(x == "regular" for x in smooth) and n2_flag:
        d["D_scheme"] = "not_indicated"
    else:
        d["D_scheme"] = "unknown"
    lp = (a1.get("law_check") or {}).get("pass")
    if v("A1_elliptic_AR6_dense") == "regular" and lp is False:
        d["D_law"] = "indicated"
    elif v("A1_elliptic_AR6_dense") == "regular" and lp is True and n1_flag:
        d["D_law"] = "not_indicated_at_3pct"
    else:
        d["D_law"] = "unknown"
    if all(x == "regular" for x in smooth) and "irregular" in samp.values():
        d["D_sampling"] = "indicated"
        d["D_sampling_irregular_arms"] = sorted(a for a, x in samp.items() if x == "irregular")
    elif all(x == "regular" for x in smooth + list(samp.values())) and n2_flag:
        d["D_sampling"] = "not_indicated"
    else:
        d["D_sampling"] = "unknown"
    f12 = [samp["F1_pectoral_L_isolated"], samp["F2_pelvic_L_isolated"]]
    if "irregular" in f12:
        d["D_interaction"] = "confounded"
    elif all(x == "regular" for x in f12) and f3 == "irregular":
        d["D_interaction"] = "indicated"
    elif all(x == "regular" for x in f12 + [f3]) and n2_flag:
        d["D_interaction"] = "not_indicated"
    else:
        d["D_interaction"] = "unknown"
    return d


def colloc_decision(core: dict, rep: dict, extended: bool) -> dict:
    """Addendum D_colloc: the repaired arms against the core rectangle (invariance) and the N2 negative."""
    fam, arm_key = ("chord_extended", "arm_extended") if extended else ("chord", "arm_core")

    def cls(arms, a):
        return arms.get(a, {}).get("classification", {})

    a3c, a3r = core.get("A3_rectangle_AR4", {}).get("solves", {}), rep.get("A3_rectangle_AR4", {}).get("solves", {})
    pairs = {k: (a3c[k].get("CL"), a3r[k].get("CL")) for k in a3r if k in a3c}
    rel = {k: (r / c - 1) if c is not None and r is not None else None for k, (c, r) in pairs.items()}
    full = {f"{n}x{m}" for n, m in points(extended)}
    if any(v is not None and abs(v) > TOL_ROUND for v in rel.values()):
        inv = False
    else:
        inv = True if full <= {k for k, v in rel.items() if v is not None} else None
    n2 = (cls(rep, "N2_notched_rectangle").get(arm_key) or "incomplete") == "irregular"
    chord = {a: (cls(rep, a).get(fam) or {}).get("verdict", "incomplete") for a in ("A1_elliptic_AR6_dense", "A2_elliptic_AR4_dense")}
    arm = {a: cls(rep, a).get(arm_key) or "incomplete" for a in chord}
    if inv is False:
        d = "invalid"
    elif not n2:
        d = "unknown"
    elif "irregular" in chord.values():
        d = "refuted"
    elif inv is True and all(v == "regular" for v in arm.values()):
        d = "supported"
    else:
        d = "unknown"
    fins = {a: {k: (cls(rep, a).get(k) or {}).get("verdict", "incomplete")
                for k in (("span_extended", "chord_extended") if extended else ("span", "chord"))}
            for a in ("F1_pectoral_L_isolated", "F2_pelvic_L_isolated", "F3_four_fins_combined")}
    return {"D_colloc": d, "invariance_rectangle": inv, "invariance_max_abs_rel": max((abs(v) for v in rel.values() if v is not None), default=None),
            "N2_flagged": n2, "A1_A2_repaired_chord": chord, "A1_A2_repaired_arm": arm, "fins_repaired_by_family": fins,
            "A1_repaired_law_check": rep.get("A1_elliptic_AR6_dense", {}).get("law_check")}


def merge(out: Path, dirs: list[Path]) -> dict:
    """Combine result directories (any mix of core/repair, core/extended) and decide on the union."""
    variants: dict[str, dict] = {"core": {}, "repair": {}}
    src, extended = [], False
    for d in dirs:
        r = json.loads((d / "results.json").read_text())
        src.append({"dir": str(d), "variant": r.get("variant", "core"), "mode": r["mode"], "status": r["status"],
                    "runner_sha256": r["runner_sha256"], "elapsed_s": r.get("elapsed_s")})
        extended |= r["mode"] == "extended"
        for a, v in r["arms"].items():
            if a in variants[r.get("variant", "core")]:
                raise SystemExit(f"REFUSED: arm {a} appears twice in variant {r.get('variant', 'core')}")
            variants[r.get("variant", "core")][a] = v
    res = {"schema": "cfd3d-vlm-diag-merged-0.1", "sources": src, "contract_sha256": sha(HERE / "vlm_diag_contract.json"),
           "addendum_sha256": sha(HERE / "vlm_diag_addendum_repair.json"), "arms": variants,
           "decisions_core": decide(variants["core"], False)}
    if extended:
        res["decisions_extended"] = decide(variants["core"], True)
    if variants["repair"]:
        res["addendum_core"] = colloc_decision(variants["core"], variants["repair"], False)
        if extended:
            res["addendum_extended"] = colloc_decision(variants["core"], variants["repair"], True)
    out.write_text(json.dumps(res, indent=1))
    return res


def write(out: Path, res: dict) -> None:
    tmp = out / f".results.json.tmp.{os.getpid()}"
    tmp.write_text(json.dumps(res, indent=1))
    os.replace(tmp, out / "results.json")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "merge":
        r = merge(Path(argv[1]), [Path(x) for x in argv[2:]])
        print(json.dumps({k: r[k] for k in r if k.startswith(("decisions", "addendum"))}, indent=1))
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--deadline", type=float, default=CONTRACT["execution"]["local_probe"]["deadline_s"])
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--repair", action="store_true")
    ap.add_argument("--arms", default="")
    ap.add_argument("--panels", type=Path, default=HERE.parents[1] / CONTRACT["source"]["panels_json"]["path"])
    a = ap.parse_args(argv)
    src = CONTRACT["source"]
    for p, want in ((HERE / "vlm.py", src["vlm_py"]["sha256"]), (a.panels, src["panels_json"]["sha256"])):
        if sha(p) != want:
            print(f"REFUSED: {p.name} sha256 {sha(p)} != contract {want}", file=sys.stderr)
            return 2
    fins = json.loads(a.panels.read_text())["fins"]
    a.outdir.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    res = {"schema": "cfd3d-vlm-diag-results-0.1", "contract_sha256": sha(HERE / "vlm_diag_contract.json"),
           "runner_sha256": sha(Path(__file__)), "vlm_py_sha256": sha(HERE / "vlm.py"), "panels_sha256": sha(a.panels),
           "environment": {"python": platform.python_version(), "numpy": np.__version__,
                           "threads": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
                           "cpus_visible": len(os.sched_getaffinity(0))},
           "mode": "extended" if a.extended else "core", "variant": "repair" if a.repair else "core",
           "addendum_sha256": sha(HERE / "vlm_diag_addendum_repair.json") if a.repair else None, "deadline_s": a.deadline, "alpha_deg": ALPHA,
           "status": "running", "arms": {}}
    write(a.outdir, res)
    build = builders(fins, repair=a.repair)
    order = CONTRACT["arm_order"]
    allowed = ADDENDUM["repair_variant"]["arms"] if a.repair else order
    chosen = [x for x in a.arms.split(",") if x] or allowed
    unknown = [x for x in chosen if x not in build or x not in allowed]
    if unknown:
        print(f"REFUSED: unknown arms {unknown}", file=sys.stderr)
        return 2
    r0 = CONTRACT["arms"][0]["values"]
    for arm in [x for x in order if x in chosen]:
        if arm == "R0_reproduce_owner07":
            pts = [tuple(map(int, k.split("x"))) for k in r0]
        else:
            pts = points(a.extended)
        rec = res["arms"].setdefault(arm, {"solves": {}})
        solves = {}
        for ns, nc in pts:
            key = f"{ns}x{nc}"
            if time.monotonic() - t0 > a.deadline:
                rec["solves"][key] = {"state": "not_run_deadline"}
                continue
            try:
                lat, S, owners, areas = build[arm](ns, nc)
                r = measure(lat, S, owners, areas)
            except Exception as e:  # noqa: BLE001  a failed solve is recorded and kept, never retried
                r = {"state": "failed", "error": f"{type(e).__name__}: {e}"}
            rec["solves"][key] = r
            solves[(ns, nc)] = r
            if arm == "R0_reproduce_owner07":
                rec["reproduction"] = {k: {"expected": r0[k], "got": rec["solves"][k].get("CL"),
                                           "rel": (rec["solves"][k]["CL"] / r0[k] - 1) if "CL" in rec["solves"][k] else None}
                                       for k in r0 if k in rec["solves"] and "state" not in rec["solves"][k]}
            else:
                rec["classification"] = classify_arm(solves, a.extended)
                if arm in ("A1_elliptic_AR6_dense", "N1_mutant_collocation_quarter_chord"):
                    rec["law_check"] = law_check(solves)
            res["elapsed_s"] = time.monotonic() - t0
            write(a.outdir, res)
        if arm == "R0_reproduce_owner07":
            reps = rec.get("reproduction", {})
            rec["reproduced"] = all(x["rel"] is not None and abs(x["rel"]) <= 1e-12 for x in reps.values()) \
                if len(reps) == len(r0) else None
            if rec["reproduced"] is False:
                res["status"] = "stopped: R0 did not reproduce owner07's values; every decision invalid"
                res["decisions"] = decide(res["arms"], False)
                write(a.outdir, res)
                return 3
    if not a.repair:
        res["decisions_core"] = decide(res["arms"], False)
        if a.extended:
            res["decisions_extended"] = decide(res["arms"], True)
    res["status"] = "complete" if not any(s.get("state") for r in res["arms"].values() for s in r["solves"].values()) \
        else "partial (see solve states)"
    res["elapsed_s"] = time.monotonic() - t0
    write(a.outdir, res)
    print(json.dumps({"status": res["status"], "elapsed_s": round(res["elapsed_s"], 1), **res.get("decisions_core", {})}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
