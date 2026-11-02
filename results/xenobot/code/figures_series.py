#!/usr/bin/env python3
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F
import matplotlib.pyplot as plt

ROOT = "/data/scratch/designspaces/xenobot"
F.setup()
D = json.load(open(f"{ROOT}/convergence.raw.json"))
SER = D["refinement_series"]["series"]

fig, axes = plt.subplots(1, 3, figsize=(F.W, F.W * 0.50))

for ax, (name, col, letter, lab) in zip(axes[:2], [
        ("A_travelling", F.S3, "A", "travelling"),
        ("B_longitudinal", F.S2, "B", "longitudinal, parity-matched")]):
    v = SER[name]
    lv = v["levels"]
    x = np.arange(len(lv))
    y = [l["normalised_by_outer_envelope"] for l in lv]
    ax.plot(x, y, "o-", color=col, ms=8)
    for xx, yy, l in zip(x, y, lv):
        ax.annotate(f"{l['voxels']}", (xx, yy), textcoords="offset points", xytext=(0, 11),
                    ha="center", fontsize=7.6, color=F.INK2)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{l['voxel_m']*1000:.3g}" for l in lv])
    ax.set_xlabel("voxel size (mm), refining →")
    ax.set_xlim(-0.4, len(lv) - 0.45)
    sp = v["total_spread_rel_to_coarsest"]
    ax.set_title(f"{letter}.  {lab}\nspread {sp*100:.0f}%, non-monotone", loc="left", fontsize=8.5)
    lo, hi = min(y), max(y)
    ax.set_ylim(lo - 0.20 * (hi - lo), hi + 0.34 * (hi - lo))
axes[0].set_ylabel("net displacement ÷ outer envelope")

ax = axes[2]
r = D["ranking_stability"]["travelling_over_longitudinal_by_level"]
lv = SER["A_travelling"]["levels"][:len(r)]
x = np.arange(len(r))
ax.plot(x, r, "o-", color=F.S1, ms=8)
ax.axhline(1.0, color=F.MUTED, lw=1.0, ls=(0, (4, 3)))
ax.annotate("equal", (len(r) - 1, 1.0), textcoords="offset points", xytext=(-4, 7),
            fontsize=7.4, color=F.MUTED, ha="right")
for xx, rr in zip(x, r):
    ax.annotate(f"{rr:.1f}×", (xx, rr), textcoords="offset points", xytext=(0, 11),
                ha="center", fontsize=7.8, color=F.INK2)
ax.set_xticks(x); ax.set_xticklabels([f"{l['voxel_m']*1000:.3g}" for l in lv])
ax.set_xlabel("voxel size (mm), refining →")
ax.set_ylabel("travelling ÷ longitudinal")
ax.set_ylim(0, 24); ax.set_xlim(-0.4, len(r) - 0.45)
ax.set_title("C.  winner stable,\nmargin not", loc="left", fontsize=8.5)

fig.suptitle("Simulation. A parity-matched grid refinement does not converge.",
             fontsize=10, ha="left", x=0.012, y=1.06)
F.save(fig, f"{ROOT}/figures/convergence-series.png")
print("wrote convergence-series.png")
