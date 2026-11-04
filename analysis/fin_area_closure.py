#!/usr/bin/env python3
"""How much lifting area a 0.4 g zebrafish needs to stall at 2 m/s, and what that demands genetically.

S902 asks whether the area needed exceeds what genetic enlargement can REACH by more than 3x. Half
of that is a calculation and half is unmeasured, and the tool says which is which rather than
quietly supplying the missing half.

CONTROLS: the script reproduces two figures already in the claim graph before reporting anything
new -- claim 283's ~20 cm2 at CL 0.8, and claim 434's 19.1-fold shortfall at CL 0.6 -- and a
must-flag case shows the calculation is sensitive to CL at all. A script that agrees with the
graph because it cannot disagree is worth nothing.
"""
from __future__ import annotations

import math

RHO = 1.225      # kg/m^3, sea-level air
G = 9.81
M = 4.0e-4       # kg, 0.4 g adult
A_NOW = 1.4e-4   # m^2, ~1.4 cm^2 whole-body planform (claim 283)


def area_needed(v: float, cl: float, m: float = M) -> float:
    """Wing area for level flight at speed v: 0.5*rho*v^2*S*CL = m*g."""
    return 2.0 * m * G / (RHO * v * v * cl)


def main() -> int:
    print("  CONTROLS -- must reproduce figures already in the claim graph\n")
    a08 = area_needed(2.0, 0.8)
    ok1 = abs(a08 * 1e4 - 20.0) < 1.0
    print(f"    claim 283: ~20 cm2 at 2 m/s, CL 0.8   -> computed {a08*1e4:.2f} cm2   {'ok' if ok1 else '*** MISMATCH ***'}")
    a06 = area_needed(2.0, 0.6)
    fold = a06 / A_NOW
    ok2 = abs(fold - 19.1) < 0.6
    print(f"    claim 434: 19.1-fold shortfall at CL 0.6 -> computed {fold:.2f}x      {'ok' if ok2 else '*** MISMATCH ***'}")
    a_bad = area_needed(2.0, 2.0)
    ok3 = abs(a_bad * 1e4 - a06 * 1e4) > 5
    print(f"    must-flag: CL 2.0 must give a different area -> {a_bad*1e4:.2f} cm2   {'ok' if ok3 else '*** INSENSITIVE ***'}")
    if not (ok1 and ok2 and ok3):
        print("\n  CONTROLS FAILED -- reporting nothing further.")
        return 1

    print(f"\n  REQUIRED AREA at a 2 m/s stall, 0.4 g, CL 0.6: {a06*1e4:.1f} cm2")
    print(f"  Present whole-body planform:                   {A_NOW*1e4:.1f} cm2")
    print(f"  AREA factor required:                          {fold:.1f}x")
    print(f"  LINEAR factor, if enlargement is isometric:    {math.sqrt(fold):.2f}x")
    print("    (area scales as length^2, so the linear demand is the square root --")
    print("     this is the number to compare against a fin-LENGTH phenotype)")

    print("\n  SENSITIVITY -- the area demand against the inputs that are actually contested:")
    print(f"    {'CL':>5} {'v (m/s)':>9} {'area cm2':>10} {'x present':>11} {'linear x':>10}")
    for cl in (0.6, 0.8, 1.07):
        for v in (2.0, 2.5, 3.0):
            a = area_needed(v, cl)
            print(f"    {cl:5.2f} {v:9.1f} {a*1e4:10.1f} {a/A_NOW:11.1f} {math.sqrt(a/A_NOW):10.2f}")

    print("\n  WHAT THIS DOES NOT ANSWER, and S902 cannot be settled without it:")
    print("    The REACHABLE fin area is not recorded anywhere in this project. S5, the subproblem")
    print("    that would supply it, is OPEN with no answer. A search of the live claim graph for a")
    print("    fin-enlargement factor returns nothing. So the required side is a calculation and the")
    print("    reachable side is unmeasured, and the ratio S902 asks for cannot be formed.")
    print("    S902's own falsifier quotes 'a few cm2 even after a 2-3x enlargement' -- that figure")
    print("    came from the proposing model, NOT from this project's evidence, and must not be")
    print("    used as though it had.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
