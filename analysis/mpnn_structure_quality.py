#!/usr/bin/env python3
"""Does the filter-glycine finding depend on the STRUCTURE it was measured on?

Claim 1080 reported that ProteinMPNN ranks the kcnk5b selectivity-filter glycines as the three
most constrained positions in the DIMER and as unconstrained in the MONOMER, and read that as
the filter needing all four pore domains. Claim 1096 then measured both structures as single
draws from a distribution with 14-30 A run-to-run spread, which removes the causal attribution.

THIS ASKS THE QUESTION THE OTHER WAY ROUND: not "dimer versus monomer" but "well-modelled versus
badly-modelled". The two structures differ in confidence AT THE FILTER by a factor that dwarfs
anything else about them:

    openfold3 monomer   filter glycines ~52.9 pLDDT   (chain mean 62.6)
    ESMFold2  monomer   filter glycines 97.4, 92.8, 97.2, 93.1   (chain mean 83.6)

Both are MONOMERS of the same 448-residue sequence, verified residue by residue (G100, Y101,
G102, W169, G205, F206, G207, S345 all present and correct in each). So a difference between
them cannot be a dimer effect, and any difference IS a structure-quality effect.

IF THE GLYCINES RANK CONSTRAINED ON THE ESMFold2 MONOMER, claim 1080's "the monomer misses" was
an artifact of a badly-modelled filter rather than evidence about pore assembly -- and the
project gains a structure it can actually use. If they still rank loose, the monomer result
survives the change of structure and is about the molecule.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import statistics as st

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
GLY = [100, 102, 205, 207]
TOLERANT = 169
QUARTILE = 0.25
ARMS = (
    ("openfold3 monomer  (filter ~53 pLDDT)", D / "kcnk5b-monomer-msa" / "mpnn" / "result.json", 1),
    ("openfold3 dimer    (filter ~53 pLDDT)", D / "kcnk5b-homodimer-msa" / "mpnn" / "result.json", 2),
    ("ESMFold2  monomer  (filter 92-97 pLDDT)", D / "kcnk5b-esmfold2" / "mpnn" / "result.json", 1),
)


def entropy(p):
    t = sum(p) or 1.0
    return -sum((x / t) * math.log2(x / t) for x in p if x > 0)


def main() -> int:
    print(f"  must CATCH: filter glycines {GLY} inside the top {QUARTILE:.0%}")
    print(f"  must NOT  : W{TOLERANT}, the alf gain-of-function position\n")
    for label, path, nchain in ARMS:
        if not path.exists():
            print(f"  {label:42} (absent)")
            continue
        d = json.loads(path.read_text())
        probs = d["probs"]
        per = len(probs[0]) // nchain
        e = [st.fmean(entropy(probs[s][i]) for s in range(len(probs))) for i in range(per)]
        order = sorted(range(per), key=lambda i: e[i])
        rk = {r: i for i, r in enumerate(order)}
        cut = int(QUARTILE * per)
        g = [rk[x - 1] for x in GLY if x <= per]
        w = rk[TOLERANT - 1]
        print(f"  {label:42} cut {cut:<4} glycines {str(g):24} "
              f"{'CAUGHT' if all(r < cut for r in g) else 'MISSED':6}  W{TOLERANT} {w}/{per}")
    print("\n  All three are the SAME 448-residue sequence. The first two differ from the third")
    print("  in how well the filter is modelled, not in what molecule it is.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
