"""Claim 95 entailment checks. CALCULATION ONLY -- nothing here is an observation.
Run: python3 -I claim-95-entail_calc.py
Inputs tagged: [reported] by cited authors; [assumption] mine or S6-D's, unsourced."""
g = 9.81
EI_bg = 3.8e-6       # [reported] bluegill ray EI as stated by Puri et al. 2018 (full text); origin untraced (S25)
L_bg, L_t = 40.3, 120.0   # mm; 40.3 = Alben 2007 max bluegill ray length [reported, relayed]; 120 = S6-D [assumption]
EI_req = 6.31e-4     # S6-D: s*m*g*L^2/(16 N c), m=0.10 kg, N=14, c=0.10, s=1 [assumptions]

lam = L_t / L_bg
print(f"[0] lambda={lam:.3f}  lambda^4={lam**4:.1f}  scaled EI={EI_bg*lam**4:.2e}  gap={EI_req/(EI_bg*lam**4):.2f}x  unscaled gap={EI_req/EI_bg:.0f}x")

# C1/C2: tolerance. Gap = 2.11 * (E_s/E_t) * (d_iso/d_t)^4. Keep the gap within x2 of 2.11:
print(f"[C1] E_t/E_s window for gap within x2: [0.5, 2]")
lo, hi = lam * 2**-0.25, lam * 2**0.25
print(f"[C2] diameter ratio window: [{lo:.2f}, {hi:.2f}]; with bluegill d=1-2 mm [reported, Puri 2018] -> 120 mm ray base d in [{1*lo:.1f}, {2*hi:.1f}] mm")
# beta at which the 'gap' is 1x (passes) and 165x (fails as originally reported)
import math
print(f"[C2] beta giving gap=1: {math.log(EI_req/EI_bg)/math.log(lam):.2f}; gap=165x is beta=0")

# C3: Fish 1990 Table I wing span = a M^b (m, kg) [reported regressions, measured specimens]; M = 0.10 kg
span = {"Cypselurus": (0.651, 0.375), "Danichthyes": (0.622, 0.310), "Exocoetus": (0.774, 0.380),
        "Fodiator": (0.476, 0.332), "Hirundichthyes": (0.566, 0.303), "Parexocoetus": (0.573, 0.353)}
Lwin = (L_t * 2**-0.25, L_t * 2**0.25)
print(f"[C3] L window for 78.6-factor within x2 in EI: [{Lwin[0]:.0f}, {Lwin[1]:.0f}] mm")
for gname, (a, b) in span.items():
    S = a * 0.10**b
    semi = [(S - w) / 2 * 1e3 for w in (0.025, 0.015)]   # body width 15-25 mm [assumption]
    print(f"     {gname:15s} span(0.1 kg)={S*1e3:5.0f} mm  base-to-tip={semi[0]:4.0f}-{semi[1]:4.0f} mm")

# C4: pectoral share of wing area, Fish 1990 Table III [reported]; lift share = area share [assumption]
share = {"Cypselurus": 0.7599, "Danichthyes": 0.774, "Hirundichthyes": 0.766, "Parexocoetus": 0.8154, "Exocoetus": 0.9183}
for gname, s in share.items():
    print(f"[C4] {gname:15s} s={s:.3f}  EI_req={EI_req*s:.2e}  gap={EI_req*s/(EI_bg*lam**4):.2f}x")
print(f"[C4] s at which gap reaches 1x: {(EI_bg*lam**4)/EI_req:.2f}")
wl = {"Cypselurus": (285.015, 0.400), "Exocoetus": (300.101, 0.360), "Hirundichthyes": (390.069, 0.526)}
for gname, (a, b) in wl.items():
    print(f"[C4] wing loading at 0.1 kg, {gname}: {a*0.1**b:.0f} N/m^2  (vs m g = {0.1*g:.3f} N)")
# ray count sensitivity
for N in (14, 17, 19):
    print(f"[C4] N={N}: gap={EI_req*14/N/(EI_bg*lam**4):.2f}x (s=1)")

# C5: factor an extra mechanism must supply
print(f"[C5] required extra stiffening: {0.76*EI_req/(EI_bg*lam**4):.2f}-{EI_req/(EI_bg*lam**4):.2f}x; Alben bluegill locking ~12x [reported, n=1, relayed]")
# Aiello 2018 labrids: proximal leading-edge EI means [reported]
print(f"[C2-x] Aiello 2018: G. varius / H. bivittatus proximal LE EI ratio = {0.8899/0.1671:.1f}x at mean mass 22.4 vs 22.0 g")
