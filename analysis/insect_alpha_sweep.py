#!/usr/bin/env python3
"""S923: is the four-wing-vs-two-wing result robust to the mid-stroke angle of attack?

Claim 1051 corrected the JUSTIFICATION for the model's 45-degree angle of attack. The file said
45 degrees "makes the baseline arm as generous as the model allows, which biases the comparison
AGAINST the claim that four wings help". It does not: the angle is declared ONCE in
model.parameters, none of the five configurations overrides it, and the wild-type arm is
normalised to lift/weight = 1 by construction, so the choice is absorbed. The choice is NEUTRAL,
not conservative.

That corrected the reasoning and left the empirical question open, which is what S923 asks: with
the angle swept, does the RANKING of configurations change, and does the normalised four-wing
ratio move more than 10%?

THE CALIBRATION MUST MOVE WITH THE ANGLE. CL_MAX is the model's one fitted parameter, chosen so
the two-wing arm produces exactly body weight AT 45 DEGREES. Sweeping the angle without
recalibrating would make the baseline drift away from 1 and the "normalised" ratio would then be
measuring the drift. Both are computed below, because the difference between them is the whole
reason claim 1051's correction mattered.
"""
from __future__ import annotations

import os
import sys

import numpy as np

CODE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "results", "insect-flight", "code")
sys.path.insert(0, CODE)
import flight_performance as fp  # noqa: E402

DEGREES = list(range(30, 61, 5))
BASE = 45


def configs_at(alpha_deg: float, recalibrate: bool):
    fp.ALPHA_MID = np.deg2rad(alpha_deg)
    fp.CL_MAX = fp.calibrate_cl_max() if recalibrate else CL_AT_45
    return {c["name"]: c for c in fp.build_configs()}


CL_AT_45 = fp.CL_MAX
NAMES = [c['name'] for c in fp.build_configs()]


def main() -> int:
    print(f"  sweeping mid-stroke angle of attack {DEGREES[0]}-{DEGREES[-1]} deg "
          f"(model default {BASE})\n")
    for recal in (True, False):
        lbl = ("RECALIBRATED at each angle (the model's own convention: the wild type is the "
               "calibration arm)" if recal else
               "NOT recalibrated -- CL_MAX held at its 45-degree value")
        print(f"  --- {lbl} ---")
        names = None
        rows = {}
        for d in DEGREES:
            c = configs_at(d, recal)
            names = names or list(c)
            rows[d] = {n: c[n]["lift_over_weight"] for n in names}
        hdr = "  " + "deg".rjust(5) + "".join(f"{n[:17]:>19}" for n in names)
        print(hdr)
        for d in DEGREES:
            print("  " + f"{d:>5}" + "".join(f"{rows[d][n]:>19.4f}" for n in names))

        # S923's two questions
        wt = "two_wing_wild_type"
        four = [n for n in names if n.startswith("four_wing")]
        print()
        for n in four:
            base = rows[BASE][n] / rows[BASE][wt]
            worst = max(abs((rows[d][n] / rows[d][wt]) / base - 1.0) for d in DEGREES)
            print(f"    {n:28} normalised ratio at {BASE} deg = {base:.4f}; "
                  f"worst deviation across the sweep {100*worst:5.1f}% "
                  f"{'within 10%' if worst <= 0.10 else 'EXCEEDS 10%'}")
        order0 = sorted(names, key=lambda n: -rows[BASE][n])
        changed = [d for d in DEGREES if sorted(names, key=lambda n: -rows[d][n]) != order0]
        print(f"    ranking at {BASE} deg: {' > '.join(x[:16] for x in order0)}")
        print(f"    angles where the ranking differs: {changed if changed else 'none'}")
        print()

    print("  CONTROLS")
    fp.ALPHA_MID = np.deg2rad(BASE)
    fp.CL_MAX = fp.calibrate_cl_max()
    c = {x["name"]: x for x in fp.build_configs()}
    wt = c["two_wing_wild_type"]["lift_over_weight"]
    print(f"    the calibration arm returns to 1.0 at {BASE} deg: {wt:.6f} "
          f"{'OK' if abs(wt-1.0) < 1e-6 else 'DRIFTED -- module state not restored'}")
    # the sweep must actually change something, or 'robust' is meaningless
    a = configs_at(30, False)["two_wing_wild_type"]["lift_over_weight"]
    b = configs_at(45, False)["two_wing_wild_type"]["lift_over_weight"]
    print(f"    without recalibration the angle DOES move the baseline: "
          f"{a:.4f} at 30 deg vs {b:.4f} at 45 "
          f"{'OK' if abs(a-b) > 0.01 else 'the sweep changes nothing -- patch not taking effect'}")
    # and with recalibration it must not
    a = configs_at(30, True)["two_wing_wild_type"]["lift_over_weight"]
    print(f"    with recalibration the baseline is pinned at 1: {a:.6f} "
          f"{'OK' if abs(a-1.0) < 1e-6 else 'NOT PINNED'}")
    fp.ALPHA_MID = np.deg2rad(BASE)
    fp.CL_MAX = fp.calibrate_cl_max()
    return 0




def power_sweep() -> int:
    """The lift ratio is angle-invariant by construction. Is the POWER ratio?

    Lift goes as CL_MAX*sin(2a) for every wing, so a shared angle cancels exactly from any
    lift ratio -- which is why the sweep above reads 0.0% and not merely "within 10%". Drag
    does NOT share that form: cd_of_alpha = CD_0 + (CD_MAX-CD_0)*(1-cos(2a))/2. So power, which
    carries the drag term, is the place where the angle could still matter, and claim 1051
    flagged exactly this when it noted that 45 degrees is not the generous end if drag counts.
    """
    print("\n  POWER, where the angle does NOT cancel")
    print(f"  {'deg':>5}" + "".join(f"{n[:17]:>19}" for n in NAMES))
    base = None
    worst = {}
    for d in DEGREES:
        c = configs_at(d, True)
        p = {n: c[n]["mass_specific_power_W_per_kg"] for n in NAMES}
        if d == BASE:
            base = dict(p)
        print(f"  {d:>5}" + "".join(f"{p[n]:>19.2f}" for n in NAMES))
    for d in DEGREES:
        c = configs_at(d, True)
        for n in NAMES:
            r = c[n]["mass_specific_power_W_per_kg"] / c["two_wing_wild_type"]["mass_specific_power_W_per_kg"]
            r0 = base[n] / base["two_wing_wild_type"]
            worst[n] = max(worst.get(n, 0.0), abs(r / r0 - 1.0))
    print()
    for n in NAMES:
        print(f"    {n:28} power ratio vs wild type, worst deviation "
              f"{100*worst[n]:5.1f}% {'within 10%' if worst[n] <= 0.10 else 'EXCEEDS 10%'}")
    print("\n    Absolute power rises steeply with the angle (drag goes as 1-cos(2a)), but the")
    print("    RATIO between configurations is what the four-wing claim rests on.")
    fp.ALPHA_MID = np.deg2rad(BASE)
    fp.CL_MAX = fp.calibrate_cl_max()
    return 0


if __name__ == "__main__":
    main()
    raise SystemExit(power_sweep())
