# Independent re-implementation of the S32 exocoetid steady-state force balance (not the author's code)
import math
rw,ra,nu,g=1000.,1.225,1e-6,9.81
def cd(U,c,mode):
    if mode=="const": return 0.08
    Re=U*c/nu
    return 0.08*math.sqrt(9560/Re) if Re>9560 else 0.08
def setup(M):
    WL=285.015*M**0.4; Sw=M*g/WL; Sh=0.003*M**0.65; L=0.46*M**0.355
    Vto=math.sqrt(2*M*g/(ra*Sw*1.07)); return WL,Sw,Sh,L,Vto
def net(U,M,App,mode,phi=0.5,f=50,c=0.025,CD0=0.08):
    WL,Sw,Sh,L,Vto=setup(M); W=M*g; S=phi*Sh
    qa=.5*ra*U*U; qw=.5*rw*U*U
    CL=min(1.07,W/(qa*Sw)); Dw=qa*Sw*(CD0+CL*CL/(math.pi*.8*5))
    Db=qa*.3*(0.6*L*0.15)**2
    Fsv=2*.072*c; Fsh=2*.072*c*.3
    need=max(0,W+Fsv-qa*Sw*CL); CLz=need/(qw*S); d=phi*Sh/c; AR=2*d*d/S
    Di=qw*S*CLz**2/(math.pi*.8*AR)
    T=.5*rw*S*(2.55*(f*App)**2-cd(U,c,mode)*U*U)
    return T-Dw-Db-Di-Fsh
def ueq(M,App,mode,**k):
    lo,hi=0.5,60
    for _ in range(100):
        m=(lo+hi)/2
        lo,hi=(m,hi) if net(m,M,App,mode,**k)>0 else (lo,m)
    return lo
def power(U,M,App,phi=0.5,f=50,c=0.025):
    S=phi*0.003*M**0.65; St=f*App/U; fs=f*c/U
    return .5*rw*U**3*S*(7.78*St**2+4.89*St**2*fs)
def app_for(Ut,M,mode,**k):
    lo,hi=0.001,0.5
    for _ in range(100):
        m=(lo+hi)/2
        lo,hi=(lo,m) if ueq(M,m,mode,**k)>=Ut else (m,hi)
    return hi
for M in (0.191,0.300):
    WL,Sw,Sh,L,Vto=setup(M)
    print(f"\nM {M*1e3:.0f} g  L {L*100:.1f} cm  V_to {Vto:.2f}  0.2L={0.2*L*100:.1f} cm")
    for App in (0.020,0.026,0.031,0.2*L):
        print(f"  A_pp {App*100:.2f} cm: U_eq const {ueq(M,App,'const'):.2f}  scaled {ueq(M,App,'scaled'):.2f}  P@10 {power(10,M,App):.0f} W")
    for mode in ("const","scaled"):
        for Ut in (10.0,Vto,16.5):
            a=app_for(Ut,M,mode); print(f"  {mode:6s}: A_pp for U_eq={Ut:.1f}: {a*100:.2f} cm ({a/L:.3f} L); foil power at that U {power(Ut,M,a):.0f} W")
