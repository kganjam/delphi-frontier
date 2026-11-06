#!/usr/bin/env python3
"""Controls for dbq.flat() -- the scrub that keeps a stored value from breaking psql framing.

THE HISTORICAL CASE IS THE MUST-FLAG ARM. On 2026-11-05 `api_frontier.py` scrubbed the field
separator and NOT the newline, so `select id, question from subproblem` returned a one-field
row for each of the 4 questions containing a newline, and `r[1]` raised IndexError. Arm 1
reproduces that against the live database with the old expression and requires it to break.

AND THE SILENT HALF, WHICH MATTERS MORE. The same function's other query selected ONE column,
where 84 of 531 statements contain a newline. A short row still has `r[0]`, so nothing raised --
the model was handed statement FRAGMENTS presented as separate settled findings. Arm 2 requires
the old expression to return MORE rows than there are claims, which is the shape of that
corruption, and arm 3 requires flat() to return exactly as many rows as claims.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dbq import PROJECT, flat, lit, q  # noqa: E402

OLD_SEP_ONLY = "replace({col}, chr(1), ' ')"          # api_frontier's expression, the bug
OLD_LF_ONLY = "replace({col}, chr(10), ' ')"          # design_spec's, safe here, unsafe for SEP


def arms() -> list[tuple[str, bool, str]]:
    out = []

    n_sub = int(q(f"select count(*) from subproblem where project_id={lit(PROJECT)}")[0][0])
    n_cl = int(q(f"select count(*) from claim "
                 f"where project_id={lit(PROJECT)} and superseded_by is null")[0][0])

    # 1. MUST FLAG: the historical two-column crash, reproduced exactly.
    rows = q(f"select id, {OLD_SEP_ONLY.format(col='question')} from subproblem "
             f"where project_id={lit(PROJECT)}")
    short = [r for r in rows if len(r) < 2]
    out.append(("the old SEP-only scrub still produces short rows (the IndexError)",
                bool(short), f"{len(short)} of {len(rows)} rows have <2 fields"))

    # 2. MUST FLAG: the silent one-column corruption -- more rows than claims.
    rows = q(f"select {OLD_SEP_ONLY.format(col='statement')} from claim "
             f"where project_id={lit(PROJECT)} and superseded_by is null")
    out.append(("the old scrub inflates a one-column select into extra rows",
                len(rows) > n_cl, f"{len(rows)} rows for {n_cl} claims"))

    # 3. MUST NOT FLAG: flat() gives exactly one row per claim, no short rows.
    rows = q(f"select id, {flat('statement')} from claim "
             f"where project_id={lit(PROJECT)} and superseded_by is null")
    ok = len(rows) == n_cl and all(len(r) == 2 for r in rows)
    out.append(("flat() returns exactly one 2-field row per claim", ok,
                f"{len(rows)} rows for {n_cl} claims, "
                f"{sum(1 for r in rows if len(r) != 2)} malformed"))

    rows = q(f"select id, {flat('question', 120)} from subproblem "
             f"where project_id={lit(PROJECT)}")
    ok = len(rows) == n_sub and all(len(r) == 2 for r in rows)
    out.append(("flat(limit) returns exactly one 2-field row per subproblem", ok,
                f"{len(rows)} rows for {n_sub} subproblems"))

    # 4. MUST NOT FLAG: the scrub must not be vacuous -- it has to CHANGE something,
    #    or arms 1-3 would pass on a database with no newlines in it and prove nothing.
    changed = int(q(f"select count(*) from claim where project_id={lit(PROJECT)} "
                    f"and superseded_by is null and {flat('statement')} <> statement")[0][0])
    out.append(("flat() actually changes some stored values (arms 1-3 are not vacuous)",
                changed > 0, f"{changed} of {n_cl} live claims are altered by the scrub"))

    # 5. MUST NOT FLAG: and it must not change the ones that need no scrubbing.
    same = int(q(f"select count(*) from claim where project_id={lit(PROJECT)} "
                 f"and superseded_by is null and statement not like '%'||chr(10)||'%' "
                 f"and {flat('statement')} <> statement")[0][0])
    out.append(("flat() leaves a single-line value byte-identical", same == 0,
                f"{same} newline-free statements were altered"))

    # 6. MUST FLAG: truncation after scrubbing, not before. A limit shorter than the
    #    first line break must still yield one row.
    probe = ("select " + flat("'a'||chr(10)||'b'||chr(10)||'c'", 3)
             + ", " + OLD_LF_ONLY.format(col="left('a'||chr(10)||'b', 2)"))
    r = q(probe)
    out.append(("scrub-then-truncate keeps one row where truncate-then-scrub would not",
                len(r) == 1 and len(r[0]) == 2 and chr(10) not in r[0][0],
                f"got {r!r}"))
    return out


def main() -> int:
    bad = 0
    for name, ok, detail in arms():
        print(f"  [{'ok' if ok else 'FAIL'}] {name}\n           {detail}")
        bad += not ok
    print(f"  -> controls {'PASS' if not bad else f'FAIL ({bad})'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
