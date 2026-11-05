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


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
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
