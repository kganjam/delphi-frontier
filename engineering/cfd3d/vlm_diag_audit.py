"""Independent audit of a returned VLM-diagnostic run (vlm_diag_contract.json + vlm_diag_addendum_repair.json).

    python -I engineering/cfd3d/vlm_diag_audit.py RETURN_DIR OUT.json [--local-probe RESULTS.json ...]

Read-only: no VLM solve. It rehashes every collected file against the collection receipt, checks the dispatched
input hashes against this repository's packet manifest, the pins and the solve identities, and re-derives every
family verdict and decision from the contract's own numbers with code written separately from vlm_diag.py
(nothing is imported from it), then compares with the native merged.json. Where local probes ran the same
(ns, nc) points, the returned CL is compared with them.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = json.loads((HERE / "vlm_diag_contract.json").read_text())
ADD = json.loads((HERE / "vlm_diag_addendum_repair.json").read_text())
MAN = json.loads((ROOT / "artifacts/cfd3d/vlm-diag/packet/cfd3d-vlmdiag-packet-manifest.json").read_text())
EPS = 1e-12          # the contract's roundoff rule, read from its text "1e-12"
assert "1e-12" in C["classification"]["triple"]


def h(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def status_of(c1: float, c2: float, c3: float) -> tuple[str, float | None]:
    a, b = c2 - c1, c3 - c2
    if abs(a) <= EPS * abs(c3) and abs(b) <= EPS * abs(c3):
        return "converged_roundoff", None
    if a == 0:
        return "divergent", None
    r = b / a
    if 0 < r < 1:
        return "monotone_convergent", r
    if -1 < r < 0:
        return "oscillatory_convergent", r
    return "divergent", r


def verdict(vals: dict[int, float], decisive, tail) -> str:
    need = {n for t in decisive for n in t} | set(tail)
    if not need <= set(vals):
        return "incomplete"
    good = all(status_of(*(vals[n] for n in t))[0] in ("monotone_convergent", "converged_roundoff") for t in decisive)
    d = [vals[tail[i + 1]] - vals[tail[i]] for i in range(len(tail) - 1)]
    same = all(x > 0 for x in d) or all(x < 0 for x in d) or all(abs(x) <= EPS * abs(vals[tail[-1]]) for x in d)
    return "regular" if good and same else "irregular"


def fams(solves: dict) -> tuple[dict, dict]:
    nc0, ns0 = C["families"]["span"]["nc"], C["families"]["chord"]["ns"]
    span, chord = {}, {}
    for k, r in solves.items():
        if "CL" not in r:
            continue
        ns, nc = map(int, k.split("x"))
        if nc == nc0:
            span[ns] = r["CL"]
        if ns == ns0:
            chord[nc] = r["CL"]
    return span, chord


def arm_verdicts(solves: dict) -> dict:
    span, chord = fams(solves)
    f, e = C["families"], C["execution"]["extended"]["families"]
    out = {"span": verdict(span, f["decisive_triples"]["span"], f["tail"]["span"]),
           "chord": verdict(chord, f["decisive_triples"]["chord"], f["tail"]["chord"]),
           "span_extended": verdict(span, e["span"]["decisive_triples"], e["span"]["tail"]),
           "chord_extended": verdict(chord, e["chord"]["decisive_triples"], e["chord"]["tail"])}
    for tag, (a, b) in (("core", ("span", "chord")), ("extended", ("span_extended", "chord_extended"))):
        v = (out[a], out[b])
        out[f"arm_{tag}"] = "incomplete" if "incomplete" in v else "regular" if v == ("regular", "regular") else "irregular"
    return out


def helmbold_check(solves: dict) -> bool | None:
    ref = 2 * math.pi * 6 / (2 + math.sqrt(40))
    f = C["families"]
    keys = [f"{f['span']['ns'][-1]}x{f['span']['nc']}", f"{f['chord']['ns']}x{f['chord']['nc'][-1]}"]
    if not all("CL" in solves.get(k, {}) for k in keys):
        return None
    return all(abs(solves[k]["CL"] / math.radians(4) / ref - 1) <= 0.03 for k in keys)


def reg(xs) -> bool:
    return all(x == "regular" for x in xs)


def decisions(core: dict, rep: dict, tag: str) -> dict:
    """Contract 'decisions' and addendum 'prediction_and_decision', re-read from their text."""
    V = {a: arm_verdicts(v["solves"]) for a, v in core.items() if a != "R0_reproduce_owner07"}
    R = {a: arm_verdicts(v["solves"]) for a, v in rep.items()}
    k = f"arm_{tag}"
    r0 = core["R0_reproduce_owner07"]["solves"]
    exp = C["arms"][0]["values"]
    r0_ok = all(abs(r0[key]["CL"] / val - 1) <= 1e-12 for key, val in exp.items())
    n1 = V["N1_mutant_collocation_quarter_chord"][k] == "irregular" or \
        helmbold_check(core["N1_mutant_collocation_quarter_chord"]["solves"]) is False
    n2 = V["N2_notched_rectangle"][k] == "irregular"
    smooth = [V[a][k] for a in ("A1_elliptic_AR6_dense", "A2_elliptic_AR4_dense", "A3_rectangle_AR4")]
    samp = {a: V[a][k] for a in ("A4_elliptic_AR4_coarse7", "A4_elliptic_AR4_coarse16", "F1_pectoral_L_isolated",
                                 "F2_pelvic_L_isolated")}
    d = {"R0": r0_ok, "N1_flagged": n1, "N2_flagged": n2}
    d["D_scheme"] = "indicated" if "irregular" in smooth else "not_indicated" if reg(smooth) and n2 else "unknown"
    a1, law = V["A1_elliptic_AR6_dense"][k], helmbold_check(core["A1_elliptic_AR6_dense"]["solves"])
    d["D_law"] = ("indicated" if a1 == "regular" and law is False else
                  "not_indicated_at_3pct" if a1 == "regular" and law is True and n1 else "unknown")
    d["D_sampling"] = ("indicated" if reg(smooth) and "irregular" in samp.values() else
                       "not_indicated" if reg(smooth + list(samp.values())) and n2 else "unknown")
    f12 = [samp["F1_pectoral_L_isolated"], samp["F2_pelvic_L_isolated"]]
    f3 = V["F3_four_fins_combined"][k]
    d["D_interaction"] = ("confounded" if "irregular" in f12 else "indicated" if reg(f12) and f3 == "irregular" else
                          "not_indicated" if reg(f12 + [f3]) and n2 else "unknown")
    # addendum
    fam = "chord_extended" if tag == "extended" else "chord"
    a3c, a3r = core["A3_rectangle_AR4"]["solves"], rep["A3_rectangle_AR4"]["solves"]
    inv = all(abs(a3r[x]["CL"] / a3c[x]["CL"] - 1) <= 1e-12 for x in a3r) and set(a3r) == set(a3c)
    rn2 = R["N2_notched_rectangle"][k] == "irregular"
    ch = [R[a][fam] for a in ("A1_elliptic_AR6_dense", "A2_elliptic_AR4_dense")]
    arms = [R[a][k] for a in ("A1_elliptic_AR6_dense", "A2_elliptic_AR4_dense")]
    d["D_colloc"] = ("invalid" if not inv else "unknown" if not rn2 else "refuted" if "irregular" in ch else
                     "supported" if reg(arms) else "unknown")
    d["addendum_N2_flagged"] = rn2
    d["invariance_rectangle"] = inv
    f12r = {a: (R[a][k], R[a][fam], R[a]["span_extended" if tag == "extended" else "span"])
            for a in ("F1_pectoral_L_isolated", "F2_pelvic_L_isolated")}
    # addendum D_fins_after_repair, applied literally: (arm, chord, span) verdicts of F1 and F2 repaired
    d["D_fins_after_repair_literal"] = (
        "explained_by_H_colloc" if all(v[0] == "regular" for v in f12r.values()) else
        "chord_regular_span_irregular_remainder_attributed_to_outline_sampling_inference"
        if all(v[1] == "regular" for v in f12r.values()) else
        "not_explained_by_H_colloc_chord_families_stay_irregular" if any(v[1] == "irregular" for v in f12r.values())
        else "unknown")
    d["fins_repaired"] = {a: {x: R[a][x] for x in (("span_extended", "chord_extended") if tag == "extended" else ("span", "chord"))}
                          for a in ("F1_pectoral_L_isolated", "F2_pelvic_L_isolated", "F3_four_fins_combined")}
    return d


def main(ret: Path, out: Path, probes: list[Path]) -> dict:
    a: dict = {"schema": "cfd3d-vlm-diag-return-audit-0.1", "return_dir": str(ret), "checks": {}}
    ck = a["checks"]
    rec = json.loads((ret / "collection_receipt.json").read_text())
    rows = rec["artifacts"]
    key = next(k for k in ("sha256", "sha256_hex") if k in rows[0])
    pkey = next(k for k in ("path", "relative_path", "name") if k in rows[0])
    bad = [r[pkey] for r in rows if h(ret / r[pkey]) != r[key]]
    on_disk = sorted(str(p.relative_to(ret)) for p in ret.rglob("*") if p.is_file())
    ck["rehash"] = {"listed": len(rows), "mismatches": bad,
                    "bytes": sum((ret / r[pkey]).stat().st_size for r in rows),
                    "unlisted_on_disk": sorted(set(on_disk) - {r[pkey] for r in rows})}
    disp = json.loads((ret / "dispatch.json").read_text())["spec"]
    man = {r["path"]: r["sha256"] for r in MAN["files"]}
    ck["inputs"] = {"archive_sha256_matches": disp["source_sha256"] == MAN["archive_sha256"],
                    "source_commit_matches": disp["source_commit"].startswith(MAN["head"][:7]) or disp["source_commit"] == MAN["head"],
                    "member_hash_mismatches": [p for p, s in disp["input_sha256"].items() if man.get(p) != s],
                    "members": len(disp["input_sha256"])}
    pins = (ret / "installed-pins.txt").read_text().split()
    sci = ret / "science"
    procs = {p: json.loads((sci / p / "results.json").read_text()) for p in ("core-f3", "repair-f3", "core-rest", "repair-rest")}
    ck["pins"] = {"numpy_2.5.4_installed": "numpy==2.5.4" in pins,
                  "per_process": {p: {"python": r["environment"]["python"], "numpy": r["environment"]["numpy"],
                                      "threads": r["environment"]["threads"],
                                      "vlm_py": r["vlm_py_sha256"] == man["engineering/cfd3d/vlm.py"],
                                      "runner": r["runner_sha256"] == man["engineering/cfd3d/vlm_diag.py"],
                                      "contract": r["contract_sha256"] == man["engineering/cfd3d/vlm_diag_contract.json"],
                                      "panels": r["panels_sha256"] == man["artifacts/fish3d/fish3d-v3a-fan/panels.json"],
                                      "addendum": (r.get("addendum_sha256") in (None, man["engineering/cfd3d/vlm_diag_addendum_repair.json"])),
                                      "mode": r["mode"], "variant": r["variant"], "status": r["status"],
                                      "elapsed_s": r["elapsed_s"]} for p, r in procs.items()}}
    core = {**procs["core-rest"]["arms"], **procs["core-f3"]["arms"]}
    rep = {**procs["repair-rest"]["arms"], **procs["repair-f3"]["arms"]}
    ext_pts = {f"{n}x{C['families']['span']['nc']}" for n in C["families"]["span"]["ns"] + C["execution"]["extended"]["families"]["span"]["ns_add"]} | \
              {f"{C['families']['chord']['ns']}x{n}" for n in C["families"]["chord"]["nc"] + C["execution"]["extended"]["families"]["chord"]["nc_add"]}
    states = {}
    for var, arms in (("core", core), ("repair", rep)):
        for arm, v in arms.items():
            want = set(C["arms"][0]["values"]) if arm == "R0_reproduce_owner07" else ext_pts
            got = set(v["solves"])
            states[f"{var}/{arm}"] = {"solves": len(got), "expected": len(want), "identical_set": got == want,
                                      "non_complete": sorted(k for k, s in v["solves"].items() if "CL" not in s),
                                      "non_finite": sorted(k for k, s in v["solves"].items()
                                                           if "CL" in s and not math.isfinite(s["CL"]))}
    ck["solves"] = {"total": sum(s["solves"] for s in states.values()), "per_arm": states,
                    "core_arms": sorted(core) == sorted(C["arm_order"]), "repair_arms": sorted(rep) == sorted(ADD["repair_variant"]["arms"])}
    r0 = core["R0_reproduce_owner07"]["solves"]
    ck["R0"] = {k: {"expected": v, "returned": r0[k]["CL"], "rel": r0[k]["CL"] / v - 1} for k, v in C["arms"][0]["values"].items()}
    # independent re-derivation vs native merged.json
    merged = json.loads((sci / "merged.json").read_text())
    mine = {"core": decisions(core, rep, "core"), "extended": decisions(core, rep, "extended")}
    nat = {"core": {**merged["decisions_core"], **{k: merged["addendum_core"][k] for k in ("D_colloc", "invariance_rectangle")}},
           "extended": {**merged["decisions_extended"], **{k: merged["addendum_extended"][k] for k in ("D_colloc", "invariance_rectangle")}}}
    agree = {}
    for tag in ("core", "extended"):
        for k in ("N1_flagged", "N2_flagged", "D_scheme", "D_law", "D_sampling", "D_interaction", "D_colloc", "invariance_rectangle"):
            agree[f"{tag}/{k}"] = {"native": nat[tag].get(k), "independent": mine[tag][k], "same": nat[tag].get(k) == mine[tag][k]}
        an = merged[f"addendum_{tag}"]
        agree[f"{tag}/addendum_N2_flagged"] = {"native": an["N2_flagged"], "independent": mine[tag]["addendum_N2_flagged"],
                                               "same": an["N2_flagged"] == mine[tag]["addendum_N2_flagged"]}
        agree[f"{tag}/fins_repaired"] = {"native": an["fins_repaired_by_family"], "independent": mine[tag]["fins_repaired"],
                                         "same": an["fins_repaired_by_family"] == mine[tag]["fins_repaired"]}
    fam_agree = []
    for var, arms in (("core", merged["arms"]["core"]), ("repair", merged["arms"]["repair"])):
        for arm, v in arms.items():
            if arm == "R0_reproduce_owner07":
                continue
            m, n = arm_verdicts(v["solves"]), v["classification"]
            for fk in ("span", "chord", "span_extended", "chord_extended"):
                fam_agree.append(n[fk]["verdict"] == m[fk])
    ck["rederivation"] = {"decisions": agree, "all_decisions_same": all(x["same"] for x in agree.values()),
                          "family_verdicts_compared": len(fam_agree), "family_verdicts_same": sum(fam_agree)}
    ck["merged_arms_equal_process_arms"] = merged["arms"]["core"] == core and merged["arms"]["repair"] == rep
    # cross-host: returned CL vs local probes at shared points
    xs = []
    for p in probes:
        r = json.loads(p.read_text())
        arms = core if r.get("variant", "core") == "core" else rep
        for arm, v in r["arms"].items():
            for k, s in v["solves"].items():
                if "CL" in s and "CL" in arms.get(arm, {}).get("solves", {}).get(k, {}):
                    xs.append(abs(arms[arm]["solves"][k]["CL"] / s["CL"] - 1))
    ck["cross_host_vs_local_probes"] = {"shared_points": len(xs), "max_abs_rel": max(xs) if xs else None,
                                        "bit_identical": sum(x == 0 for x in xs)}
    a["decisions_independent"] = mine
    out.write_text(json.dumps(a, indent=1) + "\n")
    return a


if __name__ == "__main__":
    args = sys.argv[1:]
    probes = [Path(x) for x in args[args.index("--local-probe") + 1:]] if "--local-probe" in args else []
    r = main(Path(args[0]), Path(args[1]), probes)
    c = r["checks"]
    print(json.dumps({"rehash": c["rehash"], "inputs": c["inputs"], "solves_total": c["solves"]["total"],
                      "rederivation_all_same": c["rederivation"]["all_decisions_same"],
                      "families": f'{c["rederivation"]["family_verdicts_same"]}/{c["rederivation"]["family_verdicts_compared"]}',
                      "cross_host": c["cross_host_vs_local_probes"], "merged_equal": c["merged_arms_equal_process_arms"]}, indent=1))
