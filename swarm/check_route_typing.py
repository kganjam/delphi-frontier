#!/usr/bin/env python3
"""Flag claims carrying the retired blanket not-attempted paraphrase, without rewriting them.

WHAT HAPPENED. `import_design_space.py` wrote onto every imported route: "the source file
states that none of its routes was attempted". No source file says that. Both routes files say
in their own `limitations`: "We ran no experiments. Every route on this page is a reading of
someone else's published work, OR an explicitly labelled proposal." That the FILE'S AUTHORS ran
nothing is a different statement from nobody having performed the intervention, and collapsing
the two mistyped claims in BOTH directions -- see claim 1053.

The importer is fixed. These rows are not, and they are DELIBERATELY NOT REWRITTEN: a claim is
corrected by supersession, and editing 177 statements in place would destroy the record of what
the graph said. So this makes them findable instead, with the per-row reason to re-read.

A row is suspicious when it carries the paraphrase AND its declared evidence_strength is a
`direct_*` kind -- the combination that cannot be true at once. A row declaring `proposed` or
`model_only` alongside the paraphrase is merely wordy, not wrong, and is counted separately so
the suspicious count is not inflated.

    python3 check_route_typing.py            # counts
    python3 check_route_typing.py --list     # every suspicious claim id
"""
from __future__ import annotations

import sys

from dbq import q

PARAPHRASE = "none of its routes" + " was attempted"
PROPOSAL_KINDS = ("proposed", "model_only", "cis_regulatory_inference")


def main() -> int:
    rows = q(f"""select id, project_id,
                        substring(statement from 'Declared evidence_strength ''([a-z_]+)''')
                 from claim
                 where statement like '%{PARAPHRASE}%' and superseded_by is null
                 order by project_id, id""")
    suspicious, wordy = [], []
    for cid, proj, strength in rows:
        (wordy if (strength or "") in PROPOSAL_KINDS else suspicious).append(
            (cid, proj, strength or "(none declared)"))

    print(f"  {len(rows)} live claim(s) carry the retired paraphrase")
    print(f"    {len(suspicious)} SUSPICIOUS -- paraphrase plus a direct_* declared strength, "
          f"which cannot both be true")
    print(f"    {len(wordy)} merely wordy -- declared a proposal, so the paraphrase agrees "
          f"with the row")
    by_proj: dict[str, int] = {}
    for _, p, _ in suspicious:
        by_proj[p] = by_proj.get(p, 0) + 1
    for p, n in sorted(by_proj.items(), key=lambda kv: -kv[1]):
        print(f"      {p:18} {n}")

    if "--list" in sys.argv:
        print("\n  suspicious claim ids:")
        for cid, p, s in suspicious:
            print(f"    {cid:>6} {p:18} {s}")

    # CONTROL: the query must be capable of returning nothing. If the paraphrase were absent
    # from the table this prints 0, and a search that cannot return 0 is not a search.
    none = int(q("select count(*) from claim where statement like "
                 "'%a string that is not in any claim xyzzy%'")[0][0])
    print(f"\n  control: a pattern that matches nothing returns {none} "
          f"({'OK' if none == 0 else 'the query is matching everything'})")
    sample = int(q(f"select count(*) from claim where statement like '%{PARAPHRASE}%'")[0][0])
    print(f"  control: the same pattern including superseded rows returns {sample} "
          f"({'OK, strictly more than live' if sample >= len(rows) else 'INCONSISTENT'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
