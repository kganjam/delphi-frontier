"""Independent re-derivation for claim 199 (S6 fin-ray load). Pure calculation, no observations."""
import math
g = 9.81
m = 0.4e-3                     # kg, as stated in the S6 question
W = m * g                      # N
F_fin = W / 2                  # N, two pectoral fins share the load (assumption)
EI_caudal = (1.5e-9, 4e-9)     # N m^2, Puri et al. 2018 whole caudal fin, 16-18 rays
rays_caudal = (16, 18)
rays_pect = 12                 # modal count, Hamada et al. 2019 Zool Lett (43/56 fins)
EI_ray = (EI_caudal[0]/rays_caudal[1], EI_caudal[1]/rays_caudal[0])
EI_pect = (EI_ray[0]*rays_pect, EI_ray[1]*rays_pect)
print(f"W = {W:.3e} N, per fin {F_fin:.3e} N")
print(f"EI per ray {EI_ray[0]:.2e}-{EI_ray[1]:.2e}; pectoral fin {EI_pect[0]:.2e}-{EI_pect[1]:.2e} N m^2")
for L_mm in (3, 5, 7):
    L = L_mm*1e-3
    # uniform load along span, cantilever: delta = F L^3 / (8 EI)
    d = [F_fin*L**3/(8*EI) for EI in (EI_pect[1], EI_pect[0], EI_caudal[1])]
    EI_need = F_fin*L**2/(8*0.1)   # EI for delta/L = 0.1
    M_ray = F_fin*L/2/rays_pect
    print(f"L={L_mm} mm: delta/L (pect hi, pect lo, whole-caudal-EI) = "
          + ", ".join(f"{x/L:.2f}" for x in d)
          + f"; EI needed for delta/L<=0.1: {EI_need:.2e} -> shortfall x{EI_need/EI_pect[1]:.0f}-{EI_need/EI_pect[0]:.0f}"
          + f"; root moment per ray {M_ray:.2e} N m")
    for dia in (0.1e-3, 0.15e-3, 0.2e-3):
        I = math.pi*dia**4/64
        print(f"   ray d={dia*1e3:.2f} mm solid-rod: sigma_root = {M_ray*(dia/2)/I/1e6:.1f} MPa, implied E from EI_ray = {EI_ray[0]/I/1e6:.1f}-{EI_ray[1]/I/1e6:.1f} MPa")
