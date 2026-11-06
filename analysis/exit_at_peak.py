#!/usr/bin/env python3
"""Can a zebrafish be AT its peak speed when it breaks the surface? A geometry question, answered.

Claim 546 identified the binding question: S901 uses Demesmay 2025's INSTANTANEOUS PEAK of
1.57 m/s as the water-exit speed, but that peak arrives 8 ms into the escape, during the C-bend.
If the fish is not at the surface at 8 ms it exits slower, and the required fin area swings from
4.4x to 28.4x -- a sixfold change from this one point of geometry.

The question is answerable WITHOUT new data, from the three numbers Demesmay reports for the same
trials: peak 1.57 m/s, latency to peak 8 +/- 4 ms, and 3.8 cm covered in 40 ms. Those pin a speed
profile tightly enough to ask how far the fish has travelled when it is fastest.

MODEL: a linear rise from rest to the peak at t_peak, then exponential decay. The decay constant
is not assumed -- it is SOLVED so the profile reproduces the measured 3.8 cm over 40 ms. So the
only free shape choice is "ramp then decay", and the script tests the alternative too.

Usage:  python3 exit_at_peak.py
"""
import math

V_PEAK = 1.57
T_PEAK = 0.008
T_TOT = 0.040
DIST_TOT = 0.038
BODY_L = 0.033


def distance(tau, t_peak=T_PEAK, shape="ramp"):
    """Distance over T_TOT for a rise to V_PEAK at t_peak then exp decay with constant tau."""
    if shape == "ramp":
        d_rise = 0.5 * V_PEAK * t_peak          # linear rise from 0
    else:                                        # instant-on: fastest possible early travel
        d_rise = V_PEAK * t_peak
    d_decay = V_PEAK * tau * (1.0 - math.exp(-(T_TOT - t_peak) / tau))
    return d_rise + d_decay


def solve_tau(shape="ramp"):
    lo, hi = 1e-4, 1.0
    if distance(hi, shape=shape) < DIST_TOT:
        return None
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if distance(mid, shape=shape) >= DIST_TOT:
            hi = mid
        else:
            lo = mid
    return hi


def main() -> int:
    print(f"  Demesmay 2025, same trials: peak {V_PEAK} m/s at {T_PEAK*1000:.0f} ms, "
          f"{DIST_TOT*100:.1f} cm in {T_TOT*1000:.0f} ms\n")
    for shape, lab in (("ramp", "linear rise to peak (realistic)"),
                       ("instant", "instant-on at peak (fastest possible early travel)")):
        tau = solve_tau(shape)
        if tau is None:
            print(f"  {lab}: no decay constant reproduces the measured distance")
            continue
        d_at_peak = (0.5 if shape == "ramp" else 1.0) * V_PEAK * T_PEAK
        print(f"  {lab}")
        print(f"    decay constant solved to {tau*1000:.1f} ms so the profile gives "
              f"{distance(tau, shape=shape)*100:.2f} cm (target {DIST_TOT*100:.1f})")
        print(f"    DISTANCE TRAVELLED WHEN FASTEST: {d_at_peak*100:.2f} cm "
              f"= {d_at_peak/BODY_L:.2f} body lengths\n")

    tau = solve_tau("ramp")
    d_at_peak = 0.5 * V_PEAK * T_PEAK
    print(f"  THE ANSWER: to be at peak speed when it breaks the surface, the fish must BEGIN its")
    print(f"  escape with the relevant body point about {d_at_peak*100:.1f} cm below the surface --")
    print(f"  {d_at_peak/BODY_L:.2f} of a body length. Not at an arbitrary depth: at that one.\n")

    print(f"  WHAT HAPPENS IF IT STARTS DEEPER, which is the quantity S901 actually needs:")
    print(f"  {'start depth':>12} {'exit speed':>11} {'as BL/s':>9}")
    for depth_cm in (0.6, 1.0, 2.0, 3.3, 5.0):
        d = depth_cm / 100.0
        # integrate the solved profile until the distance equals the start depth
        t, x, dt = 0.0, 0.0, 1e-5
        v = 0.0
        while x < d and t < T_TOT:
            v = (V_PEAK * t / T_PEAK) if t < T_PEAK else V_PEAK * math.exp(-(t - T_PEAK) / tau)
            x += v * dt
            t += dt
        reached = x >= d
        print(f"  {depth_cm:>10.1f} cm {v if reached else float('nan'):>10.2f} m/s "
              f"{(v/BODY_L) if reached else float('nan'):>8.1f}"
              + ("" if reached else "   never reaches this depth in 40 ms"))

    print(f"\n  CONTROL: the solved profile must reproduce the MEASURED distance, and does "
          f"({distance(tau)*100:.2f} vs {DIST_TOT*100:.1f} cm).")
    print(f"  A profile that did not would be a free-floating story about a fast-start.")
    print(f"\n  READING. The window is narrow but it is not implausible -- a zebrafish startled")
    print(f"  just under the surface is at 0.6 cm. What this rules out is the IMPLICIT assumption")
    print(f"  that peak speed is simply available at exit: it is available only from one depth,")
    print(f"  and from 2 cm down the fish is already past its peak and slowing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
