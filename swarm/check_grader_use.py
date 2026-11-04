#!/usr/bin/env python3
"""SWEEP (not a gate): live claims that may reason from a grader the calibration table distrusts.

READ EVERY HIT. Roughly 7 in 8 are false positives. That number is measured, not estimated, and
the reason it cannot be improved is the point of this file.

WHY IT EXISTS. SPEC-evaluation-kernel rule 3 says no grader may be aggregated without a calibration
that caught a known-bad item. That rule CANNOT BITE, and the spec checker says so honestly: its
control query is `select count(*) from grade`, which returns 0, so the rule reports UNCHECKED
rather than PASS. The kernel assumes grading happens by inserting `grade` rows. In this project
grading happens INSIDE CLAIM PROSE -- a grader is used by reasoning from it, never by writing a
row. So the one mechanism meant to stop an uncalibrated grader being trusted watches a table
nothing writes to.

It cost something real. ESMFold2 pLDDT deltas were used in claim 402 to conclude the designed edit
T200K is "tolerated by the fold". That grader was calibrated afterwards, on 2026-11-04, against a
known-bad item it did not catch; it is now `untrusted` (grader_calibration id 3) and 402 is
superseded by 462. Nothing in the pipeline noticed in between.

THREE BRIDGES WERE TRIED AND ALL THREE FAIL, which is why this is a sweep and not a gate:

  * through `grade`      -- 0 rows, so the rule is vacuous
  * through claim PROSE  -- two formulations measured. Requiring "esmfold2" and "plddt" flagged 10
                            claims, 8 of them false; adding a substitution pattern and an exclusion
                            flagged 8, 7 of them false. The failures are not sloppiness: claims 26
                            and 400 are about MSA DEPTH, 447 and 449 about artifacts and alignment
                            files, 461 and 464 use pLDDT as BACKBONE QUALITY. Separating "pLDDT as
                            fold confidence" from "pLDDT delta judging a mutation" requires reading
                            the inference, which a pattern cannot do.
  * through `source`     -- all 266 live claims carry one, but it records DATA PROVENANCE ("Nebius
                            ESMFold2 op-...") and not inferential role. A claim may cite ESMFold2
                            for a fold-confidence number without grading any mutation.

THE STRUCTURAL FIX, not implemented here: nothing in the schema records WHICH GRADER A CLAIM'S
INFERENCE DEPENDS ON. Until a claim declares that, no query can enforce rule 3. Backfilling 266
claims would require judging each one's reasoning -- the very thing that cannot be automated -- so
the affordable version is forward-only: new claims that rest on a grader declare it.

This is AGENTS.md section 6c's rule in a new place: pin the positive fact, do not enumerate the bad
ones. The enumeration is what has an 87 percent false-positive rate.

    python3 check_grader_use.py           # sweep; exit 1 if there is anything to read
    python3 check_grader_use.py --control # must-flag / must-miss cases

--control is not decoration. A checker that has never flagged anything is indistinguishable from
one that cannot. But note what it does and does not establish: it proved the matcher RUNS, and
both versions above passed it while being useless. Controls prove execution, not precision; only
reading every hit showed the rate.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

# A grader's calibration row names it in prose; a claim refers to it in prose too, and the two
# spellings never match exactly. The link is therefore an explicit pattern per grader, kept here
# where a reviewer can disagree with a row rather than inferred by string similarity.
#
# THE FIRST VERSION OF THIS TABLE WAS USELESS AND ITS CONTROLS PASSED. It required only that
# "esmfold2" and "plddt" both appear, which flagged 10 claims of which 8 were false positives:
# claims 25, 410, 448 and 455 report pLDDT as FOLD CONFIDENCE, which is not the thing calibrated,
# and 460, 462 and 463 are the claims that ESTABLISH the grader is untrusted. A must-flag and a
# must-miss case prove the matcher RUNS; they say nothing about its precision, and only reading
# every hit showed the rate. AGENTS.md's own threshold says a gate with that rate gets switched
# off.
#
# So each grader now needs a THIRD signal: evidence the claim is comparing a mutant against a
# wild type, which is what was actually calibrated. `exclude` drops the claims whose subject is
# the calibration itself -- those are the finding, not a violation of it.
GRADERS = [
    ("esmfold2-plddt-delta", r"esmfold2|pl?ddt",
     r"\b[acdefghiklmnpqrstvwy]\d{1,4}[acdefghiklmnpqrstvwy]\b|mutant|substitution|wild[- ]type",
     r"cannot assess|untrusted|anti-correlated|did not catch|not a stable statistic"),
    ("proteinmpnn-rank", r"proteinmpnn", r"\brank(s|ed)?\b",
     r"not a stable statistic|unstable|noise|cannot adjudicate"),
]


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def untrusted() -> dict[str, tuple[str, str]]:
    """Graders whose calibration did not catch a known-bad item, or is only provisional."""
    out = {}
    for key, a, b, _excl in GRADERS:
        rows = q(f"""select verdict, coalesce(caught_known_bad,0), coalesce(n_known_bad,0)
                     from grader_calibration where grader ilike '{key}%'
                     order by measured_at desc limit 1""")
        if not rows:
            out[key] = ("uncalibrated", "no calibration row at all")
            continue
        verdict, caught, nbad = rows[0][0], int(rows[0][1]), int(rows[0][2])
        if verdict == "untrusted" or (int(nbad) > 0 and caught == 0):
            out[key] = (verdict, f"caught {caught} of {nbad} known-bad")
        elif verdict == "provisional":
            out[key] = (verdict, f"caught {caught} of {nbad} known-bad; provisional")
    return out


def matches(key: str, text: str) -> bool:
    """True when the claim REASONS FROM the grader, not merely when it mentions it."""
    for k, a, b, excl in GRADERS:
        if k == key:
            t = text.lower()
            if excl and re.search(excl, t):
                return False       # the claim's subject IS the calibration; it is the finding
            return bool(re.search(a, t) and re.search(b, t))
    return False


def scan(live_only: bool = True) -> list[tuple[str, str, str, str]]:
    cond = "and c.superseded_by is null" if live_only else ""
    rows = q(f"""select c.id, replace(coalesce(c.statement,''), '{SEP}', ' ')
                 from claim c where c.project_id='{PROJECT}' {cond} order by c.id""")
    hits = []
    for cid, stmt in rows:
        for key, (verdict, why) in untrusted().items():
            if matches(key, stmt):
                hits.append((cid, key, verdict, why))
    return hits


def control() -> int:
    """A must-flag case and a must-miss case, both from real history."""
    ok = True
    bad = q("select replace(statement, '%s', ' ') from claim where id=402" % SEP)
    if not bad:
        print("  CONTROL CANNOT RUN: claim 402 is absent")
        return 2
    if matches("esmfold2-plddt-delta", bad[0][0]):
        print("  must-flag  claim 402 (reasons from an ESMFold2 pLDDT delta): FLAGGED  ok")
    else:
        print("  must-flag  claim 402: NOT FLAGGED  *** the matcher is broken ***")
        ok = False
    clean = "The codon at position 200 is ACA and T200K requires a single C-to-A transversion."
    if matches("esmfold2-plddt-delta", clean):
        print("  must-miss  a DNA-scale claim: FLAGGED  *** false positive ***")
        ok = False
    else:
        print("  must-miss  a DNA-scale claim mentioning neither: not flagged  ok")
    return 0 if ok else 1


def main() -> int:
    if "--control" in sys.argv:
        return control()
    u = untrusted()
    if not u:
        print("  no untrusted or provisional graders; nothing to check. "
              "That is not a pass -- it means the calibration table has nothing to say.")
        return 0
    print("  graders not cleared for aggregation:")
    for k, (v, why) in u.items():
        print(f"    {k:26} {v:12} {why}")
    hits = scan()
    print()
    if not hits:
        print("  no LIVE claim matched. That is not a clean bill: the sweep is ~7/8 false positive and cannot see an inference it has no field for.")
    for cid, key, verdict, why in hits:
        print(f"  claim {cid:>4} uses {key} ({verdict})")
    print()
    rc = control()
    return 1 if hits else rc


if __name__ == "__main__":
    sys.exit(main())
