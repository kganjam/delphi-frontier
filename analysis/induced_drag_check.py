#!/usr/bin/env python3
"""Is CD = 0.1 the favourable end, or is it below what the physics allows?

Every trajectory result in this project -- claims 523, 543, 548, 549 -- uses CL 1.07 with a
LUMPED CD of 0.1, described as "the favourable end of every input" because the falsifier demands
it. But a lifting surface cannot choose its drag freely. A finite wing generating lift sheds
vortices and pays INDUCED drag:

    CD = CD0 + CL^2 / (pi * AR * e)

and that term grows as the SQUARE of the lift coefficient. At CL 1.07 on a low-aspect-ratio fish
fin it is not small. If it exceeds 0.1 on its own, then CD = 0.1 was not the favourable end of a
range -- it was below the floor, and every lift-attributable distance in this project is
overstated.

GROUND EFFECT RUNS THE OTHER WAY and is also absent. A body gliding close to a surface sheds
weaker vortices, reducing induced drag by a factor (1 - sigma) with the Wieselsberger/McCormick
form sigma = (1 - 1.32 h/b) / (1.05 + 7.4 h/b). A fish skimming the water is deep in it.

This computes both and reports whether the assumption was optimistic, and by how much. It
proposes no new trajectory result; it audits an input every existing one depends on.

Usage:  python3 induced_drag_check.py
"""
import math

CL = 1.07
CD_ASSUMED = 0.10
CD0 = 0.03          # profile drag of a thin membrane at Re ~4e3; the generous end
SPAN_M = 0.04       # fish body/fin span, order of a body length
AR_RANGE = (1.5, 3.0)   # a pectoral fin fan is LOW aspect ratio
E_RANGE = (0.7, 0.9)    # Oswald efficiency


def cd_induced(ar, e, cl=CL):
    return cl * cl / (math.pi * ar * e)


def sigma(h_over_b):
    """Wieselsberger/McCormick ground-effect factor; induced drag is multiplied by (1 - sigma)."""
    if h_over_b > 0.9:
        return 0.0
    return (1.0 - 1.32 * h_over_b) / (1.05 + 7.4 * h_over_b)


def main() -> int:
    print(f"  CL {CL}, lumped CD assumed everywhere in this project: {CD_ASSUMED}\n")
    print(f"  {'AR':>5} {'e':>5} {'CD_induced':>11} {'CD0+CDi':>9}  vs assumed")
    worst = 0.0
    for ar in AR_RANGE:
        for e in E_RANGE:
            cdi = cd_induced(ar, e)
            tot = CD0 + cdi
            worst = max(worst, tot)
            print(f"  {ar:>5.1f} {e:>5.2f} {cdi:>11.3f} {tot:>9.3f}  "
                  f"{tot/CD_ASSUMED:>4.1f}x the assumed value")
    print(f"\n  INDUCED DRAG ALONE exceeds the assumed TOTAL in every case. The CD of 0.1 was")
    print(f"  not the favourable end of a range; it is BELOW the physical floor for a finite")
    print(f"  wing at CL {CL}, by {worst/CD_ASSUMED:.1f}x at worst.\n")

    print(f"  GROUND EFFECT, which runs the other way (span {SPAN_M*100:.0f} cm):")
    print(f"  {'height':>8} {'h/b':>6} {'sigma':>7} {'CDi x':>7} {'CD0+CDi':>9}")
    best = 1e9
    for h_cm in (0.5, 1.0, 2.0, 4.0):
        hb = (h_cm / 100.0) / SPAN_M
        s = sigma(hb)
        cdi = cd_induced(AR_RANGE[1], E_RANGE[1]) * (1 - s)
        tot = CD0 + cdi
        best = min(best, tot)
        print(f"  {h_cm:>6.1f} cm {hb:>6.2f} {s:>7.3f} {1-s:>7.2f} {tot:>9.3f}")
    print(f"\n  Even skimming at 0.5 cm, the best total CD is {best:.3f} -- still "
          f"{best/CD_ASSUMED:.1f}x the assumed 0.1.")

    # CONTROL: at CL 0 the induced term must vanish and CD must fall to CD0.
    assert abs(cd_induced(2.0, 0.8, cl=0.0)) < 1e-12, "CONTROL FAILED: induced drag nonzero at zero lift"
    # THIS CONTROL WAS VACUOUS AND THE ADVERSARIAL PANEL CAUGHT IT. It asserted
    # sigma(2.0) == 0.0, which the h_over_b > 0.9 guard GUARANTEES -- so it tested the guard
    # and never the formula, and could not have failed. The raw form actually gives -0.1035 at
    # h/b 2.0, i.e. it would RAISE induced drag by 10% if applied there, which is exactly why
    # the clamp exists. The clamp is right; the control proved nothing. Now both are checked:
    # that the clamp fires, and that it fires on a value the formula would otherwise return.
    assert sigma(2.0) == 0.0, "CONTROL FAILED: the far-field clamp did not fire"
    raw = (1.0 - 1.32*2.0)/(1.05 + 7.4*2.0)
    assert raw < -0.05, (
        f"CONTROL FAILED: the raw form gives {raw:.4f} at h/b 2.0; if it were already ~0 the "
        "clamp would be untested and this assertion vacuous")
    assert sigma(0.12) > 0.4, "CONTROL FAILED: no ground effect where there should be a large one"
    print(f"\n  CONTROLS: induced drag is exactly 0 at CL 0, and ground effect is 0 at h/b 2.0.")

    print(f"\n  WHAT THIS MEANS. Every lift-attributable distance recorded in this project used a")
    print(f"  drag coefficient below what a finite wing at CL 1.07 can achieve, even in ground")
    print(f"  effect. Those figures are therefore OPTIMISTIC, and the 1.85x area gap is a LOWER")
    print(f"  BOUND on the shortfall rather than an estimate of it. This does not say by how much")
    print(f"  -- re-running the integrator with a CL-dependent CD is the next step and is not")
    print(f"  done here, because changing a shared input invalidates several recorded claims at")
    print(f"  once and that should be a deliberate pass, not a side effect of an audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
