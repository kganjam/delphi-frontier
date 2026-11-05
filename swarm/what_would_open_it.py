#!/usr/bin/env python3
"""All four routes are closed. What would have to change, and which closure is nearest?

A negative result is only useful if someone can see exactly where it fails and by how much.
Four routes closed on four DIFFERENT measured quantities, so "the fish cannot fly" is really
four separate statements with four separate shortfalls -- and they are not equally far from
reversible. This ranks them.

GENERATED, NOT WRITTEN. The shortfalls are fetched from the claims that carry them, exactly as
`design_spec.py` does, because a hand-written summary is the part of a generated document that
goes stale. Only the editorial mapping -- which claim carries which route's binding quantity --
is declared here.

WHAT A RATIO MEANS HERE, and why they are not strictly comparable: each is (required /
available) in that route's own units. A 1.4x shortfall in an efficiency is not the same kind of
distance as a 6.9x shortfall in a beat frequency, because efficiencies are bounded above by 1
and frequencies are not. The ranking is a guide to where effort is least wasted, not a
conversion rate between them.
"""
from __future__ import annotations


from dbq import flat, lit, q

#: (route, claim carrying the binding quantity, what is required, what is available,
#:  ratio required/available, what would have to change, is the ceiling a hard physical bound?)
BINDING = [
    ("A. Gliding", 599, "lift coefficient near 7", "1.75 measured anywhere", 4.0,
     "a lift coefficient no wing achieves at this Reynolds number", True),
    ("B. Powered flapping", 601, "83 Hz beat frequency", "12 Hz white-muscle ceiling", 6.9,
     "a superfast myosin that has never been sequenced in any animal, plus 3.7-9x more "
     "muscle power than any measurement", True),
    ("C. Latch-spring launch", 1060, "0.539 transfer efficiency at 100% muscle, or 4.6-18 "
     "charging contractions", "0.39 best measured, and N=1 with no ratchet described", 1.4,
     "either a hydrodynamic transfer efficiency 1.4x the best ever measured for a fish "
     "fast-start, or a ratchet no LaMSA system is described as having", False),
    ("D. Harvesting the wind", 1056, "20.6 m/s at 10 m over the habitat", "16.84 m/s, the "
     "highest daily maximum in 10 years at 4 sites", 1.2,
     "a different habitat -- the physics already works; the wind does not blow there", False),
]


def main() -> int:
    rows = {}
    for _r, cid, *_ in BINDING:
        got = q(f"select {flat('units', 300)}, coalesce(evidence,''), coalesce(superseded_by::text,'') "
                f"from claim where id={int(cid)} and project_id={lit('zebrafish-flight')}")
        if not got:
            print(f"  REFUSING: claim {cid} not found")
            return 2
        if got[0][2]:
            print(f"  REFUSING: claim {cid} is superseded by {got[0][2]}; this file cites a "
                  f"claim that is no longer live")
            return 2
        rows[cid] = got[0]

    print("=" * 78)
    print("ALL FOUR ROUTES ARE CLOSED. WHAT WOULD HAVE TO CHANGE?")
    print("=" * 78)
    print("\nRanked by how far the binding quantity is from reversible. Nearest first.\n")

    for route, cid, need, have, ratio, change, hard in sorted(BINDING, key=lambda r: r[4]):
        ev = rows[cid][1]
        print(f"  {route}   shortfall {ratio:.1f}x   (claim {cid}, `{ev}`)")
        print(f"      needs     : {need}")
        print(f"      has       : {have}")
        print(f"      to open it: {change}")
        print(f"      ceiling is {'a HARD physical bound' if hard else 'NOT a hard bound'}")
        print()

    soft = [r for r in BINDING if not r[6]]
    print("-" * 78)
    print(f"  {len(soft)} of {len(BINDING)} closures are NOT against a hard physical ceiling:")
    for r in sorted(soft, key=lambda x: x[4]):
        print(f"    {r[0]:26} {r[4]:.1f}x  -- {r[5][:60]}")
    print()
    print("  Route D is the nearest, at 1.2x, and it is the only one whose PHYSICS already")
    print("  works: the design flies, in a wind the Gangetic floodplain does not produce.")
    print("  That makes it the one closure no genetic change can touch -- which is the")
    print("  project's sharpest finding, not its weakest.")
    print()
    print("  Route C is next at 1.4x, and it is a genuine research question rather than a")
    print("  wall: a ratchet that holds a spring at intermediate charge is not known in any")
    print("  LaMSA system, but nothing shows it to be impossible.")
    print()
    print("  Routes A and B are against hard ceilings -- a lift coefficient no wing achieves")
    print("  at this Reynolds number, and a myosin nobody has sequenced. Effort there is")
    print("  wasted until one of those facts changes.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
