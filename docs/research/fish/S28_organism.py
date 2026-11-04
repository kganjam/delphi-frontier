import math
g=9.81; rho=1.225; nu=1.5e-5
m=0.25e-3; W=m*g
CLmax=1.07; Vto=4.37
S_ws = 2*W/(rho*Vto**2*CLmax)
print("implied S at m=0.25g:", S_ws*1e6, "mm2; W/S", W/S_ws)
b=0.031; 
for S in [57e-6,125e-6,192e-6]:
    print("S mm2",S*1e6,"AR",b*b/S,"Vto",math.sqrt(2*W/(rho*S*CLmax)), "Vto m=0.4g", math.sqrt(2*0.4e-3*g/(rho*S*CLmax)))
for V in [0.45,1.38]:
    print("V",V,"R45",V*V/g,"H90",V*V/(2*g),"H45",V*V/(4*g),"L/W at CLmax S192",(V/Vto)**2, "speed ratio",Vto/V,"KE ratio",(Vto/V)**2)
for f in [0.1,0.25,0.5,1.0]: print("f",f,"V",Vto*math.sqrt(f))
# skim
A=0.0119
for St in [0.36,0.54]:
    U=52*A/St; print("St",St,"U at 52Hz",U,"L/W",(U/Vto)**2)
# glide
AR=5;e=0.8;k=1/(math.pi*e*AR)
for CD0 in [0.08,0.12,0.2]:
    print("CD0",CD0,"L/Dmax",1/(2*math.sqrt(CD0*k)),"CL*",math.sqrt(CD0/k))
print("S to fly at 1.38:",192*(Vto/1.38)**2,"mm2")
# trajectory
def traj(V0,th,CL,CD0,wing=True,S=192e-6,ARw=5,dt=1e-5):
    Af=2.4e-5; CDb=0.3; kk=1/(math.pi*0.8*ARw)
    x=y=0; vx=V0*math.cos(th); vy=V0*math.sin(th); ymax=0
    while True:
        V=math.hypot(vx,vy); q=0.5*rho*V*V
        D=q*Af*CDb; L=0
        if wing: L=q*S*CL; D+=q*S*(CD0+kk*CL*CL)
        ux,uy=vx/V,vy/V
        ax=(-D*ux - L*uy)/m; ay=(-D*uy + L*ux)/m - g
        vx+=ax*dt; vy+=ay*dt; x+=vx*dt; y+=vy*dt; ymax=max(ymax,y)
        if y<0: return x,ymax
for V0 in [0.45,1.38]:
    best0=max((traj(V0,math.radians(t),0,0,False)[0],t) for t in range(30,61))
    print("V0",V0,"WT range",best0, traj(V0,math.radians(best0[1]),0,0,False))
    for CD0 in [0.08,0.2]:
      for S in [192e-6,125e-6,57e-6]:
        ARw=b*b/S
        best=max((traj(V0,math.radians(t),cl/10,CD0,True,S,ARw)[0],t,cl/10) for t in range(30,61,2) for cl in range(0,11,1))
        print("  CD0",CD0,"S",S*1e6,"best",best,"gain",best[0]/best0[0])
print("---- CL=1.07 fixed, theta optimised")
for S,CD0 in [(192e-6,0.08),(192e-6,0.2),(125e-6,0.12),(57e-6,0.12)]:
    ARw=b*b/S
    best=max((traj(1.38,math.radians(t),1.07,CD0,True,S,ARw)[0],t) for t in range(30,61))
    r,h=traj(1.38,math.radians(best[1]),1.07,CD0,True,S,ARw)
    rw,hw=traj(1.38,math.radians(45),0,0,False)
    print(S*1e6,CD0,"range",r,"apex",h,"theta",best[1],"gain",r/rw,"apex WT",hw)
# no-drag, lift-only upper bound
best=max((traj(1.38,math.radians(t),1.07,0,True,192e-6,5)[0],t) for t in range(30,61))
print("drag-free wing UB",best, best[0]/0.19360072305948678)
print("V for 3x WT range:",1.38*math.sqrt(3))
print("fin mass mg (t=50-100um, 1100kg/m3):",192e-6*50e-6*1100*1e6,192e-6*100e-6*1100*1e6)
print("Re at 1.38, c=6.2mm:",1.38*0.0062/nu,"at 4.37:",4.37*0.0062/nu)
print("hang time WT 45deg:",2*1.38*math.sin(math.pi/4)/g)
