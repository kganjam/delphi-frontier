import numpy as np
def r(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def mx(a,K=80):
    L=len(a); return max((a[:L-k]==a[k:]).mean() for k in range(1,K+1))
rng=np.random.default_rng(7)
for name,f in [('and1','dl/E7F5V5.fa'),('and2','dl/A0ACM8QEN9.fa')]:
    a=np.frombuffer(r(f).encode(),dtype=np.uint8).copy(); o=mx(a)
    L=len(a); best=max(range(1,81),key=lambda k:(a[:L-k]==a[k:]).mean())
    v=np.array([mx(rng.permutation(a)) for _ in range(10000)])
    ge=(v>=o-1e-12).sum(); p=ge/len(v); se=np.sqrt(p*(1-p)/len(v))
    print(name,f'obs={o:.4f} at offset {best} matches={int((a[:L-best]==a[best:]).sum())}/{L-best} sumf2={sum((np.bincount(a)/L)**2):.4f} mean={v.mean():.4f} sd={v.std():.4f} 95pct={np.percentile(v,95):.4f} pct_below={(v<o).mean():.4f} p_ge={p:.4f}±{se:.4f}')
