"""R1: diagnose v3b's VLM non-convergence (CL changes 26% at 1.5x lattice) with a lattice ladder and isolation arms.

    python -m engineering.organ_sims.r1_v3b_convergence VARIANT NS NC        (one lattice, appended to ladder.jsonl)
    python -m engineering.organ_sims.r1_v3b_convergence report               (figure + manifest + checks)
"""
import json, math, sys, time
from pathlib import Path
import numpy as np
from engineering.cfd3d import vlm
from engineering.organ_sims import common as C

RID = "r1-v3b-convergence"
VARS = {"v3a": "fish3d-v3a-fan", "v3b": "fish3d-v3b-glide-pose", "v3c": "fish3d-v3c-daane-length"}
ARMS = {"all": vlm.PAIRED, "pectoral_only": ("pectoral_L", "pectoral_R"), "pelvic_only": ("pelvic_L", "pelvic_R"),
        "left_only": ("pectoral_L", "pelvic_L")}
LAD = C.OUT / RID / "ladder.jsonl"
ALPHA = 4.0


def pan(v):
    return f"artifacts/fish3d/{VARS[v]}/panels.json"


def run(v, arm, ns, nc):
    panels = json.loads((C.ROOT / pan(v)).read_text())["fins"]
    lats, geos = {}, {}
    for f in ARMS[arm]:
        lats[f], geos[f] = vlm.fin_setup(panels[f], ns, nc)
    allp = vlm.combine(lats)
    t = time.time()
    _, F, _, _ = vlm.solve(allp, ALPHA)
    a = math.radians(ALPHA)
    S = float(allp["area"].sum())
    ld = np.array([-math.sin(a), 0, math.cos(a)])
    o = np.array(allp["owner"])
    row = {"variant": v, "arm": arm, "ns": ns, "nc": nc, "panels": int(len(allp["area"])), "S_lattice_m2": S,
           "CL": float(F.sum(0) @ ld / (0.5 * S)), "lift_N_per_q": {f: float(F[o == f].sum(0) @ ld) for f in ARMS[arm]},
           "solve_s": time.time() - t}
    # nearest approach of any collocation point to a trailing leg of a different fin (wake proximity)
    d = {}
    for f in ARMS[arm]:
        P = lats[f]["C"]
        others = [g for g in ARMS[arm] if g != f]
        if not others:
            continue
        A = np.vstack([lats[g]["A"] for g in others]); B = np.vstack([lats[g]["B"] for g in others])
        m = np.inf
        for end in (A, B):
            dy = P[:, None, 1] - end[None, :, 1]; dz = P[:, None, 2] - end[None, :, 2]
            ahead = P[:, None, 0] > end[None, :, 0]               # collocation point is downstream of the leg origin
            r = np.where(ahead, np.hypot(dy, dz), np.inf)
            m = min(m, float(r.min()))
        d[f] = m
    row["min_dist_to_other_fin_trailing_leg_m"] = d
    return row


def report():
    rows = [json.loads(l) for l in LAD.read_text().splitlines()]
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    series = {}
    for r in rows:
        series.setdefault((r["variant"], r["arm"]), []).append(r)
    for (v, arm), rs in sorted(series.items()):
        rs.sort(key=lambda r: r["panels"])
        ax[0].plot([r["panels"] for r in rs], [r["CL"] for r in rs], "o-", label=f"{v} {arm}")
    ax[0].set_xscale("log"); ax[0].set_xlabel("panels"); ax[0].set_ylabel("CL (alpha 4 deg, S_lattice)"); ax[0].legend(fontsize=6)
    ax[0].set_title("VLM lattice ladder (simulated)")
    for v in ("v3a", "v3b", "v3c"):
        rs = sorted(series.get((v, "all"), []), key=lambda r: r["panels"])
        ax[1].plot([r["panels"] for r in rs], [min(r["min_dist_to_other_fin_trailing_leg_m"].values()) * 1e3 for r in rs], "o-", label=v)
    ax[1].set_xscale("log"); ax[1].set_yscale("log"); ax[1].set_xlabel("panels"); ax[1].set_ylabel("min collocation-to-foreign-trailing-leg distance, mm")
    ax[1].legend(); ax[1].set_title("wake proximity")
    fig.tight_layout(); fp = C.OUT / RID / "ladder.png"; fig.savefig(fp, dpi=110)

    def last_two(v, arm):
        rs = sorted(series[(v, arm)], key=lambda r: r["panels"])
        return rs
    summary = {}
    for (v, arm), rs in sorted(series.items()):
        rs.sort(key=lambda r: r["panels"])
        cl = [r["CL"] for r in rs]
        summary[f"{v}/{arm}"] = {"lattices": [[r["ns"], r["nc"]] for r in rs], "CL": cl,
                                 "rel_change_last_step": abs(cl[-1] / cl[-2] - 1) if len(cl) > 1 else None,
                                 "rel_change_each_step": [abs(cl[i + 1] / cl[i] - 1) for i in range(len(cl) - 1)]}
    checks = []
    for v in ("v3a", "v3c"):
        s = summary[f"{v}/all"]
        checks.append({"name": f"{v} converged: last-step CL change <= 5% (control, must hold)", "pass": s["rel_change_last_step"] <= 0.05, "detail": s["rel_change_last_step"]})
    s = summary["v3b/all"]
    checks.append({"name": "v3b CL ladder finite", "pass": all(math.isfinite(x) for x in s["CL"]), "detail": s["CL"]})
    # a variant is declared converged only if the last two steps both change <5% and shrink
    ch = s["rel_change_each_step"]
    conv = len(ch) >= 2 and ch[-1] <= 0.05 and ch[-1] < ch[-2]
    checks.append({"name": "v3b reaches 5% last-step change (recorded either way; failing here is a finding, not an error)", "pass": True, "detail": {"converged": conv, "steps": ch}})
    C.manifest(RID, "v3b VLM non-convergence diagnosis: lattice ladder and isolation arms",
               [pan(v) for v in VARS] + ["engineering/cfd3d/vlm.py"], {"ladder": rows, "summary": summary, "v3b_converged": conv},
               checks, {"note": "filled by analysis"}, seed=None, figures=[f"artifacts/organ-sims/{RID}/ladder.png"])
    print(json.dumps(summary, indent=1))
    C.enforce(checks)


# ---------------------------------------------------------------- v2: collocation-placement defect and corrected lattice
LATTICES2 = [(24, 8), (36, 12), (48, 16), (24, 16), (24, 24), (48, 8), (48, 24), (72, 24)]


def lattice_consistent(poly_uw, origin, e_u, e_w, n_up, ns=20, nc=6, normal_fn=None, colloc=0.75):
    """vlm.lattice with ONE change: the collocation point is the bilinear point of the panel's own corners (mid-span,
    `colloc` chord fraction between the panel's leading and trailing edges at both span edges). vlm.lattice instead uses
    the polygon chord at mid-span (`cm`), which on a curved outline can lie outside the panel, even upstream of its own
    bound vortex, and the mismatch grows as panels shrink chordwise."""
    lat = _ORIG_LATTICE(poly_uw, origin, e_u, e_w, n_up, ns, nc, normal_fn=None, colloc=colloc)
    uw = lat["uw"]
    u = 0.5 * (uw[:, 0, 0] + uw[:, 1, 0])
    w = 0.5 * ((uw[:, 0, 1] + colloc * (uw[:, 3, 1] - uw[:, 0, 1])) + (uw[:, 1, 1] + colloc * (uw[:, 2, 1] - uw[:, 1, 1])))
    lat["C"] = origin + u[:, None] * e_u + w[:, None] * e_w
    if normal_fn is not None:
        lat["N"] = np.array([normal_fn(ui, wi, colloc) for ui, wi in zip(u, w)])
    return lat


_ORIG_LATTICE = vlm.lattice


def colloc_fraction(lat, geo):
    uw = lat["uw"]
    cw = (lat["C"] - geo["O"]) @ geo["ew"]
    le = 0.5 * (uw[:, 0, 1] + uw[:, 1, 1]); te = 0.5 * (uw[:, 2, 1] + uw[:, 3, 1])
    return (cw - le) / (te - le)


def setup(fin, ns, nc, rule):
    vlm.lattice = lattice_consistent if rule == "consistent" else _ORIG_LATTICE
    try:
        return vlm.fin_setup(fin, ns, nc)
    finally:
        vlm.lattice = _ORIG_LATTICE


def run2(v, ns, nc, rule, normals, alphas=(0.0, 4.0)):
    panels = json.loads((C.ROOT / pan(v)).read_text())["fins"]
    lats, fr = {}, []
    for f in vlm.PAIRED:
        lat, geo = setup(panels[f], ns, nc, rule)
        if normals == "flat":
            lat["N"] = np.tile(geo["n_up"], (len(lat["C"]), 1))
        fr.append(colloc_fraction(lat, geo))
        lats[f] = lat
    fr = np.concatenate(fr)
    allp = vlm.combine(lats); o = np.array(allp["owner"]); S = float(allp["area"].sum())
    row = {"variant": v, "ns": ns, "nc": nc, "panels": int(len(o)), "rule": rule, "normals": normals, "S_lattice_m2": S,
           "colloc_fraction_min": float(fr.min()), "colloc_fraction_max": float(fr.max()),
           "n_colloc_upstream_of_own_bound_vortex": int((fr < 0.25).sum()), "n_colloc_outside_panel": int(((fr < 0) | (fr > 1)).sum())}
    t = time.time()
    for a_ in alphas:
        _, F, _, _ = vlm.solve(allp, a_)
        a = math.radians(a_); ld = np.array([-math.sin(a), 0, math.cos(a)])
        row[f"CL_a{a_:g}"] = float(F.sum(0) @ ld / (0.5 * S))
        row[f"lift_share_pectoral_a{a_:g}"] = float(sum(F[o == f].sum(0) @ ld for f in ("pectoral_L", "pectoral_R")) / (F.sum(0) @ ld))
    row["solve_s"] = time.time() - t
    return row


def lad2(v):
    return C.OUT / RID / f"ladder2-{v}.jsonl"


def ladder2(v):
    done = set()
    LAD = lad2(v)
    if LAD.exists():
        done = {(r["variant"], r["ns"], r["nc"], r["rule"], r["normals"]) for r in map(json.loads, LAD.read_text().splitlines())}
    for ns, nc in LATTICES2:
        for rule in ("original", "consistent"):
            for normals in ("source", "flat"):
                if (v, ns, nc, rule, normals) in done:
                    continue
                r = run2(v, ns, nc, rule, normals)
                with LAD.open("a") as fh:
                    fh.write(json.dumps(r) + "\n")
                print(json.dumps({k: r[k] for k in ("variant", "ns", "nc", "rule", "normals", "CL_a4", "CL_a0", "n_colloc_outside_panel", "solve_s")}), flush=True)


def pose_decomposition(v="v3b", nbins=7):
    """Split the source mid-surface's out-of-plane shape into a per-strip chord slope (local incidence; + = trailing edge
    UP = nose-down local incidence) and a quadratic camber/chord, by least squares over the quad corners in spanwise bins
    (argon review #3: incidence vs camber)."""
    fin = json.loads((C.ROOT / pan(v)).read_text())["fins"]["pectoral_L"]
    _, geo = vlm.fin_setup(fin, 24, 8)
    Q = geo["quads"].reshape(-1, 3)
    u = (Q - geo["O"]) @ geo["eu"]; w = (Q - geo["O"]) @ geo["ew"]; z = (Q - geo["O"]) @ geo["n_up"]
    bins = np.linspace(u.min(), u.max(), nbins + 1)
    out = []
    for a, b in zip(bins, bins[1:]):
        m = (u >= a) & (u <= b)
        if m.sum() < 6:
            continue
        c2 = np.polyfit(w[m], z[m], 2); c1 = np.polyfit(w[m], z[m], 1); ch = float(np.ptp(w[m]))
        out.append({"u_mm": [float(a * 1e3), float(b * 1e3)], "chord_slope_deg_TE_up_positive": float(np.degrees(np.arctan(c1[0]))),
                    "camber_over_chord": float(-c2[0] * ch * ch / 4 / ch)})
    return out


def report2():
    rows = [json.loads(l) for v in VARS for l in lad2(v).read_text().splitlines()]
    old = [json.loads(l) for l in LAD.read_text().splitlines()]
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    get = lambda v, rule, nm, ns, nc: next((r for r in rows if r["variant"] == v and r["rule"] == rule and r["normals"] == nm and r["ns"] == ns and r["nc"] == nc), None)
    diag = [(24, 8), (36, 12), (48, 16), (72, 24)]
    summ, checks = {}, []
    for v in VARS:
        for rule in ("original", "consistent"):
            for nm in ("source", "flat"):
                d = [get(v, rule, nm, *l) for l in diag]
                d = [r for r in d if r]
                cl = [r["CL_a4"] for r in d]
                ncs = [get(v, rule, nm, 24, nc) for nc in (8, 16, 24)]
                summ[f"{v}/{rule}/{nm}"] = {
                    "diagonal_lattices": [[r["ns"], r["nc"]] for r in d], "diagonal_CL_a4": cl,
                    "diagonal_rel_steps": [abs(cl[i + 1] / cl[i] - 1) for i in range(len(cl) - 1)],
                    "ns24_nc_8_16_24_CL_a4": [r and r["CL_a4"] for r in ncs],
                    "nc_sensitivity_ns24": (max(r["CL_a4"] for r in ncs if r) / min(r["CL_a4"] for r in ncs if r) - 1) if all(ncs) else None,
                    "CL_a0_finest": d[-1]["CL_a0"], "max_colloc_outside_panel": max(r["n_colloc_outside_panel"] for r in d)}
    # controls
    for o in old:
        r = get(o["variant"], "original", "source", o["ns"], o["nc"])
        if r:
            checks.append({"name": f"control: predecessor ladder reproduced ({o['variant']} {o['ns']}x{o['nc']}) to 1e-9", "pass": abs(r["CL_a4"] - o["CL"]) < 1e-9, "detail": [r["CL_a4"], o["CL"]]})
    checks.append({"name": "control: consistent rule puts every collocation point at 0.75 chord of its own panel", "pass": all(r["n_colloc_outside_panel"] == 0 and abs(r["colloc_fraction_min"] - 0.75) < 1e-6 and abs(r["colloc_fraction_max"] - 0.75) < 1e-6 for r in rows if r["rule"] == "consistent"), "detail": None})
    pa = pose_decomposition("v3a")
    checks.append({"name": "control: pose decomposition of planar v3a gives 0 slope and 0 camber (1e-6)", "pass": all(abs(x["chord_slope_deg_TE_up_positive"]) < 1e-6 and abs(x["camber_over_chord"]) < 1e-6 for x in pa), "detail": pa})
    checks.append({"name": "control: flat-normal arms give CL(alpha=0) = 0 exactly (no camber)", "pass": all(abs(r["CL_a0"]) < 1e-12 for r in rows if r["normals"] == "flat"), "detail": None})
    ctl = json.loads((C.ROOT / "artifacts/cfd3d/vlm/controls.json").read_text())
    checks.append({"name": "control: committed VLM analytic controls (elliptic AR6/AR20, camber, symmetry) all pass in the record", "pass": bool(ctl.get("all_pass", ctl.get("controls", {}).get("all_pass"))), "detail": "artifacts/cfd3d/vlm/controls.json"})
    # findings, gated
    s = summ["v3b/original/source"]
    checks.append({"name": "finding reproduced: v3b committed-lattice diagonal ladder changes > 5% per step", "pass": max(s["diagonal_rel_steps"]) > 0.05, "detail": s["diagonal_rel_steps"]})
    for v in VARS:
        c = summ[f"{v}/consistent/source"]
        checks.append({"name": f"{v}: consistent lattice converges (last diagonal step <= 2%, ns24 nc-sensitivity <= 1%)", "pass": c["diagonal_rel_steps"][-1] <= 0.02 and c["nc_sensitivity_ns24"] <= 0.01, "detail": c})
    # figure
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    for i, v in enumerate(VARS):
        for rule, ls in (("original", "--"), ("consistent", "-")):
            for nm, mk in (("source", "o"), ("flat", "s")):
                d = summ[f"{v}/{rule}/{nm}"]
                ax[0].plot([a * b * 4 for a, b in d["diagonal_lattices"]], d["diagonal_CL_a4"], ls + mk, color=f"C{i}", ms=4, label=f"{v} {rule} {nm}")
                ax[1].plot([8, 16, 24], d["ns24_nc_8_16_24_CL_a4"], ls + mk, color=f"C{i}", ms=4)
    ax[0].set_xscale("log"); ax[0].set_xlabel("panels (diagonal ladder)"); ax[0].set_ylabel("CL, alpha 4 deg"); ax[0].legend(fontsize=5, ncol=2)
    ax[0].set_title("VLM ladder: dashed committed lattice, solid consistent")
    ax[1].set_xlabel("chordwise panels nc (ns = 24)"); ax[1].set_title("chordwise-only refinement")
    lat, geo = setup(json.loads((C.ROOT / pan("v3b")).read_text())["fins"]["pectoral_L"], 24, 24, "original")
    fr = colloc_fraction(lat, geo)
    uw = lat["uw"]
    for k in range(len(uw)):
        q = np.vstack([uw[k], uw[k][:1]])
        ax[2].plot(q[:, 0] * 1e3, q[:, 1] * 1e3, color="0.8", lw=0.3)
    cu = (lat["C"] - geo["O"]) @ geo["eu"]; cw = (lat["C"] - geo["O"]) @ geo["ew"]
    bad = (fr < 0) | (fr > 1)
    ax[2].scatter(cu[~bad] * 1e3, cw[~bad] * 1e3, s=1, c="C0"); ax[2].scatter(cu[bad] * 1e3, cw[bad] * 1e3, s=8, c="r", label=f"{bad.sum()} collocation pts outside own panel")
    ax[2].invert_yaxis(); ax[2].set_aspect("equal"); ax[2].set_xlabel("span u, mm"); ax[2].set_ylabel("chord w, mm (flow down)"); ax[2].legend(fontsize=7)
    ax[2].set_title("v3b pectoral, committed lattice 24x24")
    fig.tight_layout(); fp = C.OUT / RID / "ladder2.png"; fig.savefig(fp, dpi=110)
    C.manifest(RID, "v3b VLM non-convergence diagnosis: collocation-placement defect, corrected lattice, camber effect",
               [pan(v) for v in VARS] + ["engineering/cfd3d/vlm.py", "artifacts/cfd3d/vlm/controls.json"],
               {"summary": summ, "rows": rows, "predecessor_ladder": old, "v3b_pose_decomposition": pose_decomposition("v3b"),
                "v3a_pose_decomposition_control": pose_decomposition("v3a"),
                "diagnosis": "vlm.lattice places each collocation point on the polygon chord at mid-span (cm) while bound vortices use the "
                             "panel-edge chords; on curved outlines the point leaves its panel (up to ~2 chords upstream at nc=24). Errors grow with "
                             "chordwise refinement, so CL drifts with nc for every variant; v3b's diagonal ladder looked worst because its cambered "
                             "(glide-pose) normals add an alpha-independent term that the misplaced points sample differently at each lattice."},
               checks, {"see": "docs/organ-sims.md"}, seed=None, figures=[f"artifacts/organ-sims/{RID}/ladder.png", f"artifacts/organ-sims/{RID}/ladder2.png"])
    print(json.dumps({k: {a: b for a, b in v.items() if a in ("diagonal_CL_a4", "diagonal_rel_steps", "nc_sensitivity_ns24", "CL_a0_finest")} for k, v in summ.items()}, indent=1))
    C.enforce(checks)


if __name__ == "__main__":
    if sys.argv[1] == "report":
        report()
    elif sys.argv[1] == "ladder2":
        ladder2(sys.argv[2])
    elif sys.argv[1] == "report2":
        report2()
    else:
        v, arm, ns, nc = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        LAD.parent.mkdir(parents=True, exist_ok=True)
        r = run(v, arm, ns, nc)
        with LAD.open("a") as fh:
            fh.write(json.dumps(r) + "\n")
        print(json.dumps({k: r[k] for k in ("variant", "arm", "ns", "nc", "CL", "solve_s")}))
