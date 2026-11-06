#!/usr/bin/env python3
"""Turn S904's unmeasurable exponent into a DESIGN SPECIFICATION the project can hold a fin against.

S904 asks for n in I proportional to L^n -- how a fin ray's second moment scales as the ray
lengthens. Claim 505 showed everything turns on it: across n = 0 to 4 the post-enlargement
stiffness shortfall spans a factor of 370, from 0.5x to 3743x. It is the single most valuable
missing number in the structural chain.

IT IS NOT IN THE LITERATURE AND THIS SESSION ESTABLISHED THAT WITH A SCOPED SEARCH.
PubMed counts, with a control: "zebrafish fin regeneration" returns 629, so the search works.
"lepidotrichia" 73, "fin ray stiffness" 33, "fin ray flexural rigidity" 3, "zebrafish
lepidotrichia" 22. The three flexural-rigidity papers are a ribbon-fin propulsion study (2017),
teleost fin-ray functional morphology (2013) and a biorobotic pectoral fin (2010) -- NONE
zebrafish, none comparing a long-fin mutant with wild type. Koenig 2017, the actinotrichia paper,
is not open access. Murciano 2018 is open and measures INTER-RAY soft tissue (275.8 +/- 41.8 um
marginal, 82.4 +/- 6.2 um central), not lepidotrichia cross-section, and is wild-type only, so it
could not give a scaling exponent even if it measured the right structure.

SO THE QUESTION IS INVERTED. Rather than ask what n IS, ask what the design REQUIRES. That is
computable from numbers this project already has, and it yields a falsifiable statement about
ray geometry instead of a blocked literature search.

MODEL, from analysis/rigidity_shortfall.py, which reproduces claim 199 to within 0.6%:
    D_w_required = P L^2 / (8 * CRIT * W)
with P the per-fin load, L the span, W the width, CRIT the tip-deflection criterion.

ASSUMPTIONS, stated because the conclusion is only as good as these:
  - TOTAL LIFT IS FIXED BY BODY WEIGHT. The fish does not get heavier when the fin grows, so P
    is unchanged. This is claim 505's own framing ("load per unit span goes as 1/L").
  - The 10%-of-span deflection criterion is unchanged.
  - The material modulus E is unchanged -- this asks for MORE BONE, not better bone.
  - Ray count is unchanged, which is the biological expectation since ray number is specified
    early and the long-fin phenotype elongates existing rays.
  - I proportional to d^4, a solid cross-section of characteristic width d.

Usage:  python3 ray_stiffness_spec.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rigidity_shortfall import D_W_MEASURED, d_w_required  # noqa: E402

L0 = W0 = 3.0e-3          # the 3 mm square wing claim 199 names
K_LEN = 1.71              # measured alf/wt fin LENGTH ratio (claim 529)
K_SPAN = 1.55             # measured alf/wt fin SPAN ratio (claim 529)


def main() -> int:
    req0 = d_w_required(L0, W0)
    short0 = req0 / D_W_MEASURED
    print(f"  PRESENT FIN (3 mm square, claim 199)")
    print(f"    D_w required {req0:.3e} N m   measured {D_W_MEASURED:.1e} N m   "
          f"shortfall {short0:.1f}x\n")

    L1, W1 = L0 * K_LEN, W0 * K_SPAN
    req1 = d_w_required(L1, W1)
    print(f"  ENLARGED TO THE alf PHENOTYPE (length x{K_LEN}, span x{K_SPAN})")
    print(f"    {L1*1e3:.2f} mm x {W1*1e3:.2f} mm")
    print(f"    D_w required {req1:.3e} N m   -> {req1/req0:.2f}x the present requirement")
    print(f"    requirement scales as L^2 / W = {K_LEN**2:.3f} / {K_SPAN:.2f} = "
          f"{K_LEN**2/K_SPAN:.3f}\n")

    print(f"  IF THE RAYS DO NOT THICKEN (D_w unchanged at the measured value):")
    print(f"    shortfall becomes {req1/D_W_MEASURED:.1f}x, against {short0:.1f}x now")
    print(f"    -> ENLARGEMENT NEARLY DOUBLES THE STIFFNESS PROBLEM unless the ray thickens\n")

    # What ray geometry closes it? D_w = E*I/W per unit width; with ray count fixed, the width a
    # ray must span grows with W, so d^4 must grow by (required D_w ratio) x (width ratio).
    need_dw = req1 / D_W_MEASURED           # factor on per-width rigidity
    need_d4 = need_dw * K_SPAN              # I per ray, since D_w is per unit width
    need_d = need_d4 ** 0.25
    print(f"  THE SPECIFICATION, which is the useful form:")
    print(f"    per-width rigidity must rise {need_dw:.1f}x")
    print(f"    per-RAY second moment must rise {need_d4:.1f}x (count fixed, width x{K_SPAN})")
    print(f"    so ray width d must rise {need_d:.2f}x  while ray LENGTH rises {K_LEN:.2f}x")
    alpha = (need_d ** 0.5) and __import__("math").log(need_d) / __import__("math").log(K_LEN)
    print(f"\n    d proportional to L^{alpha:.2f}")
    print(f"    Isometry is d proportional to L^1. THE DESIGN NEEDS POSITIVE ALLOMETRY:")
    print(f"    the ray must THICKEN FASTER THAN IT LENGTHENS, by a wide margin.")
    n_equiv = 4.0 * alpha
    print(f"\n    in claim 505's units this is n = 4*{alpha:.2f} = {n_equiv:.2f}, ABOVE the n=4")
    print(f"    full-isometric-thickening case that claim 505 found was the only one where")
    print(f"    enlargement helps -- so even isometric thickening does NOT close this.")

    # CONTROL: at n = 4 exactly (d proportional to L), recover claim 505's "enlargement helps" case.
    d_iso = K_LEN                            # isometric thickening
    dw_iso = (d_iso ** 4) / K_SPAN           # per-width rigidity delivered
    print(f"\n  CONTROL -- reproduce claim 505's n=4 case from this model:")
    print(f"    isometric thickening delivers {dw_iso:.2f}x per-width rigidity against the "
          f"{need_dw:.1f}x needed")
    print(f"    residual shortfall {need_dw/dw_iso:.1f}x, versus {short0:.1f}x before enlarging")
    print(f"    -> enlargement WITH isometric thickening {'helps' if need_dw/dw_iso < short0 else 'does not help'}, "
          f"which is claim 505's n=4 finding, recovered here from an independent route")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
