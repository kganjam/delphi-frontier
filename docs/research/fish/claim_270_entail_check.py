"""Claim 270 entailment, timescale check (DERIVED, not observed).

Question: starting at U = 0.45 m/s with the body airborne and only the lower caudal lobe
in water, does the body sink back into the water BEFORE the lobe's thrust carries it up to
the speed at which the lobe can support it (CL_z = 1)?

Every input is S32's own (branch claude/s32-multi-stroke-launch-qpq9g2, S32-organism.md
section 3.1). Thrust per case is back-solved from S32's tabulated T_lobe at 0.45 m/s.
The lobe is held at CL_z = 1 (S32's cap) throughout; any vertical shortfall accelerates
the body downward. Induced drag at CL_z = 1 is taken from S32's table (D_ind / CL_z^2).
Nothing here is a measurement.
"""
import math

RHO, G0, SIG, C = 1000.0, 9.81, 0.072, 0.006
S_LOBE = 18.9e-6
CASES = {
    #          mass,   phi, cos,  dcos, V_to, T@0.45 (mN), CD law, D_ind@CL=1,0.45 (mN)
    "generous": (0.25e-3, 1.0, 0.0, 0.0, 4.41, 4.66, "scaled", 0.57 / 1.27**2),
    "central":  (0.25e-3, 0.5, 0.5, 0.1, 4.41, 1.76, "scaled", 3.17 / 2.99**2),
    "stingy":   (0.40e-3, 0.25, 1.0, 0.3, 5.58, 0.61, "const", 35.2 / 9.95**2),
}


def cd(U, law):
    if law == "const":
        return 0.08
    re = U * C / 1.0e-6
    return 0.08 * math.sqrt(4780 / re) if re < 4780 else (0.08 if re <= 9560 else 0.08 * math.sqrt(9560 / re))


for name, (m, phi, cos, dcos, vto, t045, law, dind1) in CASES.items():
    S = phi * S_LOBE
    W = m * G0
    Fsv, Fsh = 2 * SIG * C * cos, 2 * SIG * C * dcos
    Gp = t045 * 1e-3 / (0.5 * RHO * S) + cd(0.45, law) * 0.45**2
    umin = math.sqrt((W + Fsv) / (0.5 * RHO * S + W / vto**2))
    U, w, z, t, dt = 0.45, 0.0, 0.0, 0.0, 1e-5
    while U < umin and t < 3.0:
        T = 0.5 * RHO * S * (Gp - cd(U, law) * U**2)
        Dind = dind1 * 1e-3 * (U / 0.45) ** 2
        U += (T - Fsh - Dind) / m * dt
        lift = W * min(1, (U / vto) ** 2) + 0.5 * RHO * U**2 * S * 1.0
        w += min(0.0, lift - W - Fsv) / m * dt
        z += w * dt
        t += dt
        if U < 0.3:
            break
    print(f"{name:9s} U_min={umin:.3f} m/s  t_to_U_min={t*1e3:7.1f} ms  "
          f"sink_before_U_min={-z*1e3:7.2f} mm  reached={U >= umin}")
