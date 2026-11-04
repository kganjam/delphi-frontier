import math
g=9.81; rho=1.225; m=0.25e-3; W=m*g
print("sqrt3*1.38",1.38*math.sqrt(3),"ratio",math.sqrt(3),"4.37/1.38",4.37/1.38,"sq",(4.37/1.38)**2)
def traj(V0,th,CL,CD0,wing,S=192e-6,ARw=5,dt=2e-5):
    Af=2.4e-5; CDb=0.3; kk=1/(math.pi*0.8*ARw)
    x=y=0; vx=V0*math.cos(th); vy=V0*math.sin(th)
    while True:
        V=math.hypot(vx,vy); q=0.5*rho*V*V
        D=q*Af*CDb; L=0
        if wing: L=q*S*CL; D+=q*S*(CD0+kk*CL*CL)
        ux,uy=vx/V,vy/V
        vx+=(-D*ux-L*uy)/m*dt; vy+=((-D*uy+L*ux)/m-g)*dt; x+=vx*dt; y+=vy*dt
        if y<0: return x
def best(V,wing,CL=0,CD0=0,S=192e-6):
    AR=0.031**2/S
    return max(traj(V,math.radians(t),cl,CD0,wing,S,AR) for t in range(20,61) for cl in ([CL] if not wing else [0,0.3,0.5,0.7,0.9,1.07]))
R0=best(1.38,False); print("WT range 1.38",R0)
def solve(f):
    lo,hi=1.38,4.0
    for _ in range(25):
        mid=(lo+hi)/2
        if f(mid)<3*R0: lo=mid
        else: hi=mid
    return mid
print("wingless V for 3x:",solve(lambda V:best(V,False)))
for CD0,S in [(0.08,192e-6),(0.2,192e-6),(0.12,125e-6),(0.12,57e-6)]:
    print("wing",CD0,S*1e6,"V for 3x:",solve(lambda V:best(V,True,CD0=CD0,S=S)))
for mm in [0.25,0.40]:
    Vto=math.sqrt(2*mm*1e-3*g/(rho*192e-6*1.07)); print("m",mm,"Vto",Vto,"ratio",Vto/1.38,"KE",(Vto/1.38)**2)
