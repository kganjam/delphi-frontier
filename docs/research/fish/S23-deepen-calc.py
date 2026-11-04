import itertools
g=9.81; m=0.4e-3; W=m*g
def EIreq(L,tol): return (W/2)*L**2/(8*tol)
# measured caudal-fin EI (Puri 2018): abstract 1.5-4e-9, conclusions 2-5e-9
EImeas=[1.5e-9,4e-9,5e-9]
# baseline actinotrichial modulus E0 candidates (Pa) and targets
E0={'Yadavally hydrated 1.2 MPa':1.2e6,'DMT 5 MPa':5e6,'DMT 10 MPa':10e6,
    'AFM PBS 0.2 GPa':0.2e9,'wet RTT fibril 0.35 GPa':0.35e9,'AFM PBS 0.5 GPa':0.5e9}
Et={'dry collagen 5 GPa':5e9,'silk-like 10 GPa':10e9}
print("Required EI:")
for L in (0.02,0.04):
  for tol in (0.05,0.10,0.20,0.50):
    print(f" L={L*100:.0f}cm tol={tol:.0%} EIreq={EIreq(L,tol):.3g}")
print("\nBaseline case: L=4cm, 10%, EImeas=4e-9, C=25 (original)")
S=EIreq(0.04,0.10)/4e-9; C=25
print(f" S={S:.0f} C={C} margin S/C={S/C:.1f}")
print(" factor-2 perturbations of each input (margin; <1 => conclusion flips):")
for name,fS,fC in [('EImeas x2',0.5,1),('EImeas /2',2,1),('tol x2',0.5,1),('L /2',0.25,1),('mass /2',0.5,1),('C x2 (E0/2)',1,2),('C /2',1,0.5)]:
  print(f"  {name:12s} margin={S*fS/(C*fC):.1f}")
print("\nMost lenient geometry/criterion corner: L=2cm, tol=50%, EImeas=5e-9")
Smin=EIreq(0.02,0.5)/5e-9
print(f" Smin={Smin:.1f}")
Smin20=EIreq(0.02,0.2)/5e-9; print(f" (tol=20%) Smin={Smin20:.1f}")
print("\nCeiling C=Et/E0 (f=1) vs lenient corner margin:")
for (a,e0),(b,et) in itertools.product(E0.items(),Et.items()):
  C=et/e0
  print(f" {a:28s}-> {b:20s} C={C:8.0f}  margin(tol50%)={Smin/C:7.3f}  margin(L4,10%,4e-9)={S/C:7.2f}")
print("\nFlip threshold on E0 (C=S): E0* = Et/S")
for b,et in Et.items():
  print(f" {b}: E0* lenient={et/Smin/1e6:.0f} MPa ; baseline={et/S/1e6:.1f} MPa")
