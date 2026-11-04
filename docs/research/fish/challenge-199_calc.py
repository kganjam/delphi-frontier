W=0.4e-3*9.81; Dlo=1.5e-9/8e-3; Dhi=4e-9/5e-3; tol=0.1
def Dreq(L,c): # uniform p=W/(2Lc), cantilever along span L, delta/L=pL^3/(8D)
    p=W/(2*L*c); return p*L**3/(8*tol)
import math
for L,c in [(3e-3,3e-3),(15e-3,15e-3),(3e-3,10e-3),(3e-3,15e-3),(3e-3,20e-3),(3e-3,30e-3),(5e-3,30e-3)]:
    d=Dreq(L,c); S=2*L*c; V=math.sqrt(2*W/(1.2*S))
    print(f"L={L*1e3:.0f} c={c*1e3:.0f} p={W/S:6.1f} Dreq={d:.2e} ratio_vs_hi={d/Dhi:.2f} vs_lo={d/Dlo:.2f} V(CL=1)={V:.1f}")
print(Dlo,Dhi)
# load-shape relaxation: linearly decreasing load, same total: delta = q0 L^4/(30D) with q0=2qbar -> factor
print("triangular/uniform", (2/30)/(1/8))
