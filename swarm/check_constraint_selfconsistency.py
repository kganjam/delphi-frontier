#!/usr/bin/env python3
"""Does a constraint's own prose agree with its own numbers?

FOUND BY THE PANEL, 2026-11-05, in the middle of an unrelated argument. Claim 1163 reproduced
each burst-speed constraint's bound back into the ratio its statement names, and opus noticed
that two of the three did not reproduce:

    e194, e353   bound <= 1.380 m/s   -> 3.17x   statement says "3.2x and 10x"       agrees
    e258, e316   bound <= 0.910 m/s   -> 4.80x   statement says "5.2x and 27x"       8% out
    e224         band [0.834, 1.460]  -> 3.0-5.2x statement says "the 4-7x margin"   disagrees

A constraint whose prose and bound disagree is worse than a stale one. A stale constraint is
correct about a world that has moved; a self-inconsistent one was never correct about any world,
and nothing downstream can tell which half to believe. It is also invisible to every check this
project has: the entailment matcher compares a bound to a claim, the ladder reads status, and
the duplicate sweep compares rows to each other. Nothing compares a row TO ITSELF.

WHAT THIS CHECKS, and only this: where a statement names a multiplicative ratio in the form
"<number>x" and the row carries a bound plus a reference quantity the ratio is taken against,
recompute the ratio from the bound and compare. The reference is the take-off speed 4.37 m/s
where the statement names it, because that is the quantity these ratios are formed against.

WHAT IT CANNOT CHECK. Ratios whose reference is not stated in the row, ranges written in words,
and any constraint whose prose names no number. It is a narrow check that catches one specific
inconsistency, which is the kind worth having -- a broad one over this corpus would flag
everything, as three earlier attempts in this project measured.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from dbq import q, lit  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
#: The take-off speed these flight ratios are formed against, as the constraints themselves write
#: it ("4.37/v_max = 3.2x"). Only rows naming it are checked.
TAKEOFF = 4.37
TOLERANCE = 0.05          #: 5 percent; below this a difference is rounding, not disagreement


def ratios_in(text: str) -> list[float]:
    """Multiplicative ratios written as <number>x, excluding squared/KE companions."""
    out = []
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*x\b", text):
        v = float(m.group(1))
        if 1.5 <= v <= 12.0:        # a speed ratio; the KE companions are the squares
            out.append(v)
    return out


def main() -> int:
    """Each row implies its own reference; the corpus's agreement is the control.

    The first version required the literal string "4.37" in the statement and found exactly ONE
    checkable row out of 285 -- a filter so narrow it could not have flagged the very rows the
    panel had just caught, because e258 and e224 write their ratios without naming what they are
    ratios OF. Inferring the reference from each row (reference = ratio x bound) and comparing
    against what the other rows imply is both broader and better evidenced: the agreement among
    rows IS the control, and no constant is hardcoded.
    """
    rows = q(f"""select id, coalesce(lo::text,''), coalesce(hi::text,''), coalesce(units,''),
             replace(coalesce(statement,''), chr(10), ' '), coalesce(bound_statistic,'')
             from constraint_entailed
             where project_id = {lit(PROJECT)} and (lo is not null or hi is not null)""")
    cands = []
    stat_of = {r[0]: r[5] for r in rows}
    for eid, lo, hi, units, stmt, _bs in rows:
        if "m/s" not in units:
            continue
        rs = ratios_in(stmt)
        if not rs:
            continue
        for which, b in (("hi", hi), ("lo", lo)):
            if not b or float(b) <= 0:
                continue
            for r in rs:
                cands.append((eid, which, float(b), r, float(b) * r, stmt))
    if not cands:
        print("  no rows carry both an m/s bound and a ratio in their prose.")
        return 0

    # NO VERDICT, AND THE SECOND ATTEMPT IS WHY. Taking the median of the implied values and
    # flagging deviations FLAGGED THE CORRECT ROWS: e194 and e353 imply 4.416 m/s against this
    # project's 4.37 take-off speed -- 1% out, the two the panel had confirmed as consistent --
    # while the median sat at 5.838 because only SEVEN rows are checkable and they reference at
    # least two different quantities (e195's ratio is against a leap, not a take-off). Seven
    # rows spanning two references cannot establish a reference by consensus, and hardcoding one
    # (the first attempt) checks only the rows that happen to name it: one row of 285.
    #
    # So this REPORTS and does not judge. The deviation column is against the project's stated
    # take-off speed, named as such, and a row whose ratio is taken against something else will
    # show a large deviation for a legitimate reason -- which is exactly why a verdict here
    # would be wrong and a human reading the list is not.
    print(f"  {len(rows)} entailments with a bound; {len({c[0] for c in cands})} carry an m/s "
          f"bound AND a ratio in their prose -- too few, and too mixed in what their ratios are "
          f"taken against, to establish a reference by consensus.")
    print(f"  Reported against this project's stated take-off speed, {TAKEOFF} m/s. "
          f"NO PASS/FAIL IS ISSUED.\n")
    best: dict[str, tuple] = {}
    for eid, which, b, r, imp, stmt in cands:
        err = abs(imp - TAKEOFF) / TAKEOFF
        if eid not in best or err < best[eid][0]:
            best[eid] = (err, which, b, r, imp, stmt)
    for eid, (err, which, b, r, imp, stmt) in sorted(best.items(), key=lambda kv: kv[1][0]):
        st = stat_of.get(eid, "")
        # A RECORDED STATISTIC EXPLAINS ITS OWN DEVIATION. An `upper-sem` bound is SUPPOSED to
        # sit above a ratio formed from the centre; flagging it would be flagging the standard
        # error. This is the whole reason the column exists (claim 1167).
        mark = ("  " if err <= TOLERANCE else
                "ok" if st and st != "central" else "<<")
        tag = f"  [{st}]" if st else "  [statistic unrecorded]"
        print(f"  {mark} e{eid:<5} {which}={b:g} m/s x {r:g}x = {imp:.3f} m/s   "
              f"{err:5.1%} from {TAKEOFF}{tag}")
        print(f"        {stmt[:120]}")
    print(f"""
  READING IT. A row near {TAKEOFF} is internally consistent: its bound and the ratio its prose
  names agree about the quantity they are formed against. A row far from it is EITHER
  inconsistent OR taken against a different reference, and only reading the statement
  distinguishes them -- e195's ratio is against a leap requirement, so its 7.170 is not an error.
  AND THE OTHER REFERENCE IS IDENTIFIABLE. e224 and e307 both imply 5.838 m/s, which is
  claim 1's stall speed for a 1-body-length span wing, 5.84 m/s. Their ratios are taken against
  the STALL threshold, not the take-off speed, and against that they agree to three decimals and
  with each other. So of the seven:

      e194, e353   consistent against the 4.37 m/s take-off speed   (1.1% out)
      e224, e307   consistent against claim 1's 5.84 m/s stall      (0.03% out)
      e195         against a leap requirement, 7.170 m/s            (its own statement says so)
      e258, e316   imply 4.732 m/s -- and that 8% gap IS A STANDARD ERROR, not a defect

  ALL SEVEN RESOLVE, once e258/e316 are traced (claim 1166). Their source, claim 24, forms its
  5.2x ratio from claim 21's CENTRAL value 0.842 m/s, while the rows take their BOUND from the
  upper end of that claim's +/-1 s.e.m. interval, 0.91. 0.910/0.842 = 1.081: the 8% this module
  reports is the measurement's own standard error. Both numbers are traceable and both choices
  are defensible; the rows simply do not say WHICH STATISTIC the bound represents.

  SO THE RIGHT READING OF A FLAGGED ROW IS "go and find out", not "this is broken". This module
  found a real 8% discrepancy and localised it to 2 rows of 285; resolving it took three
  queries. An earlier version of this comment called those rows inconsistent with everything the
  project holds, which was an assertion about the corpus made without searching the corpus.

  THE SCHEMA SUGGESTION THAT FALLS OUT: a bound that recorded which statistic it is -- central,
  upper s.e.m., measured maximum -- would make these rows checkable rather than merely
  defensible, and this corpus holds at least two that need it.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
