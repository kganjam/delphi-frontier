"""Challenge 228 -- independent recomputation of S29's energy-per-stroke shortfall.
All outputs are DERIVED (calculation), none is a measurement.
Run: python3 docs/research/fish/challenge-228.py
"""
import itertools, math

RHO_W, A = 1000.0, 24e-6          # water; S28 frontal area (PROJECT input)
ETA_SP = 0.93                      # tendon return (S29 input, Ker 1981 abstract)

def need_per_kg(V, m, cd, s):
    """J/kg body delivered to the body: KE + drag work over a constant-accel stroke."""
    ke = 0.5 * V * V
    wd = 0.5 * RHO_W * cd * A * V * V * s / 2 / m
    return ke + wd

def shortfall(V=4.37, m=0.40e-3, cd=0.2, s=0.0109, eta_h=0.37, f=0.30, w=53.0):
    return need_per_kg(V, m, cd, s) / (f * w * ETA_SP * eta_h)

print("1. Central case and stated range (w only varied)")
for w in (81, 53, 32):
    print(f"   w={w:>2} J/kg muscle -> shortfall {shortfall(w=w):.3f}x")

print("\n2. 'Order of magnitude closer'? wing KE gap / LaMSA shortfall")
wing = (4.37 / 1.38) ** 2
print(f"   wing KE gap (S28 row 1, best fish) = {wing:.2f}x")
for tag, sf in [("central", shortfall()), ("best w=81", shortfall(w=81)),
                ("mass-consistent 5.53 m/s", shortfall(V=4.37 * math.sqrt(0.40 / 0.25)))]:
    print(f"   {tag:26s} shortfall {sf:.2f}x -> wing/LaMSA = {wing/sf:.1f}x closer")

print("\n3. Like-for-like baseline: requirement vs TODAY's per-stroke muscle work")
need = need_per_kg(4.37, 0.40e-3, 0.2, 0.0109)
today_w = 0.5 * 1.38 ** 2 / 0.37 / 0.30          # J/kg one-side muscle, S29's own derivation
req_w = need / (0.30 * ETA_SP * 0.37)
print(f"   today {today_w:.2f} J/kg muscle; required {req_w:.1f} J/kg muscle -> {req_w/today_w:.1f}x")
print(f"   share of the closure carried by the frog transfer: 53/{today_w:.2f} = {53/today_w:.2f}x "
      f"(81 -> {81/today_w:.2f}x, 32 -> {32/today_w:.2f}x)")

print("\n4. One-at-a-time relaxation from the central case")
cases = {
    "eta_h 0.34 (pike low)": dict(eta_h=0.34), "eta_h 0.39 (pike high)": dict(eta_h=0.39),
    "eta_h 0.27 (pike S-start)": dict(eta_h=0.27),
    "Cd 0.1, s 1.09": dict(cd=0.1), "Cd 0.3, s 3.0": dict(cd=0.3, s=0.03),
    "V 5.53 (mass-consistent)": dict(V=5.53),
    "m 0.25 g at 4.37 (S28 mass, same 24 mm2)": dict(m=0.25e-3),
    "f 0.60 (all muscle)": dict(f=0.60),
}
for k, kw in cases.items():
    print(f"   {k:42s} {shortfall(**kw):.2f}x")

print("\n5. Joint envelope over S29's own stated input ranges (w, eta_h C-start, Cd, s, V)")
vals = []
for w, eh, cd, s, V in itertools.product((32, 53, 81), (0.34, 0.37, 0.39), (0.1, 0.2, 0.3),
                                         (0.0109, 0.03), (4.37, 5.53)):
    vals.append(shortfall(V=V, cd=cd, s=s, eta_h=eh, w=w))
print(f"   min {min(vals):.2f}x  max {max(vals):.2f}x  (n={len(vals)})")
vals437 = [shortfall(V=4.37, cd=cd, s=s, eta_h=eh, w=w) for w, eh, cd, s in
           itertools.product((32, 53, 81), (0.34, 0.37, 0.39), (0.1, 0.2, 0.3), (0.0109, 0.03))]
print(f"   at 4.37 m/s only: min {min(vals437):.2f}x  max {max(vals437):.2f}x")

print("\n6. ASSUMED-input sanity bound on single-contraction muscle work, w = stress*strain/density")
for sig in (200e3, 300e3):
    for eps in (0.10, 0.20, 0.30):
        print(f"   stress {sig/1e3:.0f} kPa, fibre strain {eps:.2f}: w = {sig*eps/1060:.0f} J/kg "
              f"-> shortfall {shortfall(w=sig*eps/1060):.2f}x")
