import sys,random,statistics as st
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def pairs(s,a,d):
    idx=[i for i,c in enumerate(s) if c==a]
    return sum(1 for x in range(len(idx)) for y in range(x+1,len(idx)) if idx[y]-idx[x]<=d)
N=2000
for f in sys.argv[1:]:
    s=rd('dl/'+f+'.fasta'); print(f,len(s),'C=',s.count('C'),'K=',s.count('K'),'CxxC',sum(1 for i in range(len(s)-3) if s[i]=='C' and s[i+3]=='C'))
    for a in 'CK':
      for d in (1,2,3,4,5):
        o=pairs(s,a,d); random.seed(1); L=list(s); n=[]
        for _ in range(N): random.shuffle(L); n.append(pairs(L,a,d))
        m=st.mean(n); sd=st.pstdev(n)
        plo=(1+sum(x<=o for x in n))/(N+1); phi=(1+sum(x>=o for x in n))/(N+1)
        print(f' {a} d<={d} obs={o} null={m:.2f}±{sd:.2f} z={(o-m)/sd if sd else float("nan"):.2f} p_lo={plo:.4f} p_hi={phi:.4f}')
