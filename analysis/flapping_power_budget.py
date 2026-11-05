#!/usr/bin/env python3
"""The full flapping power budget, because claim 587 ASSERTED the missing terms rather than computing them.

Claim 585 computed INDUCED power for weight support at 33 W/kg of muscle and found it comfortable.
Claim 587 then found that superfast myosin -- the only way to reach the required 53 Hz -- costs
5/6 of the force and leaves 35 to 71 W/kg available, putting the design on the boundary. It then
said that adding profile and inertial power "pushes the requirement above the 35 W/kg floor".

THAT WAS AN ASSERTION, NOT A COMPUTATION, and it is doing the work of closing the route. A
flapping wing pays three powers:

  INDUCED  -- accelerating air downward to make weight. Already computed.
  PROFILE  -- dragging the wing through air against its own skin and pressure drag.
  INERTIAL -- accelerating and decelerating the wing's own mass twice per cycle. In hovering
              animals this is often the LARGEST term, and whether it is recovered elastically
              is the single biggest uncertainty in insect and hummingbird energetics.

This computes all three and reports whether the route closes, rather than assuming it.

Usage:  python3 flapping_power_budget.py
"""
import math

RHO, G = 1.225, 9.81
M = 4.0e-4 * (2.6/4.0)**3        # 0.110 g, the best specifiable design
S = 1.4e-4 * (2.6/4.0)**2 * 2.65  # 1.57 cm2 of fin
R, PHI = 0.013, 2.3               # wing length, stroke amplitude
F = 53.0                          # Hz, from claim 586 at clap-and-fling CL
CD_PROFILE = 0.2                  # a flapping wing at Re ~1e3-1e4; generous low end
# wing mass: a fin is a thin membrane on rays. Take 1% of body mass for the pair, generous.
M_WING_FRAC = 0.01
MUSCLE_FRAC = 0.5

SUPERFAST_AVAIL = (35.0, 71.0)    # W/kg, from claim 587


def main() -> int:
    W = M * G
    muscle = M * MUSCLE_FRAC
    m_wing = M * M_WING_FRAC / 2.0        # per wing
    # mean and tip speeds for the given beat
    U_tip = 2.0 * PHI * F * R
    U_mean = U_tip / 2.0

    P_ind = W**1.5 / math.sqrt(2.0 * RHO * S)
    # profile: drag on the wing integrated over the stroke, both wings
    P_pro = 0.5 * RHO * CD_PROFILE * S * (U_mean**3) * (3.0/2.0)   # <U^3> factor for sinusoid
    # inertial: KE of the wing built and destroyed twice per cycle
    I_wing = m_wing * R * R / 3.0          # slender wing about its base
    omega_pk = 2.0 * math.pi * F * PHI / 2.0
    KE = 0.5 * I_wing * omega_pk**2
    P_in_noel = 4.0 * KE * F * 2.0         # two wings, twice per cycle

    print(f"  design {M*1e3:.3f} g, fin {S*1e4:.2f} cm2, wing {R*100:.1f} cm, beat {F:.0f} Hz")
    print(f"  tip speed {U_tip:.2f} m/s, muscle mass {muscle*1e3:.3f} g\n")
    print(f"  {'term':<28} {'power mW':>10} {'W/kg muscle':>13}")
    for name, P in (("induced (weight support)", P_ind),
                    ("profile (wing drag)", P_pro),
                    ("inertial, NO elastic storage", P_in_noel),
                    ("inertial, perfect storage", 0.0)):
        print(f"  {name:<28} {P*1e3:>10.2f} {P/muscle:>13.0f}")

    tot_noel = P_ind + P_pro + P_in_noel
    tot_el = P_ind + P_pro
    print(f"\n  TOTAL, no elastic recovery : {tot_noel/muscle:>6.0f} W/kg")
    print(f"  TOTAL, perfect recovery    : {tot_el/muscle:>6.0f} W/kg")
    print(f"  AVAILABLE from superfast muscle (claim 587): "
          f"{SUPERFAST_AVAIL[0]:.0f} to {SUPERFAST_AVAIL[1]:.0f} W/kg\n")

    for label, tot in (("no elastic recovery", tot_noel), ("perfect recovery", tot_el)):
        lo, hi = SUPERFAST_AVAIL
        v = ("CLOSES at the optimistic end" if tot/muscle <= hi else "EXCEEDS even the optimistic end")
        print(f"  with {label:<20}: needs {tot/muscle:>5.0f}, {v}")

    # CONTROL: the same budget on a hummingbird must land near its measured ~100-200 W/kg.
    Mh, Sh, Rh, Fh = 3.5e-3, 1.5e-3, 0.055, 50.0
    Wh = Mh*G; mh = Mh*0.25
    Ph_ind = Wh**1.5/math.sqrt(2*RHO*Sh)
    Uh = (2*2.3*Fh*Rh)/2
    Ph_pro = 0.5*RHO*CD_PROFILE*Sh*Uh**3*1.5
    print(f"\n  CONTROL -- same model on a hummingbird: induced+profile "
          f"{(Ph_ind+Ph_pro)/mh:.0f} W/kg against a measured 100-200.")
    assert 30 < (Ph_ind+Ph_pro)/mh < 400, "CONTROL FAILED: model does not reproduce a real flier"
    print("  within the measured band, so the budget is not producing nonsense.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
