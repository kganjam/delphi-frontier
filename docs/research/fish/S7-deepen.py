"""S7-D: sensitivity sweep and recomputation. All outputs are CALCULATED, not observed."""
# --- part 1: factor-of-two sensitivity sweep (sens.py) ---
import math
g=9.81;rho=1.2
def run(m=0.4e-3,CL=0.78,V=3,AR=9,hw=2.5e-3,n=3,sig=25e6,r=0.5e-3,mus=200e3):
    W=m*g;S=2*W/(rho*V*V*CL);b=math.sqrt(AR*S);s=b/2-hw;yb=4/(3*math.pi)*s
    M=n*W/2*yb;Z=M/sig;d=(32*Z/math.pi)**(1/3);F=M/r
    return dict(M=M,d=d*1e3,F_W=F/W,pcsa=F/mus*1e6,s=s*1e3)
base=run();print("base",{k:round(v,6) for k,v in base.items()})
for k,v in dict(V=3,CL=0.78,AR=9,n=3,sig=25e6,r=0.5e-3,mus=200e3,hw=2.5e-3).items():
  for f in (0.5,2):
    o=run(**{k:v*f}); print(f"{k} x{f}: M x{o['M']/base['M']:.2f}  d x{o['d']/base['d']:.2f} (d={o['d']:.3f}mm)  F/W={o['F_W']:.0f}  pcsa={o['pcsa']:.2f}")

# --- part 2: recomputation with measured fish-bone yield stress (deepen.py) ---
import math
g=9.81;rho=1.2;W=0.4e-3*g
def M(V,n,CL=0.78,AR=9,hw=2.5e-3):
    S=2*W/(rho*V*V*CL);b=math.sqrt(AR*S);s=b/2-hw;return n*W/2*4/(3*math.pi)*s
cases=[(3,1),(3,3),(5,1),(5,3)]
print("M per fin:",{c:f"{M(*c):.3e}" for c in cases})
# old bracket vs measured herring IB yield (62.6 large, 66.8 small; lower 1-SD 49.4, 43.4)
for sig in (25e6,43.4e6,62.6e6,66.8e6,114e6):
    print(f"sig={sig/1e6:5.1f} MPa  d_req(mm):",[round((32*M(*c)/(math.pi*sig))**(1/3)*1e3,3) for c in cases])
# old construction E*0.005 using herring E
for E in (2.6e9,3.5e9): print(f"E={E/1e9} GPa x0.5% -> {E*0.005/1e6:.1f} MPa (measured yield ~63-67)")
# plate model: Z=t h^2/6 ; required t for depth h at worst case, sig=62.6, SF 1.5
Mw=M(3,3)
for sig in (43.4e6,62.6e6):
  for h in (0.25e-3,0.5e-3,1e-3,2e-3):
    t=6*Mw*1.5/(sig*h*h); print(f"sig={sig/1e6} h={h*1e3}mm -> t_req={t*1e6:.0f} um (SF1.5)")
# sensitivity to actual section: stress ratio if linear dimension halves
print("halving a solid section's linear size multiplies stress by", 2**3)
