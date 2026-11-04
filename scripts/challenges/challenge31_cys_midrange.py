import random,sys,statistics as st
names={'kcnk5b':'Q6PFU3','and1':'E7F5V5','and2':'A0ACM8QEN9'}
def rd(a): return ''.join(l.strip() for l in open(f'{a}.fasta') if not l.startswith('>'))
def cnt(s,lo,hi):
    p=[i for i,c in enumerate(s) if c=='C']; return sum(lo<=b-a<=hi for a,b in zip(p,p[1:]))
random.seed(2)
for n,a in names.items():
    s=rd(a); L=list(s)
    for lo,hi in [(7,8),(5,10)]:
        o=cnt(s,lo,hi); sims=[]
        for _ in range(20000): random.shuffle(L); sims.append(cnt(L,lo,hi))
        mu=st.mean(sims); sd=st.pstdev(sims); p=sum(x>=o for x in sims)/len(sims)
        print(n,f'gap{lo}-{hi}',o,f'null {mu:.2f}±{sd:.2f}',f'z={(o-mu)/sd:+.1f}','p_hi',p, 'max_null',max(sims))
