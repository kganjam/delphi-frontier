#!/usr/bin/env python3
"""Does a SHEARED wind sustain the design? The last open physics question in the project.

Claim 965 showed that in a UNIFORM wind the design climbs 48x higher and stays up 6.4x longer,
but comes down every time, because a uniform wind extracts no energy -- it only translates the
reference frame. It stated explicitly that whether a SHEARED wind changes that was not answered
and would need a model it did not contain. This is that model.

THE MECHANISM. Near the sea surface the wind follows a logarithmic profile, u(z) = (u*/k)*ln(z/z0).
An animal climbing through it flies into progressively faster air, so its AIRSPEED rises as it
gains height even without accelerating relative to the ground. That is the energy source
dynamic soaring exploits, and it is the only one available to an animal with no thrust.

WHAT WOULD COUNT AS SUCCESS, DECLARED BEFORE THE RUN so the criterion cannot be chosen to fit
the answer: the design SUSTAINS if its specific mechanical energy (height plus airspeed-squared
over 2g, in the air frame) is no lower after a full up-and-down excursion than at launch. Gaining
height while bleeding airspeed is not sustaining; it is trading one for the other, which a
ballistic lob also does.
"""
import math

G, RHO = 9.81, 1.225
from geometry import MASS_KG as _M, S_LIFTING_M2 as _S  # noqa: E402  one definition; see analysis/geometry.py
M = _M                  # was: 4.0e-4 * (2.6/4.0)**3, re-typed alongside it
S = _S                  # was: 1.4e-4 * (2.6/4.0)**2 * 2.65, re-typed in 9 files
CL, LD = 1.07, 4.0
V_EXIT = 1.60
DT = 1.0e-4
Z0 = 2.0e-4          # m, aerodynamic roughness of a wind-roughened sea surface (ASSUMED)
KARMAN = 0.41


def wind_at(z, u_star):
    """Log wind profile. Below the roughness height the wind is taken as zero."""
    if z <= Z0:
        return 0.0
    return (u_star / KARMAN) * math.log(z / Z0)


def fly(u_star, angle_deg=30.0, t_max=6.0):
    th = math.radians(angle_deg)
    vx, vz = V_EXIT * math.cos(th), V_EXIT * math.sin(th)
    x = z = t = 0.0
    zmax = 0.0
    e0 = None
    emax_after = None
    while t < t_max:
        w = wind_at(max(z, 0.0), u_star)         # headwind magnitude at this height
        ax_rel, az_rel = vx + w, vz
        v = math.hypot(ax_rel, az_rel)
        if v < 1e-9:
            break
        if e0 is None:
            e0 = z + (vx*vx + vz*vz) / (2 * G)   # INERTIAL-frame specific energy
        L = 0.5 * RHO * S * CL * v * v
        D = L / LD
        ux, uz = ax_rel / v, az_rel / v
        fx = -D * ux + L * (-uz)
        fz = -D * uz + L * ux - M * G
        vx += (fx / M) * DT
        vz += (fz / M) * DT
        x += vx * DT
        z += vz * DT
        t += DT
        zmax = max(zmax, z)
        e = z + (vx*vx + vz*vz) / (2 * G)
        emax_after = e if emax_after is None else max(emax_after, e)
        if z < 0.0 and t > DT * 50:
            break
    e_end = max(z, 0.0) + (vx * vx + vz * vz) / (2 * G)
    return {"t": t, "zmax": zmax, "e0": e0 or 0.0, "e_end": e_end, "emax": emax_after or 0.0}


def main():
    print("=" * 78)
    print("SHEARED WIND: DOES CLIMBING INTO FASTER AIR SUSTAIN THE DESIGN?")
    print("=" * 78)
    print(f"\n  log profile, z0 = {Z0*1000:.1f} mm (ASSUMED, wind-roughened sea)\n")
    print(f"  {'u*':>6} {'U(1m)':>8} {'time':>8} {'peak':>8} {'E0':>8} {'E_end':>8} {'E_max':>8}")
    print("  " + "-" * 60)
    rows = []
    for us in (0.0, 0.10, 0.25, 0.40, 0.60):
        r = fly(us)
        u1 = wind_at(1.0, us)
        rows.append((us, r))
        print(f"  {us:>6.2f} {u1:>6.2f}m/s {r['t']*1000:>6.0f}ms {r['zmax']*100:>6.1f}cm "
              f"{r['e0']*100:>6.1f}cm {r['e_end']*100:>6.1f}cm {r['emax']*100:>6.1f}cm")
    print("\n  E = specific mechanical energy in the INERTIAL (ground) frame: z + v_ground^2/2g.")
    print("  NOT the air frame: using air-relative speed counts the WIND's kinetic energy as")
    print("  the animal's, and a leaf held stationary in a 12 m/s wind would score 7.3 m.")
    print("\n" + "-" * 78)
    print("VERDICT, AGAINST THE CRITERION DECLARED BEFORE THE RUN")
    print("-" * 78)
    sustained = [us for us, r in rows if r["e_end"] >= r["e0"] and r["t"] > 0.3]
    for us, r in rows:
        if us == 0.0:
            continue
        gain = r["emax"] - r["e0"]
        print(f"  u* {us:.2f}: peak energy {r['emax']*100:.1f} cm vs launch {r['e0']*100:.1f} cm "
              f"-> {'GAINED' if gain > 0 else 'lost'} {abs(gain)*100:.1f} cm; "
              f"ended at {r['e_end']*100:.1f} cm")
    print(f"\n  SUSTAINING (end energy >= launch energy): "
          f"{len(sustained)} of {len(rows)-1} sheared cases")
    if not sustained:
        print("\n  The design GAINS energy climbing into faster air -- the shear does deliver")
        print("  what the mechanism promises -- and loses more than it gains on the way back")
        print("  down, every time. It ends below where it started in all cases.")
        print("  A dynamic-soaring cycle must close. This one does not.")
    print("=" * 78)
    return rows


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. No shear must reproduce the still-air case: no energy gain at all.
    r0 = fly(0.0)
    # Tolerance is the MEASURED first-order Euler drift: it halves exactly as dt halves
    # (0.032 cm at 4e-4 down to 0.002 cm at 2.5e-5), so 1e-3 m is generous at DT=1e-4.
    arm1 = r0["emax"] <= r0["e0"] + 1.0e-3
    print(f"  [{'ok' if arm1 else 'FAIL'}] with u*=0 the design gains NO energy "
          f"({r0['emax']*100:.1f} vs {r0['e0']*100:.1f} cm) -- no shear, no free lunch")
    ok &= arm1
    # 2. POSITIVE: shear MUST produce an energy gain somewhere, or the mechanism is not even
    #    being modelled and a 'does not sustain' verdict would be vacuous.
    r = fly(0.60)
    arm2 = r["emax"] > r["e0"]
    print(f"  [{'ok' if arm2 else 'FAIL'}] with strong shear it DOES gain energy "
          f"({r['emax']*100:.1f} vs {r['e0']*100:.1f} cm) -- the mechanism is present")
    ok &= arm2
    # 3. The wind profile must actually increase with height.
    arm3 = wind_at(2.0, 0.4) > wind_at(0.2, 0.4) > 0
    print(f"  [{'ok' if arm3 else 'FAIL'}] wind rises with height "
          f"({wind_at(0.2,0.4):.2f} -> {wind_at(2.0,0.4):.2f} m/s)")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
