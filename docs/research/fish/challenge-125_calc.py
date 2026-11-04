# challenge-125: independent refit of S9-D-D (claim 125) inputs. ALL OUTPUTS ARE CALCULATIONS, NOT OBSERVATIONS.
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2
E_APP = {  # author's plot readings (Puri 2018 Fig S5C), taken as given
 "fish13": [(2.0,6.45),(2.3,5.72),(2.8,7.22),(3.3,9.70),(3.8,10.35),(5.0,8.00)],
 "fish12": [(1.3,3.82),(1.7,5.65),(2.3,8.80),(3.0,9.60),(3.5,8.50),(5.0,7.07)],
 "fish5":  [(1.4,3.00),(2.1,5.72),(2.8,8.55),(3.6,10.00),(4.4,10.95),(5.4,9.85)],
 "fish4":  [(2.1,6.58),(2.8,7.65),(3.4,7.20),(4.1,7.38),(4.4,7.10),(4.5,7.00)],
 "fish11": [(1.7,1.88),(2.3,3.07),(2.9,4.05),(3.5,4.85),(4.25,4.70),(4.7,4.55)]}
IR=np.array([(1.0,.488),(1.5,.500),(2.0,.500),(2.5,.490),(3.0,.450),(3.5,.405),(4.0,.372),(4.5,.353),(5.0,.337)])
Iat=lambda L: np.interp(L,IR[:,0],IR[:,1])*1e-15
def rising(p):
    k=max(range(len(p)),key=lambda i:p[i][1]); return np.array(p[:k+1])
def sig(L,E,sL=0.1,rd=0.15):
    # Puri's stated SD: L +-0.1 mm (E_app ~ L^3 -> 3 sL/L), y +-20um (~1-2%), F +-5uN (negligible); plus reading error
    return np.sqrt((E*3*sL/L)**2+(E*0.02)**2+rd**2)
models={"const":lambda p,L:p[0]+0*L,
        "trans":lambda p,L:p[0]/(1+p[1]/L**3),
        "shear":lambda p,L:p[0]/(1+p[1]/L**2),
        "offset":lambda p,L:p[0]*(L/(L+p[1]))**3}
def fitm(m,L,E,s):
    f=models[m]; x0=[E.max()]+([] if m=="const" else [1.0])
    lb=[0]+([] if m=="const" else [0]); ub=[200]+([] if m=="const" else [100])
    r=least_squares(lambda p:(f(p,L)-E)/s,x0,bounds=(lb,ub))
    return r.x,np.sum(r.fun**2)
rng=np.random.default_rng(1)
print("fish  model  chi2  dof  p(chi2)   E_inf  [MC 16-84%]  EI_corr_max(1e-9) [16-84%]")
allhi={m:[] for m in models}
for f,p in E_APP.items():
    r=rising(p); L,E=r[:,0],r[:,1]; s=sig(L,E)
    for m in models:
        x,c=fitm(m,L,E,s); dof=len(L)-len(x)
        pv=1-chi2.cdf(c,dof) if dof>0 else float('nan')
        mc=[];ei=[]
        for _ in range(400):
            Ep=E+rng.normal(0,s); xx,_=fitm(m,L,Ep,s); mc.append(xx[0]); ei.append(xx[0]*1e6*Iat(np.array(p)[:,0]).max()*1e9)
        q=np.percentile(mc,[16,84]); qe=np.percentile(ei,[16,84])
        print(f"{f:7s}{m:7s}{c:6.2f} {dof:3d} {pv:7.3f} {x[0]:7.2f} [{q[0]:6.2f},{q[1]:7.2f}] {x[0]*1e6*Iat(np.array(p)[:,0]).max()*1e9:6.2f} [{qe[0]:5.2f},{qe[1]:6.2f}]  extra={x[1:] if len(x)>1 else ''}")

# ---- Section 2: corrected-EI range per model (author's definition: E_inf * I_rays(L) over measured spans) ----
print("\ncorrected whole-fin EI range per model  [calc]")
for m in ["trans", "shear", "offset"]:
    lo = []; hi = []
    for f, p in E_APP.items():
        r = rising(p); L, E = r[:, 0], r[:, 1]; x, _ = fitm(m, L, E, sig(L, E))
        ei = x[0] * 1e6 * Iat(np.array(p)[:, 0])
        lo.append((ei.min(), f)); hi.append((ei.max(), f))
    a, b = min(lo), max(hi)
    print(f"{m:7s} fin EI {a[0]:.2e} ({a[1]}) .. {b[0]:.2e} ({b[1]})")
    for t in (11e-6, 16.5e-6):
        Ifp = 2 * 150e-6 * t**3 / 12
        print(f"        t={t*1e6:.1f} um uncoupled flat-plate bound (EI/16 rays, w=150 um): E <= {b[0]/16/Ifp/1e9:.1f} GPa")
