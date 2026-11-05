#!/usr/bin/env python3
"""The must-NOT-catch arm claim 1080 said was missing, supplied by a real allele.

Claim 1080 registered the dimer-scoped grader `provisional` and named exactly why it could not
be better: "this is a ONE-ARMED calibration. It shows the metric catching a known-critical
position; it does NOT show the metric is specific, because no must-not-catch control survived.
A specificity arm needs a position independently known to be tolerant, which has not been
established."

One is established in the literature. The zebrafish `another longfin` (alf) phenotype is caused
by GAIN-OF-FUNCTION mutations in kcnk5b, and the allele used as a hyperactive-channel reagent is
kcnk5b W169L. A tryptophan-to-leucine substitution that yields a FOLDED, FUNCTIONAL, MORE
CONDUCTIVE channel in a VIABLE adult fish is a position independently known to admit
substitution -- which is the thing the glycines are not.

NUMBERING WAS CHECKED, NOT ASSUMED: residue 169 of this construct is W. There are only 9
tryptophans in 448 residues, so a coincidental match is unlikely, and its context
(FICTIVFLLWGFLVHLIIPAF) is the hydrophobic stretch a transmembrane helix should be -- consistent
with the thesis description that the alf substitutions "affect transmembrane domains".

WHAT THIS ARM CAN AND CANNOT SHOW, stated so it is not oversold. A single tolerated substitution
proves the position admits AT LEAST ONE change compatible with folding and function. It does NOT
prove the position is unconstrained in general, so a `tight` rank here would not strictly falsify
the metric. The arm is therefore a CONCORDANCE test with a predicted direction, not a hard
falsifier, and it is n=1. The glycine arm is the stronger of the two.

READ LEVEL: the W169L identification is from an ABSTRACT (Aramaki et al. 2026, bioRxiv,
"Cell-type-dependent bioelectric regulation of fin size and fin-ray segment length in zebrafish",
read via Consensus), corroborated by the Perathoner 2014 PLoS Genetics abstract and the 2013
thesis abstract for the gain-of-function character and the transmembrane location. The full
texts were NOT read.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import statistics as st

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
GLY = [100, 102, 205, 207]       #: must CATCH -- selectivity-filter glycines
TOLERANT = 169                   #: must NOT catch -- kcnk5b W169L, viable hyperactive allele
QUARTILE = 0.25
ARMS = (("kcnk5b-homodimer-msa", "mpnn", 42), ("kcnk5b-homodimer-msa", "mpnn-seed7", 7),
        ("kcnk5b-monomer-msa", "mpnn", 42), ("kcnk5b-monomer-msa", "mpnn-seed7", 7))


def entropy(p):
    t = sum(p) or 1.0
    return -sum((x / t) * math.log2(x / t) for x in p if x > 0)


def rank_map(probs, per):
    e = [st.fmean(entropy(probs[s][i]) for s in range(len(probs))) for i in range(per)]
    order = sorted(range(per), key=lambda i: e[i])
    return {r: i for i, r in enumerate(order)}


def main() -> int:
    print(f"  must CATCH    : filter glycines {GLY} inside the top {QUARTILE:.0%}")
    print(f"  must NOT catch: W{TOLERANT}, the alf gain-of-function allele W{TOLERANT}L\n")
    ok = True
    for run, sub, seed in ARMS:
        f = D / run / sub / "result.json"
        if not f.exists():
            print(f"  {run} seed {seed}: absent")
            continue
        d = json.loads(f.read_text())
        seq = d["mfasta"].split("\n")[1]
        # numbering control: the tolerant position must actually be the residue the paper names
        assert seq[TOLERANT - 1] == "W", f"{run}: residue {TOLERANT} is {seq[TOLERANT-1]}, not W"
        per = len(d["probs"][0]) // (2 if "dimer" in run else 1)
        rk = rank_map(d["probs"], per)
        cut = int(QUARTILE * per)
        g = [rk[x - 1] for x in GLY]
        w = rk[TOLERANT - 1]
        caught = all(r < cut for r in g)
        spec = w >= cut
        ok &= spec
        print(f"  {run:24s} seed {seed:<3d} cut {cut:<4d} glycines {str(g):22s} "
              f"{'CAUGHT' if caught else 'MISSED':6s}  W{TOLERANT} rank {w:>3d}/{per} "
              f"{'LOOSE (correct)' if spec else 'TIGHT (false positive)'}")
    print(f"\n  specificity arm passes in all arms: {ok}")
    print("  NOTE: a concordance test with a predicted direction, n=1, not a hard falsifier;")
    print("        see the docstring for what a single tolerated substitution does not prove.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
