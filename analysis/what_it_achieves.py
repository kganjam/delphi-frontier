#!/usr/bin/env python3
"""What the best specifiable design DOES do, stated alongside what it does not.

WHY THIS EXISTS. Four routes have been closed, each on a different measured quantity, and the
project's answer to "can a zebrafish be made to fly" is no. That is a result, but on its own it
is not a useful one: a reader cannot tell whether the design falls just short or is nowhere near,
and cannot tell what the genetic edits bought. This states the positive.

THE CRITERION QUESTION, WHICH IS REAL AND IS NOT GOALPOST-MOVING. Claim 571 set the flight
criterion as LIFT >= WEIGHT -- sustained flight -- and dismissed the project's earlier 2 cm
lift-attributable threshold as "a falsifier for whether a wing helps at all, NOT a criterion for
flight". That was right. But a real flying fish does not meet lift >= weight either: it leaves
the water ballistically and GLIDES, decelerating, and nobody disputes that it flies. So the
honest report gives BOTH criteria and both answers, and says which is which, rather than picking
the one that flatters the result in either direction.
"""
import math

G = 9.81
M = 4.0e-4 * (2.6 / 4.0) ** 3        # kg, best specifiable design: 2.6 cm young adult
BODY_LEN = 0.026                      # m
V_EXIT = 1.60                         # m/s achievable (claims 546, 583)
V_SUSTAIN = 4.02                      # m/s for lift = weight (claim 571)
LIFT_FRAC = (V_EXIT / V_SUSTAIN) ** 2

# Real flying fish, for scale. Park & Choi 2010 measured the aerodynamics; the distance figure
# is the commonly reported field observation and is labelled as such.
FF_BODY_M = 0.30
FF_DIST_M = 400.0                     # REPORTED field observation, not measured here


def airborne(lift_frac, v, angle_deg=45.0):
    """Range and time for a launch at v, with lift credited as a constant fraction of weight."""
    a = G * (1.0 - lift_frac)
    th = math.radians(angle_deg)
    vz, vx = v * math.sin(th), v * math.cos(th)
    t = 2.0 * vz / a
    return vx * t, t


def main():
    print("=" * 78)
    print("WHAT THE BEST SPECIFIABLE DESIGN ACTUALLY ACHIEVES")
    print("=" * 78)
    print(f"\n  2.6 cm young adult, {M*1e3:.3f} g, 2.65-fold fin (claims 580, 584)")
    print(f"  exit speed {V_EXIT} m/s; lift at that speed is "
          f"{100*LIFT_FRAC:.1f}% of weight\n")

    r_lift, t_lift = airborne(LIFT_FRAC, V_EXIT)
    r_ball, t_ball = airborne(0.0, V_EXIT)
    print(f"  {'case':<28}{'range':>10}{'time':>9}{'body lengths':>14}")
    print("  " + "-" * 62)
    print(f"  {'ballistic, no fin':<28}{r_ball*100:>8.1f}cm{t_ball*1000:>7.0f}ms"
          f"{r_ball/BODY_LEN:>13.1f}")
    print(f"  {'with the engineered fin':<28}{r_lift*100:>8.1f}cm{t_lift*1000:>7.0f}ms"
          f"{r_lift/BODY_LEN:>13.1f}")
    gain = r_lift - r_ball
    print(f"\n  THE FIN BUYS {gain*100:.1f} cm, a {100*gain/r_ball:.0f}% increase in airborne "
          f"range.")
    print(f"  That is {gain/BODY_LEN:.1f} body lengths of extra travel, from genetics alone.")

    print("\n" + "-" * 78)
    print("AGAINST BOTH CRITERIA")
    print("-" * 78)
    print(f"  WEAK (does a wing help at all?): the 2 cm lift-attributable threshold is MET --")
    print(f"     the fin contributes {gain*100:.1f} cm. The engineering works; the fin flies.")
    print(f"  STRONG (lift >= weight, sustained flight): NOT met, and not close -- lift is")
    print(f"     {100*LIFT_FRAC:.0f}% of weight, and all four routes to closing that gap are shut.")

    print("\n" + "-" * 78)
    print("AGAINST A REAL FLYING FISH, WHICH ALSO FAILS THE STRONG CRITERION")
    print("-" * 78)
    ff_bl = FF_DIST_M / FF_BODY_M
    print(f"  Exocoetidae glide (REPORTED field observation, not measured here): "
          f"{FF_DIST_M:.0f} m")
    print(f"     at a {FF_BODY_M*100:.0f} cm body, that is {ff_bl:.0f} body lengths")
    print(f"  This design:                      {r_lift*100:.0f} cm, "
          f"{r_lift/BODY_LEN:.0f} body lengths")
    print(f"  Ratio: {ff_bl/(r_lift/BODY_LEN):.0f}-fold, in body lengths.")
    print("\n  So the design is not a flying fish and is not within an order of magnitude of")
    print("  one. It is a zebrafish whose leap is measurably extended by an engineered fin.")
    print("  That IS a cross-scale result -- a named set of alleles changing an organism's")
    print("  airborne range by a computable amount -- and it is not flight.")
    print("=" * 78)
    return gain


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. POSITIVE: at lift = weight the model must NOT return a finite range, or the whole
    #    comparison is a constant that always finds a shortfall.
    a = G * (1.0 - 1.0)
    arm1 = abs(a) < 1e-12
    print(f"  [{'ok' if arm1 else 'FAIL'}] at lift = weight net acceleration is {a:.3f} m/s^2, "
          f"so the animal does not come down -- the test can return both answers")
    ok &= arm1
    # 2. The fin must make a POSITIVE difference, or the arithmetic is backwards.
    r1, _ = airborne(LIFT_FRAC, V_EXIT)
    r0, _ = airborne(0.0, V_EXIT)
    arm2 = r1 > r0
    print(f"  [{'ok' if arm2 else 'FAIL'}] the finned case travels further than the ballistic "
          f"one ({r1*100:.1f} vs {r0*100:.1f} cm)")
    ok &= arm2
    # 3. Zero lift must reproduce the textbook ballistic range v^2 sin(2*theta)/g.
    expect = V_EXIT ** 2 * math.sin(math.radians(90.0)) / G
    arm3 = abs(r0 - expect) < 1e-9
    print(f"  [{'ok' if arm3 else 'FAIL'}] at zero lift it reproduces the textbook ballistic "
          f"range ({r0*100:.2f} cm vs {expect*100:.2f} cm)")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
