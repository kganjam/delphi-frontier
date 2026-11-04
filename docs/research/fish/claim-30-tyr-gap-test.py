"""Claim 30 reproduction: fraction of consecutive Tyr-Tyr gaps <= k residues vs. full-sequence shuffles.
Usage: python3 -I claim-30-tyr-gap-test.py <uniprot.fasta> <k[,k...]>   (claim used k=4, 2000 shuffles, seed 1)
This is a reconstruction that reproduces the claim's numbers, not the original pipeline."""
import sys,random,statistics as st
def readfa(p):
    d={};k=None
    for l in open(p):
        l=l.strip()
        if l.startswith('>'): k=l[1:];d[k]=''
        elif k: d[k]+=l
    return d
def gaps(s):
    pos=[i for i,c in enumerate(s) if c=='Y']
    return [b-a for a,b in zip(pos,pos[1:])]
def frac_close(s,k):
    g=gaps(s); return sum(x<=k for x in g)/len(g) if g else float('nan')
def stat(s,k): return frac_close(s,k)
def test(s,k,n=2000,seed=1):
    r=random.Random(seed);o=stat(s,k);L=list(s);null=[]
    for _ in range(n):
        r.shuffle(L);null.append(stat(''.join(L),k))
    m=st.mean(null);sd=st.pstdev(null)
    p=(1+sum(x>=o for x in null))/(n+1)
    return o,m,(o-m)/sd if sd else float('nan'),p
if __name__=='__main__':
    d=readfa(sys.argv[1]);ks=[int(x) for x in sys.argv[2].split(',')]
    for h,s in d.items():
        out=[h.split('|')[1],h.split('OS=')[1].split(' OX')[0][:22],h.split('GN=')[1].split()[0] if 'GN=' in h else '?',len(s),s.count('Y'),round(s.count('Y')/len(s),3)]
        for k in ks:
            o,m,z,p=test(s,k); out+= [f'k{k}:{o:.3f}/{m:.3f} z={z:.2f} p={p:.3f}']
        print(*out,sep='\t')
