"""Idealised fin section (thin ellipse, thickness ratio 0.12, angle of attack 10 deg) in a box of 20 c x 8 c (PROTOCOL.md C4).
Dimensionless: Re = U c / nu (stability only), lengths in chords, time in convective units t U / c, Cp = (p - p_inf)/(0.5 rho U^2), vorticity omega c / U.
Usage: python3 -m engineering.flow.obstacle run OUTDIR --chord 40 [--device cpu|cuda] [--conv-time 80] [--save-every 400]
       python3 -m engineering.flow.obstacle pilot OUT.json --chord 40 [--device cpu]"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

from .lbm import LBM

U, RE, THICK, AOA_DEG = 0.05, 100.0, 0.12, 10.0


def build(chord, device="cpu"):
    nx, ny = 20 * chord, 8 * chord
    tau = 0.5 + 3 * U * chord / RE
    x = (torch.arange(nx, dtype=torch.float64) + 0.5)[:, None] - 6.0 * chord      # leading region: centre of ellipse at x = 6 c
    y = (torch.arange(ny, dtype=torch.float64) + 0.5)[None, :] - 4.0 * chord
    a = math.radians(AOA_DEG)
    xr = x * math.cos(a) - y * math.sin(a)                                         # nose-up rotation: flow from the left sees positive angle of attack
    yr = x * math.sin(a) + y * math.cos(a)
    solid = (xr / (chord / 2)) ** 2 + (yr / (THICK * chord / 2)) ** 2 <= 1.0
    return nx, ny, tau, solid


def run(out, chord, device="cpu", conv_time=80.0, save_every=400, max_steps=None, quiet=False):
    t0 = time.time()
    nx, ny, tau, solid = build(chord)
    L = LBM(nx, ny, tau, solid=solid, device=device)
    L.set_open(U)
    L.init(1.0, U, 0.0)
    L.f = torch.where(L.solid[None], L.w.expand(9, nx, ny), L.f)
    steps = int(conv_time * chord / U) if max_steps is None else max_steps
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    states, rec = [], []
    ci = nx // 2
    for s in range(1, steps + 1):
        fr = L.step(want_force=(s % 20 == 0))
        if s % 20 == 0:
            fx, fy = fr
            q = 0.5 * 1.0 * U * U * chord
            rho, ux, uy = L.macro()
            fin = float((ux[1, 1:-1] * rho[1, 1:-1]).sum()); fout = float((ux[-2, 1:-1] * rho[-2, 1:-1]).sum())
            rec.append((s, float(fx) / q, float(fy) / q, fin, fout, float(torch.sqrt(ux ** 2 + uy ** 2).max()), bool(torch.isfinite(L.f).all())))
        if s % save_every == 0:
            rho, ux, uy = L.macro()
            states.append((s, rho.cpu().numpy().astype(np.float64), ux.cpu().numpy().astype(np.float64), uy.cpu().numpy().astype(np.float64)))
        if not quiet and s % 5000 == 0:
            print(f"step {s}/{steps} {time.time()-t0:.0f}s", flush=True)
    wall = time.time() - t0
    rec = np.array(rec)
    n = len(rec)
    w1, w2 = rec[int(0.8 * n):int(0.9 * n), 1].mean(), rec[int(0.9 * n):, 1].mean()
    flux_bal = abs(rec[int(0.9 * n):, 3].mean() - rec[int(0.9 * n):, 4].mean()) / rec[int(0.9 * n):, 3].mean()
    res = {"chord_cells": chord, "grid": [nx, ny], "tau": tau, "nu": L.nu, "Re": RE, "U_lattice": U, "steps": steps, "convective_time_total": steps * U / chord,
           "Cd_mean_last10pct": float(rec[int(0.9 * n):, 1].mean()), "Cl_mean_last10pct": float(rec[int(0.9 * n):, 2].mean()),
           "Cd_rel_change_last_two_windows": float(abs(w2 - w1) / abs(w2)), "flux_imbalance_last10pct": float(flux_bal), "max_speed_over_cs_Mach": float(rec[:, 5].max() * math.sqrt(3)),
           "all_finite": bool(rec[:, 6].all()), "steady_by_protocol": bool(abs(w2 - w1) / abs(w2) <= 0.01), "wall_seconds": wall, "device": str(device),
           "seconds_per_step": wall / steps, "torch": torch.__version__, "cuda": torch.cuda.get_device_name(0) if str(device).startswith("cuda") else None}
    res["checks"] = {"flux_balance_le_3pct": bool(flux_bal <= 0.03), "finite": res["all_finite"], "mach_le_0.3": bool(res["max_speed_over_cs_Mach"] <= 0.3), "steady_drag_le_1pct": res["steady_by_protocol"]}
    np.savez_compressed(out / f"states_c{chord}.npz", step=np.array([s[0] for s in states]), rho=np.array([s[1] for s in states]), ux=np.array([s[2] for s in states]), uy=np.array([s[3] for s in states]),
                        solid=solid.cpu().numpy(), force_history=rec, U=U, chord=chord)
    (out / f"result_c{chord}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("chord_cells", "Cd_mean_last10pct", "Cl_mean_last10pct", "flux_imbalance_last10pct", "steady_by_protocol", "wall_seconds", "checks")}))
    return res


if __name__ == "__main__":
    a = sys.argv[1:]
    chord = int(a[a.index("--chord") + 1]); dev = a[a.index("--device") + 1] if "--device" in a else "cpu"
    if a[0] == "pilot":
        t0 = time.time(); r = run(Path(a[1]).parent / "pilot_tmp", chord, dev, max_steps=1000, save_every=1000, quiet=True)
        full_steps = int(80 * chord / U)
        Path(a[1]).write_text(json.dumps({"chord": chord, "device": dev, "pilot_steps": 1000, "seconds_per_step": r["seconds_per_step"], "full_steps_80_convective": full_steps,
                                          "extrapolated_hours": r["seconds_per_step"] * full_steps / 3600}, indent=1))
        print(open(a[1]).read())
    else:
        run(a[1], chord, dev, conv_time=float(a[a.index("--conv-time") + 1]) if "--conv-time" in a else 80.0, save_every=int(a[a.index("--save-every") + 1]) if "--save-every" in a else 400)
