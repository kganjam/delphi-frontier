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
    print(f"\n  BEST lift-attributable distance over every combination: {best:.2f} cm")
    print(f"  falsifier threshold: 2 cm")
    print(f"  => S901 {'is NEGATIVELY settled' if best < 2.0 else 'is NOT settled negatively'}")
    print("\n  Note the 20 cm2 and 26.7 cm2 rows are areas the fish DOES NOT HAVE -- present")
    print("  whole-body silhouette is 1.4 cm2. They are included because the falsifier says")
    print("  'even at the favourable end of every input', and an area it cannot reach is the")
    print("  most favourable input available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
