"""S28-D-D: pixel-calibrated digitisation of Daane et al. 2021 bioRxiv preprint Fig 8B
(= Curr Biol 2021 Fig 4B), pectoral fin length / SL by genotype.

Input: the embedded raster of page 31 of the preprint PDF
  https://www.biorxiv.org/content/biorxiv/early/2021/03/07/2021.03.05.434157.full.pdf
  (sha256 of PDF d5096d02d6d154ee8843ae13aeb82df2bbeeb77e567622872abbb13927ed6c40),
  extracted with `pdfimages -f 31 -l 31 -png pre.pdf fig8` -> fig8-000.png (1554x710 px).
Usage: python3 -I S28-D-D_fig_digitize.py path/to/fig8-000.png

Everything printed is a FIGURE-READ (digitised from a plotted graphic), not a raw datum.
"""
import sys
import numpy as np
from PIL import Image

im = np.array(Image.open(sys.argv[1]).convert("RGB")).astype(int)

# --- y-axis calibration from tick marks left of the panel-B frame (x 815-827) ---
ys = []
run = []
for y in range(100, 650):
    if (im[y, 815:828].sum(1) < 300).sum() >= 4:
        run.append(y)
    elif run:
        ys.append(np.mean(run)); run = []
ys = sorted(ys)
assert len(ys) == 3, ys
vals = [0.60, 0.40, 0.20]
slope, icpt = np.polyfit(ys, vals, 1)
resid = np.array(vals) - (slope * np.array(ys) + icpt)
print(f"tick pixel rows {[round(v,1) for v in ys]} -> {1/abs(slope):.1f} px per unit; max residual {abs(resid).max():.4f}")
val = lambda y: slope * y + icpt

def mask(color, tol):
    return (np.abs(im - np.array(color)).max(2) <= tol)

groups = {
    "wt (gray)": ((165, 165, 165), 30, (840, 920)),
    "nr21/+ (blue)": ((55, 95, 135), 35, (900, 980)),
    "lof/+ (red)": ((225, 55, 55), 45, (960, 1050)),
    "nr21/+;lof/+ (purple)": ((100, 85, 165), 40, (1030, 1120)),
}
def label(m):
    """4-connected component labelling (no scipy dependency)."""
    lab = np.zeros(m.shape, int); n = 0
    for y0, x0 in zip(*np.nonzero(m)):
        if lab[y0, x0]:
            continue
        n += 1; stack = [(y0, x0)]; lab[y0, x0] = n
        while stack:
            y, x = stack.pop()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < m.shape[0] and 0 <= xx < m.shape[1] and m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; stack.append((yy, xx))
    return lab, n

for name, (col, tol, (x0, x1)) in groups.items():
    m = np.zeros(im.shape[:2], bool)
    m[110:640, x0:x1] = mask(col, tol)[110:640, x0:x1]
    # horizontal box lines: rows where the colour spans >= 25 px contiguous
    rows = []
    for y in range(110, 640):
        r = m[y, x0:x1]
        best = cur = 0
        for v in r:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best >= 25:
            rows.append(y)
    # cluster rows
    cl = []
    for y in rows:
        if cl and y - cl[-1][-1] <= 2:
            cl[-1].append(y)
        else:
            cl.append([y])
    lines = [(np.mean(c), len(c)) for c in cl]
    # dots: connected components, roughly round, area 15-120 px
    lab, n = label(m)
    dots = []
    for i in range(1, n + 1):
        yy, xx = np.nonzero(lab == i)
        h, w = np.ptp(yy) + 1, np.ptp(xx) + 1
        if 15 <= len(yy) <= 120 and 0.6 <= h / w <= 1.6 and h <= 12:
            dots.append(val(yy.mean()))
    print(f"\n{name}: horizontal lines (value, thickness px): " + ", ".join(f"{val(y):.3f} ({t})" for y, t in lines))
    if dots:
        d = np.array(dots)
        print(f"  isolated round dots found: {len(d)} (overlapping dots are merged/missed)."
              f" min {d.min():.3f}, median {np.median(d):.3f}, max {d.max():.3f}")
