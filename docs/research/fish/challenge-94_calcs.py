"""Challenge 94: independent re-derivation of S2-D-D's flying-fish back-solve and its transfer.

Self-contained: does NOT import S2D_calcs.py or S2DD_calcs.py. S2-D's zebrafish inputs
(mass, area, chord, body ellipsoid, form factor, median fins, lam, CL cap) are re-typed from
S2D_calcs.py (branch claude/deepen-s2-lift-drag-6xxrv3), and a control asserts that S2-D's
published AR-4 value of 4.80 is reproduced. Every number printed is COMPUTED, not observed.
Run: python3 -I docs/research/fish/challenge-94_calcs.py
"""
import math

NU, RHO, G = 1.5e-5, 1.2, 9.81


def blasius2(re):                       # laminar plate, both sides, on planform area (MODEL)
    return 2 * 1.328 / math.sqrt(re)


# ---- zebrafish-scale design (S2/S2-D ASSUMED inputs, re-typed) ----
M, S, CHORD = 0.4e-3, 9e-4, 0.015
BL, BD, BW, FORM, MED = 0.032, 0.007, 0.004, 1.5, 2.0e-4


def body_cda(v):
    a, b = BD / 2, BW / 2
    per = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    return FORM * 1.328 / math.sqrt(v * BL / NU) * 0.75 * per * BL + blasius2(v * 0.01 / NU) * MED


def zf(ar, e, lam=1.4, cap=0.9):
    v = 3.0
    for _ in range(5000):
        cd0 = lam * blasius2(v * CHORD / NU) + body_cda(v) / S
        k = 1 / (math.pi * e * ar)
        cl = min(math.sqrt(cd0 / k), cap)
        v2 = math.sqrt(2 * M * G / (RHO * S * cl))
        if abs(v2 - v) < 1e-13:
            break
        v = v2
    return cl / (cd0 + k * cl * cl)


# ---- flying fish (Park & Choi 2010: Re 2e4 on mean chord at 12 m/s, AR 9.0-10.7, full-text) ----
U, RE = 12.0, 2.0e4
C = RE * NU / U                          # implied chord, COMPUTED


def ff(ar, lam, e, D, L=0.2):            # body L x D ASSUMED (S2-D-D's choice)
    A = ar * C * C
    cdA = 1.5 * 1.328 / math.sqrt(U * L / NU) * 0.75 * math.pi * D * L
    cd0 = lam * blasius2(RE) + cdA / A
    return cd0, 0.5 * math.sqrt(math.pi * e * ar / cd0)


if __name__ == "__main__":
    base = zf(4, 0.7)
    assert abs(base - 4.80) < 0.01
    print(f"control: S2-D AR-4 whole-animal L/D reproduced = {base:.2f}")
    print(f"implied flying-fish chord = {C*1e3:.1f} mm")
    grid = [(ar, lam, D) for ar in (9.0, 10.7) for lam in (1.0, 1.4, 2.0) for D in (0.025, 0.035)]
    for meas in (4.4, 5.9):
        rat, ee, eAR = [], [], []
        for ar, lam, D in grid:
            cd0, ld = ff(ar, lam, 0.7, D)
            rat.append(meas / ld)
            x = (2 * meas) ** 2 * cd0 / math.pi
            eAR.append(x); ee.append(x / ar)
        print(f"\nanchor {meas}: measured/model {min(rat):.2f}-{max(rat):.2f} "
              f"(overprediction {1/max(rat):.1f}-{1/min(rat):.1f}x); "
              f"e_eff {min(ee):.3f}-{max(ee):.3f}; e*AR_eff {min(eAR):.2f}-{max(eAR):.2f}")
        # S2-D-D's own central case: AR 9, lam 1.4, D 25 mm
        cd0, _ = ff(9.0, 1.4, 0.7, 0.025)
        x = (2 * meas) ** 2 * cd0 / math.pi
        print(f"  central back-solve (AR 9, lam 1.4, D 25): e*AR_eff = {x:.3f}, e_eff = {x/9:.3f}")
        print(f"  transfer rule (i)  e_eff carried as a RATIO to AR 4:      L/D = {zf(4, x/9):.2f}")
        print(f"  transfer rule (ii) e*AR_eff carried as an ABSOLUTE cap:  L/D = {zf(4, x/4):.2f}")
        lo = min(zf(4, e, lam=lz) for e in ee for lz in (1.0, 1.4, 2.0))
        hi = max(zf(4, e, lam=lz) for e in ee for lz in (1.0, 1.4, 2.0))
        print(f"  rule (i) over the full flying-fish grid x zebrafish lam 1.0-2.0: L/D = {lo:.2f}-{hi:.2f}")
    # sanity: rule (ii) can only be >= rule (i) at AR 4 < 9
    assert zf(4, 0.905 / 4) > zf(4, 0.905 / 9)
