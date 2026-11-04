# ALL VALUES COMPUTED BY ME. Nothing here is an observation.
import math
# --- A. integer residue counts from AFDB bin fractions (3 dp) ---
def ints(fr,N):
    out=[]
    for f in fr:
        c=[n for n in range(N+1) if round(n/N,3)==f]
        out.append(c)
    return out
for acc,N,fr in (("E7F5V5",570,(0.416,0.309,0.223,0.053)),("A9JRX1",508,(0.459,0.274,0.264,0.004))):
    sols=ints(fr,N)
    uniq=[s[0] if len(s)==1 else s for s in sols]
    print(acc,"N=",N,"unique integer solutions per bin:",uniq,"sum=",sum(s[0] for s in sols))
    g70=sols[2][0]+sols[3][0]
    print("   >70 count = %d  -> %.2f%% (claim says %s)"%(g70,100*g70/N,"27.6%" if acc=="E7F5V5" else "26.8%"))
    print("   mature-chain window (signal 1-26 removed, N=%d): %.1f%%-%.1f%%"%(N-26,100*max(0,g70-26)/(N-26),100*g70/(N-26)) if acc=="E7F5V5" else "")
# --- B. EI_req, redone from first principles ---
g=9.81; m=0.4e-3; W=m*g; b2=0.02
print("\nW = %.4e N ; w = %.4e N/m"%(W,(W/2)/b2))
def EI(frac,b2=b2,W=W):
    w=(W/2)/b2; d=frac*b2
    return w*b2**4/(8*d)
print("EI_req(10%%) = %.3e  (closed form W*(b/2)^2/(16*frac) = %.3e)"%(EI(0.10), W*b2**2/(16*0.10)))
for f in (0.10,0.20,0.40,0.80):
    e=EI(f); print("  frac=%.0f%%: EI=%.3e  gap/4e-9=%.0fx  gap/1.5e-9=%.0fx  E_req@1GPa=%.0f GPa"%(100*f,e,e/4e-9,e/1.5e-9,e/4e-9))
# --- C. joint factor-of-two: span is the other free parameter (EI_req ~ (b/2)^2) ---
print("\nJoint relaxation (deflection 20% AND semi-span halved to 1 cm):")
e=EI(0.20,b2=0.01); print("  EI=%.3e gap/4e-9=%.0fx -> E_req@1GPa=%.0f GPa"%(e,e/4e-9,e/4e-9))
# --- D. what baseline modulus does the MEASURED dataset itself imply? ---
I_ray=lambda d: math.pi*d**4/64
for d in (1.0e-4,1.5e-4,2.0e-4):
    for n in (16,18):
        Isum=n*I_ray(d)
        print("  %d rays of d=%.2f mm: sum I = %.2e m^4 ; E_ray from EI 1.5-4e-9 = %.1f-%.1f MPa"%(n,d*1e3,Isum,1.5e-9/Isum/1e6,4e-9/Isum/1e6))
print("\nRequired ray E at 20%% deflection (123x) for each baseline:")
for name,E0 in (("~1 GPa whole-ray proxy (other teleosts, search-summary)",1.0),("10 MPa (parent's own alternative)",0.010),("4-10 MPa (my calc from measured EI + ray geometry)",0.004)):
    print("   %-58s -> %.2f GPa"%(name,123*E0))
