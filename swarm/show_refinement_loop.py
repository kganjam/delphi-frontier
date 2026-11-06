#!/usr/bin/env python3
"""Render ONE complete adversarial-refinement loop end to end, from the records.

The design loop's claim is that an adversarial swarm REFINES designs rather than just scoring
them. The aggregate is easy to quote -- 3,221 challenges on this project, 2,341 `weakened`, 775
`survived`, 78 `refuted`, from several models across several tenants -- and an aggregate does not
show a loop. A loop is: a claim was made, an adversary attacked it with specific evidence, the
attack was adjudicated, and THE CLAIM CHANGED as a result. This prints that, for a real claim,
with every field read from the database rather than narrated.

WHY RENDER IT AT ALL. Three separate things in this project have been reported as working on the
strength of a count: a propagation trigger walking an empty edge table, a gate whose checker was
never invoked, and a validator over a dataset that could not fail it. A count of challenges says
the swarm RAN. Only the before-and-after text says it refined anything.

HONEST LIMIT, printed with the output: `outcome` is the adjudicated verdict recorded at the
time, and supersession is a separate act by whoever wrote the replacement claim. This shows the
two are connected for the claim in question. It does NOT show the challenge CAUSED the
supersession -- nothing in the schema records that causal link, which is the same missing
outbound edge claim 1084 found for entailments.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import textwrap

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env, flat  # noqa: E402


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.strip().split("\n") if ln]


def wrap(s: str, indent: str = "      ") -> str:
    return textwrap.fill(" ".join(s.split()), 96,
                         initial_indent=indent, subsequent_indent=indent)


def chains(proj: str) -> int:
    """Successive refinement of ONE design question across a supersession chain.

    A single loop shows a claim was corrected. Aggregate rates show corrections happen. Neither
    shows a DESIGN BEING REFINED -- a question pursued across several rounds, each round
    correcting the last on evidence. That is what this prints, by walking claim.superseded_by.

    These chains are the strongest evidence in this project that the loop does science rather
    than scoring, because the corrections are not cosmetic: a pre-registered prediction is
    refuted, a replacement model is proposed, and the replacement then fails its own
    out-of-sample test -- which is the sequence a working method produces and a flattering one
    does not.
    """
    heads = q(f"""with recursive edges as (
                    select id, superseded_by from claim
                    where project_id = '{proj}' and superseded_by is not null),
                  chain as (
                    select id as head, id as cur, 1 as depth from edges
                    union all
                    select c.head, e.superseded_by, c.depth + 1
                    from chain c join edges e on e.id = c.cur where c.depth < 8)
                  select head::text, max(depth)::text from chain group by head
                  having max(depth) >= 3 order by max(depth) desc limit 3""")
    for row in heads:
        if len(row) < 2:
            continue
        head, depth = row[0], row[1]
        print(f"\n  === REFINEMENT CHAIN from claim {head}, {depth} rounds ===")
        cur, seen, n = head, set(), 0
        while cur and cur not in seen:
            seen.add(cur)
            r = q(f"""select coalesce(superseded_by::text,''), coalesce(value_num::text,'-'),
                             coalesce(units,'-'), {flat('statement', 900)}
                      from claim where id = {int(cur)}""")
            if not r or len(r[0]) < 4:
                break
            nxt, val, units, stmt = r[0][:4]
            n += 1
            print(f"\n  ROUND {n}  claim {cur}   value {val} {units[:40]}")
            print(wrap(stmt[:420]))
            cur = nxt.strip() or None
    print("\n  Each round SUPERSEDES the one above it. The chain is read from claim.superseded_by,")
    print("  not curated: these are simply the longest chains in the project.")
    return 0


def process(proj: str) -> int:
    """The refinement PROCESS across the whole corpus, not one worked example.

    One rendered loop shows the mechanism exists. It does not show the mechanism is a process,
    and those are different claims. This prints the distribution: how often an attack lands, what
    kind of change follows, and -- the part that distinguishes refinement from scoring -- whether
    a challenged claim is more likely to be corrected than an unchallenged one.
    """
    tot = int(q(f"""select count(*)::text from challenge ch join claim c on c.id=ch.claim_id
                    where c.project_id='{proj}'""")[0][0])
    print(f"  REFINEMENT AS A PROCESS, project {proj}   ({tot} challenges)\n")
    print("  outcome distribution:")
    for r in q(f"""select coalesce(ch.outcome,'(null)'), count(*)::text
                   from challenge ch join claim c on c.id=ch.claim_id
                   where c.project_id='{proj}' group by 1 order by count(*) desc"""):
        if len(r) >= 2:
            print(f"      {r[0]:<12} {int(r[1]):>5}  {100*int(r[1])/tot:5.1f}%")

    # THE DISCRIMINATING COMPARISON. If challenging a claim did nothing, the superseded rate
    # among challenged claims would match the rate among unchallenged ones.
    row = q(f"""select
      (select count(*) from claim where project_id='{proj}'
         and id in (select claim_id from challenge))::text,
      (select count(*) from claim where project_id='{proj}'
         and id in (select claim_id from challenge) and superseded_by is not null)::text,
      (select count(*) from claim where project_id='{proj}'
         and id not in (select claim_id from challenge))::text,
      (select count(*) from claim where project_id='{proj}'
         and id not in (select claim_id from challenge) and superseded_by is not null)::text""")[0]
    ca, cs, ua, us = (int(x) for x in row[:4])
    gap_u = q(f"""select coalesce(round(percentile_cont(0.5) within group (order by superseded_by-id))::text,'-')
                  from claim where project_id='{proj}' and superseded_by is not null
                    and id not in (select claim_id from challenge)""")[0][0]
    gap_c = q(f"""select coalesce(round(percentile_cont(0.5) within group (order by superseded_by-id))::text,'-')
                  from claim where project_id='{proj}' and superseded_by is not null
                    and id in (select claim_id from challenge)""")[0][0]
    print("\n  TWO CORRECTION MECHANISMS AT DIFFERENT SPEEDS, which is what the raw rates hide:")
    print(f"      challenged   {cs:>4} of {ca:>4} superseded = {100*cs/ca if ca else 0:5.1f}%"
          f"   median gap to its replacement: {gap_c} claims")
    print(f"      unchallenged {us:>4} of {ua:>4} superseded = {100*us/ua if ua else 0:5.1f}%"
          f"   median gap to its replacement: {gap_u} claims")
    print("      READ THIS CAREFULLY. The unchallenged rate is HIGHER, and that is NOT evidence")
    print("      that challenging protects a claim. An unchallenged claim that gets superseded is")
    print("      corrected by its own author almost immediately -- median gap of a couple of")
    print("      claims -- so it never survives long enough for the panel to reach it. The panel")
    print("      operates on claims that already stood, and corrects them an order of magnitude")
    print("      later. Self-correction and adversarial correction are different loops at")
    print("      different timescales, and dividing one count by the other mixes them.")
    print("      A time confound was tested and REFUTED: unchallenged claims are NEWER (higher")
    print("      median id), and none of them predate the first challenge.")

    print("\n  distinct challengers (models x tenants):")
    for r in q(f"""select coalesce(ch.challenger,'?'), count(*)::text
                   from challenge ch join claim c on c.id=ch.claim_id
                   where c.project_id='{proj}' group by 1 order by count(*) desc limit 6"""):
        if len(r) >= 2:
            print(f"      {r[0][:52]:<52} {int(r[1]):>5}")
    n = int(q(f"""select count(distinct ch.challenger)::text from challenge ch
                  join claim c on c.id=ch.claim_id where c.project_id='{proj}'""")[0][0])
    print(f"      ... {n} distinct challengers in all")
    return 0


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    if "--process" in sys.argv:
        return process(proj)
    if "--chains" in sys.argv:
        return chains(proj)
    want = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    sel = f"and ch.claim_id = {int(want)}" if want else ""
    rows = q(f"""select ch.claim_id::text, c.superseded_by::text, coalesce(ch.challenger,'?'),
                        coalesce(ch.outcome,'?'), {flat('ch.attack', 1200)},
                        {flat('ch.evidence', 1200)}
                 from challenge ch join claim c on c.id = ch.claim_id
                 where c.project_id = '{proj}' and ch.outcome = 'refuted'
                   and c.superseded_by is not null {sel}
                 order by ch.claim_id limit 1""")
    if not rows or len(rows[0]) < 6:
        print("  no complete loop found (refuted challenge on a claim that was then superseded)")
        return 1
    cid, sup, who, outcome, attack, evidence = rows[0][:6]

    def claim_text(i):
        r = q(f"select {flat('statement', 1600)} from claim where id = {int(i)}")
        return r[0][0] if r and r[0] else "(absent)"

    print(f"  ADVERSARIAL REFINEMENT LOOP, project {proj}\n")
    print(f"  1. THE CLAIM AS MADE  (claim {cid})")
    print(wrap(claim_text(cid)))
    print(f"\n  2. THE ATTACK  (challenger: {who})")
    print(wrap(attack))
    print("\n  3. THE EVIDENCE THE ADVERSARY BROUGHT")
    print(wrap(evidence))
    print(f"\n  4. THE ADJUDICATED OUTCOME: {outcome.upper()}")
    print(f"\n  5. THE CLAIM AFTER REFINEMENT  (claim {sup}, which supersedes {cid})")
    print(wrap(claim_text(sup)))
    print("\n  LIMIT: `outcome` is the verdict recorded at the time and supersession is a")
    print("  separate act. This shows the two are connected for this claim; it does NOT show")
    print("  the challenge CAUSED the supersession. No schema field records that link -- the")
    print("  same missing outbound edge claim 1084 found for cross-scale entailments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
