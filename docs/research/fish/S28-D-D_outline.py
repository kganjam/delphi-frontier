"""S28-D-D: planimetry of the dashed pectoral-fin outline of the representative
lat4a^nr21/+; kcnh2a^lof/+ fish in Daane et al. 2021 preprint Fig 8A (bottom-left image).

Vertices were read BY EYE from an ASCII dump of dark (max RGB < 70) pixels of fig8-000.png,
region x 70-250, y 560-615 (see doc S28-D-D-deepen.md section 3.3). Coordinates are local
(x - 70, y - 560). The bracket (dark line, row 641, x 85-232 = 148 px) is the authors'
"length of pectoral fin". This is a FIGURE-READ of ONE representative fish, fin ADDUCTED
(folded against the body), lateral view. It is not a spread-fin planform.
"""
import numpy as np
upper = [(6,39),(9,36),(16,35),(24,33),(28,31),(36,29),(44,26),(55,23),(64,20),(76,17),(85,16),
         (97,14),(107,13),(115,11),(130,11),(150,11),(163,12),(166,15),(175,20),(175,25)]
lower = [(170,27),(165,30),(150,31),(140,32),(115,33),(100,34),(85,36),(76,37),(64,39),(56,41),
         (47,43),(43,44),(38,45),(31,46),(27,46),(23,44),(19,41)]
P = np.array(upper + lower, float)
x, y = P[:, 0], P[:, 1]
A = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
ext = x.max() - x.min()
Lb = 148.0                      # bracket length, px
SL_px = (287.0, 277.0, 297.0)   # snout x~13 to caudal-fin origin x~300 +/- 10 px (eye-read)
print(f"outline area {A:.0f} px^2; outline x-extent {ext:.0f} px; bracket {Lb:.0f} px")
for L in (Lb, ext):
    print(f"  shape factor A/L^2 with L={L:.0f} px: {A/L**2:.3f};  mean width A/L = {A/L:.1f} px = {A/L/L:.3f} L")
for s in SL_px:
    print(f"  SL {s:.0f} px -> bracket/SL {Lb/s:.3f}; area/SL^2 (one fin, folded) {A/s**2:.4f}")
# compare with S28 geometry rules at the measured median length 0.463 SL (per fin)
Lf = 0.463
kA = A / Lb**2
print(f"\nPer fin, in units of SL^2, at L = {Lf} SL:")
print(f"  folded-outline shape factor x L^2: {kA*Lf**2:.4f}")
print(f"  rule A (0.7 x L x 0.1 SL):        {0.7*Lf*0.1:.4f}")
span = 2*Lf + 0.004/0.030
print(f"  rule C (span^2/5 /2):             {span**2/5/2:.4f}   (span {span:.3f} SL)")
