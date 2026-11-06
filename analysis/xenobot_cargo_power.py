#!/usr/bin/env python3
"""S925-S928: what fraction of a ciliated xenobot's power goes into pushing cargo?

NOT ALREADY ANSWERED BY THE PROJECT'S TWO NEIGHBOURING STUDIES, which is worth stating because
both sound like they might be. `cargo-work.json` is a DRY-FRICTION Voxelyze simulation of gaits
pushing a block -- a different physical regime. `regime-check.json` establishes that the real
object sits at Re < 0.1 and that five of six published gaits are time-reciprocal and therefore
dead there, but it ranks GAITS; it does not apportion power between body and cargo.

THE RESULT IS A CLOSED FORM AND THAT IS THE INTERESTING PART. In Stokes flow the drag on a
sphere is F = 6*pi*mu*a*U, so the power to drag it at speed U is P = 6*pi*mu*a*U^2. If the bot
and the cargo move at the SAME speed -- which is what "pushing" means -- then

    P_cargo / P_body  =  a_cargo / a_body

The viscosity cancels. The speed cancels. The answer does not depend on how fast the bot swims,
what the fluid is, or how strong the cilia are: it is the radius ratio, and nothing else. So
S925's 5% bar and S928's 1% bar are both questions about geometry alone.
"""
from __future__ import annotations

import math

A_BODY_UM = 250.0          # ~500 um diameter xenobot, literature-reported
CARGO_DIAM_UM = (10.0, 30.0, 100.0)
SPEEDS_UM_S = (50.0, 200.0)
MU = 1.0e-3                # Pa s, water at 20 C


def stokes_power(a_um: float, u_um_s: float, mu: float = MU) -> float:
    a, u = a_um * 1e-6, u_um_s * 1e-6
    return 6.0 * math.pi * mu * a * u * u


def main() -> int:
    print(f"  body radius {A_BODY_UM:.0f} um; cargo diameters {CARGO_DIAM_UM} um;"
          f" speeds {SPEEDS_UM_S} um/s\n")
    print(f"  {'cargo dia':>10}{'a_cargo':>9}{'ratio a_c/a_b':>15}"
          + "".join(f"{'P_c/P_b @'+str(int(u)):>16}" for u in SPEEDS_UM_S))
    for d in CARGO_DIAM_UM:
        a = d / 2.0
        geo = a / A_BODY_UM
        row = "".join(f"{stokes_power(a,u)/stokes_power(A_BODY_UM,u):>16.4f}"
                      for u in SPEEDS_UM_S)
        print(f"  {d:>10.0f}{a:>9.1f}{geo:>15.4f}{row}")

    print("\n  The ratio is IDENTICAL at both speeds, to every digit, because U^2 and mu")
    print("  cancel. The power fraction is a_cargo/a_body and nothing else.")

    print("\n  ANSWERS")
    for bar, who in ((0.05, "S925/S926 (5% bar)"), (0.01, "S928 (1% bar)")):
        meets = [d for d in CARGO_DIAM_UM if (d / 2.0) / A_BODY_UM >= bar]
        smallest = 2.0 * bar * A_BODY_UM
        print(f"    {who}: met by cargo diameters {meets} um; the bar is crossed at a cargo "
              f"diameter of {smallest:.0f} um")
    print(f"    So over the literature range of 10-100 um cargo, S928's 1% bar is met by all "
          f"of it and S925's 5% bar by cargo above {2*0.05*A_BODY_UM:.0f} um diameter.")

    print("\n  CONTROLS")
    # 1. the ratio must be invariant to speed and viscosity, or the cancellation is not real
    a = CARGO_DIAM_UM[1] / 2.0
    r1 = stokes_power(a, 50.0) / stokes_power(A_BODY_UM, 50.0)
    r2 = stokes_power(a, 200.0) / stokes_power(A_BODY_UM, 200.0)
    r3 = (stokes_power(a, 50.0, mu=1.0) / stokes_power(A_BODY_UM, 50.0, mu=1.0))
    print(f"    ratio at 50 vs 200 um/s: {r1:.6f} vs {r2:.6f} "
          f"{'OK, identical' if abs(r1-r2) < 1e-12 else 'DIFFERS'}")
    print(f"    ratio at 1000x viscosity: {r3:.6f} "
          f"{'OK, identical' if abs(r1-r3) < 1e-12 else 'DIFFERS'}")
    # 2. a cargo the size of the body must give ratio 1
    r = stokes_power(A_BODY_UM, 50.0) / stokes_power(A_BODY_UM, 50.0)
    print(f"    cargo equal to the body gives ratio {r:.3f} (must be 1.000)")
    # 3. a vanishing cargo must give ~0, or the formula only ever returns large numbers
    r = stokes_power(1e-6, 50.0) / stokes_power(A_BODY_UM, 50.0)
    print(f"    a 2 nm cargo gives ratio {r:.3e} (must be ~0)")

    print("\n  WHAT THIS DOES NOT MODEL, and each would RAISE the cargo's share rather than")
    print("  lower it, so the answers above are conservative:")
    print("    * a WALL. Both S927 and the real setting have the bot near a surface, and wall")
    print("      correction raises drag on the nearer body -- the cargo, which is pushed along")
    print("      the floor -- more than on the bot.")
    print("    * CONTACT. Pushing is transmitted through contact, not through the fluid, and a")
    print("      real pile of loose particles dissipates in grain-grain friction too.")
    print("    * A SQUIRMER IS NOT A TOWED SPHERE. A ciliated swimmer's own dissipation is")
    print("      larger than 6*pi*mu*a*U^2 because the cilia drive a surface flow; that would")
    print("      lower the ratio. This is the one neglected term pointing the other way, and")
    print("      it is why these numbers are an estimate of the ORDER and not a measurement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
