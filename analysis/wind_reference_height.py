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
BANDS_KT = {4: (11, 16), 5: (17, 21), 6: (22, 27), 7: (28, 33), 8: (34, 40), 9: (41, 47),
            10: (48, 55), 11: (56, 63)}
# Claim 971's own sampled friction velocities and the 1 m speeds it printed for them.
CLAIM_971 = ((0.15, 3.1), (0.25, 5.2), (0.40, 8.3), (0.60, 12.5), (0.90, 18.7))


def u(ustar: float, z: float) -> float:
    """Log-law wind speed at height z."""
    return (ustar / K) * math.log(z / Z0)


def beaufort_from_band(v_ms: float) -> int | None:
    for b, (lo, hi) in BANDS_KT.items():
        if lo * KT <= v_ms <= hi * KT:
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


if __name__ == "__main__":
    raise SystemExit(main())
