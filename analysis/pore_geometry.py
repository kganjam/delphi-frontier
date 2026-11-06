#!/usr/bin/env python3
"""Does truncation change the pore's CONFORMATION, or only the model's confidence in it?

Claim 1045 concluded that truncating Kcnk5b does not reorganise the pore, and supported that
with mean pLDDT over residues 1-240: 73.1 in the full-length dimer against 73.2 in the
truncated one. An adversarial challenge made the same point twice and it is correct:

    "Identical pore pLDDT shows the model is equally CONFIDENT, not that the pore adopts the
     same CONFORMATION."

pLDDT is a confidence estimate. Two structures can be equally well-determined and geometrically
different. The challenge also noted that a geometric comparison "was both available and
necessary", which is true -- both CIF files are on disk. This runs it.

THE TEST is a Kabsch superposition of the shared residues (1-240 of chain A) followed by RMSD.
That asks directly whether the atoms sit in the same places, which is what "the pore is
unchanged" has to mean.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cif import ca_atoms  # noqa: E402

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                 "results", "fish-proteins", "structures")
FULL = "kcnk5b-homodimer-msa"
TRUNC = "kcnk5b-trunc240-dimer-msa"
SHARED = 240


def coords(sub: str, chain: str, lo: int, hi: int) -> np.ndarray:
    # ca_atoms returns resi as a STRING (it is a CIF text field). Comparing it to an int
    # raises rather than silently mis-sorting, which is the good failure mode, but it has to
    # be cast for both the range test and the ordering -- a lexical sort would put residue
    # 100 before residue 99 and the superposition would pair up the wrong atoms.
    ats = [a for a in ca_atoms(os.path.join(D, sub, "model.cif"))
           if a["chain"] == chain and lo <= int(a["resi"]) <= hi]
    ats.sort(key=lambda a: int(a["resi"]))
    return np.array([[a["x"], a["y"], a["z"]] for a in ats])


def kabsch_rmsd(P: np.ndarray, Q: np.ndarray) -> float:
    """RMSD after optimal superposition. P and Q must correspond row for row."""
    assert P.shape == Q.shape, (P.shape, Q.shape)
    Pc, Qc = P - P.mean(0), Q - Q.mean(0)
    V, S, Wt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(V @ Wt))
    Dm = np.diag([1.0, 1.0, d])
    R = V @ Dm @ Wt
    return float(np.sqrt(((Pc @ R - Qc) ** 2).sum() / len(P)))


def main() -> int:
    full_A = coords(FULL, "A", 1, SHARED)
    trunc_A = coords(TRUNC, "A", 1, SHARED)
    print(f"  shared region: residues 1-{SHARED}, chain A")
    print(f"    {FULL:30} {len(full_A)} CA")
    print(f"    {TRUNC:30} {len(trunc_A)} CA")
    if len(full_A) != len(trunc_A):
        print("  REFUSING: residue counts differ; the comparison would not be like for like")
        return 2

    rmsd = kabsch_rmsd(full_A, trunc_A)
    print(f"\n  PORE RMSD after optimal superposition: {rmsd:.2f} A")

    print("\n  CONTROLS")
    print(f"    a structure against ITSELF: {kabsch_rmsd(full_A, full_A):.4f} A (must be ~0)")
    rng = np.random.default_rng(3)
    # a random rotation+translation must superpose away to ~0, or the algorithm is not working
    th = rng.random() * 2 * np.pi
    Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
    moved = full_A @ Rz + np.array([11.0, -7.0, 3.0])
    print(f"    against a rotated+translated copy of itself: "
          f"{kabsch_rmsd(full_A, moved):.4f} A (must be ~0)")
    # a scrambled correspondence must give a LARGE rmsd, or the metric cannot detect difference
    perm = rng.permutation(len(full_A))
    print(f"    against itself with residue correspondence SHUFFLED: "
          f"{kabsch_rmsd(full_A, full_A[perm]):.2f} A (must be large)")
    # the other chain of the same structure: a homodimer's two chains should be similar but
    # not identical, which bounds what 'the same fold' looks like in these files
    full_B = coords(FULL, "B", 1, SHARED)
    print(f"    chain A vs chain B of the SAME homodimer: "
          f"{kabsch_rmsd(full_A, full_B):.2f} A")
    print("      -- this is the natural yardstick: two copies of one protein in one model,")
    print("         so it is what 'the same structure, predicted twice' costs in this file.")

    print("\n  READING")
    ab = kabsch_rmsd(full_A, full_B)
    if rmsd <= ab:
        print(f"    The truncated pore differs from the full-length pore by {rmsd:.2f} A, which")
        print(f"    is NO MORE than the {ab:.2f} A between the two chains of the full-length")
        print("    dimer itself. On this measure truncation does not reorganise the pore.")
    else:
        print(f"    The truncated pore differs by {rmsd:.2f} A, MORE than the {ab:.2f} A between")
        print("    the two chains of the full-length dimer. Claim 1045's conclusion does not")
        print("    survive a geometric test, and pLDDT was the wrong instrument for it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
