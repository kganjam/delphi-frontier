#!/usr/bin/env python3
"""A DNA-to-organism chain with the UNMEASURED coupling carried as a free parameter.

THE PROBLEM THIS WORKS AROUND, honestly. Claim 1087: the chain
    allele -> channel conductance -> membrane potential -> fin growth rate -> fin size -> lift
is complete except at one junction. Claim 308 found ZERO published experiments pairing a
membrane-potential manipulation with a bony fin-ray growth rate, and claim 250 leaves even the
SIGN unresolved -- hyperpolarisation in oocytes, depolarisation in vivo, fibroblast Vm never
measured. Writing a transfer function there would be inventing both a magnitude and a sign, which
rule 2 forbids.

SO THE COUPLING IS NOT WRITTEN. It is LUMPED and INVERTED. The molecular input and the organ
output are each measured independently, so the composite gain between them is constrained by the
endpoints rather than assumed:

    g  =  ln(fin linear fold change)  /  ln(conductance fold change)

A g of 1 means fin size tracks conductance proportionally in log space. This does NOT identify
the intermediate steps and does not claim to -- it is one lumped number standing for a chain of
three, and any mechanism consistent with the endpoints is consistent with it.

WHAT THAT BUYS, and it is the point: the design target is a fin fold change, so the SAME lumped
gain says what conductance change the target implies. If that implied conductance is far outside
what any published allele produces, the route is closed at the molecular scale -- a conclusion
reached WITHOUT knowing the Vmem step, because the unknown is bracketed by two measurements
rather than filled in.

EVERY INPUT IS A MEASURED CLAIM AND IS CITED. Nothing here is a free choice except the explicit
sensitivity range.
"""
from __future__ import annotations

import math

#: (label, value, units, claim, what kind of number it is)
ANCHORS = [
    ("alf conductance change", 2.0, "fold increase in gK",
     "claim 250", "MEASURED in Xenopus oocytes; the in vivo SIGN is disputed"),
    ("kcnh2a lof/+ fin length/SL", 2.09, "fold vs wild type",
     "claim 984", "MEASURED from Daane 2021 Fig 4B by two models with printed-value controls"),
    ("alf linear fin", 1.74, "fold vs wild type",
     "claim 528", "MEASURED"),
    ("S345E fin-to-body ratio", 0.564 / 0.486, "fold vs non-transgenic",
     "claim 1088 / spec_parameter FBR_S345E", "MEASURED, figure read by eye, single reader"),
    ("linear requirement for the 2 cm threshold", 2.10, "fold vs wild type",
     "claim 523", "REQUIREMENT, not a measurement"),
    ("area exponent n", 1.33, "dimensionless",
     "claim 542", "MEASURED LOWER BOUND, posture confound"),
]


def gain(fin_fold: float, cond_fold: float) -> float:
    return math.log(fin_fold) / math.log(cond_fold)


def main() -> int:
    print("  ANCHORS (every one a measured claim, or a stated requirement):")
    for label, val, units, claim, kind in ANCHORS:
        print(f"    {label:38} {val:7.3f} {units:28} {claim:12} {kind[:44]}")

    cond = ANCHORS[0][1]
    req = ANCHORS[4][1]
    n = ANCHORS[5][1]

    print("\n  LUMPED GAIN g = ln(fin fold) / ln(conductance fold), from each measured fin outcome:")
    for label, fin, _, claim, _ in (ANCHORS[1], ANCHORS[2], ANCHORS[3]):
        g = gain(fin, cond)
        implied = math.exp(math.log(req) / g)
        print(f"    {label:38} fin {fin:5.3f}x -> g = {g:5.3f}")
        print(f"        at that g, the {req}x requirement needs conductance {implied:6.3f}x "
              f"({implied/cond:.2f}x what alf delivers)")

    print("\n  WHY THIS IS NOT A PREDICTION. Three separate reasons, each fatal on its own:")
    print("    1. The three fin outcomes are DIFFERENT ALLELES, and claim 542 measured the")
    print("       kcnh2a and kcnk5b families as having DIFFERENT scaling exponents -- so a gain")
    print("       fitted on one does not transfer to another.")
    print("    2. The conductance figure is from XENOPUS OOCYTES and claim 250 records that in")
    print("       vivo readouts show the OPPOSITE SIGN. A gain computed across a sign dispute")
    print("       is arithmetic, not biology.")
    print("    3. Claim 1098: the fin fold change is itself SIZE-dependent (alf k=1.88 vs wild")
    print("       type k=1.29) and BACKGROUND-dependent (~2.05x in +/+, ~3.3x in sof/sof), so")
    print("       'the' fin fold change is not a single number to fit a gain to.")

    print("\n  WHAT THE CHAIN DOES ESTABLISH, which is narrow and real:")
    gs = [gain(a[1], cond) for a in (ANCHORS[1], ANCHORS[2], ANCHORS[3])]
    lo, hi = min(gs), max(gs)
    need_lo = math.exp(math.log(req) / hi)
    need_hi = math.exp(math.log(req) / lo)
    print(f"    Across the three measured alleles the lumped gain spans {lo:.3f} to {hi:.3f}.")
    print(f"    The {req}x linear requirement therefore implies a conductance change between")
    print(f"    {need_lo:.2f}x and {need_hi:.2f}x, against the {cond:.1f}x alf is measured to give.")
    print(f"    Area follows as linear^n: requirement^{n} = {req**n:.2f}x area.")
    print(f"\n    THE {need_hi/need_lo:.0f}-FOLD SPREAD IS THE RESULT, and it must not be read from its")
    print("    favourable end. Fitted on kcnh2a the requirement is ALREADY MET by a known")
    print(f"    allele ({need_lo:.2f}x against alf's {cond:.1f}x). Fitted on S345E it is {need_hi/cond:.0f}x BEYOND")
    print("    anything published. Both fits use measured endpoints and neither is privileged,")
    print("    so the honest statement is that the molecular requirement is UNDETERMINED over")
    print(f"    a factor of {need_hi/need_lo:.0f} -- not that the route is open.")
    print("\n    THAT FACTOR IS THE PRICE OF THE MISSING MEASUREMENT, quantified. It is a")
    print("    better argument for running claim 1087's experiment than any verbal 'blocked':")
    print("    measuring the Vmem-to-growth-rate junction would collapse this spread, and")
    print("    nothing else available will.")
    print("\n  AND THE JUNCTION REMAINS UNMEASURED. This brackets the unknown between two")
    print("  measurements; it does not measure it. Claim 1087 names the experiment that would:")
    print("  bony fin-ray growth rate in um/day against a MEASURED fibroblast membrane potential")
    print("  in the SAME adult animals, under a manipulation that changes potential directly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
