import sys,random,numpy as np
sys.argv=['x']; exec(open('tr.py').read().split('N=200')[0])
for f in ['seq/Q6PFU3.fa','seq/E7F5V5.fa','seq/A0ACM8QEN9.fa','seq/A9JRX1.fa']:
    s=rd(f); o=stat(s)[0]; ps=[]
    for seed in range(5):
        rng=random.Random(seed); null=[]
        for k in range(200):
            t=list(s); rng.shuffle(t); null.append(stat(''.join(t))[0])
        ps.append((1+sum(v>=o for v in null))/201)
    rng=random.Random(99); big=[]
    for k in range(2000):
        t=list(s); rng.shuffle(t); big.append(stat(''.join(t))[0])
    print(f,o,'p@200 seeds0-4',[round(p,3) for p in ps],'p@2000',round((1+sum(v>=o for v in big))/2001,4))
