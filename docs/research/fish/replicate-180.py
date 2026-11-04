from math import pi,sqrt
def M(m=0.4e-3,V=3.0,CL=0.78,AR=9.0,hw=2.5e-3,n=3.0,rho=1.2,g=9.81):
    W=m*g; S=2*W/(rho*V**2*CL); b=sqrt(AR*S); s=b/2-hw; y=4/(3*pi)*s
    return n*(W/2)*y, dict(W=W,S=S,b=b,s=s,y=y)
def d(Mv,sig): return (32*Mv/(pi*sig))**(1/3)
M0,p=M(); print("M_worst",M0,p)
for sig in (25e6,43.4e6,49.4e6,62.6e6,66.8e6,107.5e6,114e6): print(sig/1e6, round(d(M0,sig)*1e3,4))
base=d(M0,62.6e6)
for k,v in dict(m=0.4e-3,V=3.0,CL=0.78,AR=9.0,hw=2.5e-3,n=3.0).items():
    for f in (0.5,2):
        Mx,_=M(**{k:v*f}); print(k,f,round(d(Mx,62.6e6)/base,3))
for f in (0.5,2): print("sig",f,round(d(M0,62.6e6*f)/base,3))
