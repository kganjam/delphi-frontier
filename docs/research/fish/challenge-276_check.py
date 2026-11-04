"""Challenge 276 — independent recomputation. Every number printed is CALCULATED by me,
from inputs quoted in the claim and in the project's own earlier notes. I wrote this without
reading the author's S5-deepen_calc.py formulas back; the algebra below is derived from the
stated definitions (AR = span^2 / area; area ~ f^alpha; sector geometry).

Inputs and their status:
  p0_PR   wild-type pectoral/SL, Praveenraj-2017-derived bracket adopted by S22-D-D: 0.173-0.260
          (figure-read + resection-fraction inference, carried over).
  p0_IS   wild-type pectoral/SL from Islam et al. 2025 population means, 0.094-0.168
          (calculated from a table read by fetch-extraction; recorded in Challenge 147).
  f       pectoral length fold-change, kcnk5b^alf/+ = 1.74 (figure-read, carried over);
          2.05 caudal alf/+ used only as an upper proxy.
  A0      wild-type adult zebrafish pectoral AR. UNKNOWN (my searches below also failed).
  Targets Fish 1990 individual pectoral AR 3.0-16.9; Park & Choi 2010 Cypselurus 9.0-10.7
          (carried over from the repo source cards, not re-read by me).
"""
import math

F, F_HI = 1.74, 2.05

print("== A. Span = p0 * f  (CALCULATED; 'span' here is fin LENGTH, an upper bound on true span)")
for label, (lo, hi) in {"Praveenraj bracket 0.173-0.260": (0.173, 0.260),
                        "Islam 2025 means 0.094-0.168": (0.094, 0.168)}.items():
    print(f"  {label:32s} f=1.74 -> {lo*F:.3f}-{hi*F:.3f} SL   f=2.05 -> {lo*F_HI:.3f}-{hi*F_HI:.3f} SL")
print(f"  central 0.208 * 1.74 = {0.208*F:.4f} SL")
print(f"  union of BOTH p0 sources at f=1.74: {0.094*F:.3f}-{0.260*F:.3f} SL")
print(f"  claim's stated interval 0.30-0.45 covers the Islam side? "
      f"{0.094*F >= 0.30}  (Islam high end {0.168*F:.3f} SL is {0.30/(0.168*F):.2f}x below 0.30)")

print("\n== B. Scale-invariance of AR under uniform dilation (CALCULATED, algebraic)")
print("  AR = span^2/area; span -> f*span, area -> f^2*area  =>  AR -> AR. Invariant for any f.")
print("  With area ~ f^alpha: AR_reach = A0 * f^(2-alpha).")
for a in (2.0, 1.5, 1.0):
    m = F ** (2 - a)
    print(f"  alpha={a}: multiplier {m:.3f} -> A0 needed >= {3.0/m:.2f} (Fish90 low) "
          f">= {9.0/m:.2f} (Park&Choi low) >= {16.9/m:.2f} (Fish90 high)")

print("\n== C. Equal-ray sector: AR = 2/theta(rad). What spread each target demands (CALCULATED)")
for target in (3.0, 9.0, 16.9):
    th2 = math.degrees(2.0 / target)                    # alpha=2, no gain from f
    th1 = math.degrees(2.0 / (target / F))              # alpha=1, f buys 1.74x
    print(f"  AR {target:4.1f}: needs spread <= {th2:5.1f} deg (alpha=2)  or <= {th1:5.1f} deg (alpha=1)")
print("  Conversely, A0 implied by a given spread:")
for th in (30, 45, 60, 75, 90, 120):
    A0 = 2.0 / math.radians(th)
    print(f"    spread {th:3d} deg -> A0 = {A0:.2f}; reachable AR = {A0:.2f} (alpha=2), "
          f"{A0*F:.2f} (alpha=1); in Fish90 3.0-16.9? "
          f"{3.0 <= A0 <= 16.9} / {3.0 <= A0*F <= 16.9}")

print("\n== D. Finite root, rays elongated uniformly: does AR really stay fixed? (CALCULATED)")
print("  Model: sector area theta*L^2/2 plus a root strip ~ c*b*L (b = root chord, c = 0.5).")
for th_deg in (30, 60, 90):
    th = math.radians(th_deg)
    for b in (0.1, 0.25):
        ar = lambda L: L**2 / (th * L**2 / 2 + 0.5 * b * L)
        print(f"  spread {th_deg:3d} deg, root b={b}: AR {ar(1.0):.2f} -> {ar(F):.2f} "
              f"({ar(F)/ar(1.0):.3f}x) -> asymptote {2/th:.2f}")

print("\n== E. Span-as-length bias in any future A0 measurement (CALCULATED)")
print("  If the leading ray is swept back phi from the spanwise axis, true span = L*cos(phi).")
print("  Using L as span inflates AR by 1/cos^2(phi):")
for phi in (0, 15, 30, 45):
    c = math.cos(math.radians(phi))
    print(f"    phi={phi:2d} deg: span = {c:.3f}*L; AR inflation if L used = {1/c**2:.2f}x; "
          f"an apparent AR of 3.00 is really {3.0*c**2:.2f}")

print("\n== F. Differential overgrowth needed to lift a wide fan into each band (CALCULATED)")
print("  Leading ray x f*g, trailing x f, log-linear in between; equal-length baseline, 12 rays.")


def fan_AR(lengths, theta_deg, base=0.0):
    n = len(lengths)
    pts = [(0.0, 0.0)]
    for i, L in enumerate(lengths):
        phi = math.radians(theta_deg) * i / (n - 1)
        x0 = base * i / (n - 1)
        pts.append((x0 + L * math.sin(phi), L * math.cos(phi)))
    pts.append((base, 0.0))
    area = 0.5 * abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1]
                         for k in range(len(pts))))
    return max(p[1] for p in pts) ** 2 / area


n = 12
for th in (60, 90):
    base_ar = fan_AR([1.0] * n, th)
    print(f"  spread {th} deg, baseline AR {base_ar:.2f} (sector formula says {2/math.radians(th):.2f})")
    for g in (1.0, 1.5, 2.0, 3.0, 5.0, 8.0):
        L = [F * g ** (1 - i / (n - 1)) for i in range(n)]
        a = fan_AR(L, th)
        print(f"    g={g:4.1f}: AR -> {a:5.2f} ({a/base_ar:.2f}x)  reaches 3.0? {a>=3.0}  9.0? {a>=9.0}")
