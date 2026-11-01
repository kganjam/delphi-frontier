"""R1b: test R1's proposed v3b design change.  Rebuild the v3b fins in-process with the committed builder
(engineering.fishv3.build) under altered pose knobs and solve the corrected-collocation VLM ladder.

    python -m engineering.organ_sims.r1b_v3b_fix [workers]

Variants (all other knobs = v3b): camber x{1 (control), 0.5, 0, -0.5, -1} on pectoral and pelvic camber together; and
camber x1 with v3a's lead angles (8/22 deg instead of 16/30) to test whether the sweep turns ray-wise camber into washout.
Lattices 48x16 and 72x24 (consistent collocation, source normals), alpha 0 and 4 deg.
Controls: the camber-x1 rebuild reproduces the committed v3b panels.json exactly, and its 72x24 CL equals R1's
(0.16195).  Simulated (inviscid thin-surface VLM), not observed.
"""
import json, math, sys, time
import numpy as np
from engineering.cfd3d import vlm
from engineering.organ_sims import common as C
from engineering.organ_sims import r1_v3b_convergence as R1

RID = "r1b-v3b-fix"
SCALES_C = (1.0, 0.5, 0.0, -0.5, -1.0)
LATS = ((48, 16), (72, 24))
import os
if os.environ.get("R1B_SMOKE"):          # pipeline smoke test only
    SCALES_C, LATS = (1.0, 0.0), ((24, 8),)


def variants():
    out = {f"camber_x{c:g}": {"pectoral_camber": 0.06 * c, "pelvic_camber": 0.04 * c} for c in SCALES_C}
    out["camber_x1_v3a_lead"] = {"pectoral_camber": 0.06, "pelvic_camber": 0.04, "pectoral_lead_angle_deg": 8.0, "pelvic_lead_angle_deg": 22.0}
    return out


def build_panels(knobs):
    from engineering.fishv3 import build as B
    c = B.candidate("b-glide-pose")
    for k, v in knobs.items():
        c["knobs"][k]["value"] = v
    comps, rep, fans, srec, body = B.build_components(c)
    return B.panels_json(fans, B.v(c["numerical"]["panel_chordwise"]))


def solve(args):
    name, knobs, ns, nc = args
    fins = build_panels(knobs)
    lats = {}
    for f in vlm.PAIRED:
        lat, geo = R1.setup(fins[f], ns, nc, "consistent")
        lats[f] = lat
    allp = vlm.combine(lats); S = float(allp["area"].sum())
    row = {"variant": name, "knobs": knobs, "ns": ns, "nc": nc, "S_lattice_m2": S}
    for a_ in (0.0, 4.0):
        _, F, _, _ = vlm.solve(allp, a_)
        a = math.radians(a_); ld = np.array([-math.sin(a), 0, math.cos(a)])
        row[f"CL_a{a_:g}"] = float(F.sum(0) @ ld / (0.5 * S))
    row["CLa_per_deg"] = (row["CL_a4"] - row["CL_a0"]) / 4
    row["alpha_zero_lift_deg"] = -row["CL_a0"] / row["CLa_per_deg"]
    return row


def pose(knobs):
    fins = build_panels(knobs)
    _, geo = vlm.fin_setup(fins["pectoral_L"], 24, 8)
    Q = geo["quads"].reshape(-1, 3)
    u = (Q - geo["O"]) @ geo["eu"]; w = (Q - geo["O"]) @ geo["ew"]; z = (Q - geo["O"]) @ geo["n_up"]
    bins = np.linspace(u.min(), u.max(), 8)
    res = []
    for a, b in zip(bins, bins[1:]):
        m = (u >= a) & (u <= b)
        c1 = np.polyfit(w[m], z[m], 1); c2 = np.polyfit(w[m], z[m], 2); ch = float(np.ptp(w[m]))
        res.append({"u_mm": [float(a * 1e3), float(b * 1e3)], "chord_slope_deg_TE_up_positive": float(np.degrees(np.arctan(c1[0]))), "camber_over_chord": float(-c2[0] * ch / 4)})
    return res


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    t0 = time.time()
    V = variants()
    jobs = [(n, k, ns, nc) for (ns, nc) in LATS for n, k in V.items()]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(workers) as ex:
        rows = list(ex.map(solve, jobs))
    checks = []
    ref = json.loads((C.ROOT / "artifacts/fish3d/fish3d-v3b-glide-pose/panels.json").read_text())["fins"]
    rb = build_panels(V["camber_x1"])
    md = max(float(np.abs(np.array(rb[f]["quads_m"]) - np.array(ref[f]["quads_m"])).max()) for f in ref)
    checks.append({"name": "control: in-process rebuild of v3b (camber x1) reproduces committed panels.json exactly", "pass": md == 0.0, "detail": md})
    r1 = json.loads((C.ROOT / "artifacts/organ-sims/r1-v3b-convergence/manifest.json").read_text())["results"]["rows"]
    for (ns, nc) in LATS:
        mine = [r for r in rows if r["variant"] == "camber_x1" and r["ns"] == ns and r["nc"] == nc][0]
        theirs = [r for r in r1 if r["variant"] == "v3b" and r["rule"] == "consistent" and r["normals"] == "source" and r["ns"] == ns and r["nc"] == nc]
        if theirs:
            checks.append({"name": f"control: camber x1 at {ns}x{nc} reproduces R1 CL(4) (1e-9)", "pass": abs(mine["CL_a4"] - theirs[0]["CL_a4"]) < 1e-9, "detail": [mine["CL_a4"], theirs[0]["CL_a4"]]})
    conv = {}
    if len(LATS) > 1:
        for n in V:
            a, b = [[r for r in rows if r["variant"] == n and (r["ns"], r["nc"]) == L][0] for L in LATS]
            conv[n] = abs(b["CL_a4"] / a["CL_a4"] - 1)
        checks.append({"name": "every variant: CL(4) changes <= 2% from 48x16 to 72x24", "pass": all(v <= 0.02 for v in conv.values()), "detail": conv})
    poses = {n: pose(k) for n, k in V.items()}
    figs = fig(rows)
    C.manifest(RID, "v3b design-change test: rebuilt fins with altered camber/sweep, corrected-collocation VLM",
               ["artifacts/fish3d/fish3d-v3b-glide-pose/panels.json", "artifacts/organ-sims/r1-v3b-convergence/manifest.json", "engineering/fishv3/build.py", "engineering/cfd3d/vlm.py"],
               {"rows": rows, "pose_decomposition": poses, "convergence_48_to_72": conv, "wall_s": time.time() - t0, "workers": workers},
               checks, {"see": "docs/organ-sims.md"}, seed=None, figures=figs)
    for r in rows:
        print(r["variant"], r["ns"], r["nc"], round(r["CL_a4"], 4), round(r["CL_a0"], 4), round(r["alpha_zero_lift_deg"], 2))
    C.enforce(checks)


def fig(rows):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    L = max((r["ns"], r["nc"]) for r in rows)
    rs = [r for r in rows if (r["ns"], r["nc"]) == L]
    fig, ax = plt.subplots(figsize=(8, 4))
    names = [r["variant"] for r in rs]
    ax.bar(np.arange(len(rs)) - 0.2, [r["CL_a4"] for r in rs], 0.4, label="CL at 4 deg")
    ax.bar(np.arange(len(rs)) + 0.2, [r["CL_a0"] for r in rs], 0.4, label="CL at 0 deg")
    ax.set_xticks(np.arange(len(rs))); ax.set_xticklabels(names, rotation=20, fontsize=7); ax.axhline(0, color="k", lw=0.6)
    ax.set_title(f"v3b pose variants, VLM {L[0]}x{L[1]} consistent collocation (simulated)"); ax.legend()
    fig.tight_layout(); fp = C.OUT / RID / "variants.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/variants.png"]


if __name__ == "__main__":
    main()
