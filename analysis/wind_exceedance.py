#!/usr/bin/env python3
"""S916's climatology half: how often does the Gangetic floodplain see route D's wind?

Claim 1054 established that over vegetated floodplain roughness (z0 = 0.03 m) the 10 m wind
needed to put 12.46 m/s at 1 m is 20.6 m/s -- Beaufort 8. S916 asks in what fraction of daylight
hours that occurs over the zebrafish's native range, and sets the bar at 1%.

THE OBSERVED MEANS ARE AN ORDER OF MAGNITUDE BELOW IT. Reported annual means for Bangladesh and
the Gangetic plain run 1.7-4.2 m/s at station heights, and the single most relevant site --
Rajshahi, inland on the Gangetic floodplain -- measured 3.93 m/s at 40 m over a 55-day summer
campaign. Converted to 10 m at floodplain roughness that is about 3.2 m/s.

SO THE REQUIRED WIND IS 5-10x THE MEAN, and the question is a tail question. This computes the
Rayleigh and Weibull exceedance for a range of means, AND SAYS PLAINLY THAT THE NUMBER IS NOT
TRUSTWORTHY: a Rayleigh tail at 6 sigma is an extrapolation far outside where the fit is
constrained, and real wind distributions in this region have much fatter tails because of
pre-monsoon squall lines (Kalbaisakhi / nor'westers) and cyclones. The honest reading is not the
exponent; it is that S916's falsifier is satisfied by its SECOND clause -- "or occurs only
during cyclones and monsoon squalls" -- which a Beaufort 8 gale on the Gangetic plain does.
"""
from __future__ import annotations

import math

TARGET_U10 = 20.6          # claim 1054: Beaufort 8, over z0 = 0.03 m
#: (mean 10 m wind, what it is). Means are at the stated instrument height unless noted.
MEANS = (
    (1.73, "lowest of five Bangladesh stations (annual)"),
    (3.17, "Rajshahi 40 m 3.93 m/s converted to 10 m at z0 = 0.03 m -- inland floodplain"),
    (4.17, "highest of five Bangladesh stations, Kuakata, coastal (annual)"),
    (5.00, "Bangladesh coastal belt at 30 m -- NOT the habitat, included as an upper bound"),
)


def rayleigh_exceed(u: float, mean: float) -> float:
    """P(U > u) for a Rayleigh distribution (Weibull k=2) with the given mean."""
    return math.exp(-math.pi / 4.0 * (u / mean) ** 2)


def weibull_exceed(u: float, mean: float, k: float) -> float:
    """P(U > u) for a Weibull of shape k whose mean is `mean`."""
    scale = mean / math.gamma(1.0 + 1.0 / k)
    return math.exp(-((u / scale) ** k))


def main() -> int:
    print(f"  route D needs {TARGET_U10} m/s at 10 m (claim 1054, Beaufort 8)\n")
    print(f"  {'mean U10':>9}  {'ratio':>6}  {'Rayleigh':>12}  {'Weibull k=1.5':>14}  source")
    for mean, label in MEANS:
        r = rayleigh_exceed(TARGET_U10, mean)
        w = weibull_exceed(TARGET_U10, mean, 1.5)
        print(f"  {mean:9.2f}  {TARGET_U10/mean:6.2f}  {r:12.2e}  {w:14.2e}  {label}")

    print("\n  Even the fattest tail tried here (k = 1.5, a deliberately generous choice for a")
    print("  monsoon climate) and the coastal upper bound stay far below S916's 1% bar.")

    print("\n  CONTROLS")
    # 1. the formula must reproduce the mean's own exceedance sanity: P(U > mean) for Rayleigh
    #    is exp(-pi/4) = 0.456, a textbook value independent of the mean.
    got = rayleigh_exceed(5.0, 5.0)
    print(f"    P(U > mean) under Rayleigh = {got:.3f}, textbook exp(-pi/4) = "
          f"{math.exp(-math.pi/4):.3f}  {'OK' if abs(got - math.exp(-math.pi/4)) < 1e-9 else 'WRONG'}")
    # 2. a threshold the habitat DOES meet must come back common, or the function only ever
    #    returns small numbers and the result above means nothing.
    easy = rayleigh_exceed(3.0, 3.17)
    print(f"    P(U > 3.0 m/s) at the Rajshahi mean = {easy:.3f} -- a common wind is common "
          f"{'OK' if easy > 0.3 else 'the function returns small numbers regardless'}")
    # 3. monotone in the mean
    xs = [rayleigh_exceed(TARGET_U10, m) for m, _ in MEANS]
    print(f"    exceedance rises with the mean: {all(xs[i] < xs[i+1] for i in range(len(xs)-1))}")

    print("\n  WHAT THIS NUMBER IS NOT. A Rayleigh or Weibull tail evaluated 5-10 mean-multiples")
    print("  out is an extrapolation far outside where any fit is constrained, and this region's")
    print("  real distribution has a much fatter tail: pre-monsoon squall lines (Kalbaisakhi)")
    print("  and cyclones produce gales that no smooth fit predicts. The exponent should not be")
    print("  quoted. What the data support is the ORDER: the required wind is 5-10x the local")
    print("  mean, so it is a storm, not a windy afternoon.")
    print("\n  S916's falsifier reads: non-viable if the wind occurs in fewer than 1% of daylight")
    print("  hours, OR OCCURS ONLY DURING CYCLONES AND MONSOON SQUALLS. The second clause is")
    print("  satisfied on the observed means alone, without relying on the tail arithmetic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
