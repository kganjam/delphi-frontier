#!/usr/bin/env python3
"""Assert that superseded claims are ABSENT from the emitted files.

WHY THIS EXISTS, AND WHY IT IS A DIFFERENT SHAPE FROM check_quotes.py

    `check_quotes.py` asserts that a quoted fragment IS present in its source.
    That catches an invented quote. It cannot catch the opposite failure: a
    claim of ours that WAS true, has since been superseded, and still sits in
    a prose field of a data file the renderer reads.

    That happened here. Study 1's inherited result reported the bistable
    variant missing the held-out threshold by "a factor of 40". Re-running the
    study's own code showed the real gap is 39.2%. The correction was recorded
    in three places - and the stale number was left asserted as live fact in
    `routes.json`, in a prose field, inside a different JSON from the one that
    had been corrected. A checker that verifies values against data had no
    reason to look at it.

    So this checker inverts the test: a list of superseded strings that must
    not appear, with a whitelist for the places where they legitimately DO
    appear - a recorded correction has to be able to quote the thing it is
    correcting, or the record is useless.

HOW TO USE IT
    Add a row to SUPERSEDED when a number or claim changes. Give the phrase,
    why it is dead, and the contexts in which quoting it is legitimate. A
    whitelist entry is a substring that must appear within WINDOW characters
    of the hit - so "we used to say X, and here is why that was wrong" passes
    and a bare assertion of X does not.

CONTROLS
    Both run on every invocation, because a checker that finds nothing and a
    checker that is not running look identical:
      - a string that is certainly present somewhere must be FOUND;
      - a string that is certainly absent must NOT be found.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = ["routes.json", "index-fragment.json", "venation.json",
         "flight-performance.json", "hox-identity.json", "NOTES.md"]
WINDOW = 400

SUPERSEDED = [
    {
        "phrase": r"factor of 40|40-fold|40x gap|misses it by 40",
        "why": "Study 1's bistable variant misses the held-out Antp "
               "threshold by 39.2%, not by a factor of 40. The factor of 40 "
               "came from a stale hox-identity.json whose code had been "
               "revised and never re-run.",
        "legitimate_near": [
            "stale", "superseded", "earlier", "re-running", "rather than the",
            "implied", "corrected", "do not write the", "it is wrong",
            "far more credible",
        ],
    },
    {
        "phrase": r"controls do not all pass|its declared controls do not",
        "why": "After the re-run, study 1's controls.all_variants_pass is "
               "True for every variant and every protein ratio.",
        "legitimate_near": ["stale", "earlier", "inherited", "venation",
                            "C4", "convergence"],
    },
    {
        "phrase": r"[Hh]altere input is necessary for free flight",
        "why": "This is a PREMISE sentence in Mureli & Fox 2015, not their "
               "result, and we found no free-flight ablation measurement "
               "behind it. It may be quoted as a premise, never asserted as "
               "evidence.",
        "legitimate_near": [
            "premise", "background", "second sentence", "not their result",
            "PREMISE", "flagged as such", "recurs", "not used here",
            "appears in this literature", "CITED FOR WHAT IT MEASURED",
        ],
    },
]


def hits(text, pattern):
    for m in re.finditer(pattern, text):
        yield m.start(), m.group(0)


def main():
    problems = []
    corpus = {}
    for name in FILES:
        p = ROOT / name
        if not p.exists():
            continue
        corpus[name] = p.read_text()

    for rule in SUPERSEDED:
        for name, text in corpus.items():
            for pos, matched in hits(text, rule["phrase"]):
                ctx = text[max(0, pos - WINDOW): pos + WINDOW]
                if any(w in ctx for w in rule["legitimate_near"]):
                    continue
                line = text[:pos].count("\n") + 1
                problems.append((name, line, matched, rule["why"],
                                 text[max(0, pos - 90): pos + 90]))

    # --- controls ---------------------------------------------------------
    joined = "\n".join(corpus.values())
    pos_ctrl = "Ultrabithorax" in joined
    neg_ctrl = "a small purple trombone" in joined

    print(f"scanned {len(corpus)} files, {len(SUPERSEDED)} superseded rules")
    print(f"control POSITIVE (a string certainly present): found={pos_ctrl} "
          "(must be True)")
    print(f"control NEGATIVE (a string certainly absent): found={neg_ctrl} "
          "(must be False)")
    print(f"{len(problems)} superseded claims asserted without a correction "
          "context:")
    for name, line, matched, why, ctx in problems:
        print(f"  {name}:{line}  '{matched}'\n      why dead: {why}"
              f"\n      context: ...{ctx.strip()}...")
    ok = (not problems) and pos_ctrl and not neg_ctrl
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
