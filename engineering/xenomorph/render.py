"""Figures and animations for the xenomorph runs (single-threaded matplotlib, Agg).

  python -m engineering.xenomorph.render curves  --runs RUNS_DIR --out FIG.png
  python -m engineering.xenomorph.render gif     --run RUN_DIR  --out ANIM.gif
  python -m engineering.xenomorph.render stl     --stl FILE.stl [--cells FILE.npz] --out FIG.png
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

ARM_COLOR = {"dah": "#2a78d6", "equal": "#eb6834", "zero": "#1baf7a"}
ARM_LABEL = {"dah": "unequal adhesion (DAH)", "equal": "equal adhesion (control)", "zero": "zero adhesion (control)"}
TYPE_COLOR = {1: "#2a78d6", 2: "#eb6834"}  # A blue (more cohesive), B orange
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"
SCOPE = "Simulated (Morpheus 2.3.9 Cellular Potts, dimensionless). Not a Xenobot or any organism; no frog parameter."

plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "figure.facecolor": "#fcfcfb",
                     "axes.facecolor": "#fcfcfb"})

PANELS = [("largest_cluster_fraction", "largest-cluster fraction"), ("n_aggregates", "aggregate count"),
          ("rg_norm", "radius of gyration (normalised)"), ("sphericity_largest", "sphericity of largest cluster"),
          ("contact_area_cell_cell", "cell–cell contact area (faces)"),
          ("sorting_index_homotypic", "homotypic contact fraction"), ("core_shell_index", "core–shell index (A core > 0)")]


def load_runs(root: Path, scale: float = 1.0):
    out = {}
    for m in sorted(root.glob("*/metrics.json")):
        d = json.loads(m.read_text())
        if abs(d["scale"] - scale) > 1e-9:
            continue
        out.setdefault(d["arm"], []).append(d)
    return out


def curves(root: Path, out: Path):
    runs = load_runs(root)
    fig, axes = plt.subplots(2, 4, figsize=(13, 6.2))
    axes = axes.ravel()
    for ax, (key, title) in zip(axes, PANELS):
        for arm in ("dah", "equal", "zero"):
            for d in runs.get(arm, []):
                t = [r["mcs"] for r in d["rows"]]
                y = [r[key] for r in d["rows"]]
                ax.plot(t, y, color=ARM_COLOR[arm], lw=1.6 if d["seed"] == 1 else 1.0, alpha=1.0 if d["seed"] == 1 else 0.55)
        ax.set_title(title, color=INK, fontsize=9.5, loc="left")
        ax.set_xlabel("Monte Carlo steps")
    ax = axes[-1]
    ax.axis("off")
    for i, arm in enumerate(("dah", "equal", "zero")):
        n = len(runs.get(arm, []))
        ax.plot([0.02, 0.14], [0.8 - i * 0.16] * 2, color=ARM_COLOR[arm], lw=2.2, transform=ax.transAxes)
        ax.text(0.18, 0.8 - i * 0.16, f"{ARM_LABEL[arm]}  ({n} seeds)", va="center", color=INK, transform=ax.transAxes)
    ax.text(0.02, 0.22, "thick line = seed 1; thin = other seeds", color=INK2, transform=ax.transAxes)
    ax.text(0.02, 0.04, SCOPE, color=INK2, fontsize=7, wrap=True, transform=ax.transAxes)
    fig.suptitle("Dissociated cells aggregating: morphogenesis measured per snapshot", x=0.01, ha="left", color=INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


def cell_points(ids, types):
    n = int(ids.max())
    zz, yy, xx = np.nonzero(ids)
    lab = ids[zz, yy, xx].astype(np.int64)
    cnt = np.bincount(lab, minlength=n + 1)
    c = [np.bincount(lab, weights=w, minlength=n + 1) / np.maximum(cnt, 1) for w in (xx, yy, zz)]
    keep = cnt[1:] > 0
    return np.stack(c, 1)[1:][keep], cnt[1:][keep], types[1:][keep]


def gif(run: Path, out: Path, every_frame_ms: int = 350):
    import imageio.v2 as imageio
    F = np.load(run / "fields.npz")
    M = json.loads((run / "metrics.json").read_text())
    rows = {r["mcs"]: r for r in M["rows"]}
    times = sorted(int(k.split("_")[1]) for k in F.files if k.startswith("ids_"))
    frames = []
    ids0 = F[f"ids_{times[0]}"]
    L = ids0.shape[0]
    for t in times:
        ids, ty = F[f"ids_{t}"], F[f"types_{t}"]
        C, cnt, tt = cell_points(ids, ty)
        fig = plt.figure(figsize=(8.6, 4.4))
        ax = fig.add_subplot(1, 2, 1, projection="3d")
        r = (3 * cnt / (4 * np.pi)) ** (1 / 3)
        ax.scatter(C[:, 0], C[:, 1], C[:, 2], s=(r * 4.2) ** 2, c=[TYPE_COLOR[int(k)] for k in tt],
                   edgecolors="#fcfcfb", linewidths=0.4, depthshade=True)
        ax.set_xlim(0, L); ax.set_ylim(0, L); ax.set_zlim(0, L)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=18, azim=35 + 0.6 * times.index(t))
        ax.set_title("cells (centroids, equal-volume size)", fontsize=8.5, color=INK2)
        ax2 = fig.add_subplot(1, 2, 2)
        z = L // 2
        sl = ids[z]
        img = np.full(sl.shape + (3,), 0.988)
        for k, col in TYPE_COLOR.items():
            rgb = np.array([int(col[i:i + 2], 16) / 255 for i in (1, 3, 5)])
            img[(sl > 0) & (ty[sl] == k)] = rgb
        # cell borders
        b = np.zeros(sl.shape, bool)
        b[:-1] |= sl[:-1] != sl[1:]
        b[:, :-1] |= sl[:, :-1] != sl[:, 1:]
        img[b & (sl > 0)] = img[b & (sl > 0)] * 0.55
        ax2.imshow(img, origin="lower", interpolation="nearest")
        ax2.set_xticks([]); ax2.set_yticks([]); ax2.grid(False)
        ax2.set_title(f"mid-plane slice z={z} (A blue, B orange)", fontsize=8.5, color=INK2)
        m = rows[t]
        fig.suptitle(f"{M['arm']} seed {M['seed']}   t = {t} MCS   aggregates {m['n_aggregates']}   "
                     f"largest {m['largest_cluster_fraction']:.2f}   Rg {m['rg_norm']:.3f}   "
                     f"core–shell {m['core_shell_index']:+.2f}", fontsize=9, color=INK, x=0.01, ha="left")
        fig.text(0.01, 0.015, SCOPE, fontsize=6.5, color=INK2)
        fig.canvas.draw()
        frames.append(np.asarray(fig.canvas.buffer_rgba())[..., :3].copy())
        plt.close(fig)
    imageio.mimsave(out, frames, duration=every_frame_ms / 1000, loop=0)


def stl_png(stl: Path, out: Path, cells: Path | None = None, title: str = ""):
    from engineering.geometry.validate import read_stl
    V, T = read_stl(stl.read_bytes())
    tri = V[T]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(n @ light, 0, 1)
    base = np.tile(np.array([0.78, 0.78, 0.76]), (len(T), 1))
    if cells is not None:
        z = np.load(cells)
        C, ty = z["centers_mm"] - z["centers_mm"].min(0) + (z["radii_mm"].max() * 0 ), z["types"]
        # STL was shifted to the plate origin: recover the shift from bounds
        Cs = z["centers_mm"]; Rr = z["radii_mm"]
        shift = (Cs - Rr[:, None]).min(0)
        cen = tri.mean(1) + shift
        from scipy.spatial import cKDTree
        d, k = cKDTree(Cs).query(cen)
        cols = np.array([[int(TYPE_COLOR[int(t)][i:i + 2], 16) / 255 for i in (1, 3, 5)] for t in ty])
        base = cols[k]
        near = d <= Rr[k] * 1.08
        base[~near] = [0.55, 0.55, 0.53]  # print-only struts in grey
    fc = base * shade[:, None]
    fig = plt.figure(figsize=(5.2, 5.2))
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(tri, facecolors=fc, edgecolors="none"))
    lo, hi = V.min(0), V.max(0)
    c, h = (lo + hi) / 2, (hi - lo).max() / 2
    ax.set_xlim(c[0] - h, c[0] + h); ax.set_ylim(c[1] - h, c[1] + h); ax.set_zlim(c[2] - h, c[2] + h)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(elev=22, azim=-55)
    sz = hi - lo
    ax.set_title(f"{title}\n{sz[0]:.0f} × {sz[1]:.0f} × {sz[2]:.0f} mm", fontsize=8.5, color=INK)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def offlattice_fig(summary: dict, out: Path, key: str = "trajectory"):
    """Final Rg ratio and core-shell index vs A-A adhesion, one line per B/A ratio, for each (D, dt)."""
    rows = summary["groups"]
    combos = sorted({(r["D"], r["dt"]) for r in rows})
    ratio_col = {1.0: "#2a78d6", 0.5: "#eb6834", 0.25: "#1baf7a"}
    fig, axes = plt.subplots(2, len(combos), figsize=(3.3 * len(combos), 5.6), squeeze=False)
    for j, (D, dt) in enumerate(combos):
        for ratio, col in ratio_col.items():
            rr = sorted([r for r in rows if r["D"] == D and r["dt"] == dt and (r["ratio"] == ratio or r["c_AA"] == 0)],
                        key=lambda r: r["c_AA"])
            if not rr:
                continue
            x = [r["c_AA"] for r in rr]
            axes[0, j].errorbar(x, [r["rg_ratio_mean"] for r in rr], color=col, lw=1.6, marker="o", ms=4,
                                label=f"c_BB/c_AA = {ratio:g}")
            axes[1, j].errorbar(x, [r["final_core_shell_index_mean"] for r in rr],
                                yerr=[r["final_core_shell_index_range"] / 2 for r in rr], color=col, lw=1.6, marker="o", ms=4, capsize=2)
        axes[0, j].axhline(0.95, color=INK2, lw=0.8, ls="--")
        axes[1, j].axhline(0.1, color=INK2, lw=0.8, ls="--")
        axes[0, j].set_title(f"D={D:g}, dt={dt:g}", fontsize=9, color=INK, loc="left")
        axes[1, j].set_xlabel("A–A adhesion strength c_AA")
    axes[0, 0].set_ylabel("final Rg / initial Rg")
    axes[1, 0].set_ylabel("final core–shell index")
    axes[0, 0].legend(fontsize=7, frameon=False)
    fig.suptitle(f"Off-lattice engine (N={summary['n_cells']} cells, 4 seeds per point): compaction and sorting vs adhesion",
                 x=0.01, ha="left", color=INK, fontsize=11)
    fig.text(0.01, 0.005, "dashed: 0.95 no-compaction line (top), 0.1 sorting threshold (bottom). " + SCOPE.replace("Morpheus 2.3.9 Cellular Potts", "PhysiCell-form potentials, PyTorch"),
             fontsize=6.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out, dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["curves", "gif", "stl", "offlattice"])
    ap.add_argument("--summary"); ap.add_argument("--key")
    ap.add_argument("--runs"); ap.add_argument("--run"); ap.add_argument("--stl"); ap.add_argument("--cells")
    ap.add_argument("--title", default=""); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.what == "curves":
        curves(Path(a.runs), Path(a.out))
    elif a.what == "gif":
        gif(Path(a.run), Path(a.out))
    elif a.what == "offlattice":
        offlattice_fig(json.loads(Path(a.summary).read_text())[a.key], Path(a.out))
    else:
        stl_png(Path(a.stl), Path(a.out), Path(a.cells) if a.cells else None, a.title)
