"""S5-D-D calculations. Every number this script prints is CALCULATED. Nothing here is an observation.

Run: python3 -I S5-D-deepen_calc.py

Inputs (see S5-D-deepen.md for sources and read-levels):

  Carried over from the project's flying-fish print designs on origin/main @ 7b5ba52c:
    artifacts/print/design/C-four-wing-glider.json  (sha256 bd97309f...)  Cypselurus, 0.1 kg
    artifacts/print/design/B-two-wing-glider.json   (sha256 c9cdd477...)  Exocoetus,  0.1 kg
  Those files derive the values below from Fish 1990 Table I r.m.a. fits (wing span, wing area) and Table IV
  (pectoral share of wing area). The project records them as read full-text. I did NOT re-read Fish 1990
  (could-not-access in this session). The only assumption in them is body width at the fins (design_assumption).

  S5-D's own inputs, carried over unchanged: f = 1.74 (kcnk5b alf/+ pectoral fold-change), thresholds 3.0
  (Fish 1990 low end) and 9.0 (Park & Choi 2010 low end). A0 (WT zebrafish pectoral AR) is still UNKNOWN.
"""
import math

# --- carried-over design values (SI), per fin ---------------------------------------------------------
DESIGNS = {
    "Cypselurus 0.1 kg (form C)": dict(b=0.274524, w=0.03351169717517026, A_fin=0.0033790207334999994,
                                        S_wing=0.00889333, T3_fit=8.737449351660992, T3_range=(3.0, 12.2)),
    "Exocoetus 0.1 kg (form B)":  dict(b=0.322657, w=0.02792218494101567, A_fin=0.0038345315355,
                                        S_wing=0.00835137, T3_fit=14.941748211720746, T3_range=(8.9, 19.9)),
}

print("== 1. Re-derive the three AR conventions from the carried-over span/area values")
K = {}
for name, d in DESIGNS.items():
    L = (d["b"] - d["w"]) / 2                     # single-fin semispan, fin spread straight out
    single = L ** 2 / d["A_fin"]                  # single fin: semispan^2 / one fin area
    pair = d["b"] ** 2 / (2 * d["A_fin"])         # tip-to-tip span^2 / both pectoral areas
    whole = d["b"] ** 2 / d["S_wing"]             # tip-to-tip span^2 / whole wing area
    k = d["T3_fit"] / single
    K[name] = (single, k)
    print(f"  {name}: single {single:.2f}  pair {pair:.2f}  whole-wing {whole:.2f}  "
          f"| Table III fit {d['T3_fit']:.2f}")
    print(f"     Table III fit / single-fin = k = {k:.2f};  pair / single = {pair/single:.2f} "
          f"(= 2*(b/(b-w))^2 = {2*(d['b']/(d['b']-d['w']))**2:.2f})")
    print(f"     relative miss vs Table III fit: single {single/d['T3_fit']-1:+.0%}, pair {pair/d['T3_fit']-1:+.0%}, "
          f"whole {whole/d['T3_fit']-1:+.0%}")
k_lo = min(k for _, k in K.values()); k_hi = max(k for _, k in K.values())

print("\n== 2. Sensitivity: the S5-D verdict depends on the PRODUCT k*A0, not on A0 alone")
print("   'inside Fish 1990 envelope' means k*A0 >= 3.0. S5-D implicitly used k = 1.")
print("   A0(single-fin)   k=1 (S5-D)   k=2.03   k=2.64")
for A0 in (1.0, 1.25, 1.5, 2.0, 3.0, 4.0):
    cells = []
    for k in (1.0, k_lo, k_hi):
        cells.append("in " if k * A0 >= 3.0 else "out")
    print(f"   {A0:5.2f}            {cells[0]:10s}   {cells[1]:6s}   {cells[2]}")
print("   Doubling A0 and doubling k move the verdict identically: they enter only as k*A0.")

print("\n== 3. Improved thresholds, expressed in the single-fin convention S5-D's measurement protocol produces")
for label, T in (("Fish 1990 low end 3.0", 3.0), ("Park & Choi low end 9.0 (if same convention as Fish)", 9.0)):
    print(f"  {label}: A0_single >= {T/k_hi:.2f} .. {T/k_lo:.2f}   (S5-D said >= {T:.1f})")
for name, (single, _) in K.items():
    print(f"  mean {name} single-fin planform: A0_single >= {single:.2f}")

print("\n== 4. What spread a fan of equal rays needs for each threshold (sector AR = 2/theta; GEOMETRY MODEL)")
targets = {"Fish low end, single-fin equiv (hi k)": 3.0 / k_hi, "Fish low end, single-fin equiv (lo k)": 3.0 / k_lo,
           "mean Cypselurus single fin": K["Cypselurus 0.1 kg (form C)"][0],
           "mean Exocoetus single fin": K["Exocoetus 0.1 kg (form B)"][0],
           "S5-D's bar 3.0 (k=1)": 3.0, "S5-D's bar 9.0 (k=1)": 9.0}
for lab, ar in targets.items():
    print(f"  {lab:40s} AR {ar:5.2f} -> theta <= {math.degrees(2/ar):5.1f} deg")

print("\n== 5. Recompute S5-D's alpha table with the improved bars (f = 1.74; AR_reach = A0 * f^(2-alpha))")
for a in (2.0, 1.0):
    m = 1.74 ** (2 - a)
    print(f"  alpha={a}: Fish low end needs A0 >= {3.0/k_hi/m:.2f}..{3.0/k_lo/m:.2f}; "
          f"mean Cypselurus needs A0 >= {K['Cypselurus 0.1 kg (form C)'][0]/m:.2f}; "
          f"mean Exocoetus needs A0 >= {K['Exocoetus 0.1 kg (form B)'][0]/m:.2f}")
