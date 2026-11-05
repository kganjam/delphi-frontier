#!/usr/bin/env python3
"""Read the retrieved full texts for MEASURED values, with every quote verified against the source.

WHY. swarm/fetch_fulltext.py retrieved 6 full texts (368k characters) that nothing has read.
Having the text is not having read it, and this project's blocking magnitudes have repeatedly
turned out to be sitting in papers it already held. This reads them against the open questions.

Paid from Claude Console API credit, which expires 2026-11-07 and which cloud-session tooling
cannot reach. Tenants and the API call are REUSED from api_challenge rather than restated, so
`api_allen` stays excluded by the owner's standing instruction in exactly one place.

THE FAILURE MODE THIS GUARDS AGAINST. A model asked to extract measured values from a paper will
produce measured values whether or not the paper contains any -- the same confirmation pressure
api_challenge documents for its verdicts, in a form that is far more dangerous, because a
fabricated number with a plausible quote attached is indistinguishable from a real finding and
would enter the claim graph as `measured`.

THE GUARD IS MECHANICAL, NOT PROMPTED. Every extraction must carry a verbatim quote, and this
module CHECKS that quote against the source text it supplied. A quote that is not found is
discarded and counted, no matter how plausible. Prompting a model to be honest is not a control;
searching the source for its quote is.

  python3 extract_values.py [--papers P1,P2] [--write]
"""
from __future__ import annotations

import json
import os
import re
import pathlib
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_challenge import TENANTS, call  # noqa: E402  reuse: api_allen excluded in one place

FULLTEXT = Path(__file__).resolve().parent.parent / "results" / "fulltext"
OUT = Path(__file__).resolve().parent.parent / "results" / "extracted-values.json"
CHUNK = 38_000          # characters per call
MODEL = "claude-opus-4-5-20251101"

QUESTIONS = """\
1. Fin ray or fin mechanical properties: flexural stiffness (EI), Young's modulus, second moment
   of area, force-displacement, elastic energy storage or hysteresis. Units and species.
2. Muscle power output in W/kg, and muscle power as a function of CONTRACTION FREQUENCY.
   The frequency at which power falls to zero is especially wanted.
3. Fin SIZE measurements: fold-change, length or area, for any mutant or allele, WITH the age
   and body length of the fish at measurement.
4. Any experiment COMBINING two fin-overgrowth alleles, and whether the effect added or saturated.
5. Lift or drag coefficients, with the Reynolds number and angle of attack.
6. Swimming or escape velocity, with body length and whether the fish started from rest.
"""

PROMPT = """You are extracting NUMERIC values from a scientific paper for a research database.

The database records HOW a paper came by each number, so do not restrict yourself to the paper's
own measurements. A modelling study's assumed constants and simulation outputs are wanted too,
and so is a value the paper quotes from an earlier study. Each one is simply labelled.

Below is an excerpt of the paper's full text. Find values answering any of these questions:

{questions}

RULES, and the third is enforced mechanically after you reply:
- Report ONLY values that appear in the excerpt below. Do not use anything you know about this
  paper or this field from elsewhere.
- Every item MUST carry `provenance`, which is the whole point of this extraction. Use exactly
  one of:
    "measured-here"   the authors measured it in THIS study, from real specimens or apparatus
    "modelled-here"   an output of this paper's own simulation, model or calculation
    "assumed-here"    a constant this paper's model takes as input without deriving it
    "quoted"          a value this paper attributes to an earlier study. Put that study in
                      `attributed_to` (for example "Sawicki et al. 2015").
    "unclear"         the excerpt does not let you tell. Preferred over guessing.
  A simulation output labelled "measured-here" is the single worst error you can make here,
  because it is the error this database exists to prevent.
- Be THOROUGH. A results section, a figure caption, a table or a methods paragraph often holds
  several relevant values; report each one separately. Scan the whole excerpt, not just its
  opening. Partial answers are wanted: a value whose species or conditions you cannot determine
  is still worth reporting with those fields left as "unstated".
- Report a value even when it is incidental to the paper's own argument. This database wants the
  NUMBER, not the paper's conclusion, so a control measurement or a value quoted from an earlier
  study counts, provided the sentence you quote is in the excerpt below.
- If, having scanned it all, the excerpt genuinely holds no measured value relevant to ANY of the
  questions, an empty list is the correct answer. Never invent one: a fabricated value is worse
  than a missed one, and the quote check below will catch it anyway.
- Every item MUST carry `quote`: a span copied EXACTLY, character for character, from the
  excerpt below. Your reply is checked by searching the excerpt for that string. A quote that is
  not found causes the item to be DISCARDED, so a paraphrase loses you the finding.
- If the excerpt contains no relevant measured value, reply exactly: {{"values": []}}

Reply with JSON only, no other text:
{{"values": [{{"question": <number>, "value": "...", "units": "...", "species": "...",
              "conditions": "...", "provenance": "...", "attributed_to": "...",
              "quote": "..."}}]}}

PAPER EXCERPT:
---
{excerpt}
---
"""


def norm(s: str) -> str:
    """Whitespace-insensitive comparison. The XML strip collapses spacing, and a quote that
    differs only in run-length is still a real quote; one that differs in WORDS is not."""
    return re.sub(r"\s+", " ", s).strip().lower()


def extract_json(text: str):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# POSITIVE CONTROL. The first run of this module returned ZERO values from 368,000 characters
# across six papers -- 0 verified AND 0 discarded, every reply an empty list -- and the output
# read as a finding about the papers. It was a finding about fetch_fulltext.py, which was taking
# only <body> and dropping <floats-group>, where JATS keeps every figure, table and caption and
# therefore most measured values.
#
# The quote check this module already had could not see that: it guards against INVENTED values
# and is silent about a model that returns nothing. A guard against fabrication is not a guard
# against vacuity, and an extractor that always replies {"values": []} passed every check here.
# So the control below is a MUST-FIND case: a passage known to contain a measured value must
# yield at least one verified extraction, or the run aborts and reports nothing.
# TWO CONTROLS, BECAUSE "the extractor is broken" AND "these papers contain nothing" PRODUCE
# THE IDENTICAL OUTPUT and must be told apart.
#
# History: the first run returned 0 values from 368,000 characters across six papers and read as
# a finding about the papers. Part of it WAS a bug -- fetch_fulltext.py took only <body> and
# dropped <floats-group>, where JATS keeps every figure and caption, so ~30k characters of
# exactly the content that carries numbers was discarded. That is fixed.
#
# The second attempt used a real sentence as the must-find needle (Lanni's fin allometry slope,
# "0.9209"). It failed -- and was RIGHT to: a regression slope in a figure caption is not a "fin
# size measurement with age and body length", so an extractor returning nothing there is
# behaving correctly. A control whose expected answer is arguable is not a control.
#
# So the must-find control is SYNTHETIC: a sentence written here, carrying an unambiguous value
# of a kind the questions ask for. It tests the EXTRACTOR, never the corpus, and nothing it
# contains can enter the claim graph. Alongside it a must-NOT-find control checks the extractor
# is not simply reporting whatever it is shown.
CONTROL_POSITIVE = (
    "Methods. Flexural stiffness of the pectoral fin ray was measured in bending and found to "
    "be 412 x 10-6 N m2 in adult zebrafish of 31 mm standard length at 26 degrees C."
)
CONTROL_NEGATIVE = (
    "Methods. Fish were maintained on a 14:10 light cycle and fed twice daily with brine "
    "shrimp. Tanks were cleaned weekly and water chemistry was monitored throughout."
)


def _run_control(passage: str):
    r = call(TENANTS[0], PROMPT.format(questions=QUESTIONS, excerpt=passage),
             max_tokens=2000, model=MODEL)
    data = extract_json((r.get("text") if isinstance(r, dict) else str(r)) or "")
    if not data or "values" not in data:
        return None
    hay = norm(passage)
    return [v for v in data["values"]
            if norm(str(v.get("quote", ""))) and norm(str(v.get("quote", ""))) in hay]


def controls_pass() -> tuple[bool, str]:
    pos = _run_control(CONTROL_POSITIVE)
    if pos is None:
        return False, "positive control reply was not usable JSON"
    if not pos:
        return False, ("positive control found NOTHING in a passage stating a fin-ray flexural "
                       "stiffness -- the extractor is broken, so any zero below is meaningless")
    neg = _run_control(CONTROL_NEGATIVE)
    if neg is None:
        return False, "negative control reply was not usable JSON"
    if neg:
        return False, (f"negative control extracted {len(neg)} value(s) from husbandry prose -- "
                       f"the extractor reports whatever it is shown, so its hits mean nothing")
    return True, (f"positive control found {len(pos)} verified value(s); negative control found "
                  f"0 in husbandry prose")


def load_questions() -> tuple[str, str]:
    """Return (questions_text, label). QUESTIONS WERE HARD-CODED AND THAT IS A REPLICATION BUG.

    The six questions in this module are about fin mechanics, muscle power and lift -- the
    zebrafish-flight project's questions. Any other project, and any NEW question in this one,
    had to edit the module to ask it. That is the same shape as the fish research path baked
    into every agent prompt: a project-specific constant inside a general tool, invisible to a
    search for the project's name.

    `--questions FILE` supplies them instead. The controls in controls_pass() stay pinned to the
    built-in set on purpose: they prove the EXTRACTOR works, and a run whose controls moved with
    its questions could not tell a broken extractor from a question nothing matches.
    """
    if "--questions" in sys.argv:
        path = pathlib.Path(sys.argv[sys.argv.index("--questions") + 1])
        return path.read_text(encoding="utf-8"), path.name
    return QUESTIONS, "built-in (fin/flight)"


def main() -> int:
    write = "--write" in sys.argv
    out = OUT
    if "--out" in sys.argv:
        # A fixed output path means two slices of the corpus overwrite each other, so a
        # parallel run keeps only whichever finished last. Per-slice files also give the
        # run resume for free: a slice whose file exists has already been done.
        out = Path(sys.argv[sys.argv.index("--out") + 1])
    questions, qlabel = load_questions()
    papers = sorted(FULLTEXT.glob("*.txt"))
    if "--papers" in sys.argv:
        want = set(sys.argv[sys.argv.index("--papers") + 1].split(","))
        papers = [p for p in papers if p.stem in want]
    if not papers:
        print("no full texts found; run fetch_fulltext.py first")
        return 1

    print("=" * 78)
    print("FULL-TEXT VALUE EXTRACTION")
    print("=" * 78)
    print(f"  {len(papers)} paper(s), tenants {TENANTS} (api_allen EXCLUDED)")
    print(f"  questions: {qlabel}")
    print("  every quote is verified against the source; unverified items are DISCARDED")
    ok, why = controls_pass()
    print(f"  [{'ok' if ok else 'FAIL'}] controls: {why}")
    if not ok:
        print("\n  ABORTING. Without both controls a zero result is indistinguishable from a")
        print("  broken extractor, and a non-zero one from an extractor that reports anything.")
        print("  No results are reported.")
        return 2
    print()

    kept, discarded, calls, errors = [], [], 0, 0
    for p in papers:
        text = p.read_text(encoding="utf-8")
        hay = norm(text)
        chunks = [text[i:i + CHUNK] for i in range(0, len(text), CHUNK)]
        pk, pd = 0, 0
        for ci, chunk in enumerate(chunks):
            tenant = TENANTS[calls % len(TENANTS)]
            try:
                r = call(tenant, PROMPT.format(questions=questions, excerpt=chunk),
                         max_tokens=2000, model=MODEL)
            except Exception as e:                          # noqa: BLE001
                errors += 1
                print(f"  {p.stem} chunk {ci+1}/{len(chunks)}  CALL FAILED {type(e).__name__}")
                continue
            calls += 1
            body = r.get("text") if isinstance(r, dict) else str(r)
            data = extract_json(body or "")
            if not data or "values" not in data:
                errors += 1
                continue
            for item in data["values"]:
                q = norm(str(item.get("quote", "")))
                # THE CONTROL: the quote must be in the text we sent. Not negotiable.
                if q and len(q) > 15 and q in hay:
                    item["paper"] = p.stem
                    item["verified_quote"] = True
                    kept.append(item)
                    pk += 1
                else:
                    item["paper"] = p.stem
                    item["verified_quote"] = False
                    discarded.append(item)
                    pd += 1
        print(f"  {p.stem:<16} {len(chunks):>2} chunks -> {pk:>3} verified, {pd:>3} DISCARDED")

    print("\n" + "-" * 78)
    print(f"  {calls} API calls, {errors} unusable replies")
    print(f"  {len(kept)} values with a quote VERIFIED against the source")
    print(f"  {len(discarded)} DISCARDED because the quote was not in the text")
    if calls and (len(kept) + len(discarded)):
        rate = 100.0 * len(discarded) / (len(kept) + len(discarded))
        print(f"  fabrication/paraphrase rate: {rate:.1f}% -- this is why the check exists")
    print("-" * 78)
    for it in kept[:40]:
        print(f"  Q{it.get('question')} {it.get('paper')}: {str(it.get('value'))[:48]} "
              f"{str(it.get('units'))[:22]} | {str(it.get('species'))[:24]}")

    if write:
        out.write_text(json.dumps({"verified": kept, "discarded": discarded}, indent=1))
        print(f"\n  wrote {out}")
    else:
        print("\n  (dry run; pass --write to save)")
    print("\n  A verified quote means the SENTENCE is real. Whether the value means what the")
    print("  extraction says it means is a human judgement and is not established here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
