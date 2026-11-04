#!/usr/bin/env python3
"""Propose SUBSTANTIVE new subproblems for the frontier, on Console API credit.

THE FRONTIER IS THINNER THAN ITS COUNT. Of 13 open subproblems, TWELVE are the auto-generated
template "Deepen S<id>: attack its most sensitive input" and one is a real question. A frontier
made of mechanical deepenings looks like work and does not name any.

SPEC-subproblem-lifecycle section 6 says what a subproblem must carry to be worth having, and it
was derived from the ones that worked: a NUMBER in the question, so it is a calculation rather than
a conversation; a FALSIFIER, stated before anyone looks; and a dependency list. Section 8 then names
the gap nothing checks -- "nothing checks that a falsifier is actually REACHABLE with available
tools, which is what distinguished the productive subproblems from the four that stalled."

So this tool requires the reachability to be named, and REFUSES a proposal that does not carry all
four fields. A proposal is printed for review and only written with --write: a generated question
is a suggestion, not a finding, and the thing that makes a frontier real is that someone decided
each entry was worth asking.

    python3 api_frontier.py <n> [--write]
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_challenge as ac  # noqa: E402

TOOLS = ("ESMFold2 / OpenFold3 / Boltz2 structure prediction on Nebius (single serial slot); "
         "ProteinMPNN inverse folding; MSA search against PDB70; PubMed and Europe PMC literature "
         "retrieval; local Python numerical modelling; a Postgres claim graph. NO wet-lab access, "
         "NO animal work, NO new experimental measurement of any kind.")

PROMPT = """You are proposing the next open question for a design project that is trying to work out
what it would take to turn a zebrafish (4 cm, ~0.4 g) into an animal that can glide. Not to copy
flying fish -- to derive the changes from first principles and published measurement.

WHAT IS ALREADY SETTLED OR IN HAND:
{context}

TOOLS ACTUALLY AVAILABLE: {tools}

Propose ONE subproblem that is worth adding. It must satisfy all four, and a proposal missing any
one is useless to us:

1. QUESTION containing a NUMBER or a threshold, so it is a calculation and not a conversation.
   "Can a fin ray carry load?" is unanswerable. "Can it carry the design lift without exceeding
   10% tip deflection?" is a calculation.
2. WHY it matters to the flight question specifically.
3. FALSIFIER: a concrete result that would settle it NEGATIVELY, stated before anyone looks.
4. REACHABLE: name which of the tools above would produce that falsifier, and say plainly if none
   would. A question whose falsifier needs a wet lab is honest to propose and must be labelled so,
   because we cannot run it.

Do not propose anything already settled above. Reply in EXACTLY this form:
QUESTION: <one sentence, with the number in it>
WHY: <one sentence>
FALSIFIER: <one sentence>
REACHABLE: <the tool that would settle it, or "NOT REACHABLE: needs <what>">
"""

FIELDS = ("QUESTION", "WHY", "FALSIFIER", "REACHABLE")


def context() -> str:
    rows = ac.q(f"""select left(replace(statement,'{ac.SEP}',' '), 240) from claim
                    where project_id={ac.lit(ac.PROJECT)} and superseded_by is null
                    and evidence in ('measured','derived') and value_num is not null
                    order by id desc limit 18""")
    qs = ac.q(f"""select id, left(replace(question,'{ac.SEP}',' '),120) from subproblem
                  where project_id={ac.lit(ac.PROJECT)} order by id desc limit 40""")
    return ("RECENT QUANTITATIVE FINDINGS:\n" + "\n".join("- " + r[0] for r in rows)
            + "\n\nEXISTING SUBPROBLEMS (do not duplicate):\n"
            + "\n".join(f"- {r[0]}: {r[1]}" for r in qs))


def parse(text: str) -> dict | None:
    out = {}
    for f in FIELDS:
        m = re.findall(rf"{f}:\s*(.+)", text)
        if not m:
            return None
        out[f] = m[-1].strip()[:600]
    if not re.search(r"\d", out["QUESTION"]):
        out["_no_number"] = True
    return out


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3
    write = "--write" in sys.argv
    ctx = context()
    print(f"  context: {len(ctx)} chars of settled findings and existing subproblems\n")
    good = []
    spent = 0.0
    for i in range(n):
        t = ac.TENANTS[i % len(ac.TENANTS)]
        try:
            r = ac.call_with_fallback(t, PROMPT.format(context=ctx[:14000], tools=TOOLS))
        except Exception as e:
            print(f"  [{i+1}] {t:13} FAILED {type(e).__name__}: {str(e)[:70]}")
            continue
        spent += float(r.get("cost_usd") or 0)
        p = parse(r.get("text", ""))
        if not p:
            print(f"  [{i+1}] {t:13} REFUSED: reply missing one of {FIELDS}")
            continue
        flags = []
        if p.get("_no_number"):
            flags.append("NO NUMBER IN THE QUESTION -- rejected per spec rule 1")
        if p["REACHABLE"].upper().startswith("NOT REACHABLE"):
            flags.append("falsifier NOT reachable with our tools -- honest, but we cannot run it")
        print(f"  [{i+1}] {t:13} {'  '.join(flags) if flags else 'all four fields present'}")
        print(f"       Q: {p['QUESTION'][:150]}")
        print(f"       F: {p['FALSIFIER'][:150]}")
        print(f"       R: {p['REACHABLE'][:150]}")
        if not flags:
            good.append(p)
    print(f"\n  {len(good)} of {n} proposals carry all four fields and a reachable falsifier")
    print(f"  spent ${spent:.4f}")
    print("  NOT written: a generated question is a suggestion. Review each, then --write."
          if not write else "")
    if write:
        for j, p in enumerate(good):
            sid = f"S{900 + j}"
            # `acceptance` is NOT NULL in the schema, which is the right constraint: a
            # subproblem that does not say what would settle it is a topic, not a question. It is
            # built from the REACHABLE field, because that is the one naming the instrument.
            acc = (f"Run: {p['REACHABLE']}  ->  ANSWERED when that produces a number that either "
                   f"meets or fails this pre-registered falsifier: {p['FALSIFIER']}")
            ac.q(f"""insert into subproblem (project_id, id, question, why_it_matters, acceptance,
                                             falsifier, status)
                     values ({ac.lit(ac.PROJECT)}, {ac.lit(sid)}, {ac.lit(p['QUESTION'])},
                             {ac.lit(p['WHY'])}, {ac.lit(acc)},
                             {ac.lit(p['FALSIFIER'])}, 'open')""")
            print(f"  wrote {sid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
