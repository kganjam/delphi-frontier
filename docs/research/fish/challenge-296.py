# challenge-296 reproduction scripts (computation only). Run each block separately; numpy only.

# ===== ch.py =====
import numpy as np, math
# independent: rightmost root of s^2 + c s - L2 + (kp + kd s) e^{-s tau}=0 via Chebyshev pseudospectral (Breda) discretisation
def cheb(N):
    x=np.cos(np.pi*np.arange(N+1)/N); c=np.hstack([2,np.ones(N-1),2])*(-1)**np.arange(N+1)
    X=np.tile(x,(N+1,1)).T; dX=X-X.T; D=np.outer(c,1/c)/(dX+np.eye(N+1)); D-=np.diag(D.sum(1)); return D,x
N=30; D0,x0=cheb(N)
def rightmost(kp,kd,tau,L2=1.0,c=0.0):
    # state y=(theta,omega); y'(t)=A0 y(t)+A1 y(t-tau)
    A0=np.array([[0,1],[L2,-c]]); A1=np.array([[0,0],[-kp,-kd]])
    D=D0*(-2/tau)  # map x in[-1,1] to theta in[-tau,0]: theta=tau*(x-1)/2 -> d/dtheta = 2/tau d/dx ; nodes x0[0]=1 -> theta=0
    D=D0*(2/tau)
    n=N+1; M=np.zeros((2*n,2*n))
    for i in range(1,n):
        for j in range(n): M[2*i:2*i+2,2*j:2*j+2]=D[i,j]*np.eye(2)
    M[0:2,0:2]=A0; M[0:2,2*N:2*N+2]=A1   # x0[N]=-1 -> theta=-tau
    return np.linalg.eigvals(M).real.max()
def stable(kp,kd,tau,**k): return rightmost(kp,kd,tau,**k)< -1e-6
# 1) hard limit: is there ANY stable (kp,kd) at lam*tau = 1.35, 1.40, 1.43, 1.48?
def any_stable(tau,**k):
    best=None
    for kp in np.linspace(1.0,3,60):
        for kd in np.linspace(0.05,3,60):
            r=rightmost(kp,kd,tau,**k)
            if best is None or r<best[0]: best=(r,kp,kd)
    return best
for t in (1.30,1.40,1.43,1.48): print("lam*tau",t,"best rightmost root",any_stable(t))

# ===== ch3.py =====
exec(open('ch.py').read().split('# 1)')[0])
def gm(t,c=0.0,L2=1.0):
    best=(1.0,None)
    for r in np.linspace(0.2,3.0,57):          # kd = r*kp (controller shape)
        Ks=np.exp(np.linspace(np.log(0.8),np.log(8),300))
        st=np.array([stable(K,r*K,t,c=c,L2=L2) for K in Ks])
        if st.any():
            # largest contiguous stable run
            idx=np.where(st)[0]; runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
            for run in runs:
                g=Ks[run[-1]]/Ks[run[0]]
                if g>best[0]: best=(g,r)
    return best
for t in (0.3,0.5,0.61,0.84,1.0,1.26): print("lam*tau",t,"true loop-gain margin (Kmax/Kmin, best kd/kp)",gm(t))

# ===== ch4.py =====
import math
rho=1.2; m,L=0.4e-3,0.04; Iy=m*L**2/12; St,lt,at=1e-4,0.02,1.6
for V in (1,2,3):
    k=0.5*rho*V**2*St*lt*at/Iy; lam=math.sqrt(k)
    c=0.5*rho*V*St*lt**2*at/Iy   # tail pitch-damping, per unit I (s^-1)
    p=(-c+math.sqrt(c*c+4*k))/2
    print(V,"Iy",Iy,"lam",round(lam,3),"tail damping c",round(c,3),"unstable root with damping",round(p,3),
          "hard limit no-damp ms",round(1000*math.sqrt(2)/lam,1),"V_hard@70ms",round(math.sqrt(2)/0.070/(lam/V),2),"V_rob@70",round(0.609/0.070/(lam/V),2))
# static-margin relaxation: lam scales sqrt(|SM_unstable|/SM_stable)
for f in (1,0.5,0.25,0.1):
    lam=12*math.sqrt(f); print("|SM| fraction",f,"lam@2m/s",round(lam,2),"hard ms",round(1000*math.sqrt(2)/lam),"robust ms",round(1000*0.609/lam))

# ===== pda.py =====
import numpy as np, itertools
w=np.concatenate([np.linspace(400,2,40000),np.linspace(2,-2,40000),np.linspace(-2,-400,40000)])
def nrhp(kp,kd,ka,t):
    E=np.exp(-1j*w*t)
    f=-(w**2)*(1+ka*E)+(kp+1j*kd*w)*E-1.0
    d=np.unwrap(np.angle(f)); return 1+(d[-1]-d[0])/(2*np.pi)
def anystable(t,useka=True):
    kas=np.linspace(-0.9,0.9,19) if useka else [0.0]
    for ka in kas:
        for kp in np.linspace(1.01,4,40):
            for kd in np.linspace(0.05,4,40):
                if round(nrhp(kp,kd,ka,t))==0: return (kp,kd,ka)
    return None
for t in (1.0,1.3,1.6,1.9,2.2,2.4,2.5):
    print("lam*tau",t,"PD:",anystable(t,False) if t<1.5 else "-","PDA:",anystable(t))

# ===== pda2.py =====
exec(open('pda.py').read().split('def anystable')[0])
def find(t):
    for ka in np.arange(0.3,0.96,0.05):
        for kp in np.linspace(1.002,1.3,25):
            for kd in np.linspace(t*0.9,t*1.2,25):
                if round(nrhp(kp,kd,ka,t))==0: return (round(kp,3),round(kd,3),round(ka,2))
for t in (1.48,1.75): print("lam*tau",t,find(t))
