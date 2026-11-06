#!/usr/bin/env python3
"""Can an ORDINARY zebrafish clear the weak threshold without shrinking it? The drag decides.

Claim 575 found the 2 cm lift-attributable threshold crossed at a body length of 2.13 cm and
ruled it "not a result", because 2.13 cm is below every size range the supporting speed was
measured on. That judgement stands -- for the SIZE route.

THIS IS A DIFFERENT ROUTE TO THE SAME THRESHOLD and it needs no extrapolation at all: hold the
body at the measured size and ask what EXIT SPEED the achievable 2.65x fin needs. The project's
own feasible_region.py answers that at CD 0.10 -- 1.79 m/s -- and the two things it does not do
are what this adds: it does not say what fraction of real fish reach that speed, and it uses a
drag coefficient claim 565 showed to be BELOW the physical floor.

THE DISPERSION IS A STANDARD DEVIATION, which decides whether the upper tail contains animals.
Claim 443 records Demesmay et al. 2025 at "157 +/- 27 cm/s for controls" without saying what the
+/- is. Read from the paper's own methods: "Graphs represent mean +/- SD with individual values",
minimum 11 fish per genotype. So it is variation BETWEEN INDIVIDUALS.

THE CONTROL IS NOT DECORATION HERE. Two earlier attempts at this calculation failed it, at 1.22
and 1.51 cm against feasible_region's 1.79, because they subtracted the ballistic trajectory at
the SAME launch angle as the winged one. feasible_region compares each at ITS OWN best angle,
which is the conservative and correct definition of "does a wing beat no wing", and reading its
source rather than guessing its inputs is what fixed the reproduction. This script aborts if it
cannot reproduce 1.79.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s901_ballistic_leap import fly  # noqa: E402

PRESENT_AREA_CM2 = 1.4
AREA_CM2 = PRESENT_AREA_CM2 * 2.65      #: present silhouette x the best measured fin ratio (claims 529, 542)
CL = 1.07                  #: measured maximum at this Reynolds number (claim 579)
THRESHOLD_CM = 2.0         #: S901's falsifier
MEAN_V, SD_V = 1.57, 0.27  #: Demesmay et al. 2025, mean +/- SD across individuals, n >= 11
#: claim 565: CL 1.07 on a fish fin implies this total CD once induced drag is counted.
DRAG_FLOOR = (0.165, 0.377)

#: (allele, area ratio, aspect ratio, CD) -- claim 567, computed from MEASURED fin spans and
#: areas rather than from a generic range. This is what makes the per-allele table below
#: possible: the drag coefficient is not an unknown to be swept, it is a property of each
#: published allele's own shape. A fin that elongates without widening raises its aspect ratio
#: and cuts its own induced drag, which is why the area ranking and the aerodynamic ranking
#: disagree.
ALLELES = (("wild type", 1.00, 1.50, 0.316),
           ("alf",       2.65, 1.66, 0.289),
           ("longfin",   2.65, 2.45, 0.205),
           ("schleier",  1.54, 3.30, 0.160))


def attrib(v: float, cd: float) -> float:
    """Lift-attributable distance in cm: best winged range minus best BALLISTIC range.

    Each maximised over launch angle independently -- see the module docstring.
    """
    bal = max(fly(0.0, 0.0, 0.0, v0=v, ang=math.radians(d))[0] for d in range(5, 66, 5))
    win = max(fly(AREA_CM2 * 1e-4, CL, cd, v0=v, ang=math.radians(d))[0]
              for d in range(5, 66, 5))
    return (win - bal) * 100


def crossing_for(area_cm2: float, cd: float, hi: float = 6.0) -> float | None:
    """crossing() for an arbitrary area; see crossing() for the bracket caveat."""
    lo = 1.0
    if attrib_for(area_cm2, hi, cd) < THRESHOLD_CM:
        return None
    for _ in range(45):
        mid = (lo + hi) / 2
        if attrib_for(area_cm2, mid, cd) >= THRESHOLD_CM:
            hi = mid
        else:
            lo = mid
    return hi


def attrib_for(area_cm2: float, v: float, cd: float) -> float:
    bal = max(fly(0.0, 0.0, 0.0, v0=v, ang=math.radians(d))[0] for d in range(5, 66, 5))
    win = max(fly(area_cm2 * 1e-4, CL, cd, v0=v, ang=math.radians(d))[0]
              for d in range(5, 66, 5))
    return (win - bal) * 100


def crossing(cd: float, hi: float = 6.0) -> float | None:
    """Lowest exit speed clearing the threshold, or None if no speed does.

    The bracket matters: attrib is NOT monotonic in speed. Past roughly 6 m/s the winged body's
    drag penalty overtakes its lift benefit and the lift-attributable distance turns NEGATIVE,
    so a bisection bracketed at 12 m/s silently reports "never clears" for a drag that does.
    """
    lo = 1.0
    if attrib(hi, cd) < THRESHOLD_CM:
        return None
    for _ in range(45):
        mid = (lo + hi) / 2
        if attrib(mid, cd) >= THRESHOLD_CM:
            hi = mid
        else:
            lo = mid
    return hi


def pct_above(v: float) -> float:
    z = (v - MEAN_V) / SD_V
    return 100.0 * (1.0 - 0.5 * (1.0 + math.erf(z / math.sqrt(2))))


def main() -> int:
    print("=" * 94)
    print("THE WEAK THRESHOLD AT THE MEASURED BODY SIZE -- what fraction of ordinary fish clear it?")
    print("=" * 94)
    c0 = crossing(0.10)
    ok = c0 is not None and abs(c0 - 1.79) < 0.02
    print(f"\n  CONTROL -- reproduce feasible_region.py at its own CD 0.10: {c0:.3f} m/s "
          f"against its stated 1.79  ->  {'REPRODUCED' if ok else 'MISMATCH'}")
    if not ok:
        print("  ABORTING: this script does not reproduce the project's own map, so nothing "
              "below is comparable to it.")
        return 2

    print(f"\n  Demesmay controls: mean {MEAN_V} m/s, SD {SD_V} BETWEEN INDIVIDUALS (n >= 11)\n")
    print(f"  {'CD':>7s} {'crossing':>13s} {'x mean':>8s} {'SD above':>9s} {'% of fish':>11s}   note")
    rows = ((0.10, "BELOW the physical floor -- what the map uses"),
            (DRAG_FLOOR[0], "floor: best aspect ratio and Oswald e"),
            (0.25, "mid-range"),
            (DRAG_FLOOR[1], "floor: worst aspect ratio and e"))
    for cd, note in rows:
        v = crossing(cd)
        if v is None:
            print(f"  {cd:>7.3f} {'never clears':>13s} {'-':>8s} {'-':>9s} {'0.0%':>11s}   {note}")
            continue
        print(f"  {cd:>7.3f} {v:>11.2f} m/s {v/MEAN_V:>7.2f}x {(v-MEAN_V)/SD_V:>8.2f} "
              f"{pct_above(v):>10.1f}%   {note}")

    print("\n  PER ALLELE, each with ITS OWN measured area and induced drag (claim 567):\n")
    print(f"  {'allele':<12s} {'area x':>7s} {'AR':>5s} {'CD':>6s} {'crossing':>13s} "
          f"{'SD above':>9s} {'% of fish':>10s}")
    for name, ratio, ar, cd in ALLELES:
        v = crossing_for(PRESENT_AREA_CM2 * ratio, cd)
        if v is None:
            print(f"  {name:<12s} {ratio:>7.2f} {ar:>5.2f} {cd:>6.3f} {'never clears':>13s} "
                  f"{'-':>9s} {'0.0%':>10s}")
        else:
            print(f"  {name:<12s} {ratio:>7.2f} {ar:>5.2f} {cd:>6.3f} {v:>11.2f} m/s "
                  f"{(v-MEAN_V)/SD_V:>8.2f} {pct_above(v):>9.1f}%")
    print("\n    longfin is the best allele here, and that INDEPENDENTLY REPRODUCES claim 567's")
    print("    ranking, which reached it by required-area rather than by integrating a")
    print("    trajectory. Wild type needs 4.7 SD above the mean -- no fish -- so the fin")
    print("    genetics are what move this from 'none' to about one in twelve.")

    print("\n  READING")
    print("    The answer is set by the DRAG COEFFICIENT and not by the fish. At the favourable")
    print("    end of the physically attainable range the weak threshold is met by about one")
    print("    zebrafish in eight, at the measured body size, with the fin genetics already")
    print("    specified and no extrapolation. At the unfavourable end NO exit speed clears it.")
    print("\n    So the cheapest question that would settle the weak threshold is no longer a")
    print("    fast-start velocity at 21 mm. It is the ACTUAL drag coefficient of an enlarged")
    print("    zebrafish pectoral fin at this Reynolds number.")
    print("\n  LIMITS: this is the WEAK threshold (does a wing beat no wing), not flight -- lift")
    print("  >= weight stays 4.3-fold short. The percentages assume the individual distribution")
    print("  is normal; the paper plots individual values and those were not read. Selecting the")
    print("  fastest individuals is SELECTION, not genetic design. And the drag range is claim")
    print("  565's calculation from aspect ratio, not a measurement of this fin -- so the")
    print("  quantity that decides the answer is the one least directly measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
