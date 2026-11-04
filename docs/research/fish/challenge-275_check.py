#!/usr/bin/env python3
"""Challenge 275: independent recomputation of S3 launch power for every S3 planform >= 192 mm2, all four tissue brackets. Computation only; nothing here is a measurement."""
from math import sqrt
g=9.81;ra=1.225;CL=1.07;mb=0.4e-3;WM=142.7
sig={'low':1050*40e-6,'central':(0.8*1050+0.2*1557)*120e-6,'high':1557*200e-6,'high+':1557*281e-6}
for k,s in sig.items(): print(k,round(s,4),'Vself',round(sqrt(2*s*g/(ra*CL)),3))
print('lpa1.38',0.5*ra*1.38**2*CL/g)
P=[('S28C',192),('S2s',450),('S2m',900),('S10',1070),('S2L',1800),('S28fly',1925)]
for nm,Smm in P:
  S=Smm*1e-6
  for k,s in sig.items():
    M=mb+s*S;V=sqrt(2*M*g/(ra*S*CL))
    out=[]
    for eta in (1,0.37):
      for fm in (0.6,0.3):
        Pm=V**3/(4*0.08)/eta*M/(fm*mb); out.append(f"eta{eta} f{fm}:{Pm:6.0f}({Pm/WM:4.2f}x)")
    print(f"{nm:7s}{k:8s} mw%={100*s*S/mb:5.1f} V={V:4.2f} 2BL "+' '.join(out))
# power minimum over S (continuous): P∝V^3 M
for k,s in sig.items():
  best=min(((sqrt(2*(mb+s*S*1e-6)*g/(ra*S*1e-6*CL))**3/0.32/0.37*(mb+s*S*1e-6)/(0.6*mb)),S) for S in range(100,20000,10))
  print('opt',k,round(best[0]),best[1],'mm2', round(best[0]/WM,2))
