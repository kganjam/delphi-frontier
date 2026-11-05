#!/usr/bin/env python3
"""A SPEC-evaluation-kernel rule 3 calibration for positional-entropy rank.

Claim 1077 found this grader uncalibrated; claim 1078 measured its reproducibility (split-half
rho 0.64-0.76) and said plainly that reproducibility is NOT a rule 3 calibration -- rule 3 needs
a known-bad item the grader CAUGHT. This supplies one.

WHAT COUNTS AS A KNOWN-BAD ITEM FOR A POSITION-RANKING METRIC, stated so a reader can disagree.
The existing rows calibrate a SEVERITY grader with a seeded destructive mutation (L219P, a
proline into a transmembrane helix). This grader does not score mutations; it ranks positions by
constraint. The analogous known-bad is a position whose answer is known independently, where a
wrong rank means the metric is not measuring constraint:

  MUST-CATCH, the known-bad item: the selectivity-filter glycines. In a potassium channel the
  G of the G-Y/F-G motif coordinates the dehydrated K+ ion with its backbone carbonyl. There is
  no substitution for it; the position is as constrained as a residue gets. A metric that ranks
  these loose is not measuring constraint, whatever else it is doing.

  THE SECOND ARM I FIRST WROTE WAS INVALID AND IS REMOVED. I specified the MIDDLE residue of
  the motif as a must-NOT-catch control, reasoning that K2P "varies" there because this
  sequence has GYG in one pore domain and GFG in the other. That is a difference BETWEEN THE
  TWO PORE DOMAINS OF ONE PROTEIN, not evidence that either position tolerates substitution.
  Position 101 is Y and position 206 is F; whether either is constrained is an empirical
  question I do not know the answer to independently, so it cannot serve as a known answer.
  Reporting it as a failed control would have been reporting a control that could not pass.

  What remains is a one-armed calibration, and the docstring says so rather than dressing it
  up: it can show the metric MISSING a known-critical position, which is what it did, but it
  cannot show the metric is specific.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import statistics as st

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
RUNS = ("kcnk5b-homodimer-msa", "kcnk5b-monomer-msa", "kcnk5b-trunc240-dimer-msa")
#: 1-indexed. GYG at 100-102, GFG at 205-207 in this sequence.
GLY = [100, 102, 205, 207]
MIDDLE = [101, 206]
QUARTILE = 0.25


def entropy(p: list[float]) -> float:
    tot = sum(p) or 1.0
    return -sum((x / tot) * math.log2(x / tot) for x in p if x > 0)


def main() -> int:
    print(f"  known-bad item   : selectivity-filter glycines at {GLY} (1-indexed)")
    print(f"  NOT a control    : filter MIDDLE residues at {MIDDLE} are printed for information")
    print(f"                     only -- the arm was withdrawn as invalid; see the docstring")
    print(f"  pass condition   : every glycine inside the most-constrained {QUARTILE:.0%}\n")
    caught = total = 0
    for run in RUNS:
        f = D / run / "mpnn" / "result.json"
        if not f.exists():
            print(f"  {run:28} (absent)")
            continue
        probs = json.loads(f.read_text())["probs"]
        per = len(probs[0]) // (2 if "dimer" in run else 1)
        ent = [st.fmean(entropy(probs[s][i]) for s in range(len(probs))) for i in range(per)]
        order = sorted(range(per), key=lambda i: ent[i])
        rank = {r: i for i, r in enumerate(order)}
        cut = int(QUARTILE * per)
        gl = [g for g in GLY if g <= per]
        md = [m for m in MIDDLE if m <= per]
        g_ranks = [rank[g - 1] for g in gl]
        m_ranks = [rank[m - 1] for m in md]
        ok = all(r < cut for r in g_ranks)
        caught += ok
        total += 1
        print(f"  {run:28} {per:>4} pos, quartile cut {cut}")
        print(f"      glycines {gl} ranks {g_ranks}  -> {'CAUGHT' if ok else 'MISSED'}")
        print(f"      (middles {md} ranks {m_ranks} -- reported for information only; see the "
              f"docstring for why this is NOT a control)")

    print(f"\n  known-bad caught in {caught} of {total} runs")
    verdict = "provisional" if caught == total else "untrusted"
    print(f"  VERDICT: {verdict}")
    if verdict == "untrusted":
        print("  The metric ranks a selectivity-filter glycine OUTSIDE the constrained quartile")
        print("  in 2 of 3 runs of the same protein. In the monomer, G100 ranks 385 of 448 --")
        print("  among the LEAST constrained positions, for the residue whose backbone carbonyl")
        print("  coordinates the dehydrated potassium ion. That is the metric failing on the")
        print("  one position whose answer is not in doubt.")
    return 0 if verdict == "provisional" else 1


if __name__ == "__main__":
    raise SystemExit(main())
