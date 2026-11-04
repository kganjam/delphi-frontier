"""Challenge 143: independent arithmetic. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/challenge-143_calc.py"""
from math import sqrt, sin, radians

g = 9.81
v1m = sqrt(g * 1.0 / sin(radians(90)))          # R = v^2 sin(2a)/g at a = 45 deg
print(f"v for 1 m range at 45 deg, drag-free: {v1m:.3f} m/s")
print(f"  apex of THAT trajectory v^2 sin^2(45)/(2g): {v1m**2*0.5/(2*g)*100:.1f} cm"
      f"  (vertical-jump height v^2/2g: {v1m**2/(2*g)*100:.1f} cm)")

mu, sd = 1.57, 0.27            # Demesmay 2025 controls, mean +/- SD (verified, full-text)
mu_m, sd_m = 1.61, 0.33        # mutants
for lab, v in [("mean", mu), ("+1 SD", mu + sd), ("+2 SD", mu + 2*sd), ("mutant mean", mu_m),
               ("mutant +2 SD", mu_m + 2*sd_m)]:
    print(f"  {lab:13s} v={v:.2f}  deficit x{v1m/v:.3f}  45deg range {v*v/g*100:.1f} cm"
          f"  45deg apex {v*v/(4*g)*100:.1f} cm")
print(f"SDs above control mean to reach {v1m:.2f}: {(v1m-mu)/sd:.2f}")
boost = 1.24 / 1.02
print(f"  with guppy air/water x{boost:.3f}: need in-water {v1m/boost:.2f}, {(v1m/boost-mu)/sd:.2f} SD")
print(f"ratio to D&L Re inversion 27800*1e-6/0.033 = {27800e-6/0.033:.3f}: x{mu/(27800e-6/0.033):.3f}")
c = (33 / 18.5) ** (1 / 3)
print(f"S20-D-D proxies: central {1.13*c:.3f}, extreme {1.50*c:.3f}; extreme x2 = {3.0*c:.2f} (flips: {3.0*c>=v1m})")

# Timing check on what the 1.57 m/s peak can be
print("\nTiming: peak latency 8 +/- 4 ms precedes max C-bend at 13 +/- 5 ms (author values).")
dtheta = radians(180 - 47.08)   # head-trunk angle change straight -> minimal (author minimal angle)
for share, r in [(0.5, 0.008), (0.5, 0.010), (0.6, 0.012)]:
    w = share * dtheta / 0.013
    print(f"  head share {share}, head point {r*100:.1f} cm from pivot: mean head speed "
          f"{w*r:.2f} m/s during stage 1 (rotation only)")
print(f"40 ms mean of tracked point: {0.038/0.040:.2f} m/s")
for s1 in (0.0, 0.5, 1.0):
    print(f"  if {s1} cm covered in first 13 ms: stage-2 mean {(3.8-s1)/100/0.027:.2f} m/s")

# Drag check on the drag-free assumption (0.4 g, frontal ~0.25 cm^2, Cd 0.5: assumptions)
F = 0.5 * 1.2 * v1m**2 * 0.5 * 2.5e-5
print(f"\nair drag decel at {v1m:.2f} m/s: {F/4e-4:.2f} m/s^2 (vs g = 9.81)")
