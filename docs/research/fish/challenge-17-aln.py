import sys
from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices
d=sys.argv[1]
def s(a): return str(next(SeqIO.parse(f"{d}/{a}.fa","fasta")).seq)
al=PairwiseAligner(); al.substitution_matrix=substitution_matrices.load("BLOSUM62")
al.open_gap_score=-11; al.extend_gap_score=-1; al.mode="local"
mm=s("Q9JK62")[:335]
names={"Q32PR9":"zf kcnk5a","Q6PFU3":"zf kcnk5b","O95279":"hs KCNK5","O14649":"hs KCNK3/TASK1","Q9NPC2":"hs KCNK9/TASK3","Q9H427":"hs KCNK15/TASK5","P57789":"hs KCNK10/TREK2","O95069":"hs KCNK2/TREK1","Q9NYG8":"hs KCNK4/TRAAK","Q9HB14":"hs KCNK13/THIK1"}
for q in ["Q32PR9","Q6PFU3"]:
  qs=s(q)
  for t,n in names.items():
    if t==q: continue
    a=al.align(qs, s(t) if t!="Q9JK62" else mm)[0]
    c=a.counts(); L=c.identities+c.mismatches+c.gaps
    print(f"{names[q]:10s} vs {n:18s} ident={c.identities}/{L} = {100*c.identities/L:.1f}%  aligned_q_len={a.aligned[0][-1][1]-a.aligned[0][0][0]}")
  a=al.align(qs,mm)[0]; c=a.counts(); L=c.identities+c.mismatches+c.gaps
  print(f"{names[q]:10s} vs mm Kcnk5 1-335 (6WLV construct) ident={c.identities}/{L} = {100*c.identities/L:.1f}% q-span {a.aligned[0][0][0]+1}-{a.aligned[0][-1][1]}")
