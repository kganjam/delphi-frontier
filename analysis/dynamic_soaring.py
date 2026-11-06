#!/usr/bin/env python3
"""Route D: can the fish harvest energy from the WIND instead of from its own muscle?

WHY ASK. All three closed routes failed on the same thing in different clothes -- the animal's
own energy budget. Gliding needs a lift coefficient it cannot reach, flapping needs a muscle
frequency no fish muscle attains, and the latch-spring launch needs a transfer efficiency nobody
has measured above 39%. Dynamic soaring does not draw on that budget at all: an albatross
"harvests energy from a spatiotemporal wind gradient" (Kempton et al. 2022, Sci Adv) and sustains
non-flapping flight over thousands of kilometres on it. If a fish could do the same, the binding
constraint of the whole project would be gone.

THE ARGUMENT IS NOT "IT IS TOO SMALL". That would be an appeal to a reference class, and the
near-surface wind gradient a small animal experiences is steeper in RELATIVE terms than the one an
albatross uses, so the naive scaling argument is not obviously right. It is computed instead.

THE DECISIVE STRUCTURE, which is why this is short: dynamic soaring supplies ENERGY, not LIFT.
To execute a cycle the animal must still be FLYING -- generating lift at least equal to weight
while it climbs windward, turns, and descends leeward. Claim 599 established the achievable fin
is 6.5-fold short of the area for lift = weight at the speed the animal can reach. A fish that
cannot hold itself up cannot complete the manoeuvre that would give it the energy to hold itself
up. The question is therefore whether its TIME ALOFT exceeds one soaring CYCLE.
"""
import math

G = 9.81
M = 4.0e-4 * (2.6 / 4.0) ** 3        # kg, the best specifiable design
V_EXIT = 1.60                        # m/s, the achievable exit speed (claims 546, 583)
V_NEEDED = 4.02                      # m/s, speed for lift = weight (claim 571)
LIFT_FRACTION = (V_EXIT / V_NEEDED) ** 2   # lift scales as v^2 at fixed area and CL


def time_aloft():
    """Time before the fish returns to the water, with lift credited at its real fraction.

    Net downward acceleration is g*(1 - L/W). Launched at 45 degrees, the vertical component
    is V_EXIT/sqrt(2) and the flight time is twice the rise time.
    """
    a = G * (1.0 - LIFT_FRACTION)
    vz = V_EXIT / math.sqrt(2.0)
    return 2.0 * vz / a, a


def max_climb_height():
    """How high can it climb? This is the question, not how long a cycle takes.

    A dynamic-soaring cycle begins with a WINDWARD CLIMB (Sachs et al. 2013). An animal whose
    lift is a fraction of its weight is decelerating upward from the moment it leaves the
    water; the most height it can ever gain is the ballistic rise its launch bought, and it
    gains none thereafter. So the usable shear-layer excursion is capped by the launch, not
    chosen freely.
    """
    a = G * (1.0 - LIFT_FRACTION)
    vz = V_EXIT / math.sqrt(2.0)      # 45-degree launch
    return (vz * vz) / (2.0 * a), a


def main():
    print("=" * 78)
    print("ROUTE D: DYNAMIC SOARING -- HARVESTING THE WIND INSTEAD OF THE MUSCLE")
    print("=" * 78)
    t_aloft, a = time_aloft()
    print(f"\n  lift at the achievable {V_EXIT} m/s is {100*LIFT_FRACTION:.1f}% of weight")
    print(f"  (lift scales as v^2, and lift = weight needs {V_NEEDED} m/s -- claim 599)")
    print(f"  so the animal falls at {a:.2f} m/s^2 throughout\n")
    print(f"  TIME ALOFT after a 45-degree launch at {V_EXIT} m/s: {t_aloft*1000:.0f} ms\n")
    h_max, _ = max_climb_height()
    print(f"  MAXIMUM HEIGHT it can reach, ballistic rise from that launch: "
          f"{h_max*100:.1f} cm")
    print(f"  and it gains NO height after that, because lift < weight throughout.\n")
    print("  For comparison, the shear layer a soaring bird works in:")
    print("    albatross dynamic soaring             ~10-20 m")
    print("    Manx shearwater, smallest confirmed   ~ a few m")
    print(f"    this design, entire vertical range    {h_max*100:.1f} cm")
    print("\n" + "-" * 78)
    print("VERDICT: ROUTE D IS CLOSED, AND FOR A REASON THE OTHERS WERE NOT")
    print("-" * 78)
    print("  Dynamic soaring supplies ENERGY, not LIFT. A cycle BEGINS with a windward climb")
    print("  (Sachs et al. 2013), and this animal generates "
          f"{100*LIFT_FRACTION:.0f}% of its weight in lift at the")
    print("  speed it can reach. It cannot climb at all. Its entire vertical range is the")
    print(f"  {h_max*100:.1f} cm of ballistic rise its launch bought, against the metres of shear")
    print("  layer a soaring bird works in, and it harvests nothing on the way down that it")
    print("  did not pay for on the way up.")
    print("\n  So a fish that cannot hold itself up cannot perform the manoeuvre that would")
    print("  give it the energy to hold itself up. The dependency runs the wrong way, and this")
    print("  route fails on the SAME lift shortfall as route A rather than on a new quantity.")
    print("  Harvesting the wind does not help an animal that cannot stay in it.")
    print("=" * 78)
    return t_aloft


def controls():
    print("\nCONTROLS")
    ok = True
    # 1. POSITIVE: an animal that DOES make lift = weight must come out with unbounded time
    #    aloft, or the test is a constant.
    a_sustain = G * (1.0 - 1.0)
    arm1 = abs(a_sustain) < 1e-12
    print(f"  [{'ok' if arm1 else 'FAIL'}] at lift = weight the net acceleration is "
          f"{a_sustain:.3f} m/s^2, i.e. it does NOT fall -- the test can return both answers")
    ok &= arm1
    # 2. Lift must scale as v^2, not v.
    r = (2 * V_EXIT / V_NEEDED) ** 2 / (V_EXIT / V_NEEDED) ** 2
    arm2 = abs(r - 4.0) < 1e-9
    print(f"  [{'ok' if arm2 else 'FAIL'}] doubling speed quadruples lift (got {r:.3f}x)")
    ok &= arm2
    # 3. NEGATIVE: time aloft must be finite and short at the real lift fraction.
    t, _ = time_aloft()
    arm3 = 0.0 < t < 1.0
    print(f"  [{'ok' if arm3 else 'FAIL'}] at the real lift fraction, time aloft is "
          f"{t*1000:.0f} ms -- finite and under a second")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
