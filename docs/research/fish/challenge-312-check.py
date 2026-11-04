import math
from scipy.special import k1
from scipy.optimize import brentq
a=10e-4; A=8e-6; Vt=10.0
def rho_needed(dE,geom):
    q=1-Vt/dE  # required residual fraction
    if geom=='slab': return -math.log(q)            # e^{-rho}=q, rho=w/(2lam)
    if geom=='disk': return brentq(lambda r: r*k1(r)-q,1e-9,50)   # V0=dE(1-rho K1(rho)), rho=R/lam
    if geom=='sphere': return brentq(lambda r:(1+r)*math.exp(-r)-q,1e-9,60)
def greq(dE,w,Gj,geom='slab'):
    if dE<=Vt: return float('inf')
    lam=(w/2)/rho_needed(dE,geom)
    return Gj*(a/lam)**2/A
print("slab grid check vs S40:")
for dE in (15,30,50):
  print(dE,["%.2g"%greq(dE,w*1e-4,G*1e-9) for G in (0.2,1,2) for w in (50,200,1000)])
print("worst 15/50/2nS gap to 5e-6:",greq(15,50e-4,2e-9)/5e-6)
h=1e-5
el=lambda f,x:(math.log(f(x+h))-math.log(f(x-h)))/(math.log(x+h)-math.log(x-h))
print("elast@15 worst",el(lambda d:greq(d,50e-4,2e-9),15),"elast@30 central",el(lambda d:greq(d,200e-4,1e-9),30))
def thr(w,Gj,tgt,geom='slab'):
    return brentq(lambda d:greq(d,w,Gj,geom)-tgt,10+1e-9,200)
for geom in ('slab','disk','sphere'):
  print(geom,"refute-dE worst corner vs Hosoi-low:",round(thr(50e-4,2e-9,5e-4,geom),3),
        " central(200um,1nS):",round(thr(200e-4,1e-9,5e-4,geom),3))
  for dE in (12.0,15.44):
    g=greq(dE,50e-4,2e-9,geom); print("   dE",dE,"worst g_req %.2e gap %.1fx"%(g,g/5e-6))
print("dEmax f=2:",[round(D*(math.sqrt(2)-1)/(math.sqrt(2)+1),2) for D in (90,70,58.3,50)])
print("D needed for dEmax=10 at f=2:",10/((math.sqrt(2)-1)/(math.sqrt(2)+1)), " for 10.3:",10.3/((math.sqrt(2)-1)/(math.sqrt(2)+1)))
# baseline-constrained: surround Vm given; domain has f x (or 1/f) gK
def dE_given_Vm(Vm,EL,EK,f):
    D=EL-EK; p=(EL-Vm)/D; r=p/(1-p)
    up=D*(f*r/(1+f*r)-p); dn=D*(p-(r/f)/(1+r/f))
    return up,dn
print("baseline-constrained dE (f=2), rows Vm, cols (EL,EK):")
for Vm in (-16,-20,-25,-35,-50,-60,-75):
  row=[]
  for EL in (0,-10,-20):
    for EK in (-86,-100):
      if Vm>=EL or Vm<=EK: row.append("  n/a  ");continue
      u,d=dE_given_Vm(Vm,EL,EK,2); row.append("%5.1f/%4.1f"%(u,d))
  print(Vm,row)
# optimal-baseline Vm
for EL,EK in ((0,-86),(0,-100),(-20,-86),(-20,-100)):
  r=1/math.sqrt(2); print("Vm at optimum baseline",EL,EK, round(EL-(EL-EK)*r/(1+r),1))
