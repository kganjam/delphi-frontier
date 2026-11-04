import math
g=9.80665; m=0.4e-3; W=m*g; rho=1.204; AR=9; y0=2.5e-3
def run(CL,rho=rho):
  out=[]
  for V in (3,5):
    S=2*W/(rho*V*V*CL); b=math.sqrt(AR*S); s=b/2-y0
    for n in (1,3):
      # A: fin carries nW/2, elliptic over fin length -> centroid 4s/3pi
      MA=n*W/2*4*s/(3*math.pi)
      # B: elliptic over full span, moment about y0 (closed form via numeric)
      N=200000; L0=4*W/(math.pi*b); h=(b/2-y0)/N; MB=0
      for i in range(N):
        y=y0+(i+.5)*h; MB+=L0*math.sqrt(max(0,1-(2*y/b)**2))*(y-y0)*h
      MB*=n
      # C: uniform lift over fin length (upper-bound centroid s/2)
      MC=n*W/2*s/2
      out.append((V,n,S*1e4,b*1e3,s*1e3,MA,MB,MC))
  return out
for CL in (0.78,1.03):
  print("CL",CL)
  for V,n,S,b,s,MA,MB,MC in run(CL):
    print(f" V={V} n={n} S={S:.3f}cm2 b={b:.2f}mm s={s:.2f}mm MA={MA:.3e} MB={MB:.3e} MC={MC:.3e}")
    for r in (0.5e-3,1e-3):
      F=MA/r; print(f"   r={r*1e3}mm F_A={F*1e3:.1f}mN ={F/W:.1f}W PCSA={F/200e3*1e6:.2f}mm2  F_B={MB/r/W:.1f}W F_C={MC/r/W:.1f}W")
def d(M,s): return (32*M/(math.pi*s))**(1/3)*1e3
r=run(0.78); Ms=[x[5] for x in r]
print("d range A:", d(min(Ms),114e6), d(max(Ms),25e6))
