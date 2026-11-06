#!/usr/bin/env python3
"""What does the taxi phase cost in muscle power? A lower bound that needs no drag model.

THE QUESTION IS NEW AND THIS PROJECT CREATED IT. Claim 1869 reopened the taxi lever on
frequency: the 16.3 mm design needs 90-526 Hz, which no wild-type muscle reaches but the
toadfish swimbladder's measured 200 Hz (claim 979) covers in 4 of 9 amplitude x Strouhal
corners. The lever then rests on whether that muscle's 14.19 W/kg is enough, and the taxi's
power requirement had never been computed. Subproblems S1304, S1305 and S1308 ask for it and
ask for it the hard way -- through a drag model for a partly-submerged body, which needs a
wetted area, a wave-drag coefficient and a configuration factor this project does not hold.
Claim 1015 alone puts a 4.3x spread on drag coefficient from appendage configuration at fixed
Reynolds number, so that route produces a number with a factor-of-four bar on it.

SO TAKE THE BOUND INSTEAD. The taxi must raise the fish from its exit speed to its takeoff
speed within a stated distance. The kinetic-energy increment divided by the time available is
a power the muscle must deliver REGARDLESS of drag, because drag can only add to it. If even
that bound exceeds what the muscle supplies, the lever closes and no drag model is needed. If
it does not, drag decides and this says so rather than guessing.

Every input is a claim. The control reproduces claim 1168's six-number S1040 chain exactly
from the same machinery before any new number is computed.
"""
from __future__ import annotations


#: --- inputs, each with its claim ------------------------------------------------------------
U_EXIT = (1.57, "claim 443, measured mean maximal escape speed of adult zebrafish")
U_TAXI = (2.57, "claim 1404, the post-taxi speed the exemplar's 1.64x multiplier implies")
L_BODY = (0.0163, "claim 1404, the body-size target")
TAXI_BL = (20, "subproblems S1306/S1307/S1309, which specify the taxi within 20 body lengths")
ETA = (0.539, "claim 960, measured muscle-work-to-body-KE transfer efficiency; claim 1168 "
              "restores it to the S1040 chain, which had assumed 1.00")
MUSCLE_FRAC = ((0.29, 0.55), "claim 1168, which uses 0.55 as the FAVOURABLE end and 0.29 as the "
                             "other")
SUPERFAST = (14.19, "claim 979, toadfish swimbladder work-loop power -- the highest-frequency "
                    "muscle this project holds a measured power for")
BEST_ANY = (54.0, "claim 1090, Hyla chrysoscelis external oblique at 44 Hz, the highest measured "
                  "cyclic power in this project's envelope at ANY frequency")


def specific_ke(u: float) -> float:
    """Kinetic energy per kg of body, J/kg."""
    return 0.5 * u * u


def control() -> bool:
    """Reproduce claim 1168's S1040 chain, all six numbers, before computing anything new."""
    print("  CONTROL -- reproduce claim 1168's S1040 chain from the same machinery:")
    rows = [("escape branch 7.6 m/s", specific_ke(7.6), 28.9),
            ("glide route 4.37 m/s", specific_ke(4.37), 9.5),
            ("in-water start 1.57 m/s", specific_ke(1.57), 1.2)]
    ok = True
    for label, got, stated in rows:
        hit = abs(got - stated) < 0.1
        ok &= hit
        print(f"    {label:28s} {got:7.2f} J/kg   claim states {stated:5.1f}  "
              f"{'OK' if hit else 'MISMATCH'}")
    inc = specific_ke(4.37) - specific_ke(1.57)
    body_power = 143.0 * 0.55
    dur = inc / body_power
    dur_eta = dur / ETA[0]
    for label, got, stated in (("increment", inc, 8.3),
                               ("body power 143 x 0.55", body_power, 78.7),
                               ("duration at 100% transfer (ms)", dur * 1000, 106),
                               ("duration at 0.539 transfer (ms)", dur_eta * 1000, 196)):
        hit = abs(got - stated) <= max(1.0, 0.02 * stated)
        ok &= hit
        print(f"    {label:28s} {got:7.2f}        claim states {stated:5.1f}  "
              f"{'OK' if hit else 'MISMATCH'}")
    print(f"    -> {'REPRODUCED' if ok else 'FAILED'}")
    return ok


def main() -> int:
    print("=" * 94)
    print("TAXI POWER: a lower bound that assumes NO DRAG, so drag can only make it worse")
    print("=" * 94)
    if not control():
        print("\n  ABORTING: the machinery does not reproduce the project's own prior chain.")
        return 2

    u1, u2 = U_EXIT[0], U_TAXI[0]
    dist = TAXI_BL[0] * L_BODY[0]
    # THE LOWEST BOUND USES THE LONGEST POSSIBLE TRAVERSE TIME, not the arithmetic mean.
    # This project's adversarial arm challenged the first version: "the 157.5 ms window assumes
    # the mean speed is the arithmetic average of exit and takeoff speeds, which holds only
    # under constant acceleration, so 13.14 W/kg is not the drag-free lower bound the claim says
    # it is." Correct. Speed is bounded by u1 and u2 throughout, so d/u2 <= t <= d/u1, and the
    # LOWER bound on power needs t_max = d/u1. That is 207.6 ms against the 157.5 ms the
    # arithmetic mean gives, and it lowers the bound from 13.14 to 9.97 W/kg body -- a 1.32x
    # overstatement, corrected. The closure survives: see the reading below.
    u_mean = u1
    dt = dist / u_mean
    inc = specific_ke(u2) - specific_ke(u1)
    p_body = inc / dt

    print("\n  the taxi, from claims 443/1404 and the subproblems' own 20-body-length window:")
    print(f"    speed {u1} -> {u2} m/s over {dist*100:.1f} cm")
    print(f"    time bounded by d/u2 = {1000*dist/u2:.1f} ms and d/u1 = {1000*dist/u1:.1f} ms; "
          f"the LOWER bound on power takes the longest")
    print(f"    time available                 {dt*1000:7.1f} ms")
    print(f"    specific KE increment          {inc:7.2f} J/kg body")
    print(f"    body power required            {p_body:7.2f} W/kg body   (drag EXCLUDED)")

    print("\n  converted to MUSCLE power, which is what the envelope measures:\n")
    print(f"    {'transfer':>22s} {'muscle fraction':>16s} {'W/kg muscle':>13s} "
          f"{'x superfast 14.19':>19s}")
    worst = None
    for eta_label, eta in (("100% (generous)", 1.0), (f"{ETA[0]} (claim 960)", ETA[0])):
        for frac in MUSCLE_FRAC[0]:
            p_mus = p_body / eta / frac
            ratio = p_mus / SUPERFAST[0]
            worst = ratio if worst is None else min(worst, ratio)
            print(f"    {eta_label:>22s} {frac:>16.2f} {p_mus:>13.1f} {ratio:>18.1f}x")

    print("\n  READING")
    if worst > 1.0:
        print(f"    EVERY corner exceeds the superfast muscle's measured {SUPERFAST[0]} W/kg, and "
              f"the most\n    generous one -- 100 per cent transfer efficiency, the favourable "
              f"0.55 muscle\n    fraction, and NO DRAG AT ALL -- is still {worst:.1f}x short. Drag "
              f"only adds to the\n    requirement, so no drag model can rescue this and none is "
              f"needed to close it.")
        print(f"\n    Against the highest cyclic power in the whole envelope ({BEST_ANY[0]} W/kg, "
              f"claim 1090)\n    the bound is met -- but that muscle runs at 44 Hz, and the taxi "
              f"needs 90-526 Hz.\n    The two coordinates are met by different muscles and by "
              f"neither together, which is\n    exactly the configuration claim 1127 found for "
              f"the flapping route.")
    else:
        print(f"    The bound is met at the most generous corner ({worst:.2f}x), so drag decides "
              f"and\n    this does not close the lever. A drag model is needed after all.")
    # --- is there ANY amplitude at which one muscle meets both coordinates? ----------------
    print("\n  IS THERE AN AMPLITUDE THAT RESCUES IT? The power bound above is "
          "amplitude-INDEPENDENT --\n  it is a kinetic-energy requirement -- while the required "
          "FREQUENCY falls as amplitude rises\n  (f = St U / A). So the question is whether any "
          "sweep brings the frequency down to a muscle\n  that also has the power.\n")
    p_min = p_body / max(MUSCLE_FRAC[0])
    muscles = [("Hyla external oblique (claim 1090)", 44.0, 54.0),
               ("starling syringeal (claim 997)", 50.0, 8.9),
               ("toadfish swimbladder (claim 979)", 200.0, 14.19)]
    print(f"    required muscle power, most generous corner: {p_min:.1f} W/kg\n")
    print(f"    {'muscle':>36s} {'f_max':>7s} {'W/kg':>7s} {'power?':>8s} {'A at St 0.2':>13s}")
    for name, fmax, pw in muscles:
        a_bl = 0.2 * u2 / fmax / L_BODY[0]
        print(f"    {name:>36s} {fmax:>6.0f}H {pw:>7.1f} "
              f"{('YES' if pw >= p_min else 'no'):>8s} {a_bl:>10.2f} BL")
    print(f"\n    The only muscle with enough POWER is Hyla at 54 W/kg, and reaching its 44 Hz "
          f"needs a\n    peak-to-peak tail excursion of {0.2*u2/44.0/L_BODY[0]:.2f} body lengths "
          f"at the lowest Strouhal in the\n    band and {0.3*u2/44.0/L_BODY[0]:.2f} at the "
          f"midpoint -- against the 0.12-0.35 BL this project holds\n    (claim 1464) and the "
          f"~0.2 BL ordinary for fish. A sweep approaching the animal's own\n    length is not a "
          f"design parameter. NO MEASURED MUSCLE HERE MEETS BOTH COORDINATES AT ANY\n    "
          f"PHYSICALLY ORDINARY AMPLITUDE.")

    print("\n  WHAT THIS DOES NOT SHOW: the bound assumes the taxi must complete within 20 body "
          "lengths,\n  which the subproblems specify rather than measure. A longer taxi lowers "
          "the power and\n  raises the distance over which drag acts; this script does not model "
          "that trade.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
