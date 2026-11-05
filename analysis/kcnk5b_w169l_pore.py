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


def submit(label: str, seq: str, a3m: str, chains=("A", "B")):
    """openfold3, NOT boltz2, and the reason is a schema wall rather than a preference.

    boltz2_predict_native refuses a homodimer three ways: passing the same alignment inline to
    chains A and B returns `ValueError: All proteins with the same sequence must share the same
    MSA!`, and so does uploading the alignment once and referencing that one artifact from both
    chains. Boltz's own convention for a homodimer is a single entry with `id: [A, B]`, but this
    endpoint's Polymer.id is a STRING (pattern ^[A-Za-z0-9]+$), so that form cannot be
    expressed. Three submissions, two input shapes, one unchanged error message -- and progress
    is a change of error, not a reworded same error.

    infer_openfold3_native takes `molecules` with unique chain ids and a per-chain MSA, with no
    sharing constraint, and this project already has a successful `infer_openfold3_native and3
    homodimer A+B` run (exit 0). So the working path was already in the run table.
    """
    import nebius
    mols = [{"type": "protein", "id": c, "sequence": seq,
             "msa": {"main": {"a3m": {"alignment": a3m, "format": "a3m"}}}} for c in chains]
    op, _ = nebius.submit(
        "infer_openfold3_native",
        {"request_id": f"ms-kcnk5b-{label}-of3-dimer-v2",
         "inputs": [{"input_id": f"kcnk5b-{label}", "output_format": "cif",
                     "molecules": mols}],
         "idempotency_key": f"ms-kcnk5b-{label}-of3-dimer-v2"},
        f"kcnk5b-w169l-pore:{label} -- does the alf substitution move the ion pathway?")
    print(f"  {label}: submitted {op}", flush=True)
    nebius.wait(op)
    out = D / f"kcnk5b-{label}-of3"
    out.mkdir(parents=True, exist_ok=True)
    os.system(f"python3 {HERE}/../swarm/fetch_results.py {op} {out}")
    return op, out


def wt_twice() -> int:
    """THE CONTROL CLAIM 1083 LACKS: predict wild type TWICE and measure the difference.

    Claim 1083 concluded "openfold3 does not converge on this target" from a WT-vs-W169L
    comparison of 49.178 A. That comparison cannot separate two explanations:
      (a) the predictor is non-deterministic on this target, so ANY two runs differ hugely; or
      (b) the predictor is stable and the single substitution genuinely moved the fold.
    (b) would be an extraordinary result for one conservative-ish substitution in a 448-residue
    protein, which is why (a) is the working hypothesis -- but it is a hypothesis until wild type
    is run against itself. If WT-vs-WT also lands near 49 A, (a) is confirmed and claim 1083
    stands. If WT-vs-WT is small, claim 1083 is WRONG and the mutation did something.
    """
    a3m = A3M.read_text()
    wt = [ln for ln in a3m.splitlines() if not ln.startswith(">")][0]
    print("  predicting WILD TYPE a second time; identical inputs, new idempotency key")
    op, out = submit("wt-replicate", wt, a3m)
    print(f"  {op} -> {out}")
    return 0


def monomer_twice() -> int:
    """Is kcnk5b unpredictable only as a DIMER, or at all?

    Claim 1092 measured 30.161 A between two openfold3 runs of the identical wild-type DIMER.
    That could be an interface problem -- iPTM was 0.33-0.40, and iPTM scores the interface. The
    existing monomer prediction is WORSE on its own terms (pLDDT 48.7 against the dimer's 60.7),
    so this asks whether a second monomer run lands anywhere near the first.

    IT MATTERS BEYOND THIS PROTEIN. Claims 1080 and 1081 compared ProteinMPNN across a dimer and
    a monomer structure. If the monomer is as irreproducible as the dimer, both of those rest on
    two draws from a wide distribution and neither can be read as structural.
    """
    a3m = A3M.read_text()
    wt = [ln for ln in a3m.splitlines() if not ln.startswith(">")][0]
    print("  predicting the MONOMER a second time; one chain, identical alignment")
    op, out = submit("monomer-replicate", wt, a3m, chains=("A",))
    print(f"  {op} -> {out}")
    return 0


def main() -> int:
    if "--wt-twice" in sys.argv:
        return wt_twice()
    if "--monomer-twice" in sys.argv:
        return monomer_twice()
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
