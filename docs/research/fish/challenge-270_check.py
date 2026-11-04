import math
g=9.81;rw=1000;sig=0.072;c=0.006;Slobe=18.9e-6
sc={"GEN":(0.25e-3,1.0,0.0,4.41,4.66),"CEN":(0.25e-3,0.5,0.5,4.41,1.76),"STI":(0.40e-3,0.25,1.0,5.58,0.61)}
for k,(m,phi,cth,vto,T) in sc.items():
    W=m*g;S=phi*Slobe;Fsv=2*sig*c*cth;U=0.45
    need=W*(1-(U/vto)**2)+Fsv;q=0.5*rw*U*U
    CL=need/(q*S)
    def umin(clmax): return math.sqrt((W+Fsv)/(0.5*rw*S*clmax+W/vto**2))
    print(k,"W %.3f mN need %.3f mN qS %.3f mN CL %.2f"%(W*1e3,need*1e3,q*S*1e3,CL),
          "Umin(CLmax1,1.3,1.5,2)=",["%.2f"%umin(x) for x in (1,1.3,1.5,2)],
          "| author thrust at 0.45 %.2f mN; need/thrust=%.2f; tilt deg=%s"%(T,need*1e3/T, "%.0f"%math.degrees(math.asin(need*1e3/T)) if need*1e3<T else "n/a"))
# lateral flapping speed vs U
for fA in (0.33,0.45): print("peak lateral lobe speed pi*f*App=%.2f m/s vs U=0.45"%(math.pi*fA))
