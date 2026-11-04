# Challenge 294: independent re-implementation of the S32 / S32-D taxi force model from its stated equations
# (not imported from S32-deepen_calc.py). Run: python3 docs/research/fish/challenge-294_indep.py  (<5 s). All output CALCULATED.
# Independent re-implementation (written from the stated equations, not imported).
import math
rw,ra,nu,g,sig=1000.,1.225,1e-6,9.81,0.072
def cdl(U,c=6e-3,cd0=0.08):
    Re=max(U,1e-9)*c/nu
    return cd0*math.sqrt(4780/Re) if Re<4780 else cd0*math.sqrt(9560/Re) if Re>9560 else cd0
def ueq_ratio(Cdb,Ub,cen=False,m=0.25e-3):
    A=24e-6; Sf=0.7*6e-3*9e-3; Sw=192e-6; CL=1.07
    phi,CD0,costh,dcos=(0.5,0.12,0.5,0.1) if cen else (1.0,0.08,0.0,0.0)
    G=(Cdb*A/Sf+cdl(Ub))*Ub**2
    Si=phi*Sf/2; dd=phi*9e-3/2; AR=2*dd*dd/Si; k=1/(math.pi*0.8*5)
    W=m*g; Vto=math.sqrt(2*W/(ra*Sw*CL))
    def net(U):
        qa,qw=.5*ra*U*U,.5*rw*U*U
        cl=min(CL,W/(qa*Sw)); Lw=qa*Sw*cl
        Dw=qa*Sw*(CD0+k*cl*cl); Db=qa*0.3*A
        Fv=2*sig*6e-3*costh; Fh=2*sig*6e-3*dcos
        CLz=max(0,W+Fv-Lw)/(qw*Si); Di=qw*Si*CLz**2/(math.pi*0.8*AR)
        T=.5*rw*Si*(G-cdl(U)*U*U)
        return T-Dw-Db-Di-Fh
    lo,hi=0.05,60
    for _ in range(200):
        mid=(lo+hi)/2
        if net(mid)>0: lo=mid
        else: hi=mid
    return lo/Vto
def thr(Cdb,cen=False):
    lo,hi=0.1,20
    for _ in range(80):
        mid=(lo+hi)/2
        if ueq_ratio(Cdb,mid,cen)>=1: hi=mid
        else: lo=mid
    return hi
def cdflip(Ub,cen=False):
    lo,hi=0.01,20
    for _ in range(80):
        mid=math.sqrt(lo*hi)
        if ueq_ratio(mid,Ub,cen)>=1: hi=mid
        else: lo=mid
    return hi
print("baseline thr GEN/CEN", round(thr(0.3),3), round(thr(0.2,True),3))
print("x2 Cdb thr GEN/CEN", round(thr(0.6),3), round(thr(0.4,True),3))
# wetted/frontal
L=0.030;A=24e-6;b=math.sqrt(A/math.pi);a=L/2;e=math.sqrt(1-(b/a)**2)
S=2*math.pi*b*b*(1+a/(b*e)*math.asin(e)); print("spheroid S_wet mm2",S*1e6,"ratio",S/A, "volume mm3",4/3*math.pi*a*b*b*1e9)
for r in (15,17.3,18.9,20): print("Cd_front from 0.024 at ratio",r,"=",round(0.024*r,3))
for cd in (0.36,0.45,0.48):
    print(f"Cd {cd}: thr GEN {thr(cd):.3f} CEN {thr(cd,True):.3f}  ratio@1.57 GEN {ueq_ratio(cd,1.57):.3f} CEN {ueq_ratio(cd,1.57,True):.3f}")
fg,fc=cdflip(1.57),cdflip(1.57,True)
print("flip Cd at 1.57 GEN/CEN",round(fg,3),round(fc,3),"mult over 0.4536:",round(fg/0.4536,3),round(fc/0.4536,3))
print("flume branch GEN Cd=0.4536*5:",[round(ueq_ratio(0.4536*5,u),3) for u in (0.39,0.54)])
print("Tandler 0.29 thr GEN/CEN",round(thr(0.0154*18.9),3),round(thr(0.0154*18.9,True),3))
# Re transfer of McHenry's coefficient: coefficient measured at Re_M, applied at Re_design = 1.57*0.03/nu
Red=1.57*0.03/nu; print("design Re at 1.57 m/s",Red)
for ReM in (2000,5000,10000,20000,47100):
    for n,lab in ((0.5,"lam"),(0.2,"turb")):
        cd=0.4536*(ReM/Red)**n
        print(f"  Re_M {ReM:6d} {lab}: Cd_front {cd:.3f}  multiplier needed GEN {fg/cd:.2f} CEN {fc/cd:.2f}")
