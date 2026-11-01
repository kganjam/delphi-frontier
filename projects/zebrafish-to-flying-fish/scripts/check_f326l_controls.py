#!/usr/bin/env python3
"""Negative controls for the F326L finding, using the paper's own lineage distribution.

PMID 34534441 reports F326L in flying fishes and in the FLYING halfbeaks (*Oxyporhamphus*,
*Euleptorhamphus*), and explicitly NOT in the sailfin flying fish *Parexocoetus brachypterus*. The
three species tested here are all Beloniformes that the paper's distribution predicts should carry
**F**, not L:

  - *Hemiramphus limbatus* — a halfbeak, but **not** one of the two flying-halfbeak genera;
  - *Cololabis saira* (Pacific saury) — non-gliding;
  - *Xenentodon cancila* (needlefish) — non-gliding.

If any of them carries L at the aligned position, the flying-fish result is an artefact of this
pipeline rather than a lineage-specific signal, and that is the reportable outcome.

For each species the SLC43A2-family locus is identified as the predicted protein whose best query is
a `slc43a2` paralog and which aligns over the F326 column, then the aligned residue is read.

Run: python3 check_f326l_controls.py CONTROLS_DIR REFS_FAA OUT_JSON
"""
import json
import pathlib
import sys

from Bio import Align
from Bio.Align import substitution_matrices

CTRL, REFS, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
POS = 326

refs, name = {}, None
for line in REFS.read_text().splitlines():
    if line.startswith(">"):
        name = line[1:].split()[0]
        refs[name] = ""
    else:
        refs[name] += line.strip()
A2A = next(n for n in refs if n.startswith("ZF_slc43a2a"))
REF = refs[A2A]
assert REF[POS - 1] == "F", f"reference position {POS} is {REF[POS-1]}, expected F"

aligner = Align.PairwiseAligner(scoring="blastp")
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.mode = "global"
aligner.open_gap_score, aligner.extend_gap_score = -11, -1
aligner.end_gap_score = 0.0

CONTEXT = REF[POS - 7:POS + 6]
rows = []
for sp in sorted(p.name for p in CTRL.iterdir() if p.is_dir()):
    paf = (CTRL / sp / "slc43.paf").read_text()
    cur, preds = None, []
    for line in paf.splitlines():
        if line.startswith("##STA"):
            preds.append((cur, line.split("\t", 1)[1].strip().replace("*", "")))
        elif not line.startswith("##"):
            f = line.split("\t")
            cur = f[0]
    cand = [(q, p) for q, p in preds if "slc43a2" in q and len(p) > 300]
    best = None
    for q, prot in cand:
        aln = aligner.align(REF, prot)[0]
        a, b = str(aln[0]), str(aln[1])
        ri, col = 0, None
        for k, ch in enumerate(a):
            if ch != "-":
                ri += 1
                if ri == POS:
                    col = k
                    break
        if col is None:
            continue
        obs = b[col]
        ctx = b[max(0, col - 6):col + 7]
        # score context similarity to the reference window to pick the homologous locus
        sim = sum(1 for x, y in zip(ctx, CONTEXT) if x == y)
        rec = {"from_query": q, "protein_len": len(prot), "residue": obs, "context": ctx,
               "context_identity_to_reference_window": sim}
        if best is None or sim > best["context_identity_to_reference_window"]:
            best = rec
    sha = (CTRL / sp / "genome.sha256").read_text().strip()
    rows.append({"species_dir": sp, "genome_fasta_sha256": sha,
                 "n_slc43a2_candidate_predictions": len(cand), "best_homologous": best,
                 "carries_published_L": bool(best and best["residue"] == "L"),
                 "carries_reference_F": bool(best and best["residue"] == "F")})

doc = {
    "scope": ("Residue check at one alignment column in three Beloniformes that the published lineage "
              "distribution predicts should NOT carry the substitution. Every sequence is a miniprot "
              "prediction from a public assembly, not a sequenced transcript. Nothing here measures "
              "transport activity or phenotype."),
    "prediction": ("Hemiramphus limbatus is a halfbeak but not a FLYING halfbeak; Cololabis saira and "
                   "Xenentodon cancila are non-gliding. All three should carry F."),
    "falsifier": ("If any of the three carries L in homologous context, the flying-fish L is an "
                  "artefact of this pipeline rather than a lineage signal."),
    "numbering_reference": A2A,
    "reference_window_320_332": CONTEXT,
    "results": rows,
}
OUT.write_text(json.dumps(doc, indent=1) + "\n")
print(f"reference {A2A} position {POS} = {REF[POS-1]}; window {CONTEXT}\n")
for r in rows:
    b = r["best_homologous"]
    verdict = "L (CONTRADICTS the prediction)" if r["carries_published_L"] else (
        "F (as predicted)" if r["carries_reference_F"] else
        f"{b['residue'] if b else 'no homologous locus'} (neither F nor L)")
    print(f"  {r['species_dir']:12s} n_cand={r['n_slc43a2_candidate_predictions']:2d} -> {verdict}")
    if b:
        print(f"      from {b['from_query']:22s} len={b['protein_len']:4d} context={b['context']} "
              f"(ctx identity {b['context_identity_to_reference_window']}/13)")
