import math, itertools
rw=1000.; ra=rw/816; g=9.81; nu=1.0e-6
c=0.006; Slobe=18.9e-6; hlobe=4.5e-3; Sw=192e-6; CLmax=1.07; k=1/(math.pi*0.8*5)
Af=24e-6; Sfin=37.8e-6; c6=2.55; CDf=0.08; f=52.; sig=0.072
def G_of(Cdb, U=1.38): return U*U*(CDf + Cdb*Af/Sfin)
def CD(U,mode):
    Re=U*c/nu
    if mode=='const' or 4780<=Re<=9560: return CDf
    return CDf*math.sqrt((9560 if Re>9560 else 4780)/Re)
def forces(U,p):
    m,G,phi,CD0,mode,cth,dcth,dmode=p
    W=m*g; S=phi*Slobe
    d = phi*hlobe if dmode=='prop' else hlobe
    AR=2*d*d/S
    qa=0.5*ra*U*U; qw=0.5*rw*U*U
    CL=min(CLmax, W/(qa*Sw)); L=qa*Sw*CL
    Dw=qa*Sw*(CD0+k*CL*CL)
    Db=qa*0.3*Af
    Fz=max(0.,W-L+2*sig*c*cth)
    CLz=Fz/(qw*S)
    Di=qw*S*CLz**2/(math.pi*0.8*AR)
    T=0.5*rw*S*(G-CD(U,mode)*U*U)
    Fs=2*sig*c*dcth
    return T-Dw-Db-Di-Fs, CLz, (T,Dw,Db,Di,Fs)
def run(p,U0=1.38,dt=2e-5,tmax=5.):
    m=p[0]; Vto=math.sqrt(2*m*g/(ra*Sw*CLmax))
    U=U0;x=0;t=0; Ueq=None
    a=lambda u: forces(u,p)[0]/m
    while t<tmax:
        if forces(U,p)[1]>1: return ('CLz>1',U,t,x,Vto)
        if U>=Vto: return ('reached',U,t,x,Vto)
        k1=a(U);k2=a(U+.5*dt*k1);k3=a(U+.5*dt*k2);k4=a(U+dt*k3)
        x+=U*dt; U+=dt*(k1+2*k2+2*k3+k4)/6; t+=dt
        if abs(k1)<1e-3*g: return ('equilib',U,t,x,Vto)
    return ('tmax',U,t,x,Vto)
def ceiling(p):
    # root of net force between 1.38 and Vto
    m=p[0]; Vto=math.sqrt(2*m*g/(ra*Sw*CLmax)); lo,hi=1.38,Vto
    if forces(hi,p)[0]>0: return None
    for _ in range(80):
        mid=(lo+hi)/2
        if forces(mid,p)[0]>0: lo=mid
        else: hi=mid
    return lo
def t99(p,Uc):
    m=p[0];U=1.38;t=0;x=0;dt=2e-5
    while U<0.99*Uc:
        U+=dt*forces(U,p)[0]/m; x+=U*dt; t+=dt
    return t,x
if __name__=='__main__':
    print("G(Cdb=0.1,0.2,0.3)=",[round(G_of(x),3) for x in (0.1,0.2,0.3)])
    for m,Cdb,phi,CD0,mode,dmode in itertools.product((0.25e-3,0.40e-3),(0.3,0.1),(1.0,0.5,0.25),(0.08,0.20),('scaled','const'),('prop',)):
        p=(m,G_of(Cdb),phi,CD0,mode,0.,0.,dmode)
        r=run(p); Uc=ceiling(p)
        s=f"m={m*1e3:.2f}g Cdb={Cdb} phi={phi} CD0={CD0} {mode:6s} -> {r[0]:8s} U={r[1]:.3f} t={r[2]:.3f}s x={r[3]:.2f}m Vto={r[4]:.2f} ceil={Uc and round(Uc,3)}"
        if Uc and r[0]!='CLz>1':
            tt,xx=t99(p,Uc); s+=f" | 99%: t={tt:.3f}s strokes={tt*f:.1f} x={xx:.2f}m frac={Uc/r[4]:.3f}"
        print(s)
