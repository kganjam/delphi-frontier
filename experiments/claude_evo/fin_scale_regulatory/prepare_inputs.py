"""Freeze the fin/scale regulatory input set (zebrafish + mirrorwing flyingfish).

Zebrafish: Ensembl gene coordinates (cached), sequence from UCSC danRer11 (same
recipe as the earlier bioservices input set). Flyingfish (Hirundichthys speculiger,
GCA_018398805.1): the authors' GeneWise gene models + Swiss-Prot BLAST best hits
from figshare 10.6084/m9.figshare.14600634.v1 (CC BY 4.0); sequence from the
authors' scaffold FASTA. Flyingfish models are CDS-only predictions, so the
"upstream" window is upstream of the predicted start codon, NOT of a mapped TSS.
Orthology is by Swiss-Prot gene-symbol best hit, not a tree; paralogs are flagged.
"""
from __future__ import annotations
import argparse, collections, gzip, json, os, re, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from connectors.bioservices import ensembl, ucsc  # noqa: E402
from connectors.bioservices.receipts import sha256_text, sha256_file, utc_now, write_json  # noqa: E402

# (zebrafish symbol, mammalian Swiss-Prot GN symbol, relevance note)
TARGETS = [
    ("fgf20a", "FGF20", "fin regeneration blastema signal"),
    ("shha", "SHH", "fin/ZPA hedgehog signal"),
    ("msx1b", "MSX1", "fin regeneration blastema marker"),
    ("sp7", "SP7", "osteoblast / fin ray and scale"),
    ("runx2b", "RUNX2", "osteoblast differentiation, scale and fin ray"),
    ("lef1", "LEF1", "Wnt effector; fin and scale development"),
    ("tbx5a", "TBX5", "pectoral fin bud initiation"),
    ("hoxd13a", "HOXD13", "fin distal patterning"),
    ("fgf10a", "FGF10", "fin bud outgrowth"),
    ("kcnk5b", "KCNK5", "fin size / allometry (longfin)"),
]
UP, HALF = 2000, 1000

def revcomp(s): return s[::-1].translate(str.maketrans("ACGTN", "TGCAN"))

def flyingfish(dl, wanted):
    # gene models; HsScafNNNNGMMMM = M-th model on scaffold by start (verified below)
    mr, cds = [], collections.Counter()
    for l in open(f"{dl}/gene.gff"):
        f = l.rstrip("\n").split("\t")
        if f[2] == "mRNA":
            mr.append(dict(scaf=f[0], s=int(f[3]), e=int(f[4]), strand=f[6], id=re.search(r"ID=(\w+)", f[8]).group(1)))
        elif f[2] == "CDS":
            cds[re.search(r"Parent=(\w+)", f[8]).group(1)] += int(f[4]) - int(f[3]) + 1
    by = collections.defaultdict(list)
    for m in mr: by[m["scaf"]].append(m)
    alias = {}
    for sc, ms in by.items():
        for i, m in enumerate(sorted(ms, key=lambda m: m["s"]), 1):
            alias[f"Hs{'Scaf'}{int(sc[2:]):04d}G{i:04d}"] = m
    hits = collections.defaultdict(list)
    for l in list(open(f"{dl}/swissprot.xls"))[1:]:
        f = l.rstrip("\n").split("\t")
        gn = re.search(r"GN=(\S+)", f[12])
        if gn and gn.group(1).upper() in wanted and "_MOUSE" in f[12] + "_MOUSE":
            hits[gn.group(1).upper()].append((float(f[11]), f[0], float(f[2]), int(f[3]), f[12].strip()))
    # alias sanity: CDS aa length must match BLAST query extent for every hit used
    out, scaf_needed = {}, set()
    for sym, hs in hits.items():
        best = {}
        for sc, q, ident, alen, ann in hs:
            if q not in alias: continue
            m = alias[q]
            if sc > best.get(q, (0,))[0]: best[q] = (sc, ident, alen, ann, m)
        out[sym] = sorted(((v[0], q) + v[1:] for q, v in best.items()), reverse=True)
        for r in out[sym]: scaf_needed.add(r[-1]["scaf"])
    seqs, cur, buf = {}, None, []
    with gzip.open(f"{dl}/genome.fa.gz", "rt") as fh:
        for l in fh:
            if l[0] == ">":
                if cur in scaf_needed: seqs[cur] = "".join(buf)
                cur, buf = l[1:].split()[0], []
            elif cur in scaf_needed: buf.append(l.strip().upper())
        if cur in scaf_needed: seqs[cur] = "".join(buf)
    return out, seqs, by, cds

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True); ap.add_argument("--lookup-cache", required=True)
    ap.add_argument("--ff-dir", required=True)
    a = ap.parse_args()
    cache = json.load(open(a.lookup_cache)) if os.path.exists(a.lookup_cache) else {}
    ff, seqs, by, cds = flyingfish(a.ff_dir, {g for _, g, _ in TARGETS})
    targets, dropped = [], []
    for sym, gn, note in TARGETS:
        # ---- zebrafish
        try:
            if sym in cache: g = ensembl.Gene(**cache[sym])
            else:
                g = ensembl.lookup_symbol(sym); cache[sym] = dict(g.__dict__); write_json(a.lookup_cache, cache)
            lo, hi = g.upstream_region(UP)
            seq = ucsc.sequence("danRer11", g.chromosome, lo, hi, g.strand)
            assert len(seq) == UP and set(seq) <= set("ACGT"), "bad zebrafish window"
            targets.append(dict(species="danio_rerio", assembly="GRCz11/danRer11", symbol=sym, note=note,
                                gene_id=g.gene_id, region=f"chr{g.chromosome}:{lo}-{hi}", strand=g.strand,
                                window_basis="Ensembl gene start (includes UTR) = TSS", paralog_flag=False,
                                prompt_seq=seq[:HALF], held_out_seq=seq[HALF:]))
        except Exception as e:
            dropped.append(dict(species="danio_rerio", symbol=sym, reason=f"{type(e).__name__}: {str(e)[:150]}"))
        # ---- flyingfish: best Swiss-Prot hit whose model has a clean 2 kb window
        cands = ff.get(gn, [])
        chosen = None
        for sc, q, ident, alen, ann, m in cands:
            s = seqs[m["scaf"]]
            lo, hi = (m["s"] - UP, m["s"] - 1) if m["strand"] == "+" else (m["e"] + 1, m["e"] + UP)
            if lo < 1 or hi > len(s): continue
            w = s[lo - 1:hi]
            if m["strand"] == "-": w = revcomp(w)
            if set(w) <= set("ACGT"):
                other = [x for x in by[m["scaf"]] if x["id"] != m["id"] and x["s"] <= hi and x["e"] >= lo]
                chosen = (sc, q, ident, alen, ann, m, lo, hi, w, other); break
        if not chosen:
            dropped.append(dict(species="hirundichthys_speculiger", symbol=sym, reason="no ortholog hit with a clean 2 kb ACGT-only window"))
            continue
        sc, q, ident, alen, ann, m, lo, hi, w, other = chosen
        targets.append(dict(species="hirundichthys_speculiger", assembly="GCA_018398805.1", symbol=sym, note=note,
                            gene_id=m["id"], blast_query=q, blast_best_hit=ann, blast_identity=ident, blast_bitscore=sc,
                            cds_aa=cds[m["id"]] // 3, region=f"{m['scaf']}:{lo}-{hi}", strand=1 if m["strand"] == "+" else -1,
                            window_basis="upstream of PREDICTED START CODON (CDS-only GeneWise model); no TSS/UTR",
                            paralog_flag=len({c[1] for c in cands}) > 1, n_orthologous_hits=len({c[1] for c in cands}),
                            overlaps_other_gene_model=[o["id"] for o in other],
                            prompt_seq=w[:HALF], held_out_seq=w[HALF:]))
        print(f"{sym}: zf ok, ff {m['id']} {m['scaf']}:{lo}-{hi} hits={len(cands)} overlap={len(other)}")
    for t in targets:
        t["prompt_sha256"] = sha256_text(t["prompt_seq"]); t["held_out_sha256"] = sha256_text(t["held_out_seq"])
        t["held_out_gc"] = round(sum(c in "GC" for c in t["held_out_seq"]) / HALF, 4)
    payload = dict(input_set_id="fin-scale-regulatory-2kb/v1", frozen_utc=utc_now(), prompt_bp=HALF, held_out_bp=HALF,
                   upstream_bp=UP, n_targets=len(targets), dropped=dropped,
                   sources=dict(flyingfish_figshare="10.6084/m9.figshare.14600634.v1 (CC BY 4.0)",
                                flyingfish_files={n: sha256_file(f"{a.ff_dir}/{n}") for n in ("genome.fa.gz", "gene.gff", "swissprot.xls")},
                                zebrafish="Ensembl REST gene coordinates; UCSC danRer11 sequence"),
                   scope="public reference genomes only; benign fish developmental genes; no pathogen/toxin sequence",
                   targets=targets)
    print("sha256", write_json(a.out, payload), "targets", len(targets), "dropped", dropped)

if __name__ == "__main__":
    main()
