import random,re,sys,statistics as st
from math import comb
d=sys.argv[1]
names={'kcnk5b':'Q6PFU3','and1':'E7F5V5','and2':'A0ACM8QEN9'}
def rd(a): return ''.join(l.strip() for l in open(f'{d}/{a}.fasta') if not l.startswith('>'))
def gaps(s,r):
    p=[i for i,c in enumerate(s) if c==r]; return p,[b-a for a,b in zip(p,p[1:])]
def frac(s,r,k=4):
    p,g=gaps(s,r); return sum(x<=k for x in g)/len(g) if g else 0
def anyclose(s,r,k):
    p,g=gaps(s,r); return sum(x<=k for x in g)
random.seed(1)
for n,a in names.items():
    s=rd(a); p,g=gaps(s,'C')
    print(n,len(s),'nC',len(p),'gaps',g)
    print('  min gap',min(g),'gaps<=4',sum(x<=4 for x in g),'gaps<=10',sum(x<=10 for x in g))
    print('  CxxC',len(re.findall('(?=C..C)',s)),'CxC',len(re.findall('(?=C.C)',s)),'CC',s.count('CC'))
    print('  C x6-9 C motifs',[(m.start(),s[m.start():m.start()+12]) for m in re.finditer('(?=C.{6,9}C)',s)][:20])
    for r in 'CYK':
        obs=frac(s,r); L=list(s); sims=[]
        for _ in range(20000):
            random.shuffle(L); sims.append(frac(L,r))
        mu=st.mean(sims); sd=st.pstdev(sims)
        lo=sum(x<=obs for x in sims)/len(sims); hi=sum(x>=obs for x in sims)/len(sims)
        print(f'  {r} obs={obs:.3f} null={mu:.3f} sd={sd:.3f} z={(obs-mu)/sd:+.2f} p_hi={hi:.4f} p_lo={lo:.4f}')
    # analytic: prob no two of m Cys within 4 (gap>=5) on line length N : C(N-4(m-1), m)/C(N,m)
    m=len(p);N=len(s)
    print('  analytic P(no Cys gap<=4)=',comb(N-4*(m-1),m)/comb(N,m))
