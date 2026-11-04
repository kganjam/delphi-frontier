from math import sqrt
g=9.81; ra=1.225; CL=1.07; mb=0.40e-3; BL=0.04
sig={'low':1050*40e-6,'cen':1150*120e-6,'high':1557*200e-6,'hi+':1557*281e-6}
print({k:round(v,4) for k,v in sig.items()})
for k,v in sig.items(): print(k,'Vself',round(sqrt(2*v*g/(ra*CL)),3))
print('lift/area @1.38', 0.5*ra*1.38**2*CL/g)
S={'A':57,'B':125,'C':192,'S2s':450,'S2m':900,'S10':1070,'S2L':1800,'1925':1925}
def Vto(Smm,s): Sm=Smm*1e-6; return sqrt(2*(mb+s*Sm)*g/(ra*Sm*CL))
for n,a in S.items():
  print(n, [f"{sig[k]*a*1e-6/mb*100:.1f}%" for k in sig], [round(Vto(a,sig[k]),2) for k in ('cen','high')], round(Vto(a,0),2))
print('S at which wing=body, high', mb/sig['high']*1e6)
def P(V,s_bl,eta,fm,M):
  t=2*s_bl*BL/V; return (V*V/2)/t/eta*M/(fm*mb)
for n in ('C','S2m','S10'):
  a=S[n]; V=Vto(a,sig['cen']); M=mb+sig['cen']*a*1e-6
  for s in (0.5,1,2):
    r=[P(V,s,1,.6,M),P(V,s,.37,.6,M),P(V,s,.37,.3,M)]
    print(n,round(V,2),s,[round(x) for x in r],[round(x/142.7,2) for x in r])
print('calib',P(1.38,1,1,.3,mb),P(1.38,1,.37,.3,mb))
# robustness: anchored ratio vs demonstrated wingless performance (eta,fm cancel)
for n in ('S10','S2m','C'):
  a=S[n]; V=Vto(a,sig['cen']); M=mb+sig['cen']*a*1e-6
  for s in (1,2): print('ratio',n,s, round(M/mb*(V/1.38)**3*(1/s),2))
# coherent upper bracket: soft/ray-mix density on inter-ray thickness
for t in (200e-6,281e-6):
  for rho in (1050,1150):
    sg=rho*t; print('coherent',t,rho,round(sg,3),'S_eq',round(mb/sg*1e6),'1925:',round(sg*1925e-6/mb*100),'%', 'S2L:',round(sg*1800e-6/mb*100),'%')
# area-weighted taper mean (width 5->8 mm, t 200->40)
import numpy as np
x=np.linspace(0,1,100001); w=5+3*x; t=200-160*x; print('area-wtd mean t', (w*t).mean()/w.mean())
# run-up needed to close most generous case at 142.7
a=S['S10'];V=Vto(a,sig['cen']);M=mb+sig['cen']*a*1e-6
print('s_BL to close S10 eta.37 fm.6', P(V,1,.37,.6,M)/142.7)
# CL 1.5 sensitivity on S10 2BL
CL=1.5; V=Vto(a,sig['cen']); print('CL1.5 S10 V',round(V,2),'P',round(P(V,2,.37,.6,M)),round(P(V,2,.37,.6,M)/142.7,2))
