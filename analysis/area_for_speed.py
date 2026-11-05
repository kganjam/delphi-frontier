#!/usr/bin/env python3
"""The blocker is a SPEED. The genetic levers move an AREA. This converts one into the other.

WHY THIS IS THE RIGHT QUESTION NOW. The audited hard blockers reduce to two facts (claim 1148):
adult Danio burst speed is 157 +/- 27 cm/s (Demesmay et al. 2025, five constraints restating it),
and flying-fish take-off is an extended multi-stroke taxi rather than a single release (e53). The
project has been reading the first as "the fish is too slow". But every genetic lever it holds --
kcnk5b, kcnh2a, slc12a7a, lat4a -- changes FIN SIZE, not speed. So the actionable form of the
blocker is not "how do we make it faster" but "how much fin would make the speed it already has
sufficient".

THE PHYSICS IS ONE LINE AND IT IS EXACT AT FIXED LOADING. Stall speed V = sqrt(2W / (rho S C_L)),
so at fixed weight, air density and lift coefficient, V is proportional to 1/sqrt(S). To bring a
required speed V0 down to an attainable speed V1 therefore needs an area ratio of exactly
(V0/V1)^2. No aerodynamic model is being invoked beyond the definition of stall.

WHAT THIS DELIBERATELY DOES NOT DO, and the reason is this project's own history. Claim 988
carries an explicit warning that the 2.65x achieved fin ratio is ALREADY INSIDE the baseline of
analysis/closed_loop.py, so multiplying by it again compounds. That is the same shape as the
myosin double-count the panel refuted (claims 1104 -> 1111 -> 1114): a ratio applied to a baseline
that already contains it. So this module computes the RELATION only and applies it to pairs that
are each labelled with their own source. It does not decide which baseline any published fin
ratio sits on, because this project has not settled that and guessing would reproduce the error
it is guarding against.

ADDING FIN AREA ADDS MASS, which raises W, which raises V again. The relation above holds at
FIXED W and therefore understates the required area. Claim 275 already records that large wings
"weigh 31-211% of the body", so the feedback is not small at the top of this table. Every number
here is a LOWER BOUND on the area needed.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))

from dbq import q  # noqa: E402

PROJECT = "zebrafish-flight"

#: Speeds the project REQUIRES, each with the claim that sets it. Editorial mapping only.
REQUIRED = (
    (1, "stall speed, 1-body-length span wing (AR 5, CL 0.6), 0.4 g fish"),
    (269, "glide speed the taxi must reach, from the taxi-ceiling analysis"),
)
#: Speeds the animal ATTAINS, each with its claim.
ATTAINED = (
    (443, "adult Danio maximal escape speed, measured (Demesmay et al. 2025)"),
    (269, "taxi terminal speed, derived"),
    (2, "adult Danio Ucrit, sustained not burst, literature"),
)
#: The published-genetics fin ratio, for reference only -- NOT multiplied into anything here.
GENETIC_RATIO_CLAIM = 1082


def val(cid: int):
    rows = q(f"select value_num::text, replace(coalesce(units,''), chr(10), ' ') "
             f"from claim where id = {cid} and value_num is not null")
    if not rows or not rows[0][0]:
        return None, ""
    return float(rows[0][0]), rows[0][1]


def main() -> int:
    print("  HOW MUCH FIN WOULD MAKE THE SPEED THE FISH ALREADY HAS SUFFICIENT?")
    print("  area ratio = (required speed / attained speed)^2, exact at fixed weight and CL.\n")

    reqs = [(c, d) + val(c) for c, d in REQUIRED]
    atts = [(c, d) + val(c) for c, d in ATTAINED]
    reqs = [r for r in reqs if r[2] is not None]
    atts = [a for a in atts if a[2] is not None]
    if not reqs or not atts:
        print("  missing a value; nothing to compute.")
        return 1

    for rc, rd, rv, _ru in reqs:
        print(f"  REQUIRED {rv:.2f} m/s  [claim {rc}: {rd}]")
        for ac, ad, av, _au in atts:
            ratio = (rv / av) ** 2
            print(f"     against {av:>5.2f} m/s [claim {ac}]  ->  fin area x {ratio:6.2f}   "
                  f"(speed gap {rv/av:.2f}x)")
        print()

    gv, gu = val(GENETIC_RATIO_CLAIM)
    if gv:
        print(f"  FOR REFERENCE, NOT MULTIPLIED IN: claim {GENETIC_RATIO_CLAIM} derives a fin-area "
              f"ratio of {gv:.3f}")
        print(f"     ({gu[:96]})")
        print(f"  Its speed benefit at fixed loading is a factor of sqrt({gv:.3f}) = "
              f"{gv**0.5:.2f} -- so it turns a required {reqs[0][2]:.2f} m/s into "
              f"{reqs[0][2]/gv**0.5:.2f} m/s.")
        print("  WHETHER THAT RATIO MAY BE APPLIED ON TOP OF A GIVEN MODEL'S BASELINE IS NOT")
        print("  DECIDED HERE. Claim 988 states the 2.65x is ALREADY INSIDE closed_loop.py's S,")
        print("  and compounding it is the shape of the myosin double-count the panel refuted.")

        # THE BASELINE IS NOW RESOLVED, and the answer was neither reading. An earlier
        # version printed two branches -- (A) the requirement is on wild-type area, (B) it
        # already contains the 2.666x ratio -- and said the project had not settled which.
        # Reading the code settled it: closed_loop.py line 26 is
        # S = 1.4e-4 * (2.6/4.0)**2 * 2.65, so 1.4e-4 m^2 is the WILD-TYPE fin at 4.0 cm, and
        # claim 1's "1 body-length span, AR 5" wing on a 0.4 g (4.0 cm) fish is
        # S = b^2/AR = 0.04^2/5 = 3.2e-4 m^2 -- which is 2.29x that wild-type area, not 1.0x
        # and not 2.666x. Reproduction control: that geometry gives 5.78 m/s against claim 1's
        # stated 5.84, so the geometry is read correctly. Claim 1154.
        taxi = next((a[2] for a in atts if a[0] == 269), None)
        S_WT_4CM, S_CLAIM1 = 1.4e-4, 0.04 ** 2 / 5.0
        already = S_CLAIM1 / S_WT_4CM
        if taxi:
            v0 = reqs[0][2]
            further = gv / already
            v_at_best = v0 / further ** 0.5
            print("\n  THE BASELINE, RESOLVED (claim 1154):")
            print(f"    claim 1's requirement already assumes {already:.2f}x wild-type fin area")
            print(f"      (1-BL span, AR 5 -> S = {S_CLAIM1:.3e} m^2, against closed_loop.py's")
            print(f"       wild-type {S_WT_4CM:.3e} m^2 at the same 4.0 cm body length)")
            print(f"    so the published {gv:.3f}x buys only a further {further:.3f}x area = "
                  f"{further**0.5:.3f}x speed")
            print(f"    {v0:.2f} m/s -> {v_at_best:.2f} m/s, against the {taxi:.2f} m/s taxi")
            print(f"    REMAINING: {(v_at_best/taxi)**2:.2f}x more area on top of the genetics,")
            print(f"    about {gv*(v_at_best/taxi)**2:.1f}x WILD-TYPE FIN AREA IN TOTAL.")
            print("    That is worse than either earlier reading, and it is the honest number.")

    print("""
  READING THIS HONESTLY. The right-hand column is a LOWER BOUND, because larger fins carry mass
  and the relation above holds W fixed; claim 275 records large wings at 31-211% of body mass, so
  the feedback dominates at the top of the table. And an area ratio is not a genetic instruction:
  it says what the phenotype must reach, not that any allele or stack of alleles reaches it.

  WHAT IT CHANGES. The blocker has been carried as a speed the fish cannot reach. Stated as area
  it becomes a quantity the project's levers actually move, and it becomes comparable with what
  the published genetics delivers -- which is the comparison the design needs and has never had
  in one place.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
