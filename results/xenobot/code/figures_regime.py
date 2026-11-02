#!/usr/bin/env python3
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

ROOT = "/data/scratch/designspaces/xenobot"
F.setup()
R = json.load(open(f"{ROOT}/regime-check.raw.json"))
g = np.load(f"{ROOT}/data/regime-reynolds-grid.npz")
sizes, speeds, Re = g["sizes"], g["speeds"], g["Re"]
lg = lambda v, p: ("%g" % v)

# ------------------------------------------------- 1. Reynolds number map --
fig, ax = plt.subplots(figsize=(F.W, F.W * 0.58))
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("seq", F.SEQ[::-1])
L = np.log10(Re)
im = ax.pcolormesh(sizes * 1e3, speeds * 1e6, L.T, cmap=cmap, shading="gouraud",
                   vmin=L.min(), vmax=L.max())
cs = ax.contour(sizes * 1e3, speeds * 1e6, L.T, levels=[-1.5, -1.0, -0.5],
                colors=F.INK, linewidths=1.1, alpha=0.6)
ax.clabel(cs, fmt=lambda v: f"Re = {10**v:.2g}", fontsize=7.5, colors=F.INK,
          inline_spacing=6)
for a, mk, dxy in zip(R["reynolds_map"]["anchors"], ("o", "s", "^"),
                      ((0, 0), (12, 10), (12, -16))):
    if a["L_m"] * 1e3 < sizes[0] * 1e3 * 0.999:
        continue
    ax.plot(a["L_m"] * 1e3, a["U_m_s"] * 1e6, mk, color=F.S2, markersize=10,
            markeredgecolor=F.SURFACE, markeredgewidth=1.8, zorder=6)
    nm = a["name"].split(",")[0]
    ax.annotate(f"{nm}  ·  Re = {a['Re']:.2g}", (a["L_m"] * 1e3, a["U_m_s"] * 1e6),
                textcoords="offset points", xytext=dxy,
                ha="left" if dxy[0] >= 0 else "right",
                fontsize=8.2, color=F.INK, zorder=7)
ax.set_xscale("log"); ax.set_yscale("log")
ax.xaxis.set_major_formatter(FuncFormatter(lg)); ax.xaxis.set_minor_formatter(FuncFormatter(lg))
ax.yaxis.set_major_formatter(FuncFormatter(lg)); ax.yaxis.set_minor_formatter(FuncFormatter(lg))
ax.set_xticks([0.3, 0.5, 1.0, 2.0]); ax.set_xticks([], minor=True)
ax.set_yticks([50, 100, 200, 500, 1000]); ax.set_yticks([], minor=True)
ax.set_xlabel("construct size  L  (mm)")
ax.set_ylabel("speed  U  (µm s$^{-1}$)")
ax.set_title("Simulation (closed form). Reynolds number of a millimetre-scale construct in water at 20 °C.\n"
             f"Re = ρUL/μ ranges {Re.min():.3f}–{Re.max():.2f} over this window; it exceeds 1 only in the "
             "top-right corner\n(2 mm at ≥0.5 mm s⁻¹). Everywhere a published construct actually sits, "
             "Re ≲ 0.1.", loc="left", fontsize=9.3)
cb = fig.colorbar(im, ax=ax, pad=0.015)
cb.set_label("log$_{10}$ Re", color=F.INK2); cb.ax.tick_params(colors=F.INK2)
cb.outline.set_edgecolor(F.MUTED)
sim = R["simulated_object_regime"]
ax.text(0.015, 0.97,
        "the voxel-actuation artifact's own body, in water:\n"
        f"L = {sim['L_m']*1e3:.0f} mm, U = {sim['U_m_s']*1e3:.1f} mm s⁻¹  →  Re = {sim['Re_translational']:.0f}\n"
        f"off this chart, {R['regime_separation_orders_of_magnitude']:.1f} orders above the 1 mm construct",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.2, color=F.S2,
        bbox=dict(facecolor=F.SURFACE, edgecolor=F.S2, linewidth=1.1,
                  boxstyle="round,pad=0.45", alpha=0.95), zorder=8)
F.save(fig, f"{ROOT}/figures/regime-reynolds-map.png")

# -------------------------------------------- 2. ranking side by side ------
gaits = ["travelling", "longitudinal", "lateral", "dorsoventral", "checker", "uniform"]
dry = R["dry_friction_ranking"]["per_gait_body_lengths_5_cycles"]
stk = R["stokes_ranking"]["per_gait_body_lengths_per_cycle"]
recip = {k: v["reciprocal"] for k, v in R["reciprocity"]["per_gait"].items()}
FLOOR = 3e-7
fig, axes = plt.subplots(1, 2, figsize=(F.W, F.W * 0.50), sharey=True)
y = np.arange(len(gaits))[::-1]
LOW = 1e-8

# left: dry friction, every value is real -> stem + dot
ax = axes[0]
for yy, gg in zip(y, gaits):
    v = dry[gg] / 5.0
    c = F.S3 if not recip[gg] else F.S2
    ax.plot([LOW, v], [yy, yy], color=c, lw=2.0, alpha=0.5, solid_capstyle="butt")
    ax.plot(v, yy, "o", color=c, markersize=8, markeredgecolor=F.SURFACE, markeredgewidth=1.4)
    ax.text(v * 2.0, yy, f"{v:.3g}", va="center", fontsize=8.2, color=F.INK2)
ax.set_title("Dry friction on a floor  (Re ≈ 640 in water)\nthe published artifact, per cycle",
             loc="left", fontsize=9.3)

# right: Stokes. Reciprocal gaits are EXACTLY zero; draw no magnitude for them.
ax = axes[1]
for yy, gg in zip(y, gaits):
    v = stk[gg]
    if not recip[gg]:
        ax.plot([LOW, v], [yy, yy], color=F.S3, lw=2.0, alpha=0.5, solid_capstyle="butt")
        ax.plot(v, yy, "o", color=F.S3, markersize=8, markeredgecolor=F.SURFACE, markeredgewidth=1.4)
        ax.text(v * 2.0, yy, f"{v:.3g}", va="center", fontsize=8.2, color=F.INK2)
    else:
        ax.plot(FLOOR, yy, "o", color=F.SURFACE, markersize=8,
                markeredgecolor=F.S2, markeredgewidth=1.8, zorder=4)
        ax.annotate("", xy=(LOW * 2.2, yy), xytext=(FLOOR * 0.8, yy),
                    arrowprops=dict(arrowstyle="->", color=F.S2, lw=1.4, alpha=0.9))
        ax.text(FLOOR * 2.0, yy, "exactly 0", va="center", fontsize=8.2, color=F.S2)
ax.axvline(FLOOR, color=F.MUTED, lw=1.0, ls=(0, (4, 3)))
ax.annotate("shape-solve noise floor", xy=(FLOOR, -0.95), xytext=(FLOOR * 60, -0.95),
            fontsize=7.4, color=F.MUTED, va="center", ha="left",
            arrowprops=dict(arrowstyle="-", color=F.MUTED, lw=0.9))
ax.set_title("Stokes flow in water  (Re ≈ 0.1)\nthis work, per cycle", loc="left", fontsize=9.3)

for ax in axes:
    ax.set_xscale("log"); ax.set_xlim(LOW, 1.0)
    ax.set_xlabel("net displacement  (body lengths / cycle)")
    ax.set_ylim(-1.35, len(gaits) - 0.45)
    ax.grid(axis="y", visible=False)
axes[0].set_yticks(y); axes[0].set_yticklabels(gaits)
fig.legend(handles=[Line2D([], [], marker="o", ls="", color=F.S3, markersize=8,
                           label="non-reciprocal gait — can swim at low Re"),
                    Line2D([], [], marker="o", ls="", mfc=F.SURFACE, mec=F.S2, mew=1.8,
                           color=F.S2, markersize=8,
                           label="time-reciprocal gait — scallop theorem forbids net motion")],
           loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.10))
fig.suptitle("Simulation. The published gait ranking does not survive the regime change.\n"
             "Five of the six gaits assign only the phases 0 and π, so the whole body is driven by one "
             "scalar in time\nand the stroke retraces itself. Purcell's scallop theorem makes their net "
             "displacement exactly zero in Stokes flow.",
             fontsize=9.6, ha="left", x=0.012, y=1.17)
F.save(fig, f"{ROOT}/figures/regime-ranking-compare.png")
print("wrote regime figures")
