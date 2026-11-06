#!/usr/bin/env python3
"""Bound burst speed from muscle WORK, which is better grounded than the power version it replaces.

analysis/burst_power_bound.py (claim 545) bounded exit speed from specific POWER, using a guessed
100-250 W/kg. Two findings from Sutton et al. 2019 (Integr Comp Biol, PMC6907395), surfaced by the
corpus figure sweep, improve on it and partly undercut it:

  1. IT SUPPLIES A PUBLISHED MUSCLE ENERGY DENSITY -- 15.0 J/kg, "consistent with the properties
     of bullfrog plantaris muscles" -- a measured quantity in place of my guessed power range.
  2. IT SAYS MY BOUND WAS OPTIMISTIC FOR AN ANIMAL THIS SIZE: "very small animals (weighing <1 g)
     produce less net work relative to their mass, they are unable to use a muscle-actuated system
     to jump as high as larger animals". A 0.4 g zebrafish is INSIDE that class, so force-velocity
     derating applies and the power bound ignored it entirely.

THE ENERGY BALANCE, which needs no power estimate at all:
    W_available = m_body * muscle_fraction * energy_density
    KE_exit     = 0.5 * m_body * v^2
    v = sqrt(2 * eta * muscle_fraction * energy_density)
where eta is the fraction of muscle work that becomes TRANSLATIONAL kinetic energy. In water most
of it does not: it goes into accelerating entrained fluid, into drag during the stroke, and into
body bending. eta is the honest unknown, and the script INVERTS for it rather than guessing --
reporting what efficiency each candidate speed demands.

Usage:  python3 burst_energy_bound.py
"""
import math

M_BODY = 4.0e-4
L = 0.033
MUSCLE_FRAC = (0.40, 0.60)
ENERGY_DENSITY = 15.0        # J/kg, Sutton et al. 2019, bullfrog plantaris

CANDIDATES = ((0.950, "Demesmay 40 ms average"),
              (1.570, "Demesmay instantaneous peak -- what S901 uses"),
              (1.790, "what the 2 cm threshold needs"))


def v_at(eta, frac):
    return math.sqrt(2.0 * eta * frac * ENERGY_DENSITY)


def eta_for(v, frac):
    return v * v / (2.0 * frac * ENERGY_DENSITY)


def main() -> int:
    print(f"  muscle energy density {ENERGY_DENSITY} J/kg (Sutton 2019), muscle fraction "
          f"{MUSCLE_FRAC[0]}-{MUSCLE_FRAC[1]}\n")
    for frac in MUSCLE_FRAC:
        print(f"    at muscle fraction {frac}: ideal v with eta=1 is {v_at(1.0, frac):.2f} m/s")
    print("    -- that is the frictionless ceiling and no animal reaches it\n")

    print(f"  {'speed':>7} {'BL/s':>6}   efficiency eta REQUIRED, by muscle fraction")
    print(f"  {'':>7} {'':>6}   {MUSCLE_FRAC[0]:>10}  {MUSCLE_FRAC[1]:>10}   reading")
    for v, lab in CANDIDATES:
        # Column order must match the header: MUSCLE_FRAC[0] first. More muscle needs LESS
        # efficiency, so the 0.4 column carries the HIGHER number. A first version printed these
        # swapped -- the values were right and sat under the wrong headings, which is the kind of
        # error that survives review because every individual number is correct.
        e_lo, e_hi = eta_for(v, MUSCLE_FRAC[0]), eta_for(v, MUSCLE_FRAC[1])
        worst = max(e_lo, e_hi)
        rd = ("modest" if worst < 0.25 else "demanding" if worst < 0.5 else
              "implausible in water" if worst < 1.0 else "IMPOSSIBLE")
        print(f"  {v:>7.3f} {v/L:>6.1f}   {e_lo:>10.1%}  {e_hi:>10.1%}   {rd}  <- {lab}")

    # CONTROL: the bound must call something impossible, or it constrains nothing.
    v_imp = v_at(1.0, MUSCLE_FRAC[1]) * 1.2
    assert eta_for(v_imp, MUSCLE_FRAC[1]) > 1.0, "CONTROL FAILED: bound admits everything"
    print(f"\n  CONTROL: {v_imp:.2f} m/s would need eta > 100% and is refused, so the bound "
          f"constrains something.")

    print(f"\n  READING. The speeds in play need {eta_for(0.95, 0.5):.0%} to "
          f"{eta_for(1.79, 0.5):.0%} of muscle work to arrive as translational KE at a muscle")
    print(f"  fraction of 0.5. None is impossible. For an aquatic burst, where most work goes "
          f"into the\n  water rather than the body, the upper end is demanding rather than "
          f"comfortable.")
    print(f"\n  AND THE CORRECTION TO CLAIM 545: that bound placed 1.57 m/s at the 27th percentile "
          f"of a power-\n  available band and called it comfortable. It used PEAK specific power "
          f"with no force-velocity\n  derating, which Sutton says is exactly wrong below 1 g -- "
          f"and this fish is 0.4 g. The energy\n  route needs no power figure and reaches a "
          f"soberer conclusion: available, not comfortable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
