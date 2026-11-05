#!/usr/bin/env python3
"""Resolve the fin-area lever with RANDOM search instead of a grid.

Claim 981 withdrew the fin-area numbers: at 27 controllers and again at 200, the sweep of fin
area against minimum sustaining wind came back NON-MONOTONIC while wing loading fell throughout,
which wing-loading theory forbids. It named the instrument: "an optimiser over the controller
parameters, or a closed-loop law with fewer free parameters, not a finer grid."

WHY RANDOM SEARCH AND NOT A FINER GRID. A grid aliases: it samples the same lattice at every fin
size, so a controller that works for 2x fin may fall between its lines while one for 1.5x lands
on them. That produces exactly the non-monotonicity observed. Random sampling draws independently
at every fin size and has no lattice to alias against, so the comparison across fin sizes becomes
fair even if no single search is exhaustive.

WHAT IS STILL TRUE AFTER THIS RUNS: a minimum-wind figure remains a NEGATIVE dressed as a
measurement -- the lowest wind at which the search happened to find something -- which is claim
981's own lesson. What random search buys is that the negatives are now drawn the same way at
every fin size, so their ORDERING is meaningful even where their values are not.
"""
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import closed_loop as cl  # noqa: E402

N_SAMPLES = 400        # per (fin size, wind) cell, drawn independently
SEED = 11


def search(us, n=N_SAMPLES, rng=None):
    """Return the number of sustaining controllers found in n random draws."""
    rng = rng or random.Random(SEED)
    hits = []
    for _ in range(n):
        vt = rng.uniform(2.0, 18.0)
        kb = rng.uniform(0.3, 4.0)
        zt = rng.uniform(0.3, 4.0)
        if cl.fly(us, vt, kb, zt)["aloft"]:
            hits.append((vt, kb, zt))
    return hits


def main():
    base_S = cl.S
    winds = (0.25, 0.32, 0.40, 0.50, 0.60, 0.75)
    print("=" * 78)
    print("FIN LEVER BY RANDOM SEARCH -- 400 independent draws per cell")
    print("=" * 78)
    print(f"\n  grid search gave: 12.5, 10.4, 12.5, 8.3, 10.4 m/s (non-monotonic)")
    print(f"  wing loading falls monotonically, so that ordering was noise\n")
    print(f"  {'fin x':>7} {'loading':>12} {'min wind found':>16} {'hits at that wind':>18}")
    print("  " + "-" * 60)
    rows = []
    for mult in (1.0, 1.5, 2.0, 3.0, 4.0):
        cl.S = base_S * mult
        wl = (cl.M * 9.81) / cl.S
        rng = random.Random(SEED + int(mult * 10))
        found = None
        for us in winds:
            hits = search(us, rng=rng)
            if hits:
                found = (us, len(hits))
                break
        if found:
            w = cl.wind(1.0, found[0])
            rows.append((mult, wl, w))
            print(f"  {mult:>6.1f}x {wl:>10.2f} N/m2 {w:>14.1f} m/s {found[1]:>13} of 400")
        else:
            rows.append((mult, wl, None))
            print(f"  {mult:>6.1f}x {wl:>10.2f} N/m2 {'none to 15.6':>16} {'0':>18}")
    cl.S = base_S

    print("\n" + "-" * 78)
    mono = all(rows[i][2] is not None and rows[i + 1][2] is not None
               and rows[i + 1][2] <= rows[i][2] + 1e-9
               for i in range(len(rows) - 1))
    print(f"  MONOTONIC (wind falls as fin area rises): {'YES' if mono else 'NO'}")
    if mono:
        print("  The lever is now resolved: the ordering matches wing-loading theory, so the")
        print("  numbers can be read as a trend rather than as noise.")
    else:
        print("  STILL NOT MONOTONIC. Random search has no lattice to alias against, so this")
        print("  is not a sampling-pattern artifact. Either 400 draws is too few, or the")
        print("  minimum-wind statistic itself is the wrong instrument for this question.")
    print("=" * 78)
    return rows


def controls():
    print("\nCONTROLS")
    ok = True
    base_S = cl.S
    # 1. no wind must find nothing, however many draws
    hits = search(0.0, n=100, rng=random.Random(1))
    arm1 = not hits
    print(f"  [{'ok' if arm1 else 'FAIL'}] 100 draws at ZERO wind find {len(hits)} sustaining "
          f"-- random search is not manufacturing flight")
    ok &= arm1
    # 2. strong wind must find plenty, or the sampler never hits the feasible region
    hits2 = search(1.20, n=100, rng=random.Random(2))
    arm2 = len(hits2) > 0
    print(f"  [{'ok' if arm2 else 'FAIL'}] 100 draws at 24.9 m/s find {len(hits2)} -- the "
          f"sampler reaches the feasible region")
    ok &= arm2
    # 3. more fin must never REDUCE the hit count at a fixed wind, within noise
    cl.S = base_S
    a = len(search(0.60, n=150, rng=random.Random(3)))
    cl.S = base_S * 3.0
    b = len(search(0.60, n=150, rng=random.Random(3)))
    cl.S = base_S
    arm3 = b >= a
    print(f"  [{'ok' if arm3 else 'FAIL'}] at a fixed 12.5 m/s, 3x fin finds {b} vs baseline "
          f"{a} on the SAME draws -- more fin does not help less")
    ok &= arm3
    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    main()
    if not controls():
        raise SystemExit("controls failed")
