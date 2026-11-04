import sys,re,numpy as np
rng=np.random.default_rng(171)
rd=lambda f:''.join(l.strip() for l in open(f) if not l.startswith('>'))
for x in sys.argv[2:]:
    g,a=x.split(':'); s=rd(f'{sys.argv[1]}/{a}.fa'); hd=open(f'{sys.argv[1]}/{a}.fa').readline()
    sp=re.search(r'OS=(.*?) OX',hd).group(1)
    nc=s.count('C'); h=len(re.findall(r'(?=C.{6,7}C)',s)); dp=len(re.findall(r'(?=C[DN]P.{2}D.{0,1}.C)',s))
    arr=np.array(list(s)); nl=np.array([len(re.findall(r'(?=C.{6,7}C)',''.join(rng.permutation(arr)))) for _ in range(2000)])
    print(f'{g} {a:12s} {sp[:28]:28s} L={len(s):4d} Cys={nc:2d} C-x(6,7)-C={h:2d} null_mean={nl.mean():.2f} p={(nl>=h).mean():.4f} C[DN]PxxD..C={dp}')
