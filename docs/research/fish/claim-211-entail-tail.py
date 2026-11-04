# Tail-homology check vs teleost orthologs. Usage: python3 -I claim-211-entail-tail.py <dir> A0A6P6M099 A0A2D0PX72 A0A6J2V4H0 A0A4W6D0U6 A0A672ZYS1 Q32PR9
import sys,random
from Bio import Align
from Bio.Align import substitution_matrices
d=sys.argv[1]
fa=lambda p:"".join(l.strip() for l in open(p) if not l.startswith(">"))
q=fa(d+"/Q6PFU3.fasta")
al=Align.PairwiseAligner(); al.substitution_matrix=substitution_matrices.load("BLOSUM62"); al.open_gap_score=-11; al.extend_gap_score=-1; al.mode="local"
for a in sys.argv[2:]:
    t=fa(f"{d}/{a}.fasta")
    for lo,hi in [(312,448),(1,250)]:
        sub=q[lo-1:hi]; L=al.align(sub,t)[0]
        idn=sum(1 for (s1,e1),(s2,e2) in zip(*L.aligned) for k in range(e1-s1) if sub[s1+k]==t[s2+k])
        qs,qe=lo+L.aligned[0][0][0],lo-1+L.aligned[0][-1][1]
        random.seed(0); sc=sorted(al.align("".join(random.sample(sub,len(sub))),t).score for _ in range(200))
        print(f"{a} len {len(t)} | query {lo}-{hi}: covers {qs}-{qe} ({qe-qs+1} aa), id {idn}/{qe-qs+1}={idn/(qe-qs+1):.2f}, score {L.score:.0f} vs shuffled median {sc[100]:.0f} max {sc[-1]:.0f}")
