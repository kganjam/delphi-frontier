#!/usr/bin/env python3
"""Does a claim's headline assert more than its own body supports?

MEASURED, FIVE TIMES IN ONE SESSION (2026-11-05). Each of these claims was superseded, and in
every case the BODY was already careful and the HEADLINE was not:

    1121  headline "the shortfall is in frequency rather than in power"
          body     "its power at 53 Hz is necessarily LOWER and is not measured"
    1154  headline "THE BASELINE AMBIGUITY IS RESOLVED"
          body     "1.4e-4 is an UNSOURCED CONSTANT ... if it means something else this moves"
    1160  headline "the honest figure is 1.6-2.2x ... invariant"
          body     the range IS the k-dependence, and a second parameter spans 1.60-4.20
    1179  headline "stacking CANNOT close it"
          body     "'a second fin-overgrowth allele adds nothing' is not 'no second allele can'"
    1182  headline "strictly better for a glider"
          body     (no hedge -- and this project's own e53 says the medial fins do the taxiing)

FOUR OF FIVE CARRY THE REFUTATION IN THEIR OWN TEXT. The writer knew; the title did not. That is
a checkable shape: a headline containing an ABSOLUTE, beside a body containing a HEDGE about the
same subject.

WHAT IT CANNOT DO, said plainly because this project has three dead checkers that could not say
it. It cannot tell whether a hedge REFERS to the headline's claim -- a claim may legitimately
assert one thing absolutely and hedge another. So it reports pairs for a person, it never blocks,
and the 1182 case shows the floor: a headline can overreach with no hedge anywhere, and nothing
textual will catch that one. It scores four of the five known cases, and the fifth is a reminder
that the instrument is partial.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from dbq import q, lit  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

#: Words that assert something settled, closed or universal.
ABSOLUTE = ("cannot", "can not", "resolved", "settled", "closed", "strictly", "invariant",
            "proves", "proven", "establishes", "established", "refutes", "refuted", "never",
            "always", "no point", "nothing", "only", "impossible", "definitive")
#: Words that admit the opposite in the same text.
HEDGE = ("not measured", "unmeasured", "unsourced", "untested", "not shown", "does not show",
         "is not evidence", "may be", "might", "unknown", "not established", "cannot be sure",
         "would need", "has not been", "nobody has", "not verified", "unverified",
         "insufficient", "is not ", "not been tested", "depends on")


def headline_and_body(stmt: str) -> tuple[str, str]:
    m = re.match(r"\s*\[([^\]]+)\]", stmt or "", re.S)
    if m:
        return " ".join(m.group(1).split()), stmt[m.end():]
    first = (stmt or "").split(".")[0]
    return " ".join(first.split()), (stmt or "")[len(first):]


def main() -> int:
    only = [a for a in sys.argv[1:] if a.isdigit()]
    where = f"and id in ({','.join(only)})" if only else "and superseded_by is null"
    rows = q(f"""select id, replace(coalesce(statement,''), chr(10), ' ')
             from claim where project_id = {lit(PROJECT)} {where} order by id desc limit 400""")
    flagged = []
    for cid, stmt in rows:
        head, body = headline_and_body(stmt)
        hl, bl = head.lower(), body.lower()
        abs_hits = [w for w in ABSOLUTE if w in hl]
        hedge_hits = [w for w in HEDGE if w in bl]
        if abs_hits and hedge_hits:
            flagged.append((cid, head, abs_hits, hedge_hits))
    print(f"  {len(rows)} claims examined; {len(flagged)} have an ABSOLUTE in the headline and a "
          f"HEDGE in the body\n")
    for cid, head, a, h in flagged[:12]:
        print(f"  claim {cid}  headline says {','.join(a[:3])};  body says {','.join(h[:3])}")
        print(f"     {head[:120]}")
    if len(flagged) > 12:
        print(f"  ... and {len(flagged)-12} more")
    print("""
  READ EVERY HIT. This cannot tell whether the hedge is ABOUT the headline's assertion, and a
  claim may rightly assert one thing and hedge another. It reports; it never blocks.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
