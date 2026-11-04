"""S2-D-D: attack S2-D's most sensitive input, the effective aspect ratio e*AR of a fin-derived wing.

Every number this prints is COMPUTED. None is an observation.
The aerodynamic model is copied from S2-D (S2D_calcs.py, branch claude/deepen-s2-lift-drag-6xxrv3)
so that the recompute changes only the inputs. Control C1 asserts it reproduces S2-D's published numbers.

Input tags:
  MEAS-FT  measured, read in full text (see S2-D-deepen.md for the source and read-level)
  MEAS-P   measured, read on a partial publisher page (Park & Choi 2010)
  SS       search-summary, carried over from S22-D and not re-read
  INF      my inference
  ASSUMED  carried-over assumption
Run:  python3 -I docs/research/fish/S2-D-deepen_calc.py
"""
import math

NU, RHO, G = 1.5e-5, 1.2, 9.81
M = 0.4e-3              # kg, ASSUMED (S2)
S_WING = 9e-4           # m^2, ASSUMED (S2 middle case)
E_OSW = 0.7             # span efficiency, ASSUMED, never retrieved
BODY_L, BODY_D, BODY_W = 0.032, 0.007, 0.004   # m, ASSUMED (S2-D)
FORM, MEDIAN_FINS = 1.5, 2.0e-4                # ASSUMED (S2-D)
CL_USABLE = 0.9         # ASSUMED, ~85% of W&E 1997 steady CL,max 1.07
SL = 0.032              # m, ASSUMED, inside the 2.8-3.4 cm adult SL relayed by S2


def blasius(re):
    return 2 * 1.328 / math.sqrt(re)


def body_cda(v):
    a, b = BODY_D / 2, BODY_W / 2
    perim = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    wet = 0.75 * perim * BODY_L
    cf = 1.328 / math.sqrt(v * BODY_L / NU)
    return FORM * cf * wet + blasius(v * 0.01 / NU) * MEDIAN_FINS


def ld_max_fixed(cd0_w, ar, e=E_OSW, cda=None, v=3.5, S=S_WING):
    """S2-D section-1 model (fixed CD0). Returns whole-animal L/D_max."""
    cda = body_cda(v) if cda is None else cda
    cd0 = cd0_w + cda / S
    k = 1 / (math.pi * e * ar)
    return 1 / (2 * math.sqrt(cd0 * k))


def operating_point(ar, lam=1.4, e=E_OSW, S=S_WING, cap=CL_USABLE):
    """S2-D section-3b model: Re-dependent CD0 = lam*Blasius at chord c = sqrt(S/AR),
    CL = min(CL*, cap), solved self-consistently. Returns (whole L/D, wing L/D, CL, Re, V).
    S2-D held chord fixed at 15 mm for every AR. Here the chord follows the planform (c = S/b),
    and that is the one modelling change. With chord_fixed=True, S2-D is reproduced (control C1)."""
    return _op(ar, lam, e, S, cap, chord=math.sqrt(S / ar))


def _op(ar, lam, e, S, cap, chord):
    k = 1 / (math.pi * e * ar)
    v = 3.0
    for _ in range(200):
        re = v * chord / NU
        cd0w = lam * blasius(re)
        cd0 = cd0w + body_cda(v) / S
        cl = min(math.sqrt(cd0 / k), cap)
        v_new = math.sqrt(2 * M * G / (RHO * S * cl))
        if abs(v_new - v) < 1e-10:
            break
        v = v_new
    whole = cl / (cd0 + k * cl * cl)
    wing = cl / (cd0w + k * cl * cl)
    return whole, wing, cl, re, v


def main():
    # ---- C1: reproduce S2-D ------------------------------------------------------------
    base = ld_max_fixed(0.05, 4.0)
    assert abs(base - 5.49) < 0.01, base
    s2d_ar4 = _op(4.0, 1.4, E_OSW, S_WING, CL_USABLE, chord=0.015)[0]
    assert abs(s2d_ar4 - 4.80) < 0.01, s2d_ar4
    print(f"C1 control: S2-D baseline {base:.2f} (published 5.49); AR4 lam1.4 capped {s2d_ar4:.2f} (published 4.80)")

    # ---- 1. Sensitivity re-check -------------------------------------------------------
    print("\n1. SENSITIVITY (COMPUTED, S2-D fixed-CD0 model, CD0_wing = 0.05)")
    for name, f in (("e*AR", lambda x: ld_max_fixed(0.05, 4.0 * x)),
                    ("CD0_wing", lambda x: ld_max_fixed(0.05 * x, 4.0)),
                    ("body CdA", lambda x: ld_max_fixed(0.05, 4.0, cda=body_cda(3.5) * x))):
        lo, hi = f(0.5), f(2.0)
        print(f"   {name:9s} x0.5 -> {lo:.2f}   x2 -> {hi:.2f}   swing {max(lo, hi)/min(lo, hi):.2f}")
    # analytic check: with no body drag, L/D ~ sqrt(e*AR), so x2 swing must be exactly 2.0
    r = ld_max_fixed(0.05, 8.0, cda=0.0) / ld_max_fixed(0.05, 2.0, cda=0.0)
    assert abs(r - 2.0) < 1e-12
    print("   analytic control: wing-alone L/D(eAR x2)/L/D(eAR x0.5) = 2.000 exactly")

    # ---- 2. Convention: fish-literature AR is single-fin L^2/A -----------------------------
    print("\n2. CONVENTION CONVERSION (INF). Fish ecomorphology AR_fin = L^2/A for ONE fin (leading edge L).")
    print("   For two fins as one wing: span b = 2L + w_body, S = 2A, so AR_wing = (2L+w)^2/(2A).")
    print("   If w_body = 0, AR_wing = 2 * AR_fin. Walker et al. 2013 double it for exactly this reason.")
    L = 0.03
    for arf in (0.91, 1.38, 1.84, 2.08):
        A = L * L / arf
        print(f"   AR_fin {arf:.2f} -> AR_wing (w=0) {2*arf:.2f}; with w = 4 mm body, L = 3 cm: "
              f"{(2*L+BODY_W)**2/(2*A):.2f} (span over a lifting body, not credited: e absorbs it)")

    # ---- 3. Recompute with the improved AR ranges -------------------------------------------
    print("\n3. RECOMPUTE: whole-animal L/D at S = 9 cm^2, CL cap 0.9, chord = sqrt(S/AR) (COMPUTED)")
    print("   | source of AR | AR_wing | e*AR | lam | whole L/D | wing L/D | CL | Re |")
    print("   |---|---|---|---|---|---|---|---|")
    cases = [("labrid min in table (P. hexataenia 0.91 x2)", 1.82),
             ("labrid typical Halichoeres ~1.38 x2", 2.76),
             ("Thalassoma ~1.84-1.97 x2", 3.80),
             ("labrid max (S. bandanensis 2.08 x2)", 4.16),
             ("S2/S2-D assumption", 4.0),
             ("flying fish low (Park & Choi 9.0)", 9.0),
             ("flying fish high (10.7)", 10.7)]
    out = {}
    for lab, ar in cases:
        for lam in (1.4, 2.0):
            w, wg, cl, re, v = operating_point(ar, lam)
            out[(ar, lam)] = w
            print(f"   | {lab} | {ar:.2f} | {E_OSW*ar:.2f} | {lam} | {w:.2f} | {wg:.2f} | {cl:.2f} | {re:,.0f} |")

    # e is the other half of the product, still assumed. Bracket it.
    print("\n   e bracket at the labrid-range AR (lam 1.4):")
    for ar in (1.82, 4.16):
        vals = [operating_point(ar, 1.4, e=e)[0] for e in (0.5, 0.7, 0.9)]
        print(f"   AR {ar}: e 0.5/0.7/0.9 -> {vals[0]:.2f} / {vals[1]:.2f} / {vals[2]:.2f}")

    # ---- 4. Span limit: AR and S are not independent on a 3.2 cm fish ------------------------
    print("\n4. SPAN CHECK (COMPUTED): span each AR needs at S = 9 cm^2, against flying-fish proportions")
    print("   Flying-fish pectoral length 0.65-0.77 SL (SS, E. volitans, via S22-D).")
    for ar in (1.82, 4.0, 4.16, 9.0, 10.7):
        b = math.sqrt(ar * S_WING)
        per_fin = (b - BODY_W) / 2
        print(f"   AR {ar:5.2f}: span {b*100:.1f} cm, per fin {per_fin*100:.2f} cm = {per_fin/SL:.2f} SL")
    print("\n   Span held at the flying-fish proportion (per fin 0.70 SL), S chosen by AR (lam 1.4):")
    b_ff = 2 * 0.70 * SL + BODY_W
    print("   | AR | S (cm^2) | whole L/D | CL | V (m/s) |")
    print("   |---|---|---|---|---|")
    for ar in (2.0, 3.0, 4.0, 6.0, 9.0):
        S = b_ff ** 2 / ar
        w, wg, cl, re, v = operating_point(ar, 1.4, S=S)
        print(f"   | {ar} | {S*1e4:.2f} | {w:.2f} | {cl:.2f} | {v:.2f} |")
    # must-fail: raising AR at fixed span must shrink S
    assert b_ff ** 2 / 9.0 < b_ff ** 2 / 2.0
    return out


if __name__ == "__main__":
    main()
