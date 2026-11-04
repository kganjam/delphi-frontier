# ALL COMPUTED, nothing observed. Inputs taken from the claim + parent S13-protein.md.
g=9.81; m=0.4e-3; W=m*g; b2=0.02
EIreq=lambda f: W*b2**2/(16*f)
print("EI_req: 10%%=%.3e  20%%=%.3e N m^2"%(EIreq .__call__(0.10),EIreq(0.20)))
for EI,lab in ((4e-9,"4e-9 (stiff end)"),(2.75e-9,"2.75e-9 (parent midpoint)"),(1.5e-9,"1.5e-9 (soft end)")):
    print("  ratio@10%%=%6.1f  ratio@20%%=%6.1f   EI=%s"%(EIreq(0.10)/EI,EIreq(0.20)/EI,lab))
print()
print("Required MATERIAL modulus = ratio x baseline modulus. Baselines are from parent S13-protein.md 3.5.")
print("%-42s %12s %12s"%("baseline E (unmeasured proxy)","@10% defl","@20% defl"))
for Eb,lab in ((0.005,"homogenised fin plate 5 MPa"),(0.3,"hydrated collagen fibril 0.3 GPa"),
               (1.0,"teleost whole-ray ~1.0 GPa (claim's)"),(0.11,"whole-ray distal low 0.11 GPa"),
               (3.7,"whole-ray proximal high 3.7 GPa")):
    r10,r20=EIreq(0.10)/4e-9,EIreq(0.20)/4e-9
    print("%-42s %9.1f GPa %9.1f GPa"%(lab,r10*Eb,r20*Eb))
print()
print("Baseline modulus at which the 20%-deflection requirement MEETS the ceiling (ratio 122.6):")
for ceil in (30,10):
    print("   requirement = %2d GPa  <->  baseline E = %.3f GPa (%.0f MPa)"%(ceil,ceil/122.6,1000*ceil/122.6))
print("   -> i.e. only a %.1fx reduction from the claim's 1.0 GPa baseline reaches the 30 GPa ceiling top."%(1.0/(30/122.6)))
print("   parent's own cited whole-ray range is 0.11-3.7 GPa, which brackets that value.")
