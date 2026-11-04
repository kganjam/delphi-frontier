"""S23-D-D: attack the caudal->pectoral proxy in S23-D's EI_meas.

Everything printed here is COMPUTATION, not observation.
Run: python3 docs/research/fish/S23-D-D-calc.py
"""
g = 9.81; m = 0.4e-3; W = m*g

def EIreq(L, tol):
    """Uniform-load cantilever, tip deflection = tol*L, two wings share weight."""
    return (W/2)*L**2/(8*tol)

# --- inputs carried unchanged from S23 / S23-D -------------------------------
EI_caud = {'Puri abstract low': 1.5e-9, 'Puri abstract high': 4e-9,
           'Puri conclusions high': 5e-9}          # measured, CAUDAL fin
C_vals  = {'dry-collagen target (5 GPa / 0.35 GPa)': 14,
           'silk-like target (10 GPa / 0.35 GPa)': 29}   # S23-D improved ceiling, f=1

CENTRAL = dict(L=0.04, tol=0.10, EIc=4e-9)
LENIENT = dict(L=0.02, tol=0.50, EIc=5e-9)

print("=== 0. Required EI (computed) ===")
for nm, c in (('central', CENTRAL), ('lenient', LENIENT)):
    print(f"  {nm:8s} L={c['L']*100:.0f}cm tol={c['tol']:.0%} -> EIreq={EIreq(c['L'],c['tol']):.4g} N*m^2")

print("\n=== 1. S23-D reproduced (R=1, i.e. caudal used as the wing) ===")
for nm, c in (('central', CENTRAL), ('lenient', LENIENT)):
    S = EIreq(c['L'], c['tol'])/c['EIc']
    for cn, C in C_vals.items():
        print(f"  {nm:8s} S={S:8.1f}  C={C:3d} ({cn:42s}) margin={S/C:8.3f}  {'FLIPS' if S/C<1 else 'holds'}")

print("\n=== 2. Flip threshold on the proxy ratio R = EI_pectoral / EI_caudal ===")
print("    margin = EIreq/(R*EI_caud*C) < 1  <=>  R > EIreq/(C*EI_caud)")
Rstar = {}
for nm, c in (('central', CENTRAL), ('lenient', LENIENT)):
    for cn, C in C_vals.items():
        R = EIreq(c['L'], c['tol'])/(C*c['EIc'])
        Rstar[(nm, C)] = R
        print(f"  {nm:8s} C={C:3d}  R* = {R:8.2f}")

print("\n=== 3. Independent estimate of the zebrafish pectoral fin, by isometric")
print("       scaling of MEASURED labrid pectoral ray EI (Taft et al. 2018 JEB) ===")
# measured per-ray EI, leading edge, uN*m^2 -> N*m^2 ; with mean body mass (g)
labrid = {
 'G. varius proximal LE': (0.8899e-6, 22.44),
 'G. varius middle LE':   (0.1588e-6, 22.44),
 'H. bivittatus proximal LE': (0.1671e-6, 22.03),
 'H. bivittatus middle LE':   (0.0676e-6, 22.03),
}
# isometry: EI ~ E*d^4, d ~ L_body, L ~ M^(1/3)  =>  EI ~ M^(4/3), E size-invariant
per_ray = {}
print("  per-ray EI scaled to a 0.4 g Danio by (m/M)^(4/3):")
for k, (EI, M) in labrid.items():
    s = (0.4/M)**(4/3)
    per_ray[k] = EI*s
    print(f"    {k:28s} {EI:.4g} N*m^2 @ {M:.2f} g  x{s:.3e} -> {EI*s:.4g} N*m^2")

print("\n  whole pectoral fin = N_rays * per-ray (Puri 2018 measured that rays dominate):")
whole = []
for N in (10, 12, 14):
    for k, v in per_ray.items():
        whole.append(v*N)
    print(f"    N={N:2d}: {min(per_ray.values())*N:.3g} .. {max(per_ray.values())*N:.3g} N*m^2")
lo, hi = min(whole), max(whole)
print(f"  overall scaled band: {lo:.3g} .. {hi:.3g} N*m^2")

print("\n=== 4. Implied proxy ratio R, and whether the conclusion survives ===")
Rlo = lo/max(EI_caud.values()); Rhi = hi/min(EI_caud.values())
print(f"  R = EI_pect(scaled) / EI_caud(measured)  spans {Rlo:.2f} .. {Rhi:.1f}")
for nm, c in (('central', CENTRAL), ('lenient', LENIENT)):
    for cn, C in C_vals.items():
        R = Rstar[(nm, C)]
        verdict = ('indeterminate: R* inside band' if Rlo <= R <= Rhi
                   else ('holds for whole band' if R > Rhi else 'FLIPS for whole band'))
        print(f"  {nm:8s} C={C:3d}  R*={R:7.2f}  -> {verdict}")

print("\n=== 5. Margin at the scaled band endpoints ===")
for nm, c in (('central', CENTRAL), ('lenient', LENIENT)):
    for cn, C in C_vals.items():
        for rn, R in (('R_lo', Rlo), ('R_hi', Rhi)):
            mg = EIreq(c['L'], c['tol'])/(R*c['EIc']*C)
            print(f"  {nm:8s} C={C:3d} {rn} R={R:6.2f} margin={mg:8.3f}  {'FLIPS' if mg<1 else 'holds'}")
