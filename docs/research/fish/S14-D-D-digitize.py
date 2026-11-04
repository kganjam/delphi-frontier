"""S14-D-D: digitize Perathoner et al. 2014 PLoS Genet Figure 5D.

Fig 5D plots, for each individual Xenopus oocyte, resting membrane potential Vm [mV]
against the current I50 [uA]. It is the only CALIBRATED, per-individual membrane-potential
dataset I found for Kcnk5b. The authors published no numerical table for it (PLOS
supplementary s001-s004 are TIFF figures; s005+ return HTTP 404), so the values are
recovered from the figure image.

WHAT THIS IS: a computed extraction from a published raster image. It is NOT an
author-reported measurement and NOT an observation of mine. Axis calibration comes from
detected tick-mark pixels, so the dominant error is marker-centroid rounding (~1 mV) plus
whatever markers are occluded by overlap -- see the OCCLUSION note printed at the end.

Fetch the input (one file, ~720 KB):
  curl -sSL "https://journals.plos.org/plosgenetics/article/figure/image?size=large&id=10.1371/journal.pgen.1004080.g005" -o g005.png
Run:
  python3 -I docs/research/fish/S14-D-D-digitize.py g005.png
Requires Pillow and numpy.
"""
import sys, math, statistics as st
from PIL import Image
import numpy as np

src = sys.argv[1] if len(sys.argv) > 1 else "g005.png"
full = Image.open(src).convert("RGB")
if full.size != (1875, 1123):
    print(f"WARNING: expected the 1875x1123 'large' render, got {full.size}; "
          "the hard-coded panel crop and tick rows below will not apply.")
a = np.array(full.crop((1150, 560, 1875, 1123))).astype(int)   # panel D
H, W, _ = a.shape

Y0, Y75 = 73.5, 405.0        # image rows of the 0 mV and -75 mV major ticks
X0, X40 = 154.0, 695.0       # image cols of the 0 uA and 40 uA major ticks
to_val = lambda r, c: ((Y0 - r)/(Y75 - Y0)*75.0, (c - X0)/(X40 - X0)*40.0)

SERIES = {"wt": (188, 190, 192), "W169L": (27, 117, 188), "F241Y": (46, 48, 146)}
MARKER_PX = 120              # a marker disc is ~300 px; anything smaller is anti-aliasing
LEGEND_COL, LEGEND_ROW = 430, 210

out, merged = {}, []
for name, rgb in SERIES.items():
    mask = (np.abs(a - np.array(rgb)).sum(2) < 40)
    mask[:, :155] = False; mask[472:, :] = False       # strip the axes and their labels
    seen = np.zeros(mask.shape, bool); pts = []
    for r in range(H):
        for c in range(W):
            if not mask[r, c] or seen[r, c]:
                continue
            stack, pix = [(r, c)], []
            seen[r, c] = True
            while stack:
                y, x = stack.pop(); pix.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    y2, x2 = y+dy, x+dx
                    if 0 <= y2 < H and 0 <= x2 < W and mask[y2, x2] and not seen[y2, x2]:
                        seen[y2, x2] = True; stack.append((y2, x2))
            if len(pix) < MARKER_PX:
                continue
            rc = sum(p[0] for p in pix)/len(pix); cc = sum(p[1] for p in pix)/len(pix)
            if cc > LEGEND_COL and rc < LEGEND_ROW:
                continue                                # legend swatch, not a data point
            v, i = to_val(rc, cc)
            if len(pix) > 420:
                merged.append((name, round(i, 1), round(v, 1), len(pix)))
            pts.append((round(i, 1), round(v, 1)))
    out[name] = sorted(pts)

print("COMPUTED EXTRACTION from a published figure -- not author-reported, not observed.\n")
for name, pts in out.items():
    vs = [p[1] for p in pts]
    print(f"{name}: n={len(pts)}  Vm mean={st.mean(vs):6.1f}  SD={st.stdev(vs):5.1f}  "
          f"range=[{min(vs):.1f}, {max(vs):.1f}] mV")
    for i, v in pts:
        print(f"      I50={i:5.1f} uA   Vm={v:6.1f} mV")
allv = [p[1] for s in out.values() for p in s]
print(f"\npooled: n={len(allv)} mean={st.mean(allv):.1f} SD={st.stdev(allv):.1f} mV")

pts = [(i, v) for s in out.values() for i, v in s]
n = len(pts); mx = sum(p[0] for p in pts)/n; my = sum(p[1] for p in pts)/n
b = sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts)
res = [v - (my + b*(i-mx)) for i, v in pts]
print(f"pooled OLS slope {b:.3f} mV/uA; residual SD at fixed I50 = "
      f"{math.sqrt(sum(r*r for r in res)/(n-2)):.1f} mV")

print("\nOCCLUSION note (states the error in both directions):")
for m in merged:
    print(f"  blob of {m[3]} px in series {m[0]} at I50={m[1]}, Vm={m[2]} is >1 marker merged; "
          "it is counted once, so the true n is higher than reported above.")
print("  Fig 5C reports n = 8 (wt), 11 (W169L), 12 (F241Y) for the I-V curves. This extraction"
      "\n  recovers fewer points than that in every series. If the missing markers are hidden in"
      "\n  the dense centre of each cloud, the SDs above are OVERESTIMATES; if they are in the"
      "\n  tails, underestimates. Section 4c of S14-D-D.md carries this through to the verdict.")
