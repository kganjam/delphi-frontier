import sys, re, numpy as np, itertools
D=sys.argv[1]
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
S={'and1':rd(f'{D}/E7F5V5.fa'),'and2':rd(f'{D}/A9JRX1.fa')}
def win(s,h): return s[h-6:h+16]  # 22 aa, first C at index 6
def pid(ws, skip):
    v=[]
    for a,b in itertools.combinations(ws,2):
        idx=[i for i in range(22) if i not in skip]
        v.append(np.mean([a[i]==b[i] for i in idx]))
    return np.mean(v)
rng=np.random.default_rng(3)
for n,s in S.items():
    hits=[m.start() for m in re.finditer(r'(?=C.{6,7}C)',s)]
    ws=[win(s,h) for h in hits]
    skip={6,13,14}  # both possible second-C positions + anchor C
    obs=pid(ws,skip)
    nl=[]
    for _ in range(2000):
        hs=rng.choice(np.arange(6,len(s)-16),len(hits),replace=False)
        nl.append(pid([win(s,h) for h in hs],skip))
    nl=np.array(nl); print(n,f'module flank identity (C excluded) obs={obs:.3f} random-window null mean={nl.mean():.3f} max={nl.max():.3f} p={(nl>=obs).mean():.4f}')
