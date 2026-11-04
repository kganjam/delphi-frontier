"""S25-D: sensitivity and recomputation for the Flammang 2013 fin-ray EI question.

Every output of this script is a CALCULATION from stated inputs, not an observation.
Run: python3 -I docs/research/fish/S25_deepen_calc.py
"""
import math

A = 3.8e-6     # N m^2, Puri et al. 2018 relay (full-text), attributed to Flammang 2013
B = 565e-6     # N m^2, Flammang et al. 2013 abstract (abstract read-level), "calculated"


def d_solid(EI, E):
    """Solid circular rod diameter (m) giving EI at modulus E."""
    return (64 * EI / (math.pi * E)) ** 0.25


def EI_solid(d, E):
    return E * math.pi * d ** 4 / 64


print("== 1. Sensitivity of each part of the S25 answer ==")
r = B / A
print(f"ratio B/A = {r:.2f}, log10 = {math.log10(r):.3f}")
for f in (0.5, 2.0):
    rr = r * f
    print(f"  ratio with one value moved x{f}: {rr:.1f} (log10 {math.log10(rr):.2f}) "
          f"-> power of ten? {abs(math.log10(rr) - round(math.log10(rr))) < 0.02}")

print("\nEI of a solid rod across Puri's quoted bluegill diameter range (1-2 mm):")
for E in (1e8, 1e9, 6.48e9, 1e10):
    vals = [EI_solid(d, E) for d in (0.5e-3, 1e-3, 2e-3)]
    print(f"  E={E:.2e} Pa: d=0.5mm {vals[0]:.2e}, d=1mm {vals[1]:.2e}, d=2mm {vals[2]:.2e} N m^2")
print("Diameter each value needs (solid rod):")
for E in (1e8, 1e9, 1e10):
    print(f"  E={E:.0e}: A needs {d_solid(A, E)*1e3:.2f} mm, B needs {d_solid(B, E)*1e3:.2f} mm")
print("x2 in d -> x16 in EI; x2 in E -> x2 in EI.")
print(f"  B's diameter at E=1GPa ({d_solid(B,1e9)*1e3:.2f} mm) halved -> EI = "
      f"{EI_solid(d_solid(B,1e9)/2,1e9):.2e} N m^2 (= {EI_solid(d_solid(B,1e9)/2,1e9)/A:.1f} x A)")

print("\nHemitrich (two bony layers) correction, rectangle idealisation, bone = 30% of thickness")
print("  (Alben 2007: 'bony segments take up about 30% of this thickness')")
frac = 1 - 0.7 ** 3
print(f"  I_bony / I_solid = 1 - 0.7^3 = {frac:.3f}  -> modest, cannot bridge 149x")

print("\n== 2. Improved input: Alben, Madden & Lauder 2007 (bluegill pectoral rays, same lab) ==")
k_clamped = 1.98       # N/m, both hemitrich bases clamped (quoted)
ratio_free = 12.0      # 'about 12 times the value when one hemitrich is free' (quoted)
L = 40.3e-3            # m, max ray length 40.3 +/- 0.8 mm (quoted)
print("cantilever, point load at a: k = 3EI/a^3  ->  EI = k a^3 / 3")
rows = []
for label, a in (("a = L/2", L / 2), ("a = 2L/3 (quoted load point)", 2 * L / 3), ("a = L", L)):
    EIc = k_clamped * a ** 3 / 3
    EIf = EIc / ratio_free
    rows.append((label, EIc, EIf))
    print(f"  {label:30s}: EI clamped {EIc:.2e}, one-free {EIf:.2e} N m^2; "
          f"B/EIclamped = {B/EIc:.0f}x, A/EIclamped = {A/EIc:.2f}x, A/EIfree = {A/EIf:.2f}x")

I_alben = 1e-6 * 1e-8   # 'I ~ 10^-6 cm^4' -> m^4
print(f"\nAlben 2007 order-of-magnitude I ~ 1e-6 cm^4 = {I_alben:.0e} m^4 "
      f"-> solid-equivalent d = {(64*I_alben/math.pi)**0.25*1e3:.2f} mm")
for E in (1e8, 1e9):
    print(f"  E={E:.0e} (Alben's composite range): EI = {E*I_alben:.0e} N m^2")
print(f"  E needed for B at that I: {B/I_alben:.2e} Pa ({B/I_alben/1e9:.1f} GPa)")
print(f"  E needed for A at that I: {A/I_alben:.2e} Pa ({A/I_alben/1e9:.2f} GPa)")

print("\n== 3. What ray length would make B consistent under isometric L^4 scaling? ==")
EIc = rows[1][1]
s = (B / EIc) ** 0.25
print(f"  (B / {EIc:.2e})^(1/4) = {s:.2f} -> ray length {s*L*1e3:.0f} mm (Alben rays {L*1e3:.1f} mm)")

print("\n== 4. Downstream: Puri's zebrafish check (x1e-4, 16-18 rays) ==")
for v, n in ((A, "A"), (B, "B")):
    print(f"  {n}: {v*1e-4*16:.1e} - {v*1e-4*18:.1e} N m^2 per fin "
          f"(Puri measured 1.5e-9 - 4e-9, quoted)")
