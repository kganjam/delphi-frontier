"""Summary of the proliferation-zone results (derived numbers only; no new simulation).
Reads the collected claude-tissue-pzone-* JSON files, takes the distal-half orientation A (grown tissue) per zone width,
and defines the switch Lp* as the first upward crossing of A = 0.5 by linear interpolation in Lp.  Refined-grid runs are
in grid units with half cell size: physical Lp = grid Lp / 2, physical v = grid v / 2.  lambda = linear-theory fastest
wavelength 2*pi/k_max for Schnakenberg a=0.1, b=0.9, d=10 (11.14 * gamma^-1/2), as used in the doc tables.
Output: zone-rule.json (all points and switches) and zone-rule.png (Lp*/lambda vs dimensionless speed v/sqrt(gamma))."""
import json, sys, time, pathlib, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt

A = ROOT/"artifacts/simulations"; OUT = A/"claude-tissue-pzone"
LAM1 = 11.14
GROUPS = {   # name: (gamma, physical v, grid, edge, [(dir, kind, scale)])
    "refined, sharp edge, gamma 2, v 0.1": (2.0, 0.1, "refined", "sharp", [("claude-tissue-pzone-refine", "pzone_refine", 0.5), ("claude-tissue-pzone-refine-g2b", "pzone_refine_g2b", 0.5)]),
    "refined, sharp edge, gamma 1, v 0.1": (1.0, 0.1, "refined", "sharp", [("claude-tissue-pzone-refine-g1", "pzone_refine_g1", 0.5)]),
    "refined, sharp edge, gamma 0.5, v 0.1": (0.5, 0.1, "refined", "sharp", [("claude-tissue-pzone-refine-g05", "pzone_refine_g05", 0.5), ("claude-tissue-pzone-refine-g05b", "pzone_refine_g05b", 0.5)]),
    "refined, sharp edge, gamma 1, v 0.4": (1.0, 0.4, "refined", "sharp", [("claude-tissue-pzone-refine-g1v40", "pzone_refine_g1v40", 0.5)]),
    "coarse, sharp edge, gamma 2, v 0.1": (2.0, 0.1, "coarse", "sharp", [("claude-tissue-pzone-g2r", "pzone_g2r", 1.0), ("claude-tissue-pzone-g2f", "pzone_g2f", 1.0)]),
    "coarse, sharp edge, gamma 1, v 0.1": (1.0, 0.1, "coarse", "sharp", [("claude-tissue-pzone-g1r", "pzone_g1r", 1.0), ("claude-tissue-pzone-g1f", "pzone_g1f", 1.0)]),
    "coarse, sharp edge, gamma 0.5, v 0.1": (0.5, 0.1, "coarse", "sharp", [("claude-tissue-pzone-g05r", "pzone_g05r", 1.0), ("claude-tissue-pzone-g05f", "pzone_g05f", 1.0)]),
    "coarse, sharp edge, gamma 1, v 0.25": (1.0, 0.25, "coarse", "sharp", [("claude-tissue-pzone-g1v25", "pzone_g1v25", 1.0)]),
    "coarse, sharp edge, gamma 1, v 0.4": (1.0, 0.4, "coarse", "sharp", [("claude-tissue-pzone-g1v40", "pzone_g1v40", 1.0)]),
    "coarse, sharp edge, gamma 2, v 0.25": (2.0, 0.25, "coarse", "sharp", [("claude-tissue-pzone-g2v25", "pzone_g2v25", 1.0)]),
    "coarse, sharp edge, gamma 2, v 0.4": (2.0, 0.4, "coarse", "sharp", [("claude-tissue-pzone-g2v40", "pzone_g2v40", 1.0)]),
    "coarse, smooth edge (w=1), gamma 1, v 0.1": (1.0, 0.1, "coarse", "smooth1", [("claude-tissue-pzone-smooth", "pzone_smooth", 1.0), ("claude-tissue-pzone-smooth-b", "pzone_smooth_b", 1.0)]),
}

def crossing(pts, level=0.5):
    pts = sorted(pts)
    for (x0, a0), (x1, a1) in zip(pts[:-1], pts[1:]):
        if a0 < level <= a1: return x0 + (level - a0)*(x1 - x0)/(a1 - a0)
    return None

if __name__ == "__main__":
    t0 = time.time(); res = {}; inputs = []
    for name, (g, v, grid, edge, srcs) in GROUPS.items():
        pts = {}
        for d, k, sc in srcs:
            p = A/d/f"{k}.json"
            if not p.exists(): continue
            inputs.append(str(p.relative_to(ROOT)))
            for vv in json.loads(p.read_text())["summary"].values():
                if vv["lp"] is not None and vv["lp"] > 0 and "A_distal_half_mean" in vv:
                    pts[round(vv["lp"]*sc, 4)] = vv["A_distal_half_mean"]
        lam = LAM1/np.sqrt(g); x = crossing(list(pts.items()))
        res[name] = dict(gamma=g, v=v, grid=grid, edge=edge, lambda_linear=float(lam), dimensionless_speed=float(v/np.sqrt(g)),
                         points=sorted(pts.items()), Lp_switch=x, Lp_switch_over_lambda=(float(x/lam) if x else None))
        print(name, x and round(x, 2), x and round(x/lam, 3), flush=True)
    out = dict(definition="Lp* = first upward crossing of distal-half orientation A = 0.5 (linear interpolation); lambda = 11.14/sqrt(gamma)",
               groups=res, caveats=["Brackets are 0.25-1 units wide; values near the switch have wide CIs (see per-run cards).",
                                    "One model family (Schnakenberg), d=10, b=0.9; other kinetics tested separately (claude-tissue-pzone-kin*).",
                                    "Coarse-grid gamma=2 values are biased upward (zone only 2-3 cells)."])
    pj = OUT/"zone-rule.json"; pj.write_text(json.dumps(out, indent=1))
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
    mk = {("refined", "sharp"): ("o", "tab:blue", "refined grid, sharp edge"), ("coarse", "sharp"): ("s", "tab:gray", "coarse grid, sharp edge"),
          ("coarse", "smooth1"): ("^", "tab:green", "coarse grid, smooth edge (width 1)")}
    seen = set()
    for name, r in res.items():
        if r["Lp_switch_over_lambda"] is None: continue
        m, c, lab = mk[(r["grid"], r["edge"])]
        ax[0].scatter(r["dimensionless_speed"], r["Lp_switch_over_lambda"], marker=m, color=c, s=60, label=None if lab in seen else lab); seen.add(lab)
    ax[0].set_xlabel("dimensionless outgrowth speed v / sqrt(gamma)"); ax[0].set_ylabel("zone width at switch, Lp* / lambda")
    ax[0].set_title("SIMULATED: proliferation-zone width needed for ray-like stripes", fontsize=9); ax[0].legend(fontsize=7); ax[0].set_ylim(0, 0.7)
    for name in ["refined, sharp edge, gamma 1, v 0.1", "refined, sharp edge, gamma 1, v 0.4", "coarse, smooth edge (w=1), gamma 1, v 0.1"]:
        r = res[name]
        if r["points"]:
            xs, ys = zip(*r["points"]); ax[1].plot(np.array(xs)/r["lambda_linear"], ys, "o-", label=name)
    ax[1].axhline(0.5, color="gray", ls=":"); ax[1].axhline(0, color="k", lw=0.5)
    ax[1].set_xlabel("zone width Lp / lambda"); ax[1].set_ylabel("orientation A of grown tissue (12 seeds)"); ax[1].legend(fontsize=7)
    ax[1].set_title("switch curves at gamma 1", fontsize=9)
    fig.tight_layout(); pp = OUT/"zone-rule.png"; fig.savefig(pp, dpi=110); plt.close(fig)
    write_receipt(OUT, "claude-tissue-zone-rule-summary", "python3 simulations/claude_tissue/zone_rule_summary.py", "none (derived)", inputs, [pj, pp], t0)
