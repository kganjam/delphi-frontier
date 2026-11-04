# Large-deflection (elastica) cantilever, uniform dead vertical load, a = qL^3/EI, arc length s in [0,1].
# EI theta' (s) = M(s) = q * int_s^1 (x(t)-x(s)) dt  -> use ODE form: theta'' = -a (1-s) cos(theta), theta(0)=0, theta'(1)=0.
import math
def integ(a,k0,n=4000):
    h=1.0/n; th,k,y=0.0,k0,0.0; s=0.0
    f=lambda s,th,k:(k,-a*(1-s)*math.cos(th),math.sin(th))
    for i in range(n):
        d1=f(s,th,k); d2=f(s+h/2,th+h/2*d1[0],k+h/2*d1[1]); d3=f(s+h/2,th+h/2*d2[0],k+h/2*d2[1]); d4=f(s+h,th+h*d3[0],k+h*d3[1])
        th+=h/6*(d1[0]+2*d2[0]+2*d3[0]+d4[0]); k+=h/6*(d1[1]+2*d2[1]+2*d3[1]+d4[1]); y+=h/6*(d1[2]+2*d2[2]+2*d3[2]+d4[2]); s+=h
    return k,y
def bis(fn,lo,hi,it=80):
    flo=fn(lo)
    for _ in range(it):
        m=(lo+hi)/2; fm=fn(m)
        if (fm>0)==(flo>0): lo,flo=m,fm
        else: hi=m
    return (lo+hi)/2
def tip(a):
    k0=bis(lambda k:integ(a,k)[0],0.0,a/2+1e-9)
    return integ(a,k0)[1]
# check linear limit: a small -> tip = a/8
print("small-a check", tip(0.008)/0.001)
res={}
for t in (0.05,0.10,0.20,0.50):
    a=bis(lambda a:tip(a)-t,1e-6,20.0,60); res[t]=8*t/a
    print(f"tol={t:.2f} a_lin={8*t:.3f} a_elastica={a:.3f} EI_req ratio elastica/linear={8*t/a:.3f}")
W=0.4e-3*9.81; L=0.02
for t in (0.20,0.50):
    EIl=(W/2)*L**2/(8*t); S=EIl*res[t]/4e-9
    print(f"L=2cm tol={t}: S_lin={EIl/4e-9:.1f} S_elastica={S:.1f}; margin E0=0.48: {S*0.048:.2f}, 0.57: {S*0.057:.2f}; 0.35: {S*0.035:.2f}; flip E0*={10e9/S/1e6:.0f} MPa")
