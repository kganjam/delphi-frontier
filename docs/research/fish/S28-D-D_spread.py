"""S28-D-D: planimetry of the partly abducted double-heterozygote pectoral fin, Daane et al. 2021
preprint Fig 8A, lower right panel (dorsal view, lat4a^nr21/+; kcnh2a^lof/+). FIGURE-READ of one fish.
The image has no scale bar, so only the dimensionless shape factor A/L^2 is used.
Fin pixels: mean RGB > THR inside x 510-646, y 478-688 of fig8-000.png (panel border and label excluded).
L = straight-line distance from the fin base (where fin pixels meet the body edge) to the most distal tip.
Usage: python3 -I S28-D-D_spread.py fig8-000.png"""
import sys
import numpy as np
from PIL import Image
im = np.array(Image.open(sys.argv[1]).convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 510, 646, 478, 688
sub = im[Y0:Y1, X0:X1].mean(2)
for THR in (150, 165, 180):
    m = sub > THR
    ys, xs = np.nonzero(m)
    count = m.sum()
    fill = 0
    for y in range(m.shape[0]):
        r = np.nonzero(m[y])[0]
        if len(r): fill += r.max() - r.min() + 1
    # base: fin pixels in the top-right corner (closest to body edge); tip: farthest fin pixel from it
    top = ys < ys.min() + 8
    base = np.array([xs[top].mean(), ys[top].mean()])
    d = np.hypot(xs - base[0], ys - base[1])
    L = d.max()
    print(f"THR {THR}: pixels {count}, row-filled {fill}; base ~({base[0]+X0:.0f},{base[1]+Y0:.0f}),"
          f" tip ({xs[d.argmax()]+X0},{ys[d.argmax()]+Y0}), L {L:.0f} px;"
          f" A/L^2 = {count/L**2:.3f} (pixel count) to {fill/L**2:.3f} (row-filled)")
