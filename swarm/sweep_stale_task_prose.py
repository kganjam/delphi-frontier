#!/usr/bin/env python3
"""Find subproblem prose quoting a number that a later claim corrected.

WHY THIS EXISTS. Claim 1082: subproblem S907 asks about "the 2.67x pectoral fin AREA effect",
which reads as a measured area. It is a derived FLOOR -- (2.09 linear)^(1.33 exponent lower
bound) -- and claim 1003 corrected that reading four claims before S907 was written. Nothing
noticed, because a task's question text has no caller, no test and no checker. AGENTS.md section
2 records this failure for specs/; this is the same failure inside the task table.

DELIBERATELY NOT A GATE, and AGENTS.md says why: a prose matcher cannot tell quoting from
claiming, or asserting from denying, and a check with that false-positive rate gets switched
off. This is a sweep to run by hand after a batch of landings, and every hit must be read.

THE DOMAIN IS NARROW ON PURPOSE. It does not flag every number in every subproblem. It flags a
number that appears BOTH in open/unanswered subproblem prose AND in a claim that announces
itself as a correction. That intersection is small enough to read, which is the only property
that makes a sweep survive.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env, flat  # noqa: E402

#: A claim that says it is correcting something. Anchored on this project's own phrasings.
CORRECTION = re.compile(r"\b(CORRECTS?|CORRECTION TO|SUPERSEDES|REFINES|OVERSTATED|"
                        r"I READ A|WAS OVERCONFIDENT)\b", re.I)
#: Numbers worth comparing: a decimal with a fractional part. Bare integers are far too common.
#: NOT `\b\d+\.\d+\b`. That was the first version and its must-flag control caught it: a
#: trailing \b needs a NON-word character after the digits, so "2.67x" does not match -- "x" is
#: a word character. This project writes nearly every fold change that way ("2.67x", "4.4x"), so
#: the pattern was blind to exactly the numbers it exists to find, while still matching
#: "12.5 m/s" because of the space. It reported 33 hits and looked like it was working.
NUMBER = re.compile(r"(?<![\d.])\d+\.\d+(?![\d.])")


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.strip().split("\n") if ln]


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    subs = q(f"select id, {flat('question', 1200)} from subproblem "
             f"where project_id = '{proj}'")
    claims = q(f"select id::text, {flat('statement', 4000)} from claim "
               f"where project_id = '{proj}' and superseded_by is null")
    corrections = [(c[0], c[1]) for c in claims if len(c) > 1 and CORRECTION.search(c[1])]
    print(f"  {len(subs)} subproblems, {len(claims)} live claims, "
          f"{len(corrections)} announcing a correction\n")

    hits = 0
    for sid, question in ((s[0], s[1]) for s in subs if len(s) > 1):
        nums = set(NUMBER.findall(question))
        for n in sorted(nums):
            # `n in stmt` is WRONG and its own output proved it: "0.5" matches inside
            # "20.5 percent", so S911 was flagged against an unrelated claim. The NUMBER
            # pattern has word boundaries; the COMPARISON must have them too.
            nre = re.compile(r"(?<![\d.])" + re.escape(n) + r"(?![\d])")
            for cid, stmt in corrections:
                if nre.search(stmt):
                    hits += 1
                    where = nre.search(stmt).start()
                    print(f"  {sid} quotes {n}; claim {cid} corrects something mentioning it")
                    print(f"      subproblem: ...{question[max(0,question.index(n)-70):question.index(n)+70]}...")
                    print(f"      claim {cid}: ...{stmt[max(0,where-90):where+90]}...\n")
                    break
    print(f"  {hits} intersections to READ BY HAND. A hit is not a defect: the subproblem may")
    print("  already reflect the correction, or quote the number for a different purpose.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
