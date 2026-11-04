import math
RW,RA,NU,g,SIG=1000.,1.225,1e-6,9.81,0.072
C6,CD0F,RLO,RHI=2.55,0.08,4780.,9560.
def cd(U,c,mode):
    if mode=="const": return CD0F
    Re=U*c/NU
    return CD0F*math.sqrt(RHI/Re) if Re>RHI else (CD0F*math.sqrt(RLO/Re) if Re<RLO else CD0F)
def setup(M=0.191,phi=0.5,c=0.025,CLmax=1.07,CD0=0.08):
    WL=285.015*M**0.4; Sw=M*g/WL; Sh=0.003*M**0.65
    return dict(M=M,Sw=Sw,Simm=phi*Sh,d=phi*Sh/c,c=c,CLmax=CLmax,CD0=CD0,k=1/(math.pi*0.8*5),
                Af=(0.6*0.46*M**0.355*0.15)**2,Vto=math.sqrt(2*M*g/(RA*Sw*CLmax)))
def net(U,p,fA,mode):
    W=p["M"]*g; qa=.5*RA*U*U; qw=.5*RW*U*U
    CL=min(p["CLmax"],W/(qa*p["Sw"])); Lw=qa*p["Sw"]*CL
    Dw=qa*p["Sw"]*(p["CD0"]+p["k"]*CL*CL); Db=qa*0.3*p["Af"]
    Fsv=2*SIG*p["c"]*1.0; Fsh=2*SIG*p["c"]*0.3
    CLz=max(0,W+Fsv-Lw)/(qw*p["Simm"]); AR=2*p["d"]**2/p["Simm"]
    Di=qw*p["Simm"]*CLz**2/(math.pi*0.8*AR)
    T=.5*RW*p["Simm"]*(C6*fA**2-cd(U,p["c"],mode)*U*U)
    return T-Dw-Db-Di-Fsh
def ueq(p,fA,mode,lo=0.5,hi=80):
    if net(hi,p,fA,mode)>0: return hi
    for _ in range(200):
        m=(lo+hi)/2; lo,hi=(m,hi) if net(m,p,fA,mode)>0 else (lo,m)
    return lo
def power(U,p,f,App):
    St=f*App/U; fs=f*p["c"]/U
    return .5*RW*U**3*p["Simm"]*(7.78*St**2+4.89*St**2*fs)
p=setup()
print(f"V_to={p['Vto']:.2f} m/s  S_imm={p['Simm']*1e4:.2f} cm2")
print("A) cross-check vs author table: net@10 (N)")
for App in (0.026,0.031):
    for m in ("const","scaled"): print(f"  App {App} {m}: net {net(10,p,50*App,m):+.3f}  U_eq {ueq(p,50*App,m):.2f}")
print("B) Deng steady state at 10 m/s, 50 Hz: A_pp that gives U_eq=10, and power there")
for m in ("const","scaled"):
    lo,hi=0.001,0.2
    for _ in range(100):
        a=(lo+hi)/2; lo,hi=(lo,a) if ueq(p,50*a,m)>=10 else (a,hi)
    print(f"  {m}: A_pp={hi*100:.2f} cm (deflection {math.degrees(math.asin(min(1,hi/2/0.05))):.1f} deg if lobe 5 cm), P(10 m/s)={power(10,p,50,hi):.1f} W")
print("  power at assumed A_pp 2.6 cm, 50 Hz, 10 m/s =",round(power(10,p,50,0.026),1),"W (no C_D term in power law)")
print("C) Deng 350 W -> 16.5 m/s. Hold A_pp 2.6 cm, raise f until U_eq=16.5; power at 16.5")
for App in (0.020,0.026,0.031):
  for m in ("const","scaled"):
    lo,hi=1,2000
    for _ in range(100):
        f=(lo+hi)/2; lo,hi=(lo,f) if ueq(p,f*App,m)>=16.5 else (f,hi)
    print(f"  App {App*100:.1f} cm {m}: f={hi:.0f} Hz  P(16.5)={power(16.5,p,hi,App):.0f} W  [Deng 350 W]")
print("D) const C_D: U_eq vs A_pp at 50 Hz (body 0.25 m; 0.2L = 5 cm)")
for App in (0.026,0.031,0.035,0.04,0.05,0.06):
    print(f"  App {App*100:.1f} cm: const U_eq {ueq(p,50*App,'const'):.1f}   scaled U_eq {ueq(p,50*App,'scaled'):.1f}")
