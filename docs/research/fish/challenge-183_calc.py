"""Challenge 183 arithmetic (independent of S20-deepen_calc.py). Every output is CALCULATED.
Run: python3 docs/research/fish/challenge-183_calc.py"""
from math import sqrt, sin, cos, radians
g, rho = 9.81, 1.2
def R(v, a=45): return v*v*sin(radians(2*a))/g          # drag-free range from the surface
def T(v, a=45): return 2*v*sin(radians(a))/g
def H(v, a=45): return (v*sin(radians(a)))**2/(2*g)
def S(v, m=4e-4, CL=1.0): return 2*m*g/(rho*CL*v*v)      # glide area to support weight at v
v1m, v10cm = sqrt(g*1.0), sqrt(g*0.10)
print(f"v needed: 1 m range {v1m:.3f} m/s, 0.10 m range {v10cm:.3f} m/s")

# 1. Re inversion, as the claim states it
Re, se, nu = 27800, 2140, 1.0e-6
for L, lab in ((0.033, "TL 33 mm (claim)"), (0.027, "if Re used SL ~27 mm (hypothetical; length basis unread)")):
    U = Re*nu/L; lo, hi = (Re-se)*nu/L, (Re+se)*nu/L
    print(f"U from Re, {lab}: {U:.3f} m/s ({lo:.3f}-{hi:.3f}); 45-deg range {R(U)*100:.1f} cm; "
          f"apex {H(U)*100:.2f} cm; aloft {T(U):.3f} s; glide area {S(U)*1e4:.0f} cm^2; "
          f"1 m deficit x{v1m/U:.2f}; 0.1 m deficit x{v10cm/U:.2f}")
m = 4e-4
for E in (15.0, 37.0):
    print(f"  launch cost at 0.842 m/s, eta 0.10, SMR {E} J/d: {0.5*m*0.842**2/0.10/E:.2e} of daily SMR")

# 2. Guppy-class comparator as the claim builds it
vg = sqrt(2*g*3.5*0.033)
print(f"guppy-class 3.5 BL vertical, L=33 mm: v={vg:.3f} m/s; 1 m deficit x{v1m/vg:.3f}; 45-deg range {R(vg)*100:.1f} cm")

# 3. Demesmay et al. 2025 measured adult escape maximal speed (full text re-read this session)
for lab, v in (("control mean", 1.57), ("control +1 SD", 1.84), ("control +2 SD", 2.11),
               ("mutant mean", 1.61), ("40-ms mean speed 3.8 cm/40 ms", 0.038/0.040)):
    print(f"Demesmay {lab:28s} v={v:.3f}: 45-deg range {R(v)*100:5.1f} cm, aloft {T(v):.3f} s, "
          f"1 m deficit x{v1m/v:.2f}, 0.1 m reachable: {v>=v10cm}")
print(f"source disagreement: 1.57 / 0.842 = x{1.57/0.842:.2f} in speed, x{(1.57/0.842)**2:.2f} in range")
