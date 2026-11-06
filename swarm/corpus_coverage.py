#!/usr/bin/env python3
"""Ask whether the full-text corpus CONTAINS the quantities the extractor asks for.

WHY THIS EXISTS. `extract_values.py` returned 0 verified values from 30 API calls over 14
papers, at about $0.10 a call. Its controls pass -- a synthetic sentence is extracted, husbandry
prose is not -- so the arm is working, and a working extractor returning nothing is a result
that needs a second instrument to interpret. Without one, "0 values" reads equally as "the
literature has nothing", "the questions are wrong" and "the extractor is broken", and the
cheapest of those to believe is the one that blames the literature.

WHAT IT FOUND, 2026-11-04, over 14 papers:
    flexural/EI stiffness ....... 0 mentions     <- a REAL absence
    Reynolds number ............. 0
    swim speed in BL/s .......... 0
    fin size (length/area) ..... 57              <- present, and still extracted 0
    lift/drag coefficient ...... 17
So the zero is real for three of the six questions and NOT real for the other two. Reading the
57 fin-size hits by hand says why: they are Methods prose ("fin lengths were measured along the
third ray"), figure captions naming a graph ("Graph showing body length-normalized regenerated
fin lengths of DMSO (n=8) and 5 uM cilnidipine (n=7)"), and RNA-seq "fold change", which is a
DIFFERENT QUANTITY that happens to share the words. The measurements themselves are plotted,
not written.

That corroborates claim 493 -- "this project's blocking magnitudes live in the figures and the
extraction drops them" -- which was established one paper at a time. This is the corpus-wide
version of the same finding, and it means more text extraction cannot fix the gap: the figure
arm (`figure_sweep.py`, `read_figure.py`) is the instrument that can.

USE IT BEFORE SPENDING ON EXTRACTION. A chunk costs about $0.10 whether or not the paper
contains anything, so scanning first is three orders of magnitude cheaper than asking.
"""
from __future__ import annotations

import pathlib
import re
import sys

FULLTEXT = pathlib.Path(__file__).resolve().parent.parent / "results" / "fulltext"

# One entry per question extract_values.py asks. The pattern is deliberately BROADER than the
# question: the point is to find out whether the subject is discussed at all, so a false
# positive here is harmless and a false negative is not.
QUANTITIES = {
    "flexural stiffness / EI":  r"flexural|second moment of area|\bEI\b|Young'?s modulus",
    "stiffness units":          r"\bGPa\b|\bMPa\b|N\s*m\^?2|N·m",
    "muscle power W/kg":        r"W\s*/?\s*kg|W kg",
    "fin size length/area":     r"fin length|fin area|fin ray length",
    "lift/drag coefficient":    r"\bC[_ ]?L\b|lift coefficient|drag coefficient",
    "Reynolds number":          r"Reynolds|\bRe\b\s*[=~]",
    "swim speed BL/s":          r"BL\s*/?\s*s|body lengths? per second",
}

# `fold change` is EXCLUDED from the fin-size pattern on purpose and named here so the exclusion
# is a decision rather than an oversight: in this corpus every one of its matches was RNA-seq
# differential expression, not fin morphology.
EXCLUDED_HOMONYMS = {"fold change": "RNA-seq differential expression, not fin size"}


REFHEAD = re.compile(r"\b(References|Bibliography|Literature cited)\b", re.I)


def split_references(text: str) -> tuple[str, bool]:
    """Return (body, boundary_found). A REFERENCE LIST IS NOT EVIDENCE OF CONTENT.

    Measured 2026-11-04: the top-ranked 'myostatin' paper in this corpus is about social
    dominance hierarchies, and both its hits are in the bibliography -- a cited TITLE, counted
    as if the paper discussed the subject. Over the 19 papers where a boundary can be located,
    reference sections are 18% of the file and carry 0% of the flexural-stiffness and fin-size
    hits, 8% of lift/drag, 10% of Reynolds and 25% of swim-speed-in-BL/s.

    THE BOUNDARY IS ONLY LOCATABLE IN ABOUT ONE FILE IN SIX (19 of 111), because PMC strips the
    heading from most. So this does not eliminate the contamination, it bounds it: where the
    split works the inflation is 0-25% and does not change which quantities are present. A first
    pass that compared every file to itself reported 0-4% and looked reassuring, because 92 of
    111 files contributed an identical pair by construction -- a control that cannot fail.
    """
    cut = None
    for m in REFHEAD.finditer(text):
        if m.start() > len(text) * 0.45:
            cut = m.start()
    return (text[:cut], True) if cut else (text, False)


def controls_pass() -> tuple[bool, str]:
    """A string each pattern MUST match, and prose it MUST NOT."""
    must = {
        "flexural stiffness / EI": "the flexural stiffness EI of the ray",
        "stiffness units": "a modulus of 1.2 GPa was measured",
        "muscle power W/kg": "peak power output of 14.19 W/kg",
        "fin size length/area": "the fin length increased twofold",
        "lift/drag coefficient": "the lift coefficient CL reached 0.6",
        "Reynolds number": "at a Reynolds number of 7.8e4",
        "swim speed BL/s": "swimming at 2.4 BL/s",
    }
    for name, text in must.items():
        if not re.search(QUANTITIES[name], text, re.I):
            return False, f"{name!r} failed to match its own example"
    husbandry = ("Fish were maintained at 28.5 C on a 14:10 light cycle and fed twice daily "
                 "with brine shrimp according to standard protocols.")
    hit = [n for n, p in QUANTITIES.items() if re.search(p, husbandry, re.I)]
    if hit:
        return False, f"husbandry prose matched {hit} -- the patterns match anything"
    return True, f"{len(must)} patterns matched their example; husbandry prose matched none"


def main() -> int:
    ok, why = controls_pass()
    print("=" * 78)
    print("CORPUS COVERAGE -- does the text CONTAIN what the extractor asks for?")
    print("=" * 78)
    print(f"  [{'ok' if ok else 'FAIL'}] controls: {why}")
    if not ok:
        print("\n  ABORTING: a zero from unvalidated patterns is not a finding.")
        return 2
    files = sorted(FULLTEXT.glob("*.txt"))
    if not files:
        print("  no full texts; run fetch_fulltext.py or corpus_expand.py first")
        return 1
    print(f"  {len(files)} paper(s)\n")

    totals = {k: 0 for k in QUANTITIES}
    split_ok = 0
    for f in files:
        raw = f.read_text(encoding="utf-8")
        t, found = split_references(raw)
        split_ok += found
        hits = {k: len(re.findall(p, t, re.I)) for k, p in QUANTITIES.items()}
        for k, v in hits.items():
            totals[k] += v
        nz = ", ".join(f"{k.split()[0]}={v}" for k, v in hits.items() if v)
        print(f"  {f.stem:14} {len(t):>8,} chars  {nz or '-- none --'}")

    print("\n" + "-" * 78)
    print(f"  reference lists excluded where locatable: {split_ok} of {len(files)} papers. In the")
    print("  rest the heading is absent and citations are still counted, so these totals are an")
    print("  UPPER bound (measured inflation where the split works: 0-25% by quantity).")
    absent = [k for k, v in totals.items() if v == 0]
    for k, v in totals.items():
        mark = "  <- ABSENT from the whole corpus" if v == 0 else ""
        print(f"  {k:26} {v:>5}{mark}")
    print("-" * 78)
    if absent:
        print(f"  {len(absent)} quantit(ies) absent corpus-wide. For those, an extraction run")
        print("  would spend ~$0.10 a chunk to confirm an absence this scan already shows.")
    present = [k for k, v in totals.items() if v]
    if present:
        print(f"  {len(present)} present. If extraction still returns zero for these, the text")
        print("  mentions the subject without stating the number -- in this corpus that means")
        print("  the value is in a FIGURE (claim 493), so use figure_sweep/read_figure instead.")
    for h, why2 in EXCLUDED_HOMONYMS.items():
        print(f"  NOTE: {h!r} is deliberately not counted as fin size -- {why2}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
