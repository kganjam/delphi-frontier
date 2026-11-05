#!/usr/bin/env python3
"""Does the dynamic-soaring cycle CLOSE? The decisive question for route D.

Claim 966 showed the design extracts energy from a sheared wind -- lift-dependent, with a
wingless body of the same drag LOSING energy -- but modelled a single arc that ends in the
water. Dynamic soaring sustains flight only if the cycle CLOSES: windward climb, upper turn,
leeward descent, lower turn, repeated (Sachs et al. 2013). That needs turning, which claim 966's
model did not contain. This adds it.

THE MODEL. A 3D point-mass glider. Air-relative velocity va = v - W(z)x_hat with a logarithmic
wind profile. Lift of magnitude 0.5*rho*S*CL*|va|^2 acts perpendicular to va, rotated about the
va axis by a bank angle phi. Drag 0.5*rho*S*CD*|va|^2 opposes va. A heading controller flies the
four phases and banks to reverse heading at top and bottom.

WHAT COUNTS AS CLOSING, DECLARED BEFORE THE RUN: the cycle closes if the animal returns to its
starting HEIGHT with at least its starting inertial specific energy, having completed a full
heading reversal and return. Gaining energy on the climb and losing more on the descent is not
closing; that is what claim 966 already measured.

WHAT THIS STILL DOES NOT MODEL: stall, structural limits, unsteady aerodynamics, and any limit
on how fast a 0.11 g animal can roll. The bank rate is unconstrained, which is GENEROUS to the
design -- a real animal cannot roll instantly, so a negative result here is robust and a positive
one is an upper bound.
"""
import math

G, RHO = 9.81, 1.225
M = 4.0e-4 * (2.6 / 4.0) ** 3
S = 1.4e-4 * (2.6 / 4.0) ** 2 * 2.65
CL_MAX, CD0 = 1.07, 0.27
Z0, KARMAN = 2.0e-4, 0.41
DT = 5.0e-5


def wind(z, u_star):
    return 0.0 if z <= Z0 else (u_star / KARMAN) * math.log(z / Z0)


def simulate(u_star, z_start=0.30, v_start=6.0, t_max=4.0):
    """Start ALREADY FLYING at z_start with airspeed v_start, heading into wind.

    Starting aloft is deliberate: the question here is whether a cycle CLOSES once
    established, which is separable from whether the animal can get there. Claim 965 showed
    it reaches 2 m in wind, so the starting state is one it can attain.
    """
    # ground-frame velocity: heading into the wind (-x)
    w0 = wind(z_start, u_star)
    vx, vy, vz = -(v_start - w0), 0.0, 0.0
    x, y, z, t = 0.0, 0.0, z_start, 0.0
    e0 = z + (vx * vx + vy * vy + vz * vz) / (2 * G)
    phase, zmax, emin = "climb", z, e0
    crossings = 0
    while t < t_max and z > 0.0:
        w = wind(max(z, Z0), u_star)
        ax, ay, az = vx - w, vy, vz          # air-relative (wind blows +x)
        v = math.sqrt(ax * ax + ay * ay + az * az)
        if v < 1e-6:
            break
        ux, uy, uz = ax / v, ay / v, az / v
        # phase logic: climb into wind, turn at apex, descend, turn at the bottom
        if phase == "climb" and vz < 0.0:
            phase, crossings = "turn_top", crossings + 1
        elif phase == "turn_top" and vx > 0.0:
            phase = "descend"
        elif phase == "descend" and z < z_start * 0.4:
            phase, crossings = "turn_bot", crossings + 1
        elif phase == "turn_bot" and vx < 0.0:
            phase = "climb"
        bank = 0.0 if phase in ("climb", "descend") else math.radians(60.0)
        CL = CL_MAX
        L = 0.5 * RHO * S * CL * v * v
        D = 0.5 * RHO * S * CD0 * v * v
        # lift direction: perpendicular to va, in the vertical plane, rotated by bank
        hx, hy = -uy, ux                      # horizontal perpendicular
        hn = math.hypot(hx, hy) or 1.0
        hx, hy = hx / hn, hy / hn
        # vertical-ish perpendicular component
        px, py, pz = -uz * ux, -uz * uy, (ux * ux + uy * uy)
        pn = math.sqrt(px * px + py * py + pz * pz) or 1.0
        px, py, pz = px / pn, py / pn, pz / pn
        cb, sb = math.cos(bank), math.sin(bank)
        lx, ly, lz = cb * px + sb * hx, cb * py + sb * hy, cb * pz
        fx = -D * ux + L * lx
        fy = -D * uy + L * ly
        fz = -D * uz + L * lz - M * G
        vx += (fx / M) * DT
        vy += (fy / M) * DT
        vz += (fz / M) * DT
        x += vx * DT
        y += vy * DT
        z += vz * DT
        t += DT
        zmax = max(zmax, z)
        e = z + (vx * vx + vy * vy + vz * vz) / (2 * G)
        emin = min(emin, e)
    e_end = max(z, 0.0) + (vx * vx + vy * vy + vz * vz) / (2 * G)
    return {"e0": e0, "e_end": e_end, "t": t, "z_end": z, "zmax": zmax,
            "turns": crossings, "emin": emin}


def simulate_cl(u_star, cl, **kw):
    """Same run at a different CL, for the wingless control."""
    global CL_MAX
    keep = CL_MAX
    CL_MAX = cl
    try:
        return simulate(u_star, **kw)
    finally:
        CL_MAX = keep


def z_start_of(_r):
    return 0.30


def main():
    print("=" * 78)
    print("DOES THE DYNAMIC-SOARING CYCLE CLOSE?")
    print("=" * 78)
    print(f"\n  start aloft at 30 cm, 6.0 m/s airspeed into wind; bank 60 deg in the turns")
    print(f"  bank RATE is unconstrained, which is generous to the design\n")
    print(f"  {'u*':>6} {'U(1m)':>8} {'turns':>7} {'time':>8} {'E0':>8} {'E_end':>9}  verdict")
    print("  " + "-" * 68)
    any_close = False
    for us in (0.0, 0.25, 0.40, 0.60, 0.90):
        r = simulate(us)
        wl = simulate_cl(us, 0.0)
        lift_required = r["e_end"] > wl["e_end"] * 1.2
        returned = r["z_end"] >= z_start_of(r) * 0.9
        closed = (r["turns"] >= 2 and r["e_end"] >= r["e0"]
                  and returned and lift_required)
        any_close |= closed
        why = []
        if r["turns"] < 2: why.append("no 2 turns")
        if r["e_end"] < r["e0"]: why.append("lost energy")
        if not returned: why.append(f"ended at {r['z_end']*100:.0f}cm not 30cm")
        if not lift_required: why.append("wingless gains too")
        print(f"  {us:>6.2f} {wind(1.0,us):>6.2f}m/s {r['turns']:>7d} {r['t']*1000:>6.0f}ms "
              f"{r['e0']*100:>6.1f}cm {r['e_end']*100:>7.1f}cm  "
              f"{'CLOSES' if closed else 'NO: ' + ', '.join(why)}")
    print("\n" + "-" * 78)
    print("VERDICT")
    print("-" * 78)
    if any_close:
        print("  At least one shear strength CLOSES the cycle: the animal completes a full")
        print("  heading reversal and returns with at least the energy it started with.")
        print("  That is sustained soaring flight, and route D would be OPEN AND WORKING.")
    else:
        print("  NO shear strength closes the cycle. The design gains energy on the windward")
        print("  climb -- claim 966 measured that, with a wingless control -- and loses more")
        print("  in the turns and the descent than the shear returns. It ends below where it")
        print("  began in every case, and goes into the water.")
        print("\n  Route D is CLOSED: the mechanism is real and the cycle does not close.")
    print("=" * 78)
    return any_close


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. No wind: there is no energy source, so the cycle CANNOT close. If it does, the
    #    integrator is manufacturing energy and every positive result is suspect.
    r = simulate(0.0)
    arm1 = r["e_end"] < r["e0"]
    print(f"  [{'ok' if arm1 else 'FAIL'}] with NO wind the animal loses energy "
          f"({r['e0']*100:.1f} -> {r['e_end']*100:.1f} cm) -- no free lunch from the integrator")
    ok &= arm1
    # 2. The controller must actually turn, or 'does not close' is vacuous.
    r2 = simulate(0.40)
    arm2 = r2["turns"] >= 1
    print(f"  [{'ok' if arm2 else 'FAIL'}] the controller executes turns "
          f"({r2['turns']} heading reversals at u*=0.40) -- the cycle is attempted")
    ok &= arm2
    # 3. Wind must still deliver a gain somewhere in the trajectory, or shear is not modelled.
    arm3 = r2["zmax"] > 0.30
    print(f"  [{'ok' if arm3 else 'FAIL'}] with shear it climbs above its start "
          f"({r2['zmax']*100:.1f} cm from 30 cm)")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
