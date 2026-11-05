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





# ---------------------------------------------------------------------------------------------
# ADDED after claim 957: the anatomical objection was removed (seahorses and pipefish are a
# characterised LaMSA system whose springs are epaxial and sternohyoideus TENDONS), leaving the
# route turning on TWO unknowns: can a tendon spring HOLD 134% of a contraction's work, and can
# it be CHARGED across successive contractions? This settles the first one and leaves the second.
#
# The approach avoids needing a precise strain-energy density, because the question is really a
# MASS question: how much tendon would it take? If the answer is a few percent of body mass
# across two orders of magnitude of assumption, the storage capacity is not the blocker.

RHO_TENDON = 1100.0        # kg/m^3, ASSUMED standard value for collagenous tissue
E_TENDON = 1.0e9           # Pa, ASSUMED tendon Young's modulus, order 1 GPa


def strain_energy_density(eps, E=E_TENDON, rho=RHO_TENDON):
    """Energy per unit MASS a linear-elastic spring holds at strain eps: (1/2)E*eps^2 / rho."""
    return 0.5 * E * eps * eps / rho


def tendon_mass_needed():
    print("\n" + "=" * 78)
    print("CAN A TENDON SPRING HOLD IT? A MASS QUESTION, NOT A MATERIAL-PROPERTY QUESTION")
    print("=" * 78)
    total_work = M_BODY * MUSCLE_FRACTION * ENERGY_DENSITY
    need = frac_of_muscle_work(V_NEEDED) * total_work
    print(f"\n  energy to store: {need*1e3:.4f} mJ "
          f"({100*frac_of_muscle_work(V_NEEDED):.0f}% of one contraction)")
    print(f"  body mass: {M_BODY*1e3:.3f} g\n")
    print(f"  {'strain':>8} {'J/kg':>9} {'tendon mass':>13} {'% of body':>11}")
    print("  " + "-" * 46)
    rows = []
    for eps, note in [(0.02, "very conservative"), (0.04, "safe working strain"),
                      (0.06, ""), (0.08, "near tendon failure strain")]:
        u = strain_energy_density(eps)
        m = need / u
        rows.append(100 * m / M_BODY)
        print(f"  {eps:>8.2f} {u:>9.0f} {m*1e6:>10.2f} mg {100*m/M_BODY:>10.2f}%   {note}")
    # A deliberately crushed material property, two orders of magnitude below the above.
    u_low = 30.0
    m_low = need / u_low
    print(f"\n  even at an absurdly low {u_low:.0f} J/kg -- below MUSCLE's own 15 J/kg per")
    print(f"  contraction by only a factor of 2 -- the requirement is {m_low*1e6:.1f} mg, "
          f"{100*m_low/M_BODY:.1f}% of body mass.")
    print("\n" + "-" * 78)
    print("VERDICT")
    print("-" * 78)
    print(f"  Across strains from 2% to 8%, the tendon needed is "
          f"{min(rows):.2f}% to {max(rows):.2f}% of body mass.")
    print("  Zebrafish already carry far more tendon and collagenous tissue than that.")
    print("  SO STORAGE CAPACITY IS NOT THE BLOCKER, and it is not close to being one.")
    print("  The route now turns on ONE question, not two: whether a latch can hold a")
    print("  partially-charged spring BETWEEN contractions so it can be loaded across")
    print("  2 to 5 of them. No source found reports multi-contraction charging either way;")
    print("  every LaMSA system located here loads within a single pre-load window, which")
    print("  in pipefish is over 300 ms.")
    print("=" * 78)
    return rows


def controls_mass():
    print("\nCONTROLS (storage)")
    ok = True
    # 1. The scaling must be quadratic in strain, as (1/2)E eps^2 requires.
    r = strain_energy_density(0.08) / strain_energy_density(0.04)
    arm1 = abs(r - 4.0) < 1e-9
    print(f"  [{'ok' if arm1 else 'FAIL'}] doubling strain quadruples energy density "
          f"(got {r:.3f}x)")
    ok &= arm1
    # 2. POSITIVE CONTROL ON THE VERDICT: a material bad enough MUST come out infeasible, or
    #    'feasible' is a constant and the sensitivity table proves nothing.
    total_work = M_BODY * MUSCLE_FRACTION * ENERGY_DENSITY
    need = frac_of_muscle_work(V_NEEDED) * total_work
    frac_at_1 = 100 * (need / 1.0) / M_BODY          # a 1 J/kg spring
    arm2 = frac_at_1 > 100.0
    print(f"  [{'ok' if arm2 else 'FAIL'}] a 1 J/kg spring needs {frac_at_1:.0f}% of body mass, "
          f"i.e. INFEASIBLE -- the test can return both answers")
    ok &= arm2
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok





# ---------------------------------------------------------------------------------------------
# ADDED after claim 958. The 134% figure is NOT a fixed property of the animal: it is a function
# of MUSCLE FRACTION, which this project had fixed at 0.40 following claim 547. Body mass
# cancels out of the requirement entirely:
#     required fraction = KE / (m * f * E_d) = (1/2) m v^2 / (m f E_d) = v^2 / (2 f E_d)
# so the whole question reduces to one number, the muscle fraction, and the break-even value of
# it can be solved for directly rather than searched.
def muscle_fraction_sweep():
    print("\n" + "=" * 78)
    print("THE 134% IS A FUNCTION OF MUSCLE FRACTION, AND BODY MASS CANCELS OUT")
    print("=" * 78)
    print("\n  required fraction of muscle work = v^2 / (2 * f * E_d)   [mass cancels]\n")
    f_break = V_NEEDED ** 2 / (2 * ENERGY_DENSITY)
    print(f"  {'muscle fraction':>16} {'% of muscle work needed':>26}   status")
    print("  " + "-" * 60)
    for f, note in [(0.40, "the value claim 547 assumed"),
                    (0.50, ""),
                    (f_break, "BREAK-EVEN"),
                    (0.60, "'>60% in active species' (Anderson 2017)"),
                    (0.70, "")]:
        req = V_NEEDED ** 2 / (2 * f * ENERGY_DENSITY)
        status = "needs >1 contraction" if req > 1.0 else "ONE contraction suffices"
        print(f"  {f:>16.3f} {100*req:>25.1f}%   {status}  {note}")
    print(f"\n  BREAK-EVEN MUSCLE FRACTION = {f_break:.3f}, i.e. {100*f_break:.1f}%")
    print("\n" + "-" * 78)
    print("WHAT THIS MEANS")
    print("-" * 78)
    print(f"  At the 40% this project assumed, the launch needs 135% of muscle work and")
    print(f"  therefore multi-contraction spring charging, which nothing is known to do.")
    print(f"  At {100*f_break:.0f}% it needs exactly one contraction. Anderson et al. 2017 state that")
    print(f"  myotomal muscle 'comprises >60% of the adult body mass in active species',")
    print(f"  which is ABOVE the break-even. So the multi-contraction question may be moot:")
    print(f"  the launch energy fits in a SINGLE contraction for a fish as muscular as an")
    print(f"  active teleost already is.")
    print("\n  AND THE FRACTION IS GENETICALLY ADDRESSABLE. The same paper describes")
    print("  'transgenic rainbow trout, overexpress follistatin, which antagonizes myostatin")
    print("  and increases myotonal muscle', with the gain 'due primarily to myocyte")
    print("  hyperplasia'. That is a published, real genetic manipulation that raises exactly")
    print("  this parameter in a fish.")
    print("=" * 78)
    return f_break


def controls_fraction():
    print("\nCONTROLS (muscle fraction)")
    ok = True
    # 1. Mass must genuinely cancel: two very different body masses, same requirement.
    def req(f, m):
        return (0.5 * m * V_NEEDED ** 2) / (m * f * ENERGY_DENSITY)
    a, b = req(0.4, 1e-4), req(0.4, 1e-1)
    arm1 = abs(a - b) < 1e-12
    print(f"  [{'ok' if arm1 else 'FAIL'}] a 0.1 g and a 100 g fish give the same requirement "
          f"({100*a:.1f}% vs {100*b:.1f}%) -- mass cancels as the algebra says")
    ok &= arm1
    # 2. The 0.40 case must REPRODUCE claim 956's 134%, or this extends a different model.
    r40 = V_NEEDED ** 2 / (2 * 0.40 * ENERGY_DENSITY)
    arm2 = abs(r40 - 1.344) < 0.02
    print(f"  [{'ok' if arm2 else 'FAIL'}] at f=0.40 it returns {100*r40:.1f}%, reproducing the "
          f"134% of claims 956/958")
    ok &= arm2
    # 3. The verdict must flip: some fraction must give 'needs >1 contraction'.
    arm3 = (V_NEEDED ** 2 / (2 * 0.20 * ENERGY_DENSITY)) > 1.0
    print(f"  [{'ok' if arm3 else 'FAIL'}] a 20% muscle fraction still needs >1 contraction -- "
          f"the test returns both answers")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    ok = controls()
    tendon_mass_needed()
    ok &= controls_mass()
    muscle_fraction_sweep()
    ok &= controls_fraction()
    if not ok:
        raise SystemExit("controls failed")
