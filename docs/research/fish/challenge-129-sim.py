# Challenge-129: same models as S21-D-D-deepen-sim.py, but velocity by CENTRAL difference
# Run: python3 -I challenge-129-sim.py S21-D-D-fig2b-trace.txt  (trace file from branch claude/deepen-s21-d-sensitive-input-no42sx)
# v_n = (x_{n+1}-x_{n-1})/(2 dt) (Tracker's default 'finite difference' estimator). SIMULATED.
import sys, numpy as np
rng=np.random.default_rng(7)
def alpha_x(tp,dt=1e-5,T=0.25):
    t=np.arange(0,T,dt); v=(t/tp)*np.exp(1-t/tp); return t,np.cumsum(v)*dt
def mot(t,x,fps,sx,ntr,nsim,tmax,cd):
    dt=1/fps; out=np.empty(nsim)
    for i in range(nsim):
        b=0
        for _ in range(ntr):
            ts=np.arange(rng.uniform(0,dt)-2*dt,tmax,dt)
            xs=np.interp(ts,t,x,left=0.0)+rng.normal(0,sx,len(ts))
            v=(xs[2:]-xs[:-2])/(2*dt) if cd else np.diff(xs)/dt
            b=max(b,np.abs(v).max())
        out[i]=b
    return out
print("alpha pulse, 120 fps max-of-4, sx=0: two-point vs central")
for tp in [0.001,0.0015,0.002,0.0025,0.005,0.010,0.0256]:
    t,x=alpha_x(tp,dt=1e-6 if tp<0.003 else 1e-5, T=0.06 if tp<0.003 else 0.25)
    tm=min(t.max(),8*tp+0.05)
    a=mot(t,x,120,0,4,400,tm,False).mean(); c=mot(t,x,120,0,4,400,tm,True).mean()
    print(f" tp={tp*1e3:5.2f} ms  2pt={a:.3f} M437={4.37*a/1.38:.2f}  central={c:.3f} M437={4.37*c/1.38:.2f}")
d=np.loadtxt(sys.argv[1]); tm,vm=d[:,0]*1e-3,d[:,1]
tg=np.arange(0,tm.max(),1e-5); vg=np.interp(tg,tm,vm); k=300
vs=np.convolve(vg,np.ones(k)/k,mode="same"); vs[:k//2]=vg[:k//2]; vs[-k//2:]=vg[-k//2:]
x=np.cumsum(vs)*1e-5; pk=vs.max()
print("trace span ms:",tm.min()*1e3,tm.max()*1e3, " v at end",vm[-1])
for cd in [False,True]:
    r=[]
    for p in np.linspace(0,1/120,400,endpoint=False):
        ts=np.arange(p-2/120,tg.max(),1/120); xx=np.interp(ts,tg,x,left=0.0)
        v=(xx[2:]-xx[:-2])*60 if cd else np.diff(xx)*120
        r.append(v.max()/pk)
    r=np.array(r); print(f"measured shape single trial noise-free {'central' if cd else '2pt'}: min={r.min():.3f} mean={r.mean():.3f}")
    for sx in [0,0.5e-3,1e-3,2e-3]:
        q=mot(tg,x,120,sx,4,1500,tg.max(),cd)/pk
        print(f"   sx={sx*1e3:.1f}mm max4 mean={q.mean():.3f} p5={np.percentile(q,5):.3f} p95={np.percentile(q,95):.3f}")
# truncation: trace ends at ~37ms while still 0.54 m/s; extend with linear decay to 0 at 80 ms vs hold
