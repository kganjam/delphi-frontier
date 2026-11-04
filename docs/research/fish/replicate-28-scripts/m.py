import sys
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
KD=dict(A=1.8,R=-4.5,N=-3.5,D=-3.5,C=2.5,Q=-3.5,E=-3.5,G=-0.4,H=-3.2,I=4.5,L=3.8,K=-3.9,M=1.9,F=2.8,P=-1.6,S=-0.8,T=-0.7,W=-0.9,Y=-1.3,V=4.2)
TOP=dict(W=-0.884,F=-0.697,Y=-0.510,I=-0.486,M=-0.397,L=-0.326,V=-0.121,N=0.007,C=0.02,T=0.059,A=0.06,G=0.166,R=0.180,D=0.192,H=0.303,Q=0.318,K=0.586,S=0.341,E=0.736,P=0.987)
def met(s,lab):
    n=len(s); H=sum((KD[a]+4.5)/9 for a in s)/n
    q=sum(s.count(a) for a in 'KR')-sum(s.count(a) for a in 'DE'); R=abs(q)/n
    b=(R+1.151)/2.785; top=sum(TOP[a] for a in s)/n
    print(f"{lab:22s} n={n} <H>={H:.4f} net={q:+d} <R>={R:.4f} bound={b:.4f} dist(b-H)={b-H:+.4f} TOPIDP={top:+.4f}")
k=rd('dl/Q6PFU3.fasta'); a=rd('dl/A0ACM8QEN9.fasta')
met(k,'kcnk5b full'); met(a,'and2 full'); met(a[23:],'and2 no SP(1-23)')
for st in (250,255,260,270,280,290): met(k[st:],f'kcnk5b {st+1}-end')
