#!/usr/bin/env python3
"""Propose a CHANGE TO THE DESIGN that addresses a named blocker -- not an attack on a claim.

THE GAP THIS FILLS. The adversarial arm (api_challenge.py) attacks claims and is demonstrably
effective: it overturned four consecutive design conclusions of mine in one session (claims
1149, 1154, 1156, 1160), each time on a specific, checkable ground. But attacking a claim
produces a WEAKENED CLAIM. It never produces a different design. The project's goal asks for
swarms "refining the designs", and nothing here has ever proposed a design change.

WHAT A PROPOSAL MUST CONTAIN, and why each field is mandatory:

    BLOCKER    which recorded blocker it addresses, by its entailment or claim id. A proposal
               that names no blocker is a preference, not a refinement.
    CHANGE     what to do differently, in terms of this design's actual parts and parameters --
               a lever, a geometry, a route -- not an aspiration.
    MECHANISM  why that would move the blocker's quantity. Without this the proposal cannot be
               argued with, only liked.
    COST       what it makes worse. Every real design change trades something, and a proposal
               claiming a free improvement is almost always moving the problem somewhere the
               proposer is not looking.
    FALSIFIER  what observation would show the change does NOT help, stated before anyone looks.

THE FAILURE MODE THIS GUARDS AGAINST is a model producing fluent design-shaped text: "increase
fin area", "use a different myosin", "optimise the launch angle". Those name no blocker, specify
no part, and cannot be wrong. The COST and FALSIFIER fields are what make a proposal a claim
about the world. A proposal missing either is dropped, and the drop is printed with its reason
so the arm's yield can be judged rather than assumed.

IT WRITES SUBPROBLEMS, NOT CLAIMS. A design proposal is not a finding; it is work to be done.
Landing it as a `claim` would assert something nobody has checked. It lands as an open
`subproblem` with the falsifier in its acceptance, which is the same contract api_frontier.py
uses and which the rest of this pipeline already knows how to process.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import api_challenge as ac  # noqa: E402
import api_frontier as af  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
FIELDS = ("BLOCKER", "CHANGE", "MECHANISM", "COST", "FALSIFIER")
SCALE_VOCAB = ("dna", "protein", "cell", "tissue", "organ", "organism", "behaviour", "ecology")

PROMPT = """You are a design engineer on this project. You are NOT reviewing claims. Your job is
to propose a CHANGE TO THE DESIGN that addresses one of the blockers below.

PROJECT: {title}
GOAL: {goal}

THE DESIGN'S PARTS (genetic levers, with what each does):
{parts}

THE BLOCKERS -- constraints the record says are contradicted by measurement, or failing:
{blockers}

WHAT THIS DESIGN ALREADY KNOWS, so you do not propose what has been tried:
{context}

Propose {n} DISTINCT design changes. For each, give EXACTLY these fields:

BLOCKER: <the id of the blocker you are addressing, e.g. e194 or claim 1137>
CHANGE: <what to do differently, naming a specific part, parameter or route of THIS design>
MECHANISM: <why that moves the blocker's quantity; be specific about the physics or biology>
COST: <what it makes worse -- every real change trades something; "nothing" is not an answer>
FALSIFIER: <a concrete observation that would show this change does NOT help>
SCALE: <one of: dna, protein, cell, tissue, organ, organism, behaviour, ecology>

RULES:
- Do NOT propose "increase fin area" or similar without saying by what mechanism and at what
  cost. A change that names no part and no cost will be discarded.
- Do NOT propose acquiring a measurement. That is a subproblem, not a design change.
- A change may be a RETREAT -- dropping a route, relaxing a requirement, accepting a different
  flight mode -- if that is what the blockers support. Retreats are design changes.
"""


def parts_block() -> str:
    rows = ac.q(f"""select p.name, coalesce(p.function,''), count(r.id)::text
                from part p left join part_revision r on r.part_id = p.id
                where p.project_id = {ac.lit(PROJECT)}
                group by p.name, p.function order by p.name""")
    return "\n".join(f"  {r[0]}: {r[1][:120]} [{r[2]} specified revision(s)]" for r in rows)


def blockers_block(limit=8) -> str:
    rows = ac.q(f"""select 'e' || id, coalesce(quantity,''),
                replace(left(coalesce(statement,''),150), chr(10), ' '),
                replace(left(coalesce(satisfied_by,''),200), chr(10), ' ')
                from constraint_entailed
                where project_id = {ac.lit(PROJECT)} and status in ('unsatisfiable','unsatisfied')
                order by (status = 'unsatisfiable') desc, id limit {limit}""")
    return "\n".join(f"  {r[0]} [{r[1][:40]}] {r[2]}\n      recorded: {r[3]}" for r in rows)


def context_block(limit=25) -> str:
    rows = ac.q(f"""select replace(left(coalesce(statement,''),180), chr(10), ' ')
                from claim where project_id = {ac.lit(PROJECT)} and superseded_by is null
                order by id desc limit {limit}""")
    return "\n".join(f"  - {r[0]}" for r in rows)


def parse(text: str) -> list[dict]:
    """Split on BLOCKER: and require every field; a partial proposal is dropped, not patched."""
    out = []
    for chunk in re.split(r"\n(?=BLOCKER:)", text):
        if "BLOCKER:" not in chunk:
            continue
        d = {}
        for f in FIELDS + ("SCALE",):
            m = re.search(rf"^{f}:\s*(.+?)(?=\n[A-Z]+:|\Z)", chunk, re.S | re.M)
            if m:
                d[f] = " ".join(m.group(1).split())[:700]
        out.append(d)
    return out


def vet(d: dict) -> tuple[bool, str]:
    for f in FIELDS:
        if not d.get(f):
            return False, f"missing {f}"
    cost = d["COST"].strip().lower()
    if cost.startswith(("none", "nothing", "no cost", "n/a")):
        return False, f"COST is {d['COST'][:40]!r} -- a change that trades nothing is not a design change"
    if len(d["CHANGE"]) < 25:
        return False, "CHANGE is too short to name a part or a parameter"
    return True, ""


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 4
    write = "--write" in sys.argv
    pin = sys.argv[sys.argv.index("--tenant") + 1] if "--tenant" in sys.argv else None
    title, goal = af.project_brief()
    parts, blockers, ctx = parts_block(), blockers_block(), context_block()
    if not blockers:
        print("  no blockers recorded; nothing to refine against.")
        return 0
    print(f"  project {PROJECT}: proposing {n} design change(s) against the recorded blockers\n")

    r = ac.call_with_fallback(pin or ac.TENANTS[0], PROMPT.format(
        title=str(title)[:120], goal=str(goal)[:600], parts=parts[:3000],
        blockers=blockers[:5000], context=ctx[:5000], n=n), max_tokens=4000)
    props = parse(r.get("text", ""))
    print(f"  {len(props)} proposal(s) returned, ${float(r.get('cost_usd') or 0):.4f}\n")

    good = []
    for d in props:
        ok, why = vet(d)
        if not ok:
            print(f"  DROPPED  {why}")
            print(f"           {str(d.get('CHANGE', d.get('BLOCKER','?')))[:80]}")
            continue
        good.append(d)
        print(f"  [{d['BLOCKER'][:14]}] {d['CHANGE'][:100]}")
        print(f"      mechanism: {d['MECHANISM'][:100]}")
        print(f"      cost:      {d['COST'][:100]}")
        print(f"      falsifier: {d['FALSIFIER'][:100]}")
    print(f"\n  {len(good)} accepted, {len(props)-len(good)} dropped.")

    if not write:
        print("  NOT written. Re-run with --write to record them as open subproblems.")
        return 0
    # api_frontier's allocator is next_subproblem_number(), not next_id(). The first version
    # guessed the name behind a hasattr() and so FAILED SILENTLY -- it printed "cannot allocate
    # ids" after a successful $0.03 API call and four accepted proposals, which reads like a
    # database problem rather than a typo. A hasattr guard around a name you did not verify
    # converts a NameError into a plausible-looking refusal, which is strictly worse.
    nxt = af.next_subproblem_number()
    for i, d in enumerate(good):
        sid = f"S{nxt + i}"
        sc = str(d.get("SCALE", "")).strip().lower().split()[0] if d.get("SCALE") else ""
        sc = sc if sc in SCALE_VOCAB else None
        acc = (f"Design change proposed against {d['BLOCKER']}. ANSWERED when the falsifier is "
               f"tested: {d['FALSIFIER']}")
        got = ac.q(f"""insert into subproblem (project_id, id, question, why_it_matters,
                   acceptance, falsifier, status, scale_id)
                   values ({ac.lit(PROJECT)}, {ac.lit(sid)},
                   {ac.lit('DESIGN CHANGE: ' + d['CHANGE'])},
                   {ac.lit('Addresses ' + d['BLOCKER'] + '. Mechanism: ' + d['MECHANISM'] +
                           ' COST: ' + d['COST'])},
                   {ac.lit(acc)}, {ac.lit(d['FALSIFIER'])}, 'open', {ac.lit(sc)})
                   on conflict (id) do nothing returning id""")
        print(f"  wrote {sid}" if got else f"  NOT WRITTEN {sid}: id taken")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
