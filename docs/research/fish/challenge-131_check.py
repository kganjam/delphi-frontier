# Independent re-derivation: brute-force minimum of total drag over airspeed V.
# Inputs are those stated in S2-D-D (rho, nu, m, S, e, body ellipsoid, form 1.5, median fins 2 cm^2,
# CD0w = lam * 2*1.328/sqrt(Re_c), CL <= cap). Everything printed is COMPUTED.
import math
rho,nu,g=1.2,1.5e-5,9.81
def lift_to_drag(AR,S,lam=1.4,e=0.7,m=0.4e-3,cap=0.9,body_scale=1.0,SL=0.032):
    W=m*g; b=math.sqrt(AR*S); c=S/b
    # body: prolate-ish ellipsoid 32x7x4 mm; wetted ~ 0.75*perimeter*length (S2-D's approximation)
    a,bb=0.0035,0.002
    P=math.pi*(3*(a+bb)-math.sqrt((3*a+bb)*(a+3*bb)))
    wet=0.75*P*0.032
    best=None
    V=0.5
    while V<40:
        q=0.5*rho*V*V
        CL=W/(q*S)
        if CL<=cap:
            cd0w=lam*2.656/math.sqrt(V*c/nu)
            cdab=body_scale*(1.5*1.328/math.sqrt(V*0.032/nu)*wet + 2.656/math.sqrt(V*0.01/nu)*2e-4)
            Di=W*W/(q*math.pi*e*b*b)
            D=q*cd0w*S+q*cdab+Di
            Dw=q*cd0w*S+Di
            if best is None or D<best[0]: best=(D,W/D,W/Dw,CL,V,b)
        V+=0.002
    return best
print("labrid-range recompute, S=9cm2")
for ar in (1.82,2.76,3.80,4.0,4.16,9.0,10.7):
    r14=lift_to_drag(ar,9e-4,1.4); r20=lift_to_drag(ar,9e-4,2.0)
    print(f"AR {ar:5.2f}: whole L/D lam1.4 {r14[1]:.2f} (wing {r14[2]:.2f}, CL {r14[3]:.2f}, V {r14[4]:.2f}); lam2.0 {r20[1]:.2f}")
print("\ncorner cases of the stated input ranges")
for ar in (1.82,4.16):
    for lam in (1.4,2.0):
        for e in (0.5,0.7,0.9):
            print(f" AR {ar} lam {lam} e {e}: {lift_to_drag(ar,9e-4,lam,e)[1]:.2f}")
print("\nspan per fin needed (b-4mm)/2/SL at S=9cm2")
for ar in (1.82,4.0,9.0,10.7):
    b=math.sqrt(ar*9e-4); print(f" AR {ar}: {(b-0.004)/2/0.032:.2f} SL")
def fixed_span(per_fin,ar,**kw):
    b=2*per_fin*0.032+0.004; S=b*b/ar; return lift_to_drag(ar,S,**kw),S
print("\nfixed span 0.70 SL/fin, sweep AR (lam1.4,e0.7,cap0.9)")
for ar in (2,3,4,5,6,7,8,9,12):
    r,S=fixed_span(0.70,ar); print(f" AR {ar}: S {S*1e4:.2f} cm2 L/D {r[1]:.2f} CL {r[3]:.2f} V {r[4]:.2f}")
def peak(per_fin,**kw):
    best=max(((r[0][1],ar/4) for ar in range(4,60) for r in [fixed_span(per_fin,ar/4,**kw)] if r[0]))
    return best
print("\nrelax hidden assumptions: peak L/D over AR 1.5-15 at fixed span")
for lab,kw,pf in [("base 0.70SL",{},0.70),("0.77SL",{},0.77),("0.65SL",{},0.65),
                  ("cap 1.07",{"cap":1.07},0.70),("cap 1.5",{"cap":1.5},0.70),("no cap",{"cap":99},0.70),
                  ("e 0.9",{"e":0.9},0.70),("e 0.5",{"e":0.5},0.70),("lam 2.0",{"lam":2.0},0.70),
                  ("body drag x0.5",{"body_scale":0.5},0.70),("body drag x2",{"body_scale":2},0.70),
                  ("mass 0.25 g",{"m":0.25e-3},0.70),("mass 0.55 g",{"m":0.55e-3},0.70),
                  ("S2 span 0.87SL",{},0.87),("WT 0.21SL",{},0.21),("alf 0.40SL",{},0.40)]:
    p=peak(pf,**kw); print(f" {lab:16s}: peak L/D {p[0]:.2f} at AR {p[1]:.2f}")
print("\nreachable zebrafish spans (S22-D-D inference 0.36-0.43 SL), peak over AR, with S unconstrained by 9 cm2")
for pf in (0.21,0.36,0.43):
    for lam in (1.4,2.0):
        p=peak(pf,lam=lam); r,S=fixed_span(pf,p[1],lam=lam)
        print(f" {pf} SL lam {lam}: peak L/D {p[0]:.2f} at AR {p[1]:.2f}, S {S*1e4:.2f} cm2, V {r[4]:.2f} m/s")
