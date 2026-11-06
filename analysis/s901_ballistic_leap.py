#!/usr/bin/env python3
"""S901: does a 0.4 g zebrafish leaving water at 1.57 m/s gain any horizontal distance from LIFT?

The falsifier, fixed before this ran: lift-attributable horizontal distance under 2 cm even at the
favourable end of every input, OR re-entry before the flight-path angle falls below 20 degrees,
settles it negatively.

"Lift-attributable" is the difference between the trajectory WITH aerodynamic forces and the pure
ballistic one from the same launch -- not the total range, which is mostly ballistic and would
flatter the design.

The integration is explicit Euler at 0.1 ms, which is crude and adequate: the control below
reproduces the analytic ballistic range to better than 0.1 mm, so the integrator is not what
decides the answer.
"""
from __future__ import annotations

import math

G = 9.81
RHO = 1.225
M = 4.0e-4            # kg
V0 = 1.57             # m/s, Demesmay mean of maximal
ANGLE = math.radians(45.0)
DT = 1.0e-4


def fly(area: float, cl: float, cd: float, v0: float = V0, ang: float = ANGLE) -> tuple[float, float, float]:
    """Return (range_m, min_flight_path_angle_deg, time_s). area=0 gives pure ballistics."""
    x, y = 0.0, 0.0
    vx, vy = v0 * math.cos(ang), v0 * math.sin(ang)
    min_ang = 90.0
    t = 0.0
    while y >= 0.0 and t < 5.0:
        v = math.hypot(vx, vy)
        if v > 1e-9 and area > 0.0:
            q = 0.5 * RHO * v * v * area
            L, D = cl * q, cd * q
            # lift perpendicular to velocity, drag opposed
            ux, uy = vx / v, vy / v
            ax = (-D * ux - L * uy) / M
            ay = (-D * uy + L * ux) / M - G
        else:
            ax, ay = 0.0, -G
        vx += ax * DT
        vy += ay * DT
        x += vx * DT
        y += vy * DT
        t += DT
        if vx != 0:
            min_ang = min(min_ang, math.degrees(math.atan2(vy, vx)))
    return x, min_ang, t


def main() -> int:
    bal, _, bt = fly(0.0, 0.0, 0.0)
    analytic = V0 * V0 * math.sin(2 * ANGLE) / G
    print(f"  CONTROL -- integrator against the analytic ballistic range:")
    print(f"    integrated {bal*100:.3f} cm   analytic {analytic*100:.3f} cm   "
          f"diff {abs(bal-analytic)*1000:.4f} mm   {'ok' if abs(bal-analytic) < 1e-4 else '*** BAD ***'}")
    print(f"    pure ballistic flight time {bt*1000:.1f} ms\n")

    print(f"  {'area cm2':>9} {'CL':>5} {'CD':>5} {'range cm':>9} {'ballistic cm':>13} "
          f"{'LIFT-ATTRIB cm':>15} {'min angle':>10}")
    best = -1.0
    for area_cm2 in (1.4, 20.0, 26.7):
        for cl in (0.6, 1.07):
            for cd in (0.1, 0.3):
                r, ma, _ = fly(area_cm2 * 1e-4, cl, cd)
                attrib = (r - bal) * 100
                best = max(best, attrib)
                print(f"  {area_cm2:>9.1f} {cl:>5.2f} {cd:>5.2f} {r*100:>9.2f} {bal*100:>13.2f} "
                      f"{attrib:>15.2f} {ma:>9.1f}d")
    print(f"\n  BEST lift-attributable distance at the FIXED 45 deg launch: {best:.2f} cm")

    # ----------------------------------------------------------------------
    # LAUNCH ANGLE SWEEP -- added after claude-opus-5-5, reviewing claim 520 in the
    # adversarial arm, objected that "every winged combination is integrated only at the
    # 45 deg launch angle, which is optimal for a ballistic body but not for a lifting one".
    # That is correct and it is a real gap: lift acts perpendicular to velocity, so on the
    # ASCENDING half of a steep arc it points partly BACKWARD and costs horizontal distance.
    # A glider should launch shallow. The falsifier says "the favourable end of every input",
    # and launch angle is an input that was not swept. Nothing below is tuned -- it is the
    # same integrator over a grid.
    # ----------------------------------------------------------------------
    print("\n  LAUNCH ANGLE SWEEP (the arm the adversarial reviewer asked for)\n")
    bal_best, bal_best_ang = -1.0, None
    for deg in range(5, 66, 5):
        r, _, _ = fly(0.0, 0.0, 0.0, ang=math.radians(deg))
        if r > bal_best:
            bal_best, bal_best_ang = r, deg
    print(f"  best PURE BALLISTIC range over the same grid: {bal_best*100:.2f} cm "
          f"at {bal_best_ang} deg (the analytic optimum is 45 deg)")

    sweep_best, sweep_cfg = -1.0, None
    rows = []
    for area_cm2 in (1.4, 20.0, 26.7):
        for cl in (0.6, 1.07):
            for cd in (0.1, 0.3):
                for deg in range(5, 66, 5):
                    r, _, _ = fly(area_cm2 * 1e-4, cl, cd, ang=math.radians(deg))
                    # compare against the best the SAME body could do with no wing at all,
                    # which is the honest attribution: what did the lift surface buy?
                    attrib = (r - bal_best) * 100
                    rows.append((attrib, area_cm2, cl, cd, deg, r))
                    if attrib > sweep_best:
                        sweep_best, sweep_cfg = attrib, (area_cm2, cl, cd, deg, r)
    rows.sort(reverse=True)
    print(f"\n  {'area cm2':>9} {'CL':>5} {'CD':>5} {'launch':>7} {'range cm':>9} "
          f"{'LIFT-ATTRIB cm':>15}")
    for attrib, a_, cl_, cd_, deg_, r_ in rows[:8]:
        print(f"  {a_:>9.1f} {cl_:>5.2f} {cd_:>5.2f} {deg_:>6}d {r_*100:>9.2f} {attrib:>15.2f}")
    a_, cl_, cd_, deg_, r_ = sweep_cfg
    print(f"\n  BEST over area x CL x CD x LAUNCH ANGLE: {sweep_best:.2f} cm")
    print(f"    at area {a_} cm2, CL {cl_}, CD {cd_}, launch {deg_} deg, range {r_*100:.2f} cm")
    if sweep_best > best:
        print(f"    the angle sweep RAISED the best from {best:.2f} to {sweep_best:.2f} cm, "
              "so the 45 deg restriction WAS costing lift-attributable distance")
    best = max(best, sweep_best)

    # ----------------------------------------------------------------------
    # The winning configuration uses 26.7 cm2, which the fish DOES NOT HAVE -- its present
    # whole-body silhouette is 1.4 cm2. A verdict quoted from an area it cannot reach answers
    # a question nobody asked. So the useful form of S901 is not yes/no but: HOW MUCH LIFTING
    # SURFACE DOES THE 2 cm THRESHOLD REQUIRE? That turns a settled/unsettled flag into a
    # quantitative demand the enlargement work (S904) can be held against.
    # ----------------------------------------------------------------------
    print("\n  LIFT-ATTRIBUTABLE DISTANCE BY AREA (angle and coefficients swept)\n")
    print(f"  {'area cm2':>9} {'x present':>10} {'best attrib cm':>15}  clears 2 cm?")
    for a in (1.4, 2.0, 3.0, 5.0, 7.0, 10.0, 14.0, 20.0, 26.7):
        b = max((fly(a * 1e-4, cl, cd, ang=math.radians(d))[0] - bal_best) * 100
                for cl in (0.6, 1.07) for cd in (0.1, 0.3) for d in range(5, 66, 5))
        print(f"  {a:>9.1f} {a/1.4:>9.1f}x {b:>15.2f}  {'YES' if b >= 2.0 else 'no'}")

    lo, hi = 1.0, 40.0
    for _ in range(50):
        mid = (lo + hi) / 2
        b = max((fly(mid * 1e-4, 1.07, 0.1, ang=math.radians(d))[0] - bal_best) * 100
                for d in range(5, 66, 5))
        lo, hi = (lo, mid) if b >= 2.0 else (mid, hi)
    area_2cm = hi
    q = 0.5 * RHO * V0 * V0
    area_lw1 = (M * G) / (1.07 * q) * 1e4          # area at which lift equals weight, cm2

    print(f"\n  TWO THRESHOLDS, AND THEY ARE FAR APART:")
    print(f"    {area_2cm:>5.1f} cm2 ({area_2cm/1.4:.1f}x present) buys the 2 cm the falsifier asked for;")
    print(f"           L/W there is only {1.07*q*area_2cm*1e-4/(M*G):.2f}, so this is a lifting-assisted")
    print(f"           BALLISTIC ARC, not a glide -- the animal is still falling throughout.")
    print(f"    {area_lw1:>5.1f} cm2 ({area_lw1/1.4:.1f}x present) is where lift first equals weight at")
    print(f"           {V0} m/s, which is the floor for anything describable as GLIDING.")
    print("\n  So S901's own threshold is met by a far smaller wing than flight requires, and")
    print("  reporting only 'clears 2 cm' would overstate what the animal could do.")

    print(f"\n  falsifier threshold: 2 cm")
    print(f"  => S901 {'is NEGATIVELY settled' if best < 2.0 else 'is NOT settled negatively'}")
    print("\n  Note the 20 cm2 and 26.7 cm2 rows are areas the fish DOES NOT HAVE -- present")
    print("  whole-body silhouette is 1.4 cm2. They are included because the falsifier says")
    print("  'even at the favourable end of every input', and an area it cannot reach is the")
    print("  most favourable input available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
