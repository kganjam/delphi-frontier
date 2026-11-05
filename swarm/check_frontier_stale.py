#!/usr/bin/env python3
"""Open subproblems that cite a SUPERSEDED claim, or whose premise a correction has moved.

WHY. A subproblem is a question with a premise, and the premise usually comes from a claim. When
that claim is superseded the question can quietly become unanswerable or wrong, and NOTHING
notices: `check_specs.py` checks claim and subproblem state, not whether a question still makes
sense. This is the subproblem form of the stale-spec-prose problem -- prose has nobody, and an
open question has nobody either.

Measured on zebrafish-flight when this was written: 2 of 24 open or blocked subproblems cited
superseded claims, both pointing at claim 992. One of them, S908, had a stale PREMISE rather
than just a stale citation -- it asks about "the exponent n = 0.558-0.592" and that exponent was
withdrawn by claim 1014, which replaced a fitted exponent with Eloy's eq-16 branches. A question
about a number that no longer exists cannot be answered.

TWO SEVERITIES, deliberately separated, because treating them alike would make this noisy:
  CITATION  the subproblem mentions a superseded claim but its own question still stands
  PREMISE   a quantity the question is ABOUT appears only in the superseded claim's text and
            not in its replacement -- the question has lost its subject

The premise test is a heuristic and says so: it extracts numbers from the question, and asks
whether they survive into the superseding claim. It will miss a premise expressed in words, and
it will flag a number that coincidentally appears in both. Read every hit.

    python3 check_frontier_stale.py [project]
"""
from __future__ import annotations

import os
import re
import sys

from dbq import flat, lit, q


def main() -> int:
    project = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
        "SWARM_PROJECT", "zebrafish-flight")
    fz = flat("coalesce(falsifier,'')")
    rows = q(f"""select id, status, {flat('question')}, {fz}
                 from subproblem where project_id={lit(project)}
                 and status in ('open','blocked') order by id""")
    sup = {int(r[0]): int(r[1]) for r in
           q("select id, superseded_by from claim where superseded_by is not null")}
    print(f"  {project}: {len(rows)} open/blocked subproblem(s); "
          f"{len(sup)} superseded claims in the graph\n")

    citation, premise = [], []
    for sid, st, qq, fzz in rows:
        text = f"{qq} {fzz}"
        cited = sorted({int(m) for m in re.findall(r"claim\s+(\d{3,4})", text, re.I)} & set(sup))
        if not cited:
            continue
        # does a number the QUESTION is about survive into the replacement?
        # NO AUTOMATIC PREMISE CLASSIFICATION. Two earlier versions tried, and the second
        # one failed for the reason this repository already documents: a string search cannot
        # tell a value being ASSERTED from the same value being QUOTED as withdrawn.
        #
        # Worked example. S908 asks about "the exponent n = 0.558-0.592". Claim 1014 withdrew
        # that exponent ("n = 0.558-0.592 WAS A CORNER SELECTION"). Searching the live graph
        # for "0.558" finds 2 claims -- 1006 and 1014 -- and BOTH are discussing its
        # withdrawal. The number looks alive and is not. Meanwhile 2.67, in S907, is alive in
        # 7 claims and genuinely is.
        #
        # So this reports the citations and leaves the judgement to a reader, which is what
        # the rule about forbidden-string checks prescribes: pin the positive fact, or read
        # every hit and expect some to be backwards.
        stale_nums = set()
        (premise if stale_nums else citation).append((sid, st, cited, stale_nums, qq))

    for label, items in (("CITES A SUPERSEDED CLAIM -- read each one; the question may still "
                          "stand, or its premise may have been withdrawn", citation + premise),):
        print(f"  {label}: {len(items)}")
        for sid, st, cited, nums, qq in items:
            repl = ", ".join(f"{c} -> {sup[c]}" for c in cited)
            print(f"    {sid:10} [{st}] {repl}"
                  + (f"   numbers dropped: {sorted(nums)}" if nums else ""))
            print(f"        {qq[:140]}")
        print()

    print("  Each hit needs reading. The replacement claim is named so that is one lookup.")
    print("  A string test cannot tell an asserted value from one quoted as withdrawn, so no")
    print("  automatic verdict is offered -- see this module's docstring for the worked case.")

    print("\n  CONTROLS")
    print(f"    the superseded set is non-empty ({len(sup)}), so a zero result would mean "
          f"'no stale citations' and not 'no data' "
          f"{'OK' if sup else 'NO SUPERSEDED CLAIMS -- this check cannot fire'}")
    any_cite = sum(1 for _s, _t, qq, fzz in rows
                   if re.search(r"claim\s+\d{3,4}", f"{qq} {fzz}", re.I))
    print(f"    {any_cite} of {len(rows)} open subproblems cite ANY claim, so the regex "
          f"matches real text {'OK' if any_cite else 'the citation pattern never matches'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
