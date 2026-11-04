import sys, random, numpy as np
from Bio.Align import substitution_matrices as sm
B=sm.load('BLOSUM62'); AA=B.alphabet
idx={a:i for i,a in enumerate(AA)}; M=np.array(B)
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def stat(s):
    x=np.array([idx[c] for c in s]); L=len(x); best=(-1e9,0,0,0)
    for p in range(1,L//2+1):
        d=M[x[:-p],x[p:]]             # s[i] vs s[i+p]
        P=np.concatenate([[0],np.cumsum(d)])  # prefix
        n=len(d)
        if n<p: break
        # best segment of length >= p (two adjacent copies of period p)
        runmin=np.minimum.accumulate(P[:n-p+1])
        sc=P[p:]-runmin
        j=int(np.argmax(sc)); v=sc[j]
        if v>best[0]:
            i=int(np.argmin(P[:j+1])); best=(float(v),p,i,j+p)
    return best
def ident_stat(s):
    # longest stretch where s[i]==s[i+p] with >=50% identity over >=2 copies: simpler: max identical-run length fraction
    L=len(s); best=(0,0)
    for p in range(1,L//2+1):
        r=0
        for i in range(L-p):
            r=r+1 if s[i]==s[i+p] else 0
            if r>best[0]: best=(r,p)
    return best
N=200; rng=random.Random(20261104)
for f in sys.argv[1:]:
    s=rd(f); o=stat(s); oi=ident_stat(s)
    null=[];nulli=[]
    for k in range(N):
        t=list(s); rng.shuffle(t); t=''.join(t)
        null.append(stat(t)[0]); nulli.append(ident_stat(t)[0])
    null=np.array(null); nulli=np.array(nulli)
    pv=(1+(null>=o[0]).sum())/(N+1); pvi=(1+(nulli>=oi[0]).sum())/(N+1)
    print(f, len(s), 'obs',o, 'null mean %.1f sd %.1f max %.1f'%(null.mean(),null.std(),null.max()),'z %.2f'%((o[0]-null.mean())/null.std()),'p',round(pv,4))
    print('   seg', s[o[2]:o[3]+1] if o[3]-o[2]<200 else '(long)')
    print('   exact-run obs',oi,'null mean %.1f max %d'%(nulli.mean(),nulli.max()),'p',round(pvi,4))
