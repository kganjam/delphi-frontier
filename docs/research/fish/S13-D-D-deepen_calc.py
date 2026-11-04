"""S13-D-D: sensitivity of the S13/S13-D feasibility negative to its ray-modulus baseline.

Every number printed here is a CALCULATION. Inputs are tagged with their source in comments.
Run from the repo root:  python3 -I docs/research/fish/S13-D-D-deepen_calc.py
"""
import math

g = 9.81
# --- inputs carried from S13 (S13-protein.md, s13_arith.py) -------------------------------
m = 0.4e-3            # kg, S13 assumption
L = 0.02              # m semi-span, S13 assumption
tol = 0.10            # allowable tip deflection / semi-span, S13 assumption (S13-D tested 5-80 %)
EI_meas = (1.5e-9, 4.0e-9)   # N m^2, Puri et al. 2018 whole caudal fin (full-text, cantilever-fit)
n_rays = (16, 18)            # Puri et al. 2018
E_ceiling = 30e9             # Pa, top of S13's 10-30 GPa amyloid range (search-summary)
E_base_S13 = 1.0e9           # Pa, S13's "teleost whole-ray ~1 GPa" (search-summary, Lauder 2011 via S13)


def EI_req(m=m, L=L, tol=tol):
    w = (m * g / 2) / L                # UDL per half-wing
    return w * L**4 / (8 * tol * L)    # cantilever tip deflection = tol*L


def margin(E_base, EI=EI_meas[1], E_ceil=E_ceiling, **kw):
    """>1 means the required material modulus exceeds the protein ceiling (negative holds)."""
    gap = EI_req(**kw) / EI
    return gap * E_base / E_ceil


print("== 1. S13-D feasibility margin, as recorded ==")
r = EI_req()
print(f"EI_req = {r:.3e} N m^2 ; gap = {r/EI_meas[1]:.0f}x - {r/EI_meas[0]:.0f}x")
for EI in EI_meas:
    print(f"  EI_meas={EI:.1e}: required E = {r/EI*E_base_S13/1e9:.0f} GPa, "
          f"margin over 30 GPa ceiling = {margin(E_base_S13, EI):.1f}x")

print("\n== 2. factor-of-two test on every input (least-favourable EI_meas = 4e-9) ==")
base = margin(E_base_S13)
tests = {
    "E_base x0.5":       margin(E_base_S13 / 2),
    "E_ceiling x2":      margin(E_base_S13, E_ceil=2 * E_ceiling),
    "EI_meas x2":        margin(E_base_S13, EI=2 * EI_meas[1]),
    "tol x2 (20%)":      margin(E_base_S13, tol=2 * tol),
    "semi-span x0.5":    margin(E_base_S13, L=L / 2),
    "mass x0.5":         margin(E_base_S13, m=m / 2),
}
print(f"  baseline margin = {base:.2f}")
for k, v in tests.items():
    print(f"  {k:18s} -> margin {v:6.2f}  ({'FLIPS' if v < 1 else 'holds'})")
print("  all six together ->", f"{margin(E_base_S13/2, EI=2*EI_meas[1], E_ceil=2*E_ceiling, tol=2*tol, L=L/2, m=m/2):.4f}")
for EI in EI_meas:
    print(f"  flip threshold on E_base (EI_meas={EI:.1e}): {E_ceiling/(r/EI)/1e6:.0f} MPa")

print("\n== 3. the real spread of E_base (all calculated from the same measured EI) ==")
I_eff = (3e-16, 7e-16)   # m^4, Puri 2018 effective I
for EI in EI_meas:
    for I in I_eff:
        print(f"  Puri EI/I_eff: {EI:.1e}/{I:.0e} = {EI/I/1e6:.1f} MPa")
print("  challenge-175 per-ray models (D=150 um, t=15 um): solid rod 3.35-10.1 MPa ... flat plates 0.99-2.96 GPa;"
      " envelope 11 MPa - 11.3 GPa (calc, not re-run here)")

print("\n== 4. improved input: measured hemiray TISSUE modulus (Bohns et al. 2020, full-text) ==")
Er = (4.57e9, 8.68e9)   # Pa, reduced modulus means: CTRL_REGEN proximal (lowest), ALN_REGEN proximal (highest, 'pre-amputation level' per authors)
nu = 0.3                # ASSUMPTION (bone-typical Poisson ratio); diamond-tip term neglected
E_t = tuple((1 - nu**2) * e for e in Er)
print(f"  E_r = {Er[0]/1e9:.2f}-{Er[1]/1e9:.2f} GPa -> E = (1-nu^2)E_r = {E_t[0]/1e9:.2f}-{E_t[1]/1e9:.2f} GPa (nu=0.3 assumed)")
for E in E_t:
    for EI in EI_meas:
        print(f"  E_base={E/1e9:.2f} GPa, EI_meas={EI:.1e}: required E = {r/EI*E/1e12:.2f} TPa, "
              f"margin = {margin(E, EI):.0f}x")
print("  S13-D's most lenient row (tol 80%) with the low tissue modulus:",
      f"required E = {EI_req(tol=0.8)/EI_meas[1]*E_t[0]/1e9:.0f} GPa, margin = {margin(E_t[0], tol=0.8):.1f}x")

print("\n== 5. what the tissue modulus says about the fin's architecture ==")
for EI in EI_meas:
    for E in E_t:
        for n in n_rays:
            I_ray = EI / n / E
            print(f"  EI={EI:.1e}, E={E/1e9:.2f} GPa, n={n}: structural I per ray = {I_ray:.2e} m^4")
I_solid, I_tube, I_flat = 2.49e-17, 1.47e-17, 8.44e-20   # challenge-175 grid integration, D=150 t=15 (calc)
lo = EI_meas[0] / n_rays[1] / E_t[1]
hi = EI_meas[1] / n_rays[0] / E_t[0]
print(f"  per-ray structural I range = {lo:.2e} - {hi:.2e} m^4")
print(f"  vs uncoupled flat hemitrich plates {I_flat:.2e}: ratio {I_flat/hi:.1f}-{I_flat/lo:.1f}")
print(f"  full-coupling headroom (bonded tube) = {I_tube/hi:.0f}-{I_tube/lo:.0f}x ; (solid rod) = {I_solid/hi:.0f}-{I_solid/lo:.0f}x")

print("\n== 6. coupling route, measured lever (~12x, sunfish hemitrich clamping, search-summary) ==")
F = 12
for EI in EI_meas:
    print(f"  EI_meas={EI:.1e}: residual gap after 12x = {r/EI/F:.0f}x")
