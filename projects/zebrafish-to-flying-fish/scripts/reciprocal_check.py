#!/usr/bin/env python3
"""Reciprocal check (analysis G2) for the two paralog collisions found by merge_and_check_hits.py.

The forward direction (zebrafish protein -> Exocoetid genome) cannot say which paralog a region is,
because both paralogs of a family align to the same place. This runs the other direction:

  1. cut the one scaffold carrying the collision out of the assembly;
  2. let miniprot predict the protein that region encodes (--trans), using the family's queries;
  3. align that predicted Exocoetid protein against EVERY member of the zebrafish gene family with
     Biopython's PairwiseAligner (BLOSUM62, global), and rank them.

The zebrafish family member that scores best against the predicted protein is the reciprocal best
hit. If it is not the gene the forward run named, the forward assignment is wrong.

What this still is NOT: a gene tree, a synteny test, or proof of orthology. A reciprocal best hit
between two species can be a best hit without being an ortholog, and the predicted protein is
miniprot's prediction from an unannotated assembly, not a sequenced transcript.

Run: python3 reciprocal_check.py GENOME.fna MINIPROT FAMILIES.json OUTDIR
"""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

from Bio import Align
from Bio.Align import substitution_matrices

GENOME, MP, FAM_JSON, OUT = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
FAMILIES = json.load(open(FAM_JSON))


def fetch(acc):
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    for i in range(4):
        try:
            return url, urllib.request.urlopen(url, timeout=60).read().decode()
        except Exception:
            if i == 3:
                raise
            time.sleep(3)


def read_scaffold(name):
    keep, buf = False, []
    with open(GENOME) as fh:
        for line in fh:
            if line.startswith(">"):
                if keep:
                    break
                keep = line[1:].split()[0] == name
            elif keep:
                buf.append(line.strip())
    return "".join(buf)


aligner = Align.PairwiseAligner(scoring="blastp")
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.mode = "global"
aligner.open_gap_score, aligner.extend_gap_score = -11, -1
aligner.end_gap_score = 0.0  # free end gaps, so a partial prediction is not penalised

report = {
    "scope": ("Reciprocal best-hit check on one scaffold per paralog collision. Inputs are an "
              "unannotated assembly and miniprot's own protein prediction, so a result here is a "
              "sequence-similarity ranking, not an orthology proof, not a gene tree, and not evidence "
              "of expression or function."),
    "tool": subprocess.run([MP, "--version"], capture_output=True, text=True).stdout.strip(),
    "aligner": "Biopython PairwiseAligner, global, BLOSUM62, gap open -11 extend -1, free end gaps",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "families": {},
}

for fam, spec in FAMILIES.items():
    members, ledger = {}, []
    for gene, acc in spec["members"].items():
        url, fa = fetch(acc)
        seq = "".join(fa.split("\n")[1:])
        members[gene] = seq
        ledger.append({"gene": gene, "uniprot": acc, "len": len(seq), "url": url,
                       "sha256": hashlib.sha256(fa.encode()).hexdigest()})

    scaf_name = spec["scaffold"]
    scaf = read_scaffold(scaf_name)
    if not scaf:
        raise SystemExit(f"scaffold {scaf_name} not found")
    scaf_fa = OUT / f"{fam}_{scaf_name}.fna"
    scaf_fa.write_text(f">{scaf_name}\n{scaf}\n")

    q_fa = OUT / f"{fam}_queries.faa"
    q_fa.write_text("".join(f">{g}\n{s}\n" for g, s in members.items()))

    # miniprot's predicted proteins for this scaffold, from the whole family as queries
    r = subprocess.run([MP, "-t4", "--trans", "--outn=1", str(scaf_fa), str(q_fa)],
                       capture_output=True, text=True, check=True)
    (OUT / f"{fam}_trans.txt").write_text(r.stdout)
    scaf_fa.unlink()  # a slice of a public assembly: reproducible, not worth committing

    # --trans emits a plain PAF line per alignment followed by '##STA\t<protein>'
    preds, cur_q = [], None
    for line in r.stdout.splitlines():
        if line.startswith("##STA"):
            preds.append({"from_query": cur_q, "protein": line.split("\t", 1)[1].strip()})
        elif not line.startswith("##"):
            cur_q = line.split("\t")[0]

    # de-duplicate identical predictions (the family's members often predict the same ORF)
    uniq = {}
    for p in preds:
        uniq.setdefault(p["protein"], []).append(p["from_query"])

    fam_out = {"scaffold": scaf_name, "scaffold_len": len(scaf), "why": spec.get("why"),
               "query_ledger": ledger, "predictions": []}
    for prot, from_queries in sorted(uniq.items(), key=lambda kv: -len(kv[0])):
        ranked = []
        for gene, seq in members.items():
            aln = aligner.align(prot.replace("*", ""), seq)[0]
            a, b = str(aln[0]), str(aln[1])
            ident = sum(1 for x, y in zip(a, b) if x == y and x != "-")
            cols = sum(1 for x, y in zip(a, b) if x != "-" and y != "-")
            ranked.append({"zebrafish_gene": gene, "score": round(aln.score, 1),
                           "identity_over_aligned_columns": round(ident / cols, 3) if cols else None,
                           "aligned_columns": cols})
        ranked.sort(key=lambda r: -r["score"])
        fam_out["predictions"].append({
            "predicted_protein_len": len(prot.replace("*", "")),
            "predicted_by_queries": sorted(from_queries),
            "ranked_zebrafish_family_members": ranked,
            "reciprocal_best": ranked[0]["zebrafish_gene"],
            "margin_over_second": round(ranked[0]["score"] - ranked[1]["score"], 1) if len(ranked) > 1 else None,
        })
    report["families"][fam] = fam_out
    print(f"[{fam}] {scaf_name}: {len(uniq)} distinct predicted protein(s)")
    for pr in fam_out["predictions"]:
        top = pr["ranked_zebrafish_family_members"][:3]
        print(f"  len={pr['predicted_protein_len']} reciprocal_best={pr['reciprocal_best']} "
              f"margin={pr['margin_over_second']}")
        for t in top:
            print(f"    {t['zebrafish_gene']:10s} score={t['score']:9.1f} id={t['identity_over_aligned_columns']}")

(OUT / "reciprocal_check.json").write_text(json.dumps(report, indent=1) + "\n")
