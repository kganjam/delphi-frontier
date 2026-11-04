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
    ("muscle energy per stroke", 98.5, 53.0, 81.0,   1.2,  1.9,  0.1),
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

    if bad:
        print(f"\n  {bad} row(s) no longer reproduce. A shortfall ratio and the cell it is")
        print("  computed from must not drift apart -- that is how this table was wrong before.")
        return 1
    print(f"\n  all {len(ROWS)} rows reproduce from their own cells.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
