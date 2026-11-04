import sys, re, numpy as np
D=sys.argv[1]
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
S={'kcnk5b':rd(f'{D}/Q6PFU3.fa'),'and1':rd(f'{D}/E7F5V5.fa'),'and2':rd(f'{D}/A9JRX1.fa')}
enc=lambda s: np.frombuffer(s.encode(),dtype=np.uint8)
def gmax(a): return max((a[:-k]==a[k:]).mean() for k in range(1,81))
rng=np.random.default_rng(7)
def block_shuf(a,B):
    b=a.copy()
    for i in range(0,len(b),B):
        seg=b[i:i+B].copy(); rng.shuffle(seg); b[i:i+B]=seg
    return b
for n,s in S.items():
    a=enc(s); g=gmax(a)
    for B in (20,40):
        nl=np.array([gmax(block_shuf(a,B)) for _ in range(1000)])
        print(n,f'blockshuffle B={B}: obs={g:.3f} null mean={nl.mean():.3f} p={(nl>=g).mean():.3f}')
# offset profile top 5
for n,s in S.items():
    a=enc(s); oi=np.array([(a[:-k]==a[k:]).mean() for k in range(1,81)])
    top=np.argsort(-oi)[:5]+1
    print(n,'top offsets',[(int(k),round(float(oi[k-1]),3)) for k in top])
# and1 offset 8: which residues match
s=S['and1']; k=8
m=[s[i] for i in range(len(s)-k) if s[i]==s[i+k]]
from collections import Counter; print('and1 off8 matched residues',Counter(m).most_common(6))
pos=[i for i in range(len(s)-k) if s[i]==s[i+k]]
print('and1 off8 match density per 100aa',np.histogram(pos,bins=range(0,601,100))[0])
s=S['and2']; k=61
m=[s[i] for i in range(len(s)-k) if s[i]==s[i+k]]; print('and2 off61 matched',Counter(m).most_common(6))
for n in ('and1','and2'):
    s=S[n]; ms=[(x.start()) for x in re.finditer(r'(?=C.{0,12}DP.{0,12}C)',s)]
    dp=[x.start() for x in re.finditer('DP',s)]; c=[i for i,ch in enumerate(s) if ch=='C']
    print(n,'Cys pos',c); print(n,'DP pos',dp, 'diffs',np.diff(dp).tolist())
    print(n,'PAPV pos',[x.start() for x in re.finditer('PAPV|DPYC',s)])
