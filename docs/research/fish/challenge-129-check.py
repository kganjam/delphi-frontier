import numpy as np, sys
rng=np.random.default_rng(7)
d=np.loadtxt(sys.argv[1]); tm,vm=d[:,0]*1e-3,d[:,1]
dt=1e-5; tg=np.arange(0,tm.max(),dt); vg=np.interp(tg,tm,vm)
k=int(0.003/dt); vs=np.convolve(vg,np.ones(k)/k,mode="same"); vs[:k//2]=vg[:k//2]; vs[-k//2:]=vg[-k//2:]
pk=vs.max(); print("pk",pk, "t>=0.9pk ms",(vs>=0.9*pk).sum()*dt*1e3)
def run(scale,sx,n=2000):
    x=np.cumsum(vs*scale)*dt; out=[]
    for i in range(n):
        b=0
        for _ in range(4):
            t0=rng.uniform(0,1/120)-1/120; ts=np.arange(t0,tg.max(),1/120)
            xs=np.interp(ts,tg,x,left=0.0)+rng.normal(0,sx,len(ts))
            b=max(b,np.max(np.abs(np.diff(xs)))*120)
        out.append(b/(pk*scale))
    o=np.array(out); return o.mean(),np.percentile(o,5),np.percentile(o,95)
for scale_to in [pk, 1.38/0.975]:
    for sx in [0,0.5e-3,1e-3]:
        print(f"peak {scale_to:.3f} m/s sx {sx*1e3} mm ->", ["%.3f"%v for v in run(scale_to/pk,sx)])
# alpha pulse sensitivity, independent
def alpha(tp,sx=0,n=1500):
    t=np.arange(0,0.25,1e-6 if tp<2e-3 else 1e-5); v=(t/tp)*np.exp(1-t/tp); x=np.cumsum(v)*(t[1]-t[0]); out=[]
    for i in range(n):
        b=0
        for _ in range(4):
            t0=rng.uniform(0,1/120)-1/120; ts=np.arange(t0,min(0.24,8*tp+0.05),1/120)
            b=max(b,np.max(np.diff(np.interp(ts,t,x,left=0.0)))*120)
        out.append(b)
    return np.mean(out)
for tp in [5e-3,2.5e-3,1e-3]:
    b=alpha(tp,n=600); print(f"tp {tp*1e3} b {b:.3f} M@4.37 {4.37*b/1.38:.2f} M@4.22 {4.22*b/1.38:.2f}")
print("arith", 4.22/(1.38/0.964), 4.37/(1.38/1.657), 1.38/4.37, 0.856/0.0256)
