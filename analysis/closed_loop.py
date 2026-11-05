#!/usr/bin/env python3
"""A CLOSED-LOOP soaring controller, to test whether the knife edge is the policy or the physics.

Claim 975 found the sustained flight of claims 971 and 974 to be a knife edge: the most robust of
24 sustaining controllers survived only 5 of 12 one-at-a-time perturbations, with non-monotonic
failures. It named the specific thing that might change that: "every trajectory here flies an
OPEN-LOOP fixed schedule. An albatross does not... A closed-loop controller might find a basin
where this family finds a point. Untested, and not to be assumed either way."

This tests it. The controller below regulates STATE instead of following a schedule:

  * it climbs while its airspeed is above a target and descends when it falls below, which is
    the energy trade a glider actually flies, rather than turning at a fixed height;
  * it banks in proportion to how far it is from the heading it wants, instead of a fixed angle;
  * it reduces lift coefficient when the load factor is high and raises it when slow, which is
    what keeps a real wing off its stall.

If the knife edge is a property of the PHYSICS, feedback will not help and this will be as
fragile as the open-loop family. If it is a property of the POLICY, the basin should widen.
That is a real question with two possible answers, which is why it is worth running.
"""
import math

G, RHO = 9.81, 1.225
from geometry import MASS_KG as _M, S_LIFTING_M2 as _S  # noqa: E402  one definition; see analysis/geometry.py
M = _M                  # was: 4.0e-4 * (2.6/4.0)**3, re-typed alongside it
S = _S                  # was: 1.4e-4 * (2.6/4.0)**2 * 2.65, re-typed in 9 files
CD0 = 0.27
Z0, KARMAN = 2.0e-4, 0.41
DT = 5.0e-5
V_EXIT = 1.60
CL_MIN, CL_MAX = 0.4, 1.75
N_MAX = 40.0          # load factor above which the controller sheds lift


def wind(z, us):
    return 0.0 if z <= Z0 else (us / KARMAN) * math.log(z / Z0)


def fly(us, v_target, k_bank, z_target, ang_deg=30.0, t_max=6.0, v_exit=None):
    v_exit = V_EXIT if v_exit is None else v_exit
    th = math.radians(ang_deg)
    vx, vy, vz = -v_exit * math.cos(th), 0.0, v_exit * math.sin(th)
    z, t = 0.0, 0.0
    zmax = 0.0
    W = M * G
    while t < t_max:
        w = wind(max(z, 0.0), us)
        ax, ay, az = vx + w, vy, vz
        v = math.sqrt(ax * ax + ay * ay + az * az)
        if v < 1e-9:
            break
        ux, uy, uz = ax / v, ay / v, az / v

        # --- FEEDBACK, not a schedule -------------------------------------------------
        # 1. CL regulates airspeed: slow -> more lift, fast -> less. Clamped to the wing.
        cl = CL_MIN + (CL_MAX - CL_MIN) * max(0.0, min(1.0, (v_target - v) / v_target + 0.6))
        L = 0.5 * RHO * S * cl * v * v
        # 2. shed lift if the load factor would exceed what the structure is flown to
        if L / W > N_MAX:
            L = N_MAX * W
            cl = L / (0.5 * RHO * S * v * v)
        # 3. bank in PROPORTION to the height error, turning harder the further off we are
        err = (z - z_target) / max(z_target, 0.01)
        bank = max(-1.2, min(1.2, k_bank * err))
        # 4. head into wind when low (to climb), downwind when high (to gain speed)
        want_upwind = z < z_target
        if (want_upwind and vx > 0) or ((not want_upwind) and vx < 0):
            bank = math.copysign(max(abs(bank), 0.6), bank if bank != 0 else 1.0)
        # ------------------------------------------------------------------------------

        D = 0.5 * RHO * S * CD0 * v * v
        hx, hy = -uy, ux
        hn = math.hypot(hx, hy) or 1.0
        hx, hy = hx / hn, hy / hn
        px, py, pz = -uz * ux, -uz * uy, (ux * ux + uy * uy)
        pn = math.sqrt(px * px + py * py + pz * pz) or 1.0
        px, py, pz = px / pn, py / pn, pz / pn
        cb, sb = math.cos(bank), math.sin(bank)
        lx, ly, lz = cb * px + sb * hx, cb * py + sb * hy, cb * pz
        vx += ((-D * ux + L * lx) / M) * DT
        vy += ((-D * uy + L * ly) / M) * DT
        vz += ((-D * uz + L * lz) / M - G) * DT
        z += vz * DT
        t += DT
        zmax = max(zmax, z)
        if z < 0.0 and t > DT * 100:
            break
    return {"t": t, "z": z, "zmax": zmax,
            "aloft": t >= t_max - DT * 2 and z > 0.0}


def robustness(us, vt, kb, zt):
    """12 one-at-a-time perturbations, exactly as claim 975 applied to the open-loop family."""
    hits = 0
    for d in (-10, 10):
        hits += fly(us, vt, kb, zt, v_exit=V_EXIT * (1 + d / 100))["aloft"]
    for d in (-10, 10):
        hits += fly(us, vt, kb, zt, ang_deg=30.0 + d)["aloft"]
    for f in (0.9, 1.1):
        hits += fly(us * f, vt, kb, zt)["aloft"]
    for f in (0.9, 1.1):
        hits += fly(us, vt * f, kb, zt)["aloft"]
    for f in (0.8, 1.2):
        hits += fly(us, vt, kb * f, zt)["aloft"]
    for f in (0.8, 1.2):
        hits += fly(us, vt, kb, zt * f)["aloft"]
    return hits


def main():
    print("=" * 78)
    print("CLOSED-LOOP CONTROLLER: IS THE KNIFE EDGE THE POLICY OR THE PHYSICS?")
    print("=" * 78)
    print("\n  open-loop baseline (claim 975): most robust of 24 survived 5 of 12\n")
    print(f"  {'u*':>6} {'v_target':>9} {'k_bank':>8} {'z_target':>9} {'sustains':>9} {'robust':>8}")
    print("  " + "-" * 58)
    best = (0, None)
    for us in (0.60, 0.90, 1.20):
        for vt in (8.0, 12.0, 16.0):
            for kb in (1.0, 2.0, 4.0):
                for zt in (1.0, 2.0, 3.0):
                    r = fly(us, vt, kb, zt)
                    if not r["aloft"]:
                        continue
                    rb = robustness(us, vt, kb, zt)
                    if rb > best[0]:
                        best = (rb, (us, vt, kb, zt))
                    if rb >= 8:
                        print(f"  {us:>6.2f} {vt:>8.1f} {kb:>8.1f} {zt:>8.1f} "
                              f"{'yes':>9} {rb:>6}/12")
    rb, p = best
    print("\n" + "-" * 78)
    if p:
        print(f"  BEST: {rb} of 12 perturbations survived, at u* {p[0]}, v_target {p[1]}, "
              f"k_bank {p[2]}, z_target {p[3]}")
        if rb > 5:
            print(f"  That is better than the open-loop family's best of 5 of 12, so the knife")
            print(f"  edge is at least partly a property of the POLICY rather than the physics.")
        else:
            print(f"  That is no better than the open-loop family's 5 of 12, so the knife edge")
            print(f"  is a property of the PHYSICS and feedback does not rescue it.")
    else:
        print("  NO closed-loop controller in this family sustains at all.")
    print("=" * 78)
    return best


def controls():
    print("\nCONTROLS")
    ok = True
    r = fly(0.0, 12.0, 2.0, 2.0)
    arm1 = not r["aloft"]
    print(f"  [{'ok' if arm1 else 'FAIL'}] with NO wind the closed loop does not sustain "
          f"(peak {r['zmax']*100:.1f} cm) -- feedback is not manufacturing energy")
    ok &= arm1
    r2 = fly(1.20, 12.0, 2.0, 2.0)
    arm2 = r2["zmax"] > r["zmax"]
    print(f"  [{'ok' if arm2 else 'FAIL'}] wind raises the peak "
          f"({r['zmax']*100:.1f} -> {r2['zmax']*100:.1f} cm)")
    ok &= arm2
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
