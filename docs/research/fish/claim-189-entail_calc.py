"""Calculations for claim-189-entail.md. Every output is a CALCULATION, not an observation.
Inputs: m = 0.25 g, SL = 3.0 cm (assumed, from S28); CL_max = 1.07 (project-derived);
rho_air = 1.225 kg/m^3; speeds are zebrafish in-water escape peaks relayed in the repository
(Miln 2021 1.38 m/s; Demesmay 2025 1.57 +/- 0.27 m/s) -- stand-ins, not exit speeds."""
import math
g, rho, CL, m, SL = 9.81, 1.225, 1.07, 0.25e-3, 0.030
W = m * g

def S_for_LW(V):  # pair planform area (m^2) at which lift = weight
    return 2 * W / (rho * V**2 * CL)

print("C1: pair area needed for L=W")
for V in (1.38, 1.57, 2.11):
    S = S_for_LW(V) * 1e6
    print(f"  V={V:.2f} m/s  S={S:.0f} mm2  x over 96 mm2 = {S/96:.1f}  x over 202 mm2 = {S/202:.1f}")

print("C2: skim frequency requirement as period")
for f in (132, 199, 95, 100, 52):
    print(f"  {f} Hz -> {1000/f:.1f} ms")

print("C3: exit-speed bounds")
V3 = 1.38 * math.sqrt(3)
print(f"  3x ballistic range needs V = {V3:.2f} m/s; flight needs 4.37 m/s (S28 case C)")
r = 123.57 / 102.36  # guppy (Poecilia reticulata) in-air peak / in-water peak, Soares & Bierman 2013
print(f"  guppy in-air/in-water peak ratio = {r:.3f}")
for V in (1.38, 1.57, 2.11):
    print(f"  zebrafish {V:.2f} x {r:.3f} = {V*r:.2f} m/s  (cross-species transfer, hypothetical)  "
          f"range x{(V*r/1.38)**2:.2f} of 19.4 cm baseline")
print(f"  guppy check: v for 6.54 cm vertical = {math.sqrt(2*g*0.0654):.2f} m/s")

print("C5: per-fin length needed for L=W at fixed planform shape A/L^2 = k per fin")
for V in (1.38, 2.11):
    S = S_for_LW(V)
    for k in (0.13, 0.25, 0.523):
        L = math.sqrt(S / (2 * k))
        print(f"  V={V:.2f} k={k:.3f}: L = {L*1000:.1f} mm = {L/SL:.2f} SL  "
              f"(x{L/SL/0.463:.1f} the double-het median 0.463 SL)")
