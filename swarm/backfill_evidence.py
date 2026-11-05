#!/usr/bin/env python3
"""Re-type live claims whose evidence level the importer would now assign differently.

WHY THIS EXISTS. `import_design_space.refine_evidence` was added after the measured finding
that 12 xenobot parameters had been typed `literature` because a study declared their status
as 'sourced', when the stated source was a simulator config file. The function demotes those to
`assumed`. It was wired into the importer and never applied to the rows already in the graph,
so the defect it fixes is still sitting in the data: `g = 9.80665 m s^-2` from
`results/xenobot/cargo-work.json` is recorded as LITERATURE. Fixing the writer does not fix
what was already written, and nothing re-reads old rows.

It found them because ASK-artifact-graph rule 2 was red -- `evidence='literature'` with no
`read_level` -- which is the shape a mis-typed row takes: there is no read level because
nobody read anything, because there is no publication.

WHAT IT WILL NOT DO. It does not invent a read_level for a row it cannot re-type. A claim that
really is literature and really has no recorded read level is a GAP, and this prints it as one
rather than filling it in. Guessing `abstract` to clear a red would be exactly the relaxation
that rule exists to catch.

It reuses refine_evidence rather than restating its rules, so the backfill and the importer
cannot drift apart (the restated-vocabulary failure, AGENTS.md 6c).
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from design_chain import env                                 # noqa: E402
from import_design_space import refine_evidence              # noqa: E402

PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm",
      "-d", "designswarm", "-tAq", "-P", "pager=off"]
SEP = "|@|"


def q(sql: str) -> list[str]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:400])
    return [ln for ln in r.stdout.strip().split("\n") if ln]


def lit(s: str) -> str:
    return "'" + str(s).replace("'", "''") + "'"


def controls_pass() -> tuple[bool, str]:
    """Arms this backfill MUST change, arms it MUST NOT, and the mistake that produced them.

    THE SECOND GROUP IS NOT DECORATION. The first version of this module passed the claim's
    `source` COLUMN -- a file path -- to refine_evidence, matched `.json`, and demoted 16 rows
    of which 13 cite real publications. Its control arm passed a file path too, so it confirmed
    the call it was written beside instead of challenging it. A control built from the same
    misunderstanding as the code cannot see the misunderstanding. These arms are therefore the
    real statements from the rows that were wrongly demoted.
    """
    must_change = [
        ("Defined value of standard gravity", "assumed"),
        ("standard gravity, used only in the closed-form friction work", "assumed"),
    ]
    must_keep = [
        ("onimaru2016 Methods, 'Parameter values were beta=8, ...' for Figs 4-5", "literature"),
        ("Gumuskaya et al. 2023 report 5-50 um/s for anthrobots (PMID 38032125)", "literature"),
        ("Handbook value for dry air at 20 C and 101.3 kPa.", "literature"),
    ]
    for text, want in must_change + must_keep:
        got = refine_evidence("literature", text)[0]
        if got != want:
            return False, f"{text[:44]!r} -> {got!r}, expected {want!r}"
    if refine_evidence("measured", "Defined value of standard gravity")[0] != "measured":
        return False, "a `measured` row was altered; this must only touch `literature`"
    return True, (f"{len(must_change)} demoted, {len(must_keep)} kept (incl. the 13 rows the "
                  f"first version wrongly demoted), `measured` untouched")


def main() -> int:
    write = "--write" in sys.argv
    ok, why = controls_pass()
    print("=" * 78)
    print("EVIDENCE BACKFILL -- apply the importer's current typing to rows already stored")
    print("=" * 78)
    print(f"  [{'ok' if ok else 'FAIL'}] controls: {why}")
    if not ok:
        print("\n  ABORTING: without both arms a 'nothing to change' result is meaningless.")
        return 2
    if not write:
        print("  DRY RUN -- pass --write to apply")

    rows = q(f"""select id || '{SEP}' || project_id || '{SEP}'
                     || coalesce(substring(statement from 'SOURCE AS STATED[^:]*: (.*)$'), '')
                 from claim
                 where superseded_by is null and evidence = 'literature'
                   and read_level is null
                 order by id""")
    print(f"\n  {len(rows)} live literature claim(s) with no read_level\n")

    changed, residue, nosrc = [], [], []
    for line in rows:
        cid, proj, stated = line.split(SEP, 2)
        stated = stated.strip()
        if not stated:
            # NO DECLARED SOURCE TEXT. Do NOT fall back to the `source` column: that column
            # holds the file the row was imported from, and judging by it is the exact error
            # that demoted 13 published parameters. A row with nothing to judge is residue.
            nosrc.append((cid, proj))
            continue
        new_ev, note = refine_evidence("literature", stated)
        if new_ev != "literature":
            changed.append((cid, proj, stated, new_ev))
            print(f"  claim {cid:>4} {proj:<16} literature -> {new_ev:<9} {stated[:44]}")
            if write:
                q(f"""update claim set evidence = {lit(new_ev)},
                          statement = statement || {lit(note)}
                      where id = {int(cid)}""")
        else:
            residue.append((cid, proj, stated))

    print("\n" + "-" * 78)
    print(f"  {len(changed)} re-typed{'' if write else ' (dry run)'}; "
          f"{len(residue)} genuinely literature; {len(nosrc)} with no declared source text")
    if residue:
        print("\n  GENUINELY LITERATURE, READ LEVEL UNRECORDED -- a REPORTED GAP, not a")
        print("  cleared one. Each names a real publication but nothing records how deeply it")
        print("  was read. Supplying a read_level here would fabricate provenance.")
        for cid, proj, stated in residue:
            print(f"     claim {cid:>4} {proj:<16} {stated[:52]}")
    if nosrc:
        print("\n  NO DECLARED SOURCE TEXT -- cannot be judged by this rule at all:")
        for cid, proj in nosrc:
            print(f"     claim {cid:>4} {proj}")
    print("-" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
