#!/usr/bin/env python3
"""Analysis G4, finally runnable: does the flying-fish LAT4 locus carry the published F326L?

The full text of PMID 34534441 (PMC9172250, read 2026-11-01) states the convergent substitution
explicitly: *"a shared amino acid substitution in lat4a that is found across multiple lineages
having enlarged pectoral fins (F326L)"*, present in both flying-halfbeak lineages and in all
sequenced flying fishes **except** the sailfin flying fish *Parexocoetus brachypterus*. The paper's
own reference 17 identifies Lat4 as **Slc43a2**, which ties "lat4a" to the SLC43A2 family this
project has already mapped.

*Hirundichthys speculiger* is an Exocoetid and is not *P. brachypterus*, so the paper's result
predicts **L** at that position in its LAT4. This script tests that prediction against the two
SLC43A2-family loci this project predicted from the assembly.

Method: align each flying-fish predicted protein to each zebrafish reference with Biopython
(global, BLOSUM62), find the column holding reference position 326, and report the aligned
flying-fish residue plus a short window of context. The reference whose numbering the paper used is
NOT stated in the text read, so both zebrafish paralogs are reported and the ambiguity is declared
rather than resolved.

Run: python3 check_lat4a_f326l.py TREE_INPUT_FAA OUT_JSON
"""
import json
import pathlib
import sys

from Bio import Align
from Bio.Align import substitution_matrices

FA, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

seqs, name = {}, None
for line in FA.read_text().splitlines():
    if line.startswith(">"):
        name = line[1:].split()[0]
        seqs[name] = ""
    else:
        seqs[name] += line.strip()

REFS = [n for n in seqs if n.startswith("ZF_slc43a2")]
LOCI = [n for n in seqs if n.startswith("HSPEC_slc43locus")]
POS = 326

aligner = Align.PairwiseAligner(scoring="blastp")
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.mode = "global"
aligner.open_gap_score, aligner.extend_gap_score = -11, -1
aligner.end_gap_score = 0.0

rows = []
for ref in REFS:
    r = seqs[ref]
    ref_res = r[POS - 1] if len(r) >= POS else None
    for loc in LOCI:
        aln = aligner.align(r, seqs[loc])[0]
        a, b = str(aln[0]), str(aln[1])
        # walk the alignment to the column carrying reference residue POS
        ri, col = 0, None
        for k, ch in enumerate(a):
            if ch != "-":
                ri += 1
                if ri == POS:
                    col = k
                    break
        obs = b[col] if col is not None else None
        rows.append({
            "reference": ref,
            "reference_len": len(r),
            f"reference_residue_at_{POS}": ref_res,
            "locus": loc,
            "aligned_residue_in_locus": obs,
            "reference_context_320_332": r[POS - 7:POS + 6] if len(r) >= POS + 6 else None,
            "locus_context_aligned": b[max(0, col - 6):col + 7] if col is not None else None,
            "matches_published_L": obs == "L",
            "matches_reference_F": obs == ref_res,
        })

doc = {
    "scope": ("Residue check at one alignment column. It tests a published amino-acid state against "
              "a miniprot PREDICTION from an unannotated draft assembly, not against a sequenced "
              "transcript, and it is not evidence of transport activity or phenotype."),
    "published_claim": ("PMID 34534441 full text (PMC9172250): a shared amino acid substitution in "
                        "lat4a found across multiple lineages with enlarged pectoral fins, F326L; "
                        "present in both flying-halfbeak lineages and all sequenced Exocoetidae "
                        "except Parexocoetus brachypterus. Lat4 = Slc43a2 per the paper's ref 17."),
    "prediction_tested": ("H. speculiger is an Exocoetid and is not P. brachypterus, so its LAT4 "
                          "should carry L at the F326 position."),
    "declared_ambiguity": ("The paper's text as read does not state which sequence's numbering F326 "
                           "refers to. Both zebrafish SLC43A2 paralogs are therefore used as the "
                           "numbering reference and both results are reported."),
    "results": rows,
}
OUT.write_text(json.dumps(doc, indent=1) + "\n")
for r in rows:
    print(f"ref={r['reference']:32s} (len {r['reference_len']}) res{POS}={r[f'reference_residue_at_{POS}']} "
          f"| {r['locus'][:28]:28s} -> {r['aligned_residue_in_locus']} "
          f"{'== published L' if r['matches_published_L'] else ''}")
    print(f"    ref context {r['reference_context_320_332']}   locus context {r['locus_context_aligned']}")
