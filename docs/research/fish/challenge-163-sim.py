# Challenge 163: relaxed-assumption rerun. Output is SIMULATED.
# Run: python3 -I challenge-163-sim.py (numpy). Relaxes S21-D-D sim: adds central differencing, t_p 3 ms, sigma 2 mm, sharp two-stage profile.
import numpy as np
rng=np.random.default_rng(163)
dt0=1e-5; T=np.arange(0,0.25,dt0)
def run(tp,sx,mode,ntrial=4,fps=120,nsim=1500,shape='alpha'):
    if shape=='alpha': v=(T/tp)*np.exp(1-T/tp)
    else: # two-stage: stage-1 weak pulse then stage-2 pulse peaking at 2*tp, gaussian width tp/2 (sharp)
        v=0.3*np.exp(-((T-tp)/(tp/2))**2)+np.exp(-((T-2.5*tp)/(tp/2))**2)
    x=np.cumsum(v)*dt0; dt=1/fps; out=[]
    for _ in range(nsim):
        b=0
        for k in range(ntrial):
            ts=np.arange(rng.uniform(0,dt),0.2,dt); xs=np.interp(ts,T,x)+rng.normal(0,sx,len(ts))
            vv=np.abs(np.diff(xs))/dt if mode=='fwd' else np.abs(xs[2:]-xs[:-2])/(2*dt)
            b=max(b,vv.max())
        out.append(b)
    o=np.array(out); return round(o.mean(),3),round(np.percentile(o,5),3),round(np.percentile(o,95),3)
for shape in ['alpha','sharp']:
  for mode in ['fwd','central']:
    for tp in [0.003,0.005,0.010,0.020]:
      for sx in [0,0.5e-3,1e-3,2e-3]:
        print(shape,mode,int(tp*1e3),'ms',sx*1e3,'mm',run(tp,sx,mode,shape=shape))
