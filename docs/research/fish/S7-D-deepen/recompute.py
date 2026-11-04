"""S7-D-D recomputation. Every number printed is CALCULATED."""
import json, math
g=9.81; rho=1.2; W=0.4e-3*g
def M(V,n,CL=0.78,AR=9,hw=2.5e-3):
    S=2*W/(rho*V*V*CL); b=math.sqrt(AR*S); s=b/2-hw; return n*W/2*4/(3*math.pi)*s
Mw=M(3,3)
req={}
for sig,lab in ((25e6,"S7 floor 25 MPa"),(62.6e6,"S7-D herring mean 62.6 MPa"),(43.4e6,"S7-D lower 1-SD 43.4 MPa")):
    for sf in (1.0,1.5):
        req[f"{lab}, SF {sf}"]=Mw*sf/sig*1e9   # mm^3
print(f"worst-case root moment M = {Mw:.3e} N m")
for k,v in req.items(): print(f"  Z_req {k}: {v:.2e} mm^3  (solid rod d = {(32*v/math.pi)**(1/3):.3f} mm)")
for lab,f in (("SL24","sweep_SL24.json"),("SL20","sweep_SL20.json")):
    rows=json.load(open(f))
    for hw in (15,30):
        R=[r for r in rows if r['hw']==hw]
        mn_sum=min(R,key=lambda r:r['sumZ']); mn_max=min(R,key=lambda r:r['maxZ'])
        print(f"{lab} hw{hw}: min plane-sum Z {mn_sum['sumZ']:.2e} (y={mn_sum['y']:.0f}); min largest-component Z {mn_max['maxZ']:.2e} (y={mn_max['y']:.0f}); median largest-comp Z {sorted(r['maxZ'] for r in R)[len(R)//2]:.2e}")
        for key in ("S7-D herring mean 62.6 MPa, SF 1.0","S7-D lower 1-SD 43.4 MPa, SF 1.5","S7 floor 25 MPa, SF 1.0"):
            print(f"     ratio to {key}: sum {mn_sum['sumZ']/req[key]:.2f}x, largest-comp {mn_max['maxZ']/req[key]:.2f}x")
# isometric scaling of measured fish to the 40 mm design body (two readings of '40 mm')
for lab,SL,TL in (("SL24",24,30.9),("SL20",20,23.5)):
    print(f"{lab}: Z scale-up to 40 mm if 40 mm is TL: x{(40/TL)**3:.2f}; if SL: x{(40/SL)**3:.2f}")
# linear-size margin = (Z ratio)^(1/3)
for r in (1.6,3.9,6.4,8.7): print(f"Z margin {r}x = linear-size margin {r**(1/3):.2f}x")
