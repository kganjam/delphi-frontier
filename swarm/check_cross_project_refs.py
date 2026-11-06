#!/usr/bin/env python3
"""Does any row cite evidence belonging to a DIFFERENT project?

WHY THIS IS A DATA CHECK AND NOT A SOURCE CHECK. Four times now a tool has read SWARM_PROJECT,
used it for the heading and the id prefix, and carried hard-coded zebrafish content underneath:

    claim 470   one tool ignored the project switch; its domain filter was a fish-term list
    claim 481   check_specs.py read SWARM_PROJECT into a constant it never used in a query
    claim 1057  the frontier generator wrote 24 ZEBRAFISH subproblems into four other projects,
                and the structure checker counted them as progress
    2026-11-05  design_candidates.py would have written parts keyed `coral/gene/kcnk5b`, backed
                by zebrafish claims, into the coral project

Two source-level sweeps were tried for this and both failed the repo's own bar. Looking for
`from claim` without `project_id` returns 29 hits in project-aware files, nearly all of them
lookups by explicit id or deliberately database-wide checks -- and it MISSED the
design_candidates bug, whose SQL is built across lines. Looking for fish tokens in
project-aware code returns 41 files, of which the overwhelming majority are the harmless
`os.environ.get("SWARM_PROJECT", "zebrafish-flight")` default. A gate with that false-positive
rate gets switched off.

So this checks the ARTIFACT, which is the repo's standing rule when two things disagree: prefer
what computed a number over what wrote it down. Every row that carries BOTH a project_id and a
reference to a claim is compared against that claim's own project. A mismatch is a row whose
evidence belongs to someone else, and no amount of hard-coding can hide it here -- the
contamination is visible in the data whether or not the source looks generic.

    python3 swarm/check_cross_project_refs.py          # report
    python3 swarm/check_cross_project_refs.py --strict # exit 1 on any mismatch

WHAT IS NOT A VIOLATION, declared so the check is not quietly over-strict. A cross-project
reference is legitimate when it is deliberate transfer: SPEC ASK D5 is about carrying a result
from one design to another, and `transfer`-flavoured tables exist for exactly that. Those are
listed in ALLOWED below rather than discovered, so adding one is a decision somebody makes.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dbq import q  # noqa: E402

#: (table, column) pairs that may legitimately point at another project's claim.
ALLOWED: set[tuple[str, str]] = set()


def pairs() -> list[tuple[str, str]]:
    """Every (table, column) where the table has a project_id and the column references a claim."""
    have_proj = {r[0] for r in q("select table_name from information_schema.columns "
                                 "where column_name='project_id' and table_schema='public'")}
    out = []
    for t, c in q("""select table_name, column_name from information_schema.columns
                     where table_schema='public'
                       and (column_name in ('claim_id','source_claim','satisfied_by','claim')
                            or column_name like '%_claim')
                     order by table_name, column_name"""):
        if t in have_proj and (t, c) not in ALLOWED:
            out.append((t, c))
    return out


def main() -> int:
    strict = "--strict" in sys.argv
    print("=" * 94)
    print("CROSS-PROJECT REFERENCES -- a row whose cited claim belongs to another project")
    print("=" * 94)
    total = checked = 0
    findings: list[str] = []
    for t, c in pairs():
        # The column may be text or bigint; compare as text so both work and a non-numeric
        # value (a slug rather than an id) simply fails to join rather than raising.
        rows = q(f"""select x.project_id, cl.project_id, count(*)
                     from {t} x join claim cl on cl.id::text = x.{c}::text
                     where x.project_id is not null and cl.project_id <> x.project_id
                     group by 1, 2 order by 3 desc""")
        n = q(f"""select count(*) from {t} x join claim cl on cl.id::text = x.{c}::text
                  where x.project_id is not null""")[0][0]
        checked += int(n)
        for owner, cited, cnt in rows:
            total += int(cnt)
            findings.append(f"  {t}.{c}: {cnt} row(s) in {owner!r} cite a claim owned by {cited!r}")
    print(f"\n  {len(pairs())} (table, column) pair(s) examined, {checked} joined row(s)\n")
    if findings:
        print("\n".join(findings))
    else:
        print("  no cross-project reference found")

    # A control, because a join that silently matches nothing reports exactly like a clean
    # result. If the checker joined no rows at all it has not checked anything.
    print(f"\n  [{'ok' if checked else 'FAIL'}] control: the joins matched {checked} row(s), so "
          f"the comparison ran (a zero here would mean the check is inert, not that the data "
          f"is clean)")
    if not checked:
        return 2
    print(f"  {total} violating row(s)")
    return 1 if (strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())
