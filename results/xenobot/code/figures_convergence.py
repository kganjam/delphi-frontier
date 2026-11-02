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
SW = json.load(open(f"{ROOT}/data/sweeps.json"))
FO = json.load(open(f"{ROOT}/data/freqopt.json"))
g_ = lambda v, p: "%g" % v
VOX = 0.01


def merged(pat, nx):
    row = {float(k): v for k, v in FO["data"][pat].get(str(nx), {}).items()}
    for f, v in SW["freq_nx_map"][pat].get(str(nx), {}).items():
        row[float(f)] = v["body_lengths"]
    fs = sorted(row)
    return fs, [row[f] for f in fs]


fig = plt.figure(figsize=(F.W, F.W * 1.15))
gs = fig.add_gridspec(3, 1, height_ratios=[1.25, 1.0, 1.0])

# ------------------------------------------------------------- panel A ----
ax = fig.add_subplot(gs[0, 0])
nxs = list(range(3, 17))
lo = [SW["parity_sweep"]["longitudinal"][str(n)]["body_lengths"] for n in nxs]
tr = [SW["parity_sweep"]["travelling"][str(n)]["body_lengths"] for n in nxs]
ax.plot(nxs, lo, color=F.MUTED, lw=0.9, alpha=0.45, zorder=0)
odd = [i for i, n in enumerate(nxs) if n % 2]
evn = [i for i, n in enumerate(nxs) if not n % 2]
ax.plot([nxs[i] for i in odd], [lo[i] for i in odd], "o-", color=F.S2, zorder=3)
ax.plot([nxs[i] for i in evn], [lo[i] for i in evn], "s--", color=F.S2, alpha=0.6,
        markerfacecolor=F.SURFACE, markeredgewidth=1.6, zorder=3)
ax.plot(nxs, tr, "^-", color=F.S3, zorder=3)
for n in (4, 5, 6, 7):
    ax.plot(n, lo[nxs.index(n)], "o", ms=14, mfc="none", mec=F.S5, mew=1.7, zorder=5)
ax.annotate("the four points the audit flagged as a\n'non-monotone ten-fold swing' are two\n"
            "adjacent points of each smooth branch",
            xy=(6.2, lo[nxs.index(6)]*1.15), xytext=(8.0, 1.05), color=F.S5, fontsize=8.2,
            arrowprops=dict(arrowstyle="->", color=F.S5, lw=1.2))
ax.legend(loc="lower left", fontsize=8.0, handles=[
    Line2D([], [], marker="^", ls="-", color=F.S3, ms=7,
           label="travelling — phase is a continuous gradient, parity-free"),
    Line2D([], [], marker="o", ls="-", color=F.S2, ms=7,
           label="longitudinal, odd $n_x$ — asymmetric actuator split"),
    Line2D([], [], marker="s", ls="--", color=F.S2, ms=7, mfc=F.SURFACE, mew=1.6,
           label="longitudinal, even $n_x$ — symmetric actuator split")])
ax.set_yscale("log"); ax.set_ylim(5e-5, 9.0)
ax.set_xlabel("$n_x$  —  voxels along the travel axis, lattice spacing fixed at 10 mm")
ax.set_ylabel("net displacement\n(body lengths, 5 cycles)")
ax.set_xticks(nxs); ax.yaxis.set_major_formatter(FuncFormatter(g_))
ax.set_title("A.  Simulation. The flagged non-monotonicity is the actuation ENCODING, not the mechanics.",
             loc="left", fontsize=9.6)

# ------------------------------------------------------------- panel B ----
axL = fig.add_subplot(gs[1, 0])
for nx, c, dy in zip((4, 6, 8, 12), [F.SEQ[1], F.SEQ[3], F.SEQ[5], F.S5], (9, 0, -10, 0)):
    fs, vs = merged("travelling", nx)
    axL.plot(fs, vs, "o-", color=c, ms=4, lw=1.7)
    axL.annotate(f"L = {(nx-1)*VOX*100:.0f} cm", (fs[-1], vs[-1]), textcoords="offset points",
                 xytext=(6, dy), fontsize=7.8, color=c, va="center")
axL.set_xscale("log"); axL.set_xlim(0.2, 90)
axL.set_xticks([0.25, 1, 4, 16]); axL.set_xticks([], minor=True)
axL.xaxis.set_major_formatter(FuncFormatter(g_))
axL.set_xlabel("drive frequency (Hz) — 5 cycles at every point")
axL.set_ylabel("body lengths / 5 cycles")
axL.set_title("B.  travelling: a broad, shallow frequency response at every body length — no resonant peak", loc="left", fontsize=9.2)

# ------------------------------------------------------------- panel C ----
axR = fig.add_subplot(gs[2, 0])
for pat, c, mk in (("longitudinal", F.S2, "o"), ("travelling", F.S3, "^")):
    for nx in (4, 5, 6, 7, 8):
        fs, vs = merged(pat, nx)
        bi = max(range(len(fs)), key=lambda i: vs[i])
        edge = bi in (0, len(fs) - 1)
        L = (nx - 1) * VOX
        axR.plot(L, fs[bi], mk, color=c, ms=9, mfc=F.SURFACE if edge else c,
                 mew=1.8, mec=c, zorder=4)
        axR.annotate(f"{nx}", (L, fs[bi]), textcoords="offset points",
                     xytext=(0, 12 if pat == "longitudinal" else -16),
                     ha="center", fontsize=7.2, color=F.INK2)
Lx = np.array([0.029, 0.072])
axR.plot(Lx, 12.0 * 0.03 / Lx, ls=(0, (5, 3)), color=F.MUTED, lw=1.5)
axR.annotate("a length resonance would\ngive $f_{opt}\\propto 1/L$", (Lx[1], 12 * 0.03 / Lx[1]),
             textcoords="offset points", xytext=(8, 14), fontsize=7.6, color=F.MUTED,
             ha="left", va="center")
axR.set_xscale("log"); axR.set_yscale("log")
axR.set_xlim(0.026, 0.115); axR.set_ylim(0.13, 200)
axR.set_xticks([0.03, 0.05, 0.07]); axR.set_xticks([], minor=True)
axR.set_yticks([0.25, 1, 4, 16]); axR.set_yticks([], minor=True)
axR.xaxis.set_major_formatter(FuncFormatter(g_)); axR.yaxis.set_major_formatter(FuncFormatter(g_))
axR.set_xlabel("body length L (m) — point labels are $n_x$")
axR.set_ylabel("optimum frequency (Hz)")
axR.legend(handles=[Line2D([], [], marker="o", ls="", color=F.S2, ms=8, label="longitudinal"),
                    Line2D([], [], marker="^", ls="", color=F.S3, ms=8, label="travelling"),
                    Line2D([], [], marker="o", ls="", mfc=F.SURFACE, mec=F.MUTED, mew=1.8,
                           color=F.MUTED, ms=8, label="optimum at the swept boundary")],
           fontsize=7.4, loc="lower left", bbox_to_anchor=(0.005, 0.015))
axR.set_title("C.  body length doubles from $n_x$=4 to 8 and the optimum frequency does not move with it", loc="left", fontsize=9.2)
F.save(fig, f"{ROOT}/figures/convergence-parity-resonance.png")
print("wrote convergence-parity-resonance.png")
