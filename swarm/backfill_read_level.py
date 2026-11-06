#!/usr/bin/env python3
"""Assign the missing read_level on literature claims by a STATED convention.

CONVENTION: where a claim synthesises sources read at different depths, its single read_level
is the WEAKEST level its CONCLUSION depends on. A claim is only as strong as its weakest
load-bearing source, and recording the strongest would be the "summarise an abstract in the
voice of having read the paper" failure docs/research/README.md exists to prevent.

Each assignment below quotes the claim's own words that fix its level.
"""
import sys
sys.path.insert(0, "swarm")
from dbq import PG, env, lit, q  # noqa: E402
import subprocess  # noqa: E402

ASSIGN = {
    127: ("full-text",
          "rests on Azevedo et al. 2011 'Fig 4L/M, read off plot +-0.5 um' -- reading a figure "
          "panel and its error bars is a full-text read, and it is the claim's KEY value"),
    204: ("search-summary",
          "the conclusion is a NEGATIVE over the published literature ('No pectoral-restricted "
          "regulatory element adequate ... is published', KEY '0 named elements'); the per-element "
          "detail is deeper, but what the conclusion depends on is the completeness of the search"),
    233: ("search-summary",
          "the conclusion is a negative over the edit catalogue -- 'six required slots ... contain "
          "no demonstrated zebrafish edit, so a minimal edit stack ... cannot be written'"),
    261: ("could-not-access",
          "the claim names its own limiting source verbatim: 'Flammang's body text could not be "
          "accessed', and states the conclusion is 'most sensitive to an unmeasured premise' about "
          "that ray's size. The Alben re-read is full-text, but the conditional rests on the gap"),
    267: ("abstract",
          "Alben 2007 is read at full text ('authors state EI ~1e-6 to 1e-5'), but the quantity "
          "being corrected is Flammang's, and the claim says '565e-6 stays the ABSTRACT's printed "
          "value' -- the abstract is the load-bearing read for the number under dispute"),
    308: ("search-summary",
          "an explicit negative search with its date and scope in the claim: 'KEY: 0 peer-reviewed "
          "experiments pairing a membrane-potential manipulation ... (searched 2026-11-04)'"),
    605: ("listing",
          "not a study read at all: a handbook value for dry air at 20 C and 101.3 kPa, taken from "
          "a reference listing. Recording it as full-text or abstract would claim a paper was read"),
}

VOCAB = ("full-text", "abstract", "listing", "search-summary", "could-not-access")


def main() -> int:
    write = "--write" in sys.argv
    rows = {int(r[0]): r for r in q(
        "select id, coalesce(evidence,'<NULL>'), coalesce(read_level,'<NULL>') from claim "
        "where superseded_by is null and (evidence is null or "
        "(evidence='literature' and read_level is null))")}
    print(f"  {len(rows)} non-compliant row(s); {len(ASSIGN)} assignment(s) prepared\n")
    missing = set(rows) - set(ASSIGN)
    extra = set(ASSIGN) - set(rows)
    if missing:
        print(f"  REFUSING: rows with no assignment: {sorted(missing)}")
        return 2
    if extra:
        print(f"  NOTE: assignments for rows already compliant (skipped): {sorted(extra)}")
    bad = [c for c, (lv, _) in ASSIGN.items() if lv not in VOCAB]
    if bad:
        print(f"  REFUSING: level outside the vocabulary for {bad}")
        return 2
    for cid in sorted(rows):
        lv, why = ASSIGN[cid]
        print(f"  claim {cid:>4} -> {lv}")
        print(f"            {why}")
        if write:
            r = subprocess.run(
                PG + ["-c", f"update claim set read_level={lit(lv)} where id={cid} "
                             f"and read_level is null returning id"],
                capture_output=True, text=True, env=env(), timeout=60)
            print(f"            updated: {r.stdout.strip() or 'NO ROW'}")
    if not write:
        print("\n  dry run; pass --write to apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
