#!/usr/bin/env python3
"""Does any SATISFIED cross-scale entailment rest on a claim that has since been withdrawn?

THE GAP THIS GUARDS IS NAMED BY CLAIM 1084: "the schema has no outbound link from an
entailment". `constraint_entailed.source_claim` records what a constraint derives FROM -- it is
set on 137 of 137 satisfied rows for zebrafish-flight, so the INBOUND link is complete. What
satisfies a constraint is recorded in `satisfied_by`, which is free prose: 379 of this project's
381 rows are non-numeric text. So the chain's own evidence cannot be joined, and a claim that
satisfies an entailment and is later superseded leaves the entailment reading `satisfied` with
nothing to notice.

THE PROSE RECOVERS ALMOST NONE OF IT, measured 2026-11-05 before this was written: only 7 of
137 satisfied rows (5 per cent) name a claim id in their prose at all. So this checker is cheap
insurance over a small set rather than a real audit of the chain, and saying so is the point --
a reader who sees it pass should not conclude the chain is verified. The 95 per cent that name
no claim are unverifiable here by construction, and closing that needs a schema column, which
is a design decision rather than something a checker can do.

WHAT IT DOES CHECK, and it is worth the few seconds: of the ids that ARE named, every one must
resolve to a claim in the same project and must not be superseded. Measured at the time of
writing: 12 distinct ids, 12 live, 0 superseded, 0 unresolved -- clean, and now watched.

    python3 swarm/check_entailment_provenance.py           # report
    python3 swarm/check_entailment_provenance.py --strict  # exit 1 on a withdrawn citation
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dbq import PROJECT, lit, q  # noqa: E402

CITE = re.compile(r"\bclaims?\s+(\d{1,5})", re.I)


def main() -> int:
    strict = "--strict" in sys.argv
    print("=" * 92)
    print(f"ENTAILMENT PROVENANCE -- withdrawn claims cited as satisfying, project {PROJECT!r}")
    print("=" * 92)
    rows = q(f"""select id::text, coalesce(source_claim::text,''),
                        replace(coalesce(satisfied_by,''), chr(10), ' ')
                 from constraint_entailed
                 where project_id = {lit(PROJECT)} and status = 'satisfied'""")
    if not rows:
        print("  no satisfied entailments in this project; nothing to check")
        return 0
    with_src = sum(1 for r in rows if r[1])
    named = [(r[0], set(CITE.findall(r[2]))) for r in rows]
    named = [(e, ids) for e, ids in named if ids]
    cited: set[str] = set()
    for _e, ids in named:
        cited |= ids

    print(f"\n  {len(rows)} satisfied entailment(s)")
    print(f"    with source_claim set (the INBOUND link): {with_src} "
          f"({100*with_src/len(rows):.0f}%)")
    print(f"    naming a claim id in satisfied_by prose : {len(named)} "
          f"({100*len(named)/len(rows):.0f}%)  <- all this checker can see")
    print(f"    distinct claim ids cited                : {len(cited)}")

    bad: list[str] = []
    if cited:
        ids = ",".join(sorted(cited, key=int))
        rs = q(f"""select id::text, coalesce(superseded_by::text,''), project_id
                   from claim where id in ({ids})""")
        found = {r[0]: (r[1], r[2]) for r in rs}
        for e, idset in named:
            for i in sorted(idset, key=int):
                if i not in found:
                    bad.append(f"  {e}: cites claim {i}, which does not exist")
                elif found[i][0]:
                    bad.append(f"  {e}: cites claim {i}, SUPERSEDED by {found[i][0]}")
                elif found[i][1] != PROJECT:
                    bad.append(f"  {e}: cites claim {i}, which belongs to {found[i][1]!r}")

    print()
    if bad:
        print("  WITHDRAWN OR FOREIGN CITATIONS:")
        print("\n".join(bad))
    else:
        print("  every cited claim resolves, is live, and belongs to this project")

    # The control that stops a pass from being mistaken for an audit.
    print(f"\n  [{'ok' if cited else 'INERT'}] control: {len(cited)} id(s) were actually looked "
          f"up, so a clean result here means those resolved -- NOT that the chain is verified. "
          f"{len(rows)-len(named)} of {len(rows)} satisfied entailments name no claim at all and "
          f"are outside what this can see (claim 1084).")
    if not cited:
        return 2
    print(f"  {len(bad)} problem(s)")
    return 1 if (strict and bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
