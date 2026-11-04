"""S28-D: sensitivity of the S28 conclusion to each input, and recompute with improved inputs.
All outputs are CALCULATIONS on stated inputs, not observations. Run from repo root."""
import math
g=9.81; rho=1.225
BASE=dict(V=1.38, th=45.0, S=192e-6, span=0.031, m=0.25e-3, CL=1.07, CD0=0.08)
Af=2.4e-5; CDb=0.3

def fly(p, wing=True, dt=2e-6, ascent_only=False):
    th=math.radians(p['th']); m=p['m']; S=p['S']; AR=p['span']**2/S; k=1/(math.pi*0.8*AR)
    vx,vy=p['V']*math.cos(th),p['V']*math.sin(th); x=y=t=0.0; ymax=0
    while True:
        V=math.hypot(vx,vy); q=0.5*rho*V*V; ux,uy=vx/V,vy/V
        D=q*Af*CDb; L=0.0
        if wing: L=q*S*p['CL']; D+=q*S*(p['CD0']+k*p['CL']**2)
        ax=(-D*ux-L*uy)/m; ay=(-D*uy+L*ux)/m-g
        vy_old=vy
        vx+=ax*dt; vy+=ay*dt; x+=vx*dt; y+=vy*dt; t+=dt; ymax=max(ymax,y)
        if ascent_only and vy<=0: return dict(t_up=t, apex=y)
        if y<0: return dict(R=x, apex=ymax)

def metrics(p):
    wt=fly(p,False,ascent_only=True); mu=fly(p,True,ascent_only=True)
    vy0=p['V']*math.sin(math.radians(p['th']))
    dec_red=1-(vy0/mu['t_up'])/(vy0/wt['t_up'])
    R0=fly(p,False,dt=1e-5)['R']; R1=fly(p,True,dt=1e-5)['R']
    Vto=math.sqrt(2*p['m']*g/(rho*p['S']*p['CL']))
    return dict(LW_exit=0.5*rho*p['V']**2*p['S']*p['CL']/(p['m']*g), dec_red=dec_red,
                gain=R1/R0-1, R0=R0, Vto=Vto, deficit=Vto/p['V'])

def show(tag,p):
    r=metrics(p)
    print(f"{tag:42s} L/W exit {100*r['LW_exit']:5.1f}%  ascent-decel red {100*r['dec_red']:5.2f}%  "
          f"range gain {100*r['gain']:5.2f}%  WT range {100*r['R0']:5.1f} cm  Vto {r['Vto']:.2f}  flight deficit x{r['deficit']:.2f}")
    return r

def area_from_fin(Lfin, body_w=0.004, AR=None, chord=None):
    span=2*Lfin+body_w
    if AR: return span, span**2/AR          # case C rule: AR imposed
    return span, 2*0.7*Lfin*chord             # case A rule: chord fixed

print("== 1. Baseline (S28 case C) and x0.5 / x2 on each input ==")
show("baseline",BASE)
for key in ['V','S','m','CL']:
    for f in (0.5,2.0):
        p=dict(BASE); p[key]*=f; show(f"{key} x{f}",p)
# fin length: case C geometry (AR 5 at span=2L+4mm) so S scales ~L^2
for f in (0.5,2.0):
    Lf=0.0135*f; span,S=area_from_fin(Lf,AR=5); p=dict(BASE,span=span,S=S)
    show(f"fin length x{f} (AR5 rule, S={S*1e6:.0f} mm2)",p)
for th in (60,80):
    show(f"launch angle {th} deg",dict(BASE,th=th))

print("\n== 2. Phenotype vs pectoral fin length (per fin, as fraction of SL) -- the unmeasured input ==")
print("   geometry rule C (generous): AR 5 at span = 2*Lfin + body width;  rule A: chord 0.1 SL fixed, 0.7 fill")
def geom(frac, SL, rule):
    Lf=frac*SL; bw=0.004*SL/0.030
    span=2*Lf+bw
    S = span**2/5 if rule=='C' else 2*0.7*Lf*(0.1*SL)
    return span,S
def run_case(frac,V,SL,m,rule,th=45):
    global Af
    Af_save=Af; Af=2.4e-5*(SL/0.030)**2
    span,S=geom(frac,SL,rule)
    p=dict(BASE,V=V,th=th,S=S,span=span,m=m)
    wt=fly(p,False,ascent_only=True); mu=fly(p,True,ascent_only=True,)
    vy0=V*math.sin(math.radians(th))
    red=1-wt['t_up']/mu['t_up']   # mean-decel reduction = 1 - a_mu/a_wt = 1 - t_wt/t_mu
    dapex=(mu['apex']-wt['apex'])*1000
    Vto=math.sqrt(2*m*g/(rho*S*p['CL']))
    Af=Af_save
    return S*1e6, red, dapex, Vto/V
bodies=[("SL 3.0 cm, m 0.25 g (S28)",0.030,0.25e-3),
        ("SL 3.6 cm, m 0.43 g (isometric from S28)",0.036,0.25e-3*(3.6/3.0)**3)]
speeds=[("0.95 Demesmay 40-ms floor",0.95),("1.38 Miln max",1.38),("1.57 Demesmay mean",1.57),("2.11 Demesmay +2SD",2.11)]
fracs=[0.15,0.20,0.25,0.30,0.35,0.45]
for rule in ('C','A'):
  for bname,SL,m in bodies:
    print(f"\n-- rule {rule}, {bname}")
    print("   frac/SL  S(mm2) | " + " | ".join(f"{s[1]:.2f} m/s: red%, d_apex mm" for s in speeds))
    for fr in fracs:
        row=[]; S0=None
        for sn,V in speeds:
            S,red,da,defi=run_case(fr,V,SL,m,rule); S0=S
            row.append(f"{100*red:5.2f}%, {da:5.2f}")
        print(f"   {fr:.2f}   {S0:6.0f} | "+" | ".join(row))

print("\n== 3. Fin length (per fin / SL) at which the 45-deg ascent-decel reduction reaches 2% and 5% (rule C) ==")
def solve(target,V,SL,m):
    lo,hi=0.02,1.5
    for _ in range(30):
        mid=(lo+hi)/2
        if run_case(mid,V,SL,m,'C')[1]<target: lo=mid
        else: hi=mid
    return (lo+hi)/2
for bname,SL,m in bodies:
    for sn,V in speeds[1:3]:
        print(f"   {bname}, V={V}: 2% at {solve(0.02,V,SL,m):.3f} SL/fin; 5% at {solve(0.05,V,SL,m):.3f} SL/fin")

print("\n== 4. Flight (L=W) speed vs fin length, rule C, SL 3.0 / 0.25 g; best measured-tail exit 2.11 m/s ==")
for fr in fracs+[0.79]:
    span,S=geom(fr,0.030,'C'); Vto=math.sqrt(2*0.25e-3*g/(rho*S*1.07))
    print(f"   {fr:.2f} SL/fin  S {S*1e6:6.0f} mm2  Vto {Vto:5.2f} m/s  deficit vs 1.57: x{Vto/1.57:.2f}  vs 2.11: x{Vto/2.11:.2f}")

print("\n== 5. Tracking-noise floor on a per-leap fitted vertical acceleration (ASSUMED camera parameters) ==")
# Least-squares quadratic fit, N evenly spaced points over duration T, iid position noise sigma:
# var(c2) ~= 180 sigma^2 / (N T^4)  (large-N limit); a = 2 c2.
for fps,sig in [(240,0.5e-3),(1000,0.2e-3),(1000,0.5e-3)]:
    T=0.10; N=int(fps*T)
    sa=2*math.sqrt(180*sig**2/(N*T**4))
    print(f"   {fps} fps, sigma {sig*1e3:.1f} mm, ascent {T*1e3:.0f} ms: sigma_a = {sa:.3f} m/s^2 = {100*sa/g:.2f}% of g per leap")
print("   Plaut 2000 abstract: SL = 56.0/15.5 =", round(56.0/15.5,2), "cm (WT);", round(43.7/12.5,2), "cm (long-finned)")
