#!/usr/bin/env python3
"""Report how many `measured` claims are about the ANIMAL and how many about this SWARM.

WHY, measured 2026-11-05. goal_status.py's grounded-claims row reports "49 of 543 live claims
are `measured` AND carry a biological scale; 169 are `measured` in all, so 120 measure this
PROJECT (tooling, panels, generators) rather than the animal". That reads as though scale_id
separates the two. It does not: of the 49, twenty-five name only this repository's own code or a
Nebius operation in their `source`, and thirteen name neither code nor a citation. Read, they
include

    [organism] "THE PANEL IS NOT ORDER-BIASED: 24/24 CORRECT, 0/12 FLIPS"
    [organism] "THE REFINEMENT LOOP'S ACTUAL RATE: 18% OF TONIGHT'S CLAIMS WERE LATER CORRECTED"
    [protein]  "THE PARTNER CHAIN DOES NOT CAUSE THE INTERFACE CONSTRAINT -- SUPERSEDES 1048"

all of which measure this swarm while carrying an organism- or protein-scale tag. scale_id
answers "what scale is this claim ABOUT", and a claim about predicting a protein is loosely about
a protein, so the tag is not wrong -- it simply does not carry the distinction the row needs.

WHAT THIS IS NOT. It does not write a field, and it deliberately does not. A regex-populated
`subject` column would look authoritative on a question that needs reading: the honest output of
a heuristic this crude is a LIST SOMEONE READS, not a value other code consumes. Nothing here
feeds a threshold, and the grounded-claims row is left exactly as it is -- a redefinition
proposed by whoever is adding claims to the corpus is not a redefinition worth having.

HOW IT DECIDES, and both directions of its error are known:
  - a `source` naming a paper, accession or database  -> about the ANIMAL
  - a `source` naming only this repo's code or an operation id -> about the SWARM
  - neither -> UNDECIDED, printed in full for reading
A claim citing a paper for a fact about the pipeline is counted as ANIMAL, which errs generous;
a biological measurement recorded with only a script name as its source is counted as SWARM,
which errs strict. Both are listed so the counts can be disagreed with.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbq  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

SWARM = re.compile(r"\.py\b|analysis/|swarm/|scripts/|studio/|op-[0-9a-f]{8}|panel|studio|"
                   r"endpoint|this repo|module|backlog", re.I)
ANIMAL = re.compile(r"PMC\d|PMID|doi:|ENSDAR|\bNP_\d|\bNM_\d|UniProt|et al\.|J Exp Biol|"
                    r"Ensembl|GenBank|accession", re.I)


def rows(evidence: str | None = None):
    where = f"project_id = {dbq.lit(PROJECT)} and superseded_by is null"
    if evidence:
        where += f" and evidence = {dbq.lit(evidence)}"
    return dbq.q(
        "select id::text, coalesce(scale_id,''), coalesce(evidence,''), "
        "replace(replace(coalesce(source,''), chr(1), ' '), chr(10), ' '), "
        "replace(replace(left(statement,150), chr(1), ' '), chr(10), ' ') "
        f"from claim where {where} order by id")


def bucket(source: str) -> str:
    a, s = bool(ANIMAL.search(source)), bool(SWARM.search(source))
    if a:
        return "animal"            # generous on purpose; see the docstring
    if s:
        return "swarm"
    return "undecided"


def main() -> int:
    scoped = "--scaled-only" in sys.argv
    all_rows = rows("measured")
    if scoped:
        all_rows = [r for r in all_rows if r[1]]
    counts = {"animal": 0, "swarm": 0, "undecided": 0}
    undecided = []
    for r in all_rows:
        b = bucket(r[3])
        counts[b] += 1
        if b == "undecided":
            undecided.append(r)

    print("=" * 78)
    print(f"MEASURED CLAIMS: ABOUT THE ANIMAL, OR ABOUT THIS SWARM?   project {PROJECT!r}")
    print("=" * 78)
    print(f"  {len(all_rows)} `measured` claim(s)" + (" carrying a scale" if scoped else ""))
    for k in ("animal", "swarm", "undecided"):
        print(f"    {k:<10} {counts[k]:>4}")
    if all_rows:
        print(f"\n  So at most {counts['animal'] + counts['undecided']} and at least "
              f"{counts['animal']} of them are about the organism. The scoreboard's "
              f"grounded-claims row counts all {len(all_rows)}.")
    print("\n  THE UNDECIDED ONES, IN FULL, BECAUSE A HEURISTIC THIS CRUDE OWES YOU THE LIST:")
    for r in undecided[:25]:
        print(f"    {r[0]:>5} [{r[1] or '-':<9}] {r[4][:92]}")
    if len(undecided) > 25:
        print(f"    ... and {len(undecided) - 25} more")
    print("\n  Nothing here writes a field or feeds a threshold. It reports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
