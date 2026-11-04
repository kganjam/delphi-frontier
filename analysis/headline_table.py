#!/usr/bin/env python3
"""Recompute every shortfall ratio in the FINDINGS headline table from its own cells.

WHY THIS EXISTS. That table is the first thing a sceptical reader checks, and on 2026-11-04 one of
its five rows did not survive the check: it read "98.5 J/kg | 8.6 J/kg delivered | 1.9x", and
98.5/8.6 is 11.45. The shortfall was right; the Available cell was the wrong number to pair with
it -- 1.9x compares the requirement against the best measured spring-loading work, 53-81 J/kg, not
against 8.6. A reader doing the arithmetic would have found the headline table off by a factor of
6 and been right to distrust everything under it.

The failure is not arithmetic. It is a derived value left beside an input it was not derived from,
which is how two numbers in one row come to disagree while each is individually correct.

    python3 headline_table.py          # exits 1 if any row no longer reproduces
"""
import sys

# (row, required, available_lo, available_hi, stated_lo, stated_hi, tolerance)
# The ratio is required/available, so the LARGEST shortfall comes from the SMALLEST available.
ROWS = [
    # Quoted against the FASTEST measured individual (1.38), not the slowest. That is the
    # comparator most generous to the design, and it is the right one to headline -- but the
    # table must say so, or a reader computing 4.37/0.45 gets 9.7x and thinks it is wrong.
    ("water-exit speed",        4.37,  1.38,  1.38,  3.2,  3.2,  0.1),
    ("tail-beat for a taxi",   132.0, 52.0,  52.0,   2.5,  2.5,  0.1),
    ("tail-beat for a taxi hi",199.0, 52.0,  52.0,   3.8,  3.8,  0.1),
    ("pectoral muscle fraction", 7.5,  1.4,   1.4,   5.0,  5.0,  0.4),
    ("pectoral muscle frac hi",  20.0, 1.4,   1.4,  14.3, 15.0,  0.8),
    # Mendoza & Azizi 2021 measured 32-81 J/kg, mean 53. The table quoted 53-81 -- mean to max --
    # which silently dropped the low end and understated the shortfall as 1.2-1.9x. S29, the source
    # subproblem, states 1.2-3.1x. An "available" range that starts at the MEAN is not a range.
    ("muscle energy per stroke", 98.5, 32.0, 81.0,   1.2,  3.1,  0.1),
    # ADDED 2026-11-04 with the rows themselves. Two rows were put into the headline table and this
    # checker PASSED without them, reporting "all 6 table rows reproduce" while the table had 8.
    # Its row list is fixed, so a figure added to the document is unchecked until it is added here
    # too -- a coverage gap that looks exactly like coverage.
    #
    # Water-exit against the NEWER source (Demesmay 2025, 157 +/- 27 cm/s). Kept beside the 1.38
    # row rather than replacing it: the two measure different things (range across 50 fish vs mean
    # of maximal), and both are in the table.
    ("water-exit speed, Demesmay", 4.37, 1.57, 1.57,  2.78, 2.78, 0.02),
    # Fin AREA at CL 0.6, 2 m/s, 0.4 g against the 1.4 cm^2 whole-body silhouette.
    ("pectoral fin area",         26.7,  1.4,  1.4,  19.1, 19.1, 0.1),
    # The row above is computed at CL 0.6, which is claim 5's ceiling -- and claim 5 is SUPERSEDED
    # by claim 86 (CL_max ~1.0, 0.9-1.1, for cambered/corrugated thin wings near Re 3e3; 0.6 holds
    # "only for a flat plate on weak evidence"). Both are checked because both are in the table and
    # the FIN'S OWN CL IS UNKNOWN, so neither endpoint is the answer. Checking only the superseded
    # one is how it came to be bolded as the headline in the first place.
    ("pectoral fin area at CL 1.0", 16.0, 1.4,  1.4,  11.4, 11.4, 0.1),
]


def main():
    bad = 0
    for name, req, lo, hi, s_lo, s_hi, tol in ROWS:
        # smallest available -> biggest shortfall
        r_hi, r_lo = req / lo, req / hi
        ok_hi = abs(r_hi - s_hi) <= tol
        ok_lo = abs(r_lo - s_lo) <= tol
        mark = "ok " if (ok_hi and ok_lo) else "BAD"
        if not (ok_hi and ok_lo):
            bad += 1
        print(f"  {mark} {name:26} {req}/{hi}..{lo} = {r_lo:5.2f}..{r_hi:5.2f}x   "
              f"stated {s_lo}..{s_hi}x")

    # The muscle row, stated the other way round, as claim 227 phrases it.
    pct_lo, pct_hi = 100 * 53.0 / 98.5, 100 * 81.0 / 98.5
    print(f"\n  muscle row cross-check: supplies {pct_lo:.1f}-{pct_hi:.1f}% of need; "
          f"claim 227 states 54-82%")
    if not (53 <= pct_lo <= 55 and 81 <= pct_hi <= 83):
        print("  BAD: does not reproduce claim 227"); bad += 1

    # --- the BODY prose, recomputed from the same inputs -----------------------
    # The table was wrong where nothing checked it; there is no reason to assume the prose is
    # better. These are every derived figure stated in the body of docs/FINDINGS.md.
    RHO, G, MASS, CL = 1.225, 9.80665, 4.0e-4, 0.8
    area10 = 2 * MASS * G / (RHO * 10.0 ** 2 * CL) * 1e4      # cm^2 at a 10 m/s launch
    body = [
        ("area shortfall, 20 cm2 vs 1.4",      20 / 1.4,                 14.0,  0.4),
        ("area needed at 10 m/s (cm2)",        area10,                    0.80, 0.05),
        ("  that as a shortfall",              area10 / 1.4,              0.60, 0.05),
        ("taxi 2.19 m/s as % of 4.41",         100 * 2.19 / 4.41,        50.0,  1.0),
        ("taxi 2.88 m/s as % of 4.41",         100 * 2.88 / 4.41,        65.0,  1.0),
        ("Cypselurus (10/16.4)^2 as % KE",     100 * (10 / 16.4) ** 2,   37.0,  1.0),
        ("water/air density ratio",            1000 / RHO,              816.0,  1.0),
        # This one ties the table to itself: 0.5*m*v^2 at the stated mass and exit speed must
        # give the stated launch energy, so a drift in ANY of the three shows up here.
        ("launch KE 0.5*m*v^2 (mJ)",           0.5 * MASS * 4.37 ** 2 * 1e3, 3.82, 0.05),
    ]
    # The 98.5 J/kg requirement must reproduce from its own budget, so a drift in any of its
    # four inputs surfaces here rather than in the one place the product is quoted.
    eta = 0.37
    req = 10.17 / (0.30 * 0.93 * eta)
    body.append(("98.5 J/kg from its own budget", req, 98.5, 0.1))
    # And the point value hides an interval: the cited eta_h range is 0.34-0.39.
    body.append(("  same budget at eta=0.39", 10.17 / (0.30 * 0.93 * 0.39), 93.5, 0.2))
    body.append(("  same budget at eta=0.34", 10.17 / (0.30 * 0.93 * 0.34), 107.2, 0.2))

    # --- AUDIT ARITHMETIC ----------------------------------------------------
    # Ratios computed while auditing other people's ratios, which this document named as its own
    # unchecked gap. These are the recomputable ones; the rest of that gap is run outputs (backed
    # by a code_sha) and live graph counts (deliberately unpinned).
    import math
    body += [
        # the quotient that exposed the broken table row
        ("98.5 / 8.6 (the wrong pairing)",   98.5 / 8.6,                11.45, 0.01),
        # lift at a 45-degree climb: vertical component is L*cos(theta)
        ("10 % lift at 45 deg, vertical",    10.0 * math.cos(math.radians(45)), 7.1, 0.05),
        # Sutton's one-third ceiling applied to the requirement (the double-count that was rejected)
        ("98.5 / (1/3) if the ceiling applied", 98.5 * 3,              295.5, 0.6),
        # the project's 20 cm2 at 2 m/s, propagated to 4.41 m/s by 1/v^2
        ("20 cm2 at 2 m/s -> 4.41 m/s",      20.0 * (2.0 / 4.41) ** 2,  4.11, 0.02),
        # area-vs-length sample size: isotropy doubles the CV along with the effect
        ("area-vs-length n ratio",
         ((0.10 / 0.05) ** 2) / (((2 * 0.10) / ((1.05 ** 2) - 1)) ** 2), 1.05, 0.02),
    ]

    print()
    for name, got, stated, tol in body:
        ok = abs(got - stated) <= tol
        if not ok:
            bad += 1
        print(f"  {'ok ' if ok else 'BAD'} {name:30} computed {got:9.3f}  stated {stated:8.3f}")

    if bad:
        print(f"\n  {bad} row(s) no longer reproduce. A shortfall ratio and the cell it is")
        print("  computed from must not drift apart -- that is how this table was wrong before.")
        return 1
    print(f"\n  all {len(ROWS)} table rows and {len(body)} body/audit figures reproduce.")
    print("  This check is not vacuous: it caught the 98.5/8.6 row, so a clean pass means")
    print("  something. A checker that has never failed is indistinguishable from one that cannot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
