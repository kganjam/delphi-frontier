import random, numpy as np
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def st(s):
    a=np.frombuffer(s.encode(),dtype=np.uint8)
    return max((a[:-p]==a[p:]).mean() for p in range(1,81))
for name,f in [('kcnk5b','seq/Q6PFU3.fa'),('and1','seq/E7F5V5.fa'),('and2','seq/A0ACM8QEN9.fa')]:
    s=rd(f); o=st(s); from collections import Counter
    c=Counter(s); sf=sum((v/len(s))**2 for v in c.values())
    for seed in [1,2,3]:
        r=random.Random(seed); n=[]
        for k in range(200):
            t=list(s); r.shuffle(t); n.append(st(''.join(t)))
        n=np.array(n); print(name,'obs %.3f sumf2 %.3f null mean %.3f max %.3f  p=%.3f'%(o,sf,n.mean(),n.max(),(1+(n>=o).sum())/201))
