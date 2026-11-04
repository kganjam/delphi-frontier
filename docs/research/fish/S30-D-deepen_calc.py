"""S30-D-D -- deepen S30-D by attacking the input its verdict is most sensitive to.

Every number in docs/research/fish/S30-D-deepen.md is printed by this script.
Parent: S30-D (branch claude/deepen-s30-launch-budget-jb7qj4, commit efe54c57), whose verdict
"no realisable single-impulse window" is the comparison
        m*  <  m_floor,   m_floor = mass at which the scaled S28 wing reaches Re_air = 700,
the lower edge of the CL_max data (Wakeling & Ellington 1997, via S2 at read-level S).
Below that edge S30 and S30-D both kept CL_max = 1.07, i.e. they EXTRAPOLATED it.
Labels: PROJECT (inherited), LIT (literature, read level in the .md), DERIVED (calculated here).
Nothing here is a measurement.  Run: python3 docs/research/fish/S30-D-deepen_calc.py
"""
import math

line = "-" * 78
def h(t):
    print("\n" + line + "\n" + t + "\n" + line)

# ---------------------------------------------------------------- PROJECT inputs (S30 / S30-D)
M0 = 0.25e-3                 # kg, S28 anchor (back-solved with CL_max 1.07)
M_ZF = 0.40e-3
NEED0 = 10.17                # J/kg body at CL_max 1.07 (S29), incl. 6.5 % drag
F = 0.30
ETA_S, ETA_H = 0.93, 0.37
CL0 = 1.07                   # S28/S30 CL_max (Sympetrum, wind tunnel; S2 read-level S)
SL0, CHORD0, V0 = 0.030, 0.0062, 4.37
NU_AIR = 1.5e-5
RE_FLOOR = 700.0             # lower edge of the CL_max data used (S2)
W_TEL = 0.5 * 250e3 * 0.13 / 1060   # S30-D central teleost w, 15.33 J/kg muscle
W_TEL_HI = 0.5 * 300e3 * 0.15 / 1060
W_CEIL = 0.5 * 300e3 * 0.24 / 1060
W_FROG = 53.0

def r0(w=W_TEL, f=F, es=ETA_S, eh=ETA_H, cl=CL0):
    # need = WL/(rho*CL) per kg -> need scales as 1/CL (drag fraction is a fixed share of KE)
    need = NEED0 * CL0 / cl
    return f * w * es * eh / need

def mstar(r, beta=1/3):
    return M0 * r ** (1 / beta)

def design(m, cl=CL0):
    s = (m / M0) ** (1 / 3)
    v = V0 * (m / M0) ** (1 / 6) * math.sqrt(CL0 / cl)
    c = CHORD0 * s
    return SL0 * s * 1e3, c * 1e3, v, v * c / NU_AIR

def m_floor(re_floor=RE_FLOOR, cl=CL0):
    # Re_air ~ m^(1/2) at fixed CL; solve Re(m) = re_floor
    re_at_m0 = design(M0, cl)[3]
    return M0 * (re_floor / re_at_m0) ** 2

h("0. Reproduce S30-D")
for lab, w, b in (("central", W_TEL, 1/3), ("best one-side corner", W_TEL_HI, 0.533), ("S30 frog", W_FROG, 1/3)):
    m = mstar(r0(w=w), b)
    print(f"{lab:22s} w {w:5.1f}  beta {b:.3f}: m* {m*1e6:7.2f} mg, Re_air {design(m)[3]:5.0f}")
MF = m_floor()
print(f"validity floor (Re_air = 700 at CL 1.07): m_floor = {MF*1e6:.1f} mg")

# ---------------------------------------------------------------- 1. sensitivity of the VERDICT
h("1. Sensitivity of S30-D's verdict: margin = m_floor / m*  (verdict flips when margin < 1)")
def margin(w=W_TEL, beta=1/3, cl_below=CL0, re_floor=RE_FLOOR, f=F, eh=ETA_H):
    m = mstar(r0(w=w, f=f, eh=eh, cl=cl_below), beta)
    return m_floor(re_floor) / m          # floor itself defined at the data edge (CL 1.07 there)
for lab, kw in (("central (w 15.3, beta 1/3)", {}), ("best one-side corner (w 21.2, beta .533)", {"w": W_TEL_HI, "beta": 0.533})):
    base = margin(**kw)
    print(f"\n{lab}: margin {base:.2f}")
    tests = [
        ("w  (or fibre strain eps)", lambda k: margin(**{**kw, "w": kw.get("w", W_TEL) * k})),
        ("CL below Re 700 (1.07)", lambda k: margin(**{**kw, "cl_below": CL0 * k})),
        ("Re floor (700)", lambda k: margin(**{**kw, "re_floor": RE_FLOOR * k})),
        ("eta_h (0.37)", lambda k: margin(**{**kw, "eh": ETA_H * k})),
        ("f (0.30)", lambda k: margin(**{**kw, "f": F * k})),
        ("beta", lambda k: margin(**{**kw, "beta": kw.get("beta", 1/3) * k})),
    ]
    for name, fn in tests:
        up, dn = fn(2.0), fn(0.5)
        flip = lambda x: "FLIPS" if x < 1 else "holds"
        print(f"  {name:26s} x2 -> margin {up:9.3f} ({flip(up)})   /2 -> margin {dn:9.3f} ({flip(dn)})")

# ---------------------------------------------------------------- 2. improved input: CL below Re 700
h("2. Recompute with lift at Re < 700 from Zhang & Taira 2020 DNS (Re 400) instead of extrapolated 1.07")
# LIT (computed by those authors, read from their Fig. 3c by eye, sAR 2 = AR 4, Lambda 0, NACA 0015):
#   time-averaged CL ~0.6 at alpha 30 deg (still rising, so not a CL_max), ~0.38-0.40 at alpha 16 deg (max L/D)
#   max L/D < 1.5 at Re 400 (stated in their text).
# LIT (measured, via S2 read-level S): Wakeling & Ellington free glides CL 0.93; wind tunnel 1.07.
CASES = (("S30/S30-D extrapolation", 1.07), ("W&E free glide (Re 700-2400)", 0.93),
         ("Z&T Re 400, alpha 30", 0.60), ("Z&T Re 400, alpha 16 (max L/D)", 0.39))
print(f"{'CL used below Re 700':32s}{'m* central':>12s}{'Re at m*':>10s}{'m* best corner':>16s}{'Re':>7s}{'zf/m* central':>15s}")
for lab, cl in CASES:
    mc = mstar(r0(cl=cl)); mb = mstar(r0(w=W_TEL_HI, cl=cl), 0.533)
    print(f"{lab:32s}{mc*1e6:9.3f} mg{design(mc, cl)[3]:10.0f}{mb*1e6:13.3f} mg{design(mb, cl)[3]:7.0f}{M_ZF/mc:13.0f}x")
print("note: Re at m* uses V_to raised by sqrt(1.07/CL); every m* above lies at Re_air < 700,"
      " i.e. in the regime where the improved CL applies")

h("3. Does any S30-D case that CLEARED the floor survive? (they sit at Re >= 700, CL data unchanged)")
for lab, w, f in (("teleost ceiling, all muscle", W_CEIL, 0.60),):
    for b in (1/3, 0.533):
        m = mstar(r0(w=w, f=f), b)
        print(f"{lab} beta {b:.3f}: m* {m*1e6:.1f} mg, Re_air {design(m)[3]:.0f} (>= 700: {design(m)[3] >= 700})")

h("4. S30's own 39 mg window under the W&E disagreement (0.93 glide vs 1.07 tunnel)")
for cl in (1.07, 0.93):
    m = mstar(r0(w=W_FROG, cl=cl))
    print(f"frog w 53, CL {cl}: m* {m*1e6:.1f} mg, Re_air {design(m, cl)[3]:.0f}; floor at this CL "
          f"{m_floor(cl=cl)*1e6:.1f} mg -> inside data: {design(m, cl)[3] >= 700}")

h("5. What CL (held at every Re) would be needed to RESTORE a window?")
# need m* >= the mass where Re reaches 700 -> no solution below the floor by construction;
# instead: which CL makes the best one-side corner reach m_floor?
# Self-consistent: a higher CL lowers V_to and so Re, which raises the floor mass (m_floor ∝ CL).
# Solve m*(CL) = m_floor(CL) by bisection on CL.
for lab, w, b in (("central", W_TEL, 1/3), ("best corner", W_TEL_HI, 0.533)):
    lo, hi = 0.1, 20.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mstar(r0(w=w, cl=mid), b) < m_floor(cl=mid):
            lo = mid
        else:
            hi = mid
    print(f"{lab:12s}: one CL at every Re, floor self-consistent: CL needed {mid:.2f} "
          f"(window would open at {m_floor(cl=mid)*1e6:.0f} mg). "
          f"Compare 1.07 measured at Re 700-2400, ~0.6 computed at Re 400")

h("6. Glide-ratio check at Re 400 (Z&T max L/D < 1.5)")
LD = 1.5
print(f"L/D {LD} -> minimum glide angle {math.degrees(math.atan(1/LD)):.0f} deg; "
      f"horizontal gain per metre of height {LD:.1f} m (S28 case C at Re ~1800 assumed 4-6)")
