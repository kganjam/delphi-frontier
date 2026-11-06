#!/usr/bin/env python3
"""Where in (exit speed, fin area) does the leap clear S901's threshold? The map, not one point.

Every shortfall this project has reported is a single point on a surface. Claim 523 computed that
4.4x AREA clears the 2 cm lift-attributable threshold -- but it computed it AT ONE EXIT SPEED,
1.57 m/s. Lift goes as v^2 A, so area and speed trade off, and the achievable-area ceiling
(2.65x, reached independently by alf and by longfin -- claims 529 and 542) is only binding at a
particular speed.

This integrates the same trajectory model over a grid and reports the FEASIBLE REGION: which
combinations clear 2 cm, and specifically what exit speed the ACHIEVABLE fin would need.

It does NOT relax anything. The threshold, the model, the mass and the drag are the ones already
recorded; only the speed axis is opened, because it was never a fixed quantity -- it is an input
S900 measured and S901 held constant.

Usage:  python3 feasible_region.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s901_ballistic_leap import fly  # noqa: E402

PRESENT_AREA_CM2 = 1.4        # whole-body dorsal silhouette
ACHIEVED_AREA_RATIO = 2.65    # best measured, alf and longfin alike (claims 529, 542)
MEASURED_V = 1.57             # m/s, exit speed S900/S901 used
THRESHOLD_CM = 2.0            # lift-attributable distance, from S901's falsifier
CL, CD = 1.07, 0.1            # the favourable end, as the falsifier requires


def best_attrib(area_cm2: float, v: float) -> float:
    """Best lift-attributable distance over launch angle, in cm, at this area and speed."""
    bal = max(fly(0.0, 0.0, 0.0, v0=v, ang=math.radians(d))[0] for d in range(5, 66, 5))
    win = max(fly(area_cm2 * 1e-4, CL, CD, v0=v, ang=math.radians(d))[0]
              for d in range(5, 66, 5))
    return (win - bal) * 100


def main() -> int:
    print(f"  threshold {THRESHOLD_CM} cm lift-attributable, CL {CL}, CD {CD}, "
          f"launch angle swept 5-65 deg\n")
    speeds = [1.57, 1.8, 2.0, 2.25, 2.5, 3.0]
    ratios = [1.0, 1.9, 2.65, 4.4, 6.0]
    print(f"  {'area x':>7} " + "".join(f"{v:>8.2f}" for v in speeds) + "   m/s")
    for r in ratios:
        row = f"  {r:>7.2f} "
        for v in speeds:
            a = best_attrib(PRESENT_AREA_CM2 * r, v)
            row += f"{a:>8.2f}"
        tag = ""
        if abs(r - ACHIEVED_AREA_RATIO) < 0.01:
            tag = "  <- BEST MEASURED (alf, longfin)"
        if abs(r - 1.0) < 0.01:
            tag = "  <- present fin"
        print(row + tag)
    print("\n  (cells are lift-attributable cm; >= 2.00 clears the threshold)\n")

    # BISECTION IS ONLY VALID ON THE SPEED AXIS, AND THAT HAD TO BE CHECKED RATHER THAN ASSUMED.
    # Lift-attributable distance is MONOTONIC in speed at fixed area (1.12, 2.05, 3.17, 5.04,
    # 8.14 across the grid row), so bisecting speed is sound. It is NOT monotonic in AREA: at
    # 1.57 m/s it peaks near 28x and falls after, because beyond some area the drag penalty
    # exceeds the lift gain and the winged trajectory lands SHORT of the ballistic one. A
    # bisection over area therefore converges on whatever its bracket happens to enclose. One
    # did, in an earlier version of this analysis, and returned "400x" -- which was the search
    # CEILING, not a crossing. The true first crossing at 0.842 m/s is near 44x, found by
    # scanning upward. Area questions are scanned here; only speed is bisected.
    # What speed does the ACHIEVABLE fin need? Bisect rather than read off the grid.
    lo, hi = MEASURED_V, 6.0
    if best_attrib(PRESENT_AREA_CM2 * ACHIEVED_AREA_RATIO, hi) < THRESHOLD_CM:
        print("  even at 6 m/s the achievable fin does not clear it")
        return 1
    for _ in range(40):
        mid = (lo + hi) / 2
        if best_attrib(PRESENT_AREA_CM2 * ACHIEVED_AREA_RATIO, mid) >= THRESHOLD_CM:
            hi = mid
        else:
            lo = mid
    v_need = hi
    print(f"  THE ACHIEVABLE FIN ({ACHIEVED_AREA_RATIO}x area) CLEARS 2 cm AT {v_need:.2f} m/s")
    print(f"    against the {MEASURED_V} m/s S900 and S901 used: a {v_need/MEASURED_V:.2f}x "
          f"speed increase")
    print(f"    in body lengths per second for a 4 cm fish: "
          f"{MEASURED_V/0.04:.0f} BL/s now, {v_need/0.04:.0f} BL/s required")

    # The naive scaling, stated so the difference from the integrated answer is visible.
    naive = MEASURED_V * math.sqrt(4.4 / ACHIEVED_AREA_RATIO)
    print(f"\n  CONTROL -- the v^2*A hand-scaling predicts {naive:.2f} m/s. The integrated answer "
          f"is {v_need:.2f}.")
    print(f"    They differ by {abs(v_need-naive)/naive*100:.0f}%, and the DIRECTION matters.")
    print(f"    The hand-scaling assumes required area goes as 1/v^2, i.e. that the lift benefit")
    print(f"    grows as v^2. Integrated, it grows as roughly v^4.4 at this area -- far steeper,")
    print(f"    because a faster launch raises BOTH the lift force and the time it acts over.")
    print(f"    So the hand-scaling OVERSTATES the speed required and is CONSERVATIVE, not")
    print(f"    optimistic. An earlier version of this script said optimistic, which had the")
    print(f"    sign backwards; the two numbers are printed above so the direction is checkable.")

    print(f"\n  WHETHER {v_need:.2f} m/s IS REACHABLE IS A SEPARATE, ALREADY-CONTESTED QUESTION.")
    print(f"    S900 settled that the measured-burst route does not reach TAKE-OFF speed, with a")
    print(f"    deficit of 2.29 even jointly optimistic -- but take-off is lift=weight, a much")
    print(f"    higher bar than this 2 cm threshold. And claim 21's 0.84 m/s fast-start was itself")
    print(f"    REFUTED by the panel as implying an implausible Reynolds number, so the project's")
    print(f"    own speed inputs disagree. This map says what speed is needed; it does not claim")
    print(f"    the fish can reach it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
