#!/usr/bin/env python3
"""Cheap Voxelyze sweeps for the convergence study: the fine nx parity sweep and
the nx x frequency map, run for BOTH 'longitudinal' (which the artifact's own
post-hoc diagnosed as parity-confounded) and 'travelling' (whose phase is a
continuous gradient and carries no parity dependence by construction).

That pairing is the discriminator. If the non-monotone nx series is a
gait-length RESONANCE it is a property of the mechanics and must appear in both
patterns, and its favoured nx must move when the drive frequency moves. If it is
the ENCODING, it must appear in longitudinal only and must not move with
frequency.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_voxelyze as R

OUT = "/data/scratch/designspaces/xenobot/data"
BASE = dict(ny=3, nz=3, voxel=0.01, freq=4.0)


def main():
    t0 = time.time()
    out = {"parity_sweep": {}, "freq_nx_map": {}}
    for pat in ("longitudinal", "travelling"):
        out["parity_sweep"][pat] = {}
        for nx in range(3, 17):
            d = R.run(pattern=pat, nx=nx, **BASE)
            out["parity_sweep"][pat][str(nx)] = {
                "body_lengths": R.bl(d), "net_disp_m": R.net_m(d),
                "voxels": nx * 3 * 3, "body_len_m": d["result"]["body_len_m"],
                "diverged": d["numerics"]["diverged"]}
            print(f"parity {pat:12s} nx={nx:2d} {R.bl(d):.6f} BL", flush=True)
    for pat in ("longitudinal", "travelling"):
        out["freq_nx_map"][pat] = {}
        for nx in (4, 5, 6, 7, 8):
            out["freq_nx_map"][pat][str(nx)] = {}
            for f in (1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0):
                kw = dict(BASE); kw["freq"] = f
                # hold the number of CYCLES fixed at 5, not the duration
                kw["measure"] = 5.0 / f
                d = R.run(pattern=pat, nx=nx, **kw)
                out["freq_nx_map"][pat][str(nx)][str(f)] = {
                    "body_lengths": R.bl(d), "net_disp_m": R.net_m(d),
                    "diverged": d["numerics"]["diverged"]}
            print(f"freqmap {pat:12s} nx={nx}", flush=True)
    out["protocol_note"] = ("the frequency sweep holds CYCLES fixed at 5 and lets the "
                            "duration vary as 5/f, so every point is the same number of "
                            "actuation cycles. Holding duration fixed instead would "
                            "confound frequency with cycle count.")
    out["wall_s"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, "sweeps.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote sweeps.json", out["wall_s"], "s")


if __name__ == "__main__":
    main()
