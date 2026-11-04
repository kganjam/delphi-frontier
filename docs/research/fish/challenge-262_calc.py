# Independent re-implementation: RK4 on state (vx,vy,x,y), event-located apex.
import math
g=9.81; rho=1.225
def deriv(s,P,wing):
    vx,vy=s[0],s[1]; V=math.hypot(vx,vy); q=0.5*rho*V*V
    D=q*P['Ab']*P['CDb']; L=0
    if wing:
        AR=P['b']**2/P['S']; CDi=P['CL']**2/(math.pi*P['e']*AR)
        L=q*P['S']*P['CL']; D+=q*P['S']*(P['CD0']+CDi)
    ax=(-D*vx/V - L*vy/V)/P['m']; ay=(-D*vy/V + L*vx/V)/P['m'] - g
    return (ax,ay,vx,vy)
def ascent(P,wing,dt=2e-5):
    th=math.radians(P['th']); s=(P['V']*math.cos(th),P['V']*math.sin(th),0,0); t=0
    while True:
        k1=deriv(s,P,wing); s2=tuple(a+0.5*dt*b for a,b in zip(s,k1))
        k2=deriv(s2,P,wing); s3=tuple(a+0.5*dt*b for a,b in zip(s,k2))
        k3=deriv(s3,P,wing); s4=tuple(a+dt*b for a,b in zip(s,k3)); k4=deriv(s4,P,wing)
        n=tuple(a+dt/6*(b+2*c+2*d+e) for a,b,c,d,e in zip(s,k1,k2,k3,k4))
        if n[1]<=0:  # interpolate apex
            f=s[1]/(s[1]-n[1]); return t+f*dt, s[3]+f*(n[3]-s[3])
        s=n; t+=dt
def P_of(frac=0.45,SL=0.030,m=0.25e-3,V=1.38,th=45,rule='C',CL=1.07,CD0=0.08,e=0.8,CDb=0.3):
    L=frac*SL; bw=0.004*SL/0.030; b=2*L+bw
    S=b*b/5 if rule=='C' else 2*0.7*L*0.1*SL
    return dict(S=S,b=b,m=m,V=V,th=th,CL=CL,CD0=CD0,e=e,CDb=CDb,Ab=2.4e-5*(SL/0.03)**2)
def red(P):
    t0,a0=ascent(P,False); t1,a1=ascent(P,True); return 1-t0/t1,(a1-a0)*1e3
print("S at 0.45 SL rule C (mm2):", round(P_of()['S']*1e6,1))
print("grid rule C SL3.0/0.25g  (frac: 0.95,1.38,1.57,2.11)")
for fr in (0.15,0.2,0.25,0.3,0.35,0.45):
    print(fr, round(P_of(fr)['S']*1e6), [f"{100*red(P_of(fr,V=V))[0]:.2f}%" for V in (0.95,1.38,1.57,2.11)])
print("grid rule C SL3.6/0.432g")
for fr in (0.15,0.25,0.45):
    print(fr, [f"{100*red(P_of(fr,SL=0.036,m=0.25e-3*1.2**3,V=V))[0]:.2f}%" for V in (1.38,1.57)])
def solve(tgt,**kw):
    lo,hi=0.02,1.5
    for _ in range(25):
        mid=(lo+hi)/2
        if red(P_of(mid,**kw))[0]<tgt: lo=mid
        else: hi=mid
    return round(mid,3)
for SL,m in ((0.03,0.25e-3),(0.036,0.25e-3*1.2**3)):
  for V in (1.38,1.57):
    print("thresh",SL,V,"2%:",solve(0.02,SL=SL,m=m,V=V),"5%:",solve(0.05,SL=SL,m=m,V=V))
print("rule A best cases:", [f"{100*red(P_of(0.45,V=V,rule='A'))[0]:.2f}%" for V in (1.38,1.57,2.11)])
print("x2 / x0.5 on inputs the S28-D table did not vary (baseline 0.45 SL, 1.38):")
print(" base", round(100*red(P_of())[0],2))
for k,vals in (('CD0',(0.04,0.16)),('e',(0.4,1.0)),('CDb',(0.15,0.6)),('th',(22.5,90)),('CL',(0.535,2.14))):
    print(" ",k,[ (v,round(100*red(P_of(**{k:v}))[0],2)) for v in vals])
# Vto at 0.79 SL and 0.45
for fr in (0.45,0.79):
    P=P_of(fr); Vto=math.sqrt(2*P['m']*g/(rho*P['S']*1.07)); print("Vto",fr,round(Vto,2),"def vs 2.11",round(Vto/2.11,2),"vs 2*1.38",round(Vto/2.76,2))
# Low-AR realistic-ish: AR imposed 2.5 (paddle fin) at same length
for fr in (0.25,0.45):
    L=fr*0.03;b=2*L+0.004;S=b*b/2.5;P=P_of(fr);P.update(S=S)
    print("AR2.5",fr,round(S*1e6),[f"{100*red(dict(P,V=V))[0]:.2f}%" for V in (1.38,1.57)])
print("\n== relaxations at fin <=0.25 SL ==")
def withAR(fr,AR,V,th=45,slope_corr=True):
    P=P_of(fr,V=V,th=th); b=P['b']; P['S']=b*b/AR
    if slope_corr: P['CL']=1.07*(1+2/5)/(1+2/AR)   # Helmbold-type finite-AR lift-slope ratio, same AoA
    return 100*red(P)[0]
for AR in (5,3.5,2.5):
    print(" AR",AR,"0.25SL 45deg", [f"{withAR(0.25,AR,V):.2f}%" for V in (1.38,1.57)])
for th in (30,22.5):
    print(" AR5 0.25SL th",th, [f"{100*red(P_of(0.25,V=V,th=th))[0]:.2f}%" for V in (1.38,1.57)])
print(" AR2.5 (CL corr) 0.25SL th 30", [f"{withAR(0.25,2.5,V,th=30):.2f}%" for V in (1.38,1.57)])
print(" 22.5deg 0.25SL apex rise mm", [round(red(P_of(0.25,V=V,th=22.5))[1],2) for V in (1.38,1.57)], " 45deg:",[round(red(P_of(0.25,V=V))[1],2) for V in (1.38,1.57)])
print(" 5% threshold at 22.5deg, 1.38/1.57:", solve(0.05,th=22.5,V=1.38), solve(0.05,th=22.5,V=1.57))
