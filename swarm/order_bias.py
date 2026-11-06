#!/usr/bin/env python3
"""Does presentation ORDER change which claim the panel prefers? Measured on supersession pairs.

WHY THIS EXISTS. `check_specs.py` reports SPEC-evaluation-kernel rule 5 -- "every pairwise
comparison run in both orders with the order recorded" -- as UNCHECKED, because the `grade` and
`comparison` tables are empty. UNCHECKED is not a pass: the rule is exactly as unenforced as it
was before the checker existed. It cannot be cleared by inserting rows; it needs a real
comparison to have been run. This runs one.

AND THE QUESTION IS REAL FOR THIS PROJECT. Claim 497 measured that the adversarial arm's verdict
depends on WHICH MODEL saw the claim. Nobody has asked whether it depends on the order the
options are shown in, which is a documented failure mode of LLM judges and would quietly
corrupt every pairwise judgement the project makes.

THE GROUND TRUTH IS FREE. 85 fish claims were superseded by a later claim, each supersession a
recorded judgement that the newer claim is better supported. So each pair gives TWO
measurements at once:
    ACCURACY   does the model pick the superseding claim?
    ORDER BIAS does the winner change when the two are swapped?
A model that picks position rather than content scores ~50% accuracy and ~100% flip rate; one
that reads the claims scores high accuracy and ~0% flip rate. The two numbers separate those.

The rubric is registered FROZEN and identified by the sha256 of the prompt, matching the
convention the adversarial-challenge rubric already uses, so editing the prompt supersedes the
rubric rather than silently changing what past rows were graded against.

    python3 order_bias.py 12 --write
"""
from __future__ import annotations

import hashlib
import json
import re
import sys

import api_challenge as ac
from dbq import flat, lit, q

PROMPT = """Two scientific claims from the same project are shown below. They address the same
question and one supersedes the other.

Which is BETTER SUPPORTED -- by its own evidence, its controls, and the limits it states?

CLAIM A:
{a}

CLAIM B:
{b}

Answer with exactly one line:
WINNER: A
or
WINNER: B
Then one sentence of reason."""

RUBRIC_ID = "pairwise-support-v1-" + hashlib.sha256(PROMPT.encode()).hexdigest()[:16]
CRITERIA = {
    "note": "Pairwise 'which claim is better supported' as applied by swarm/order_bias.py. "
            "Criteria are the closed winner vocabulary plus the prompt itself, identified by "
            "hash, so editing the prompt changes the rubric identity.",
    "closed": True,
    "winner_vocabulary": ["A", "B"],
    "unparseable_reply": "recorded as winner null, never guessed",
    "both_orders_required": True,
}


def register_rubric() -> None:
    q(f"""insert into rubric (id, project_id, applies_to, version, criteria, aggregation,
                              frozen)
          values ({lit(RUBRIC_ID)}, {lit(ac.PROJECT)}, 'pairwise-support', 1,
                  {lit(json.dumps(CRITERIA))},
                  'no aggregation across graders; each (pair, order, grader) is its own row',
                  true)
          on conflict (id) do nothing""")


def winner(text: str) -> str | None:
    m = re.findall(r"WINNER:\s*([AB])\b", text or "", re.I)
    return m[-1].upper() if m else None


#: Phrases that TELL a judge which claim is the later one without it reading any evidence.
#: 9 of the first 12 superseding claims carried one and only 3 of the superseded ones did, so
#: a judge that merely pattern-matched these would score ~11/12 while evaluating nothing.
TELL = re.compile(
    r"\b(supersedes?|superseded|corrects? claim|correction to claim|replaces claim"
    r"|refutes claim|withdraw[sn]?|claim \d+ is corrected)\b", re.I)


def blind(text: str) -> str:
    """Remove the supersession tell, so the judge must read the evidence."""
    return TELL.sub("[REDACTED]", text)


def pairs(n: int) -> list[tuple[int, int, str, str]]:
    """(old_id, new_id, old_statement, new_statement) for supersession pairs."""
    return [(int(r[0]), int(r[1]), r[2], r[3]) for r in q(f"""
        select old.id, new.id, {flat('old.statement', 2600)}, {flat('new.statement', 2600)}
        from claim old join claim new on new.id = old.superseded_by
        where old.project_id={lit(ac.PROJECT)} and length(old.statement) > 200
          and length(new.statement) > 200
        order by old.id desc limit {int(n)}""")]


def main() -> int:
    write = "--write" in sys.argv
    redact = "--redact" in sys.argv
    nums = [a for a in sys.argv[1:] if a.isdigit()]
    n = int(nums[0]) if nums else 10
    rows = pairs(n)
    if write:
        register_rubric()
    print(f"  rubric {RUBRIC_ID}  ({'registered' if write else 'dry run'})")
    print("  measurement only: the result is recorded as a CLAIM, not in `comparison`,")
    print("  whose foreign keys point at `candidate` rather than `claim`.")
    print(f"  {len(rows)} supersession pair(s); each run in BOTH orders"
          + ("; supersession TELL redacted from both claims" if redact else "") + "\n")

    correct = flips = unparsed = 0
    spent = 0.0
    for i, (old_id, new_id, old_s, new_s) in enumerate(rows):
        t = ac.TENANTS[i % len(ac.TENANTS)]
        verdicts = {}
        for swapped in (False, True):
            # swapped=False shows the SUPERSEDED claim as A; True shows the superseder as A.
            a, b = (new_s, old_s) if swapped else (old_s, new_s)
            if redact:
                a, b = blind(a), blind(b)
            out = ac.call_with_fallback(t, PROMPT.format(a=a, b=b))
            spent += float(out.get("cost_usd") or 0.0)
            w = winner(out.get("text", ""))
            verdicts[swapped] = w
            # NOT WRITTEN TO `comparison`, DELIBERATELY. That table's left_id/right_id are
            # foreign keys to `candidate`, and its winner vocabulary is left/right/tie: it is
            # built for comparing DESIGN CANDIDATES, not claims. Writing claim ids there would
            # be mis-typing an entity to clear a checkbox, which is what SPEC rule 5 exists to
            # prevent. The measurement is recorded as a claim instead, where it belongs.
        # Did the SUPERSEDING claim win in each order?
        picked_new = {s: (v == ("A" if s else "B")) for s, v in verdicts.items()
                      if v is not None}
        if len(picked_new) < 2:
            unparsed += 1
            mark = "unparseable"
        else:
            both = list(picked_new.values())
            correct += sum(both)
            flips += both[0] != both[1]
            mark = ("superseder won BOTH orders" if all(both) else
                    "superseded won BOTH orders" if not any(both) else
                    "FLIPPED with order")
        print(f"    {old_id:>5} -> {new_id:<5} {str(verdicts[False]):>4}/{str(verdicts[True]):<4}  {mark}")

    judged = len(rows) - unparsed
    if judged:
        print(f"\n  ACCURACY  the superseding claim won {correct}/{judged*2} of the "
              f"{judged*2} judgements ({100*correct/(judged*2):.0f}%)")
        print(f"  ORDER BIAS the winner flipped with order in {flips}/{judged} pairs "
              f"({100*flips/judged:.0f}%)")
        print("  A position-picking judge gives ~50% accuracy and ~100% flips;")
        print("  a content-reading judge gives high accuracy and ~0% flips.")
    print(f"  unparseable {unparsed}   spent ${spent:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
