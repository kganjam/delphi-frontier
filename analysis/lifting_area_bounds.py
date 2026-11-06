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
#: ETA: how much lift a unit of BODY silhouette makes against a unit of FIN. The first version of
#: this module implicitly set it to 1.0 -- treating a thick, rounded, low-aspect-ratio fish body
#: as exactly as lift-effective as a thin fin -- and then declared its conclusion "invariant".
#: The panel objected (claim 1161) and it reverses the result: across eta the ratio spans 1.60x
#: to 4.22x and the 2.65x those nine modules use sits INSIDE that band. Sweeping one unknown
#: proves nothing when a second unswept one dominates.
ETA_RANGE = (1.0, 0.5, 0.25, 0.10, 0.0)

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

    Lw = FIN_SL[0][1] * SL_M
    Lm = FIN_SL[1][1] * SL_M
    print("\n  THE MUTANT / WILD-TYPE ADVANTAGE IN TOTAL LIFTING AREA, swept over BOTH unknowns:")
    print(f"    {'eta':>5}   " + "  ".join(f"k={k:.2f}" for k, _ in K_RANGE))
    lo, hi = float("inf"), 0.0
    for eta in ETA_RANGE:
        cells = []
        for k, _ in K_RANGE:
            w = eta * SILHOUETTE_M2 + 2 * k * Lw * Lw
            m = eta * SILHOUETTE_M2 + 2 * k * Lm * Lm
            r = m / w
            lo, hi = min(lo, r), max(hi, r)
            cells.append(f"{r:6.2f}x")
        print(f"    {eta:5.2f}   " + "  ".join(cells))
    print(f"""
  ACROSS BOTH UNKNOWNS THE ADVANTAGE IS {lo:.2f}x TO {hi:.2f}x, AND THE 2.65x THOSE NINE MODULES
  USE SITS INSIDE THAT BAND. So this project cannot say the factor is wrong. It can say it is
  UNCONSTRAINED: the value implied depends on how lift-effective a fish body is per unit
  silhouette, which nothing here measures, and 2.65x corresponds to roughly eta = 0.3-0.5.

  AT eta = 0 the body contributes nothing and the ratio is the pure fin-area ratio,
  (0.46/0.224)^2 = {(FIN_SL[1][1]/FIN_SL[0][1])**2:.2f}x. At eta = 1 the body is as good a lifting
  surface as the fin, which for a thick, rounded, low-aspect-ratio body is the implausible end.

  WHAT STANDS AND WHAT DOES NOT. The LABELLING problem stands: nine modules multiply a body
  silhouette by a fin-to-fin allometry and three of them call the product "of fin" (claim 1157).
  The NUMERICAL claim that 2.65x overstates the genetics does NOT stand, and an earlier version
  of this module made it by implicitly setting eta = 1 and then calling the result invariant
  across k. Sweeping one unknown while a second unswept one spans the whole answer is not a
  sensitivity analysis; it is an assumption wearing one.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
