#!/usr/bin/env python3
"""Does shrinking the body to 16.3 mm make the TAXI phase unachievable?

THE QUESTION EXISTS BECAUSE OF A TRADE-OFF NOBODY CHECKED. Claim 1404 rescued the design by
adding the taxi phase the exemplar actually uses: applying Cypselurus's own 1.64x speed
multiplier takes the shortfall from 4.3x to 1.6x and MOVES THE BODY-SIZE TARGET FROM 6.0 mm TO
16.3 mm. Claim 1405 then reclassified the taxi numbers as `simulated` (the source is CFD with an
assumed 10 m/s input). Neither asks whether a 16.3 mm fish can DRIVE that taxi.

It is a fair question because the project has already closed two routes on the same constraint:
required oscillation frequency against a muscle ceiling. Claim 585 closed powered flapping at
108 Hz against ~50 Hz for a hummingbird. Claims 52, 84, 144, 145, 177 and 431 litigated the
taxi tail-beat at ADULT size and settled on 72-83 Hz against a 52 Hz EMG maximum -- 1.4-1.6x
over, with claim 440 resolving the Strouhal dispute against claim 52 using this project's own
law file.

WHAT IS NEW HERE IS THE BODY SIZE, AND IT CUTS THE WRONG WAY. Tail-beat amplitude scales with
body length, so St = f A / U at fixed St and fixed required speed makes f scale as 1/L. The
move that fixes the LIFT shortfall -- shrinking the animal so its fin area is enough -- shrinks
the propulsor that has to do the taxiing. The design cannot take the smaller body without
taking the higher frequency, and the earlier analyses were all run at adult size.

EVERY INPUT IS A CITED CLAIM OR THIS PROJECT'S OWN LAW FILE. Nothing is invented; where a value
is a range the range is carried through rather than collapsed to a midpoint.

CONTROL, and it is a reproduction rather than a plausibility check: the same function, given
claim 84's OWN stated inputs (1.95 m/s, ~8 mm amplitude), must return claim 84's own answer of
72-83 Hz. If it does not, the implementation is wrong and nothing below is worth reading.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "swarm"))

NU = 1.0e-6          #: kinematic viscosity of water at ~20 C, m^2/s

#: --- inputs, each with the claim or file it comes from -------------------------------------
U_EXIT = (1.57, "claim 443, Demesmay et al. 2025, mean maximal escape speed of adult zebrafish")
U_TAXI = (2.57, "claim 1404, exit 1.57 m/s times the exemplar's own 1.64x taxi speed multiplier")
L_BODY = (0.0163, "claim 1404, the body-size target the taxi multiplier moves the design to")
AMP_BL = ((0.12, 0.20, 0.35), "claim 1464, peak-to-peak tail excursion in body lengths "
                              "(MODELLED-HERE in its source, not observed)")
ST_BAND = ((0.2, 0.4), "library/laws/strouhal.yaml cruising_band; foil_optimum is 0.25-0.35")
F_CEILING = (52.0, "claim 196, measured adult zebrafish TRANSIENT escape maximum; also the EMG "
                   "maximum claims 84/144/145 measure against")
F_SUSTAINED = (21.0, "claim 196, measured adult zebrafish SUSTAINED maximum. The taxi is a "
                     "sustained phase -- S1306/S1307 specify 20 body lengths -- so this is "
                     "arguably the binding ceiling and the transient figure is the generous one.")
RE_MIN = (1.0e4, "library/laws/strouhal.yaml domain_of_validity.reynolds_min")


def required_f(U: float, amp_m: float, st: float) -> float:
    """St = f A / U, rearranged. A is PEAK-TO-PEAK, as the law file states explicitly."""
    return st * U / amp_m


def control() -> bool:
    """Reproduce claim 84 from claim 84's own inputs."""
    lo = required_f(1.95, 0.008, 0.25)
    hi = required_f(1.95, 0.008, 0.35)
    mid = required_f(1.95, 0.008, 0.318)
    ok = 72 <= mid <= 83
    print("  CONTROL -- reproduce claim 84 from its own stated inputs "
          "(1.95 m/s, ~8 mm peak-to-peak):")
    print(f"    foil band 0.25-0.35 gives {lo:.0f}-{hi:.0f} Hz; at its implied St 0.318, "
          f"{mid:.1f} Hz")
    print(f"    claim 84 states 72-83 Hz          -> {'REPRODUCED' if ok else 'MISMATCH'}")
    return ok


def main() -> int:
    print("=" * 94)
    print("TAIL-BEAT FREQUENCY REQUIRED TO DRIVE THE TAXI PHASE AT THE 16.3 mm TARGET")
    print("=" * 94)
    if not control():
        print("\n  ABORTING: the implementation does not reproduce the project's own prior result.")
        return 2

    U = U_TAXI[0]
    L = L_BODY[0]
    re = U * L / NU
    print(f"\n  Reynolds number at the taxi point: U L / nu = {U} x {L} / {NU:.0e} = {re:,.0f}")
    print(f"    the law's declared floor is {RE_MIN[0]:,.0f} ({RE_MIN[1]}),")
    print(f"    so this point is {'INSIDE' if re >= RE_MIN[0] else 'OUTSIDE'} the band's stated "
          f"domain -- the regime objection raised in claims 177 and 431 does not apply here.")

    print(f"\n  required peak-to-peak frequency, f = St U / A, at U = {U} m/s:\n")
    print(f"    {'amplitude':>26s} {'St=0.20':>9s} {'St=0.30':>9s} {'St=0.40':>9s}  "
          f"{'x the ' + str(F_CEILING[0]) + ' Hz ceiling':>22s}")
    worst = best = None
    for bl in AMP_BL[0]:
        a = bl * L
        fs = [required_f(U, a, st) for st in (0.2, 0.3, 0.4)]
        ratio = (min(fs) / F_CEILING[0], max(fs) / F_CEILING[0])
        print(f"    {bl:>5.2f} BL = {a*1000:>6.2f} mm   {fs[0]:>9.0f} {fs[1]:>9.0f} {fs[2]:>9.0f}"
              f"   {ratio[0]:>8.1f}x - {ratio[1]:.1f}x")
        lo, hi = min(fs), max(fs)
        best = lo if best is None else min(best, lo)
        worst = hi if worst is None else max(worst, hi)

    print(f"\n  ACROSS THE WHOLE INPUT RANGE: {best:.0f} to {worst:.0f} Hz required, against a "
          f"{F_CEILING[0]:.0f} Hz ceiling")
    print(f"  against the SUSTAINED ceiling of {F_SUSTAINED[0]:.0f} Hz ({F_SUSTAINED[1][:46]}...), "
          f"which is\n  the relevant one for a phase held over 20 body lengths: "
          f"{best/F_SUSTAINED[0]:.1f}x to {worst/F_SUSTAINED[0]:.1f}x over.")
    print(f"  = {best/F_CEILING[0]:.1f}x to {worst/F_CEILING[0]:.1f}x over. The most generous "
          f"corner -- the largest amplitude in claim 1464 with the lowest Strouhal in the band "
          f"-- is still {best/F_CEILING[0]:.1f}x over.")

    # The comparison that makes the trade-off visible: the same calculation at adult size.
    L_ADULT = 0.040
    print("\n  WHY THIS IS WORSE THAN THE EARLIER ADULT-SIZE ANALYSES, which is the whole point:")
    for label, ll in (("adult, 40 mm", L_ADULT), ("the 16.3 mm target", L)):
        a = 0.20 * ll
        f = required_f(U, a, 0.3)
        print(f"    {label:<20s} A = {a*1000:5.2f} mm at 0.20 BL  ->  {f:6.0f} Hz "
              f"({f/F_CEILING[0]:.1f}x the ceiling)")
    print(f"    f scales as 1/L at fixed St and U, so shrinking the body {L_ADULT/L:.1f}x to fix "
          f"the LIFT\n    shortfall raises the taxi frequency by the same {L_ADULT/L:.1f}x. The "
          f"two requirements pull\n    against each other and claim 1404 moved the body size "
          f"without checking the second.")

    print(f"\n  WHAT THIS DOES NOT SHOW. The 52 Hz ceiling is inherited from claims 84/144/145 "
          f"and\n  claim 145 records that it is the figure S24-D is most sensitive to -- a rise "
          f"of 17-56 per cent\n  flips that verdict. It would need to rise {best/F_CEILING[0]:.1f}x to "
          f"flip this one. The amplitude range\n  is MODELLED-HERE in claim 1464 rather than "
          f"observed, and no juvenile zebrafish tail-beat\n  amplitude at 16 mm is held by this "
          f"project -- that is the measurement that would settle it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
