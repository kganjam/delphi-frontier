import math
rw,ra,nu,g,sig=1000,1.225,1e-6,9.81,0.072
c6,c8,c9=2.55,7.78,4.89
def geo(M):
    WL=285.015*M**0.4; Sw=M*g/WL; Sh=0.003*M**0.65; Vto=math.sqrt(2*M*g/(ra*Sw*1.07)); return Sw,Sh,Vto
def cd(U,mode,c=0.025):
    if mode=='const': return 0.08
    Re=U*c/nu; return 0.08*math.sqrt(9560/Re) if Re>9560 else 0.08
def other(U,M,phi=0.5,c=0.025):
    Sw,Sh,Vto=geo(M); S=phi*Sh; W=M*g; qa=.5*ra*U*U; qw=.5*rw*U*U
    CL=min(1.07,W/(qa*Sw)); Dw=qa*Sw*(0.08+CL*CL/(math.pi*0.8*5))
    Af=(0.6*0.46*M**0.355*0.15)**2; Db=qa*0.3*Af
    need=max(0,W+2*sig*c-qa*Sw*CL); CLz=need/(qw*S); d=phi*Sh/c; AR=2*d*d/S
    Di=qw*S*CLz**2/(math.pi*0.8*AR); Fsh=2*sig*c*0.3
    return Dw+Db+Di+Fsh, S
def net(U,M,fA,mode,phi=0.5):
    o,S=other(U,M,phi); return .5*rw*S*(c6*fA**2-cd(U,mode)*U*U)-o
def ueq(M,fA,mode):
    lo,hi=0.5,80
    for _ in range(200):
        m=(lo+hi)/2; lo,hi=(m,hi) if net(m,M,fA,mode)>0 else (lo,m)
    return lo
def power(U,S,fA,f,c=0.025): return .5*rw*U*S*fA**2*(c8+c9*f*c/U)
M=0.191; Sw,Sh,Vto=geo(M); print(f"191g: Sw {Sw*1e4:.1f} cm2 Sh {Sh*1e4:.2f} Vto {Vto:.2f}")
for M_ in (0.191,0.300):
    _,_,V=geo(M_); L=0.256 if M_==0.191 else None
    for A in (0.020,0.026,0.031,0.051,0.060):
        print(f"M {M_} A {A*100:.1f}cm Ueq const {ueq(M_,50*A,'const'):.2f} scaled {ueq(M_,50*A,'scaled'):.2f} Vto {V:.2f}")
# 36 W check with no C_D
S=0.5*Sh
for A in (0.020,0.026,0.031): print("P@10",A,round(power(10,S,50*A,50),1))
# steady-state amplitude and power needed
def fA_needed(U,mode,M=0.191):
    o,S=other(U,M); return math.sqrt((o/(.5*rw*S)+cd(U,mode)*U*U)/c6)
for U,PD in ((10,36),(16.5,350)):
    for mode in ('const','scaled'):
        fA=fA_needed(U,mode); print(f"U {U} {mode}: A_pp@50Hz {fA/50*100:.2f} cm P {power(U,S,fA,50):.1f} W (Deng {PD})")
    # implied C_D for given power, several frequencies
    o,_=other(U,M)
    for f in (13.5,25,50,100):
        fA2=PD/(.5*rw*U*S*(c8+c9*f*0.025/U)); T=.5*rw*S*c6*fA2
        print(f"   f {f}: gross thrust {T:.3f} N other drag {o:.3f} N implied C_D {(T-o)/(.5*rw*S*U*U):.4f}  A_pp {math.sqrt(fA2)/f*100:.1f} cm")
    # sensitivity to propulsive power law: multiply P/T by k
    for k in (0.5,0.75,1.0,1.5):
        fA2=PD/(k*.5*rw*U*S*(c8+c9*50*0.025/U)); T=.5*rw*S*c6*fA2
        print(f"   power-law factor {k}: implied C_D {(T-o)/(.5*rw*S*U*U):.4f}")
    # sensitivity to immersed fraction phi
    for phi in (0.25,0.5,1.0):
        o2,S2=other(U,M,phi); fA2=PD/(.5*rw*U*S2*(c8+c9*50*0.025/U)); T=.5*rw*S2*c6*fA2
        print(f"   phi {phi}: implied C_D {(T-o2)/(.5*rw*S2*U*U):.4f}")
print("Re-scaled cd at 10, 16.5:",cd(10,'s'),cd(16.5,'s'))
print("--- phi sweep: power needed for steady U (50 Hz)")
for phi in (0.25,0.5,1.0):
    for mode in ('const','scaled'):
        Ps=[]
        for U in (10,16.5):
            o,S=other(U,0.191,phi); fA=math.sqrt((o/(.5*rw*S)+cd(U,mode)*U*U)/c6); Ps.append(power(U,S,fA,50))
        print(f"phi {phi} {mode}: P10 {Ps[0]:.1f} W P16.5 {Ps[1]:.1f} W ratio {Ps[1]/Ps[0]:.2f} (Deng 36/350, 9.72)")
# A_pp for const to reach Vto
lo,hi=0.03,0.1
for _ in range(100):
    m=(lo+hi)/2; lo,hi=(m,hi) if ueq(0.191,50*m,'const')<14.98 else (lo,m)
print("const A_pp for Ueq=Vto 191 g:",round(hi*100,2),"cm")
