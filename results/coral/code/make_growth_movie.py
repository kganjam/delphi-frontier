#!/usr/bin/env python3
"""
make_growth_movie.py — morphology-growth.mp4.

Renders two colonies growing side by side, at the two ends of the control parameter, so
the comparison is the point rather than the animation. Frames are occupied-voxel
projections, not renderings, and the title says so because a moving picture of a
simulation is the easiest thing on this page to mistake for a recording.
"""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402
import colony_morphology as cm                                    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = os.path.join(ROOT, "frames")
OUT = os.path.join(ROOT, "figures", "morphology-growth.mp4")

KW = dict(nx=88, ny=88, nz=72, target_volume=7000, n_gen=400)
ARMS = [(0.02, "Da 0.02  —  uptake-limited: compact mound"),
        (80.0, "Da 80  —  transport-limited: open lobed mound")]


def main():
    os.makedirs(FRAMES, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    series = []
    for Da, label in ARMS:
        fr = []
        cm.grow(Da=Da, seed=0, record_every=1, frames=fr, **KW)
        print(f"Da={Da}: {len(fr)} frames", flush=True)
        series.append((label, fr))

    n = max(len(f) for _, f in series)
    plt.rcParams.update({"figure.dpi": 110, "savefig.facecolor": "white",
                         "font.size": 8.5})
    for i in range(n):
        fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.0))
        for col, (label, fr) in enumerate(series):
            occ = fr[min(i, len(fr) - 1)]
            axes[0, col].imshow(occ.any(axis=1).T, origin="lower", cmap="bone_r",
                                interpolation="nearest")
            axes[0, col].set_title(label, fontsize=7.5, loc="left")
            axes[1, col].imshow(occ.any(axis=2).T, origin="lower", cmap="bone_r",
                                interpolation="nearest")
            axes[0, col].text(0.02, 0.95, f"gen {min(i, len(fr)-1)}   "
                                          f"vol {int(occ.sum())}",
                              transform=axes[0, col].transAxes, fontsize=6.5, va="top")
            for a in (axes[0, col], axes[1, col]):
                a.set_xticks([]); a.set_yticks([]); a.grid(False)
            if col == 0:
                axes[0, col].set_ylabel("side view")
                axes[1, col].set_ylabel("plan view")
        fig.suptitle("SIMULATED accretive growth. Occupied-voxel silhouettes, not "
                     "renderings; no coral was filmed.", fontsize=8.0, x=0.012,
                     ha="left")
        fig.tight_layout(rect=(0, 0, 1, 0.94))
        fig.savefig(os.path.join(FRAMES, f"f{i:04d}.png"))
        plt.close(fig)
    print(f"rendered {n} frames", flush=True)

    cmd = ["ffmpeg", "-y", "-framerate", "12", "-i",
           os.path.join(FRAMES, "f%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-crf", "22", OUT]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
