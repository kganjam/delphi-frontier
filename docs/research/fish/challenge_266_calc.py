"""challenge-266: independent recomputation of S26-D-D. All outputs CALCULATED. Run: python3 -I <this file>"""
from math import log
EI_REQ, F_A, L_REQ, L_BG = 6.3e-4, 12.0, 0.120, 0.0403
# EI_req re-derived: 0.10 kg, 2 wings, 14 rays/wing, uniform load cantilever, delta/L = 0.10
W = 0.10*9.81/2/14
print(f"EI_req check: W/ray {W:.4f} N -> EI = W L^2/(8*0.1) = {W*L_REQ**2/0.8:.3e}")
S = (L_REQ/L_BG)**4
print(f"size factor (120/40.3)^4 = {S:.2f}")
for lab, src in (("relay 3.8e-6", 3.8e-6), ("primary 1.07e-6", 1.07e-6)):
    need = EI_REQ/(src*S); m = F_A/need
    print(f"{lab}: need {need:.2f}x margin {m:.3f}; m/2 {m/2:.3f}; m/16 {m/16:.3f}; m/8 (d^3 t, t fixed) {m/8:.3f}")
    print(f"   break-even d ratio (d^4) {(1/m)**0.25:.3f}; (d^3) {(1/m)**(1/3):.3f}; n_be {4-log(m)/log(L_REQ/L_BG):.2f}")
# Aiello 2017: pairs (mm, %) per phenotype
for lab, pairs, eis in (("high-AR", [(1.05,5.91),(1.50,8.20)], (1.9e-7,2.1e-7)),
                        ("low-AR", [(3.6,17.84),(6.12,30.67)], (2e-8,4e-8))):
    Ls = [mm/(p/100) for mm,p in pairs]
    print(f"{lab}: implied ray-3 lengths {', '.join(f'{x:.2f}' for x in Ls)} mm")
    needs = [EI_REQ/(ei*(L_REQ/(L/1e3))**4) for ei in eis for L in Ls]
    print(f"   phenotype-own lengths: need {min(needs):.2f}-{max(needs):.2f}x")
