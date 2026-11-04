# Independent check of S32 taxi ceiling. Written from the stated inputs, not importing S32_taxi.py.
import math
rw,ra,nu,g=1000.,1.225,1e-6,9.81
c6,CDf,ReLo,ReHi=2.55,0.08,4780.,9560.
Ub,A,c=1.38,24e-6,6e-3
Sw,CLm=192e-6,1.07
def CD(U,mode):
    if mode=='const': return CDf
    Re=U*c/nu
    return CDf*math.sqrt(ReHi/Re) if Re>ReHi else (CDf*math.sqrt(ReLo/Re) if Re<ReLo else CDf)
def Vto(m): return math.sqrt(2*m*g/(ra*Sw*CLm))
# Step A: foil-only ceiling, closed form: U_max^2 = G/CD(U_max), G=(Cd*A/Sc + CD(Ub))*Ub^2
def umax(Cdb,Sc,mode):
    G=(Cdb*A/Sc+CD(Ub,mode))*Ub**2
    U=2.
    for _ in range(300): U=math.sqrt(G/CD(U,mode))
    return U,G
print("foil-only ceiling (no wing/induced/air drag), Sc=37.8 mm2")
for Cdb in (0.1,0.2,0.3):
  for mode in ('const','scaled'):
    U,G=umax(Cdb,37.8e-6,mode); print(f" Cdb {Cdb} {mode:6s} G {G:.3f} Umax {U:.2f} = {U/Vto(.25e-3):.2f} Vto(0.25g {Vto(.25e-3):.2f})")
# Full model GENEROUS (phi 1) with my own force balance, sweep fin area Sc
def ueq(Cdb,Sc,mode,m=.25e-3,phi=1.,CD0=.08,costh=0,dcos=0,H=None):
    G=(Cdb*A/Sc+CD(Ub,mode))*Ub**2
    if H is None: H=Sc/(0.7*c)          # keep the author's 0.7 taper; fin height follows area
    Simm=phi*Sc/2; d=phi*H/2; AR=2*d*d/Simm; W=m*g
    def net(U):
        qa=.5*ra*U*U; qw=.5*rw*U*U
        CL=min(CLm,W/(qa*Sw)); Lw=qa*Sw*CL
        Dw=qa*Sw*(CD0+CL*CL/(math.pi*.8*5)); Db=qa*.3*A
        CLz=max(0,W+2*.072*c*costh-Lw)/(qw*Simm)
        Di=qw*Simm*CLz**2/(math.pi*.8*AR)
        return .5*rw*Simm*(G-CD(U,mode)*U*U)-Dw-Db-Di-2*.072*c*dcos
    lo,hi=0.3,30.
    for _ in range(200):
        mid=(lo+hi)/2; lo,hi=(mid,hi) if net(mid)>0 else (lo,mid)
    return lo
print("\nfull-model U_eq, GENEROUS otherwise, sweep caudal fin area (author fixed 37.8 mm2, unmeasured)")
for Sc in (12,15,18,20,25,30,37.8,45):
    r=[ueq(Cdb,Sc*1e-6,mode) for Cdb in (0.2,0.3) for mode in ('const','scaled')]
    print(f" Sc {Sc:5.1f} mm2: Cdb0.2 const {r[0]:.2f} scaled {r[1]:.2f} | Cdb0.3 const {r[2]:.2f} scaled {r[3]:.2f}  (Vto 4.41)")
# area at which U_eq = Vto
for Cdb in (0.2,0.3):
  for mode in ('const','scaled'):
    lo,hi=1e-6,60e-6
    for _ in range(100):
        mid=(lo+hi)/2; lo,hi=(mid,hi) if ueq(Cdb,mid,mode)>=Vto(.25e-3) else (lo,mid)
    print(f" Cdb {Cdb} {mode}: closes (U_eq>=4.41) if Sc <= {lo*1e6:.1f} mm2")
print("\nbody Cd (frontal) needed to close at Sc 37.8, 0.25 g:")
for mode in ('const','scaled'):
    lo,hi=.1,5.
    for _ in range(100):
        mid=(lo+hi)/2; lo,hi=(lo,mid) if ueq(mid,37.8e-6,mode)>=Vto(.25e-3) else (mid,hi)
    print(f" {mode}: Cdb >= {hi:.2f}")
# CENTRAL replicate
print("\nCENTRAL replicate (Cdb .2 phi .5 scaled CD0 .12 cos .5 dcos .1):", round(ueq(.2,37.8e-6,'scaled',phi=.5,CD0=.12,costh=.5,dcos=.1,H=9e-3),2))
print("GENEROUS replicate:", round(ueq(.3,37.8e-6,'scaled',H=9e-3),2), " const:", round(ueq(.3,37.8e-6,'const',H=9e-3),2))
