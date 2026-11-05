#!/usr/bin/env python3
"""How many unactioned 'weakened' verdicts actually warrant a correction? Measured, not written.

THE GAP THIS MEASURES. `project_structure.py` shows coral, insect-flight, xenobot and
limbless-mouse with 0 superseded claims between them, against 85 for the fish. They are not
unchallenged -- the adversarial arm ran and left 170 live claims carrying a `weakened` verdict.
It produced verdicts and nothing was ever written back, so the refinement half of the loop has
never run on those projects.

WHY THIS DOES NOT AUTO-CORRECT. Writing a superseding claim is an assertion about the world,
and the fish project's 85 supersessions each came from a person reading the attack and deciding.
Automating that would manufacture claims at exactly the rate the arm manufactures objections,
which is the confirmation-pressure failure `api_challenge.py` was built to avoid, pointed the
other way. So this ADJUDICATES ONLY: for each weakened claim it asks whether the attack is
correct AND actionable, in a closed vocabulary, and reports counts. Nothing is written to
`claim`.

The output is a work list with a size on it: if most attacks are not actionable, the 0
supersessions are honest; if most are, the projects owe 170 corrections.

    SWARM_PROJECT=coral python3 adjudicate.py 20
"""
from __future__ import annotations

import collections
import os
import re
import sys

import api_challenge as ac
from dbq import flat, lit, q

VERDICTS = ("ACTIONABLE", "MINOR", "WRONG")

PROMPT = """A scientific claim was attacked by an adversarial reviewer, who judged it WEAKENED.
Your job is to adjudicate that attack, not to re-attack the claim.

CLAIM:
{stmt}

THE ATTACK:
{attack}

Decide whether the attack is correct AND material enough to require the claim be rewritten.
Answer with exactly one of these words on the first line:

ACTIONABLE  the attack is correct and the claim states something that is wrong or
            unsupported as written; a corrected claim is owed
MINOR       the attack is correct but cosmetic -- a hedge, a caveat the claim already
            implies, or a scope note; the claim stands as written
WRONG       the attack is incorrect, misreads the claim, or objects to something the claim
            does not say

Then one sentence of reason."""


def pick(text: str) -> str | None:
    hits = [w for w in re.findall(r"[A-Z]{5,}", text or "") if w in VERDICTS]
    return hits[0] if hits else None


def main() -> int:
    project = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    nums = [a for a in sys.argv[1:] if a.isdigit()]
    n = int(nums[0]) if nums else 15
    rows = q(f"""select c.id, {flat('c.statement', 2600)}, {flat('ch.evidence', 1800)}
                 from claim c join challenge ch on ch.claim_id = c.id
                 where c.project_id={lit(project)} and c.superseded_by is null
                   and ch.outcome = 'weakened' and length(coalesce(ch.evidence,'')) > 80
                 order by c.id limit {int(n)}""")
    print(f"  {project}: {len(rows)} weakened claim(s) to adjudicate "
          f"(nothing is written to `claim`)\n")
    tally: collections.Counter[str] = collections.Counter()
    spent = 0.0
    for i, (cid, stmt, attack) in enumerate(rows):
        out = ac.call_with_fallback(ac.TENANTS[i % len(ac.TENANTS)],
                                    PROMPT.format(stmt=stmt, attack=attack))
        spent += float(out.get("cost_usd") or 0.0)
        v = pick(out.get("text", "")) or "unparseable"
        tally[v] += 1
        first = (out.get("text") or "").strip().splitlines()
        why = next((ln for ln in first[1:] if ln.strip()), "")[:96]
        print(f"    claim {cid:>5}  {v:<12} {why}")
    print(f"\n  {dict(tally)}")
    act = tally.get("ACTIONABLE", 0)
    judged = sum(v for k, v in tally.items() if k in VERDICTS)
    if judged:
        print(f"  {act} of {judged} judged attacks are ACTIONABLE ({100*act/judged:.0f}%) -- "
              f"that is the size of the correction debt this project carries.")
    print(f"  spent ${spent:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
