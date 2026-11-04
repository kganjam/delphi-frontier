"""S6 fin-ray load check. COMPUTATION, not observation. Inputs and provenance in S6-organ.md."""
import math
g, rho_air = 9.81, 1.2
m = 0.4e-3                      # body mass, kg (project brief)
W = m * g                       # N
# Measured (Puri et al. 2018, JEB 221:jeb171777): whole caudal fin EI 1.5e-9..4e-9 N m^2, width 5..8 mm
D_lo, D_hi = 1.5e-9 / 8e-3, 4e-9 / 5e-3   # flexural rigidity per unit width, N m
mu = 1100 * 100e-6              # ASSUMED areal density: tissue 1100 kg/m^3 x 100 um mean thickness
CL = 1.0                        # ASSUMED glide lift coefficient
tol = 0.10                      # ASSUMED aerodynamic tolerance on tip deflection, delta/L
print(f"W = {W:.3e} N ; D_w measured-derived range = {D_lo:.2e} .. {D_hi:.2e} N m")
for L in (3e-3, 5e-3, 10e-3, 15e-3):          # square fin-wing, span L = chord c, two wings
    c = L; S = 2 * L * c; p = W / S
    V = math.sqrt(2 * W / (rho_air * S * CL))
    dl = [p * L**3 / (8 * D) for D in (D_lo, D_hi)]
    Dreq = p * L**3 / (8 * tol)
    sag = [mu * g * L**3 / (8 * D) for D in (D_lo, D_hi)]
    f1 = [(1.875**2 / (2 * math.pi)) * math.sqrt(D / (mu * L**4)) for D in (D_lo, D_hi)]
    Uk = [math.pi * f * c / 0.1 for f in f1]
    print(f"L=c={L*1e3:4.0f} mm  S={S*1e6:6.1f} mm2  p={p:6.1f} Pa  V_glide={V:5.1f} m/s  "
          f"delta/L={dl[0]:6.2f}..{dl[1]:5.2f}  D_req={Dreq:.2e}  shortfall x{Dreq/D_hi:5.1f}..{Dreq/D_lo:5.1f}  "
          f"self-sag delta/L={sag[0]:.2f}..{sag[1]:.2f}  f1={f1[0]:5.1f}..{f1[1]:5.1f} Hz  U(k=0.1)={Uk[0]:4.1f}..{Uk[1]:4.1f} m/s")
# Per-ray cross-checks
n_rays = 16                                           # Puri: 16-18 caudal rays
print("per-ray EI from fin (measured/n):", 1.5e-9/18, "..", 4e-9/16)
for d in (0.1e-3, 0.15e-3, 0.2e-3):
    I = math.pi * d**4 / 64
    print(f"d={d*1e6:.0f}um solid-section EI @E=4.57GPa {4.57e9*I:.2e}, @E=8.68GPa {8.68e9*I:.2e}, @E=1e8 {1e8*I:.2e}, @E=1e9 {1e9*I:.2e}")
for t in (10e-6, 15e-6, 20e-6):
    w = 150e-6
    print(f"decoupled 2 hemirays t={t*1e6:.0f}um w=150um, E=4.57..8.68GPa: EI={2*4.57e9*w*t**3/12:.2e}..{2*8.68e9*w*t**3/12:.2e}")
# Required D for L=c=10 mm, converted to per-ray EI at 12 rays across 10 mm
L = 10e-3; Dreq = (W/(2*L*L)) * L**3 / (8*tol)
print("L=10mm D_req", Dreq, "-> per-ray EI at 12 rays/10mm:", Dreq*L/12)
