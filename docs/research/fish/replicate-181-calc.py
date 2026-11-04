# Independent re-derivation for claim 181 (S23-D). Computation only, not observation.
g = 9.81; m = 0.4e-3; W = m * g
def EI_req(L, tol): return (W / 2) * L**2 / (8 * tol)   # UDL cantilever, tip defl = tol*L
EI_meas = (1.5e-9, 4e-9)          # Puri 2018 whole caudal fin, N m^2
E_target = (5e9, 10e9)            # dry-collagen-like / silk-like ceiling, Pa
E0_lb = {"wet RTT fascicle 0.48 GPa": 0.48e9, "wet RTT fibre 0.57 GPa": 0.57e9,
         "hydrated fibre 1.17 GPa": 1.17e9}
for L in (0.02, 0.04):
    for tol in (0.05, 0.10, 0.20, 0.50):
        r = EI_req(L, tol)
        Smin, Smax = r / EI_meas[1], r / EI_meas[0]
        print(f"L={L*100:.0f}cm tol={tol:.2f} EI_req={r:.3e} S=[{Smin:.1f},{Smax:.1f}] "
              f"E0_flip=[{E_target[0]/Smax/1e6:.2f},{E_target[1]/Smin/1e6:.1f}] MPa")
for label, (L, tol) in {"parent-grid lenient (2cm,20%)": (0.02, 0.20),
                        "extended lenient (2cm,50%)": (0.02, 0.50),
                        "strict (4cm,5%)": (0.04, 0.05)}.items():
    lenient = "strict" not in label
    S = EI_req(L, tol) / (EI_meas[1] if lenient else EI_meas[0])
    Et = E_target[1] if lenient else E_target[0]
    for k, E0 in E0_lb.items():
        C = Et / E0
        print(f"{label:32s} S={S:8.1f} {k:28s} C={C:6.2f} margin=S/C={S/C:8.2f}")
