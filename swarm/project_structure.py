#!/usr/bin/env python3
"""Measure every project against the structure the zebrafish project actually has.

WHY. The fish project works end to end -- claims typed by evidence, placed on a scale, a
frontier of open subproblems, an adversarial arm that writes BACK (supersession), and a
generated design spec. The other four projects in this database were built ad hoc and are, in
the owner's words, "scattered and less interesting". That is not a vague impression; it is
five numbers, and this prints them:

    project          scales  subproblems  superseded  measured  typed-beyond-literature
    coral                 0            0           0         0                        6
    insect-flight         0            0           0         0                        5
    limbless-mouse        0            0           0         0                       15
    xenobot               0            0           0         0                       16
    zebrafish-flight      8          112          85       117                      339

A project with 0 scales is not "across scales". A project with 0 subproblems has no frontier,
so nothing tells an agent what to do next. A project with 0 superseded claims has never had a
claim corrected, which means the adversarial arm ran and nothing was written back -- 53 to 194
challenges exist against each of those projects and not one changed a claim.

THIS IS A MEASUREMENT, NOT A GATE. The thresholds below are the fish's own shape, and a
different design question may legitimately need fewer scales. The point is to make the gap
visible and per-dimension, so closing it is a work list rather than an opinion.

    python3 project_structure.py            # every project
    python3 project_structure.py coral      # one
"""
from __future__ import annotations

import sys

from dbq import q

#: Each dimension: (label, SQL returning one count for a project, why it matters).
DIMENSIONS = (
    ("claims (live)",
     "select count(*) from claim where project_id={p} and superseded_by is null",
     "the body of the project"),
    ("scales used",
     "select count(distinct scale_id) from claim where project_id={p} "
     "and superseded_by is null and scale_id is not null",
     "0 means the project is not 'across scales' whatever its prose says"),
    ("claims placed on a scale",
     "select count(*) from claim where project_id={p} and superseded_by is null "
     "and scale_id is not null",
     "an unplaced claim cannot enter a cross-scale argument"),
    ("subproblems",
     "select count(*) from subproblem where project_id={p}",
     "the frontier: with none, nothing tells an agent what to do next"),
    ("subproblems answered",
     "select count(*) from subproblem where project_id={p} and status='answered'",
     "a frontier nobody closes is a wish list"),
    ("superseded claims",
     "select count(*) from claim where project_id={p} and superseded_by is not null",
     "0 means no claim was ever corrected -- the adversarial arm never wrote back"),
    ("measured claims",
     "select count(*) from claim where project_id={p} and superseded_by is null "
     "and evidence='measured'",
     "0 means nothing in the project was measured here"),
    ("typed beyond literature",
     "select count(*) from claim where project_id={p} and superseded_by is null "
     "and evidence in ('measured','derived','simulated')",
     "a project of only literature claims is a reading list"),
    ("challenges recorded",
     "select count(*) from challenge ch join claim c on c.id = ch.claim_id "
     "where c.project_id={p}",
     "the adversarial arm has run at all"),
    ("claims with a read_level where needed",
     "select count(*) from claim where project_id={p} and superseded_by is null "
     "and evidence='literature' and read_level is not null",
     "SPEC-ASK rule 2"),
)

REFERENCE = "zebrafish-flight"


def lit(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def measure(project: str) -> dict[str, int]:
    return {label: int(q(sql.format(p=lit(project)))[0][0]) for label, sql, _ in DIMENSIONS}


def main() -> int:
    want = sys.argv[1:] or [r[0] for r in q("select distinct project_id from claim order by 1")]
    data = {p: measure(p) for p in want}
    if REFERENCE not in data:
        data[REFERENCE] = measure(REFERENCE)

    labels = [d[0] for d in DIMENSIONS]
    names = [p for p in want if p != REFERENCE] + [REFERENCE]
    w = max(len(x) for x in labels) + 2
    print("=" * (w + 14 * len(names)))
    print("PROJECT STRUCTURE -- every project against the reference the fish actually has")
    print("=" * (w + 14 * len(names)))
    print(" " * w + "".join(f"{n[:13]:>14}" for n in names))
    for label in labels:
        row = "".join(f"{data[n][label]:>14}" for n in names)
        print(f"{label:<{w}}{row}")

    print("\nWHERE EACH PROJECT IS STRUCTURALLY EMPTY (a zero the reference does not have):")
    any_gap = False
    for n in names:
        if n == REFERENCE:
            continue
        gaps = [(label, why) for label, _, why in DIMENSIONS
                if data[n][label] == 0 and data[REFERENCE][label] > 0]
        if not gaps:
            print(f"  {n}: none")
            continue
        any_gap = True
        print(f"  {n}:")
        for label, why in gaps:
            print(f"      {label:<32} -- {why}")
    if not any_gap:
        print("  (none)")
    print("\nThis is a MEASUREMENT, not a gate: a different design question may legitimately")
    print("need fewer scales. It exists so the gap is a work list rather than an opinion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
