#!/usr/bin/env python3
"""Sobol variance decomposition of the coral bleaching model's four thermal-tolerance knobs.

Answers coral subproblems S918 and S920: does any single knob reach a first-order Sobol index
of at least 0.5 for degree-heating-weeks to bleaching, and are the interaction terms small?

WHY THIS AND NOT THE TEST ALREADY DONE. `bleaching_dynamics.py` already reports an additivity
test -- adjusted R^2 of main effects against main effects plus two-way terms. That asks whether
a linear-plus-interaction surrogate FITS. A Sobol decomposition asks how the model's OUTPUT
VARIANCE is apportioned, which is the question the routes actually pose: four routes each claim
to raise thermal tolerance by moving one knob, and the design needs to know whether one knob
dominates or whether they only work together.

THE DUMMY PARAMETER IS THE CONTROL. A fifth variable is sampled over a comparable range and
passed NOWHERE -- the model never sees it. Its first-order index must come out near zero. Any
sensitivity method can produce confident-looking indices from noise; a dummy that scores like a
real knob says the estimator, the sample size, or the readout is wrong. This is the standard
check for exactly that, and it is why the number of real knobs reported below can be trusted.

The model is a port of Cunning, Muller, Gates & Nisbet 2017 (J Theor Biol 431:49-62, PMID
28782552), with the thermal coupling added by that file and flagged there. NOTHING HERE IS A
MEASUREMENT OF A CORAL: this is a sensitivity analysis OF A SIMULATION, and the claim it
supports is about the model, not about the reef.
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np

CODE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "results", "coral", "code")
sys.path.insert(0, CODE)
import bleaching_dynamics as bd  # noqa: E402

N = 256                 # base sample; evaluations = N * (2k + 2)
DUMMY = "dummy_unused"


def saltelli(bounds: list[tuple[float, float]], n: int, seed: int = 20261105):
    """Saltelli sample: returns A, B and the k matrices AB_i."""
    rng = np.random.default_rng(seed)
    k = len(bounds)
    lo = np.array([b[0] for b in bounds])
    hi = np.array([b[1] for b in bounds])
    A = lo + (hi - lo) * rng.random((n, k))
    B = lo + (hi - lo) * rng.random((n, k))
    ABs = []
    for i in range(k):
        AB = A.copy()
        AB[:, i] = B[:, i]
        ABs.append(AB)
    return A, B, ABs


def sobol(yA: np.ndarray, yB: np.ndarray, yABs: list[np.ndarray]):
    """First-order and total-order indices (Saltelli 2010 / Jansen estimators)."""
    var = np.var(np.concatenate([yA, yB]), ddof=1)
    s1, st = [], []
    for yAB in yABs:
        s1.append(np.mean(yB * (yAB - yA)) / var)                 # Saltelli 2010
        st.append(0.5 * np.mean((yA - yAB) ** 2) / var)           # Jansen 1999
    return np.array(s1), np.array(st)


def main() -> int:
    ctrl = bd.control_arm()
    SH_ref = float(ctrl["SH_steady_state"])
    print(f"  control arm passed: {ctrl.get('passed')}   SH_ref = {SH_ref:.6f}")
    if not ctrl.get("passed"):
        print("  REFUSING: the model's own control arm did not pass; a sensitivity analysis "
              "of a model that fails its control measures nothing.")
        return 2

    names = list(bd.KNOBS) + [DUMMY]
    bounds = [(bd.KNOBS[k]["low"], bd.KNOBS[k]["high"]) for k in bd.KNOBS]
    # The dummy spans a comparable relative range so it is not trivially distinguishable.
    bounds.append((0.0, 1.0))
    print(f"  knobs: {names}")
    for n_, (lo, hi) in zip(names, bounds):
        print(f"    {n_:16} [{lo}, {hi}]")

    A, B, ABs = saltelli(bounds, N)
    mats = [A, B] + ABs
    total = sum(m.shape[0] for m in mats)
    print(f"\n  {len(mats)} matrices x {N} rows = {total} model evaluations")

    ys = []
    t0 = time.time()
    for j, M in enumerate(mats):
        grid = {k: M[:, i] for i, k in enumerate(bd.KNOBS)}   # the dummy column is NOT passed
        out = bd.thresholds(grid, SH_ref)
        y = np.asarray(out["dhw_host"], dtype=float)
        ys.append(y)
        print(f"    matrix {j+1}/{len(mats)} done ({time.time()-t0:.0f}s), "
              f"NaN {np.isnan(y).sum()}/{len(y)}", flush=True)

    # Censored members (never bleached) come back NaN. Replace with the maximum DHW tested,
    # which is the honest lower bound on their threshold, and report how many.
    cap = float(np.asarray(bd.thresholds({k: np.array([(bd.KNOBS[k]['low']+bd.KNOBS[k]['high'])/2])
                                          for k in bd.KNOBS}, SH_ref)["max_dhw_tested"]))
    ncens = sum(int(np.isnan(y).sum()) for y in ys)
    ys = [np.where(np.isnan(y), cap, y) for y in ys]
    print(f"  censored (never bleached) replaced with max DHW tested {cap:.2f}: "
          f"{ncens} of {total}")

    s1, st = sobol(ys[0], ys[1], ys[2:])
    print(f"\n  {'knob':16}{'S1':>9}{'ST':>9}   interaction (ST-S1)")
    for i, n_ in enumerate(names):
        print(f"  {n_:16}{s1[i]:9.3f}{st[i]:9.3f}{st[i]-s1[i]:>14.3f}"
              + ("   <- DUMMY, must be ~0" if n_ == DUMMY else ""))
    print(f"  {'sum':16}{s1.sum():9.3f}{st.sum():9.3f}")

    print("\n  CONTROLS")
    d = abs(s1[names.index(DUMMY)])
    biggest_real = max(abs(s1[i]) for i, n_ in enumerate(names) if n_ != DUMMY)
    print(f"    dummy S1 = {s1[names.index(DUMMY)]:+.3f}; largest real knob S1 = "
          f"{biggest_real:.3f}; ratio {d/max(biggest_real,1e-9):.3f} "
          f"{'OK' if d < 0.05 else 'DUMMY SCORES LIKE A REAL KNOB -- estimator or N is wrong'}")
    print(f"    sum of S1 = {s1.sum():.3f} (must be <= ~1 for a mostly additive model) "
          f"{'OK' if s1.sum() <= 1.15 else 'ABOVE 1'}")
    bad = [names[i] for i in range(len(names)) if st[i] + 1e-9 < s1[i]]
    print(f"    ST >= S1 for every parameter: {not bad} {bad if bad else ''}")

    print("\n  ANSWERS")
    top = int(np.argmax(s1[:-1]))
    print("    S918/S920 ask: does any single knob reach S1 >= 0.5?")
    print(f"      largest is {names[top]} at S1 = {s1[top]:.3f} -> "
          f"{'YES' if s1[top] >= 0.5 else 'NO'}")
    inter = st.sum() - s1.sum()
    print(f"      summed interaction (sum ST - sum S1) = {inter:.3f} -> "
          f"{'below 0.1' if inter < 0.1 else 'NOT below 0.1'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
