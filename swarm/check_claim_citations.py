#!/usr/bin/env python3
"""Commit messages that cite a claim id which does not resolve.

WHY. On 2026-11-05 commit e041ca7e announced "claim 1075". The insert had failed --
`evidence='could-not-access'` is a READ_LEVEL value, not an evidence value -- and no claim 1075
was ever created. The message was pushed asserting an id that resolves to nothing.

That is the same failure the repository already guards against for commit SHAs: a citation
reads as provenance and only fails when somebody tries to resolve it, which nobody does for an
id that looks fine. SHAs have a checker. Claim ids did not.

WHAT IT CHECKS: phrases that cite a claim in this project's own conventions -- "claim 1075",
"claims 1072 and 1073", "(claim 1075)" -- against the claim table. A citation to a claim that
does not exist is a HARD failure. A citation to a SUPERSEDED claim is reported separately and
is not a failure: commit messages legitimately discuss claims that were later superseded, and
most of this project's history does.

WHAT IT DELIBERATELY DOES NOT DO: match bare numbers. "1075" appears in dates, counts, byte
sizes and PMIDs, and a checker that flagged those would be switched off within a day -- the
same reasoning the SHA checker records for being phrase-anchored rather than clever.

    python3 check_claim_citations.py [N]      # last N commits, default 40
"""
from __future__ import annotations

import re
import subprocess
import sys

from dbq import q

CITE = re.compile(r"\bclaims?\s+((?:\d{3,4})(?:\s*(?:,|and|&)\s*\d{3,4})*)", re.I)


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 40
    log = subprocess.run(["git", "log", f"-{n}", "--format=%H%x01%B%x02"],
                         capture_output=True, text=True, timeout=120).stdout
    commits = [c for c in log.split("\x02") if c.strip()]
    live = {int(r[0]) for r in q("select id from claim")}
    sup = {int(r[0]) for r in q("select id from claim where superseded_by is not null")}

    # THE CLAIMING-VS-QUOTING TRAP, HIT ON THE FIRST RUN. The commit that CORRECTS a bad
    # citation has to name the bad id to explain it, so this checker flagged the correction
    # for quoting the thing it was correcting -- 0ecec4ab, twice. A forbidden-string check
    # cannot tell asserting from quoting, which this repository already records for its
    # delivery-path scanner and its spec sweep.
    #
    # The exemption is explicit and narrow rather than clever: a commit whose message states
    # that an id does not exist is a correction, and its citations to missing ids are the
    # subject rather than a defect. Anything subtler would be guessing at intent.
    CORRECTION = re.compile(r"does not exist|never (?:created|recorded)|resolves to nothing",
                            re.I)

    missing, superseded, checked, exempt = [], [], 0, 0
    for c in commits:
        sha, _, body = c.strip().partition("\x01")
        is_correction = bool(CORRECTION.search(body))
        for m in CITE.finditer(body):
            for tok in re.findall(r"\d{3,4}", m.group(1)):
                cid = int(tok)
                checked += 1
                if cid not in live:
                    if is_correction:
                        exempt += 1
                    else:
                        missing.append((sha[:8], cid, body.splitlines()[0][:70]))
                elif cid in sup:
                    superseded.append((sha[:8], cid))

    print(f"  {len(commits)} commits, {checked} claim citations checked\n")
    if missing:
        print(f"  FAIL: {len(missing)} citation(s) to a claim that does not exist")
        for sha, cid, subj in missing:
            print(f"    {sha}  claim {cid}  -- {subj}")
    else:
        print("  OK: every cited claim id resolves")
    print(f"\n  (for information: {len(superseded)} citations point at superseded claims, "
          f"which is normal and not a failure)")
    print(f"  ({exempt} citation(s) to missing ids are inside CORRECTION commits, which must "
          f"name the bad id to explain it)")

    print("\n  CONTROLS")
    # must-flag: an id that cannot exist
    top = int(q("select max(id) from claim")[0][0])
    probe = f"this mentions claim {top + 5000} which cannot exist"
    hits = [int(t) for m in CITE.finditer(probe) for t in re.findall(r"\d{3,4}", m.group(1))]
    print(f"    a message citing claim {top+5000}: parsed {hits}, "
          f"resolves = {bool(set(hits) & live)} "
          f"{'OK, would be flagged' if hits and not (set(hits) & live) else 'NOT FLAGGED'}")
    # must-not-flag: a bare number is not a citation
    probe2 = "the file is 1075 bytes and PMID 38232499 was retrieved"
    hits2 = [t for m in CITE.finditer(probe2) for t in re.findall(r"\d{3,4}", m.group(1))]
    print(f"    a message with a bare number and a PMID: parsed {hits2} "
          f"{'OK, not treated as citations' if not hits2 else 'FALSE POSITIVE'}")
    # must-flag: the real historical case
    probe3 = "Record the access attempt on the paper that could answer S904 (claim 1075)"
    hits3 = [int(t) for m in CITE.finditer(probe3) for t in re.findall(r"\d{3,4}", m.group(1))]
    print(f"    the actual e041ca7e subject: parsed {hits3}, resolves = "
          f"{bool(set(hits3) & live)} {'OK, would be flagged' if hits3 and not (set(hits3) & live) else 'MISSED'}")
    # must-not-flag: the correction commit's own text
    probe4 = "it cited claim 1075, which does not exist; the claim is 1076"
    print(f"    the correction commit's own text is exempt: "
          f"{bool(CORRECTION.search(probe4))} (must be True)")
    # must-flag: a correction-looking phrase must not exempt an UNRELATED bad citation in
    # another commit -- the exemption is per commit, so this is a scoping check
    print(f"    the exemption is per-commit, not global: "
          f"{not CORRECTION.search('Record the access attempt (claim 1075)')} (must be True)")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
