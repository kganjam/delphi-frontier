import math
g=9.81;rho=1.2
def Mom(m=0.4e-3,V=3,n=3,CL=0.78,AR=9,hw=2.5e-3):
    W=m*g; S=2*W/(rho*V**2*CL); b=(AR*S)**.5; s=b/2-hw
    return n*(W/2)*(4/(3*math.pi))*s
def d(M,sig): return (32*M/(math.pi*sig))**(1/3)*1e3
M0=Mom(); print("M0",M0)
for s in (62.6,66.8,49.4,43.4,36.2,20.0,25,114): print(s,"MPa d=",round(d(M0,s*1e6),3),"SF1.5:",round(d(1.5*M0,s*1e6),3))
for f in (0.5,2): print("mass x",f,"M x",Mom(m=0.4e-3*f)/M0,"d x",(Mom(m=0.4e-3*f)/M0)**(1/3))
for f in (0.5,2): print("hw x",f,"d x",(Mom(hw=2.5e-3*f)/M0)**(1/3))
print("E*eps_y: small",3.5*0.030*1e3,"large",2.6*0.036*1e3,"MPa")
# isometric: mass x2 -> L x 2^(1/3); section x 2^(1/3) -> Z x2 ; M x?
f=2; Mi=Mom(m=0.4e-3*f,hw=2.5e-3*f**(1/3)); print("isometric mass x2: M x",Mi/M0,"Z x",f, "stress x",Mi/M0/f)
