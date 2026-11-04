import sys, re, numpy as np, itertools
from collections import Counter
D=sys.argv[1]
rd=lambda f:''.join(l.strip() for l in open(f) if not l.startswith('>'))
S={'kcnk5b':rd(D+'/Q6PFU3.fa'),'and1':rd(D+'/E7F5V5.fa'),'and2':rd(D+'/A9JRX1.fa')}
print('and2 == A0ACM8QEN9:', S['and2']==rd(D+'/A0ACM8QEN9.fa'))
rng=np.random.default_rng(71)
def prof(s,K):
    return [sum(s[i]==s[i+k] for i in range(len(s)-k))/(len(s)-k) for k in range(1,K+1)]
def gm(a,K=80):
    return max((a[:-k]==a[k:]).mean() for k in range(1,K+1))
N=10000
for n,s in S.items():
    p=prof(s,80); obs=max(p); k=p.index(obs)+1
    a=np.array(list(s))
    nl=np.array([gm(rng.permutation(a)) for _ in range(N)])
    pct=(nl<obs).mean()*100
    print(f'{n} L={len(s)} obs={obs:.4f} k={k} nullmean={nl.mean():.4f} sd={nl.std():.4f} pct_below={pct:.1f} p(>=)={(nl>=obs).mean():.4f} max200 of first draws={nl[:200].max():.4f}')
    # sensitivity: K=L/2
    K=len(s)//2; p2=prof(s,K); o2=max(p2)
    nl2=np.array([gm(rng.permutation(a),K) for _ in range(1000)])
    print(f'   K={K}: obs={o2:.4f} k={p2.index(o2)+1} p={(nl2>=o2).mean():.3f}')
# Cys
for n,s in S.items():
    c=[i for i,x in enumerate(s) if x=='C']
    sp=Counter(c[j+1]-c[j] for j in range(len(c)-1))
    print(n,'nCys',len(c),'consecutive C-C spacings',sorted(sp.items()))
    ov=[m.start() for m in re.finditer(r'(?=C.{6,7}C)',s)]
    x6=len(re.findall(r'(?=C.{6}C)',s)); x7=len(re.findall(r'(?=C.{7}C)',s))
    print('   C-x(6,7)-C overlapping hits',len(ov),'x6',x6,'x7',x7, 'Cys used', len(set(ov)|set(h+8 for h in ov if s[h+8]=='C')|set(h+7 for h in ov if s[h+7]=='C')))
    # all-spacings scan: count C-x(k)-C pairs for k 0..30, vs shuffle
    def cnt(t,k): return len(re.findall(r'(?=C.{%d}C)'%k,t))
    obsk=[cnt(s,k) for k in range(31)]
    print('   C-x(k)-C counts k=0..30:',obsk)
# nulls for C-x(6,7)-C count: whole, block 20/40, and look-elsewhere (best of window k,k+1 over k=0..29)
def c67(t): return len(re.findall(r'(?=C.{6,7}C)',t))
def bestwin(t):
    return max(len(re.findall(r'(?=C.{%d,%d}C)'%(k,k+1),t)) for k in range(30))
def bshuf(a,B):
    b=a.copy()
    off=rng.integers(B)
    for i in range(-off,len(b),B):
        lo=max(0,i); seg=b[lo:i+B].copy(); rng.shuffle(seg); b[lo:i+B]=seg
    return b
for n in ('and1','and2'):
    s=S[n]; a=np.array(list(s)); o=c67(s)
    for lab,f in [('whole',lambda: rng.permutation(a)),('block20',lambda: bshuf(a,20)),('block10',lambda: bshuf(a,10))]:
        nl=np.array([c67(''.join(f())) for _ in range(5000)])
        print(n,lab,'obs',o,'mean',nl.mean().round(2),'max',nl.max(),'p',(nl>=o).mean())
    nl=np.array([bestwin(''.join(rng.permutation(a))) for _ in range(2000)])
    print(n,'look-elsewhere: best C-x(k,k+1)-C over k=0..29 in shuffles: mean',nl.mean().round(2),'max',nl.max(),'p',(nl>=o).mean())
# flank identity with Cys-preserving null: keep Cys positions fixed, shuffle non-Cys residues
def win(s,h): return s[h-6:h+16]
def pid(ws):
    skip={6,13,14}; idx=[i for i in range(22) if i not in skip]
    return np.mean([np.mean([a[i]==b[i] for i in idx]) for a,b in itertools.combinations(ws,2)])
for n in ('and1','and2'):
    s=S[n]; hits=[m.start() for m in re.finditer(r'(?=C.{6,7}C)',s)]
    hits=[h for h in hits if h>=6 and h+16<=len(s)]
    o=pid([win(s,h) for h in hits])
    cpos=[i for i,x in enumerate(s) if x=='C']; non=[i for i in range(len(s)) if s[i]!='C']
    nl=[]
    for _ in range(2000):
        t=list(s); vals=[s[i] for i in non]; rng.shuffle(vals)
        for i,v in zip(non,vals): t[i]=v
        t=''.join(t); nl.append(pid([win(t,h) for h in hits]))
    nl=np.array(nl)
    print(n,'flank id obs',round(o,3),'Cys-fixed shuffle null mean',nl.mean().round(3),'max',nl.max().round(3),'p',(nl>=o).mean())
    # flank identity excluding DP positions too: which columns drive it
    ws=[win(s,h) for h in hits]
    col=[np.mean([a[i]==b[i] for a,b in itertools.combinations(ws,2)]) for i in range(22)]
    print('   per-column identity',[round(x,2) for x in col])
    print('   x6/x7:',[len(re.match(r'C(.{6,7}?)C',s[h:]).group(1)) for h in hits])
