import math
g=9.81; m,N,L,lim=0.10,14,0.12,0.10
P=m*g/(2*N); EIreq=P*L**2/(8*lim); req=EIreq/L**4
print(f"P={P:.5f} N EIreq={EIreq:.4e} req_idx={req:.3f} Pa")
k=1.98
for Lt in (0.0403,0.035,0.030):
    a=2*Lt/3
    tip=k*a**2*(3*Lt-a)/6     # deflection read at tip
    lp=k*a**3/3               # deflection read at load point
    for nm,EIc in (("tip",tip),("loadpt",lp)):
        for st,EI in (("clamped",EIc),("onefree",EIc/12)):
            idx=EI/Lt**4
            print(f"Lt={Lt*1e3:.1f}mm {nm:6s} {st:8s} EI={EI:.3e} idx={idx:.3f} R_iso={req/idx:.2f}")
for EI in (1e-6,10**-5.5,1e-5):
    idx=EI/0.0403**4; print(f"3pt EI={EI:.2e} idx={idx:.3f} R_iso={req/idx:.2f}  (at L=40mm typical: {req/(EI/0.04**4):.2f})")
