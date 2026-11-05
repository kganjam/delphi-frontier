#!/usr/bin/env python3
"""Does the Kcnk5b contact profile measure structure, or MSA depth?

Claim 1037 reported that in two predicted Kcnk5b structures the region removed by the
fin-overgrowth truncation does not contact the rest of the fold unusually, and both
predictions put the biologically meaningful split at 240 BELOW an arbitrary split at 180.
Claim 1038 withdrew the inference on an adversarial panel's objection that both predictors
share a tendency to extend disordered tails, so their agreement is not independent.

That objection was asserted. This measures it. If the contact profile is tracking how much
homology information exists at each position rather than the fold, then the curve should
follow the MSA depth curve -- and the project holds the alignment: kcnk5b_pdb70.a3m.

Coordinates are read through analysis/cif.py, which takes the column index from the file's
declared `_atom_site` header. Two earlier hand-indexed attempts read the occupancy and the
B-factor columns as coordinates; see that module.
"""
from __future__ import annotations

import math
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cif import ca_atoms, check_protein_like  # noqa: E402

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
FILES = ("kcnk5b_boltz2.cif", "kcnk5b_esmfold2.cif")
CUT = 10.0
SPLITS = list(range(100, 401, 10))


def depth_profile(a3m: pathlib.Path) -> list[int]:
    lines = a3m.read_text().splitlines()
    seqs = [lines[i + 1] for i, ln in enumerate(lines) if ln.startswith(">")]
    n = len(seqs[0])
    cov = [0] * n
    for s in seqs[1:]:
        j = 0
        for ch in s:
            if ch.isupper() or ch == "-":          # lowercase = insertion, not a query column
                if j < n:
                    if ch != "-":
                        cov[j] += 1
                    j += 1
    return cov


def contact_fraction(ats: list[dict], split: int, cut: float = CUT) -> float:
    a, b = ats[:split], ats[split:]
    c2 = cut * cut
    n = sum(1 for p in a for q in b
            if (p["x"] - q["x"]) ** 2 + (p["y"] - q["y"]) ** 2 + (p["z"] - q["z"]) ** 2 <= c2)
    return 100.0 * n / (len(a) * len(b))


def spearman(a: list[float], b: list[float]) -> float:
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):                       # average ties, which the depth curve has
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((x - mb) ** 2 for x in rb))
    return num / den if den else float("nan")


def main() -> int:
    cov = depth_profile(D / "kcnk5b_pdb70.a3m")
    zero = [i + 1 for i, c in enumerate(cov) if c == 0]
    print(f"  MSA kcnk5b_pdb70.a3m: {len(cov)} query columns, "
          f"{len(zero)} with ZERO homologue coverage, first at residue {zero[0] if zero else None}")

    prof = {}
    for name in FILES:
        ats = ca_atoms(D / name)
        check_protein_like(ats, name)
        prof[name] = [contact_fraction(ats, s) for s in SPLITS]
    depth = [sum(cov[s:]) / len(cov[s:]) for s in SPLITS]

    print(f"\n  {len(SPLITS)} split points, residues {SPLITS[0]}..{SPLITS[-1]} step 10, "
          f"CA-CA cutoff {CUT:.0f} A\n")
    print("  split   C-side MSA depth   " + "   ".join(f"{n.split('_')[1][:7]:>8}" for n in FILES))
    for i, s in enumerate(SPLITS):
        print(f"   {s:>4}   {depth[i]:>14.2f}   " + "   ".join(f"{prof[n][i]:8.3f}" for n in FILES))

    print("\n  SPEARMAN rho between contact fraction and C-side MSA depth, over the 31 splits")
    for n in FILES:
        print(f"    {n:24} rho = {spearman(prof[n], depth):+.3f}")

    print("\n  AND BETWEEN THE TWO PREDICTIONS THEMSELVES")
    print(f"    boltz2 vs esmfold2       rho = {spearman(prof[FILES[0]], prof[FILES[1]]):+.3f}")

    print("\n  THE THREE SPLITS CLAIM 1037 REPORTED")
    for s in (180, 240, 300):
        i = SPLITS.index(s)
        print(f"    split {s}: depth {depth[i]:5.2f}   "
              + "   ".join(f"{n.split('_')[1][:7]} {prof[n][i]:.3f}%" for n in FILES))
    return 0




def autocorrelation_control() -> int:
    """The splits are NOT independent, so a naive rho over 31 of them is not evidence.

    An adversarial challenge on claim 1039 made three points and all three are right:
      1. the 31 split points overlap almost completely -- a split at 100 and one at 110 share
         98% of their data -- so the effective sample size is far below 31 and a correlation
         computed over them cannot be read as if the points were independent;
      2. the causal story ("the profile is largely a measure of homology availability") needs a
         control that breaks the alignment between the two curves while keeping their shape;
      3. "the two predictions disagree outright" overstates what rho = -0.29 supports; "show no
         agreement" is what the data say.

    THE RIGHT NULL IS A CIRCULAR SHIFT, NOT A SHUFFLE. Shuffling the depth profile destroys its
    spatial autocorrelation, which is the very thing that makes the naive correlation look
    impressive -- a shuffled null is too easy to beat and would confirm the result spuriously.
    A circular shift preserves the autocorrelation exactly and destroys only the registration
    between depth and contact, which is the thing under test.
    """
    cov = depth_profile(D / "kcnk5b_pdb70.a3m")
    prof = {}
    for name in FILES:
        ats = ca_atoms(D / name)
        check_protein_like(ats, name)
        prof[name] = [contact_fraction(ats, s) for s in SPLITS]
    depth = [sum(cov[s:]) / len(cov[s:]) for s in SPLITS]

    print("\n  AUTOCORRELATION CONTROL -- circular shift of the depth profile")
    print(f"  the {len(SPLITS)} splits share most of their residues, so they are not "
          f"{len(SPLITS)} independent observations")
    n = len(cov)
    for name in FILES:
        real = spearman(prof[name], depth)
        null = []
        for shift in range(20, n - 20, 7):            # every circular shift, coarsely sampled
            rolled = cov[shift:] + cov[:shift]
            d2 = [sum(rolled[s:]) / len(rolled[s:]) for s in SPLITS]
            null.append(spearman(prof[name], d2))
        bigger = sum(1 for x in null if abs(x) >= abs(real))
        print(f"    {name:24} real rho {real:+.3f}   "
              f"|null| >= |real| in {bigger:>3} of {len(null)} shifts  "
              f"(p ~ {bigger/len(null):.3f})")
    print("    A circular shift keeps the depth curve's shape and destroys only its")
    print("    registration with the contact curve, so beating it is evidence the ALIGNMENT")
    print("    matters rather than the shape. A plain shuffle would destroy the shape too and")
    print("    would be far too easy to beat.")
    return 0


if __name__ == "__main__":
    main()
    raise SystemExit(autocorrelation_control())
