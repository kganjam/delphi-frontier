import random,re
def r(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
pat=re.compile(r'(?=C.{6,7}C)')
for name,f in [('and1','dl/E7F5V5.fa'),('and2','dl/A0ACM8QEN9.fa')]:
    s=r(f); o=len(pat.findall(s)); rng=random.Random(71); l=list(s); v=[]
    for _ in range(5000): rng.shuffle(l); v.append(len(pat.findall(''.join(l))))
    print(name,'obs',o,'nC',s.count('C'),'mean %.2f max %d ge %d'%(sum(v)/5000,max(v),sum(x>=o for x in v)))
