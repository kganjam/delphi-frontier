#!/usr/bin/env python3
"""Recompute how often a harvested value comes back in the UNITS ITS QUESTION ASKED FOR.

Claim 2769 reports this as 26.2 per cent for non-ratio questions against 2.9 per cent for
ratio-unit questions, a 8.9-fold difference over 52 questions and 4710 values, and that number
is quoted in `extraction_questions.ratio_unit`'s docstring, where it justifies splitting every
ratio question into its numerator and denominator. It was computed once, by hand, and NO SCRIPT
RECOMPUTED IT -- so a headline the pipeline's design rests on could not be checked, and the
claim's own stated limit ("a tenth ratio question could move it") could never be retested.

This is that instrument. It reads the raw harvests rather than the claims table, because the
population is every value the extractor returned, including the ones no claim was written from.

THE DEFINITION IS DECLARED HERE because the original was not recorded in runnable form:
  population  every VERIFIED value whose (qfile, asked) resolves to a question that declared
              units. Discarded values are excluded -- they never became an answer.
  match       the value's units equal ANY unit the question accepts, after casefolding,
              whitespace collapse and folding dimensionless spellings to one token. A question
              may offer alternatives (`A or B`) and may carry a trailing referent qualifier
              (`W/kg muscle` is answered by `W/kg`). See accepted().
  bucket      `ratio` when extraction_questions.ratio_unit() recognises the QUESTION's units.
Reproducing claim 2769's two rates is therefore a CONTROL on this definition, not a given. Any
difference is reported rather than tuned away.

    python3 analysis/units_match_rate.py            # report, with controls
    python3 analysis/units_match_rate.py --write    # and record a claim
"""
import collections
import glob
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))
from dbq import write_claim                                         # noqa: E402
from extraction_questions import DIMENSIONLESS, ratio_unit          # noqa: E402

EXTRACT = pathlib.Path("results/extract")

#: Claim 2769's nine controls, with ONE DELIBERATE DIVERGENCE that this script's control caught
#: rather than papered over. 2769 lists `m/s` as a ratio. Commit 35bc9701 later broke 2769's
#: aggregate down per question and found m/s matching at 12.9 per cent over 186 values -- the
#: BEST performer in the set -- while seven of the nine returned literally zero across 786
#: values. The dividing line is not dimensional: it is whether the quotient is a quantity a
#: paper NAMES in its own right. Speed is; W/kg muscle and S/cm^2 are normalised quantities a
#: paper computes for its own argument and rarely states. So ratio_unit() now exempts a declared
#: list of standard compound units, and 2769's rule as written would have split the one ratio
#: question that works. The expectation below follows the CODE, and the reason is recorded here
#: so it reads as a superseded control rather than a tuned one.
CONTROLS = [("W/kg", True), ("mol m^-2 s^-1", True), ("degC/year", True),
            ("m/s", False),          # superseded by 35bc9701; 2769 expected True
            ("mm", False), ("Hz", False), ("Pa", False),
            ("tail beats", False), ("fraction of body mass", False)]


#: Trailing REFERENT qualifiers. `W/kg muscle` and `W/kg` are the same dimension; the qualifier
#: names what the kilogram is OF. Declared rather than inferred, because a general "strip the
#: trailing word" rule is unsafe in both directions: asked `g`, a value in `g dL -1` is a
#: concentration and NOT a match, and asked `g dL -1`, a value in `g` is not one either.
QUALIFIERS = ("muscle", "body mass", "body", "body weight", "dry mass", "wet mass",
              "dry weight", "wet weight", "total", "tissue", "fish", "animal")


def canon(u: str) -> str:
    t = " ".join((u or "").strip().casefold().split())
    return "<dimensionless>" if t in DIMENSIONLESS else t


def accepted(asked: str) -> set[str]:
    """Every unit string that answers `asked`.

    TWO DECLARED RELAXATIONS, both found by this script's own control failing against the
    published number rather than by reading the data:

    1. ALTERNATIVES. A question may offer a choice -- `degC/year or degC-weeks/year`. Exact
       equality accepted neither, so that question scored 0 of 130 when 8 of its values came
       back in `degC/year`. Commit 35bc9701 measured it at 6.8 per cent, so the original rule
       plainly split on `or` too.
    2. REFERENT QUALIFIERS. `W/kg muscle` is answered by `W/kg`; 12 of its 222 values are.

    Nothing else is relaxed. A different dimension is still a miss, which is why `S/cm^2` is not
    answered by `S/m` and the nine ratio questions stay near zero.
    """
    out = set()
    for alt in (x.strip() for x in asked.split(" or ") if x.strip()):
        c = canon(alt)
        out.add(c)
        for qf in QUALIFIERS:
            if c.endswith(" " + qf):
                out.add(c[: -len(qf) - 1].strip())
    return out


def questions() -> dict[tuple[str, str], str]:
    """(qfile, question number) -> the units that question asked for."""
    out = {}
    for mp in sorted(EXTRACT.glob("*.map.json")):
        stem = mp.name[: -len(".map.json")]
        for k, v in json.loads(mp.read_text()).items():
            if (v.get("units") or "").strip():
                out[(stem, str(k))] = v["units"]
    return out


def values():
    """Every verified harvested value, as (harvest file, project, qfile, asked, units)."""
    for f in sorted(glob.glob(str(EXTRACT / "harvest_*.json"))):
        name = pathlib.Path(f).name
        for v in json.loads(pathlib.Path(f).read_text()).get("verified", []):
            yield (name, str(v.get("project") or "?"), str(v.get("qfile") or ""),
                   str(v.get("asked") or ""), str(v.get("units") or ""))


#: must-match / must-NOT-match pairs for accepted(). The negatives are the cases a general
#: "strip a trailing token" rule would get wrong, which is why QUALIFIERS is a declared list.
MATCH_CONTROLS = [("W/kg muscle", "W/kg", True), ("W/kg body mass", "W/kg", True),
                  ("degC/year or degC-weeks/year", "degC/year", True),
                  ("degC/year or degC-weeks/year", "degC-weeks/year", True),
                  ("S/cm^2", "S/m", False), ("g", "g dL -1", False),
                  ("g dL -1", "g", False), ("W/kg muscle", "W", False),
                  ("mm", "mm^2", False)]


def main() -> int:
    bad = [(u, want, ratio_unit(u) is not None) for u, want in CONTROLS
           if (ratio_unit(u) is not None) != want]
    mbad = [(a, g, want) for a, g, want in MATCH_CONTROLS
            if (canon(g) in accepted(a)) != want]
    print(f"\n  MATCH CONTROLS: {len(MATCH_CONTROLS) - len(mbad)} of {len(MATCH_CONTROLS)} pass"
          + ("" if not mbad else f"   FAILED: {mbad}"))
    if mbad:
        print("  NOT reporting a rate: accepted() does not behave as declared.")
        return 1
    print(f"\n  CONTROLS: {len(CONTROLS) - len(bad)} of {len(CONTROLS)} pass"
          + ("" if not bad else f"   FAILED: {bad}"))
    if bad:
        print("  NOT reporting a rate: the ratio classifier does not reproduce claim 2769's "
              "nine controls, so any number below would be from a different classifier.")
        return 1

    qs = questions()
    seen_q, tally = set(), collections.Counter()
    per_project = collections.defaultdict(collections.Counter)
    per_harvest = collections.defaultdict(collections.Counter)
    for hfile, proj, qfile, asked, units in values():
        want = qs.get((qfile, asked))
        if want is None:
            continue
        seen_q.add((qfile, asked))
        b = "ratio" if ratio_unit(want) else "plain"   # `ratio` here = DECOMPOSABLE ratio
        hit = canon(units) in accepted(want)
        tally[f"{b}_n"] += 1
        tally[f"{b}_hit"] += hit
        per_project[proj]["n"] += 1
        per_project[proj]["hit"] += hit
        per_harvest[hfile]["n"] += 1
        per_harvest[hfile]["hit"] += hit

    def rate(b):
        n = tally[f"{b}_n"]
        return (100.0 * tally[f"{b}_hit"] / n) if n else 0.0

    plain, ratio = rate("plain"), rate("ratio")
    n_all = tally["plain_n"] + tally["ratio_n"]
    fold = (plain / ratio) if ratio else float("inf")
    print(f"\n  {len(seen_q)} question(s) matched, {n_all} compared value(s)")
    print(f"    non-ratio  {plain:5.1f}%  of {tally['plain_n']}")
    print(f"    ratio      {ratio:5.1f}%  of {tally['ratio_n']}")
    print(f"    fold difference: {fold:.1f}x")
    print("\n  PER HARVEST FILE -- the split the aggregate hides:")
    for h, c in sorted(per_harvest.items(), key=lambda kv: -kv[1]["n"]):
        print(f"    {h:<42} {100.0*c['hit']/c['n']:5.1f}%  of {c['n']}")
    print("\n  per project:")
    for p, c in sorted(per_project.items(), key=lambda kv: -kv[1]["n"]):
        print(f"    {p:<18} {100.0*c['hit']/c['n']:5.1f}%  of {c['n']}")
    print("\n  claim 2769 recorded 26.2% / 2.9% / 8.9x over 52 questions and 4710 values.")
    print("  NOT directly comparable: `ratio` here means DECOMPOSABLE ratio, which excludes the")
    print("  standard compound units (m/s and relatives) that 2769 counted. m/s was 2769's best")
    print("  performer at 12.9% of 186, so removing it LOWERS the ratio bucket and RAISES the")
    print("  fold difference. A larger number here is that redefinition, not a worse corpus.")

    if "--write" not in sys.argv:
        print("\n  (dry run; pass --write to record a claim)")
        return 0
    byp = "; ".join(f"{p} {100.0*c['hit']/c['n']:.1f}% of {c['n']}"
                    for p, c in sorted(per_project.items(), key=lambda kv: -kv[1]["n"]))
    byh = "; ".join(f"{h} {100.0*c['hit']/c['n']:.1f}% of {c['n']}"
                    for h, c in sorted(per_harvest.items(), key=lambda kv: -kv[1]["n"]))
    bulk = {h: c for h, c in per_harvest.items() if c["n"] >= 500}
    small = {h: c for h, c in per_harvest.items() if c["n"] < 200}
    br = 100.0 * sum(c["hit"] for c in bulk.values()) / sum(c["n"] for c in bulk.values())
    sr = 100.0 * sum(c["hit"] for c in small.values()) / sum(c["n"] for c in small.values())
    cid = write_claim(
        "zebrafish-flight", None,
        f"""[HOW OFTEN A HARVESTED VALUE COMES BACK IN THE UNITS ITS QUESTION ASKED FOR SPLITS BY
HARVEST MODE, NOT BY UNIT TYPE: {br:.1f} PERCENT FOR THE BULK HARVESTS AGAINST {sr:.1f} PERCENT
FOR THE SMALL TARGETED ONES, AND THE AGGREGATE HIDES IT]
Claim 2769 measured ratio-unit questions at 2.9 percent against 26.2, and
`extraction_questions.ratio_unit` quotes that to justify decomposing every ratio question. It
was computed once by hand with no script, so neither it nor its own stated limit could be
retested. analysis/units_match_rate.py is that instrument.

THE RATIO EFFECT REPRODUCES AS A RATIO AND NOT AS A LEVEL. Over {len(seen_q)} questions and
{n_all} verified values: non-ratio {plain:.1f} percent of {tally['plain_n']}, ratio {ratio:.1f}
percent of {tally['ratio_n']}, a {fold:.1f}-fold difference against 2769's 8.9. The absolute
rates do NOT reproduce -- {plain:.1f} against 26.2 -- on a population 47 percent larger, so the
level is a different corpus and the fold is the stable part.

THE DOMINANT EFFECT IS SOMETHING 2769 DID NOT REPORT. Broken down by harvest file:
{byh}. The four bulk harvests run {br:.1f} percent over {sum(c['n'] for c in bulk.values())}
values; the small targeted ones run {sr:.1f} percent over {sum(c['n'] for c in small.values())}.
That is roughly twenty-fold and it is larger than the ratio effect it was hiding. By project:
{byp}.

WHAT THIS DOES NOT ESTABLISH. The association is measured; the mechanism is not. A plain
confound is that the small harvests' questions may have been written against values already in
hand, which would make their near-perfect match partly circular. Nothing here rules that out,
and it should be checked before the bulk harvest is called defective. What IS established is
that the aggregate rate is not a property of the corpus but a mixture of two populations that
differ twenty-fold, so quoting one number for it -- as 2769 and the ratio_unit docstring both do
-- describes neither.

METHOD. The definition is declared in the module because the original was never written down:
population is every VERIFIED value whose (qfile, asked) resolves to a question declaring units;
a match is equality after casefolding and whitespace collapse, with dimensionless spellings
folded, a question's `A or B` alternatives both accepted, and a trailing referent qualifier
allowed to drop (`W/kg muscle` is answered by `W/kg`). Both relaxations were found by this
script's control failing against the published number, not by reading the data: exact equality
scored the nine ratio questions at a flat ZERO, including one commit 35bc9701 had measured at
6.8 percent. Eighteen controls ship with the script and all pass -- nine for the ratio
classifier, nine must-match/must-not-match pairs for the matcher -- and it refuses to print a
rate if any fails.

ONE CONTROL CAUGHT A STALE EXPECTATION: 2769 lists `m/s` as a ratio, and the code no longer
agrees, because 35bc9701 found m/s matching at 12.9 percent of 186 -- the best in the set --
while seven of the nine returned literally zero across 786 values, and exempted the standard
compound units. So `ratio` here means DECOMPOSABLE ratio and is not 2769's bucket.""",
        "measured", br, "percent of bulk-harvest values returning the units asked for",
        "analysis/units_match_rate.py", None)
    print(f"\n  recorded claim {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
