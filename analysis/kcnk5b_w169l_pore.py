#!/usr/bin/env python3
"""Does the alf gain-of-function substitution W169L change the pore geometry?

W169L is the hyperactive kcnk5b allele behind the `another longfin` phenotype: it raises K+
conductance and hyperpolarises the cell. Claim 1081 used position 169 as a known-tolerant
control and found ProteinMPNN ranks it 447 of 448 -- structurally the LEAST constrained
position in the protein. That is a statement about the backbone, not about function. This asks
the separate structural question: does substituting it move the ion pathway?

METHOD CONTROL, which is the whole reason both arms are run here rather than reusing a
structure already on disk. The existing kcnk5b-homodimer-msa model came from a different
predictor. Comparing a boltz2 mutant against it would confound METHOD with MUTATION, and the
mutation effect expected here is small. So wild type and W169L are both predicted with boltz2,
same alignment, same settings, same chain layout, and only the one residue differs.

FLOOR, without which an RMSD is unreadable: chain A against chain B of one homodimer is 0.22 A
(measured earlier in this project) -- two copies of the same sequence in the same structure, so
that is the reproducibility floor of this comparison. A truncated-versus-full pore difference
measured 1.35 A for scale. A mutant-vs-wild-type RMSD near 0.22 A is no detected change; one
approaching 1.35 A is a real rearrangement.
"""
from __future__ import annotations

import os
import pathlib
import sys

HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(HERE / ".." / "swarm"))
D = HERE / ".." / "results" / "fish-proteins" / "structures"
A3M = D / "kcnk5b_pdb70.a3m"
POS = 169          #: 1-indexed; the alf gain-of-function position
WT, MUT = "W", "L"


def variant_sequence(seq: str) -> str:
    assert seq[POS - 1] == WT, f"residue {POS} is {seq[POS-1]!r}, not {WT!r} -- wrong numbering"
    return seq[:POS - 1] + MUT + seq[POS:]


def submit(label: str, seq: str, a3m: str):
    import nebius
    poly = [{"id": c, "molecule_type": "protein", "sequence": seq,
             "msa": {"msa_search": {"a3m": {"alignment": a3m}}}} for c in ("A", "B")]
    op, _ = nebius.submit(
        "boltz2_predict_native",
        {"polymers": poly, "diffusion_samples": 1, "recycling_steps": 3,
         "idempotency_key": f"ms-kcnk5b-{label}-boltz2-dimer-v1"},
        f"kcnk5b-w169l-pore:{label} -- does the alf substitution move the ion pathway?")
    print(f"  {label}: submitted {op}", flush=True)
    nebius.wait(op)
    out = D / f"kcnk5b-{label}-boltz2"
    out.mkdir(parents=True, exist_ok=True)
    os.system(f"python3 {HERE}/../swarm/fetch_results.py {op} {out}")
    return op, out


def main() -> int:
    a3m = A3M.read_text()
    wt = [ln for ln in a3m.splitlines() if not ln.startswith(">")][0]
    print(f"  alignment {len(a3m.splitlines())//2} sequences; query length {len(wt)}")
    mut = variant_sequence(wt)
    diff = [i for i, (x, y) in enumerate(zip(wt, mut)) if x != y]
    print(f"  wild type vs W{POS}{MUT}: differ at {len(diff)} position(s) {[i+1 for i in diff]}")
    assert diff == [POS - 1], "the two sequences must differ at exactly the one position"
    for label, seq in (("wt", wt), (f"w{POS}l", mut)):
        op, out = submit(label, seq, a3m)
        print(f"  {label}: fetched into {out}", flush=True)
    print("\n  both predicted with the SAME method and alignment; compare with pore_geometry.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
