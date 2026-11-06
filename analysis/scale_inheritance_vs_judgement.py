#!/usr/bin/env python3
"""Measure whether an INHERITED scale agrees with a JUDGED one, on the same claims.

`claim.scale_id` had two writers with different meanings. classify_scale.py places a claim
"at the biological scale it is ABOUT" -- a judgement about the claim's own content.
claims_from_extraction.py knew only which QUESTION fetched the row, and wrote the scale that
question's originating constraint declared. Those two coincide only when the harvest is on
topic, and nothing checked that it was.

The second writer also PRE-EMPTED the first: classify_scale.py selects `where scale_id is
null`, so once an inherited value was present no content judgement would ever visit that claim.

This script reports the agreement rate between the two on the gaps4 harvest, where both are
available: the map file gives the inherited label, the column now holds the judged one.

    python3 analysis/scale_inheritance_vs_judgement.py            # report
    python3 analysis/scale_inheritance_vs_judgement.py --write    # and record a claim
"""
import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))
from dbq import q, write_claim                                      # noqa: E402

PROJECT = "zebrafish-flight"
QFILE = "questions_gaps4.txt"
MAP = pathlib.Path("results/extract") / f"{QFILE}.map.json"
ASKED = re.compile(rf"asked: question (\d+) of {re.escape(QFILE)}")


def rows() -> list[tuple[str, str | None, str | None]]:
    """(claim id, inherited scale or None, judged scale or None) for every gaps4 claim."""
    m = json.loads(MAP.read_text())
    out = []
    for cid, judged, stmt in q(
        f"""select id::text, scale_id, replace(statement, chr(10), ' ') from claim
            where project_id = '{PROJECT}' and statement like '%{QFILE}%' order by id"""):
        g = ASKED.search(stmt)
        sc = (m.get(g.group(1)) or {}).get("scales") or [] if g else []
        out.append((cid, sc[0] if len(sc) == 1 else None, judged))
    return out


def main() -> int:
    r = rows()
    both = [(i, a, b) for i, a, b in r if a and b]
    agree = sum(1 for _, a, b in both if a == b)
    unjudged = sum(1 for _, _, b in r if not b)
    inh = collections.Counter(a for _, a, _ in r if a)
    jud = collections.Counter(b for _, _, b in r if b)
    pairs = collections.Counter(f"{a} -> {b}" for _, a, b in both if a != b)

    print(f"\n  {QFILE}: {len(r)} claim(s)")
    print(f"  both labels available: {len(both)}   "
          f"left unjudged by the classifier (NONE / refused): {unjudged}")
    print(f"\n  AGREE {agree} of {len(both)}"
          + (f"  ({100*agree/len(both):.1f}%)" if both else ""))
    print(f"\n  inherited distribution: {dict(inh)}")
    print(f"  judged distribution:    {dict(jud)}")
    print("\n  most common disagreements:")
    for k, c in pairs.most_common(8):
        print(f"    {k:<28} {c}")

    if "--write" not in sys.argv:
        print("\n  (dry run; pass --write to record a claim)")
        return 0
    if not both:
        print("\n  NOT recording: no claim carries both labels, so there is nothing to compare.")
        return 1

    top = "; ".join(f"{k} ({c})" for k, c in pairs.most_common(4))
    cid = write_claim(
        PROJECT, None,
        f"""[AN INHERITED SCALE AND A JUDGED ONE AGREE ON {agree} OF {len(both)} CLAIMS, SO THE TWO
WRITERS OF claim.scale_id WERE NOT MEASURING THE SAME THING]
`claim.scale_id` had two writers. classify_scale.py places a claim at the biological scale it
is ABOUT, judging the claim's own text. claims_from_extraction.py wrote the scale declared by
the constraint behind whichever QUESTION fetched the row, which is provenance, not content.
Both wrote the same column and nothing distinguished them.

Measured on the {QFILE} harvest, the only set where both labels exist: {len(both)} claims carry
an inherited label and a judged one, and they agree on {agree}. The commonest disagreements are
{top}. Inherited distribution {dict(inh)}; judged {dict(jud)}. {unjudged} claim(s) the
classifier declined to place (NONE or API refusal) are excluded, because a missing judgement is
not a disagreement.

The inherited writer also PRE-EMPTED the judging one: classify_scale.py selects `where scale_id
is null`, so an inherited value meant no content judgement would ever visit that claim. The
agreement rate is therefore the rate at which that silent substitution was harmless.

claims_from_extraction.py no longer writes an inherited scale. Nothing is lost: the statement
carries `asked: question N of <qfile>` and the map file is committed beside the harvest, so the
constraint's scale stays recoverable from the join those two make.

SCOPE: one harvest file on one project. It does not measure how often harvests are off topic in
general, and the judged labels are a model's, checked only by classify_scale.py's own control.""",
        "measured", 100.0 * agree / len(both), "percent agreement",
        "analysis/scale_inheritance_vs_judgement.py", None)
    print(f"\n  recorded claim {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
