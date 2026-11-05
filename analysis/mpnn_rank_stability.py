#!/usr/bin/env python3
"""Is POSITIONAL-ENTROPY RANK reproducible across ProteinMPNN samples?

check_grader_use.py reports `proteinmpnn-rank` as uncalibrated, and it is. But the nearest
existing calibration -- `proteinmpnn-probability`, whose note says "MAGNITUDES ONLY, NOT RANKS"
-- is about a DIFFERENT statistic, and the prohibition does not transfer:

    residue rank WITHIN a position   lysine at 200 ranked [14,14,11,12,10,12,10,7] across the
                                     8 samples of one run. Unstable. That is what the existing
                                     note forbids.
    position rank ACROSS positions   claim 1032's metric: Shannon entropy of each position's
                                     distribution, AVERAGED over all samples, then positions
                                     ranked against each other. Never measured.

The second is what claims 1032, 1043, 1049 and 1069 compute, so its reproducibility is the
question that matters for tonight's protein conclusions. This splits the 8 samples into two
disjoint halves and asks whether the two halves rank the positions the same way. Disjoint
halves, not a bootstrap: the question is whether INDEPENDENT samples agree, and resampling the
same 8 would answer a different one.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import pathlib
import statistics as st

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
RUNS = ("kcnk5b-homodimer-msa", "kcnk5b-monomer-msa", "kcnk5b-trunc240-dimer-msa")


def entropy(p: list[float]) -> float:
    tot = sum(p) or 1.0
    return -sum((x / tot) * math.log2(x / tot) for x in p if x > 0)


def spearman(a: list[float], b: list[float]) -> float:
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = st.fmean(ra), st.fmean(rb)
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((x - mb) ** 2 for x in rb))
    return num / den if den else float("nan")


def main() -> int:
    print("  split-half reproducibility of POSITIONAL-ENTROPY RANK\n")
    print(f"  {'run':28}{'pos':>6}{'splits':>8}{'median rho':>12}{'worst rho':>11}"
          f"{'top-50 overlap':>16}")
    worst_overall = 1.0
    for run in RUNS:
        f = D / run / "mpnn" / "result.json"
        if not f.exists():
            print(f"  {run:28}  (absent)")
            continue
        probs = json.loads(f.read_text())["probs"]
        n_s, n_p = len(probs), len(probs[0])
        ent = [[entropy(probs[s][i]) for i in range(n_p)] for s in range(n_s)]
        rhos, overlaps = [], []
        for half in itertools.combinations(range(n_s), n_s // 2):
            other = [s for s in range(n_s) if s not in half]
            a = [st.fmean(ent[s][i] for s in half) for i in range(n_p)]
            b = [st.fmean(ent[s][i] for s in other) for i in range(n_p)]
            rhos.append(spearman(a, b))
            ta = {i for i in sorted(range(n_p), key=lambda i: a[i])[:50]}
            tb = {i for i in sorted(range(n_p), key=lambda i: b[i])[:50]}
            overlaps.append(len(ta & tb) / 50.0)
        worst_overall = min(worst_overall, min(rhos))
        print(f"  {run:28}{n_p:>6}{len(rhos):>8}{st.median(rhos):>12.3f}"
              f"{min(rhos):>11.3f}{100*st.median(overlaps):>15.0f}%")

    print("\n  CONTROLS")
    probs = json.loads((D / RUNS[0] / "mpnn" / "result.json").read_text())["probs"]
    n_p = len(probs[0])
    ent0 = [entropy(probs[0][i]) for i in range(n_p)]
    print(f"    a profile against ITSELF: rho = {spearman(ent0, ent0):.3f} (must be 1.000)")
    import random
    rng = random.Random(11)
    sh = ent0[:]
    rng.shuffle(sh)
    print(f"    against a SHUFFLED copy:  rho = {spearman(ent0, sh):+.3f} (must be ~0, so the "
          f"statistic can report disagreement)")
    print(f"\n  worst split-half rho across all runs: {worst_overall:.3f}")
    print("  A metric whose two halves disagree cannot carry a position ranking; one whose")
    print("  halves agree is reproducible WITHIN this model and this structure, which is a")
    print("  narrower claim than being calibrated against a known-bad item.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
