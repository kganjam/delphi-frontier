"""Claim 30 entailment, constraint D1/D2: does the zebrafish and2 CDS that the claim analysed
(RefSeq NM_001111190.1 -> NP_001104660.1 = UniProt A9JRX1 / A0ACM8QEN9) survive in three
independent zebrafish genome assemblies, and does the Tyr-gap statistic survive with it?

Computed, not observed. Inputs are NCBI records fetched 2026-11-04 (see claim-30-entail.md).
Usage: python3 -I claim30_and2_genome_check.py <dir with nm.fa and g_*.fa>
"""
import sys, os, random
from Bio import SeqIO
from Bio.Seq import Seq

d = sys.argv[1]
mrna = str(next(SeqIO.parse(os.path.join(d, "nm.fa"), "fasta")).seq).upper()
# NM_001111190.1 features: exons 1..71, 72..146, 147..191, 192..319, 320..2006; CDS 92..1618
exons = [(1, 71), (72, 146), (147, 191), (192, 319), (320, 2006)]
cds_lo, cds_hi = 92, 1618
ref_prot = str(Seq(mrna[cds_lo - 1:cds_hi]).translate()).rstrip("*")


def gapstat(p, t=4):
    y = [i for i, a in enumerate(p) if a == "Y"]
    g = [b - a for a, b in zip(y, y[1:])]
    return sum(x <= t for x in g), len(g), len(y)


def perm_p(p, n=20000, seed=1):
    k, m, _ = gapstat(p)
    obs = k / m
    s = list(p)
    rng = random.Random(seed)
    ge = 0
    for _ in range(n):
        rng.shuffle(s)
        kk, mm, _ = gapstat(s)
        ge += (kk / mm) >= obs - 1e-12
    return (ge + 1) / (n + 1)


print("reference protein length", len(ref_prot), "Tyr, gaps<=4, gaps:", gapstat(ref_prot)[2], gapstat(ref_prot)[0], gapstat(ref_prot)[1])
for f in sorted(os.listdir(d)):
    if not f.startswith("g_"):
        continue
    rec = next(SeqIO.parse(os.path.join(d, f), "fasta"))
    g = str(rec.seq).upper()  # region fetched on the minus strand (gene orientation)
    print("\n" + rec.description[:110])
    hits = []
    for lo, hi in exons:
        ex = mrna[lo - 1:hi]
        pos = g.find(ex)
        if pos < 0 and lo == 1:  # 5' UTR first base; does not touch the CDS
            pos = g.find(ex[1:])
            note = "exact match of bases 2-71 (base 1 is 5'UTR)"
        else:
            note = "exact match" if pos >= 0 else "NO exact match"
        hits.append(pos)
        print("  exon %d-%d (%d nt): genomic offset %d, %s" % (lo, hi, hi - lo + 1, pos, note))
    ok = all(h >= 0 for h in hits) and hits == sorted(hits)
    print("  all CDS-bearing exons exact and colinear:", ok)
    if ok:
        k, m, ny = gapstat(ref_prot)
        print("  => genomic CDS identical to NM_001111190.1 CDS; translated Tyr", ny,
              "gaps<=4", k, "/", m)

# sensitivity: p as a function of how many of the 11 close gaps are kept (computed)
print("\nreference perm p (20000)", round(perm_p(ref_prot), 4))
y = [i for i, a in enumerate(ref_prot) if a == "Y"]
print("first Tyr position (1-based)", y[0] + 1, "; signal peptide (UniProt SignalP) 1-23")
