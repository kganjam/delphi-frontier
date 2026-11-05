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

PROMPT = """You are extracting MEASURED values from a scientific paper for a research database.

Below is an excerpt of the paper's full text. Find values answering any of these questions:

{questions}

RULES, and the third is enforced mechanically after you reply:
- Report ONLY values that appear in the excerpt below. Do not use anything you know about this
  paper or this field from elsewhere.
- Reporting NOTHING is a correct and expected answer. Most excerpts contain no relevant value.
  An empty list is a good result. Inventing a value is far worse than returning none.
- Every item MUST carry `quote`: a span copied EXACTLY, character for character, from the
  excerpt below. Your reply is checked by searching the excerpt for that string. A quote that is
  not found causes the item to be DISCARDED, so a paraphrase loses you the finding.
- If the excerpt contains no relevant measured value, reply exactly: {{"values": []}}

Reply with JSON only, no other text:
{{"values": [{{"question": <1-6>, "value": "...", "units": "...", "species": "...",
              "conditions": "...", "quote": "..."}}]}}

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


def main() -> int:
    write = "--write" in sys.argv
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
    print(f"  every quote is verified against the source; unverified items are DISCARDED\n")

    kept, discarded, calls, errors = [], [], 0, 0
    for p in papers:
        text = p.read_text(encoding="utf-8")
        hay = norm(text)
        chunks = [text[i:i + CHUNK] for i in range(0, len(text), CHUNK)]
        pk, pd = 0, 0
        for ci, chunk in enumerate(chunks):
            tenant = TENANTS[calls % len(TENANTS)]
            try:
                r = call(tenant, PROMPT.format(questions=QUESTIONS, excerpt=chunk),
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
        OUT.write_text(json.dumps({"verified": kept, "discarded": discarded}, indent=1))
        print(f"\n  wrote {OUT}")
    else:
        print("\n  (dry run; pass --write to save)")
    print("\n  A verified quote means the SENTENCE is real. Whether the value means what the")
    print("  extraction says it means is a human judgement and is not established here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
