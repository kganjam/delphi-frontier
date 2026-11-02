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
C = json.load(open(f"{ROOT}/cargo-work.json"))
g_ = lambda v, p: "%g" % v
GAITS = ["travelling", "longitudinal", "lateral", "dorsoventral", "uniform", "checker"]

# ------------------------------------------- 1. by gait: self vs cargo -----
fig = plt.figure(figsize=(F.W, F.W * 0.72))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.80], hspace=0.22)
ax = fig.add_subplot(gs[0, 0])
b = C["arm1b_contact_gated_40_cycles"]["per_gait"]
y = np.arange(len(GAITS))[::-1]
h = 0.34
self_v = [b[g]["self_locomotion_40cyc_m"] * 1000 for g in GAITS]
cargo_v = [b[g]["M1_cargo_net_disp_m"] * 1000 for g in GAITS]
ax.barh(y + h / 2, self_v, height=h, color=F.S1, edgecolor=F.SURFACE, linewidth=1.4,
        label="the construct moves itself")
ax.barh(y - h / 2, cargo_v, height=h, color=F.S2, edgecolor=F.SURFACE, linewidth=1.4,
        label="the construct moves an 8 g cargo")
for yy, g, sv, cv in zip(y, GAITS, self_v, cargo_v):
    ax.text(sv + 1.6, yy + h / 2, f"{sv:.1f}", va="center", fontsize=8, color=F.INK2)
    if b[g]["M1_cargo_net_disp_m"] > 1e-6:
        ax.text(cv + 1.6, yy - h / 2, f"{cv:.1f}", va="center", fontsize=8, color=F.INK2)
    else:
        ax.text(1.6, yy - h / 2, "never reached the cargo", va="center", fontsize=8, color=F.MUTED)
ax.set_yticks(y); ax.set_yticklabels(GAITS)
ax.set_xlabel("net displacement in 40 actuation cycles (mm)")
ax.set_xlim(0, 150)
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.02))
ax.set_title("A.  Simulation, dry friction. The best self-mover is also the best pusher — our prediction was wrong.\n"
             "Three of six gaits never reach the cargo at all, even in 40 cycles.", loc="left", fontsize=9.3)

# ------------------------------------------------ 2. transport ratio -------
# Two measures on different scales get TWO axes side by side, never one axes
# with two x-scales: a dual-axis chart lets the author choose the comparison.
gsb = gs[1, 0].subgridspec(1, 2, wspace=0.30)
contacting = C["arm1b_contact_gated_40_cycles"]["gaits_that_made_contact"]
order = sorted(contacting, key=lambda g: -b[g]["transport_ratio_after_contact"])
x = np.arange(len(order))
for k, (ax2, vals, col, lab, fmt, xlim) in enumerate([
        (fig.add_subplot(gsb[0, 0]), [b[g]["transport_ratio_after_contact"] for g in order],
         F.S3, "transport ratio\n(cargo displacement ÷ construct path)", "{:.2f}", 1.15),
        (fig.add_subplot(gsb[0, 1]), [b[g]["efficiency_after_contact"] * 100 for g in order],
         F.S5, "efficiency\n(friction work on cargo ÷ actuation work, %)", "{:.2f}%", 4.1)]):
    ax2.barh(x, vals, height=0.52, color=col, edgecolor=F.SURFACE, linewidth=1.4)
    for xx, v in zip(x, vals):
        ax2.text(v + xlim * 0.025, xx, fmt.format(v), va="center", fontsize=8.2, color=F.INK2)
    ax2.set_yticks(x); ax2.set_ylim(-0.65, len(order) - 0.35)
    ax2.set_yticklabels(order)
    ax2.set_xlim(0, xlim); ax2.set_xlabel(lab, fontsize=8.4)
    ax2.grid(axis="y", visible=False)
    if k == 0:
        ax2.set_title("B.  …and it is not just faster. Measured over the post-contact window only, it transfers\n"
                      "95% of its own path to the cargo against 51% and 26%, and does 7.5× the useful work per unit energy.",
                      loc="left", fontsize=9.3)
F.save(fig, f"{ROOT}/figures/cargo-work-by-gait.png")

# ------------------------------------------------- 3. swarm ---------------
fig = plt.figure(figsize=(F.W, F.W * 0.76))
gsw = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.92])
axes = [fig.add_subplot(gsw[0, 0]), fig.add_subplot(gsw[0, 1]), fig.add_subplot(gsw[1, :])]
S = C["arm3_swarm"]["per_N"]
ns = sorted(S, key=int)
nn = [int(n) for n in ns]
ax = axes[0]
lo = [S[n]["S1_min_median_max"][0] * 1000 for n in ns]
md = [S[n]["S1_min_median_max"][1] * 1000 for n in ns]
hi = [S[n]["S1_min_median_max"][2] * 1000 for n in ns]
ax.fill_between(nn, lo, hi, color=F.S1, alpha=0.25, lw=0)
ax.plot(nn, md, "o-", color=F.S1)
p = C["arm3_swarm"]["S1_scaling_exponent_vs_N"]
ax.plot(nn, md[0] * np.array(nn, float) ** 1.0, ls=(0, (5, 3)), color=F.MUTED, lw=1.4)
ax.annotate("linear in N", (nn[-1], md[0] * nn[-1]), textcoords="offset points",
            xytext=(-6, 8), fontsize=7.8, color=F.MUTED, ha="right")
ax.set_xlabel("swarm size N"); ax.set_ylabel("mean particle displacement (mm)")
ax.set_xticks(nn)
ax.set_title(f"A.  more constructs move more material, as N$^{{{p:.2f}}}$\nband is min–max over 5 seeds",
             loc="left", fontsize=8.9)

ax = axes[1]
lo = [S[n]["S2_min_median_max"][0] * 1000 for n in ns]
md = [S[n]["S2_min_median_max"][1] * 1000 for n in ns]
hi = [S[n]["S2_min_median_max"][2] * 1000 for n in ns]
ax.axhspan(-1.0, 0, color=F.S3, alpha=0.13, lw=0)
ax.axhline(0, color=F.MUTED, lw=1.2)
ax.fill_between(nn, lo, hi, color=F.S2, alpha=0.25, lw=0)
ax.plot(nn, md, "o-", color=F.S2)
ax.text(nn[0] + 0.1, -0.33, "aggregation would be here", fontsize=7.8, color=F.S3)
ax.annotate("2 of 5 seeds at N=8", (8, lo[-1]), textcoords="offset points", xytext=(-8, -2),
            fontsize=7.4, color=F.MUTED, ha="right")
ax.set_xlabel("swarm size N")
ax.set_ylabel("change in particle radius\nof gyration (mm)")
ax.set_xticks(nn); ax.set_ylim(-0.75, 1.75)
ax.set_title("B.  but the field DISPERSES in 28 of 30 runs\nboth exceptions at the largest N", loc="left", fontsize=8.9)
ax.set_ylabel("change in particle\nradius of gyration (mm)")
# panel C: the apparent aggregation at the largest N, resolved
axc = axes[2]
rows = C["arm3b_onset_test"]["span_analysis"]["rows"]
for tag, col, mk in (("narrow(y +/-22)", F.S2, "o"), ("wide(y +/-42)", F.S1, "s")):
    rr = [r for r in rows if r["field"] == tag]
    axc.plot([r["span_over_field"] for r in rr], [r["median_rg_change_mm"] for r in rr],
             mk, color=col, ms=7, ls="none",
             label=("narrow field" if "22" in tag else "wide field, density-matched"))
    for r in rr:
        if r["aggregating_seeds"]:
            axc.annotate(f"N={r['N']}\n{r['aggregating_seeds']}/5 aggregate",
                         (r["span_over_field"], r["median_rg_change_mm"]),
                         textcoords="offset points", xytext=(-14, 26), ha="right",
                         fontsize=7.4, color=F.S5,
                         arrowprops=dict(arrowstyle="->", color=F.S5, lw=1.1))
axc.axvspan(0.70, 0.80, color=F.MUTED, alpha=0.25, lw=0)
axc.axhline(0, color=F.MUTED, lw=1.1)
axc.set_xlabel("swarm span ÷ field half-width")
axc.set_ylabel("median rg change (mm)")
axc.set_xlim(0, 1.08); axc.set_ylim(-0.15, 1.75)
axc.legend(fontsize=7.6, loc="upper left", ncol=2)
axc.annotate("every configuration below 0.7 disperses in all 5 seeds", (0.05, 0.05),
             fontsize=7.6, color=F.INK2)
axc.set_title("C.  …and the two exceptions track the ARENA, not the swarm size: the same N = 8 in a wider field, and a LARGER N = 12, both disperse", loc="left", fontsize=8.9)

fig.suptitle("Simulation, dry friction. A uniform swarm sweeps; it does not corral, over N = 1 to 16.\n"
             "Every construct runs the same gait, so their effects add as a common drift rather than converging.",
             fontsize=9.6, ha="left", x=0.012, y=1.08)
F.save(fig, f"{ROOT}/figures/cargo-swarm-aggregation.png")
print("wrote cargo figures")
