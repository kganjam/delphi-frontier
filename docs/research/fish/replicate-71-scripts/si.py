import random,re,sys
def r(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
def mx(s,K=80):
    L=len(s); return max(sum(s[i]==s[i+k] for i in range(L-k))/(L-k) for k in range(1,K+1))
for name,f in [('and1','dl/E7F5V5.fa'),('and2','dl/A0ACM8QEN9.fa')]:
    s=r(f); o=mx(s); print(name,len(s),'obs %.4f'%o)
    for seed,N in [(1,200),(2,200),(3,200),(4,2000)]:
        rng=random.Random(seed); l=list(s); v=[]
        for _ in range(N): rng.shuffle(l); v.append(mx(''.join(l)))
        ge=sum(x>=o for x in v); lt=sum(x<o for x in v)
        print(f'  seed{seed} N={N} mean={sum(v)/N:.4f} max={max(v):.4f} pct_below={lt/N:.3f} p_ge={(ge)/N:.3f} p_ge+1={(ge+1)/(N+1):.3f}')
    m=[(x.start(),x.group()) for x in re.finditer(r'(?=(C.{6,7}C))',s)]
    print('  C-x(6,7)-C:',len(m),[(a+1,g) for a,g in [(x.start(),x.group(1)) for x in re.finditer(r'(?=(C.{6,7}C))',s)]])
