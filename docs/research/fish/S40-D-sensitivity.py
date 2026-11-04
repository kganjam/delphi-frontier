import math
def greq(dE,w,Gj,a=10e-4,A=8e-6):
    if dE<=10: return float('inf')
    L=-math.log(1-10/dE); lam=w/(2*L)
    return Gj*(a/lam)**2/A
base=dict(dE=15,w=50e-4,Gj=2e-9)
g0=greq(**base); print("worst base",g0, "ratio to Hosoi low 5e-6:",g0/5e-6)
for k in ['dE','w','Gj']:
  for f in (0.5,2):
    p=dict(base); p[k]*=f; g=greq(**p); print(k,f,g, g/g0, "Hosoi-low gap",g/5e-6)
# a and A
print("a x2", greq(**base,a=20e-4)/g0, greq(**base,a=20e-4)/5e-6)
print("A /2", greq(**base,A=4e-6)/g0)
# elasticity wrt dE at 15
h=1e-4; print("elast dE@15", (math.log(greq(15+h,50e-4,2e-9))-math.log(greq(15-h,50e-4,2e-9)))/(math.log(15+h)-math.log(15-h)))
print("elast dE@30", (math.log(greq(30+h,200e-4,1e-9))-math.log(greq(30-h,200e-4,1e-9)))/(math.log(30+h)-math.log(30-h)))
# central case factor 2
c=greq(30,200e-4,1e-9); print("central",c, "dE15", greq(15,200e-4,1e-9), "dE15/central",greq(15,200e-4,1e-9)/c)
# dE where Hosoi-low is 100x below requirement (refutation) in w=50,Gj=2nS
lo,hi=10.0001,15
for _ in range(100):
  m=(lo+hi)/2
  if greq(m,50e-4,2e-9)>5e-4: lo=m
  else: hi=m
print("dE at which req = 100x Hosoi-low (5e-4):",hi)
for target,name in [(5e-4,'100xHosoiLow'),(1.5e-3,'100xHosoiHigh'),(3.3e-2,'100xKohlHigh'),(1e-2,'100xKohlLow')]:
  for (w,Gj) in [(50e-4,2e-9),(200e-4,1e-9),(1000e-4,0.2e-9)]:
    lo,hi=10.0000001,60
    for _ in range(200):
      m=(lo+hi)/2
      if greq(m,w,Gj)>target: lo=m
      else: hi=m
    print(name,w*1e4,Gj,"dE_refute<=",round(hi,3))
# dE_max from fold f
for D in (90,70,50):
  for f in (1.5,2,4,12):
    print("D",D,"f",f,"dEmax",round(D*(math.sqrt(f)-1)/(math.sqrt(f)+1),2))
for D in (90,70):
  for dE in (10,15,30,50):
    x=dE/D; print("D",D,"dE",dE,"f_min",round(((1+x)/(1-x))**2,2) if x<1 else 'inf')
# with dEmax=15.4 (D=90,f=2): requirement grid
for dE in (15.44,12.0,10.5):
  for (w,Gj) in [(50e-4,0.2e-9),(50e-4,1e-9),(50e-4,2e-9),(200e-4,1e-9),(200e-4,2e-9),(1000e-4,2e-9)]:
    print("dE",dE,"w",round(w*1e4),"Gj",Gj,"%.2e"%greq(dE,w,Gj))
