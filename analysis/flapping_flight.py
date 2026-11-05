#!/usr/bin/env python3
"""Could a zebrafish FLAP its way into the air? The route every other analysis here assumed away.

Claims 523 through 584 all model a ballistic or gliding leap: the fish exits the water with a fixed
speed and a fixed-CL wing, and decelerates. The goal explicitly says not to copy the gliding flying
fish, and POWERED flapping is the other way a body gets into the air -- insects, birds and bats all
do it, and none of them needs a launch speed at all. It has never been evaluated here.

TWO INDEPENDENT REQUIREMENTS, AND BOTH ARE COMPUTABLE FROM NUMBERS ALREADY IN THE GRAPH:

  1. KINEMATIC -- the wing must move fast enough through the air to make weight in lift. That
     fixes a mean wing speed, and for a wing of given length a flapping frequency.
  2. ENERGETIC -- the muscle must supply the aerodynamic power at that frequency.

The kinematic one binds first and is the interesting one, because muscle CONTRACTION FREQUENCY is
a hard vertebrate limit rather than a soft one.

Usage:  python3 flapping_flight.py
"""
import math

RHO, G, CL = 1.225, 9.81, 1.07
# the best specifiable design (claims 580, 584): 2.6 cm young adult, 2.65x fin genetics
from geometry import MASS_KG as _M, S_LIFTING_M2 as _S  # noqa: E402  one definition; see analysis/geometry.py
M = _M                  # was: 4.0e-4 * (2.6/4.0)**3, re-typed alongside it
S = _S                  # was: 1.4e-4 * (2.6/4.0)**2 * 2.65, re-typed in 9 files
R = 0.013                           # m, wing (fin) length -- half a body length, generous
PHI = (2.0, 2.6)                    # rad, stroke amplitude: 115 to 150 degrees


def main() -> int:
    W = M * G
    print(f"  best specifiable design: {M*1e3:.3f} g, {S*1e4:.2f} cm2 of fin, wing length "
          f"{R*100:.1f} cm")
    print(f"  weight {W:.3e} N\n")

    # 1. KINEMATIC: mean wing speed for weight support
    U = math.sqrt(2.0 * W / (RHO * CL * S))
    print(f"  REQUIRED MEAN WING SPEED for lift = weight: {U:.2f} m/s")
    print(f"    (this is the WING's speed through air, not the body's -- flapping supplies it)\n")

    # a flapping wing's mean speed over the span is about half its tip speed
    U_tip = 2.0 * U
    print(f"  tip speed needed (mean over span is ~half the tip): {U_tip:.2f} m/s")
    print(f"\n  {'amplitude':>10} {'f needed':>10} {'vs vertebrate limits'}")
    for phi in PHI:
        f = U_tip / (2.0 * phi * R)
        note = ("ABOVE any vertebrate locomotor muscle" if f > 100 else
                "near the hummingbird/bat ceiling" if f > 50 else "attainable")
        print(f"  {math.degrees(phi):>8.0f}d {f:>9.0f} Hz  {note}")

    f_mid = U_tip / (2.0 * sum(PHI)/2 * R)
    print(f"\n  CONTEXT FOR THAT FREQUENCY, which is the binding constraint:")
    print(f"    hummingbird hovering          ~50 Hz")
    print(f"    the fastest bat wingbeats     ~15-20 Hz")
    print(f"    fastest vertebrate muscle of any kind (toadfish swimbladder,")
    print(f"      rattlesnake shaker) reaches ~100-250 Hz -- but those are SOUND-PRODUCING")
    print(f"      muscles that develop almost no force, not locomotor muscle")
    print(f"    required here                 ~{f_mid:.0f} Hz")

    # 2. ENERGETIC, for completeness: aerodynamic power at that speed
    # induced power for weight support, actuator-disk form
    P_ind = W**1.5 / math.sqrt(2.0 * RHO * S)
    muscle_mass = M * 0.5
    print(f"\n  ENERGETIC CHECK (actuator-disk induced power, the irreducible part):")
    print(f"    induced power {P_ind*1e3:.2f} mW, muscle mass {muscle_mass*1e3:.3f} g")
    print(f"    => {P_ind/muscle_mass:.0f} W/kg of muscle required")
    print(f"    hovering animals sustain roughly 100-200 W/kg; vertebrate burst peaks ~400")
    verdict = ("within reach" if P_ind/muscle_mass < 200 else
               "at the burst ceiling" if P_ind/muscle_mass < 400 else "beyond any muscle")
    print(f"    -> {verdict}")

    # CONTROL: a hummingbird must come out near its known wingbeat frequency.
    M_h, S_h, R_h = 3.5e-3, 1.5e-3, 0.055      # 3.5 g, 15 cm2 of wing, 5.5 cm wing
    U_h = math.sqrt(2.0 * M_h * G / (RHO * CL * S_h))
    f_h = (2.0 * U_h) / (2.0 * 2.3 * R_h)
    print(f"\n  CONTROL -- run the same model on a hummingbird (3.5 g, 15 cm2, 5.5 cm wing):")
    print(f"    predicts {f_h:.0f} Hz against a real ~50 Hz. Same order, so the model is not")
    print(f"    producing nonsense; a factor under 2 on a quasi-steady estimate is expected.")
    assert 20 < f_h < 120, "CONTROL FAILED: the model does not reproduce a known flier"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
