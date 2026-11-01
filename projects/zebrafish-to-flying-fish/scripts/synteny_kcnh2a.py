#!/usr/bin/env python3
"""Synteny test (analysis G3b): is the kcnh2a NEIGHBOURHOOD present in the flying-fish assembly?

Three gene trees have now failed to find a kcnh2a-like region in GCA_018398805.1. Two explanations
remain and they have opposite consequences:

  (A) the assembly is generally incomplete here, and the whole neighbourhood is missing or scattered
      -> the absence says nothing about the gene;
  (B) the neighbourhood is present and contiguous with a gap exactly where kcnh2a should be
      -> the absence is gene-specific in this assembly, which is a sharper and more useful statement
      (still about the assembly, NOT about the species).

This takes the protein-coding genes flanking zebrafish kcnh2a on GRCz11 chromosome 2, fetches one
protein per gene from Ensembl, maps them onto the assembly with miniprot, and reports how many land
on the same scaffold as the kcnh2b-like region and in what order.

Run: python3 synteny_kcnh2a.py GENOME.fna MINIPROT OUTDIR
"""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

GENOME, MP, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)

REGION = "2:23600000-24700000"
KCNH2A = ("ENSDARG00000029881", 24080694, 24168670)


def get(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(url, timeout=60).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(3)


genes = json.loads(get(f"https://rest.ensembl.org/overlap/region/danio_rerio/{REGION}"
                       "?feature=gene;content-type=application/json"))
genes = sorted([g for g in genes if g.get("biotype") == "protein_coding"], key=lambda g: g["start"])

seqs, ledger = [], []
for g in genes:
    gid = g["id"]
    try:
        fa = get(f"https://rest.ensembl.org/sequence/id/{gid}?type=protein;"
                 "multiple_sequences=1;content-type=text/x-fasta").decode()
    except Exception as e:
        ledger.append({"gene": gid, "name": g.get("external_name"), "error": str(e)})
        continue
    blocks = [b for b in fa.split(">") if b.strip()]
    best = max(blocks, key=lambda b: len("".join(b.split("\n")[1:])))
    s = "".join(best.split("\n")[1:]).replace("*", "")
    if len(s) < 50:
        ledger.append({"gene": gid, "name": g.get("external_name"), "error": "protein shorter than 50 aa"})
        continue
    name = f"{g.get('external_name') or gid}|{gid}|{g['start']}"
    seqs.append((name, s))
    ledger.append({"gene": gid, "name": g.get("external_name"), "zf_start": g["start"],
                   "zf_end": g["end"], "zf_strand": g["strand"], "protein_len": len(s),
                   "sha256": hashlib.sha256(s.encode()).hexdigest()})

fa_path = OUT / "neighbourhood.faa"
fa_path.write_text("".join(f">{n}\n{s}\n" for n, s in seqs))
print(f"{len(seqs)} neighbourhood proteins fetched, {len(genes)} genes in the region")

CH = 5
chunks = [OUT / f"sc{i}.fna" for i in range(CH)]
handles = [open(c, "w") for c in chunks]
sizes = [0] * CH
total = pathlib.Path(GENOME).stat().st_size
cur = 0
for line in open(GENOME):
    if line.startswith(">"):
        cur = min(int(sum(sizes) / (total / CH) + 1e-9), CH - 1)
    handles[cur].write(line)
    sizes[cur] += len(line)
for h in handles:
    h.close()

paf = ""
for c in chunks:
    paf += subprocess.run([MP, "-t4", "-N3", "--outs=0.6", str(c), str(fa_path)],
                          capture_output=True, text=True, check=True).stdout
    c.unlink()
(OUT / "synteny.paf").write_text(paf)

best = {}
for line in paf.splitlines():
    f = line.split("\t")
    tags = {x.split(":")[0]: x.split(":")[2] for x in f[12:]}
    a = int(tags.get("AS", 0))
    q = f[0]
    if q not in best or a > best[q]["AS"]:
        best[q] = {"AS": a, "scaffold": f[5], "start": int(f[7]), "end": int(f[8]),
                   "coverage": round((int(f[3]) - int(f[2])) / int(f[1]), 3),
                   "identity": round(int(f[9]) / int(f[10]), 3)}

TARGET = "JAGFBZ010001591.1"
rows = []
for name, _ in seqs:
    sym, gid, zstart = name.split("|")
    b = best.get(name)
    rows.append({"zebrafish_symbol": sym, "gene_id": gid, "zf_start": int(zstart),
                 "side_of_kcnh2a": "before" if int(zstart) < KCNH2A[1] else "after",
                 "hit": b, "on_target_scaffold": bool(b and b["scaffold"] == TARGET)})

on_t = [r for r in rows if r["on_target_scaffold"]]
mapped = [r for r in rows if r["hit"]]
scafs = {}
for r in mapped:
    scafs[r["hit"]["scaffold"]] = scafs.get(r["hit"]["scaffold"], 0) + 1
top = sorted(scafs.items(), key=lambda kv: -kv[1])[:5]

doc = {
    "scope": ("Protein-to-genome mapping of a zebrafish neighbourhood onto an unannotated assembly. "
              "Co-location of best hits is evidence about assembly content and gene order, not an "
              "orthology proof and not evidence of expression or function."),
    "question": ("Is the kcnh2a neighbourhood present in GCA_018398805.1, and is it on the same "
                 "scaffold as the kcnh2b-like region?"),
    "zebrafish_region": REGION,
    "kcnh2a_gene": {"id": KCNH2A[0], "start": KCNH2A[1], "end": KCNH2A[2],
                    "note": "the longfin(t2) abstract (PMID 34061172) places the overexpressed "
                            "kcnh2a on chromosome 2; Ensembl agrees, which is a consistency check "
                            "on this project's reading of that abstract"},
    "target_scaffold_of_the_kcnh2b_like_region": TARGET,
    "n_genes_in_region": len(genes),
    "n_proteins_fetched": len(seqs),
    "n_with_a_hit": len(mapped),
    "n_on_target_scaffold": len(on_t),
    "top_scaffolds_by_hit_count": top,
    "genes": rows,
    "fetch_ledger": ledger,
}
(OUT / "synteny.json").write_text(json.dumps(doc, indent=1) + "\n")
print(f"mapped {len(mapped)}/{len(seqs)}; on {TARGET}: {len(on_t)}")
print("top scaffolds:", top)
for r in sorted(rows, key=lambda r: r["zf_start"]):
    h = r["hit"]
    print(f"  {r['zebrafish_symbol']:22s} {r['side_of_kcnh2a']:6s} "
          f"{(h['scaffold'] + ' ' + str(h['start'])) if h else 'NO HIT':38s} "
          f"{('cov ' + str(h['coverage'])) if h else ''}")
