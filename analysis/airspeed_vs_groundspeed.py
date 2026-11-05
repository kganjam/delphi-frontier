#!/usr/bin/env python3
"""The project has been using GROUND speed where LIFT needs AIRSPEED. In wind they differ.

FOUND BY THE PROJECT'S OWN ADVERSARIAL ARM, against claim 961, written an hour earlier:
  "The 15.8%-of-weight lift figure uses the animal's 1.60 m/s as its airspeed, which only
   holds in still air, the one condition in which dynamic soaring cannot occur."

That is correct, and it reaches further than the claim it was aimed at. Lift depends on the
speed of the wing THROUGH THE AIR. Every lift figure in this project -- claim 571's 4.02 m/s
requirement, claim 599's 6.5-fold area shortfall, claim 961's 15.8% -- has been computed from
the fish's speed relative to the WATER it launched from, which is its ground speed.

A fish leaving the water into a headwind W has an initial airspeed of (v_exit + W). That is not
a modelling convenience; it is a real one-time gift from the relative motion of water and air,
and flying fish are observed to launch into the wind.

WHAT THIS DOES AND DOES NOT CHANGE, because the temptation is to over-claim it:
  * It DOES change the launch condition. Lift scales as airspeed squared.
  * It does NOT give sustained flight. In steady uniform wind the whole problem is identical in
    the air frame -- the wind just translates the reference frame -- so holding altitude still
    requires the animal to MAINTAIN that airspeed against drag, and it has no thrust. The gift
    is to the initial condition only, and it decays.
"""
import math

G = 9.81
V_EXIT = 1.60          # m/s relative to the water, i.e. GROUND speed (claims 546, 583)
V_LIFT_EQ = 4.02       # m/s AIRSPEED at which lift = weight for the achievable fin (claim 571)


def lift_fraction(airspeed):
    return (airspeed / V_LIFT_EQ) ** 2


def main():
    print("=" * 78)
    print("LIFT NEEDS AIRSPEED, NOT GROUND SPEED, AND IN WIND THEY DIFFER")
    print("=" * 78)
    print(f"\n  exit speed relative to the water: {V_EXIT} m/s")
    print(f"  airspeed for lift = weight:        {V_LIFT_EQ} m/s (claim 571)\n")
    print(f"  {'headwind':>10} {'airspeed at exit':>18} {'lift / weight':>15}   note")
    print("  " + "-" * 66)
    w_break = V_LIFT_EQ - V_EXIT
    for w, note in [(0.0, "still air -- what the project assumed"),
                    (1.0, "barely a breeze"),
                    (w_break, "LIFT = WEIGHT AT EXIT"),
                    (4.0, "a moderate breeze"),
                    (8.0, "fresh breeze, Beaufort 5")]:
        a = V_EXIT + w
        lf = lift_fraction(a)
        print(f"  {w:>8.2f}m/s {a:>16.2f}m/s {lf:>14.2f}   {note}")
    print(f"\n  HEADWIND AT WHICH LIFT EQUALS WEIGHT AT THE MOMENT OF EXIT: "
          f"{w_break:.2f} m/s")
    print(f"  That is about {w_break*1.944:.1f} knots -- a light breeze, Beaufort 2.")

    print("\n" + "-" * 78)
    print("WHAT IT DOES NOT BUY, STATED BEFORE WHAT IT DOES")
    print("-" * 78)
    print("  It does NOT give sustained flight. In steady uniform wind the problem is")
    print("  identical in the air frame; the wind only translates the frame. Holding")
    print("  altitude still demands the animal MAINTAIN that airspeed against drag, and it")
    print("  has no thrust in air. The gift is to the INITIAL CONDITION and it decays.")
    print("  So claim 571's requirement is unchanged: sustained flight needs the animal to")
    print("  make 4.02 m/s of airspeed by itself, and it cannot.")

    print("\n" + "-" * 78)
    print("WHAT IT DOES BUY, AND IT IS NOT NOTHING")
    print("-" * 78)
    print(f"  At exit in a {w_break:.1f} m/s headwind the design is not falling at "
          f"{G*(1-lift_fraction(V_EXIT)):.1f} m/s^2 --")
    print("  it is momentarily in equilibrium, and begins to fall only as drag erodes the")
    print("  airspeed. Every airborne-range number in this project was computed in still")
    print("  air and is therefore a LOWER BOUND for a fish that launches into wind, which")
    print("  is what flying fish are observed to do.")
    print("\n  THE PROJECT'S FOUR CLOSURES ARE UNAFFECTED, and this is why the correction is")
    print("  bounded rather than route-reopening: all four are about SUSTAINED flight, which")
    print("  needs self-generated airspeed. But claim 961's dynamic-soaring closure rested")
    print("  specifically on 'it cannot climb at all', computed at the still-air lift")
    print("  fraction, and that premise is wrong in the only conditions soaring happens in.")
    print("=" * 78)
    return w_break


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. Still air must reproduce the project's existing 15.8%, or this contradicts rather
    #    than extends the claims it corrects.
    lf0 = lift_fraction(V_EXIT)
    arm1 = abs(lf0 - 0.158) < 0.002
    print(f"  [{'ok' if arm1 else 'FAIL'}] at zero wind it returns {100*lf0:.1f}%, reproducing "
          f"claim 961's 15.8%")
    ok &= arm1
    # 2. The break-even wind must actually give lift = weight.
    lfb = lift_fraction(V_EXIT + (V_LIFT_EQ - V_EXIT))
    arm2 = abs(lfb - 1.0) < 1e-12
    print(f"  [{'ok' if arm2 else 'FAIL'}] at the break-even headwind lift/weight is "
          f"{lfb:.6f}")
    ok &= arm2
    # 3. NEGATIVE: a tailwind must make it WORSE, or the model ignores direction.
    lf_tail = lift_fraction(max(0.0, V_EXIT - 1.0))
    arm3 = lf_tail < lf0
    print(f"  [{'ok' if arm3 else 'FAIL'}] a 1 m/s TAILWIND drops lift to {100*lf_tail:.1f}% "
          f"from {100*lf0:.1f}% -- direction matters, the model is not symmetric")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
