import math
g=9.80665; W=0.4e-3*g; rho=1.204; AR=9; y0=2.5e-3
for CL in (0.78,1.03):
  for V in (3,5):
    S=2*W/(rho*V**2*CL); b=math.sqrt(AR*S); s=b/2-y0; yb=4*s/(3*math.pi)
    for n in (1,3):
      M=n*W/2*yb
      d=lambda sig:(32*M/(math.pi*sig))**(1/3)*1e3
      for r in (0.5e-3,1e-3):
        F=M/r/W; L=n/2
        print(f"CL={CL} V={V} n={n} r={r*1e3}mm s={s*1e3:.2f}mm M={M:.3e} d25={d(25e6):.3f} d114={d(114e6):.3f} Fm/W={F:.2f} class3(F-L)={F-L:.2f} class1(F+L)={F+L:.2f}")
