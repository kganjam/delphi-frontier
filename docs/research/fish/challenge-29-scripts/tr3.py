import sys, re, numpy as np
D=sys.argv[1]
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
S={'kcnk5b':rd(f'{D}/Q6PFU3.fa'),'and1':rd(f'{D}/E7F5V5.fa'),'and2':rd(f'{D}/A9JRX1.fa')}
for n in S:
    s=S[n]; hits=[m.start() for m in re.finditer(r'(?=C.{6,7}C)',s)]
    print(n,'C-x(6,7)-C count',len(hits))
    for h in hits: print(f'  {h+1:4d} {s[max(0,h-6):h+16]}')
# null: how many C-x(6,7)-C expected under shuffle
rng=np.random.default_rng(1)
for n in S:
    s=S[n]; obs=len(re.findall(r'(?=C.{6,7}C)',s)); a=list(s); c=[]
    for _ in range(5000):
        rng.shuffle(a); c.append(len(re.findall(r'(?=C.{6,7}C)',''.join(a))))
    c=np.array(c); print(n,'obs',obs,'shuffle mean',round(c.mean(),2),'max',c.max(),'p',(c>=obs).mean())
