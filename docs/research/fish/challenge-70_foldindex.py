import sys, random, re
KD=dict(A=1.8,R=-4.5,N=-3.5,D=-3.5,C=2.5,Q=-3.5,E=-3.5,G=-0.4,H=-3.2,I=4.5,L=3.8,K=-3.9,M=1.9,F=2.8,P=-1.6,S=-0.8,T=-0.7,W=-0.9,Y=-1.3,V=4.2)
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def fi(s):
    n=len(s); H=sum((KD[c]+4.5)/9 for c in s)/n
    R=(sum(c in 'KR' for c in s)-sum(c in 'DE' for c in s))/n
    return 2.785*H-abs(R)-1.151, H, R
seqs={k:rd(f'dl/{k}.fasta') for k in ['A9JRX1','E7F5V5','Q6PFU3','A0ACM8QEN9']}
print('dup identical:', seqs['A9JRX1']==seqs['A0ACM8QEN9'])
a2=seqs['A9JRX1']; a1=seqs['E7F5V5']
for name,s in [('and2 pre',a2),('and2 mat24',a2[23:]),('and1 pre',a1),('and1 mat27',a1[26:]),('kcnk5b',seqs['Q6PFU3'])]:
    print(name,len(s),['%.4f'%x for x in fi(s)])
print('furin-like motifs and2:',[(m.start()+1,m.group()) for m in re.finditer('R.[KR]R',a2)])
for cut in [23,49,50,51]:
    print('and2 from',cut+1, '%.4f'%fi(a2[cut:])[0])
# block bootstrap, several block lengths, non-circular & circular
def boot(s,L,B=4000,seed=1,circ=True):
    r=random.Random(seed); n=len(s); k=-(-n//L); out=[]
    ss=s+s if circ else s
    for _ in range(B):
        t=''.join(ss[(st:=r.randrange(n if circ else n-L+1)):st+L] for _ in range(k))[:n]
        out.append(fi(t)[0])
    out.sort(); return out[int(.025*B)], out[int(.975*B)-1], sum(x<0 for x in out)/B
m=a2[23:]
for L in [1,10,25,51,75,100]:
    for c in [True,False]:
        lo,hi,p=boot(m,L,circ=c); print('L',L,'circ',c,'CI [%.3f,%.3f] Pneg %.3f'%(lo,hi,p))
# windowed profile mature and2 w=51
w=51; prof=[fi(m[i:i+w])[0] for i in range(len(m)-w+1)]
print('frac neg windows', sum(x<0 for x in prof)/len(prof))
# composition
from collections import Counter
c=Counter(m); print(sorted(((v/len(m),k) for k,v in c.items()),reverse=True)[:8])
