import math
g=9.81; rho=1.225
print("sqrt3*1.38",1.38*math.sqrt(3),"ratio",math.sqrt(3))
for Vto in [4.37,4.41,5.47,8.10,4.37*math.sqrt(0.40/0.25)]:
    print("Vto",round(Vto,3),"speed x",round(Vto/1.38,3),"KE x",round((Vto/1.38)**2,2))
for V in [1.57,1.57+0.27,1.57+2*0.27]:
    print("Demesmay V",V,"3xleap/V",round(1.38*math.sqrt(3)/V,3),"flight/V",round(4.37/V,3),"KE",round((4.37/V)**2,2))
# trajectory, reimplemented independently (RK-free semi-implicit Euler, dt 2e-5)
m=0.25e-3
def rng(V0,th,S=0,CL=0,CD0=0,AR=5,dt=2e-5):
    Af=2.4e-5;CDb=0.3;k=1/(math.pi*0.8*AR) if S else 0
    x=y=0;vx=V0*math.cos(th);vy=V0*math.sin(th)
    while True:
        V=math.hypot(vx,vy);q=0.5*rho*V*V
        D=q*(Af*CDb+S*(CD0+k*CL*CL));L=q*S*CL
        ux,uy=vx/V,vy/V
        vx+=(-D*ux-L*uy)/m*dt; vy+=((-D*uy+L*ux)/m-g)*dt
        x+=vx*dt;y+=vy*dt
        if y<0:return x
def best(V0,**kw): return max(rng(V0,math.radians(t),**kw) for t in range(25,61))
R0=best(1.38); print("WT range 1.38 with body drag",R0)
def solve(f,target,lo=1.5,hi=3.0):
    for _ in range(30):
        mid=(lo+hi)/2
        if f(mid)<target: lo=mid
        else: hi=mid
    return mid
print("V for 3x, body drag only:",solve(lambda v:best(v),3*R0))
for CD0 in [0.08,0.2]:
    for CL in [0.5,1.07]:
        print("V for 3x with wing C CD0",CD0,"CL",CL,":",solve(lambda v:best(v,S=192e-6,CL=CL,CD0=CD0),3*R0))
print("V for 3x drag-free wing C CL1.07:",solve(lambda v:best(v,S=192e-6,CL=1.07,CD0=0,AR=1e9),3*R0))
