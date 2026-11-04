# S21-D-D: Monte Carlo of frame-differenced peak-speed bias. Output is SIMULATED, not observed.
# Run: python3 S21-D-deepen-sim.py  (numpy only; seed fixed)
# Simulation (not observation): bias of frame-differenced peak speed.
import numpy as np
rng=np.random.default_rng(1)
def profile(tp):
    dt=1e-5; t=np.arange(0,0.2,dt); v=(t/tp)*np.exp(1-t/tp)  # alpha pulse, peak=1 m/s at tp
    x=np.cumsum(v)*dt; return t,x
def measured(fps,tp,V,sx,ntrial,nsim=4000):
    t,x=profile(tp); x=x*V; dt=1/fps; out=[]
    for _ in range(nsim):
        best=0
        for k in range(ntrial):
            ph=rng.uniform(0,dt); ts=np.arange(ph,0.15,dt)
            xs=np.interp(ts,t,x)+rng.normal(0,sx,len(ts))
            best=max(best,np.max(np.abs(np.diff(xs)))/dt)
        out.append(best)
    out=np.array(out); return out.mean()/V, np.percentile(out,95)/V
print("fps tp_ms V sx_mm ntrial  mean_meas/true  p95/true")
for fps,ntr in [(120,4),(1000,1)]:
  for tp in [0.005,0.010,0.020]:
    for sx in [0,0.25e-3,0.5e-3,1.0e-3] if fps==120 else [0,0.03e-3,0.06e-3,0.12e-3]:
      m,p=measured(fps,tp,1.0,sx,ntr,nsim=1500)
      print(fps,int(tp*1e3),1.0,sx*1e3,ntr,round(m,3),round(p,3))
