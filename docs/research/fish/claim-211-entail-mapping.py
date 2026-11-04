# Reproduces the computed numbers in claim-211-entail.md.
# Inputs: a directory holding kcnk5b_pdb70.a3m (git show 8bf7ee39:results/fish-proteins/structures/kcnk5b_pdb70.a3m)
# and UniProt FASTA files Q6PFU3, O95279, Q9JK62 (rest.uniprot.org/uniprotkb/<acc>.fasta).
# Usage: python3 -I claim-211-entail-mapping.py <dir>
import sys,re
from Bio import Align
from Bio.Align import substitution_matrices
d=sys.argv[1]
def fa(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">"))
recs=[];cur=None
for l in open(d+"/kcnk5b_pdb70.a3m"):
    l=l.strip()
    if l.startswith(">"): cur=[l[1:],""];recs.append(cur)
    else: cur[1]+=l
q=recs[0][1]; zf=fa(d+"/Q6PFU3.fasta"); hs=fa(d+"/O95279.fasta"); mm=fa(d+"/Q9JK62.fasta")
print("query len",len(q),"Q6PFU3 len",len(zf),"identical:",q==zf)
# 6WLV construct sequence from PDBe (1-335 mouse + tag)
wlv="MVDRGPLLTSAIIFYLAIGAAIFEVLEEPHWKEAKKNYYTQKLHLLKEFPCLSQEGLDKILQVVSDAADQGVAITGNQTFNNWNWPNAMIFAATVITTIGYGNVAPKTPAGRLFCVFYGLFGVPLCLTWISALGKFFGGRAKRLGQFLTRRGVSLRKAQITCTAIFIVWGVLVHLVIPPFVFMVTEEWNYIEGLYYSFITISTIGFGDFVAGVNPSANYHALYRYFVELWIYLGLAWLSLFVNWKVSMFVEVHKAIKKRRRRRKESFESSPHSRKALQMAGSTASKDVNIFSFLSKKEETYNDLIKQIGKKAMKTSGGGERVPGPGHGLGPQGDRSNSLEVLF"
print("6WLV construct 1-335 == mouse Q9JK62[0:335]:", wlv[:335]==mm[:335], "tag:",wlv[335:])
al=Align.PairwiseAligner(); al.substitution_matrix=substitution_matrices.load("BLOSUM62")
al.open_gap_score=-11; al.extend_gap_score=-1; al.mode="global"
def mapping(a,b):
    A=al.align(a,b)[0]; m={}
    for (s1,e1),(s2,e2) in zip(*A.aligned):
        for k in range(e1-s1): m[s1+k+1]=s2+k+1
    return A,m
A,m=mapping(q,mm)
inv={v:k for k,v in m.items()}
def near(mp,x):
    ks=[k for k in mp if k<=x]; return (max(ks), mp[max(ks)]) if ks else None
print("query 311 -> mouse", near(m,311)); print("mouse 260 -> query", near(inv,260)); print("mouse 335 -> query", near(inv,335))
def ident(a,b,lo,hi,name):
    sub=q[lo-1:hi]; al.mode="local"; L=al.align(sub,b)[0]; al.mode="global"
    idn=sum(1 for (s1,e1),(s2,e2) in zip(*L.aligned) for k in range(e1-s1) if sub[s1+k]==b[s2+k])
    alen=L.aligned[0][-1][1]-L.aligned[0][0][0]
    tspan=(L.aligned[1][0][0]+1,L.aligned[1][-1][1])
    print(f"{name}: query {lo}-{hi} local aln covers query {lo+L.aligned[0][0][0]}-{lo-1+L.aligned[0][-1][1]}, target {tspan}, identities {idn}/{alen} = {idn/alen:.2f}, score {L.score}")
    # shuffled control
    import random; random.seed(0); sc=[]
    for _ in range(200):
        s=list(sub); random.shuffle(s); al.mode="local"; sc.append(al.align("".join(s),b).score); al.mode="global"
    sc.sort(); print(f"   shuffled-query local scores (n=200): median {sc[100]}, max {sc[-1]}")
for name,t in [("mouse",mm),("human",hs)]:
    ident(q,t,312,448,name); ident(q,t,326,448,name); ident(q,t,1,250,name)
