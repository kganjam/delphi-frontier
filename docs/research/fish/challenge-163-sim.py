# Challenge 163: relaxed-assumption rerun of the S21-D-D bias model. Output is SIMULATED, not observed. numpy only, seed 7.
import numpy as np
rng=np.random.default_rng(7)
g,rho=9.81,1.2
for CL in (0.6,0.9,1.07,1.15):
    print("Vs CL",CL, round(np.sqrt(2*0.0004*g/(rho*3.2e-4*CL)),3))
dt0=2e-5; t=np.arange(0,0.25,dt0)
def alpha(tp): return (t/tp)*np.exp(1-t/tp)
def gauss(fw,t0=0.03): s=fw/2.355; return np.exp(-0.5*((t-t0)/s)**2)
def run(v,fps,sx,ntr,n=3000,V=1.0):
    x=np.cumsum(v*V)*dt0; d=1/fps; out=[]
    for _ in range(n):
        b=0
        for k in range(ntr):
            ts=np.arange(rng.uniform(0,d),0.2,d)
            xs=np.interp(ts,t,x)+rng.normal(0,sx,len(ts))
            b=max(b,np.max(np.abs(np.diff(xs)))/d)
        out.append(b)
    o=np.array(out)/V; return [round(q,3) for q in (o.mean(),np.percentile(o,5),np.percentile(o,95))]
print("mean p5 p95")
for tp in (0.0025,0.005,0.01,0.02):
    for sx in (0,1e-3):
        print("alpha tp",tp*1e3,"sx",sx*1e3,"max4",run(alpha(tp),120,sx,4),"1trial",run(alpha(tp),120,sx,1))
for fw in (0.005,0.008,0.012,0.02):
    print("gauss FWHM",fw*1e3,"max4 sx0",run(gauss(fw),120,0,4),"1trial",run(gauss(fw),120,0,1))
# noise at real speed 1.38
print("alpha10 sx1 V=1.38", run(alpha(0.01),120,1e-3,4,V=1.38))
print("alpha20 sx1 V=1.38", run(alpha(0.02),120,1e-3,4,V=1.38))
