"""challenge-305 independent check. Run from docs/research/fish: python3 -I challenge-305_check.py
Imports only the S32-D force model (S32-deepen_calc.py, copied unchanged from
origin/claude/deepen-s32-sensitive-input-sy9vpn). The threshold search and the Re sweep are
written independently of S32-D-deepen_calc.py. Everything printed is CALCULATED, nothing is measured."""
# Independent check: threshold from analytic G* (no import of author's search code except force model for G*)
import math, importlib.util, contextlib, io
spec=importlib.util.spec_from_file_location("d","S32-deepen_calc.py"); d=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(d)
A=24e-6; S=0.7*6e-3*9e-3
def cdl(U):
    Re=U*6e-3/1e-6
    return 0.08*math.sqrt(4780/Re) if Re<4780 else (0.08*math.sqrt(9560/Re) if Re>9560 else 0.08)
def Gstar(s):  # G at which U_eq = V_to, by bisection on G directly
    lo,hi=0.01,50
    for _ in range(80):
        m=(lo+hi)/2; p=d.build(s); p=dict(p,G=m)
        r=d.u_eq(p)/p["Vto"]; lo,hi=(lo,m) if r>=1 else (m,hi)
    return hi
def thr(G,cdb):
    lo,hi=0.1,20
    for _ in range(80):
        m=(lo+hi)/2; v=(cdb*A/S+cdl(m))*m*m; lo,hi=(lo,m) if v>=G else (m,hi)
    return hi
for nm,s in (("GEN",d.BASE),("CEN",d.CENTRAL)):
    G=Gstar(s); print(nm,"G*=%.3f"%G,"thr S32 Cdb=%.2f"%thr(G,s["Cdb"]),"x2 %.2f"%thr(G,2*s["Cdb"]))
    for cdb in (0.024*15,0.024*17.3,0.024*18.9,0.024*20):
        print("   Cdb %.3f thr %.2f"%(cdb,thr(G,cdb)))
    for ub in (1.57,0.95):
        need=(G/ub**2-cdl(ub))*S/A; print("   U_b %.2f needs Cd_front %.3f = x%.2f on 0.4536"%(ub,need,need/0.4536))
# Re-invariance relaxed: C at design Re = 0.024*(Re_M/Re_d)^n, Re_d at U_b=1.57, L=30mm
Red=1.57*0.03/1e-6
print("Re_design(1.57)=%.0f"%Red)
GG=Gstar(d.BASE); GC=Gstar(d.CENTRAL)
for n in (0.2,0.5):
  for ReM in (3000,10000,20000,47100):
    c=0.024*(ReM/Red)**n*18.9
    mg=((GG/1.57**2-cdl(1.57))*S/A)/c; mc=((GC/1.57**2-cdl(1.57))*S/A)/c
    print("n=%.1f Re_M=%6d Cd_front %.3f thrGEN %.2f thrCEN %.2f mult-to-flip GEN x%.2f CEN x%.2f"%(n,ReM,c,thr(GG,c),thr(GC,c),mg,mc))
