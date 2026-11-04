import math
need=10.17; m0=0.25e-3
for s in (3.30,5.47,8.36,10.94):
    R=s/need
    print(s, round(R,4), [round(m0*R**(1/b)*1e6,1) for b in (1/3,0.36,0.40,0.533)])
bs={'Cyp':(0.400,113),'Dan':(0.533,11),'Exo':(0.360,26),'Fod':(0.434,9),'Hir':(0.526,21),'Par':(0.408,19)}
print('mean b',sum(v[0] for v in bs.values())/6, 'N-weighted',sum(v[0]*v[1] for v in bs.values())/sum(v[1] for v in bs.values()))
# central m* if beta=0.45 used
print('m* beta .45', m0*(5.47/need)**(1/0.45)*1e6)
# sign condition with eta_h exponent gamma: R ~ m^(alpha+gamma-beta)
# max average gamma over a span if eta rises from eta_s to <=1
for eta_s in (0.37,0.2,0.1):
  for span in (10,100,1000):
    print('eta_s',eta_s,'span',span,'max avg gamma',round(math.log(1/eta_s)/math.log(span),3))
# laminar-friction Cd drift: Re ~ m^(1/2), Cd ~ Re^-1/2 -> drag frac ~ m^-1/4
for m in (39e-6,8.5e-6):
    d=0.065*(m/m0)**-0.25; print('drag frac at',m*1e6,'mg',round(d,3))
# m* with drag drift included (solve numerically, w=53, beta=1/3)
def R(m,b=1/3): 
    ke=0.5*4.37**2*(m/m0)**(b); d=0.065*(m/m0)**-0.25
    return 5.47/(ke*(1+d)/0.935/ (0.5*4.37**2*1.0/ (10.17*0.935/ (0.5*4.37**2)) ) )
# simpler: need(m)=10.17*(m/m0)^b*(1+d(m))/(1+0.065)
f=lambda m: 5.47/(10.17*(m/m0)**(1/3)*(1+0.065*(m/m0)**-0.25)/1.065)-1
lo,hi=1e-9,m0
for _ in range(200):
    mid=math.sqrt(lo*hi)
    (lo,hi)=(mid,hi) if f(mid)>0 else (lo,mid)
print('m* with laminar Cd drift', lo*1e6,'mg')
# surface energy per kg to break surface ~ sigma/(rho L)
for L in (0.016,0.0076,0.001): print('surface J/kg at L',L, 0.072/(1000*L))
# high eta_h counterexample: w=81, eta 0.8 at 1 g
print('R at 1 g, w=81, eta 0.8:', 0.822*(0.8/0.37)*(1e-3/m0)**(-1/3))
print('R at 1 g, w=53, eta 1.0:', 0.538*(1/0.37)*(1e-3/m0)**(-1/3))
