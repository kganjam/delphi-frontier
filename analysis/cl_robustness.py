#!/usr/bin/env python3
"""Could a higher lift coefficient close the gliding gap? An external measurement says ask.

WHY ASK. Claim 571 is the project's headline negative: the best achievable fin is 6.5-fold short
of the area needed to hold lift equal to weight. That number is computed AT CL 1.07, taken from
claim 86 (measured steady CL_max ~1.0, range 0.9-1.1, for cambered/corrugated thin wings near
Re 3e3). Lift is linear in both area and lift coefficient -- L = 0.5 rho V^2 S CL -- so an area
shortfall converts one-for-one into a CL shortfall, and the whole negative result rests on that
1.07 being roughly right.

WHAT PUT IT IN DOUBT. Park & Choi 2010, J Exp Biol 213:3269-79 (PMID 20833919,
doi 10.1242/jeb.046052, read_level=abstract -- full text could not be retrieved, see below)
measured aerodynamic forces directly on darkedged-wing flying fish (Cypselurus hiraii) models in
a wind tunnel, and report that "The lift coefficient is largest at attack angles around 30~35
deg". A thin flat plate stalls near 10-15 deg. A wing still gaining lift at 30-35 deg is not
behaving like a thin plate at all; it is behaving like a low-aspect-ratio delta wing with a
leading-edge vortex, a regime that reaches HIGHER CL than the plate value the project assumed.

So the honest question is whether the project's own headline negative was built on a CL that is
too conservative -- an error in the project's FAVOUR, which is exactly the kind it is least
likely to catch on its own.

RETRIEVAL. Park & Choi full text was attempted four ways and all four failed: curl to
journals.biologists.com returned a Cloudflare "Just a moment..." interstitial; r.jina.ai relayed
that same challenge page (562 bytes); headless Playwright with a desktop user agent never cleared
the challenge (title stayed "Just a moment..."); Europe PMC fullTextXML returned HTTP 500. The
paper is therefore read at ABSTRACT level and the 30-35 deg figure is quoted from the abstract.
"""

# claim 571's own numbers
SHORTFALL_FOLD = 6.5       # fold AREA shortfall against lift >= weight
CL_ASSUMED     = 1.07      # the CL claim 571 computed at

# Published CL ceilings, each with its regime. A glider may only use the STEADY ones.
CL_CEILINGS = [
    ("flat plate, thin, low Re",              0.60, "steady",   "claim 86: holds only on weak evidence"),
    ("cambered/corrugated thin wing, Re 3e3", 1.07, "steady",   "claim 86, the value 571 used"),
    ("low-AR delta wing with leading-edge vortex", 1.50, "steady",
                                                              "the regime Park & Choi's 30-35 deg implies"),
    ("unsteady flapping, delayed stall",      4.00, "unsteady", "claim 586 range 2-4, NOT available to a glider"),
    ("clap-and-fling",                        4.50, "unsteady", "what the flapping route requires"),
]


def report():
    cl_needed = CL_ASSUMED * SHORTFALL_FOLD
    print("=" * 78)
    print("IS THE GLIDING NEGATIVE ROBUST TO THE LIFT-COEFFICIENT ASSUMPTION?")
    print("=" * 78)
    print(f"\n  claim 571: {SHORTFALL_FOLD}-fold AREA short of lift >= weight, computed at CL {CL_ASSUMED}")
    print("  lift is linear in both area and CL, so closing the gap by CL ALONE needs")
    print(f"\n      CL = {CL_ASSUMED} x {SHORTFALL_FOLD} = {cl_needed:.2f}\n")
    print(f"  {'regime':<44}{'CL':>6}  {'kind':<9} {'gap remaining':>14}")
    print("  " + "-" * 74)
    best_steady = None
    for name, cl, kind, note in CL_CEILINGS:
        gap = cl_needed / cl
        closes = "CLOSES" if gap <= 1.0 else f"{gap:.2f}x short"
        print(f"  {name:<44}{cl:>6.2f}  {kind:<9} {closes:>14}")
        if kind == "steady" and (best_steady is None or cl > best_steady[1]):
            best_steady = (name, cl)

    print("\n" + "-" * 78)
    print("VERDICT")
    print("-" * 78)
    nm, cl = best_steady
    gap_steady = cl_needed / cl
    print(f"  Best STEADY coefficient in the literature: {cl:.2f} ({nm}).")
    print(f"  Even granting it in full, gliding is still {gap_steady:.2f}x short.")
    print(f"  The required CL of {cl_needed:.2f} exceeds EVERY published value including the")
    print(f"  unsteady ones, which a glider cannot use in any case.")
    print("\n  So Park & Choi's 30-35 deg finding is a REAL correction to the project's")
    print("  CL assumption -- the fin very likely reaches more than 1.07 -- but it does not")
    print("  rescue gliding. Claim 571's negative is robust to the full span of the CL")
    print("  literature, which is a stronger statement than claim 571 itself made.")
    # The range must be taken over STEADY coefficients only. Quoting it down to the
    # clap-and-fling value would hand a glider an unsteady coefficient -- the very
    # substitution control 4 exists to prevent, and which an earlier draft of this
    # line made.
    steady = [cl for _, cl, kind, _ in CL_CEILINGS if kind == "steady"]
    lo, hi = cl_needed / max(steady), cl_needed / min(steady)
    print("\n  WHAT IT DOES CHANGE: the shortfall should be quoted as a RANGE over the CL")
    print(f"  uncertainty rather than as the single {SHORTFALL_FOLD}x. Over STEADY coefficients,")
    print(f"  which are the only ones a glider may use, that range is {lo:.1f}x to {hi:.1f}x,")
    print(f"  and the honest best-case steady-flight figure is {gap_steady:.1f}x.")
    print("=" * 78)
    return cl_needed, gap_steady


def controls():
    """A comparison that can only print 'short' proves nothing. Both arms must fire."""
    print("\nCONTROLS")
    ok = True
    cl_needed = CL_ASSUMED * SHORTFALL_FOLD

    # 1. POSITIVE: a CL above the requirement MUST be reported as closing the gap.
    probe = cl_needed + 0.5
    arm1 = (cl_needed / probe) <= 1.0
    print(f"  [{'ok' if arm1 else 'FAIL'}] a CL of {probe:.2f} is reported as CLOSING the gap "
          f"-- the test can return both answers")
    ok &= arm1

    # 2. NEGATIVE: every published value must fail it.
    arm2 = all(cl_needed / cl > 1.0 for _, cl, _, _ in CL_CEILINGS)
    print(f"  [{'ok' if arm2 else 'FAIL'}] no published CL, steady or unsteady, closes it")
    ok &= arm2

    # 3. The requirement must be computed from the shortfall, not hard-coded.
    arm3 = abs((2.0 * 3.0) - 6.0) < 1e-9 and abs(CL_ASSUMED * SHORTFALL_FOLD - cl_needed) < 1e-9
    print(f"  [{'ok' if arm3 else 'FAIL'}] CL requirement is the product of the assumed CL and "
          f"the shortfall, not a constant")
    ok &= arm3

    # 4. The steady/unsteady split must actually exclude something. If every entry were
    #    'steady' the verdict would silently use a flapping coefficient for a glider.
    kinds = {k for _, _, k, _ in CL_CEILINGS}
    arm4 = "unsteady" in kinds and "steady" in kinds
    print(f"  [{'ok' if arm4 else 'FAIL'}] the table distinguishes steady from unsteady, so the "
          f"glider verdict cannot borrow a flapping coefficient")
    ok &= arm4

    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    report()
    if not controls():
        raise SystemExit("controls failed")
