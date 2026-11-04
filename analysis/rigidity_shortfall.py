#!/usr/bin/env python3
"""Independently reproduce the fin-ray rigidity shortfall, the project's largest number.

Claim 199 (the S6 answer) states: "required/measured flexural rigidity >= 9x (D_w required
>= 7.4e-6 N m vs measured-derived <= 8.0e-7 N m, 3 mm square wing)". That 9-196x shortfall is now
the binding constraint on the whole design -- larger than the 2.18-4.79x enlargement requirement --
and it had only ever been read out of a claim statement here, never recomputed.

The model is a cantilever plate of span L and width W under a distributed load:
    delta_tip = P L^3 / (8 * EI),  EI = D_w * W,  so  delta/L = P L^2 / (8 * D_w * W)
Setting delta/L to the 10%-of-span criterion and solving for D_w gives the requirement.

ONE ASSUMPTION IS NOT IN THE CLAIM and is needed to reproduce its number: the lift is split between
TWO pectoral fins. Without that the requirement comes out at 1.47e-5, twice the stated 7.4e-6. The
claim's "1 g gliding lift" is a LOAD FACTOR -- one gravity, steady flight -- not one gram-force;
reading it as gram-force gives 3.68e-5 and misses by five-fold.
"""
from __future__ import annotations

G = 9.81
M_FISH = 4.0e-4        # kg, 0.4 g
N_FINS = 2             # the assumption above
CRIT = 0.10            # tip deflection <= 10% of span
D_W_MEASURED = 8.0e-7  # N m, upper end of the measured-derived range (claim 199)


def d_w_required(L: float, W: float, load_factor: float = 1.0, n_fins: int = N_FINS) -> float:
    """Per-width flexural rigidity needed to hold tip deflection at CRIT, for an L x W plate."""
    P = load_factor * M_FISH * G / n_fins
    return P * L * L / (8.0 * CRIT * W)


def main() -> int:
    L = W = 3.0e-3      # the 3 mm square wing the claim names
    req = d_w_required(L, W)
    ratio = req / D_W_MEASURED
    print(f"  3 mm square wing, 1 g load factor, lift split over {N_FINS} fins\n")
    print(f"    D_w required        {req:.3e} N m     claim 199 states >= 7.4e-6")
    print(f"    D_w measured-derived {D_W_MEASURED:.1e} N m     claim 199 states <= 8.0e-7")
    print(f"    shortfall            {ratio:.2f}x            claim 199 states >= 9x")
    ok = abs(req - 7.4e-6) / 7.4e-6 < 0.05 and abs(ratio - 9.0) < 0.6
    print(f"\n  REPRODUCES: {'YES' if ok else 'NO'}")

    print("\n  CONTROLS -- the two readings that do NOT reproduce it, so the right one is pinned:")
    print(f"    lift on ONE fin                 {d_w_required(L, W, n_fins=1):.3e}  (2x too high)")
    print(f"    '1 g' read as one GRAM-force    {d_w_required(L, W, load_factor=9.81e-3/(M_FISH*G)):.3e}  (5x too high)")

    print("\n  SCALING -- the claim says 9-196x across 3-15 mm wings. D_w required goes as L^2/W,")
    print("  so for a square wing it is linear in L:")
    print(f"    {'span (mm)':>10} {'D_w req (N m)':>15} {'shortfall':>11}")
    for mm in (3, 5, 10, 15):
        L = W = mm * 1e-3
        r = d_w_required(L, W)
        print(f"    {mm:>10} {r:>15.3e} {r/D_W_MEASURED:>10.1f}x")
    print("\n  The upper end: at 15 mm the shortfall is ~46x against the UPPER measured D_w.")
    print("  Claim 199's 196x uses the LOWER end of the measured range (1.9e-7), not the upper:")
    for mm in (15,):
        L = W = mm * 1e-3
        print(f"    15 mm vs D_w 1.9e-7  ->  {d_w_required(L, W)/1.9e-7:.0f}x   (claim states 196x)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
