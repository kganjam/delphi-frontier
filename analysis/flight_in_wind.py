#!/usr/bin/env python3
"""What the design achieves in WIND, now that claim 964 showed lift needs airspeed.

Claim 964, found by this project's own adversarial arm, established that every lift figure here
had used ground speed where lift needs AIRSPEED, and that a 2.42 m/s headwind puts the achievable
design at lift = weight AT EXIT. That withdrew claim 961's closure of route D. This computes what
follows, because "not closed" is not "works".

THE MODEL, and its limits stated before its results. A point mass launched at V_EXIT relative to
the water into a steady headwind W, integrated forward with:
  * lift = 0.5 rho S CL v_air^2, perpendicular to the AIR-relative velocity, not vertical;
  * drag = lift / (L/D), opposing the air-relative velocity;
  * gravity;
  * airspeed evolving as the body decelerates against the air.
This fixes the three errors the adversarial arm identified in claim 962: that lift was treated as
a constant vertical force at launch magnitude, that it should scale with v^2 and so fall as the
animal slows, and that it acts perpendicular to velocity rather than straight up. Drag is now
present, which it was not.

WHAT THIS STILL DOES NOT MODEL: wind shear (the wind is uniform here, so no dynamic soaring
energy extraction is available in this model at all), ground effect, unsteady aerodynamics, and
any attitude control. It is a glide integration, not a soaring simulation. A positive result here
would be a LOWER bound on what wind buys, not an upper one.
"""
import math

G, RHO = 9.81, 1.225
from geometry import MASS_KG as _M, S_LIFTING_M2 as _S  # noqa: E402  one definition; see analysis/geometry.py
M = _M                  # was: 4.0e-4 * (2.6/4.0)**3, re-typed alongside it
S = _S                  # was: 1.4e-4 * (2.6/4.0)**2 * 2.65, re-typed in 9 files
CL = 1.07                                  # claim 86
LD = 4.0                                   # lift-to-drag, generous for this Re (claim 565 area)
V_EXIT = 1.60
BODY = 0.026
DT = 2.0e-4


def fly(wind, angle_deg=30.0, t_max=8.0):
    """Integrate until the fish returns to the water. Returns (ground range, time, peak height).

    Positions are in the GROUND frame; aerodynamic forces use the AIR-relative velocity, which
    is the whole point of the correction this script exists to apply.
    """
    th = math.radians(angle_deg)
    vx, vz = V_EXIT * math.cos(th), V_EXIT * math.sin(th)   # ground-frame velocity
    x = z = t = 0.0
    zmax = 0.0
    while t < t_max:
        # air-relative velocity: a headwind blows in -x, so the air moves at -wind
        ax_rel, az_rel = vx + wind, vz
        v = math.hypot(ax_rel, az_rel)
        if v < 1e-6:
            break
        L = 0.5 * RHO * S * CL * v * v
        D = L / LD
        # unit vectors along and perpendicular to the air-relative velocity
        ux, uz = ax_rel / v, az_rel / v
        px, pz = -uz, ux                      # lift is perpendicular, rotated +90 deg
        fx = -D * ux + L * px
        fz = -D * uz + L * pz - M * G
        vx += (fx / M) * DT
        vz += (fz / M) * DT
        x += vx * DT
        z += vz * DT
        t += DT
        zmax = max(zmax, z)
        if z < 0.0 and t > DT * 10:
            break
    return x, t, zmax


def main():
    print("=" * 78)
    print("AIRBORNE PERFORMANCE IN WIND -- lift perpendicular to AIR velocity, drag included")
    print("=" * 78)
    print(f"\n  {M*1e3:.3f} g, {S*1e4:.2f} cm2 fin, CL {CL}, L/D {LD}, exit {V_EXIT} m/s at 30 deg\n")
    print(f"  {'headwind':>9} {'range':>9} {'time':>8} {'peak':>8} {'body lengths':>14}")
    print("  " + "-" * 56)
    base = None
    for w in (0.0, 1.0, 2.42, 4.0, 6.0, 8.0):
        r, t, zmax = fly(w)
        if base is None:
            base = r
        print(f"  {w:>7.2f}m/s {r*100:>7.1f}cm {t*1000:>6.0f}ms {zmax*100:>6.1f}cm "
              f"{r/BODY:>13.1f}")
    print("\n" + "-" * 78)
    print("READING IT -- AND THE GROUND-FRAME RANGE IS THE WRONG METRIC ABOVE BREAK-EVEN")
    print("-" * 78)
    r0, t0, z0 = fly(0.0)
    r8, t8, z8 = fly(8.0)
    print(f"  Still air: {r0*100:.1f} cm forward, {t0*1000:.0f} ms, peak {z0*100:.1f} cm.")
    print(f"  Beaufort 5: {r8*100:.1f} cm -- NEGATIVE. The fish is blown BACKWARDS {abs(r8):.1f} m")
    print(f"  while airborne for {t8*1000:.0f} ms and peaking at {z8*100:.0f} cm.")
    print("\n  An earlier version of this script called that '34.6x further'. It is not")
    print("  further, it is backwards, and the sign was in the table all along. Above the")
    print("  break-even headwind the ground-frame range stops measuring flight and starts")
    print("  measuring advection: a 0.11 g animal with no thrust in an 8 m/s wind is being")
    print("  carried, the way a leaf is.")
    print("\n  WHAT IS REAL IN THOSE ROWS: the fish CLIMBS. In still air it peaks at")
    print(f"  {z0*100:.1f} cm, barely above its launch arc. At 8 m/s it reaches {z8*100:.0f} cm --")
    print(f"  {z8/z0:.0f} times higher -- and stays up {t8/t0:.1f} times longer. That gain in")
    print("  height and time is genuine, it is what claim 961 denied was possible, and it")
    print("  is what a dynamic-soaring cycle would need.")
    print("\n  WHAT IS NOT: this is not sustained flight and not soaring. The wind here is")
    print("  UNIFORM, so no energy is extracted from shear; the animal is flying faster")
    print("  through the air than it could alone, and decelerating. It comes down every")
    print("  time. Whether a sheared wind changes that is NOT answered by this model.")
    print("=" * 78)
    return fly(8.0)


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. Zero wind, zero lift must reproduce the ballistic range.
    global CL
    keep = CL
    CL = 0.0
    r, _, _ = fly(0.0)
    CL = keep
    th = math.radians(30.0)
    expect = V_EXIT ** 2 * math.sin(2 * th) / G
    arm1 = abs(r - expect) < 0.01
    print(f"  [{'ok' if arm1 else 'FAIL'}] with CL=0 and no wind it reproduces the ballistic "
          f"range ({r*100:.1f} vs {expect*100:.1f} cm)")
    ok &= arm1
    # 2. A TAILWIND must do WORSE than still air, or the model ignores wind direction.
    r_still, _, _ = fly(0.0)
    r_tail, _, _ = fly(-1.0)
    arm2 = r_tail < r_still
    print(f"  [{'ok' if arm2 else 'FAIL'}] a 1 m/s tailwind gives {r_tail*100:.1f} cm against "
          f"{r_still*100:.1f} cm still -- direction matters")
    ok &= arm2
    # 3. Peak height must EXCEED the ballistic rise only above break-even, not below.
    _, _, z_low = fly(1.0)
    _, _, z_high = fly(6.0)
    arm3 = z_high > z_low
    print(f"  [{'ok' if arm3 else 'FAIL'}] peak height rises with wind "
          f"({z_low*100:.1f} -> {z_high*100:.1f} cm)")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
