import math, numpy as np
g=9.81; rho=1.225; m=0.25e-3; W=m*g; b=0.031
Af=2.4e-5; CDb=0.3
def run(V0,thdeg,S,CL,CD0,wing=True,dt=2e-6):
    th=math.radians(thdeg); AR=b*b/S; k=1/(math.pi*0.8*AR)
    vx,vy=V0*math.cos(th),V0*math.sin(th); x=y=t=0
    T=[];Y=[];AY=[];LV=[]
    while vy>0:
        V=math.hypot(vx,vy); q=0.5*rho*V*V; ux,uy=vx/V,vy/V
        D=q*Af*CDb; L=0
        if wing: L=q*S*CL; D+=q*S*(CD0+k*CL*CL)
        ax=(-D*ux-L*uy)/m; ay=(-D*uy+L*ux)/m-g
        T.append(t);Y.append(y);AY.append(ay);LV.append(L/W)
        vx+=ax*dt; vy+=ay*dt; x+=vx*dt; y+=vy*dt; t+=dt
    T=np.array(T);Y=np.array(Y)
    fit=np.polyfit(T,Y,2)[0]*2   # fitted constant vertical accel
    return dict(t=t,apex=y,mean_ay=-V0*math.sin(th)/t,fit=fit,L0=LV[0],Lapex=LV[-1])
for V0 in [1.38,0.9,0.45]:
  for th in [45,60,80]:
    wt=run(V0,th,192e-6,0,0,False)
    for name,S in [("C",192e-6),("B",125e-6),("A",57e-6)]:
      for CD0 in [0.08,0.20]:
        r=run(V0,th,S,1.07,CD0)
        print(f"V0={V0} th={th} case {name} CD0={CD0}: L/W exit {r['L0']:.3f} apex {r['Lapex']:.3f} | "
              f"mean ascent decel {-r['mean_ay']:.3f} vs WT {-wt['mean_ay']:.3f} -> red {100*(1-r['mean_ay']/wt['mean_ay']):.2f}% | "
              f"fit-accel red {100*(1-r['fit']/wt['fit']):.2f}% | apex {r['apex']*100:.3f} vs {wt['apex']*100:.3f} cm ({100*(r['apex']/wt['apex']-1):+.2f}%) | t_up {r['t']*1000:.1f} ms")
