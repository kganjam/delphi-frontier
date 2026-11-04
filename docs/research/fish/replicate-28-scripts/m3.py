exec(open('m.py').read().split('def met')[0])
k=rd('dl/Q6PFU3.fasta'); a=rd('dl/A0ACM8QEN9.fasta')
def U(s):
    n=len(s);H=sum((KD[c]+4.5)/9 for c in s)/n;R=abs(sum(c in 'KR' for c in s)-sum(c in 'DE' for c in s))/n
    return (R+1.151)/2.785-H
def T(s): return sum(TOP[c] for c in s)/len(s)
hits=[]
for i in range(len(k)):
  for j in range(i+30,len(k)+1):
    u=U(k[i:j]);t=T(k[i:j])
    if abs(u-0.166)<0.0006: hits.append(('U',i+1,j,round(u,4)))
    if abs(t-0.166)<0.0003 and j==len(k): hits.append(('T',i+1,j,round(t,4)))
print(len(hits)); print([h for h in hits if h[0]=='T']); print([h for h in hits if h[0]=='U' and h[2]==len(k)][:10])
print('max U window>=30', max((U(k[i:j]),i+1,j) for i in range(len(k)) for j in range(i+30,len(k)+1)))
