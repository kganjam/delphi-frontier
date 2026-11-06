#!/usr/bin/env python3
"""Claim 971's wind threshold is quoted at 1 m; the Beaufort scale is defined at 10 m.

Claim 971 reports that the design sustains flight "in a wind of roughly 12.5 m/s or more AT ONE
METRE", and then calls that "a strong breeze to near-gale, Beaufort 6 to 7 -- ... conditions in
which flying fish are in fact observed to launch". The Beaufort equivalent speed is defined at
10 metres above the surface, so a 1 m value cannot be read off it directly. Converting the
claim's own log-law profile to 10 m moves the threshold two forces up the scale.

The simulation is NOT affected: it used 1 m winds with a log-law profile and did so correctly.
What is wrong is the LABEL and the plausibility argument hanging off it.
"""
from __future__ import annotations

import math

K = 0.41           # von Karman constant
Z0 = 2e-4          # 0.2 mm, the roughness length claim 971 states it assumed

# WMO/NWS Beaufort bands at the 10 m reference, in knots (NWS Miami table), converted here.
KT = 0.514444
BANDS_KT = {0: (0, 0), 1: (1, 3), 2: (4, 6), 3: (7, 10), 4: (11, 16), 5: (17, 21),
            6: (22, 27), 7: (28, 33), 8: (34, 40), 9: (41, 47), 10: (48, 55),
            11: (56, 63), 12: (64, 999)}
# Claim 971's own sampled friction velocities and the 1 m speeds it printed for them.
CLAIM_971 = ((0.15, 3.1), (0.25, 5.2), (0.40, 8.3), (0.60, 12.5), (0.90, 18.7))


def u(ustar: float, z: float) -> float:
    """Log-law wind speed at height z."""
    return (ustar / K) * math.log(z / Z0)


def beaufort_from_band(v_ms: float) -> int | None:
    """Beaufort force for a 10 m wind, by the NWS knot bands.

    ROUND TO KNOTS FIRST. The published bands are contiguous IN KNOTS (…40, 41…) but their
    m/s images are not: force 8 ends at 20.58 m/s and force 9 begins at 21.09, so a speed of
    20.6 m/s fell in a gap and this returned None -- which reads as a missing band rather than
    as a unit-conversion artifact. Rounding to the nearest knot restores contiguity.
    """
    kt = round(v_ms / KT)
    for b, (lo, hi) in BANDS_KT.items():
        if lo <= kt <= hi:
            return b
    return None


def beaufort_from_formula(v_ms: float) -> float:
    """WMO empirical relation v = 0.836 * B**1.5, v being the speed at 10 m."""
    return (v_ms / 0.836) ** (2.0 / 3.0)


def main() -> int:
    print("  POSITIVE CONTROL -- the profile must reproduce claim 971's own printed 1 m speeds,")
    print("  or this script is modelling something else.")
    worst = 0.0
    for ustar, said in CLAIM_971:
        got = u(ustar, 1.0)
        worst = max(worst, abs(got - said))
        print(f"    u* {ustar:4.2f}   claim {said:5.1f} m/s   recomputed {got:6.2f} m/s")
    print(f"    worst disagreement {worst:.3f} m/s -> {'MATCH' if worst < 0.15 else 'DIFFERS'}")

    print(f"\n  The profile is self-similar, so U(10)/U(1) = {u(1, 10)/u(1, 1):.4f} at every u*.")
    print("\n   u*    U(1 m)   U(10 m)    Beaufort by band   by WMO formula")
    for ustar in (0.40, 0.60, 0.90):
        u1, u10 = u(ustar, 1.0), u(ustar, 10.0)
        print(f"   {ustar:4.2f}  {u1:6.2f}   {u10:7.2f}        {str(beaufort_from_band(u10)):>5}"
              f"            {beaufort_from_formula(u10):6.2f}")

    print("\n  THE ERROR'S DIRECTION: reading the 1 m value straight off the scale")
    for ustar, said in ((0.60, 12.5), (0.90, 18.7)):
        print(f"    {said} m/s looked up as if at 10 m -> Beaufort {beaufort_from_band(said)}; "
              f"it is at 1 m, so the true 10 m wind is {u(ustar, 10.0):.1f} m/s "
              f"-> Beaufort {beaufort_from_band(u(ustar, 10.0))}")

    print("\n  NEGATIVE CONTROL -- a speed far outside every band must return None: "
          f"{beaufort_from_band(500.0)}")
    print("  NEGATIVE CONTROL -- U must RISE with height, not fall: "
          f"{u(0.6, 10) > u(0.6, 1)}")
    return 0




# ---------------------------------------------------------------------------
# S916's roughness point, which changes the answer more than the height did.
# ---------------------------------------------------------------------------

#: Roughness lengths in metres. The open-water value is what claim 971 assumed; the others are
#: the standard Davenport/WMO classes for the terrain a floodplain pond actually sits in.
Z0_CLASSES = (
    (2e-4, "open water, claim 971's assumption"),
    (1e-3, "mud flats, no vegetation"),
    (8e-3, "open flat terrain, short grass"),
    (3e-2, "low crops, occasional obstacles -- S916's floor for vegetated floodplain"),
    (1e-1, "high crops, scattered obstacles"),
    (2.5e-1, "parkland, bushes, numerous obstacles"),
)


def u_at(u10: float, z: float, z0: float) -> float:
    """Wind at height z, given the 10 m wind, under a log profile of roughness z0."""
    return u10 * math.log(z / z0) / math.log(10.0 / z0)


def roughness_table() -> int:
    """How much 10 m wind is needed to put 12.5 m/s at 1 m, as the surface gets rougher?

    THE RATIO U(1)/U(10) FALLS WITH ROUGHNESS, which is the opposite of the intuition that a
    rough surface 'slows the wind' uniformly: it steepens the profile, so the same 10 m wind
    leaves LESS at 1 m. Claim 971 assumed open water. A pond ringed by crops and scrub is two
    to three Davenport classes rougher, and the required 10 m wind rises accordingly.
    """
    need_1m = 12.46            # claim 971's threshold at 1 m, recomputed in main()
    print("\n  S916: THE ROUGHNESS THE PROFILE ASSUMES")
    print(f"  {'z0 (m)':>8}  {'U(1)/U(10)':>10}  {'U10 needed':>11}  {'Beaufort':>8}  terrain")
    for z0, label in Z0_CLASSES:
        ratio = math.log(1.0 / z0) / math.log(10.0 / z0)
        need = need_1m / ratio
        b = beaufort_from_band(need)
        print(f"  {z0:8.4f}  {ratio:10.3f}  {need:9.1f}    {str(b):>8}  {label}")
    print("\n  Claim 1044 corrected the threshold from Beaufort 6 to 7 by fixing the REFERENCE")
    print("  HEIGHT. Fixing the ROUGHNESS moves it further, and in the same direction.")
    print("  CONTROL: at z0 = 0.2 mm the ratio must reproduce claim 1044's 1/1.2703 = 0.787 --")
    print(f"  computed {math.log(1/2e-4)/math.log(10/2e-4):.3f}")
    print("  CONTROL: the ratio must FALL as z0 rises (a rougher surface steepens the profile) --")
    rs = [math.log(1/z0)/math.log(10/z0) for z0, _ in Z0_CLASSES]
    print(f"  monotone decreasing: {all(rs[i] > rs[i+1] for i in range(len(rs)-1))}")
    print("  NOTE: this answers only S916's CONVERSION. The climatology half -- how often such")
    print("  a wind occurs over a Ganges-Brahmaputra floodplain pond -- is NOT answered here.")
    return 0


if __name__ == "__main__":
    main()
    raise SystemExit(roughness_table())
