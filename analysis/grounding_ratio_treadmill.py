#!/usr/bin/env python3
"""Is the `grounded, non-fabricated claims` row reachable, and what moves it?

The row reports `measured` claims carrying a biological scale as a fraction of ALL live claims,
and gates at 20 per cent. The numerator is the right thing to want: measurements about the
ANIMAL rather than about this project's tooling. The DENOMINATOR is every live claim of every
evidence kind, and the project produces literature, derived and simulated claims far faster than
it can produce biology measurements -- it has no wet lab, so almost everything about the organism
arrives as `literature` by construction.

That makes the ratio move the wrong way during ordinary work. This script measures by how much,
using a harvest that actually happened rather than a hypothetical.

IT DOES NOT PROPOSE RELAXING THE GATE. Changing a denominator to make a red row green is exactly
what the project forbids. The gate stays as it is; this records what it is measuring so the
choice of threshold can be made with the number in hand.

    python3 analysis/grounding_ratio_treadmill.py [--write]
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))
from dbq import q, write_claim                                      # noqa: E402

PROJECT = "zebrafish-flight"
THRESHOLD = 0.20
QFILE = "questions_gaps4.txt"


def main() -> int:
    live = int(q(f"""select count(*) from claim where project_id='{PROJECT}'
                     and superseded_by is null""")[0][0])
    bio = int(q(f"""select count(*) from claim where project_id='{PROJECT}'
                    and superseded_by is null and evidence='measured'
                    and scale_id is not null""")[0][0])
    harvest = int(q(f"""select count(*) from claim where project_id='{PROJECT}'
                        and superseded_by is null and statement like '%{QFILE}%'""")[0][0])
    bio_h = int(q(f"""select count(*) from claim where project_id='{PROJECT}'
                      and superseded_by is null and statement like '%{QFILE}%'
                      and evidence='measured' and scale_id is not null""")[0][0])

    now = bio / live
    before = bio / (live - harvest) if live > harvest else 0.0
    need = int(THRESHOLD * live) - bio
    print(f"\n  live claims {live}, measured-and-scaled {bio}  ->  {100*now:.2f}%")
    print(f"  gate is {100*THRESHOLD:.0f}%, so it needs {need} more such claims AT TODAY'S SIZE")
    print(f"\n  ONE HARVEST, measured rather than supposed: {QFILE} contributed {harvest} live")
    print(f"  claim(s), of which {bio_h} are measured-and-scaled.")
    print(f"    ratio without that harvest : {100*before:.2f}%")
    print(f"    ratio with it              : {100*now:.2f}%")
    print(f"    the harvest moved the row  : {100*(now-before):+.2f} points")
    print("\n  Each such harvest raises the denominator and not the numerator, so the gate")
    print("  recedes as the project does ordinary work. For every 1 literature claim added,")
    print(f"  {THRESHOLD/(1-THRESHOLD):.2f} measured-biology claims are needed just to hold station.")

    if "--write" not in sys.argv:
        print("\n  (dry run; pass --write to record a claim)")
        return 0
    cid = write_claim(
        PROJECT, None,
        f"""[THE `grounded, non-fabricated claims` GATE RECEDES WHEN THE PROJECT DOES ORDINARY
WORK: ONE HARVEST MOVED IT {100*(now-before):+.2f} POINTS, ALL OF IT DOWNWARD]
The row counts `measured` claims carrying a biological scale as a fraction of ALL live claims and
gates at {100*THRESHOLD:.0f} per cent. The numerator is the right thing to want -- measurement
about the ANIMAL rather than about this project's tooling, which is the drift claim 513 named.
The denominator is every live claim of every evidence kind.

This project has no wet lab, so nearly everything about the organism arrives as `literature` by
construction, and literature, derived and simulated claims accumulate far faster than biology
measurements can. Measured rather than supposed: the {QFILE} harvest contributed {harvest} live
claims, {bio_h} of them measured-and-scaled. The ratio was {100*before:.2f} per cent without it
and is {100*now:.2f} per cent with it. One ordinary harvest cost {abs(100*(now-before)):.2f}
points.

At today's size the gate needs {need} further measured-biology claims, and that target GROWS
with every claim of any kind the project records: holding station costs
{THRESHOLD/(1-THRESHOLD):.2f} measured-biology claims for each literature claim added.

THIS IS NOT A PROPOSAL TO CHANGE THE DENOMINATOR. Relaxing a criterion to turn a red row green
is forbidden here, and the row is red for a real reason: {bio} of {live} is genuinely thin
grounding. What is recorded is that the metric is partly a measure of HARVEST VOLUME, so its
movement cannot be read as a change in empirical grounding, and a reader comparing it across
dates is comparing two corpus sizes as much as two bodies of evidence.

SCOPE: one project, one harvest file. The before-ratio holds the numerator fixed while removing
the harvest from the denominator, which is correct only because that harvest contributed
{bio_h} to the numerator.""",
        "measured", 100.0 * (now - before), "percentage points moved by one harvest",
        "analysis/grounding_ratio_treadmill.py", None)
    print(f"\n  recorded claim {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
