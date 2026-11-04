"""Bounds used in claim-272-entail.md. All DERIVED from S32's ceiling law
U_max = f*A_pp*sqrt(c6/C_D), c6 = 2.55 (Floryan 2017 pitching fit, via S32).
Nothing here is a measurement."""
from math import sqrt
c6 = 2.55
nu = 1.0e-6

def cd_scaled(Re):  # S32's "scaled" branch: 0.08 at Re 9560, Re^-1/2 outside
    return 0.08 * min(1.0, sqrt(9560 / Re))

print("C1 exocoetid: C_D needed for U_max >= V_to, r = f*A_pp/V_to")
for r in (0.087, 0.095, 0.10):
    print(f"  r={r:.3f}  C_D <= {c6*r*r:.4f}")
print("C2 zebrafish: C_D needed for U_max < V_to")
for r in (0.095, 0.103):
    print(f"  r={r:.3f}  C_D >  {c6*r*r:.4f}")
for Re in (8e3, 1.7e4, 2.6e4):
    print(f"  scaled C_D at Re {Re:.0e} = {cd_scaled(Re):.4f}")
print("C3 exocoetid A_pp implied by r=0.087-0.103 at V_to 15 m/s, L 0.256 m")
for f in (13.5, 50.0, 70.0):
    lo, hi = 0.087*15/f, 0.103*15/f
    print(f"  f={f:5.1f} Hz  A_pp {lo*100:.1f}-{hi*100:.1f} cm = {lo/0.256:.2f}-{hi/0.256:.2f} L")
print("C5 juvenile exocoetid, L = 5 cm, geometric similarity with S32 adult (25.6 cm, 191 g, chord 2.5 cm)")
s = 5/25.6
M = 0.191 * s**3
WL = 285.0 * M**0.400          # Fish 1990 Table II, extrapolated far below its range
Vto = sqrt(2*WL/(1.225*1.07))
c = 0.025 * s
for U in (Vto/2, Vto):
    Re = U*c/nu
    cd = cd_scaled(Re)
    print(f"  M={M*1e3:.2f} g Vto={Vto:.2f} U={U:.2f} Re={Re:.2e} C_D={cd:.4f} r_needed={sqrt(cd/c6):.3f} "
          f"U_max/Vto at r=0.095: {0.095*sqrt(c6/cd):.2f}")
