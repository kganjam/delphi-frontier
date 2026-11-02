#!/usr/bin/env python3
"""Locate the travelling-wave optimum frequency as a function of body length.

The 8-point frequency map put the optimum for nx=7 and nx=8 AT the lowest
sampled frequency, which is a boundary and not an optimum. This arm extends the
range downward so the optimum is interior, and tests the physical signature of a
gait-length resonance: if the optimum sits at a fixed WAVE SPEED, then
f_opt * L should be constant.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_voxelyze as R

FREQS = (0.25, 0.375, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0)
NXS = (4, 5, 6, 7, 8, 10, 12)
out = {"freqs": FREQS, "data": {}}
t0 = time.time()
for pat in ("travelling", "longitudinal"):
    out["data"][pat] = {}
    for nx in NXS:
        row = {}
        for f in FREQS:
            d = R.run(pattern=pat, nx=nx, ny=3, nz=3, voxel=0.01, freq=f,
                      measure=5.0 / f)
            row[str(f)] = R.bl(d)
        out["data"][pat][str(nx)] = row
        best = max(row, key=lambda k: row[k])
        print(f"{pat:13s} nx={nx:2d} L={(nx-1)*0.01:.2f}m  f_opt={best:>6s}Hz "
              f"max={row[best]:.6f}  f_opt*L={float(best)*(nx-1)*0.01:.5f}", flush=True)
out["wall_s"] = round(time.time() - t0, 1)
with open("/data/scratch/designspaces/xenobot/data/freqopt.json", "w") as fh:
    json.dump(out, fh, indent=2)
print("done", out["wall_s"], "s")
