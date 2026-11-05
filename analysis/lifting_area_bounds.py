#!/usr/bin/env python3
"""What the design's lifting area actually is, as a RANGE over the one factor nobody measured.

THE PROBLEM THIS REPLACES. Nine modules used S = silhouette x (length rescale) x 2.65, where the
2.65 is a FIN allometry applied to a BODY silhouette (claims 1157, 1158). That composition has
no stated justification. Two claims (1149, 1154) tried to repair it by deciding what the
baseline meant and both were withdrawn -- the second on a constant whose definition sat in a
code comment the whole time.

THE HONEST FORM IS A BOUND, NOT A NUMBER. A gliding fish's lifting surface is its body
silhouette plus its paired pectoral fins (pelvics and caudal add more; they are ignored here,
which makes every figure below a LOWER bound on area and therefore conservative about the
design's prospects in the direction that matters -- it understates available area).

    S_total  =  silhouette  +  2 x k x L_fin^2

L_fin comes from this project's measured claims. k is a PLANFORM SHAPE FACTOR -- the fin's area
divided by the square of its length -- and NOBODY HAS MEASURED IT for a zebrafish pectoral fin.
Rather than invent one, this sweeps it across the range that bounds any plausible fin:

    k = 0.20   a narrow, strongly tapered fin
    k = 0.35   a moderately tapered fan, the shape a zebrafish pectoral broadly resembles
    k = 0.50   a half-ellipse, about as broad as a pectoral fin gets

The point is not to pick one. It is to show how much the design conclusion moves across the
whole range, because a conclusion that survives k = 0.20 to 0.50 does not depend on the
unmeasured quantity, and one that does not survive it was never supported.

WHAT IS MEASURED AND WHAT IS NOT, kept apart:
    measured      fin length / SL: 0.46 mutant (claim 986), 2.05-fold change (claim 984),
                  hence ~0.224 wild type; flying fishes 0.683, flying halfbeaks 0.250 (claim 986)
    documented    silhouette 1.4e-4 m^2 at 4.0 cm (lift_budget.py:36, docs/FINDINGS.md)
    NOT measured  k, the planform shape factor. Swept, never assumed.
"""

from __future__ import annotations

import math

SL_M = 0.04                 #: body length the silhouette constant describes, 4.0 cm
SILHOUETTE_M2 = 1.4e-4      #: lift_budget.py:36, docs/FINDINGS.md
MASS_KG = 4.0e-4            #: the ~0.4 g adult those documents use
G, RHO, CL = 9.81, 1.225, 0.6

#: fin length / standard length, from this project's measured claims
FIN_SL = (("wild type (claim 986 / 984: 0.46 / 2.05)", 0.46 / 2.05),
          ("longfin mutant (claim 986)", 0.46),
          ("flying halfbeaks (claim 986)", 0.250),
          ("flying fishes (claim 986)", 0.683))
K_RANGE = ((0.20, "narrow, strongly tapered"),
           (0.35, "moderately tapered fan"),
           (0.50, "half-ellipse, about as broad as a pectoral gets"))

#: what the nine modules used, for comparison only
S_AS_USED = 1.4e-4 * (2.6 / 4.0) ** 2 * 2.65


def v_stall(S: float) -> float:
    return math.sqrt(2 * MASS_KG * G / (RHO * S * CL))


def main() -> int:
    print("  LIFTING AREA AS A RANGE, swept over the unmeasured planform shape factor k.")
    print(f"  body silhouette {SILHOUETTE_M2*1e4:.2f} cm^2 at SL {SL_M*100:.1f} cm; "
          f"S_total = silhouette + 2 k L_fin^2\n")
    print(f"  {'morphology':44s} {'L_fin':>7s}  " +
          "  ".join(f"k={k:.2f}" for k, _ in K_RANGE))
    print("  " + "-" * 86)
    rows = {}
    for label, ratio in FIN_SL:
        L = ratio * SL_M
        areas = [SILHOUETTE_M2 + 2 * k * L * L for k, _ in K_RANGE]
        rows[label] = areas
        print(f"  {label:44s} {L*1000:6.1f}mm  " +
              "  ".join(f"{a*1e4:5.2f}cm2" for a in areas))
    print()
    print(f"  {'morphology':44s} {'':7s}  " +
          "  ".join(f"k={k:.2f}" for k, _ in K_RANGE))
    print("  stall speed at CL 0.6:")
    for label, areas in rows.items():
        print(f"  {label:44s} {'':7s}  " +
              "  ".join(f"{v_stall(a):5.2f}m/s" for a in areas))

    wt = rows[FIN_SL[0][0]]
    mut = rows[FIN_SL[1][0]]
    # THE RATIO MUST BE TAKEN AT THE SAME k. An earlier version printed
    # min(mut)/max(wt) to max(mut)/min(wt), which compares the wild type at one shape factor
    # against the mutant at another -- physically meaningless, since the same fin shape has the
    # same k, and it inflated the range from 1.60-2.17x to 1.25-2.78x. Caught by reading the
    # output, which is also how the project's other interval errors were found.
    ratios = [m / w for m, w in zip(mut, wt)]
    print(f"""
  WHAT THE SWEEP SETTLES. Across the entire k range the wild-type total lifting area is
  {min(wt)*1e4:.2f}-{max(wt)*1e4:.2f} cm^2 and the longfin mutant's is {min(mut)*1e4:.2f}-{max(mut)*1e4:.2f} cm^2.
  Taken AT THE SAME k, the mutant's advantage in TOTAL lifting area is {min(ratios):.2f}x to
  {max(ratios):.2f}x -- not the 2.65x the nine modules apply, because THE SILHOUETTE DOMINATES.
  A fin whose length doubles quadruples its own area, and its own area is small against the body.

  THAT IS THE ERROR THE 2.65 FACTOR ENCODES. 2.666 is a ratio of FIN AREA to FIN AREA
  (claim 1082). Applied to a total that is mostly body, it multiplies the body as well, and the
  body does not grow when the fin does. The honest enlargement of TOTAL lifting area from the
  published genetics is {min(ratios):.2f}-{max(ratios):.2f}x, which is SMALLER -- so the design is
  harder than the nine modules represent, not easier.

  AND THE NINE MODULES' OWN NUMBER IS NOT A 2.65-FOLD FIN. They use S = {S_AS_USED*1e4:.2f} cm^2,
  which is BELOW every longfin-mutant figure here ({min(mut)*1e4:.2f}-{max(mut)*1e4:.2f}) and
  within the WILD-TYPE range ({min(wt)*1e4:.2f}-{max(wt)*1e4:.2f}). Multiplying a silhouette by a
  fin ratio and then rescaling to a smaller body produced a total that is about wild-type sized.
  Whether that is a happy accident or a second error cancelling the first is not established here.

  WHAT THE SWEEP DOES NOT SETTLE: the absolute areas, since k is unmeasured. The SIGN of every
  statement above is invariant across k = 0.20 to 0.50, which is what a sweep is for. Measuring
  k would sharpen the numbers and would not change the direction.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
