import sys, json, random
import numpy as np
D = sys.argv[1]
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
S = {'kcnk5b': rd(f'{D}/Q6PFU3.fa'), 'and1': rd(f'{D}/E7F5V5.fa'), 'and2': rd(f'{D}/A9JRX1.fa')}
AA = 'ACDEFGHIKLMNPQRSTVWY'

def enc(s): return np.frombuffer(s.encode(), dtype=np.uint8)

def offset_ident(a, kmax=80):
    return np.array([(a[:-k] == a[k:]).mean() for k in range(1, kmax+1)])

def win_ident(a, kmax=80, W=50):
    # max over offsets and over windows of W consecutive comparisons
    best = 0.0
    for k in range(1, kmax+1):
        m = (a[:-k] == a[k:]).astype(np.int32)
        if len(m) < W: continue
        c = np.convolve(m, np.ones(W, dtype=np.int32), 'valid')
        best = max(best, c.max()/W)
    return best

def stats(a):
    oi = offset_ident(a)
    return oi.max(), int(oi.argmax())+1, win_ident(a)

rng = np.random.default_rng(29)
def shuf(a):
    b = a.copy(); rng.shuffle(b); return b

out = {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
for name, s in S.items():
    a = enc(s)
    f = np.bincount(a, minlength=256)/len(a)
    g, gk, w = stats(a)
    ng, nw = [], []
    for _ in range(N):
        b = shuf(a); x = stats(b); ng.append(x[0]); nw.append(x[2])
    ng, nw = np.array(ng), np.array(nw)
    first200 = ng[:200]
    # kmer recurrence
    km = {}
    for k in (5, 6, 7):
        c = {}
        for i in range(len(s)-k+1): c[s[i:i+k]] = c.get(s[i:i+k], 0)+1
        km[k] = sorted(c.items(), key=lambda t: -t[1])[:3]
    out[name] = dict(L=len(s), sumf2=float((f**2).sum()), max_obs=float(g), at_offset=gk,
        null_mean=float(ng.mean()), null_sd=float(ng.std()), null_max200=float(first200.max()),
        null_mean200=float(first200.mean()), null_maxN=float(ng.max()),
        p_global=float((ng >= g).mean()), z_global=float((g-ng.mean())/ng.std()),
        win_obs=float(w), win_null_mean=float(nw.mean()), win_null_95=float(np.quantile(nw, .95)),
        p_win=float((nw >= w).mean()), top_kmers={k: v for k, v in km.items()})
print(json.dumps(out, indent=1))
