# challenge-130: independent re-check of S21-D-D arithmetic and bias simulation. Output is SIMULATED/CALCULATED, not observed.
# Uses the closed-form position of the alpha pulse (not the author's cumulative-sum integration); 20000 replicates, seed 7.
import numpy as np
g=9.81;rho=1.2;m=0.4e-3;S=3.2e-4
for cl in [0.6,0.9,1.07,1.15]: print("Vs",cl,round(np.sqrt(2*m*g/(rho*S*cl)),3))
for U in [1.38,1.58,0.99,1.16,0.84]: print("M",U,[round(v/U,2) for v in (4.22,4.37,4.77,5.84)])
print("U band",1.38/1.40,1.38/0.875, "flip factor",4.37/1.38,(4.37/1.38)**2)
# independent sim: analytic positions of alpha pulse x(t)=V tp e (1 - e^{-s}(1+s)), s=t/tp
rng=np.random.default_rng(7)
def xpos(t,tp): s=t/tp; return tp*np.e*(1-np.exp(-s)*(1+s))
def run(fps,tp,sx,ntr,n=20000):
    dt=1/fps; k=np.arange(int(0.15*fps))
    ph=rng.uniform(0,dt,(n,ntr,1)); ts=ph+k*dt
    xs=xpos(ts,tp)+rng.normal(0,sx,ts.shape)
    v=np.abs(np.diff(xs,axis=2)).max(axis=2)/dt
    best=v.max(axis=1); return best.mean(),np.percentile(best,[5,50,95])
for tp in [0.0025,0.005,0.010,0.020]:
  for sx in [0,0.5e-3,1e-3,2e-3]:
    mu,p=run(120,tp,sx,4); print(120,tp*1e3,sx*1e3,round(mu,3),np.round(p,3))
# single-trial min reading at tp=5ms
mu,p=run(120,0.005,0,1); print("1trial tp5",round(mu,3),np.round(p,3))
