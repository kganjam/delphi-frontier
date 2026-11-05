#!/usr/bin/env python3
"""Could a latch-mediated spring (LaMSA) launch reach the exit speed muscle cannot?

THE ROUTE NOBODY CONSIDERED. The project has closed gliding (needs CL ~7) and powered flapping
(needs ~83 Hz against a measured 12 Hz muscle ceiling). Both failed on limits of what muscle can
do DIRECTLY. Real animals routinely beat those limits with latch-mediated spring actuation: a
click beetle, a mantis shrimp, a froghopper and a trap-jaw ant all exceed the power their muscle
can produce, by loading a spring slowly and releasing it through a latch. Nothing in this project
has tested that route, and it attacks exactly the binding constraint.

THE DISTINCTION THAT DECIDES IT. LaMSA amplifies POWER, not ENERGY. The spring returns the work
the muscle put into it, faster. So it helps if and only if the limit is a POWER limit. If the
limit is the total WORK the muscle can do, a latch moves the same energy through a shorter time
and the exit speed is unchanged.

WHICH LIMIT IS THIS ONE? Claim 547 settles it and settles it against the route. Using the
MEASURED muscle energy density of 15.0 J/kg from Sutton et al. 2019 (PMC6907395), it found that
the observed 1.57 m/s peak already requires 20.5% of the animal's entire muscle work to arrive
as translational kinetic energy. That is an ENERGY budget, not a power budget.

Kinetic energy scales as v^2, so the required fraction scales as v^2 too, and the arithmetic
below is the whole argument.

ONE WAY OUT IS REAL AND IS COSTED HERE. A spring can be loaded over SEVERAL muscle contractions
before release -- a bow is drawn once but a crossbow can be cranked. If the energy needed exceeds
one contraction's work, the route is not dead, it just needs N contractions and a latch that
holds between them. That number is computed rather than asserted.
"""
import math

G = 9.81
ENERGY_DENSITY = 15.0      # J/kg of muscle, MEASURED, Sutton et al. 2019 (PMC6907395)
MUSCLE_FRACTION = 0.40     # of body mass, the value claim 547 used
V_OBSERVED = 1.57          # m/s, measured peak escape speed (Demesmay 2025)
FRAC_AT_OBSERVED = 0.205   # claim 547: 20.5% of muscle work at 1.57 m/s
V_NEEDED = 4.02            # m/s, claim 571: lift = weight for the achievable 3.7 cm2 fin

# the best specifiable design, claims 580/584
M_BODY = 4.0e-4 * (2.6 / 4.0) ** 3


def frac_of_muscle_work(v):
    """Fraction of total muscle work needed as translational KE at speed v.

    Anchored on claim 547's measured point rather than recomputed from scratch, so this cannot
    drift from the claim it extends: KE ~ v^2, so the fraction scales as (v/v_obs)^2.
    """
    return FRAC_AT_OBSERVED * (v / V_OBSERVED) ** 2


def main():
    muscle_mass = M_BODY * MUSCLE_FRACTION
    total_work = muscle_mass * ENERGY_DENSITY
    print("=" * 78)
    print("A LATCH-SPRING (LaMSA) LAUNCH: DOES IT REACH THE SPEED MUSCLE CANNOT?")
    print("=" * 78)
    print(f"\n  body {M_BODY*1e3:.3f} g, muscle fraction {MUSCLE_FRACTION}, "
          f"energy density {ENERGY_DENSITY} J/kg (MEASURED, Sutton 2019)")
    print(f"  total muscle work available in one full contraction: {total_work*1e3:.4f} mJ\n")
    print(f"  {'speed':>8}  {'KE':>12}  {'% of ONE contraction':>22}")
    print("  " + "-" * 48)
    for v, label in [(V_OBSERVED, "observed peak"), (2.5, ""), (3.0, ""),
                     (V_NEEDED, "needed for lift = weight")]:
        ke = 0.5 * M_BODY * v * v
        f = frac_of_muscle_work(v)
        print(f"  {v:>6.2f}m/s  {ke*1e3:>9.4f} mJ  {100*f:>19.1f}%   {label}")

    f_needed = frac_of_muscle_work(V_NEEDED)
    print("\n" + "-" * 78)
    print("WHY A LATCH DOES NOT HELP HERE")
    print("-" * 78)
    print(f"  Reaching {V_NEEDED} m/s needs {100*f_needed:.0f}% of the animal's ENTIRE muscle")
    print(f"  work as translational kinetic energy -- more than one contraction contains.")
    print("  A latch releases stored work faster; it does not create any. So on a single")
    print("  loading stroke the exit speed is unchanged and the route is closed for the")
    print("  same reason the others were: the energy is not there.")

    print("\n" + "-" * 78)
    print("THE ONE WAY OUT, COSTED RATHER THAN DISMISSED")
    print("-" * 78)
    n = math.ceil(f_needed / 1.0)
    print(f"  A spring loaded over SEVERAL contractions before release -- cranking a crossbow")
    print(f"  rather than drawing a bow -- needs N >= {n} full contractions at 100% transfer,")
    print(f"  and more at any realistic efficiency:")
    for eff in (1.0, 0.8, 0.5, 0.3):
        print(f"     at {100*eff:>3.0f}% storage-and-release efficiency: "
              f"{math.ceil(f_needed/eff):>2d} contractions")
    print("\n  That is not absurd on its face, and it is the first route in this project that")
    print("  is blocked by ANATOMY rather than by physics: it needs a spring that can hold")
    print(f"  {f_needed*100:.0f}% of the animal's muscle work and a latch that holds it between")
    print("  contractions. Neither is catalogued in this project, and no fish is known to")
    print("  this analysis that does it. What it is NOT is energetically impossible.")
    print("=" * 78)
    return f_needed


def controls():
    print("\nCONTROLS")
    ok = True

    # 1. The anchor must reproduce claim 547's measured point. If it does not, this analysis
    #    is extending a different claim than the one it cites.
    arm1 = abs(frac_of_muscle_work(V_OBSERVED) - FRAC_AT_OBSERVED) < 1e-12
    print(f"  [{'ok' if arm1 else 'FAIL'}] at the observed 1.57 m/s the model returns "
          f"{100*frac_of_muscle_work(V_OBSERVED):.1f}%, reproducing claim 547's measured point")
    ok &= arm1

    # 2. POSITIVE: a speed the muscle CAN reach must come out under 100%, or the test can only
    #    ever say 'impossible' and proves nothing.
    arm2 = frac_of_muscle_work(2.0) < 1.0
    print(f"  [{'ok' if arm2 else 'FAIL'}] 2.0 m/s comes out at "
          f"{100*frac_of_muscle_work(2.0):.0f}%, i.e. ACHIEVABLE -- the test returns both answers")
    ok &= arm2

    # 3. The v^2 scaling must actually be quadratic, not linear.
    r = frac_of_muscle_work(2 * V_OBSERVED) / frac_of_muscle_work(V_OBSERVED)
    arm3 = abs(r - 4.0) < 1e-9
    print(f"  [{'ok' if arm3 else 'FAIL'}] doubling speed quadruples the requirement "
          f"(got {r:.3f}x), so KE scales as v^2 and not v")
    ok &= arm3

    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
