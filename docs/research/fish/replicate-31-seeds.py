import random,statistics as st
def rd(f): return ''.join(l.strip() for l in open('dl/'+f+'.fasta') if not l.startswith('>'))
def pairs(s,a,d):
    idx=[i for i,c in enumerate(s) if c==a]
    return sum(1 for x in range(len(idx)) for y in range(x+1,len(idx)) if idx[y]-idx[x]<=d)
for f,a,ds in [('A0ACM8QEN9','C',(3,4,5)),('Q6PFU3','K',(3,4))]:
  s=rd(f)
  for d in ds:
    zs=[];ps=[]
    for seed in range(10):
      random.seed(seed);L=list(s);n=[]
      for _ in range(2000): random.shuffle(L); n.append(pairs(L,a,d))
      o=pairs(s,a,d);m=st.mean(n);sd=st.pstdev(n);zs.append((o-m)/sd)
      ps.append((1+sum(x>=o for x in n))/2001 if a=='K' else (1+sum(x<=o for x in n))/2001)
    print(f,a,d,'z range %.2f..%.2f'%(min(zs),max(zs)),'p range %.4f..%.4f'%(min(ps),max(ps)))
s=rd('Q6PFU3');idx=[i+1 for i,c in enumerate(s) if c=='C'];print('kcnk5b C pos',idx)
s=rd('A0ACM8QEN9');idx=[i+1 for i,c in enumerate(s) if c=='C'];print('and2 C pos',idx,'min gap',min(b-a for a,b in zip(idx,idx[1:])))
s=rd('E7F5V5');idx=[i+1 for i,c in enumerate(s) if c=='C'];print('and1 C pos',idx,'min gap',min(b-a for a,b in zip(idx,idx[1:])))
