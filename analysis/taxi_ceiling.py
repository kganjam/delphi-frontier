#!/usr/bin/env python3
"""The surface-taxi speed ceiling, and the drag drop on leaving the water.

Two quantities from docs/FINDINGS.md, re-derived.

1. DRAG DROP. Leaving the water replaces water with air around the body, so at equal speed and
   equal drag coefficient the body drag falls by exactly the density ratio. FINDINGS states 816x.

2. TAXI CEILING. Measured foil thrust scales with TAIL speed squared, independent of forward
   speed; body drag scales with forward speed squared. Setting them equal:

       U_max = f * A_pp * sqrt(c6 / C_D(Re))

   Immersed area and body mass cancel. Only tail speed and lobe drag at Reynolds number remain.

   THE TEST, and it is not a tautology. c6 is the one free constant. It is fitted HERE to the
   exocoetid row -- the case FINDINGS says the model reproduces, i.e. the validated one -- and
   then used to PREDICT the zebrafish row. A single constant must serve both, or the two rows of
   that table are not outputs of one model.

    python3 taxi_ceiling.py
"""
import sys

RHO_WATER = 1000.0    # kg/m^3
RHO_AIR = 1.225       # kg/m^3

# docs/FINDINGS.md, the two rows of the U_max table.
# (label, f*A_pp / V_to, lobe C_D low, lobe C_D high, stated U_max/V_to low, high)
ROWS = [
    ("exocoetid, Re ~3e5", 0.09, 0.10, 0.008, 0.012, 1.3, 1.5),
    ("zebrafish,  Re ~1e4", 0.09, 0.10, 0.06, 0.08, 0.58, 0.68),
]


def u_ratio(fa, cd, c6):
    """U_max / V_to for a given f*A_pp/V_to, lobe C_D and the constant c6."""
    return fa * (c6 / cd) ** 0.5


def fit_c6(fa_lo, fa_hi, cd_lo, cd_hi, u_lo, u_hi):
    """Range of c6 consistent with a stated U_max/V_to band."""
    lo = (u_lo / fa_hi) ** 2 * cd_lo
    hi = (u_hi / fa_lo) ** 2 * cd_hi
    return lo, hi


def main():
    ratio = RHO_WATER / RHO_AIR
    print(f"1. DRAG DROP ON LEAVING THE WATER")
    print(f"   rho_water / rho_air = {RHO_WATER:.0f} / {RHO_AIR} = {ratio:.1f}x")
    print(f"   FINDINGS states 816x -> {'agrees' if abs(ratio-816) < 1 else 'DISAGREES'}")
    print(f"   (this is an identity, not a measurement: equal speed, equal C_D, density ratio)\n")

    print("2. TAXI CEILING")
    name, fa_lo, fa_hi, cd_lo, cd_hi, u_lo, u_hi = ROWS[0]
    c6_lo, c6_hi = fit_c6(fa_lo, fa_hi, cd_lo, cd_hi, u_lo, u_hi)
    print(f"   c6 fitted to the VALIDATED row ({name}): {c6_lo:.3f} to {c6_hi:.3f}")

    name2, fa_lo2, fa_hi2, cd_lo2, cd_hi2, u_lo2, u_hi2 = ROWS[1]
    pred_lo = u_ratio(fa_lo2, cd_hi2, c6_lo)
    pred_hi = u_ratio(fa_hi2, cd_lo2, c6_hi)
    print(f"   predicted U_max/V_to for {name2}: {pred_lo:.3f} to {pred_hi:.3f}")
    print(f"   FINDINGS states                      : {u_lo2} to {u_hi2}")

    overlap = not (pred_hi < u_lo2 or pred_lo > u_hi2)
    print(f"   -> {'CONSISTENT: one c6 serves both rows' if overlap else 'INCONSISTENT'}")
    if not overlap:
        print("   The two rows of that table are not outputs of a single model.")
        return 1

    # A TEST MUST REPORT ITS OWN POWER. Propagating the extremes of two input ranges compounds
    # them, so the predicted band is wider than the stated one and will bracket a lot. Saying
    # "consistent" without this ratio would oversell a weak check.
    width_pred = pred_hi - pred_lo
    width_stated = u_hi2 - u_lo2
    print(f"\n   POWER OF THIS TEST: the predicted band is {width_pred:.3f} wide against a stated "
          f"{width_stated:.3f},")
    print(f"   a factor of {width_pred/width_stated:.1f}. It would catch a GROSS inconsistency -- "
          f"a stated")
    print(f"   zebrafish ratio above {pred_hi:.2f} or below {pred_lo:.2f} -- and would not catch a "
          f"subtle one.")

    print("\n   SCOPE: this checks the table's INTERNAL consistency under its own formula. It is")
    print("   not a validation against measurement, and c6 is fitted, not independently known.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
