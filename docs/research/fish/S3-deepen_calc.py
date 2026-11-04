#!/usr/bin/env python3
"""S3-D: sensitivity of S3's power and self-carry conclusions, and recompute with an improved CL_max.

Everything printed is COMPUTATION on stated inputs. Nothing is a measurement.
The model is S3's own (S3_budget.py, copied verbatim from claude/s3-organism-mass-budget-000ync @ d0fd062f).
Run: python3 -I docs/research/fish/S3-deepen_calc.py
"""
from math import sqrt

g, rho = 9.81, 1.225
m_body = 0.40e-3
P_AVAIL = 142.7                      # W/kg muscle, Wakeling & Johnston 1998 (abstract, via S3)
SIG_C = (0.8 * 1050 + 0.2 * 1557) * 120e-6   # S3 central areal density, kg/m^2

BASE = dict(CL=1.07, sigma=SIG_C, eta=0.37, fm=0.6, s_bl=2.0, P=P_AVAIL, m=m_body, S=1070e-6, BL=0.04)


def ratio(CL, sigma, eta, fm, s_bl, P, m, S, BL):
    """S3 sec 3.5 model: required mean W/kg muscle divided by available."""
    M = m + sigma * S
    V = sqrt(2 * M * g / (rho * S * CL))
    t = 2 * s_bl * BL / V
    Pm = (V**2 / 2) / t / eta * M / (fm * m)
    return Pm / P, Pm, V


def selfcarry_margin(CL, sigma, V=1.38):
    """>1 means fin tissue cannot carry itself at V (S3 sec 3.1)."""
    return sigma / (0.5 * rho * V**2 * CL / g)


def hr(t):
    print("\n" + t + "\n" + "-" * len(t))


hr("0. Reproduce S3 (controls)")
r, Pm, V = ratio(**BASE)
print(f"S10, 2 BL, eta 0.37, f_m 0.6: V_to {V:.2f} m/s, {Pm:.0f} W/kg muscle, {r:.2f}x short  (S3: 2.77, 409, 2.9x)")
r28, Pm28, V28 = ratio(**{**BASE, "S": 192e-6})
print(f"S28 C, 2 BL: V_to {V28:.2f}, {Pm28:.0f} W/kg, {r28:.1f}x (S3: 5.77, 2878, 20x)")
print(f"self-carry margin at 1.38 m/s, central sigma, CL 1.07: {selfcarry_margin(1.07, SIG_C):.3f} (S3: 0.138 vs 0.127)")
assert abs(Pm - 409) < 2 and abs(Pm28 - 2878) < 10

hr("1. x2 and x0.5 on each input, most generous case (S10, 2 BL, eta 0.37, f_m 0.6)")
for k in ("CL", "sigma", "eta", "fm", "s_bl", "P", "m"):
    out = []
    for f in (2.0, 0.5):
        r_, _, _ = ratio(**{**BASE, k: BASE[k] * f})
        out.append(f"x{f:g}: {r_:5.2f}x short")
    print(f"{k:6s} " + "   ".join(out))
print("elasticity of required/available to CL (numerical):",
      f"{(ratio(**{**BASE,'CL':1.07*1.001})[0]/r - 1)/0.001:.2f}")
print("\nself-carry claim (margin >1 = fin cannot lift itself at 1.38 m/s):")
for f in (2.0, 0.5):
    print(f"  CL x{f:g}: {selfcarry_margin(1.07*f, SIG_C):.2f}   sigma x{f:g}: {selfcarry_margin(1.07, SIG_C*f):.2f}")
print(f"  CL that flips self-carry: {1.07*selfcarry_margin(1.07, SIG_C):.3f}")
# CL needed for closure of the generous case
lo, hi = 1.0, 10.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if ratio(**{**BASE, "CL": mid})[0] > 1 else (lo, mid)
print(f"CL_max needed to close the most generous case: {hi:.2f}")
for S in (192e-6, 900e-6):
    lo, hi = 1.0, 200.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ratio(**{**BASE, "S": S, "CL": mid})[0] > 1 else (lo, mid)
    print(f"  CL needed, S = {S*1e6:.0f} mm2, 2 BL, eta .37, f_m .6: {hi:.2f}")

hr("2. Recompute with alternative CL_max values (see S3-deepen.md sec 3 for sources/read-levels)")
CASES = [
    ("S3 baseline: W&E 1997 isolated dragonfly/damselfly wing", 1.07),
    ("W&E 1997 C. splendens isolated wing", 1.15),
    ("W&E 1997 max CL in free glides (whole insect)", 0.93),
    ("flying fish wind tunnel, Park & Choi IUTAM 2007, low end (search-summary)", 1.0),
    ("flying fish wind tunnel, Park & Choi IUTAM 2007, high end (search-summary)", 1.1),
    ("flying fish CFD, C. hiraii-like model, 2019 Bioinspir Biomim (abstract)", 1.03),
    ("flying fish, 0.78 as relayed by S7 (UNCONFIRMED: replicate-201 found it absent from abstract)", 0.78),
    ("SCENARIO, not a source: CL needed to close the most generous case", 2.16),
]
for label, CL in CASES:
    r_g, P_g, V_g = ratio(**{**BASE, "CL": CL})
    r_h, P_h, V_h = ratio(**{**BASE, "S": 192e-6, "CL": CL})
    sc = selfcarry_margin(CL, SIG_C)
    print(f"{label:72s} CL {CL:4.2f}: generous {P_g:5.0f} W/kg ({r_g:4.2f}x, V {V_g:.2f}); "
          f"S28-C {r_h:5.1f}x (V {V_h:.2f}); self-carry margin {sc:.2f}")

hr("3. Reynolds number of the designed wings at V_to (chord = S / span)")
nu = 1.5e-5
for label, S, span, CL in [("S10 (R 4 cm, AR 6)", 1070e-6, 0.08, 1.07), ("S28 C (AR 5, 31 mm span)", 192e-6, 0.031, 1.07),
                           ("S2 mid (2 x 30 x 15 mm)", 900e-6, 0.06, 1.07)]:
    V = ratio(**{**BASE, "S": S, "CL": CL})[2]
    c = S / span
    print(f"{label:28s} chord {c*1e3:5.1f} mm, V_to {V:.2f} m/s, Re = {V*c/nu:6.0f}")
print("Wakeling & Ellington 1997 isolated wings: Re 700-2400 (abstract). Park & Choi 2010: Re ~1.9-2.2e4 (via S2-D-D, full-text).")
