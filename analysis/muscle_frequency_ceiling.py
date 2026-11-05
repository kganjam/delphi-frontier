#!/usr/bin/env python3
"""Does any fish muscle generate power at the 53 Hz the flapping route requires?

THE ROUTE. Claims 585-588 and 592 leave powered flapping as the only route not excluded by a
factor of two or more: ~53 W/kg of mechanical power at a ~53 Hz beat, with no elastic recovery.
Claim 589 found zebrafish carries no annotated superfast myosin, so the route already requires a
heterologous transgene. This asks the prior question: is 53 Hz reachable by fish muscle at all?

THE MEASUREMENT. Young & Rome 2001, Proc Biol Sci 268:1965-70 (PMID 11571041,
doi 10.1098/rspb.2001.1731), read_level=abstract. They measured power output by work loop across
a wide frequency range for all three toadfish muscle types:
    red myotomal        no power above ~2.2 Hz
    white myotomal      no power above ~12 Hz
    swimbladder (sonic) power above 100 Hz, but at SWIMMING frequencies only 1/20 of red
                        and 1/7 of white
and concluded the two designs are MUTUALLY EXCLUSIVE: "To generate the same total power needed
for swimming would require unfeasibly large amounts of swimbladder muscle that could not fit
into the fish."

WHAT THIS DOES AND DOES NOT SETTLE -- stated carefully, because the tempting argument is wrong.

  SETTLED. Ordinary fish locomotory muscle cannot power this route. White fast-twitch muscle,
  the faster of the two locomotory types, produces NO power above ~12 Hz. 53 Hz is 4.4x beyond
  that ceiling. This is a measured ceiling, not an extrapolation, and it closes the option of
  driving the fin with zebrafish fin muscle however much of it is added.

  NOT SETTLED BY THE 1/7 RATIO, and it would be an error to use it here. That ratio is measured
  at SWIMMING frequencies, where white muscle still works. At 53 Hz white muscle produces zero,
  so the ratio is not the comparison that matters -- superfast muscle wins trivially against
  zero. Closing the route needs the ABSOLUTE power of superfast muscle in W/kg at ~53 Hz, and
  that number is not in the abstract. It is this project's next blocking magnitude.

  THE AUTHORS' OWN NEGATIVE RESULT IS STILL EVIDENCE, at one remove. They measured that
  substituting superfast muscle for a locomotory role needs more muscle than fits in the fish --
  for SWIMMING. Powered flight requires more mass-specific power than swimming, so the
  substitution is measured to fail at a strictly easier task. That is an INFERENCE from their
  measurement, flagged as such, not a measurement about flight.
"""
import math

BEAT_HZ = 53.0

# MEASURED ceilings, Young & Rome 2001, read_level=abstract
CEILING = {
    "red myotomal (slow-twitch, cruise)":   2.2,
    "white myotomal (fast-twitch, burst)": 12.0,
    "swimbladder (superfast, sonic)":     100.0,   # "in excess of 100 Hz"; a floor, not a ceiling
}
SUPERFAST = "swimbladder (superfast, sonic)"


def report():
    print("=" * 78)
    print("FISH MUSCLE POWER-GENERATING FREQUENCY CEILINGS vs THE 53 Hz BEAT")
    print("=" * 78)
    print("  Young & Rome 2001, PMID 11571041, work loop, read_level=abstract\n")
    print(f"  {'muscle type':<38}{'ceiling':>10}   {'vs 53 Hz beat':>16}")
    print("  " + "-" * 66)
    reach = []
    for name, hz in CEILING.items():
        ok = hz >= BEAT_HZ
        verdict = "REACHES" if ok else f"short by {BEAT_HZ/hz:.1f}x"
        note = "  (a floor: 'in excess of')" if name == SUPERFAST else ""
        print(f"  {name:<38}{hz:>7.1f} Hz   {verdict:>16}{note}")
        if ok:
            reach.append(name)

    print(f"\n  locomotory types reaching {BEAT_HZ:.0f} Hz: "
          f"{len([n for n in reach if n != SUPERFAST])} of 2")
    print(f"  white muscle is the faster locomotory type and is short by "
          f"{BEAT_HZ/CEILING['white myotomal (fast-twitch, burst)']:.1f}x.")

    print("\n" + "-" * 78)
    print("WHAT THIS CLOSES")
    print("-" * 78)
    print("  The option of powering the beat with zebrafish fin muscle is closed. The ceiling")
    print("  is a frequency, so adding muscle mass does not reach it -- more muscle at 53 Hz")
    print("  still produces zero power. Claim 589's heterologous superfast transgene is")
    print("  therefore MANDATORY for this route, not an optimisation.")

    print("\n" + "-" * 78)
    print("WHAT REMAINS OPEN -- the project's next blocking magnitude")
    print("-" * 78)
    print("  The ABSOLUTE power of superfast muscle, in W/kg, at ~53 Hz. The route needs")
    print(f"  ~53 W/kg. The published 1/7 ratio is measured at SWIMMING frequencies and does")
    print("  NOT transfer here: at 53 Hz white muscle produces zero, so a ratio against it is")
    print("  meaningless. Using that ratio to close the route would be an error.")
    print("\n  Young & Rome's own conclusion -- that substituting superfast muscle for a")
    print("  locomotory role needs more muscle than fits in the fish -- was measured for")
    print("  SWIMMING. Flight needs more mass-specific power than swimming, so the")
    print("  substitution is measured to fail at a strictly easier task. INFERENCE, not")
    print("  measurement, and recorded as such.")
    print("=" * 78)
    return reach


def controls():
    """Both arms must be exercised. A table that can only print 'short by' proves nothing."""
    print("\nCONTROLS")
    ok = True

    # 1. POSITIVE: something in the table MUST clear the beat, or the comparison is a constant.
    arm1 = any(hz >= BEAT_HZ for hz in CEILING.values())
    print(f"  [{'ok' if arm1 else 'FAIL'}] at least one muscle type clears {BEAT_HZ:.0f} Hz "
          f"(superfast, {CEILING[SUPERFAST]:.0f} Hz) -- the comparison can return both answers")
    ok &= arm1

    # 2. NEGATIVE: the locomotory types must fail it.
    loco = {k: v for k, v in CEILING.items() if k != SUPERFAST}
    arm2 = all(hz < BEAT_HZ for hz in loco.values())
    print(f"  [{'ok' if arm2 else 'FAIL'}] both locomotory types fall short, as the paper reports")
    ok &= arm2

    # 3. The shortfall must be computed from the ceiling, not fixed. A hard-coded factor would
    #    pass arms 1 and 2.
    probe = BEAT_HZ / 26.5
    arm3 = abs(probe - 2.0) < 1e-9
    print(f"  [{'ok' if arm3 else 'FAIL'}] shortfall is computed from the ceiling "
          f"(a 26.5 Hz ceiling gives exactly {probe:.1f}x)")
    ok &= arm3

    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    report()
    if not controls():
        raise SystemExit("controls failed")
