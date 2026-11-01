#!/usr/bin/env python3
"""Map zebrafish UniProt proteins to the Hirundichthys speculiger assembly with miniprot.

Computed comparison only: protein-to-genome alignment, no annotation, no function.
Run:  python3 map_proteins.py GENOME.fna MINIPROT_BIN OUTDIR
Controls: actb1 (conserved positive, P53486-like fetched below) and a shuffled
fgf10a sequence (negative, fixed seed). Identity here is miniprot's own PAF/GFF value.
"""
import time, hashlib, json, random, subprocess, sys, urllib.request, datetime, pathlib

GENOME, MP, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
GENES = {"tbx5a": "Q9IAK8", "fgf10a": "Q8AY90", "shha": "Q92008", "hoxd13a": "Q90472",
         "hoxa13a": "Q6W990", "msxb": "Q03356", "kcnk5b": "Q6PFU3", "and1": "E7F5V5",
         "pitx1": "A9Y0D5", "tbx4": "F1R688", "fgf24": "Q0IIQ7", "edar": "A0A0R4IGE7",
         "actb1_POSITIVE_CONTROL": "Q7ZVI7"}
def fetch(acc):
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    for i in range(4):
        try:
            return url, urllib.request.urlopen(url, timeout=60).read().decode()
        except Exception:
            if i == 3: raise
            time.sleep(3)
seqs, ledger = {}, []
for g, acc in GENES.items():
    url, fa = fetch(acc)
    s = "".join(fa.split("\n")[1:]); hdr = fa.split("\n")[0]
    seqs[g] = s
    ledger.append({"gene": g, "uniprot": acc, "header": hdr, "url": url, "len": len(s),
                   "sha256": hashlib.sha256(fa.encode()).hexdigest(),
                   "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")})
rnd = random.Random(12345)
sh = list(seqs["fgf10a"]); rnd.shuffle(sh); seqs["fgf10a_SHUFFLED_NEGATIVE_CONTROL"] = "".join(sh)
fa = OUT / "queries.faa"
fa.write_text("".join(f">{g}\n{s}\n" for g, s in seqs.items()))
# miniprot indexing of the whole 1.04 Gb assembly exceeded the 4 GB cap (measured: SIGKILL),
# so the assembly is split into ~5 chunks of whole scaffolds, each mapped separately and merged.
CH = 5; chunks = [OUT / f"chunk{i}.fna" for i in range(CH)]
sizes = [0] * CH; cur = 0; handles = [open(c, "w") for c in chunks]; total = pathlib.Path(GENOME).stat().st_size
for line in open(GENOME):
    if line.startswith(">"):
        cur = min(int(sum(sizes) / (total / CH) + 1e-9), CH - 1)
    handles[cur].write(line); sizes[cur] += len(line)
for h in handles: h.close()
class P: pass
paf = P(); paf.stdout = ""
for c in chunks:
    paf.stdout += subprocess.run([MP, "-t4", "-N5", "--outs=0.6", str(c), str(fa)], capture_output=True, text=True, check=True).stdout
    c.unlink()
(OUT / "miniprot.paf").write_text(paf.stdout)
(OUT / "miniprot.version.txt").write_text(subprocess.run([MP, "--version"], capture_output=True, text=True).stdout)
rows = {}
for line in paf.stdout.splitlines():
    f = line.split("\t")
    q, ql, qs, qe, strand, t, tl, ts, te, nm, bl = f[0], int(f[1]), int(f[2]), int(f[3]), f[4], f[5], int(f[6]), int(f[7]), int(f[8]), int(f[9]), int(f[10])
    tags = {x.split(":")[0]: x.split(":")[2] for x in f[12:]}
    rows.setdefault(q, []).append({"scaffold": t, "strand": strand, "t_start": ts, "t_end": te,
        "query_aa_covered": qe - qs, "query_len": ql, "coverage": round((qe - qs) / ql, 3),
        "aa_identity": round(nm / bl, 3), "miniprot_score_AS": int(tags.get("AS", 0)),
        "frameshifts_or_stops": {"fs": "frameshift" in line, "st": tags.get("ST")}})
res = {"genome": "GCA_018398805.1 Hirundichthys speculiger_1.0 (scaffold level, no annotation)",
       "tool": "miniprot", "queries": ledger, "hits": {g: sorted(v, key=lambda r: -r["miniprot_score_AS"]) for g, v in rows.items()},
       "no_hit": [g for g in seqs if g not in rows]}
(OUT / "mapping_summary.json").write_text(json.dumps(res, indent=1))
for g in seqs:
    h = res["hits"].get(g)
    print(g, "NO HIT" if not h else (h[0]["coverage"], h[0]["aa_identity"], len(h)))
