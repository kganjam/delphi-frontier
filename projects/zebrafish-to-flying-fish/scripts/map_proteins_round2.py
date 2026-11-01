#!/usr/bin/env python3
"""Round-2 protein-to-genome mapping onto the Hirundichthys speculiger assembly.

Same method as map_proteins.py (miniprot, whole-scaffold chunking to stay inside the
memory cap), but the query set is read from a JSON file so the gene list can grow with
the literature. Round 2 adds the loci named by the 2021 flying-fish phylogenomic paper
(kcnh2a, LAT4/slc43a2), the bioelectric chain (rcan2, cacna1g, gja1/cx43), hhip, shhb
and and2, plus the same two controls.

Computed comparison only: an alignment is not an annotation, an ortholog call or a
function. Identity values are miniprot's own PAF residue-match count over alignment block length.

Run: python3 map_proteins_round2.py GENOME.fna MINIPROT_BIN QUERIES.json OUTDIR
"""
import datetime
import hashlib
import json
import pathlib
import random
import subprocess
import sys
import time
import urllib.request

GENOME, MP, QJSON, OUT = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
GENES = json.load(open(QJSON))


def fetch(acc):
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    for i in range(4):
        try:
            return url, urllib.request.urlopen(url, timeout=60).read().decode()
        except Exception:
            if i == 3:
                raise
            time.sleep(3)


seqs, ledger = {}, []
for g, spec in GENES.items():
    acc = spec["uniprot"]
    url, fa = fetch(acc)
    s = "".join(fa.split("\n")[1:])
    ledger.append({"gene": g, "uniprot": acc, "header": fa.split("\n")[0], "url": url, "len": len(s),
                   "sha256": hashlib.sha256(fa.encode()).hexdigest(),
                   "why": spec.get("why"), "name_mapping_confidence": spec.get("name_mapping_confidence"),
                   "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")})
    seqs[g] = s

rnd = random.Random(12345)
base = next(iter(seqs))
sh = list(seqs[base])
rnd.shuffle(sh)
seqs[f"{base}_SHUFFLED_NEGATIVE_CONTROL"] = "".join(sh)

fa_path = OUT / "queries_round2.faa"
fa_path.write_text("".join(f">{g}\n{s}\n" for g, s in seqs.items()))

CH = 5
chunks = [OUT / f"r2chunk{i}.fna" for i in range(CH)]
sizes = [0] * CH
handles = [open(c, "w") for c in chunks]
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
    r = subprocess.run([MP, "-t4", "-N5", "--outs=0.6", str(c), str(fa_path)],
                       capture_output=True, text=True, check=True)
    paf += r.stdout
    c.unlink()
(OUT / "miniprot_round2.paf").write_text(paf)
(OUT / "miniprot_round2.version.txt").write_text(
    subprocess.run([MP, "--version"], capture_output=True, text=True).stdout)

rows = {}
for line in paf.splitlines():
    f = line.split("\t")
    q, ql, qs, qe, strand, t = f[0], int(f[1]), int(f[2]), int(f[3]), f[4], f[5]
    ts, te, nm, bl = int(f[7]), int(f[8]), int(f[9]), int(f[10])
    tags = {x.split(":")[0]: x.split(":")[2] for x in f[12:]}
    rows.setdefault(q, []).append({
        "scaffold": t, "strand": strand, "t_start": ts, "t_end": te,
        "query_aa_covered": qe - qs, "query_len": ql, "coverage": round((qe - qs) / ql, 3),
        "aa_identity": round(nm / bl, 3), "miniprot_score_AS": int(tags.get("AS", 0)),
        "frameshifts_or_stops": {"fs": "frameshift" in line, "st": tags.get("ST")}})

res = {
    "genome": "GCA_018398805.1 Hirundichthys speculiger_1.0 (scaffold level, no annotation)",
    "genome_fasta_sha256": hashlib.sha256(pathlib.Path(GENOME).read_bytes()).hexdigest(),
    "tool": "miniprot",
    "tool_version": (OUT / "miniprot_round2.version.txt").read_text().strip(),
    "params": "-t4 -N5 --outs=0.6, assembly split into 5 whole-scaffold chunks",
    "scope": "Protein-to-genome alignment of Danio rerio query proteins. Not an annotation, not an "
             "ortholog assignment, not evidence of expression or function in Hirundichthys. "
             "aa_identity = PAF residue matches (col 10) / alignment block length (col 11). "
             "Secondary-hit counts are per-chunk artefacts of -N5/--outs applied to 5 chunks.",
    "queries": ledger,
    "hits": {g: sorted(v, key=lambda r: -r["miniprot_score_AS"]) for g, v in rows.items()},
    "no_hit": [g for g in seqs if g not in rows],
}
(OUT / "mapping_summary_round2.json").write_text(json.dumps(res, indent=1) + "\n")
for g in seqs:
    h = res["hits"].get(g)
    print(g, "NO HIT" if not h else (h[0]["coverage"], h[0]["aa_identity"], len(h)))
