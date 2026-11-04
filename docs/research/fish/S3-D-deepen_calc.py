#!/usr/bin/env python3
"""S3-D-D: attack the weakest input of S3-D (the deepening of S3).

S3-D's verdict ("power budget STANDS") rests on one comparison:
    CL needed to close the most generous launch case (2.16)  vs  best CL a fin wing can give (1.0-1.1).

Everything printed here is CALCULATION on stated inputs. Nothing is a measurement.
The launch model is S3's, as recoded by S3-D (branch claude/s3-mass-power-budget-rcrklv @ 1384d67f,
docs/research/fish/S3-deepen_calc.py). It is re-implemented below and asserted to reproduce
S3's 409 W/kg and 2,878 W/kg before anything else is printed.

Run: python3 -I docs/research/fish/S3-D-deepen_calc.py
"""
from math import sqrt

g, rho = 9.81, 1.225
m_body = 0.40e-3                                  # kg, project brief (via S3)
P_AVAIL = 142.7                                   # W/kg muscle, Wakeling & Johnston 1998 (abstract, via S3)
SIG_C = (0.8 * 1050 + 0.2 * 1557) * 120e-6        # kg/m^2, S3 central fin areal density
BASE = dict(CL=1.07, sigma=SIG_C, eta=0.37, fm=0.6, s_bl=2.0, P=P_AVAIL, m=m_body, S=1070e-6, BL=0.04)
SPAN_S10 = 0.08                                   # m, S10 planform (R 4 cm, AR 6), as used by S3-D for Re


def ratio(CL, sigma, eta, fm, s_bl, P, m, S, BL, S_extra=0.0):
    """S3 sec 3.5 model. Returns (required/available, W/kg muscle, V_to).
    S_extra: additional LIFTING planform that carries no wing mass (e.g. body), scenario only."""
    M = m + sigma * S
    V = sqrt(2 * M * g / (rho * (S + S_extra) * CL))
    t = 2 * s_bl * BL / V
    Pm = (V**2 / 2) / t / eta * M / (fm * m)
    return Pm / P, Pm, V


def cl_needed(**kw):
    lo, hi = 0.01, 500.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ratio(**{**BASE, **kw, "CL": mid})[0] > 1 else (lo, mid)
    return hi


def hr(t):
    print("\n" + t + "\n" + "-" * len(t))


hr("0. Controls: reproduce S3 and S3-D")
r, Pm, V = ratio(**BASE)
r28, Pm28, _ = ratio(**{**BASE, "S": 192e-6})
CLN = cl_needed()
print(f"S10, 2 BL, eta .37, f_m .6, CL 1.07: {Pm:.0f} W/kg, {r:.2f}x short, V_to {V:.2f} m/s  (S3: 409, 2.9x)")
print(f"S28-C: {Pm28:.0f} W/kg, {r28:.1f}x  (S3: 2878, 20x)")
print(f"CL needed to close the generous case: {CLN:.3f}  (S3-D: 2.16)")
assert abs(Pm - 409) < 2 and abs(Pm28 - 2878) < 10 and abs(CLN - 2.16) < 0.01

hr("1. Sensitivity of S3-D's conclusion. Margin = CL_needed / CL_best_available (S3-D: 2.16/1.1)")
CL_BEST = 1.10
print(f"S3-D margin: {CLN/CL_BEST:.2f}  (>1 means the budget does not close; the verdict STANDS)")
for k in ("CL_best", "sigma", "eta", "fm", "s_bl", "P", "m"):
    out = []
    for f in (2.0, 0.5):
        if k == "CL_best":
            mg = CLN / (CL_BEST * f)
        else:
            mg = cl_needed(**{k: BASE[k] * f}) / CL_BEST
        out.append(f"x{f:g}: margin {mg:5.2f} -> {'STANDS' if mg > 1 else 'FALLS'}")
    print(f"{k:8s} " + "   ".join(out))

hr("2. Recompute with the CL regimes found in this session (sources and read-levels in S3-D-deepen.md)")
REGIMES = [
    ("A steady, fin wing: Park & Choi 2007 'about 1.0~1.1', low (search-summary)", 1.00),
    ("A steady, fin wing: Park & Choi 2007, high (search-summary)", 1.10),
    ("B steady LEV, revolving flat card replica of pigeon wing, Usherwood 2009 (search-summary)", 1.44),
    ("B steady LEV, revolving dried pigeon wing, Usherwood 2009 (search-summary)", 1.64),
    ("C transient: 1.8 x 1.07 (+80% impulsive-start lift, Dickinson & Goetz 1993, abstract)", 1.80 * 1.07),
    ("C transient: 1.8 x 1.10", 1.80 * 1.10),
]
for label, CL in REGIMES:
    rr, PP, VV = ratio(**{**BASE, "CL": CL})
    print(f"{label:88s} CL {CL:4.2f}: {PP:4.0f} W/kg, {rr:4.2f}x short, V_to {VV:.2f} m/s")

hr("3. Scenario (NOT a measurement): body planform also lifts at the same CL, carries no wing mass")
print("Zebrafish dorsal planform area: unknown (no measured value found). Bracket assumed: 0, 120, 240 mm^2.")
for Ab in (0, 120e-6, 240e-6):
    for label, CL in [("steady fin 1.10", 1.10), ("revolving pigeon 1.64", 1.64), ("transient 1.98", 1.98)]:
        rr, _, VV = ratio(**{**BASE, "CL": CL, "S_extra": Ab})
        print(f"  body {Ab*1e6:3.0f} mm^2, {label:22s}: {rr:4.2f}x short {'<- closes' if rr <= 1 else ''}")
print(f"  CL needed with 240 mm^2 body lift: {cl_needed(S_extra=240e-6):.2f}")

hr("4. How long would transient (impulsive-start) lift last, and what would it buy?")
chord = BASE["S"] / SPAN_S10
CL_t = 1.80 * 1.10
_, _, V_t = ratio(**{**BASE, "CL": CL_t, "S_extra": 240e-6})   # speed at which transient + body lift = weight
d = 2 * chord                     # Dickinson & Goetz 1993: LEV 'stayed attached ... for the first 2 chord lengths'
t_lev = d / V_t
print(f"S10 mean chord {chord*1e3:.1f} mm; 2 chords = {d*1e3:.1f} mm; at {V_t:.2f} m/s that is {t_lev*1e3:.1f} ms")
# After the transient decays, CL falls back to steady (1.10). Lift then supports only 1.10/1.98 of weight.
frac = 1.10 / CL_t
print(f"after the transient, lift = {frac:.2f} of weight at the same speed; net downward accel {g*(1-frac):.2f} m/s^2")
# Upper bound on the hop: assume excess lift during the transient equals full weight (a generous 2 g).
dv = g * t_lev
print(f"generous bound on vertical speed gained in the transient (1 g excess for {t_lev*1e3:.1f} ms): {dv*1e3:.0f} mm/s,"
      f" apex {dv**2/(2*g)*1e3:.2f} mm")
_, _, V_steady = ratio(**{**BASE, "CL": 1.10, "S_extra": 240e-6})
print(f"speed needed to stay up on steady CL 1.10 with body lift: {V_steady:.2f} m/s vs {V_t:.2f} m/s reached")
rr_st, _, _ = ratio(**{**BASE, "CL": 1.10, "S_extra": 240e-6})
print(f"=> sustained launch still {rr_st:.2f}x short on power")

hr("5. Reynolds numbers, for the transfer argument")
nu = 1.5e-5
print(f"designed S10 wing at V_to {V:.2f} m/s: Re = {V*chord/nu:.0f}")
print("Park & Choi 2010: Re 1.9-2.2e4 (full-text, read this session). Usherwood 2009: up to 1.08e5 (search-summary).")
print("Dickinson & Goetz 1993: 10 < Re < 1000 (abstract, this session).")
