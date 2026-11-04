"""S9-D sensitivity calculation. Every output of this script is a CALCULATION, not an observation.

Inputs and their read-levels:
  EI_fin      1.5e-9 .. 4e-9 N m^2   whole caudal fin, in vivo      Puri et al. 2018 JEB 221:jeb171777, full-text
  N_rays      16 .. 18                caudal fin rays                Puri et al. 2018, full-text
  D_ray       100 .. 200 um           ray diameter (fin 200->40 um)  Puri et al. 2018, full-text
  E_puri      ~1.9 .. ~11 MPa         ray-only effective modulus     Puri et al. 2018 Fig. S5C, full-text (read off plot)
  I_puri      ~0.28 .. 0.50e-15 m^4   summed ray I                   Puri et al. 2018 Fig. S5B, full-text (read off plot)
  t_hemi      ~11 .. ~16.5 um         WT hemiray wall thickness      hox13 PLoS Genet 2026, PMC12956070 Fig 7E,
                                                                     full-text (bar heights read off plot, +-1 um; DORSAL fin)
  E_bone      ~23 .. 25 GPa           zebrafish vertebra nanoindent. S9-tissue B3/B4, search-summary only
  E_bluegill  1.34 GPa (0.24..3.7)    bluegill proximal ray          S9-tissue L1, search-summary only
"""
from math import pi, sin, cos

EI_FIN = (1.5e-9, 4e-9)
N = (16, 18)
EI_RAY = (EI_FIN[0] / N[1], EI_FIN[1] / N[0])  # widest per-ray range
print(f"per-ray EI (calc) = {EI_RAY[0]:.2e} .. {EI_RAY[1]:.2e} N m^2")


def I_solid_rod(D):
    return pi * D**4 / 64


def I_coupled_tube(D, t):
    # two hemitrichs rigidly bonded -> behaves like a hollow tube
    Ro, Ri = D / 2, D / 2 - t
    return pi / 4 * (Ro**4 - Ri**4)


def I_flat_pair(w, t):
    # two hemitrichs bending independently as flat plates (no shear transfer through core)
    return 2 * w * t**3 / 12


def I_arc_pair(R, t, half_angle):
    # two hemitrichs bending independently, each a thin circular arc (crescent) of mid-radius R,
    # thickness t, half-angle a, bowed out of the fin plane. I about own centroidal axis
    # parallel to the fin plane: thin-arc formula + the plate's own t^3 term.
    a = half_angle
    A = 2 * a * R * t
    # coordinate y measured out of the fin plane, y = R cos(theta), theta in [-a, a]
    Iy0 = R**3 * t * (a + sin(a) * cos(a))       # integral of y^2 dA
    ybar = R * sin(a) / a
    I_own = Iy0 - A * ybar**2
    chord = 2 * R * sin(a)
    I_own += chord * t**3 / 12                   # bending of the wall itself (small)
    return 2 * I_own


def E_range(I):
    return EI_RAY[0] / I, EI_RAY[1] / I


rows = []
D_mid, t_mid = 150e-6, 15e-6
for label, I in [
    ("solid rod, D=150um", I_solid_rod(D_mid)),
    ("coupled hollow tube, D=150um, t=15um", I_coupled_tube(D_mid, t_mid)),
    ("uncoupled arcs, semicircle (90deg), R=67.5um, t=15um", I_arc_pair(67.5e-6, t_mid, pi / 2)),
    ("uncoupled arcs, 60deg half-angle, R=67.5um, t=15um", I_arc_pair(67.5e-6, t_mid, pi / 3)),
    ("uncoupled arcs, 30deg half-angle, R=67.5um, t=15um", I_arc_pair(67.5e-6, t_mid, pi / 6)),
    ("uncoupled flat plates, w=150um, t=15um", I_flat_pair(D_mid, t_mid)),
]:
    lo, hi = E_range(I)
    rows.append((label, I, lo, hi))
    print(f"{label:58s} I={I:.2e} m^4  E_implied = {lo/1e6:9.1f} .. {hi/1e6:9.1f} MPa")

print("\nSensitivity to hemitrich thickness t (uncoupled flat plates, w=150um):")
for t in (7.5e-6, 11e-6, 15e-6, 16.5e-6, 30e-6):
    lo, hi = E_range(I_flat_pair(D_mid, t))
    print(f"  t={t*1e6:5.1f} um  E_implied = {lo/1e9:6.2f} .. {hi/1e9:6.2f} GPa")
print("Sensitivity to hemitrich thickness t (uncoupled semicircular arcs, R=67.5um):")
for t in (7.5e-6, 15e-6, 30e-6):
    lo, hi = E_range(I_arc_pair(67.5e-6, t, pi / 2))
    print(f"  t={t*1e6:5.1f} um  E_implied = {lo/1e6:6.1f} .. {hi/1e6:6.1f} MPa")
print("Sensitivity to ray diameter D (flat plates, t=15um; w=D):")
for D in (100e-6, 150e-6, 200e-6):
    lo, hi = E_range(I_flat_pair(D, t_mid))
    print(f"  D={D*1e6:5.0f} um  E_implied = {lo/1e9:6.2f} .. {hi/1e9:6.2f} GPa")

# thickness at which the flat-plate model would require E above bone tissue (25 GPa)
E_BONE = 25e9
t_crit = (12 * EI_RAY[1] / (2 * D_mid * E_BONE)) ** (1 / 3)
print(f"\nflat-plate model needs E > 25 GPa (upper EI) if t < {t_crit*1e6:.1f} um")

# Forward check: what fin EI would 1.34 GPa predict under each model (N=17)?
print("\nForward check (calc): whole-fin EI predicted from E=1.34 GPa, 17 rays, D=150um, t=15um")
for label, I, _, _ in rows:
    print(f"  {label:58s} EI_fin = {1.34e9*I*17:.2e} N m^2  (measured 1.5e-9..4e-9)")

# Bluegill consistency, using Puri's cited bluegill ray EI 3.8e-6 N m^2 and D = 1..2 mm
print("\nBluegill (Puri's citation of Flammang 2013): EI=3.8e-6 N m^2, solid rod:")
for D in (1e-3, 2e-3):
    print(f"  D={D*1e3:.0f} mm  E_implied = {3.8e-6/I_solid_rod(D)/1e6:.1f} MPa")
