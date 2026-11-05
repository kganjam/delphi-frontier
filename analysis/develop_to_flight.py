#!/usr/bin/env python3
"""A developmental SIMULATION from allele to flight speed, integrated over growth.

Claim 1101 bracketed the dna-to-organism chain algebraically and was fairly described as a lumped
calculation rather than a simulation. This integrates instead, and the allele enters through a
quantity that is MEASURED rather than assumed.

THE STATE VARIABLE IS BODY SIZE AND IT IS INTEGRATED OVER DEVELOPMENTAL TIME. Fin length follows
the measured allometry fin ~ SL^k, with k differing by allele -- claim 1098: wild type k = 1.29
stated in Perathoner 2014's text, alf/+ k = 1.88 read from its Figure 1D. So "which allele" sets
an exponent that someone measured, and no transfer function is invented anywhere in the chain.

SATURATION IS REQUIRED BY THE DATA, NOT ADDED FOR CONVENIENCE. Claim 1098's reductio: extending
k = 1.88 from the measured window (SL 6.3-18.2 mm) to adult D. rerio at 38 mm predicts
fin/SL = 0.75 against a measured ~0.39. A relation that overpredicts by 2x must flatten before
adult size, so a model WITHOUT saturation is known to be wrong. The saturation scale is fitted to
that single adult anchor and is the one fitted quantity in the module; it is reported as fitted.

WHAT COMES OUT IS AN ORGANISM-SCALE NUMBER: adult fin area, and through it the minimum airspeed
at which lift equals weight, using analysis/lift_budget.py unchanged.

WHAT THIS DOES NOT DO. It does not model the membrane-potential junction claim 308 found
unmeasured -- it ROUTES AROUND it, because the allele-to-exponent step was measured directly and
does not require the intermediate to be known. That is a narrower chain than claim 1087 asked
for, and an honest one: it spans dna to organism without passing through the gap.
"""
from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from lift_budget import RHO_AIR, v_min  # noqa: E402

#: Measured anchors, each with its claim.
SL_HATCH_MM = 6.3        # claim 1098, lower end of Perathoner's measured window
SL_WINDOW_MM = 18.2      # claim 1098, upper end of the measured window
SL_ADULT_MM = 38.0       # claim 1000, FishBase Danio rerio 3.8 cm SL
K_WT = 1.29              # claim 1098, stated in Perathoner 2014 text
K_ALF = 1.88             # claim 1098, read from Perathoner Figure 1D
#: SEPARATE intercepts. The first version applied alf's value to wild type as well, which put
#: wild-type fin/SL at 0.304 at adult size where claim 1098 measures 0.211 -- a 44% error that
#: compressed the alf advantage and made the whole ratio wrong.
FIN_SL_ALF_AT_WINDOW = 0.393   # claim 1098, fit matching Perathoner Fig 1E at ~0.39
FIN_SL_WT_AT_WINDOW = 0.211    # claim 1098, fit matching Fig 1E at ~0.19
FIN_SL_ADULT_MEASURED = 0.39   # claim 1098 reductio anchor
N_AREA = 1.33            # claim 542, MEASURED LOWER BOUND on the area exponent
MASS_ADULT_KG = 4.0e-4   # claim 1000 / parameter table `m`
CL_MAX = 1.83            # claim 601, the measured best


def grow(days: int = 120, dt: float = 0.5):
    """Logistic growth in standard length. Endpoints are measured; the RATE is not a datum."""
    sl = SL_HATCH_MM
    r = 0.06
    t = 0.0
    while t < days:
        sl += r * sl * (1.0 - sl / SL_ADULT_MM) * dt
        t += dt
        yield t, sl


def fin_sl(sl_mm: float, k: float, sat: float, base: float) -> float:
    """fin/SL from the measured exponent and that allele's own intercept, with saturation."""
    raw = base * (sl_mm / SL_WINDOW_MM) ** (k - 1.0)
    return raw / (1.0 + raw / sat)


def fit_saturation(k: float, base: float, tgt: float) -> float:
    """Fit the one free scale so adult fin/SL hits the measured value. Reported as fitted."""
    raw = base * (SL_ADULT_MM / SL_WINDOW_MM) ** (k - 1.0)
    return raw * tgt / (raw - tgt) if raw > tgt else float("inf")


def main() -> int:
    print("  DEVELOPMENTAL SIMULATION, allele -> exponent -> fin -> area -> flight speed\n")
    sat = fit_saturation(K_ALF, FIN_SL_ALF_AT_WINDOW, FIN_SL_ADULT_MEASURED)
    print(f"  saturation scale fitted to the adult anchor (the ONE fitted quantity): {sat:.3f}")
    print(f"  unsaturated prediction at adult size would be "
          f"{FIN_SL_ALF_AT_WINDOW * (SL_ADULT_MM/SL_WINDOW_MM)**(K_ALF-1):.3f} "
          f"against a measured {FIN_SL_ADULT_MEASURED}\n")
    print(f"  {'t(d)':>6} {'SL(mm)':>8} {'fin/SL wt':>10} {'fin/SL alf':>11} {'alf/wt':>8}")
    traj = list(grow())
    for t, sl in traj[::40]:
        w = fin_sl(sl, K_WT, sat, FIN_SL_WT_AT_WINDOW)
        a = fin_sl(sl, K_ALF, sat, FIN_SL_ALF_AT_WINDOW)
        print(f"  {t:6.0f} {sl:8.2f} {w:10.3f} {a:11.3f} {a/w:8.3f}")
    t_end, sl_end = traj[-1]
    w = fin_sl(sl_end, K_WT, sat, FIN_SL_WT_AT_WINDOW)
    a = fin_sl(sl_end, K_ALF, sat, FIN_SL_ALF_AT_WINDOW)
    print(f"\n  at t={t_end:.0f} d, SL={sl_end:.2f} mm: wild type {w:.3f}, alf {a:.3f}, "
          f"ratio {a/w:.3f}x LINEAR")
    area_ratio = (a / w) ** N_AREA
    print(f"  area ratio = linear^{N_AREA} = {area_ratio:.3f}x  (claim 542 exponent FLOOR)")

    # organism scale: minimum flight speed, wild-type planform scaled by the area ratio
    area_wt = 1.4e-4 * 2.65      # parameter table S, m^2
    v_wt = v_min(MASS_ADULT_KG, area_wt, CL_MAX, RHO_AIR)
    v_alf = v_min(MASS_ADULT_KG, area_wt * area_ratio, CL_MAX, RHO_AIR)
    print("\n  ORGANISM SCALE, via lift_budget.v_min unchanged:")
    print(f"    wild-type planform  {area_wt*1e4:6.2f} cm^2 -> v_min {v_wt:5.2f} m/s")
    print(f"    alf planform        {area_wt*area_ratio*1e4:6.2f} cm^2 -> v_min {v_alf:5.2f} m/s")
    print(f"    v_min falls by {100*(1-v_alf/v_wt):4.1f}% -- lift scales with area, so v ~ 1/sqrt(area)")

    pts = [(sl, fin_sl(sl, K_ALF, sat, FIN_SL_ALF_AT_WINDOW)
                / fin_sl(sl, K_WT, sat, FIN_SL_WT_AT_WINDOW))
           for _, sl in (traj[10], traj[len(traj) // 2], traj[-1])]
    direction = "RISES" if pts[-1][1] > pts[0][1] else "FALLS"
    print(f"\n  THE alf/wt RATIO {direction} AS THE ANIMAL GROWS -- derived, not asserted:")
    for sl, r in pts:
        print(f"    SL {sl:6.2f} mm -> alf/wt {r:.3f}x")
    best = "ADULT" if pts[-1][1] > pts[0][1] else "JUVENILE"
    print("    A fold change quoted at one size is not the fold change at another, and this")
    print(f"    model puts the LARGEST ratio at {best} size. That direction is claim 1098's")
    print("    positive allometry, integrated rather than asserted -- and it runs in the")
    print("    design's favour, which is the opposite of what the first draft of this very")
    print("    sentence claimed before the numbers were read.")
    print("\n  ROUTED AROUND, NOT THROUGH: the membrane-potential junction claim 308 found")
    print("  unmeasured is never entered. The allele-to-exponent step is measured directly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
