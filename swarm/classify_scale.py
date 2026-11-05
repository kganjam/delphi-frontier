#!/usr/bin/env python3
"""Place claims on a biological scale, and PROVE the classifier first on claims already placed.

WHY. `project_structure.py` measures that coral, insect-flight, limbless-mouse and xenobot use
ZERO scales between them, while the fish uses 8. A project whose claims carry no scale is not
"across scales" whatever its prose says, and no cross-scale argument can be assembled from it.

THE CONTROL IS THE WHOLE DESIGN. 193 fish claims already carry a scale, assigned by hand over
the life of that project. Those are ground truth. Before writing anything, this classifies a
held-out sample of them BLIND -- the prompt never sees the stored value -- and reports
agreement. If agreement is at or below what guessing the most common scale would score, the
run REFUSES to write. A classifier that cannot reproduce labels a person already made has not
earned the right to make new ones.

That bar is deliberately a comparison against the majority-class baseline rather than a round
number: `organism` is 62 of 193, so a classifier that answered "organism" every time would
score 32% and look respectable against an arbitrary 30% threshold.

    python3 classify_scale.py --control            # measure agreement, write nothing
    SWARM_PROJECT=coral python3 classify_scale.py 40 --write
"""
from __future__ import annotations

import collections
import os
import random
import re
import sys

import api_challenge as ac
from dbq import flat, lit, q

SCALES = ("dna", "protein", "cell", "tissue", "organ", "organism", "behaviour", "ecology")

PROMPT = """Place this scientific claim at the biological scale it is ABOUT.

Choose exactly one of: {scales}

Guidance:
- dna        sequence, alleles, regulatory elements, genotype
- protein    structure, folding, a molecule's function
- cell       cell types, cell behaviour, signalling between cells
- tissue     a tissue's material properties, growth, patterning
- organ      a fin, a wing, a swim bladder, a skeleton -- a structure made of tissues
- organism   whole-animal performance, body size, locomotion, energetics
- behaviour  what the animal chooses to do
- ecology    environment, habitat, climate, populations, between-organism effects

If the claim is about a METHOD, a measurement tool or the project's own process rather than
about biology, answer exactly: NONE

CLAIM:
{stmt}

Reply with one word only: one of {scales}, or NONE."""


#: A SUBPROBLEM IS A QUESTION, NOT AN ASSERTION, and the claim prompt mis-handles it. Measured
#: 2026-11-05: run against 30 subproblems a person had already placed, the claim prompt answered
#: NONE for 24 of them, leaving 6 scoreable -- too few to judge, so the control correctly REFUSED
#: and 43 scale assignments were not written. The cause is the claim prompt's own rule, "if the
#: claim is about a METHOD ... answer NONE": a subproblem legitimately names its instrument
#: ("Run: micro-CT cross-sections at matched positions"), so it reads as method. The subject of
#: the question is what carries the scale, not the instrument used on it.
SUBPROBLEM_PROMPT = """Place this open research QUESTION at the biological scale of its SUBJECT.

Choose exactly one of: {scales}

Guidance:
- dna        sequence, alleles, regulatory elements, genotype
- protein    structure, folding, a molecule's function
- cell       cell types, cell behaviour, signalling between cells
- tissue     a tissue's material properties, growth, patterning
- organ      a fin, a wing, a swim bladder, a skeleton -- a structure made of tissues
- organism   whole-animal performance, body size, locomotion, energetics
- behaviour  what the animal chooses to do
- ecology    environment, habitat, climate, populations, between-organism effects

IMPORTANT: a research question normally names the INSTRUMENT it would use -- a literature
search, micro-CT, a simulation, a re-run at finer resolution. The instrument is NOT the subject.
Classify by what the answer would be ABOUT. "Measure fin ray cross-sections by micro-CT" is
`organ`, not a method. Answer NONE only if the question is about the PROJECT'S OWN process --
its records, its task list, its code, its gates -- with no biological subject at all.

QUESTION:
{stmt}

Reply with one word only: one of {scales}, or NONE."""


def pick(text: str) -> str | None:
    """The last standalone scale word in the reply, or None."""
    t = text.strip().lower()
    if re.search(r"\bnone\b", t):
        found = [w for w in re.findall(r"[a-z]+", t) if w in SCALES]
        if not found:
            return None
    hits = [w for w in re.findall(r"[a-z]+", t) if w in SCALES]
    return hits[-1] if hits else None


def classify(tenant: str, stmt: str) -> tuple[str | None, float]:
    """Returns ('dna'...'ecology' | 'NONE' | None, cost).

    THREE OUTCOMES, NOT TWO, and conflating them hid the real result. 'NONE' is the model
    JUDGING the claim to be about a method or the project's own process rather than about
    biology. None is an API refusal -- no answer at all. The first version of this returned
    None for both and the control printed them identically as "REFUSED", which made a
    deliberate, and as it turned out correct, judgement look like a transport failure.
    """
    out = ac.call_with_fallback(tenant, spec()['prompt']().format(scales=", ".join(SCALES), stmt=stmt[:4000]))
    cost = float(out.get("cost_usd") or 0.0)
    if out.get("_refused"):
        return None, cost
    got = pick(out.get("text", ""))
    return (got or "NONE"), cost


#: What a run classifies. Added 2026-11-05: every side-project SUBPROBLEM carried no scale
#: (0 of 43, against zebrafish's 99 of 112), and a subproblem with no scale cannot join the
#: cross-scale chain that `scale_chain.py` walks -- which is the structure that makes the fish
#: project work and the one the other projects were said to lack. The classifier and its control
#: are identical for both tables, so this parameterises rather than duplicating them.
TABLES = {
    "claim": {
        "table": "claim",
        "text": lambda: flat("statement", 3000),
        "live": "and superseded_by is null",
        "min_len": "and length(statement) > 120",
        "noun": "claim",
        "prompt": lambda: PROMPT,
    },
    "subproblem": {
        "table": "subproblem",
        # A question alone is short and often elliptical; why_it_matters carries the scale cues.
        "text": lambda: flat("coalesce(question,'') || ' ' || coalesce(why_it_matters,'')", 3000),
        "live": "",
        "min_len": "and length(coalesce(question,'')) > 40",
        "noun": "subproblem",
        "prompt": lambda: SUBPROBLEM_PROMPT,
    },
}


def spec():
    return TABLES["subproblem" if "--subproblems" in sys.argv else "claim"]


def control(n: int = 30, seed: int = 11) -> tuple[bool, str, float]:
    """Blind-classify claims that ALREADY carry a hand-assigned scale, and compare."""
    S = spec()
    rows = q(f"""select scale_id, {S['text']()} from {S['table']}
                 where project_id='zebrafish-flight' {S['live']}
                 and scale_id is not null {S['min_len']}
                 order by id""")
    random.Random(seed).shuffle(rows)
    rows = rows[:n]
    dist = collections.Counter(r[0] for r in q(f"""select scale_id from {S['table']}
            where project_id='zebrafish-flight' {S['live']} and scale_id is not null"""))
    base = max(dist.values()) / sum(dist.values())
    print(f"  CONTROL: {len(rows)} {S['noun']}s that a person already placed, classified blind.")
    print(f"  Majority-class baseline is '{dist.most_common(1)[0][0]}' at {100*base:.1f}% -- "
          f"the bar to beat, so a one-word classifier cannot pass.")
    agree = none_said = refused = 0
    spent = 0.0
    seen: list[tuple[str, str]] = []
    for i, (truth, stmt) in enumerate(rows):
        got, c = classify(ac.TENANTS[i % len(ac.TENANTS)], stmt)
        spent += c
        if got is None:
            refused += 1
        elif got == "NONE":
            none_said += 1
        else:
            agree += got == truth
        seen.append((truth, got or "API-REFUSED"))

    # SCORE ON THE CLAIMS WHERE BOTH SIDES COMMIT TO A SCALE. A 'NONE' is the model declining
    # to call the claim biological at all, and counting that as a wrong SCALE assumes the stored
    # label is right. On this project it frequently is not: claims about a METHOD get filed
    # under the scale of whatever work produced them. Two of the first three checked by hand --
    # claim 19 ("the no-homolog result is scoped to PDB70, a STRUCTURE database") and claim 449
    # ("THE A3M WAS COMMITTED ALL ALONG ... git ls-files finds it") -- are stored as `protein`
    # and are not about a protein at all. So NONE is reported separately, never as an error.
    scored = len(rows) - none_said - refused
    acc = agree / scored if scored else 0.0
    print(f"  both committed to a scale: {scored}/{len(rows)}   agreement {agree}/{scored} = "
          f"{100*acc:.1f}%   baseline {100*base:.1f}%")
    print(f"  model said NONE (method/process, scored separately): {none_said}    "
          f"API refusals: {refused}    spent ${spent:.4f}")
    conf = collections.Counter(seen)
    for (t, g), k in conf.most_common(10):
        mark = "OK " if t == g else ("?? " if g == "NONE" else "   ")
        print(f"      {mark} person {t:<10} -> model {g:<10} x{k}")
    ok = scored >= 10 and acc > base
    if scored < 10:
        print(f"  -> REFUSE: only {scored} scoreable {S['noun']}s, too few to judge the classifier")
    else:
        print(f"  -> {'PASS, beats the baseline on claims where both commit' if ok else 'REFUSE, at or below baseline'}")
    return ok, f"{agree}/{scored} = {100*acc:.1f}% vs baseline {100*base:.1f}%", spent


def main() -> int:
    write = "--write" in sys.argv
    nums = [a for a in sys.argv[1:] if a.isdigit()]
    n = int(nums[0]) if nums else 25
    project = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

    ok, detail, spent = control()
    if "--control" in sys.argv:
        return 0 if ok else 1
    if not ok:
        print(f"\n  NOT classifying {project}: the control did not beat its baseline ({detail}).")
        return 1

    # --ids lets a caller target specific claims rather than taking the lowest ids. The
    # design spec cites 53 claims spread across the whole id range, 50 of them unplaced, so
    # "the first N unplaced" would mostly miss them and the spec's scale coverage would not
    # move.
    want = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--ids=")]
    S = spec()
    quoted = S["table"] == "subproblem"   # subproblem ids are text (S933), claim ids are bigint
    if want:
        parts = [x.strip() for x in want[0].split(",") if x.strip()]
        ids = ",".join(lit(x) if quoted else str(int(x)) for x in parts)
        rows = q(f"""select id, {S['text']()} from {S['table']}
                     where project_id={lit(project)} {S['live']}
                     and scale_id is null and id in ({ids})
                     order by id""")
    else:
        rows = q(f"""select id, {S['text']()} from {S['table']}
                     where project_id={lit(project)} {S['live']}
                     and scale_id is null {S['min_len']}
                     order by id limit {n}""")
    print(f"\n  {project}: {len(rows)} unplaced {S['noun']}(s) to classify"
          + ("" if write else "  (dry run; pass --write)"))
    tally: collections.Counter[str] = collections.Counter()
    for i, (cid, stmt) in enumerate(rows):
        got, c = classify(ac.TENANTS[i % len(ac.TENANTS)], stmt)
        spent += c
        tally[got or "API-REFUSED"] += 1
        label = ("API refused, left unplaced" if got is None else
                 "NONE (method/process, left unplaced)" if got == "NONE" else got)
        print(f"    {S['noun']} {str(cid):>5} -> {label}")
        if write and got and got != "NONE":
            key = lit(cid) if quoted else str(int(cid))
            q(f"update {S['table']} set scale_id={lit(got)} "
              f"where id={key} and scale_id is null")
    print(f"\n  {dict(tally)}")
    print(f"  spent ${spent:.4f} including the control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
