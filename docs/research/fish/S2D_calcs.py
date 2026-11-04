"""S2-D: sensitivity of the S2 lift-to-drag answer, and a recompute with an improved input.

Every number this prints is COMPUTED from stated inputs. None is a measurement.
Inputs are tagged:  MEAS-A = measured value read at abstract level (see S2-deepen.md),
                    ASSUMED = design or geometry assumption, MODEL = modelling choice.
Run:  python3 -I docs/research/fish/S2D_calcs.py
"""
import math

NU, RHO, G = 1.5e-5, 1.2, 9.81
M = 0.4e-3            # kg, ASSUMED (same as S2)
S = 9e-4              # m^2, both fins, ASSUMED (S2's middle case: 2 x 3 cm x 1.5 cm)
CHORD = 0.015         # m, ASSUMED
SPAN = 0.06           # m, tip to tip of the two fins, ASSUMED -> AR = b^2/S = 4
E_OSW = 0.7           # span efficiency, ASSUMED (typical low-AR value; not retrieved)

# Body: ellipsoid, ASSUMED geometry (zebrafish SL 2.8-3.4 cm relayed in S2; depth/width not retrieved)
BODY_L, BODY_D, BODY_W = 0.032, 0.007, 0.004
FORM = 1.5            # pressure-drag multiplier on laminar friction, ASSUMED
MEDIAN_FINS = 2.0e-4  # m^2 planform of caudal+dorsal+anal fins (wetted both sides), ASSUMED


def blasius_plate_cd(re):
    """Laminar flat-plate friction, BOTH sides, referenced to planform area. MODEL."""
    return 2 * 1.328 / math.sqrt(re)


def body_drag_area(v):
    """Drag area (m^2) of body + median fins: laminar friction x form factor. MODEL."""
    a, b = BODY_D / 2, BODY_W / 2
    perim = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))  # Ramanujan
    wetted_body = 0.75 * perim * BODY_L        # ~ellipsoid of revolution, ASSUMED factor
    re_l = v * BODY_L / NU
    cf = 1.328 / math.sqrt(re_l)
    re_f = v * 0.01 / NU                        # median fins, ~1 cm chord, ASSUMED
    return FORM * cf * wetted_body + blasius_plate_cd(re_f) * MEDIAN_FINS


def ld_max(cd0_wing, ar=SPAN**2 / S, e=E_OSW, body_cda=None, v=3.5):
    """Parabolic polar CD = CD0 + CL^2/(pi e AR).  Returns (L/D_max, CL at that point)."""
    if body_cda is None:
        body_cda = body_drag_area(v)
    cd0 = cd0_wing + body_cda / S
    k = 1 / (math.pi * e * ar)
    return 1 / (2 * math.sqrt(cd0 * k)), math.sqrt(cd0 / k)


def section_1_sensitivity():
    print("1. SENSITIVITY of whole-animal L/D_max to each input, x0.5 and x2 (COMPUTED)")
    base_cd0 = 0.05   # S2's implicit value: Kesel 2000 'CD,min < 0.06' (Re 7,880-10,000)
    base_cda = body_drag_area(3.5)
    ar0 = SPAN**2 / S
    b, cl = ld_max(base_cd0)
    wing_only, _ = ld_max(base_cd0, body_cda=0.0)
    print(f"   baseline: CD0_wing={base_cd0}, AR={ar0:.1f}, e={E_OSW}, body CdA={base_cda*1e4:.3f} cm^2"
          f" (= {base_cda/S:.4f} on wing area)")
    print(f"   baseline wing-alone L/D_max = {wing_only:.2f}   whole animal = {b:.2f}  (CL* = {cl:.2f})")
    print("   | input | x0.5 -> L/D | x2 -> L/D | swing (x2/x0.5) |")
    print("   |---|---|---|---|")
    rows = {
        "CD0_wing (profile drag)": lambda f: ld_max(base_cd0 * f)[0],
        "AR (planform)":           lambda f: ld_max(base_cd0, ar=ar0 * f)[0],
        "e (span efficiency)":     lambda f: ld_max(base_cd0, e=min(E_OSW * f, 1.0))[0],
        "body drag area":          lambda f: ld_max(base_cd0, body_cda=base_cda * f)[0],
    }
    for name, fn in rows.items():
        lo, hi = fn(0.5), fn(2.0)
        print(f"   | {name} | {lo:.2f} | {hi:.2f} | {lo/hi if lo>hi else hi/lo:.2f} |")
    print("   note: e x2 is capped at 1.0 (physical limit), so its x2 swing is smaller.")
    # control (known answer): CD0 x4 must halve L/D_max exactly when body drag is zero
    a1, _ = ld_max(0.05, body_cda=0.0)
    a4, _ = ld_max(0.20, body_cda=0.0)
    assert abs(a1 / a4 - 2.0) < 1e-12
    # must-fail: more body drag can never raise L/D
    assert ld_max(0.05, body_cda=base_cda * 2)[0] < ld_max(0.05)[0]
    print("   controls passed: CD0 x4 halves L/D exactly; more body drag lowers L/D")
    return b


def section_2_profile_drag_vs_re():
    print("\n2. PROFILE DRAG vs Re: Blasius (MODEL) beside the measured anchors (MEAS-A)")
    print("   | Re | Blasius 2-sided | x1.4 | measured anchor |")
    print("   |---|---|---|---|")
    anchors = {700: "W&E 1997: CD(alpha=0) 0.07-0.14 over Re 700-2,400",
               2400: "(same range)",
               8000: "Kesel 2000: CD,min < 0.06 over Re 7,880-10,000",
               10000: "(same range)"}
    for re in (700, 1000, 2000, 2400, 3500, 5000, 8000, 10000):
        cb = blasius_plate_cd(re)
        print(f"   | {re:,} | {cb:.3f} | {1.4*cb:.3f} | {anchors.get(re, '')} |")
    # control: Blasius at Re=10,000 is 2*1.328/100 = 0.02656 by hand
    assert abs(blasius_plate_cd(1e4) - 0.02656) < 1e-6


def cd0_improved(re, lam):
    """Improved CD0: lam x Blasius, lam bracketed from W&E 1997 ('little more than Blasius').
    INFERENCE, not the authors' fit."""
    return lam * blasius_plate_cd(re)


def section_3_recompute():
    print("\n3. RECOMPUTE L/D_max with Re-dependent profile drag (COMPUTED)")
    print("   Operating point is solved self-consistently: V from wing loading at CL*, Re from V.")
    print("   | lam | AR | Re at CL* | CD0_wing | wing-alone L/D | whole-animal L/D | CL* | V (m/s) |")
    print("   |---|---|---|---|---|---|---|---|")
    out = {}
    for ar in (4.0, 8.0):
        for lam in (1.0, 1.4, 2.0):
            v = 3.5
            for _ in range(50):          # fixed point: CD0 depends on Re, Re on V, V on CL*
                re = v * CHORD / NU
                cd0 = cd0_improved(re, lam)
                ld, cl = ld_max(cd0, ar=ar, v=v)
                v_new = math.sqrt(2 * M * G / (RHO * S * cl))
                if abs(v_new - v) < 1e-9:
                    break
                v = v_new
            wing, _ = ld_max(cd0, ar=ar, body_cda=0.0)
            out[(lam, ar)] = (ld, cl, re, cd0, wing)
            print(f"   | {lam} | {ar:.0f} | {re:,.0f} | {cd0:.3f} | {wing:.2f} | {ld:.2f} | {cl:.2f} | {v:.2f} |")
    print("   lam = 1.0 is a clean laminar plate (lower bound on drag); 1.4 is the 'little more than")
    print("   Blasius' reading of W&E 1997; 2.0 is a rough, fluttering or corrugated-and-unlucky fin.")
    print("   AR 4 is S2's fin planform; AR 8 is shown only to bound the 'insect wing' ceiling.")
    return out


CL_USABLE = 0.9   # ~85% of W&E 1997 steady CL,max 1.07 (MEAS-A); margin is an ASSUMPTION


def ld_at_cl(cl, cd0, ar, v):
    k = 1 / (math.pi * E_OSW * ar)
    return cl / (cd0 + body_drag_area(v) / S + k * cl * cl)


def section_3b_ar_scan():
    print("\n3b. WHOLE-ANIMAL L/D vs effective aspect ratio, improved CD0 (lam 1.4), CL capped (COMPUTED)")
    print(f"   CL is min(CL*, {CL_USABLE}); above that the parabolic polar is past the measured stall region.")
    print("   | AR | e*AR | CL used | Re | L/D whole animal | L/D wing alone |")
    print("   |---|---|---|---|---|---|")
    res = {}
    for ar in (1.5, 2, 3, 4, 6, 8):
        v = 3.0
        for _ in range(60):
            re = v * CHORD / NU
            cd0 = cd0_improved(re, 1.4)
            _, cls = ld_max(cd0, ar=ar, v=v)
            cl = min(cls, CL_USABLE)
            v_new = math.sqrt(2 * M * G / (RHO * S * cl))
            if abs(v_new - v) < 1e-9:
                break
            v = v_new
        ld = ld_at_cl(cl, cd0, ar, v)
        k = 1 / (math.pi * E_OSW * ar)
        wing = cl / (cd0 + k * cl * cl)
        res[ar] = ld
        print(f"   | {ar} | {E_OSW*ar:.2f} | {cl:.2f} | {re:,.0f} | {ld:.2f} | {wing:.2f} |")
    # control: capping CL can only lower L/D relative to the uncapped optimum
    for ar in (6, 8):
        cd0 = cd0_improved(2300, 1.4)
        assert ld_at_cl(CL_USABLE, cd0, ar, 2.3) <= ld_max(cd0, ar=ar, v=2.3)[0] + 1e-12
    return res


def glide_range(S_, CL, lam, ar, h0=0.5, vx0=2.0, dt=1e-5, re_dependent=True, ld_fixed=None):
    """S2's point-mass glide, but with CD recomputed at every step from the local Re. MODEL."""
    k = 1 / (math.pi * E_OSW * ar)
    x, z, vx, vz = 0.0, h0, vx0, 0.0
    while z > 0:
        v = math.hypot(vx, vz)
        if v < 1e-9:
            vz -= G * dt; z += vz * dt; continue
        if ld_fixed is not None:
            cd = CL / ld_fixed
        else:
            re = max(v * CHORD / NU, 50.0)
            cd = cd0_improved(re, lam) + CL * CL * k + body_drag_area(v) / S_
        q = 0.5 * RHO * v * v * S_
        ux, uz = vx / v, vz / v
        ax = (-q * cd * ux - q * CL * uz) / M
        az = (-q * cd * uz + q * CL * ux) / M - G
        vx += ax * dt; vz += az * dt; x += vx * dt; z += vz * dt
    return x


def section_4_downstream():
    print("\n4. DOWNSTREAM: glide range from 0.5 m, 2 m/s horizontal launch, S = 9 cm^2, CL = 0.6")
    print("   | case | range (m) | body lengths (4 cm) |")
    print("   |---|---|---|")
    ballistic = 2.0 * math.sqrt(2 * 0.5 / G)
    for lab, kw in (("S2 fixed L/D = 6", dict(ld_fixed=6)),
                    ("S2 fixed L/D = 3", dict(ld_fixed=3)),
                    ("Re-dependent drag, lam 1.0, AR 4", dict(lam=1.0, ar=4)),
                    ("Re-dependent drag, lam 1.4, AR 4", dict(lam=1.4, ar=4)),
                    ("Re-dependent drag, lam 2.0, AR 4", dict(lam=2.0, ar=4))):
        lam = kw.pop("lam", 1.0); ar = kw.pop("ar", 4)
        r = glide_range(9e-4, 0.6, lam, ar, **kw)
        print(f"   | {lab} | {r:.3f} | {r/0.04:.1f} |")
    for lab, kw in (("S = 18 cm^2, fixed L/D = 6", dict(ld_fixed=6)),
                    ("S = 18 cm^2, fixed L/D = 4", dict(ld_fixed=4)),
                    ("S = 18 cm^2, Re-dependent drag, lam 1.4, AR 4", dict()),
                    ("S = 18 cm^2, Re-dependent drag, lam 2.0, AR 4", dict(lam=2.0))):
        lam = kw.pop("lam", 1.4)
        r = glide_range(18e-4, 0.6, lam, 4, **kw)
        print(f"   | {lab} | {r:.3f} | {r/0.04:.1f} |")
    print(f"   | wingless ballistic | {ballistic:.3f} | {ballistic/0.04:.1f} |")
    # control: fixed L/D=6 must reproduce S2's 0.94 m for this case
    assert abs(glide_range(9e-4, 0.6, 1.0, 4, ld_fixed=6) - 0.94) < 0.01


if __name__ == "__main__":
    section_1_sensitivity()
    section_2_profile_drag_vs_re()
    section_3_recompute()
    section_3b_ar_scan()
    section_4_downstream()
