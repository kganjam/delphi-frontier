import numpy as np, math
rng=np.random.default_rng(0)
# Fig 5D digitised (I50 uA, Vm mV); grey blob of 391px at (3.7,-5.5) = two overlapping dots, dark 556px blob = two dots
wt=[(3.5,-5.0),(3.9,-6.0),(10.8,-17.7),(10.5,-27.0),(12.8,-37.0),(14.0,-41.0)]
w169=[(12.0,-12.0),(7.0,-18.0),(21.0,-27.0),(16.0,-31.0),(27.0,-46.0),(34.0,-68.0),(36.0,-81.0)]
f241=[(13.1,-12.0),(10.0,-20.0),(16.0,-24.0),(19.0,-30.0),(20.0,-30.0),(13.0,-32.1),(20.0,-36.0),(19.5,-45.0),(26.0,-55.0),(31.0,-61.0)]
mut=w169+f241
def s(g): v=np.array([p[1] for p in g]); return v
for n,g in (('wt',wt),('W169L',w169),('F241Y',f241),('mut pooled',mut)):
    v=s(g); print(f"{n:11s} n={len(v):2d} mean={v.mean():6.1f} median={np.median(v):6.1f} min={v.min():6.1f} sd={v.std(ddof=1):5.1f}")
a,b=s(wt),s(mut)
d=b.mean()-a.mean()
se=math.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))
print('mean shift mut-wt = %.1f mV, Welch t=%.2f'%(d,d/se))
bs=[rng.choice(b,len(b)).mean()-rng.choice(a,len(a)).mean() for _ in range(20000)]
print('bootstrap 95%% CI: %.1f to %.1f mV'%tuple(np.percentile(bs,[2.5,97.5])))
print('n oocytes <= -90 mV:', sum(1 for p in wt+mut if p[1]<=-90), ' most negative:', min(p[1] for p in wt+mut))
# matched current window 7-14 uA
win=lambda g:[p[1] for p in g if 7<=p[0]<=14.5]
print('matched I50 7-14.5uA: wt',win(wt),'mean %.1f'%np.mean(win(wt)),'| mut',win(mut),'mean %.1f'%np.mean(win(mut)))
# pooled regression Vm ~ I50 + genotype
X=np.array([[1,p[0],0] for p in wt]+[[1,p[0],1] for p in mut]); y=np.array([p[1] for p in wt+mut])
beta,res,_,_=np.linalg.lstsq(X,y,rcond=None)
r=y-X@beta; s2=r@r/(len(y)-3); cov=s2*np.linalg.inv(X.T@X)
print('OLS Vm = %.1f + %.2f*I50 + %.1f*mutant ; SE(mutant)=%.1f'%(beta[0],beta[1],beta[2],math.sqrt(cov[2,2])))

# Fig 5C digitised normalised currents (WT at -60 read by eye: overlapping markers)
V=[-100,-80,-60,-40,-20,0,20,40,60]
WT=[-0.106,-0.083,-0.05,0.028,0.134,0.281,0.493,0.658,1.0]
W=[-0.419,-0.212,0.069,0.368,0.686,1.027,1.381,1.763,2.178]
F=[-0.483,-0.295,-0.051,0.262,0.594,1.004,1.459,1.952,2.5]
print('\ncurrent ratio mut/WT by voltage:')
for i,v in enumerate(V):
    if v>=-20: print(f"  {v:4d} mV  W169L {W[i]/WT[i]:.1f}x  F241Y {F[i]/WT[i]:.1f}x")
sl=lambda c,i,j:(c[j]-c[i])/(V[j]-V[i])
for (i,j) in ((1,3),(2,4)):
    print(f"  slope conductance {V[i]}..{V[j]} mV: WT {sl(WT,i,j):.4f}, W169L {sl(W,i,j)/sl(WT,i,j):.1f}x, F241Y {sl(F,i,j)/sl(WT,i,j):.1f}x")
def rev(c):
    for i in range(len(V)-1):
        if c[i]<=0<c[i+1]: return V[i]+(0-c[i])*(V[i+1]-V[i])/(c[i+1]-c[i])
print('  zero-current (reversal) potential: WT %.0f, W169L %.0f, F241Y %.0f mV'%(rev(WT),rev(W),rev(F)))

# GHK, S42-D's own parameters
RT=25.4; Ki,Ko,Nai,Nao=140,4,12,145
def Vm(pk,pna): return RT*math.log((pk*Ko+pna*Nao)/(pk*Ki+pna*Nai))
print('\nGHK dV (mV) by fold-change N in pK, S42-D concentrations:')
print('p_Na/p_K  V0    x2     x3     x5     x8')
for r in (0.02,0.05,0.1,0.2,0.4):
    v0=Vm(1,r); print(f"{r:<8} {v0:6.1f} "+" ".join(f"{Vm(N,r)-v0:6.1f}" for N in (2,3,5,8)))
for N in (2,3,5,8): print(f"  analytic ceiling RT/F*ln({N}) = {RT*math.log(N):.1f} mV")
# what N is needed for 30 mV at best-case p ratio
for target in (30,40):
    best=None
    for N in np.arange(1.5,20,0.01):
        mx=max(abs(Vm(N,r)-Vm(1,r)) for r in np.logspace(-3,1,400))
        if mx>=target: best=N;break
    print(f"  min fold-change in pK for a {target} mV hyperpolarisation (any p_Na/p_K): {best:.2f}x")
