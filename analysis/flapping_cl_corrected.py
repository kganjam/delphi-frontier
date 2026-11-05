#!/usr/bin/env python3
"""The flapping route's CL 4.5 is refuted by measurement, and the frequency it implied rises.

WHAT WAS ASSUMED. The powered-flapping route derives its beat frequency from the lift
coefficient: a higher CL needs less wing speed, hence a lower frequency. analysis/
flapping_flight.py computes the required mean WING speed (not body speed) as
U = sqrt(2W / (rho CL S)), and flapping_power_budget.py records "F = 53.0 Hz, from claim 586
at clap-and-fling CL". That 53 Hz -- the number claims 587, 588, 592 and 593 are all measured
against -- is the frequency AT CL 4.5.

WHAT THE MEASUREMENTS SAY. Reported by a peer session on 2026-11-04 with verbatim quotes and
read-levels; the two load-bearing ones are full-text reads and are marked as such.

  1. CLAP-AND-FLING IS A PERCENTAGE, NOT A MULTIPLIER. Every measured study reports the
     benefit as augmentation over a single wing, in the band 5-17%, across Re 20 to 8.3e4:
       Phan, Au & Park 2016 (PMID 28083112, full-text, Re ~1.5e4, 6-axis load cell):
         "the clap and flings at both the stroke reversals augmented the average vertical
          force by 16.2% when compared with the force without the clap-and-fling effect"
       Lehmann, Sane & Dickinson 2005 (PMID 16081606, abstract, Re 100-200):
         "the clap-and-fling augmented total lift production by up to 17%"
     So no CL near 4.5 is reachable by this mechanism at any Reynolds number.

  2. THE DELAYED-STALL CEILING IS 1.75, MEASURED AT Re 8071.
       Usherwood & Ellington 2002 (PMID 12000800, FULL-TEXT, revolving model hawkmoth wings):
         "then the maximum lift coefficient CL,max for the 'pooled' data is 1.75, found at
          alpha'=41 deg"
     Our Re is ~3e3, inside the range part II reports the same behaviour over (Re 1100-26000),
     and Lentink & Dickinson 2009 (PMID 19648415, abstract) report that LEV stability "is not
     dependent on Reynolds number, at least over the range most relevant for insect flight
     (100<Re<14,000)".

  3. AND THE LEV REGIME IS GENUINELY AVAILABLE TO A FISH FIN, which is what licenses using
     an insect-wing coefficient here at all. Lentink & Dickinson 2009:
       "We calculated the Rossby number from single-wing aspect ratios of over 300 insects,
        birds, bats, autorotating seeds, and pectoral fins of fish. We found that, on average,
        wings and fins have a Rossby number close to that of flies (Ro=3)."
     A fish pectoral fin is already in the geometric regime that sustains a stable LEV. That is
     a positive, grounded finding and it is why CL 1.75 is used below rather than a plate value.

  4. A FIN CAN CLAP -- AGAINST THE BODY, not against its contralateral partner.
       Karakas, D'Oliveira, Maas & Murphy 2018 (PMID 30348646, abstract), on the atlantiid
       heteropod Atlanta selvagensis: "use of the clap and fling mechanism twice during each
       stroke cycle". A single fin claps against a rigid shell.
     So the 17% bonus is not geometrically forbidden to our design, and is applied below.

  NOT USED, and why: a relayed search-summary attributing "lift coefficients of roughly 4 to 6"
  to Weis-Fogh 1973 could not be verified, and Weis-Fogh's Encarsia figures are a REQUIRED CL
  inferred from weight support at Re 10-20, not a measured force coefficient. Maxworthy 1979,
  the primary fling experiments, is could-not-access and is the largest gap behind this.

WHAT CHANGES. Frequency scales as 1/U_tip and U scales as 1/sqrt(CL), so f ~ 1/sqrt(CL).
Lowering CL from 4.5 to the measured ceiling RAISES the required frequency.
"""
import math

RHO, G = 1.225, 9.81
from geometry import MASS_KG as _M, S_LIFTING_M2 as _S  # noqa: E402  one definition; see analysis/geometry.py
M = _M                  # was: 4.0e-4 * (2.6/4.0)**3, re-typed alongside it
S = _S                  # was: 1.4e-4 * (2.6/4.0)**2 * 2.65, re-typed in 9 files
R = 0.013                           # m, wing (fin) length
PHI_MID = 2.3                       # rad, mid of the 115-150 deg stroke amplitude range

WHITE_MUSCLE_HZ = 12.0              # claim 593, Young & Rome 2001, measured

CASES = [
    ("clap-and-fling, as assumed", 4.50, "ASSUMED -- refuted by the 5-17% measurements"),
    ("delayed stall, measured ceiling", 1.75, "Usherwood & Ellington 2002, full-text, Re 8071"),
    ("best MEASURED two-wing value", 1.83,
     "Lehmann & Pick 2007 Table 1 pattern I, full-text, cycle-averaged, Re 134"),
    ("cambered thin wing (claim 86)", 1.07, "the value the gliding analysis uses"),
]


def freq_for(cl):
    W = M * G
    u = math.sqrt(2.0 * W / (RHO * cl * S))      # mean WING speed, not body speed
    return (2.0 * u) / (2.0 * PHI_MID * R), u    # tip speed / (2 phi R)


def main():
    print("=" * 78)
    print("REQUIRED BEAT FREQUENCY vs LIFT COEFFICIENT")
    print("=" * 78)
    print(f"  design: {M*1e3:.3f} g, {S*1e4:.2f} cm2 fin, wing length {R*100:.1f} cm, "
          f"stroke {math.degrees(PHI_MID):.0f} deg\n")
    print(f"  {'case':<34}{'CL':>6}{'U_wing':>9}{'f':>8}   vs 12 Hz white-muscle ceiling")
    print("  " + "-" * 76)
    out = {}
    for name, cl, note in CASES:
        f, u = freq_for(cl)
        out[name] = f
        print(f"  {name:<34}{cl:>6.2f}{u:>8.2f}m/s{f:>7.0f}Hz   {f/WHITE_MUSCLE_HZ:>5.1f}x over")
    for name, cl, note in CASES:
        print(f"    {name:<34} {note}")

    f_assumed = out["clap-and-fling, as assumed"]
    f_best = out["best MEASURED two-wing value"]
    print("\n" + "-" * 78)
    print("VERDICT")
    print("-" * 78)
    print(f"  The 53 Hz the project has been measuring against is the frequency at the")
    print(f"  REFUTED CL of 4.5 (computed here as {f_assumed:.0f} Hz, which reproduces it).")
    print(f"  At the best MEASURED coefficient available to this design, including the")
    print(f"  clap bonus, the requirement is {f_best:.0f} Hz -- a factor of "
          f"{f_best/f_assumed:.2f} higher.")
    print(f"\n  Against the measured 12 Hz ceiling for fish white locomotory muscle, the")
    print(f"  shortfall worsens from {f_assumed/WHITE_MUSCLE_HZ:.1f}x to "
          f"{f_best/WHITE_MUSCLE_HZ:.1f}x.")
    print("\n  So the peer's refutation of CL 4.5 does not reopen the flapping route. It")
    print("  closes it harder, and it does so with measured numbers where the route")
    print("  previously rested on an assumed one. Claims 587, 588, 592 and 593 are all")
    print("  stated against 53 Hz and are now QUANTITATIVELY CONSERVATIVE: each understates")
    print("  the difficulty. Their directions are unchanged.")
    print("=" * 78)
    return out


def controls():
    print("\nCONTROLS")
    ok = True

    # 1. The relation must be f ~ 1/sqrt(CL). A 4x CL change must halve the frequency.
    f1, _ = freq_for(1.0)
    f4, _ = freq_for(4.0)
    arm1 = abs(f1 / f4 - 2.0) < 1e-6
    print(f"  [{'ok' if arm1 else 'FAIL'}] f scales as 1/sqrt(CL): 4x CL gives exactly "
          f"{f1/f4:.3f}x the frequency")
    ok &= arm1

    # 2. POSITIVE CONTROL: the assumed CL must REPRODUCE the project's published 53 Hz. If it
    #    does not, this script is not modelling the same thing the claims were built on and
    #    every number above is about something else.
    f_assumed, _ = freq_for(4.50)
    arm2 = abs(f_assumed - 53.0) < 2.0
    print(f"  [{'ok' if arm2 else 'FAIL'}] CL 4.5 reproduces the published 53 Hz "
          f"(got {f_assumed:.1f} Hz) -- this script matches the claims it corrects")
    ok &= arm2

    # 3. NEGATIVE: a CL high enough must bring the requirement UNDER the muscle ceiling, or
    #    the comparison can only ever return 'too fast'.
    f_huge, _ = freq_for(500.0)
    arm3 = f_huge < WHITE_MUSCLE_HZ
    print(f"  [{'ok' if arm3 else 'FAIL'}] an absurd CL of 500 drops the requirement to "
          f"{f_huge:.1f} Hz, under the ceiling -- the test can return both answers")
    ok &= arm3

    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
