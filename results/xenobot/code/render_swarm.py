#!/usr/bin/env python3
"""Render cargo-swarm.mp4 from the swarm run's voxel dump.

What this draws and what it does NOT: voxel CENTRES only, as points, plus a
convex outline per construct. The CSV stores centres and nothing else - no
orientations, no deformed meshes, no forces, no cellular state. Nothing cellular
or tissue-like is drawn, and the frame is labelled as a simulation of a
soft-voxel model, not a recording of an organism.
"""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/data/scratch/designspaces/xenobot"
F.setup()
raw = np.genfromtxt(f"{ROOT}/data/cargo/ANIM-voxels.csv", delimiter=",", names=True,
                    dtype=None, encoding="utf-8")
steps = np.unique(raw["step"])
print("frames:", len(steps))
NB = 6
VOX = 0.01
tmp = f"{ROOT}/data/anim_frames"
os.makedirs(tmp, exist_ok=True)
isbot = raw["kind"] == "bot"
botlen = 5 * 3 * 3

xs, ys = raw["x_m"] * 1000, raw["y_m"] * 1000
xlim = (xs.min() - 8, xs.max() + 8)
ylim = (ys.min() - 8, ys.max() + 8)
for k, s in enumerate(steps):
    m = raw["step"] == s
    t = raw["t_s"][m][0]
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    bx, by = raw["x_m"][m & isbot] * 1000, raw["y_m"][m & isbot] * 1000
    px, py = raw["x_m"][m & ~isbot] * 1000, raw["y_m"][m & ~isbot] * 1000
    ax.scatter(px, py, s=26, c=F.S2, edgecolors=F.SURFACE, linewidths=0.5, zorder=3,
               label="passive particles (never actuated)")
    for b in range(NB):
        sl = slice(b * botlen, (b + 1) * botlen)
        ax.scatter(bx[sl], by[sl], s=16, c=F.S3, alpha=0.95, zorder=4,
                   label="construct voxel centres" if b == 0 else None)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)")
    ax.grid(alpha=0.5)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("Simulation, not a recording. Soft-voxel model: 6 constructs (travelling gait),\n"
                 "120 passive particles, dry Coulomb friction on a floor.  "
                 f"t = {t:6.2f} s", loc="left", fontsize=9)
    ax.text(0.012, 0.015, "voxel CENTRES only — no orientations, no deformed meshes, no cellular state",
            transform=ax.transAxes, fontsize=7.4, color=F.MUTED)
    fig.savefig(f"{tmp}/f{k:05d}.png", dpi=125, facecolor=F.SURFACE,
                bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    if k % 20 == 0:
        print(" frame", k, flush=True)
out = f"{ROOT}/figures/cargo-swarm.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "20", "-i",
                f"{tmp}/f%05d.png", "-vf", "scale=900:-2,pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
                "-threads", "2", out], check=True)
print("wrote", out, os.path.getsize(out), "bytes")
