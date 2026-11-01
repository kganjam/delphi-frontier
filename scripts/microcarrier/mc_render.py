#!/usr/bin/env python3
"""Render a microcarrier run (voxel dump CSV) to MP4 + GIF: side view (x-z) and top view (x-y),
voxels coloured by the prescribed drive strain (blue = contracting, red = expanding), with the
COM trail. Single-threaded. Labels say what it is: generic soft-voxel mechanics, not biology.
usage: mc_render.py RUN_PREFIX TITLE OUT_STEM [--every k]"""
import csv, sys, collections, argparse, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib import animation

ap = argparse.ArgumentParser(); ap.add_argument("prefix"); ap.add_argument("title"); ap.add_argument("out")
ap.add_argument("--every", type=int, default=2); a = ap.parse_args()
frames = collections.OrderedDict()
with open(a.prefix + "-voxels.csv") as f:
    for r in csv.DictReader(f):
        frames.setdefault(r["t_s"], []).append((float(r["x"]), float(r["y"]), float(r["z"]), float(r["strain_drive"])))
keys = list(frames)[::a.every]
P = [np.array(frames[k]) for k in keys]; T = [float(k) for k in keys]
import json
meta = json.load(open(a.prefix + ".json")); vox = meta["mesh"]["voxel_m"]
com = np.array([p[:, :3].mean(0) for p in P])
x0 = com[0, 0]; y0 = com[0, 1]
um = 1e6
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 7.2), dpi=110, gridspec_kw={"height_ratios": [1, 1.25]})
fig.patch.set_facecolor("#fbfbf8")
allp = np.concatenate(P)
xl = ((allp[:, 0].min() - x0 - vox) * um - 30, (allp[:, 0].max() - x0 + vox) * um + 30)
yl = ((allp[:, 1].min() - y0 - vox) * um - 30, (allp[:, 1].max() - y0 + vox) * um + 30)
ztop = (allp[:, 2].max() + vox) * um + 30
cmap = plt.get_cmap("coolwarm"); vmax = 0.15
def draw(i):
    for ax in (ax1, ax2): ax.clear(); ax.set_facecolor("#fbfbf8")
    p = P[i]; c = cmap(0.5 + 0.5 * np.clip(p[:, 3] / vmax, -1, 1)); s = vox * um
    order = np.argsort(p[:, 1])  # side view: far voxels first
    ax1.add_collection(PatchCollection([Rectangle(((p[j, 0] - x0) * um - s / 2, p[j, 2] * um - s / 2), s, s) for j in order],
                                       facecolor=c[order], edgecolor="#333", linewidth=0.3))
    ax1.axhline(-s / 2, color="#6b5b3e", lw=2); ax1.set_xlim(*xl); ax1.set_ylim(-s / 2 - 40, max(700, ztop)); ax1.set_aspect("equal")
    ax1.set_ylabel("z (um)"); ax1.set_title("side view", fontsize=9, loc="left")
    order = np.argsort(p[:, 2])
    ax2.add_collection(PatchCollection([Rectangle(((p[j, 0] - x0) * um - s / 2, (p[j, 1] - y0) * um - s / 2), s, s) for j in order],
                                       facecolor=c[order], edgecolor="#333", linewidth=0.3))
    ax2.plot((com[:i + 1, 0] - x0) * um, (com[:i + 1, 1] - y0) * um, color="k", lw=1.2)
    ax2.plot([0], [0], "o", ms=3, color="#888")
    ax2.set_xlim(*xl); ax2.set_ylim(*yl); ax2.set_aspect("equal")
    ax2.set_xlabel("x (um), relative to start"); ax2.set_ylabel("y (um)"); ax2.set_title("top view + COM path", fontsize=9, loc="left")
    d = np.hypot(com[i, 0] - x0, com[i, 1] - y0) * um
    import textwrap
    fig.suptitle(textwrap.fill(a.title, 80) + f"\nt = {T[i] - T[0]:.3f} s   COM displacement {d:.1f} um", fontsize=10)

    fig.subplots_adjust(bottom=0.12, top=0.88, hspace=0.35)
    return []
fig.text(0.01, 0.005, "Voxelyze @4287e365, generic soft-voxel mechanics on a frictional floor. Not tissue, not a xenobot, not cilia.\n"
             "Colour: prescribed drive strain (blue contract, red expand). All material values assumed.\nFloor drawn at the bottom face; the engine's contact acts at bottom-voxel centres.", fontsize=6.5, color="#555")
ani = animation.FuncAnimation(fig, draw, frames=len(P), blit=False)
ani.save(a.out + ".mp4", writer=animation.FFMpegWriter(fps=24, bitrate=1800, extra_args=["-threads", "1", "-pix_fmt", "yuv420p"]))
ani.save(a.out + ".gif", writer=animation.PillowWriter(fps=12))
print("wrote", a.out + ".mp4", a.out + ".gif", len(P), "frames")
