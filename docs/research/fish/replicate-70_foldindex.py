import sys
KD=dict(A=1.8,R=-4.5,N=-3.5,D=-3.5,C=2.5,Q=-3.5,E=-3.5,G=-0.4,H=-3.2,I=4.5,L=3.8,K=-3.9,M=1.9,F=2.8,P=-1.6,S=-0.8,T=-0.7,W=-0.9,Y=-1.3,V=4.2)
def fi(s):
    h=sum((KD[c]+4.5)/9 for c in s)/len(s)
    q=(s.count('K')+s.count('R')-s.count('D')-s.count('E'))/len(s)
    return 2.785*h-abs(q)-1.151,h,q
def rd(f): return ''.join(open(f).read().split('\n')[1:])
for name,f,sp in [('and1',sys.argv[1]+'/E7F5V5.fa',26),('and2',sys.argv[1]+'/A9JRX1.fa',23),('kcnk5b',sys.argv[1]+'/Q6PFU3.fa',0)]:
    s=rd(f)
    for lab,x in [('full',s),('mature',s[sp:])]:
        v,h,q=fi(x); W=51
        ws=[fi(x[i:i+W])[0] for i in range(len(x)-W+1)]
        neg=sum(w<0 for w in ws)
        # per-residue: residue disordered if centred window negative (ends extended)
        print(f"{name:7}{lab:7} N={len(x):4d} <H>={h:.4f} <R>={q:+.4f} FI={v:+.4f}  win51 neg={neg}/{len(ws)}={neg/len(ws)*100:.1f}%  minW={min(ws):+.3f} maxW={max(ws):+.3f}")
