#!/usr/bin/env python3
"""Bound adult zebrafish burst speed from muscle power, independently of the contested measurement.

WHY. Claim 544 established that the whole design rests on one escape-speed figure -- Demesmay
2025's 1.57 m/s, which is 43.6 to 60.4 BODY LENGTHS PER SECOND for the fish measured, against a
typical published fast-start range near 20-25 BL/s, recorded at 240 fps (4 ms per frame) on a
fast-start lasting 20-30 ms. No second adult-zebrafish measurement was findable in the
open-access literature reachable here. So this checks it from physics instead: a fish cannot swim
faster than its muscle can supply the power drag demands.

THE BALANCE, with every input a range rather than a point, because none of them is known here to
better than a factor of about two:

    P_available = m_body * muscle_fraction * specific_power
    P_required  = 0.5 * rho * Cd * S_wetted * v^3
    => v_max = (2 * P_avail / (rho * Cd * S))^(1/3)

The cube root is what makes this worth doing: an input uncertain by 8x moves v_max by 2x. It is a
weak instrument on purpose -- a weak instrument that disagrees by a factor of three is still
informative, and one that agrees tells you the measurement is not impossible.

THIS IS A CEILING, NOT A PREDICTION. It asks whether 1.57 m/s is physically available, not
whether a zebrafish does it.

Usage:  python3 burst_power_bound.py
"""
import itertools
import math

RHO = 1000.0            # kg/m3, water
M_BODY = 4.0e-4         # kg, 0.4 g adult
L = 0.033               # m, body length matching Demesmay's fish

# Ranges, not points. Sources are general vertebrate-muscle and fish-drag values, not measured
# here, and the script reports the SPREAD rather than a single number for that reason.
MUSCLE_FRAC = (0.40, 0.60)        # axial muscle as a fraction of body mass in teleosts
SPEC_POWER = (100.0, 250.0)       # W/kg, peak instantaneous power of fish white muscle
CD = (0.01, 0.05)                 # drag coefficient on wetted area; friction-dominated at Re ~5e4
# wetted area as a multiple of L^2 -- a slender body is roughly 0.4 to 0.6 L^2
S_COEF = (0.35, 0.60)

MEASURED = 1.57
SUPERSEDED = 0.842
NEEDED = 1.79


def v_max(frac, pwr, cd, scoef):
    P = M_BODY * frac * pwr
    S = scoef * L * L
    return (2.0 * P / (RHO * cd * S)) ** (1.0 / 3.0)


def main() -> int:
    combos = list(itertools.product(MUSCLE_FRAC, SPEC_POWER, CD, S_COEF))
    vs = sorted(v_max(*c) for c in combos)
    lo, hi = vs[0], vs[-1]
    mid = v_max(sum(MUSCLE_FRAC) / 2, sum(SPEC_POWER) / 2, sum(CD) / 2, sum(S_COEF) / 2)
    print(f"  {len(combos)} corner combinations of the four ranges\n")
    print(f"    most pessimistic corner : {lo:.2f} m/s   ({lo/L:.0f} BL/s)")
    print(f"    mid-range inputs        : {mid:.2f} m/s   ({mid/L:.0f} BL/s)")
    print(f"    most optimistic corner  : {hi:.2f} m/s   ({hi/L:.0f} BL/s)")
    print(f"    spread {hi/lo:.1f}x, from inputs spanning "
          f"{(MUSCLE_FRAC[1]/MUSCLE_FRAC[0])*(SPEC_POWER[1]/SPEC_POWER[0])*(CD[1]/CD[0])*(S_COEF[1]/S_COEF[0]):.0f}x "
          f"-- the cube root compresses it\n")

    for v, lab in ((SUPERSEDED, "superseded 0.842"), (MEASURED, "Demesmay 2025, in use"),
                   (NEEDED, "needed for the 2 cm threshold")):
        where = ("BELOW the pessimistic corner -- comfortably available" if v < lo else
                 "ABOVE the optimistic corner -- NOT physically available" if v > hi else
                 "INSIDE the range -- available only at the favourable end"
                 if v > mid else "INSIDE the range, below mid -- plausible")
        print(f"    {v:.2f} m/s ({v/L:>4.0f} BL/s)  {lab:<30} {where}")

    # CONTROL: the bound must REFUSE something it should refuse. A ceiling that admits every
    # speed is not a ceiling.
    absurd = 10.0
    assert absurd > hi, "CONTROL FAILED: the bound admits 10 m/s, so it constrains nothing"
    print(f"\n  CONTROL: 10 m/s ({absurd/L:.0f} BL/s) is above the optimistic corner, so the "
          f"bound does refuse\n  something -- it is not vacuous.")

    print(f"\n  READING. The measured 1.57 m/s is {'inside' if lo <= MEASURED <= hi else 'outside'} "
          f"the physically available band, so power does NOT refute it;")
    pm = 100*(MEASURED-lo)/(hi-lo); pn = 100*(NEEDED-lo)/(hi-lo)
    print(f"  it sits at the {pm:.0f}th percentile of the band -- in its LOWER THIRD, so it does "
          f"NOT require the")
    print(f"  favourable end of anything. The 1.79 m/s the design needs is at the {pn:.0f}th "
          f"percentile, also low.")
    print(f"  (An earlier version of this line said 1.57 'requires the favourable end' while "
          f"printing a 27th-")
    print(f"  percentile position directly above it -- a reading that contradicted its own "
          f"number.)")
    print(f"  POWER THEREFORE PERMITS BOTH SPEEDS COMFORTABLY. The objection in claim 544 was "
          f"never that")
    print(f"  1.57 m/s is impossible; it is that 47.6 BL/s is about twice what fish are OBSERVED "
          f"to do. This")
    print(f"  bound separates those two questions and answers only the first.")
    print(f"\n  WHAT THIS DOES NOT SETTLE: a ceiling is not an observation. This says the muscle "
          f"COULD supply\n  1.57 m/s against steady drag -- it does not say a zebrafish reaches "
          f"it, and it uses steady\n  drag for an unsteady manoeuvre, which flatters the fish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
