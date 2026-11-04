"""S25-D-D: sensitivity of S25-D's conclusion, and recomputation with the re-read Alben 2007 test geometry.

Every number printed here is a CALCULATION from stated inputs. None is an observation.
Run: python3 -I docs/research/fish/S25-D-deepen_calc.py
"""

B565 = 565e-6   # N m^2, Flammang et al. 2013 abstract ("calculated"); abstract read-level
A38 = 3.8e-6    # N m^2, Puri et al. 2018 relay of Flammang 2013; full-text read-level (via S25-D)
k = 1.98        # N/m, Alben et al. 2007, both hemitrich bases clamped (quoted)
L = 40.3e-3     # m, Alben 2007 "maximum ray length" of the fins (quoted); NOT the length of each tested ray

# Uniform Euler-Bernoulli cantilever. Load F at distance a from the clamp; deflection read at distance x.
# x <= a: d = F x^2 (3a - x) / (6 EI);  x >= a: d = F a^2 (3x - a) / (6 EI).
def coeff(a, x):
    """Return c such that EI = c * k * L^3, with a and x given as fractions of L."""
    if x <= a:
        g = x * x * (3 * a - x) / 6
    else:
        g = a * a * (3 * x - a) / 6
    return g  # k = F/d = EI/(g L^3)  ->  EI = g k L^3


cases = [
    ("S25-D: load & read at L/2", 0.5, 0.5),
    ("S25-D: load & read at 2L/3", 2 / 3, 2 / 3),
    ("S25-D: load & read at L", 1.0, 1.0),
    ("NEW: load at 2L/3, deflection read at tip", 2 / 3, 1.0),
]
print("== Recomputed EI from Alben's k under each test geometry ==")
base = {}
for name, a, x in cases:
    EI = coeff(a, x) * k * L ** 3
    base[name] = EI
    print(f"  {name:45s} EI = {EI:.3e} N m^2;  565e-6/EI = {B565/EI:6.1f}x;  3.8e-6/EI = {A38/EI:.2f}x")

ref = base["S25-D: load & read at 2L/3"]
print("\n== Sensitivity of the gap (565e-6 / EI) to a factor-of-2 change in each input, at the 2L/3 case ==")
gap0 = B565 / ref
print(f"  baseline gap: {gap0:.1f}x")
print(f"  k x2   -> EI x2  -> gap {gap0/2:.1f}x;  k /2 -> gap {gap0*2:.1f}x")
print(f"  lever (L or a) x2 -> EI x8  -> gap {gap0/8:.1f}x")
print(f"  Flammang ray 2x longer than Alben's, isometric (EI ~ L^4) -> EI x16 -> gap {gap0/16:.2f}x")
for name in base:
    print(f"     same x16 applied to '{name}': gap {B565/base[name]/16:.2f}x")
print(f"  E or I alone x2 (Alben's EI ~ 1e-6..1e-5 bracket) -> gap halves; 565e-6 / 1e-5 = {B565/1e-5:.1f}x")

print("\n== Ray length Flammang's ray would need for 565e-6 to be a clamped single ray (EI ~ L^4) ==")
for name, EI in base.items():
    s = (B565 / EI) ** 0.25
    print(f"  {name:45s} scale {s:.2f} -> ray length {s*L*1e3:.0f} mm")

print("\n== Independent anchor: Aiello et al. 2018 (Labridae pectoral rays, three-point bending) ==")
# Abstract: 'ranged from 0.0001 to 1.5109 uN m2'. 1 uN m^2 = 1e-6 N m^2, so the max is 1.5109e-6 N m^2
# and the min is 1e-10 N m^2.
amax = 1.5109e-6
print(f"  max labrid pectoral ray EI = {amax:.2e} N m^2; 565e-6 / max = {B565/amax:.0f}x; 3.8e-6 / max = {A38/amax:.1f}x")

print("\n== Abstract-internal check: curvature a 67 mN impact would cause in a 40 mm cantilever ==")
F = 0.067  # N, Flammang 2013 abstract, force at impact (quoted)
for lbl, EI in (("565e-6", B565), ("3.8e-6", A38), ("Alben 2L/3 clamped", ref)):
    kap = F * L / EI  # max moment / EI if the whole force acted at the tip (upper bound on linear curvature)
    print(f"  EI {lbl:20s}: kappa_max (linear, tip load) = {kap:.3g} 1/m = {kap/1e3:.3g} 1/mm")
print("  abstract reports: <=0.029 (proximal) and <=0.065 1/mm (distal) in normal swimming; 9.38 1/mm under impact (buckling)")
