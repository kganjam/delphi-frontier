#!/usr/bin/env python3
"""Measure S904's exponent n -- does alf fin AREA scale as length^2, or less?

WHY IT MATTERS. Claim 528 established that the alf (kcnk5b gain-of-function) pectoral fin is
1.74x wild type in LINEAR proportion. The aerodynamic requirement in claim 523 is in AREA:
4.4x for S901's 2 cm threshold, 17.4x for lift to equal weight. Converting between them needs
area = linear^n, and n was unmeasured -- claim 505 records the same exponent spanning 370x on
the coupled stiffness side. At n=1 alf gives 1.74x area and at n=2 it gives 3.03x, which is the
difference between hopeless and nearly sufficient.

HOW. Daane 2018 Fig 1B photographs wt, wt+FK506, sof+FK506 and alf+FK506 from above with the
pectoral fins spread. Fin LENGTH (base to longest ray tip) and SPAN (anterior tip to posterior
tip across the fan) were read from the pixels by two vision models, three reads each.

THREE THINGS MAKE THIS A MEASUREMENT RATHER THAN A GUESS, and the second was a real error caught
only by doing the third:

1. THE ABSOLUTE SPAN IS NOT MEASURABLE AND THE RATIO IS. The two models disagreed on absolute
   span by 60% (wt 123 px against 197 px) while agreeing on the alf/wt span RATIO to 0.5%
   (1.592 against 1.585). Each model places the fan edge differently but places it the same way
   in both fish, so the bias cancels in the ratio. Length, by contrast, agreed to 4% absolute.

2. EACH SUB-PANEL HAS ITS OWN MAGNIFICATION. The first pass compared raw pixels across panels,
   which is only valid if the scales match. They do not exactly: the 2 mm bars measure 83, 76
   and 85 px in the wt, wt+FK506 and alf+FK506 panels. Bars are detected here by image
   processing -- the longest run of dark pixels in each panel's corner -- not by asking a model.

3. THE DRUG IS A CONFOUND AND IT IS CONTROLLED. Comparing "wt" with "alf + FK506" conflates
   genotype with treatment. Fig 1B also has wt + FK506, so the comparison is repeated with the
   drug held constant.

Usage:  python3 fin_shape_exponent.py
"""
import math

# scale bars, px per 2 mm, detected from panelB by longest-dark-run (see module docstring)
BAR = {"wt": 83, "wt_fk506": 76, "alf_fk506": 85}

# raw pixel ratios alf/wt, mean over reads; (model -> (length_ratio, span_ratio))
NO_DRUG_CONTROL = {"claude-opus-5-5": (406.33 / 231.33, 195.33 / 122.67),
                   "claude-sonnet-5-5": (389.67 / 224.00, 311.67 / 196.67)}
DRUG_CONTROLLED = {"claude-opus-5-5": (409.00 / 223.00, 177.50 / 123.00),
                   "claude-sonnet-5-5": (380.00 / 196.50, 361.50 / 177.50)}

NEEDS = (("S901 2 cm threshold", 4.4), ("lift = weight", 17.4))


def main() -> int:
    mag_nodrug = BAR["alf_fk506"] / BAR["wt"]
    mag_drug = BAR["alf_fk506"] / BAR["wt_fk506"]
    print(f"magnification alf/wt       {mag_nodrug:.3f}   (2mm = {BAR['wt']} vs "
          f"{BAR['alf_fk506']} px)")
    print(f"magnification alf/wt+FK506 {mag_drug:.3f}   (2mm = {BAR['wt_fk506']} vs "
          f"{BAR['alf_fk506']} px)\n")

    print(f"{'comparison':<22} {'model':<20} {'length':>8} {'span':>8}  (scale-corrected)")
    lens, spans = [], []
    for label, data, mag in (("wt vs alf", NO_DRUG_CONTROL, mag_nodrug),
                             ("both on FK506", DRUG_CONTROLLED, mag_drug)):
        for m, (lr, sr) in data.items():
            print(f"{label:<22} {m:<20} {lr/mag:>8.3f} {sr/mag:>8.3f}")
            if label == "wt vs alf":
                lens.append(lr / mag)
                spans.append(sr / mag)
        print()

    # CROSS-MODEL AGREEMENT GATE. Span is only usable where the two models agree on the ratio.
    # In the drug-controlled pair they do not (the wt+FK506 photograph is much darker), so that
    # pair contributes its LENGTH only. Saying so is the point; silently averaging would hide it.
    d_lo, d_hi = (DRUG_CONTROLLED["claude-opus-5-5"][1] / mag_drug,
                  DRUG_CONTROLLED["claude-sonnet-5-5"][1] / mag_drug)
    disagree = abs(d_hi - d_lo) / ((d_hi + d_lo) / 2)
    print(f"span cross-model disagreement, drug-controlled pair: {disagree*100:.0f}% "
          f"({d_lo:.2f} vs {d_hi:.2f})")
    print("  -> that pair's SPAN is discarded; its LENGTH is kept. The wt+FK506 photograph is")
    print("     much darker and the fan edge is not findable in it.\n")

    L = sum(lens) / len(lens)
    S = sum(spans) / len(spans)
    area = L * S
    n = math.log(area) / math.log(L)
    drug_len = sum(lr / mag_drug for lr, _ in DRUG_CONTROLLED.values()) / 2
    print(f"LINEAR ratio alf/wt           {L:.2f}   (drug-controlled: {drug_len:.2f}; "
          f"plot-axis route in claim 528: 1.74)")
    print(f"SPAN ratio alf/wt             {S:.2f}")
    print(f"AREA ratio alf/wt             {area:.2f}")
    print(f"EXPONENT n (area = linear^n)  {n:.2f}   <- S904's open exponent, for the lift side")
    print("  n is BELOW 2, so the fin lengthens faster than it widens and the isometric")
    print(f"  assumption would have given {L**2:.2f}x area against the measured {area:.2f}x, "
          f"an OVERSTATEMENT of {(L**2/area - 1)*100:.0f}%.\n")

    for name, need in NEEDS:
        print(f"  {name:<22} needs {need:>5.1f}x area -> alf is {need/area:.2f}x short")

    # CONTROL: the three independent routes to the linear ratio must agree. If the pixel route
    # disagreed with the plot-axis route, the pixel method would be wrong and nothing here
    # would stand, since the area result is the pixel method extended.
    assert abs(L - 1.74) / 1.74 < 0.10, f"pixel linear ratio {L:.2f} disagrees with 1.74"
    assert abs(drug_len - 1.74) / 1.74 < 0.10, f"drug-controlled {drug_len:.2f} disagrees"
    print(f"\nCONTROL ok: pixel route {L:.2f} and drug-controlled route {drug_len:.2f} both "
          "agree with the\n  plot-axis route 1.74 from a DIFFERENT figure, within 10%. The "
          "drug-controlled value\n  matching means FK506 is not producing the difference -- "
          "the genotype is.")
    print("\nSCOPE: one fish per genotype, so there is NO biological replication here. The")
    print("agreement measured above is between READERS of the same photographs, not between")
    print("animals. n = %.2f is a shape statement about these individuals." % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
