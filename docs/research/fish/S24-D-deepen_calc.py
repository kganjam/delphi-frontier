"""S24-D-D: sensitivity of S24-D's 3-BL taxi verdict to f_max, and recomputation with the
improved f_max reading. Every output is a CALCULATION. See S24-D-deepen.md for sources.
Run: python3 S24-D-deepen_calc.py
"""
import math

U = 1.95                       # m/s, 3-BL glide target (inherited)
L = 0.040                      # m, project premise TL
LAMBDA = (0.8, 0.7, 0.6)       # stride, L/beat (Wardle 1975 via S24-D)
LAMBDA_FF = 0.48               # flying-fish taxi stride lower end (challenge 85, calc on relayed obs)
F52 = 52.0                     # Hz, Kyriakatos 2011 max across animals during escape

def f_req(lam, Lx=L):
    return U / (lam * Lx)

req = [f_req(l) for l in LAMBDA]
print("Requirement at L 40 mm:", ", ".join(f"lambda {l}: {f:.1f} Hz" for l, f in zip(LAMBDA, req)),
      f"; flying-fish lambda {LAMBDA_FF}: {f_req(LAMBDA_FF):.1f} Hz")

print("\n1. Sensitivity of S24-D's answer (ratio f_req/f_max; S24-D band 1.17-1.56)")
for name, fr, fm in (("as recorded", 1, 1), ("f_max x2", 1, 2), ("f_max /2", 1, 0.5),
                     ("lambda x2", 0.5, 1), ("lambda /2", 2, 1)):
    lo, hi = req[0] * fr / (F52 * fm), req[2] * fr / (F52 * fm)
    print(f"  {name:12s}: {lo:.2f}-{hi:.2f}")
print(f"  break-even f_max = {req[0]:.0f}-{req[2]:.0f} Hz; break-even lambda at 52 Hz = {U/(F52*L):.2f} L/beat")

print("\n2. Spread of each input across sources on record (max/min)")
print(f"  lambda 0.48..0.8 (Wardle, Bainbridge, flying-fish taxi): {0.8/0.48:.2f}x")
print(f"  f_max candidates 21 (sustained) .. 52 (single escape peak): {52/21:.2f}x")

print("\n3. Size scaling of f_max from Kyriakatos fish (18-30 mm) to 40 mm, f ~ L^-x")
# x bracket 0..1 is an ASSUMPTION; x from larval 95-100 Hz at ~4 mm (search-summary, length assumed)
for fl in (95.0, 100.0):
    for Lref in (0.018, 0.024, 0.030):
        x = math.log(fl / F52) / math.log(Lref / 0.004)
        print(f"  larval {fl:.0f} Hz @ 4 mm vs 52 Hz @ {Lref*1e3:.0f} mm: x = {x:.2f}")
for x in (0.0, 0.25, 0.35, 0.5, 1.0):
    for Lref in (0.018, 0.024, 0.030):
        s = (Lref / L) ** x
        print(f"  x {x:.2f}, Lref {Lref*1e3:.0f} mm: factor {s:.2f} -> 52 Hz becomes {F52*s:.1f}, "
              f"42 Hz becomes {42*s:.1f}, 30 Hz becomes {30*s:.1f}")

print("\n4. Recomputed ratio f_req/f_max (L 40 mm, lambda 0.8-0.6; flying-fish 0.48 in brackets)")
cases = [("52 Hz, single max across animals (S24-D input)", 52),
         ("42 Hz, top of usual escape range 'slightly >40'", 42),
         ("30 Hz, bottom of usual escape range", 30),
         ("43 Hz, 52 Hz size-scaled x=0.35 Lref 24 mm", F52 * (0.024 / L) ** 0.35),
         ("35 Hz, 42 Hz size-scaled x=0.35 Lref 24 mm", 42 * (0.024 / L) ** 0.35),
         ("25 Hz, 42 Hz size-scaled x=1 Lref 24 mm", 42 * (0.024 / L) ** 1.0),
         ("21 Hz, max steady swimming", 21)]
for name, fm in cases:
    print(f"  {name:48s} f_max {fm:5.1f}: {req[0]/fm:.2f}-{req[2]/fm:.2f}  ({f_req(LAMBDA_FF)/fm:.2f})")

print("\n5. Beats needed vs beats observed")
print("  S24 taxi run: 12-46 beats at 52 Hz (S24 sec 3.4); observed escape bouts: 3-5 cycles (Kyriakatos)")
print(f"  shortfall in bout length: {12/5:.1f}-{46/3:.1f}x")
