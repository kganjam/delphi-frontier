import math
rho,g=1.225,9.81
def run(S,m,V0,CL,CD0=0.08,AR=5.0,e=0.8,gam=45.0):
    W=m*g; k=0.5*rho*CL*S/W            # (L/W) per V^2
    CD=CD0+CL*CL/(math.pi*e*AR); DL=CD/CL
    LW0=k*V0**2
    u=V0*math.cos(math.radians(gam)); vy0=V0*math.sin(math.radians(gam))
    # instantaneous, exit
    vert_exit=LW0*math.cos(math.radians(gam))-LW0*DL*math.sin(math.radians(gam))
    LWap=k*u**2
    # time-mean over ascent, vy linear 0..vy0 (g_eff approx g)
    N=20000; sl=sd=0.0
    for i in range(N):
        vy=vy0*(i+0.5)/N; V=math.hypot(u,vy)
        sl+=k*V*V*(u/V); sd+=k*V*V*DL*(vy/V)
    sl/=N; sd/=N
    return dict(LW0=LW0,LWap=LWap,DW0=LW0*DL,vert_exit=vert_exit,mean=sl-sd,meanlift=sl,meandrag=sd,LD=1/DL)
for S in (196e-6,80e-6,40e-6):
    r=run(S,0.25e-3,1.38,1.07)
    print(f"S={S*1e6:5.0f} mm2  L/W exit {r['LW0']*100:5.2f}%  apex {r['LWap']*100:5.2f}%  D/W {r['DW0']*100:4.2f}%  vert@exit {r['vert_exit']*100:5.2f}%  path-mean {r['mean']*100:5.2f}%  L/D={r['LD']:.2f}")
print()
# sensitivity: realistic low-Re polar / lower CL
for CL,CD0 in ((1.07,0.08),(1.07,0.20),(0.8,0.15),(0.6,0.20),(0.5,0.30)):
    r=run(196e-6,0.25e-3,1.38,CL,CD0=CD0)
    print(f"CL={CL} CD0={CD0}: L/D={r['LD']:.2f} exit L/W={r['LW0']*100:.2f}% vert@exit={r['vert_exit']*100:.2f}% path-mean={r['mean']*100:.2f}%")
print()
# vertical leap: gamma=90
r=run(196e-6,0.25e-3,1.38,1.07,gam=89.999)
print("vertical leap gamma=90: vert@exit = %.2f%% (lift has no vertical part; drag is purely downward)"%(r['vert_exit']*100))
print("  pure drag penalty D/W = -%.2f%%"%(r['DW0']*100))
# mass 0.40 g
r=run(196e-6,0.40e-3,1.38,1.07); print("m=0.40 g: exit L/W %.2f%% path-mean %.2f%%"%(r['LW0']*100,r['mean']*100))
r=run(196e-6,0.25e-3,0.45,1.07); print("V0=0.45: exit L/W %.2f%% path-mean %.2f%%"%(r['LW0']*100,r['mean']*100))
# Re estimate for AR 5, S=196mm2 (two fins -> each 98mm2)
for S in (196e-6,80e-6):
    b=math.sqrt(5*S); c=S/b
    print(f"S={S*1e6:.0f}mm2 AR5 single wing: span {b*1e3:.1f} mm chord {c*1e3:.2f} mm  Re@1.38 = {1.38*c/1.5e-5:.0f}")
