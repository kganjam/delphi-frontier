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

import os
import difflib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_challenge as ac  # noqa: E402

TOOLS = ("ESMFold2 / OpenFold3 / Boltz2 structure prediction on Nebius (single serial slot); "
         "ProteinMPNN inverse folding; MSA search against PDB70; PubMed and Europe PMC literature "
         "retrieval; local Python numerical modelling; a Postgres claim graph. NO wet-lab access, "
         "NO animal work, NO new experimental measurement of any kind.")

PROMPT = """You are proposing the next open question for this design project:

PROJECT: {title}
GOAL: {goal}

WHAT IS ALREADY SETTLED OR IN HAND:
{context}

TOOLS ACTUALLY AVAILABLE: {tools}

Propose ONE subproblem that is worth adding. It must satisfy all four, and a proposal missing any
one is useless to us:

1. QUESTION containing a NUMBER or a threshold, so it is a calculation and not a conversation.
   "Can a fin ray carry load?" is unanswerable. "Can it carry the design lift without exceeding
   10% tip deflection?" is a calculation.
2. WHY it matters to THIS PROJECT'S goal specifically, as stated above.
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
    rows = ac.q(f"""select {ac.flat('statement', 240)} from claim
                    where project_id={ac.lit(ac.PROJECT)} and superseded_by is null
                    and evidence in ('measured','derived') and value_num is not null
                    order by id desc limit 18""")
    qs = ac.q(f"""select id, {ac.flat('question', 120)} from subproblem
                  where project_id={ac.lit(ac.PROJECT)} order by id desc limit 40""")
    return ("RECENT QUANTITATIVE FINDINGS:\n" + "\n".join("- " + r[0] for r in rows)
            + "\n\nEXISTING SUBPROBLEMS (do not duplicate):\n"
            + "\n".join(f"- {r[0]}: {r[1]}" for r in qs))


def project_brief() -> tuple[str, str]:
    """This project's title and goal, from the `project` table. REFUSES if absent.

    THE PROMPT USED TO HARDCODE THE FISH: "turn a zebrafish (4 cm, ~0.4 g) into an animal that
    can glide", and "WHY it matters to the flight question". Running it under SWARM_PROJECT=coral
    therefore wrote ZEBRAFISH questions into the coral project -- 24 such rows across coral,
    insect-flight, xenobot and limbless-mouse before this was caught, every one of them
    mentioning zebrafish and none mentioning its own organism. The `project` table has carried a
    title and goal for all five projects the whole time.

    Refusing on an absent brief rather than falling back to a default is deliberate: a default
    is what produced 24 wrong rows that LOOKED like progress on the structure checker.
    """
    rows = ac.q(f"""select {ac.flat('title')}, {ac.flat('goal')} from project
                    where id={ac.lit(ac.PROJECT)}""")
    if not rows or not rows[0][0].strip():
        raise SystemExit(
            f"REFUSING: no project row with a title for {ac.PROJECT!r}. The prompt is written "
            f"from the project's own goal, and defaulting to another project's text is what "
            f"put 24 zebrafish questions into four other projects.")
    return rows[0][0], (rows[0][1] if len(rows[0]) > 1 else "")


def next_subproblem_number() -> int:
    """One past the highest S<digits> in the WHOLE TABLE, floored at 900.

    NOT per project. `subproblem_pkey` is `PRIMARY KEY (id)` -- the id is globally unique, not
    unique per project. Scoping this query by project_id is how coral's first frontier run
    allocated S900-S905, collided with the zebrafish rows of those names, and wrote NOTHING
    while printing "wrote S903" for each: `on conflict (id) do nothing` had converted the
    crash into a silent no-op, which is strictly worse than the crash it replaced. The insert
    below now reads its `returning` value and says which ids actually landed.

    The id family is S<number>; ids with a suffix (S9-D, S25-D-D) are deepenings of those and
    are left alone. `regexp_replace` strips the S and anything after the digits so a suffixed
    id cannot be read as a number.
    """
    rows = ac.q("""select coalesce(max((regexp_replace(id, '^S([0-9]+).*$', chr(92) || '1'))::int), 0)
                   from subproblem where id ~ '^S[0-9]+'""")
    return max(900, int(rows[0][0]) + 1)


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


#: Pairwise question similarity above which two proposals are treated as the same question.
#: MEASURED, not guessed (2026-11-05). On a thin project every tenant proposes the obvious
#: question: all 10 insect-flight pairs and 3 of 10 coral pairs scored above 0.6, while the
#: zebrafish frontier -- 112 subproblems built from a 474-claim history -- maxes out at 0.29
#: pairwise. So 0.6 separates "the generator repeated itself" from "these are different
#: questions", with a must-flag case and a must-not-flag case on real data.
DUP_RATIO = 0.6


def _ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def existing_questions() -> list[str]:
    """Questions already on this project's frontier, so a run cannot re-propose one."""
    rows = ac.q(f"select {ac.flat('question', 400)} from subproblem "
                f"where project_id = {ac.lit(ac.PROJECT)}")
    return [r[0] for r in rows if r and r[0]]


def dedupe(props: list[dict], prior: list[str]) -> tuple[list[dict], list[tuple]]:
    """Drop proposals that repeat each other or a question already on the frontier.

    WHY THIS IS NOT OPTIONAL. The frontier generator is the piece that is supposed to make the
    pipeline replicate to a new project. It does replicate mechanically -- coral and
    insect-flight both returned five well-formed proposals with reachable falsifiers. But a new
    project has a thin context (coral: 588 characters of settled findings, against the fish's
    474 claims), and with little to go on every tenant converges on the same obvious question.
    Writing those unfiltered would add five versions of one question to a project whose stated
    problem is already that it is scattered -- the pipeline would be actively making the thing
    it exists to fix worse.
    """
    kept: list[dict] = []
    dropped: list[tuple] = []
    for p in props:
        q = p["QUESTION"]
        hit = next(((r, "already on the frontier", e)
                    for e in prior if (r := _ratio(q, e)) >= DUP_RATIO), None)
        if hit is None:
            hit = next(((r, "repeats proposal " + k["QUESTION"][:60], k["QUESTION"])
                        for k in kept if (r := _ratio(q, k["QUESTION"])) >= DUP_RATIO), None)
        if hit:
            dropped.append((q, hit[0], hit[1]))
        else:
            kept.append(p)
    return kept, dropped


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3
    write = "--write" in sys.argv
    title, goal = project_brief()
    print(f"  project {ac.PROJECT}: {title[:70]}")
    ctx = context()
    print(f"  context: {len(ctx)} chars of settled findings and existing subproblems\n")
    good = []
    spent = 0.0
    for i in range(n):
        t = ac.TENANTS[i % len(ac.TENANTS)]
        try:
            r = ac.call_with_fallback(t, PROMPT.format(context=ctx[:14000], tools=TOOLS, title=title, goal=goal))
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
    prior = existing_questions()
    good, dropped = dedupe(good, prior)
    for q, r, why in dropped:
        print(f"  DROPPED (similarity {r:.2f}, {why[:50]}): {q[:90]}")
    print(f"  {len(good)} distinct after deduplication against each other and "
          f"{len(prior)} existing subproblems")
    if write:
        # ALLOCATE FROM WHAT EXISTS, NOT FROM A LITERAL. This read `f"S{900 + j}"` with j the
        # loop index, so every run started at S900 regardless of the table. S900-S908 were
        # already taken, so the FIRST insert raised `duplicate key value violates unique
        # constraint "subproblem_pkey"` and the exception discarded all ten questions the run
        # had just paid for -- a failure that costs money and leaves nothing to show for it.
        base = next_subproblem_number()
        for j, p in enumerate(good):
            sid = f"S{base + j}"
            # `acceptance` is NOT NULL in the schema, which is the right constraint: a
            # subproblem that does not say what would settle it is a topic, not a question. It is
            # built from the REACHABLE field, because that is the one naming the instrument.
            acc = (f"Run: {p['REACHABLE']}  ->  ANSWERED when that produces a number that either "
                   f"meets or fails this pre-registered falsifier: {p['FALSIFIER']}")
            # ON CONFLICT DO NOTHING so a collision costs one row, not the whole batch.
            # The surviving rows are still worth having and the run is not cheap.
            got = ac.q(f"""insert into subproblem (project_id, id, question, why_it_matters, acceptance,
                                             falsifier, status)
                     values ({ac.lit(ac.PROJECT)}, {ac.lit(sid)}, {ac.lit(p['QUESTION'])},
                             {ac.lit(p['WHY'])}, {ac.lit(acc)},
                             {ac.lit(p['FALSIFIER'])}, 'open')
                     on conflict (id) do nothing
                     returning id""")
            print(f"  wrote {sid}" if got else
                  f"  NOT WRITTEN {sid}: id already taken (ids are globally unique)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
