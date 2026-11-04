#!/usr/bin/env python3
"""Does enlarging the fin to meet the LIFT requirement make the STIFFNESS requirement worse?

The project holds two shortfalls and has treated them separately: the fin needs about 4.37x linear
enlargement to generate the lift (claim 491), and at measured rigidity it is already 9-196x too
floppy to carry that lift (claim 199, via S6). Enlargement is not neutral between them -- a longer
ray is a longer cantilever -- so the question is whether solving one worsens the other.

THE ANSWER DEPENDS ENTIRELY ON HOW THE RAY'S SECOND MOMENT SCALES, and that is an assumption, not
a measurement. This script therefore reports the whole family rather than one number, and labels
which member matches the one enlargement phenotype the literature actually describes.

Relative tip deflection for a cantilever under a distributed load w:
    delta/L  proportional to  w * L^3 / (E * I)
The total lift is fixed by body weight, so load per unit span w scales as 1/L. Hence
    delta/L  proportional to  L^2 / I(L)
and everything turns on the exponent n in I proportional to L^n.
"""
from __future__ import annotations

L = 4.37          # linear enlargement needed for lift (claim 491, CL 0.6, 2 m/s)
SHORT_LO, SHORT_HI = 9.0, 196.0     # present rigidity shortfall (claim 199)


def rel_deflection_factor(n: float, scale: float = L) -> float:
    """How relative tip deflection changes when length scales by `scale` and I scales as L**n."""
    return scale ** (2.0 - n)


def main() -> int:
    print(f"  Enlarging linear fin dimension by {L}x to meet the lift requirement.\n")
    print(f"  {'I scaling':>26}  {'n':>4}  {'rel. deflection':>16}  {'new shortfall (9-196x)':>24}")
    cases = [
        ("isometric (thickens fully)", 4.0),
        ("thickness fixed, width ~L",  3.0),
        ("cross-section fixed",        0.0),
        ("length only, I unchanged",   0.0),
        ("partial thickening",         2.0),
    ]
    seen = set()
    for label, n in cases:
        if (label, n) in seen:
            continue
        seen.add((label, n))
        f = rel_deflection_factor(n)
        print(f"  {label:>26}  {n:4.1f}  {f:>15.3f}x  {SHORT_LO*f:>10.1f} - {SHORT_HI*f:<10.1f}")

    print("\n  WHICH ONE APPLIES is the question, and the project cannot answer it:")
    print("    n = 4 (isometric) is the only case where enlargement HELPS, dropping relative")
    print("      deflection by 4.37^-2 = 0.052x and taking the shortfall to 0.5-10x.")
    print("    n = 2 leaves it EXACTLY unchanged -- enlargement is neutral.")
    print("    n < 2 makes it WORSE; at n = 0 the shortfall grows 19x, to 171-3755x.")
    print("\n  THE ONE PHENOTYPE THE LITERATURE DESCRIBES POINTS BELOW ISOMETRY. Koenig et al.")
    print("    2017 (10.1016/j.ydbio.2017.07.024, abstract level) report the long-fin kcnk5b")
    print("    phenotype as 'an extended size of actinotrichia' -- an elongation phenotype. The")
    print("    kcnk5b literature describes ray LENGTHENING, and none of the six papers found")
    print("    states a thickness or second-moment measurement (claims 492, 493).")
    print("    So n is unmeasured, and the sign of the coupling is unknown.")
    print("\n  WHAT IS CERTAIN: the two shortfalls are NOT independent, and the project has been")
    print("    reporting them as if they were. Whether enlargement helps or hurts stiffness spans")
    print("    a factor of 370 across the plausible range of n, which is larger than either")
    print("    shortfall on its own.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
