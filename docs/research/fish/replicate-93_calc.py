import math
g=9.81; m=0.10; L=0.12; N=14; c=0.10
P=m*g/(2*N); EIreq=P*L**2/(8*c)
print(f"P={P:.5f} N  EIreq={EIreq:.4e}")
k=1.98; Lb=0.0403
for lab,a in [("tip",Lb),("2/3",2/3*Lb)]:
    EI=k*a**3/3; r=EIreq/EI; beta=math.log(r)/math.log(L/Lb)
    print(lab,f"EI_bluegill={EI:.3e} shortfall(beta0)={r:.1f}x beta_flip={beta:.2f} EI_beta4={EI*(L/Lb)**4:.3e} margin4={EI*(L/Lb)**4/EIreq:.2f}")
s4=(L/Lb)**4; print(f"scale^4={s4:.1f}")
for EI in [1e-6,1e-5,3.8e-6,565e-6]:
    print(f"EI={EI:.2e} dL(beta0)={P*L**2/(8*EI):.3f} ratio={EI/EIreq:.3f} beta4 ratio={EI*s4/EIreq:.3f} beta_flip={math.log(EIreq/EI)/math.log(L/Lb) if EI<EIreq else float('nan'):.2f}")
