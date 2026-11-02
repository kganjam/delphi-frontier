#!/usr/bin/env python3
"""Grid refinement on PARITY-MATCHED grids, run locally, one at a time.

Series A, travelling: outer envelope fixed at 50 x 30 x 30 mm.
    (nx,ny,nz,voxel) = (5,3,3,10mm) (10,6,6,5mm) (15,9,9,3.333mm) (20,12,12,2.5mm)
    The travelling phase field is 2*pi*x/nx, a function of fractional position
    along the body, so it is identical on every grid by construction.

Series B, longitudinal: outer envelope fixed at 40 x 30 x 30 mm, EVEN nx only.
    (nx,ny,nz,voxel) = (4,3,3,10mm) (8,6,6,5mm) (12,9,9,3.333mm) (16,12,12,2.5mm)
    The split at index nx/2 then falls at the SAME PHYSICAL PLANE, x = 20 mm, on
    every grid: 2*10 = 4*5 = 6*3.333 = 8*2.5 mm. The artifact's own refinement
    went 5 -> 10, which moves the split from 20 mm to 25 mm AND flips its parity,
    which is the confound its post-hoc identified. This series removes it.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_voxelyze as R

LEVELS = [
    ("A1", "travelling", 5, 3, 3, 0.01), ("A2", "travelling", 10, 6, 6, 0.005),
    ("A3", "travelling", 15, 9, 9, 1.0 / 300.0), ("A4", "travelling", 20, 12, 12, 0.0025),
    ("B1", "longitudinal", 4, 3, 3, 0.01), ("B2", "longitudinal", 8, 6, 6, 0.005),
    ("B3", "longitudinal", 12, 9, 9, 1.0 / 300.0), ("B4", "longitudinal", 16, 12, 12, 0.0025),
]
only = sys.argv[1:] or [t for t, *_ in LEVELS]
out = {}
path = "/data/scratch/designspaces/xenobot/data/refine_local.json"
if os.path.exists(path):
    out = json.load(open(path))
for tag, pat, nx, ny, nz, vox in LEVELS:
    if tag not in only or tag in out:
        continue
    t0 = time.time()
    d = R.run(pattern=pat, nx=nx, ny=ny, nz=nz, voxel=vox, timeout=14400)
    p, r, n = d["params"], d["result"], d["numerics"]
    out[tag] = {"tag": tag, "pattern": pat, "nx": nx, "ny": ny, "nz": nz,
                "voxel_m": vox, "voxels": nx * ny * nz,
                "outer_envelope_m": [nx * vox, ny * vox, nz * vox],
                "centre_span_m": (nx - 1) * vox,
                "net_disp_m": r["net_disp_m"], "net_dx_m": r["net_dx_m"],
                "net_dy_m": r["net_dy_m"], "path_len_m": r["path_len_m"],
                "stored_body_lengths": r["disp_in_body_lengths"],
                "disp_over_outer_envelope": r["net_disp_m"] / (nx * vox),
                "dt_s": n["dt_s"], "steps": n["steps_settle"] + n["steps_measure"],
                "diverged": n["diverged"], "wall_s": round(time.time() - t0, 1),
                "cached": d.get("_cached", False)}
    json.dump(out, open(path, "w"), indent=2)
    print(f"{tag} {pat} {nx}x{ny}x{nz} s={vox*1000:.3f}mm N={nx*ny*nz} "
          f"net={r['net_disp_m']*1000:.6f} mm  env_norm={out[tag]['disp_over_outer_envelope']:.6f} "
          f"wall={out[tag]['wall_s']}s", flush=True)
print("done")
