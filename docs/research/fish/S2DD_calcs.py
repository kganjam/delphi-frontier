"""S2-D-D: attack the most sensitive input of S2-D (effective aspect ratio / induced-drag efficiency).

Every number printed is COMPUTED. None is an observation.
Imports S2-D's model unchanged from S2D_calcs.py (copied verbatim from branch
claude/deepen-s2-lift-drag-6xxrv3) so that the recompute is apples-to-apples.
Run:  python3 -I docs/research/fish/S2DD_calcs.py
"""
import math, os, importlib.util

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("s2d", os.path.join(_here, "S2D_calcs.py"))
s2d = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(s2d)
NU, G, RHO = s2d.NU, s2d.G, s2d.RHO


def solve(ar=4.0, e=0.7, lam=1.4, bodyf=1.0, cd0f=1.0, M=0.4e-3, cap=0.9):
    """S2-D's final operating point: Re-coupled CD0 = lam*Blasius, CL capped at `cap`.
    bodyf scales body drag area; cd0f scales the wing profile drag (both 1.0 = S2-D)."""
    v = 3.0
    for _ in range(500):
        re = v * s2d.CHORD / NU
        cd0 = cd0f * s2d.cd0_improved(re, lam)
        cdb = bodyf * s2d.body_drag_area(v) / s2d.S
        k = 1 / (math.pi * e * ar)
        cl = min(math.sqrt((cd0 + cdb) / k), cap)
        vn = math.sqrt(2 * M * G / (RHO * s2d.S * cl))
        if abs(vn - v) < 1e-11:
            break
        v = vn
    return cl / (cd0 + cdb + k * cl * cl), cl, re


def section_1():
    print("1. SENSITIVITY on S2-D's FINAL model (lam 1.4, CL cap 0.9, Re-coupled), x0.5 / x2 (COMPUTED)")
    base = solve()[0]
    print(f"   baseline whole-animal L/D = {base:.2f}  (S2-D reported 4.80)")
    assert abs(base - 4.80) < 0.01, "must reproduce S2-D's AR-4 row"
    print("   | input | x0.5 | x2 | swing |")
    print("   |---|---|---|---|")
    rows = [("e*AR (effective aspect ratio)", lambda f: dict(e=0.7 * f)),
            ("lam (profile drag / Blasius)", lambda f: dict(lam=1.4 * f)),
            ("body drag area", lambda f: dict(bodyf=f)),
            ("mass (wing loading)", lambda f: dict(M=0.4e-3 * f)),
            ("usable CL cap", lambda f: dict(cap=0.9 * f))]
    out = {}
    for name, kw in rows:
        lo, hi = solve(**kw(0.5))[0], solve(**kw(2.0))[0]
        out[name] = (lo, hi)
        print(f"   | {name} | {lo:.2f} | {hi:.2f} | {max(lo, hi) / min(lo, hi):.2f} |")
    # control: e and AR enter only as a product
    assert abs(solve(ar=8, e=0.35)[0] - solve(ar=4, e=0.7)[0]) < 1e-9
    print("   control passed: e and AR enter only as the product e*AR")
    return out


# ---- Flying fish check (Park & Choi 2010, JEB 213:3269) ----
# FULL-TEXT (body text via journals.biologists.com): Re = 1.9-2.2e4 on mean pectoral chord at u = 12 m/s;
#   pectoral aspect ratio 9.0-10.7, defined as S^2/A1 (symbol list).  Specimens SL ~200 mm.
# SEARCH-SUMMARY ONLY: maximum L/D ~ 4.4 (model with pectoral + pelvic fins spread).
FF_U, FF_RE, FF_LD_MEAS = 12.0, 2.0e4, 4.4
FF_BODY = [(0.20, 0.025), (0.20, 0.035)]   # body length x diameter, ASSUMED (not retrieved)


def ff_model(ar, lam, e, body):
    c = FF_RE * NU / FF_U                       # chord implied by the stated Re (COMPUTED)
    b = ar * c; A = b * c
    L, D = body
    wet = 0.75 * math.pi * D * L                # same style of estimate as S2-D's body, ASSUMED
    cdA = 1.5 * 1.328 / math.sqrt(FF_U * L / NU) * wet
    cd0w = lam * s2d.blasius_plate_cd(FF_RE)
    cd0 = cd0w + cdA / A
    return 0.5 * math.sqrt(math.pi * e * ar / cd0), cd0w, cdA / A, c


def section_2():
    print("\n2. S2-D's MODEL APPLIED TO THE ONLY MEASURED FIN-WING ANIMAL (COMPUTED vs search-summary 4.4)")
    print("   | AR | lam | e | body | model L/D_max | measured / model |")
    print("   |---|---|---|---|---|---|")
    ratios = []
    for ar in (9.0, 10.7):
        for lam in (1.0, 1.4, 2.0):
            for e in (0.7, 0.9):
                for body in FF_BODY:
                    ld, cw, cb, c = ff_model(ar, lam, e, body)
                    ratios.append(FF_LD_MEAS / ld)
                    print(f"   | {ar} | {lam} | {e} | {body[0]*1000:.0f}x{body[1]*1000:.0f} mm | {ld:.1f} | {FF_LD_MEAS/ld:.2f} |")
    print(f"   implied chord from Re: {c*1000:.0f} mm (COMPUTED, not retrieved)")
    print(f"   measured/model ratio range: {min(ratios):.2f} - {max(ratios):.2f}")
    return min(ratios), max(ratios)


def section_3(ld_meas=FF_LD_MEAS):
    print(f"\n3. WHAT WOULD HAVE TO BE TRUE for the model to give {ld_meas} (COMPUTED back-solve)")
    ar, lam, body = 9.0, 1.4, FF_BODY[0]
    _, cw, cb, _ = ff_model(ar, lam, 0.7, body)
    cd0 = cw + cb
    eAR_req = (2 * ld_meas) ** 2 * cd0 / math.pi
    cd0_req = math.pi * 0.7 * ar / (2 * ld_meas) ** 2
    print(f"   (A) all of the gap in induced drag: e*AR_eff = {eAR_req:.2f} for geometric AR {ar}"
          f"  -> e_eff = {eAR_req/ar:.3f}")
    print(f"   (B) all of the gap in wing profile drag: CD0_wing = {cd0_req - cb:.3f}"
          f"  = {(cd0_req - cb)/cw:.1f} x the model's {cw:.3f}")
    print(f"   (C) all of the gap in body drag: body CdA/A = {cd0_req - cw:.3f}"
          f"  = {(cd0_req - cw)/cb:.1f} x the model's {cb:.4f}")
    # physical check on (C): body drag as CD on frontal area
    A = ar * (FF_RE * NU / FF_U) ** 2
    frontal = math.pi * (body[1] / 2) ** 2
    cd_front = (cd0_req - cw) * A / frontal
    print(f"   check on (C): that body drag is CD = {cd_front:.2f} on the body's frontal area"
          f" (a flat plate held normal to the flow is ~1.2, remembered textbook value)")
    return eAR_req / ar, (cd0_req - cb) / cw, (cd0_req - cw) / cb


def section_4(e_eff, cd0x, bodyx):
    print("\n4. RECOMPUTE S2-D's zebrafish-scale whole-animal L/D with the calibration carried over (COMPUTED)")
    print("   Transfer from Re 2e4 / SL 200 mm to Re ~3e3 / SL 32 mm is an ASSUMPTION (see text).")
    print("   | attribution | AR 1.5 | AR 2 | AR 4 | AR 8 |")
    print("   |---|---|---|---|---|")
    rows = [("S2-D as published (e 0.7, lam 1.4)", dict()),
            ("(A) e_eff from flying fish", dict(e=e_eff)),
            ("(B) wing CD0 x factor", dict(cd0f=cd0x)),
            ("(C) body CdA x factor", dict(bodyf=bodyx))]
    res = {}
    for name, kw in rows:
        vals = [solve(ar=a, **kw)[0] for a in (1.5, 2, 4, 8)]
        res[name] = vals
        print(f"   | {name} | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
    # must-fail direction: every attribution must LOWER L/D relative to S2-D
    for name in list(res)[1:]:
        assert all(a < b for a, b in zip(res[name], res[rows[0][0]]))
    print("   control passed: each attribution lowers L/D (the calibration can only subtract)")
    return res


def section_5():
    print("\n5. WHAT TELEOST FIN PLANFORMS ACTUALLY MEASURE (labrid single-fin AR = L_leading^2 / A_fin)")
    # Fulton et al. 2017 Ecol Evol (PMC5214093) Table 1, full-text; Fulton et al. 2013 PLoS One (PMC3541231)
    lab = dict(lo=0.76, hi=2.08)
    print(f"   measured single-fin AR range: {lab['lo']} - {lab['hi']} (full-text)")
    s2_fin = 0.03 ** 2 / (0.03 * 0.015)
    print(f"   S2's design fin, 30 x 15 mm: single-fin AR = {s2_fin:.2f}; two fins tip-to-tip (no body gap) AR = {2*s2_fin:.1f}")
    print(f"   -> S2's AR 4 sits at the labrid upper extreme ({lab['hi']} per fin); flying fish ~9-10.7 (whole wing)")
    assert abs(s2_fin - 2.0) < 1e-12


def section_6(res):
    print("\n6. DOWNSTREAM: glide range from 0.5 m, 2 m/s launch, S = 9 cm^2, CL = 0.6, fixed L/D (COMPUTED)")
    for ld in (4.8, 3.0, 2.0, 1.5):
        r = s2d.glide_range(9e-4, 0.6, 1.0, 4, ld_fixed=ld)
        print(f"   L/D {ld}: range {r:.3f} m = {r/0.04:.1f} BL")
    print(f"   wingless ballistic: {2.0*math.sqrt(2*0.5/G)/0.04:.1f} BL")


if __name__ == "__main__":
    section_1()
    lo, hi = section_2()
    e_eff, cd0x, bodyx = section_3()
    res = section_4(e_eff, cd0x, bodyx)
    print("\n   --- same, anchored instead on the upper relayed flying-fish value 5.9 (S2, read-level S) ---")
    e2, c2, b2 = section_3(5.9)
    section_4(e2, c2, b2)
    section_5()
    section_6(res)
