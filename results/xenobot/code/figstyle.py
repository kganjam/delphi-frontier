"""Shared figure style. Dark surface, because MorphoSwarm Studio is dark-only.
Palette slots and surfaces are the dataviz reference instance's DARK column,
validated for this chart's series count with scripts/validate_palette.js:
  node validate_palette.js "#3987e5,#d95926,#199e70" --mode dark  -> ALL CHECKS PASS
  (lightness band, chroma floor, CVD dE 9.4 deutan, normal-vision dE 26.5, >=3:1)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#1a1a19"
INK = "#f0efec"
INK2 = "#c3c2b7"
MUTED = "#6e6d66"
S1, S2, S3 = "#3987e5", "#d95926", "#199e70"   # blue, orange, aqua
S4, S5 = "#c98500", "#d55181"                   # yellow, magenta (slots 4,5)
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

DPI = 150
W = 900 / DPI          # 900 px wide at DPI


def setup():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE, "savefig.dpi": DPI, "figure.dpi": DPI,
        "text.color": INK, "axes.labelcolor": INK2, "axes.edgecolor": MUTED,
        "xtick.color": INK2, "ytick.color": INK2,
        "axes.titlecolor": INK, "axes.grid": True,
        "grid.color": "#33332f", "grid.linewidth": 0.6, "grid.alpha": 1.0,
        "axes.spines.top": False, "axes.spines.right": False,
        "font.size": 9, "axes.titlesize": 10.5, "axes.labelsize": 9,
        "legend.fontsize": 8.5, "legend.frameon": False, "legend.labelcolor": INK2,
        "lines.linewidth": 2.0, "lines.markersize": 5.5,
        "figure.constrained_layout.use": True,
    })


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return path
