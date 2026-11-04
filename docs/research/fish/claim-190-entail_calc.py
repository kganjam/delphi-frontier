"""Bounds and comparisons for docs/research/fish/claim-190-entail.md.
Every printed number is a CALCULATION, not an observation. Inputs are S28's
(m 0.25 g, S 192 mm2, CL_max 1.07, exit 1.38 m/s, 45 deg, SL 30 mm, body width 4 mm)
unless a line says otherwise. Run: python3 -I claim-190-entail_calc.py"""
import math
g, rho = 9.81, 1.225
m, S, CL, V0, SL, bw = 0.25e-3, 192e-6, 1.07, 1.38, 0.030, 0.004
W = m * g
frac = lambda V, S=S, m=m: 0.5 * rho * V**2 * S * CL / (m * g)
print(f"W = {W:.4e} N; L/W at {V0} = {frac(V0):.4f}; apex 45 deg = {frac(V0*math.cos(math.pi/4)):.4f}")

print("\n[C1] planform area band for 9-11 % W at 1.38 m/s")
for f in (0.09, 0.10, 0.11):
    print(f"  {f:.0%}: S = {f*W/(0.5*rho*V0**2*CL)*1e6:.0f} mm2")
L = 0.463 * SL                       # figure-read median per-fin length (S28-D-D)
for k in (0.13, 0.25):               # figure-read A/L^2 per fin (S28-D-D)
    Sf = 2 * k * L**2
    print(f"  A/L^2 = {k}: S = {Sf*1e6:.0f} mm2 -> L/W at 1.38 = {frac(V0, S=Sf):.3f}; "
          f"shortfall vs 177 mm2 = x{177e-6/Sf:.1f}")

print("\n[C2] per-fin length / SL band for span within x1.2 of 1 SL")
b0 = 2*0.45*SL + bw                  # S28's 31 mm
for b in (b0/1.2, b0*1.2):
    print(f"  span {b*1e3:.1f} mm -> l/SL = {(b-bw)/2/SL:.3f}")
for r in (0.449, 0.463, 0.488):
    print(f"  figure-read l/SL {r}: span = {(2*r*SL+bw)*1e3:.1f} mm = {(2*r*SL+bw)/SL:.2f} SL")

print("\n[C3] stiffness: tip deflection <= 10 % of fin length, uniform-load cantilever, one fin")
Lf = 0.0135
F = 0.5 * frac(V0) * W
EI = F * Lf**2 / (8 * 0.10)
print(f"  lift per fin {F:.3e} N; loading {F/(S/2):.2f} Pa; EI_req = {EI:.2e} N m2")
print(f"  mean chord of case-C fin = {(S/2)/Lf*1e3:.1f} mm (Puri caudal measured width 5-8 mm)")
for EIm in (1.5e-9, 4e-9):
    print(f"  Puri caudal EI {EIm:.1e}: ratio req/meas = {EI/EIm:.0f}x; small-deflection delta/L = {F*Lf**2/(8*EIm):.2f}")
print(f"  S28 quoted requirement 6.3e-5 / mine = {6.3e-5/EI:.0f}x")

print("\n[C4] exit-speed band for 9-11 % W at S = 192 mm2")
for f in (0.09, 0.10, 0.11):
    print(f"  {f:.0%}: V = {math.sqrt(f*W/(0.5*rho*S*CL)):.3f} m/s")
for V in (1.30, 1.57, 1.84):         # Demesmay 2025 mean -/+ 1 SD (in-water escape peak)
    print(f"  in-water peak {V} m/s -> L/W if it were the exit speed = {frac(V):.3f}")

print("\n[C5] airtime, apex time, abduction window (vacuum, 45 deg)")
T = 2 * V0 * math.sin(math.pi/4) / g
print(f"  airtime {T*1e3:.0f} ms; apex {T/2*1e3:.0f} ms; 10 % of airtime {T*100:.0f} ms")
print("  apex fraction vs launch angle:")
for th in (30, 38, 45, 50, 60, 75, 90):
    print(f"    {th} deg -> {frac(V0)*math.cos(math.radians(th))**2:.3f}")
for fa in (0.04, 0.06):
    print(f"  apex {fa:.0%} -> theta = {math.degrees(math.acos(math.sqrt(fa/frac(V0)))):.1f} deg")
