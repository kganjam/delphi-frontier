import math
g=9.81;rho=1.225;S=192e-6;CL=1.07
def frac(V,m): return 0.5*rho*V*V*S*CL/(m*g)
for m in [0.25e-3,0.25e-3+21.1e-6,0.40e-3]:
    print("m g",m*1e3,"launch",frac(1.38,m),"vertical comp @45",frac(1.38,m)*math.cos(math.pi/4),"apex(0.976)",frac(1.38*math.cos(math.pi/4),m))
print("Vto from S=192,m=.25:",math.sqrt(2*0.25e-3*g/(rho*S*CL)))
# integrate script-style to get actual apex speed with wing CL1.07 CD0 .08, theta 45 and opt
def traj(V0,th,CD0=0.08,m=0.25e-3,dt=1e-6):
    Af=2.4e-5;k=1/(math.pi*0.8*5);x=y=0;vx=V0*math.cos(th);vy=V0*math.sin(th)
    while True:
        V=math.hypot(vx,vy);q=0.5*rho*V*V;D=q*Af*0.3+q*S*(CD0+k*CL*CL);L=q*S*CL
        ux,uy=vx/V,vy/V;ax=(-D*ux-L*uy)/m;ay=(-D*uy+L*ux)/m-g
        nvy=vy+ay*dt
        if vy>0 and nvy<=0: return V, L/(m*g)
        vx+=ax*dt;vy=nvy;x+=vx*dt;y+=vy*dt
for th in [40,45,50]:
    print("theta",th,"apex V, L/W",traj(1.38,math.radians(th)))
