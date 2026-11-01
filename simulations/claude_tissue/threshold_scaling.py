"""Edge-speed threshold for ray-like stripes vs rate scale gamma (b=0.9, d=10), from collected GPU results:
gamma=0.5 and 2 from claude-tissue-edge2d-gamma; gamma=1 pooled from claude-tissue-edge2d and claude-tissue-edge2d-cases.
Threshold = edge speed where mean orientation A crosses a level (0 and 0.5), by linear interpolation (4 seeds/point).
Hypothesis: v* scales with lambda*sigma_max ~ sqrt(gamma) (outgrowth racing pattern formation).  Derived numbers only."""
import json, sys, time, pathlib, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt

A = ROOT/"artifacts/simulations"; OUT = A/"claude-tissue-edge2d-gamma"
INPUTS = ["artifacts/simulations/claude-tissue-edge2d-gamma/edge2d_gamma.json", "artifacts/simulations/claude-tissue-edge2d/edge2d.json",
          "artifacts/simulations/claude-tissue-edge2d-cases/edge2d_cases.json"]

def cross(pts, level):
    sp = sorted(pts); a = [pts[s] for s in sp]
    for (s0, a0), (s1, a1) in zip(zip(sp, a), zip(sp[1:], a[1:])):
        if a0 >= level > a1: return s0 + (a0 - level)*(s1 - s0)/(a0 - a1)
    return None

if __name__ == "__main__":
    t0 = time.time(); g, e, c = (json.loads((ROOT/p).read_text())["summary"] for p in INPUTS)
    pts = {0.5: {}, 1.0: {}, 2.0: {}}
    for v in g.values(): pts[v["b"]][v["speed"]] = v["orientation_A_mean"]
    for v in e.values():
        if v["d"] == 10 and v["speed"] > 0: pts[1.0][v["speed"]] = v["orientation_A_mean"]
    for v in c.values():
        if v["b"] == 0.9 and v["d"] == 10 and v["speed"] > 0: pts[1.0][v["speed"]] = v["orientation_A_mean"]
    th = {str(G): dict(points={str(k): v for k, v in sorted(p.items())}, v_A0=cross(p, 0.0), v_A05=cross(p, 0.5)) for G, p in pts.items()}
    G = np.log([0.5, 1.0, 2.0]); v0 = np.log([th[k]["v_A0"] for k in ("0.5", "1.0", "2.0")]); v5 = np.log([th[k]["v_A05"] for k in ("0.5", "1.0", "2.0")])
    out = dict(method="linear interpolation of mean orientation A vs edge speed; 4 seeds per point", thresholds=th,
               loglog_slope_vA0_vs_gamma=float(np.polyfit(G, v0, 1)[0]), loglog_slope_vA05_vs_gamma=float(np.polyfit(G, v5, 1)[0]),
               predicted_slope_if_v_star_scales_with_lambda_sigma=0.5,
               caveat="Few speeds per gamma and 4 seeds; gamma=2 points near 0.2 have SD ~0.5, so the A=0.5 crossing is poorly determined.")
    p = OUT/"threshold-scaling.json"; p.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("loglog_slope_vA0_vs_gamma", "loglog_slope_vA05_vs_gamma")}))
    write_receipt(OUT, "claude-tissue-threshold-scaling", "python3 simulations/claude_tissue/threshold_scaling.py", "none (derived)", INPUTS, [p], t0)
