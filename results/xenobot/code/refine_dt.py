#!/usr/bin/env python3
"""Separate temporal from spatial error: repeat the refinement series at HALF the
timestep. If the spatial spread is temporal error in disguise, halving dt at each
level should change the series; if it does not, the spread is spatial."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_voxelyze as R

LEVELS = [("A1", "travelling", 5, 3, 3, 0.01), ("A2", "travelling", 10, 6, 6, 0.005),
          ("A3", "travelling", 15, 9, 9, 1.0 / 300.0),
          ("B1", "longitudinal", 4, 3, 3, 0.01), ("B2", "longitudinal", 8, 6, 6, 0.005),
          ("B3", "longitudinal", 12, 9, 9, 1.0 / 300.0)]
ENV = {"travelling": 0.05, "longitudinal": 0.04}
path = "/data/scratch/designspaces/xenobot/data/refine_dt.json"
out = json.load(open(path)) if os.path.exists(path) else {}
for tag, pat, nx, ny, nz, vox in LEVELS:
    if tag in out:
        continue
    t0 = time.time()
    d = R.run(pattern=pat, nx=nx, ny=ny, nz=nz, voxel=vox, dtScale=0.25, timeout=14400)
    out[tag] = {"tag": tag, "pattern": pat, "nx": nx, "voxel_m": vox, "dtScale": 0.25,
                "net_disp_m": d["result"]["net_disp_m"],
                "normalised_by_outer_envelope": d["result"]["net_disp_m"] / (nx * vox),
                "dt_s": d["numerics"]["dt_s"], "diverged": d["numerics"]["diverged"],
                "wall_s": round(time.time() - t0, 1)}
    json.dump(out, open(path, "w"), indent=2)
    print(f"{tag} dtScale=0.25 net={d['result']['net_disp_m']*1000:.6f} mm "
          f"norm={out[tag]['normalised_by_outer_envelope']:.6f} wall={out[tag]['wall_s']}s", flush=True)
print("done")
