"""S45: arithmetic for the refute-from-below sweep. Every number printed here is a COMPUTATION
by this script, not an observation. Run: python3 -I docs/research/fish/S45_sweep_calc.py"""
import numpy as np

L   = 0.0403          # m, Alben 2007 §2: max bluegill pectoral ray length 40.3 +/- 0.8 mm (measured)
a   = 2.0 * L / 3.0   # m, load point ~2/3 base-to-tip (Alben 2007 Fig 7a caption, authors' statement)
k   = 1.98            # N/m, both hemitrich bases clamped (Alben 2007 Fig 7a, measured linear fit)
B_lo, B_hi = 1e-6, 1e-5   # N m^2, Alben 2007 §3.3 "measured B = EI ~ 10^-6-10^-5 J m" (3-pt bending)
FLAM = 565e-6         # N m^2, Flammang et al. 2013 abstract (authors call it "calculated")

print("== 1. Invert Alben's cantilever slope two ways (uniform EI) ==")
ei_loadpt = k * a**3 / 3.0                       # if 1.98 = force/deflection AT the load point
ei_tip    = k * a**2 * (3*L - a) / 6.0           # if 1.98 = force/TIP deflection (Alben §5.2 wording)
print(f"  load-point convention : EI = k a^3/3        = {ei_loadpt:.3e} N m^2")
print(f"  tip-deflection conv.  : EI = k a^2(3L-a)/6  = {ei_tip:.3e} N m^2")
print(f"  one-base-free (paper's 12x ratio): {ei_loadpt/12:.3e} to {ei_tip/12:.3e} N m^2")

print("\n== 2. Flammang's 565e-6 against Alben's OWN measured bending rigidity ==")
print(f"  565e-6 / Alben measured B: {FLAM/B_hi:.1f}x to {FLAM/B_lo:.1f}x above the measured range")
print(f"  565e-6 / apparent locked EI ({ei_tip:.2e}): {FLAM/ei_tip:.1f}x")

print("\n== 3. Does a STEPPED ray rescue 565e-6? (the test that kills the candidate) ==")
# Euler-Bernoulli cantilever, point load P at s=a, EI(s) = EI_p for s<f*L, EI_d beyond.
# Tip deflection by direct integration of M(s)/EI(s), M(s) = P*(a-s) for s<a, 0 beyond.
def tip_defl(P, EI_p, EI_d, frac):
    s = np.linspace(0.0, L, 400001)
    EI = np.where(s < frac*L, EI_p, EI_d)
    M  = np.where(s < a, P*(a-s), 0.0)
    th = np.concatenate(([0.0], np.cumsum(np.diff(s)*(M/EI)[:-1])))   # slope
    return np.trapezoid(th, s)                                        # deflection at the tip
P = 1.0
for frac in (0.40, 0.50, 0.60):
    # solve for the distal EI that reproduces k = 1.98 N/m with the proximal section at 565e-6
    lo, hi = 1e-10, 1e-3
    for _ in range(200):
        mid = (lo*hi)**0.5
        if P/tip_defl(P, FLAM, mid, frac) < k: lo = mid
        else: hi = mid
    EI_d = (lo*hi)**0.5
    print(f"  proximal {frac:.0%} at 565e-6 -> distal EI = {EI_d:.2e} N m^2 reproduces k = "
          f"{P/tip_defl(P, FLAM, EI_d, frac):.2f} N/m")

print("\n== 4. Project requirement figures the chain is compared against ==")
for name, req in (("S6 organ, 120 mm ray", 6.3e-4), ("S23 zebrafish central (L=4cm,tol=10%)", 3.924e-6),
                  ("S23 zebrafish lenient (L=2cm,tol=50%)", 1.962e-7)):
    print(f"  {name:40s} EI_req = {req:.3e} N m^2")
EI_ZF = (1.5e-9, 4e-9)
print(f"  measured adult zebrafish whole caudal fin EI (Puri 2018, via project): "
      f"{EI_ZF[0]:.1e}-{EI_ZF[1]:.1e} N m^2")
print(f"  shortfall vs S23 central : {3.924e-6/EI_ZF[1]:.0f}x to {3.924e-6/EI_ZF[0]:.0f}x")
