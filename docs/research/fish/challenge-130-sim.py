# Challenge-130 independent Monte Carlo. SIMULATED output, not observation.
import numpy as np
rng=np.random.default_rng(130)
def prof(tp):
    dt=1e-5;t=np.arange(0,0.25,dt);v=(t/tp)*np.exp(1-t/tp);return t,np.cumsum(v)*dt
def meas(fps,tp,sx,ntr,method,nsim=1500):
    t,x=prof(tp);dt=1/fps;out=np.empty(nsim)
    for s in range(nsim):
        b=0
        for k in range(ntr):
            ts=np.arange(rng.uniform(0,dt),0.2,dt)
            xs=np.interp(ts,t,x)+rng.normal(0,sx,len(ts))
            v=np.diff(xs)/dt if method=='fwd' else (xs[2:]-xs[:-2])/(2*dt)
            b=max(b,np.max(np.abs(v)))
        out[s]=b
    return out.mean(),np.percentile(out,95),np.percentile(out,98)
print("method tp_ms sx_mm mean p95 p98")
for m in ['fwd','central']:
  for tp in [0.003,0.005,0.010,0.020]:
    for sx in [0,0.5e-3,1e-3,1.5e-3]:
      r=meas(120,tp,sx,4,m);print(m,tp*1e3,sx*1e3,*[round(z,3) for z in r])
# rise time needed for a 2x under-read (noise-free, max of 4)
for m in ['fwd','central']:
  for tp in [0.001,0.0015,0.002,0.0025]:
    print('2x-check',m,tp*1e3,round(meas(120,tp,0,4,m,400)[0],3))
# V_s arithmetic
g=9.81;m_=0.4e-3;rho=1.2;S=3.2e-4
for CL in [0.6,0.9,1.07,1.15]: print('Vs',CL,round((2*m_*g/(rho*S*CL))**.5,3))
