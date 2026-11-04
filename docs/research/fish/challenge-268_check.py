"""Challenge 268: independent checks on S32's 'THRUST PASSES' claim.

Usage:
  git show origin/claude/s32-multi-stroke-launch-qpq9g2:docs/research/fish/S32_taxi.py > /tmp/S32_taxi.py
  python3 -I docs/research/fish/challenge-268_check.py /tmp/S32_taxi.py

Part A is standalone arithmetic. Part B reuses S32's own force model (forces, G_calibrated, zf_params, SCEN),
loaded by exec with its printout suppressed, and changes one input at a time. Everything here is CALCULATED.
"""
import contextlib
import io
import math
import sys

# ---------------------------------------------------------------- A. body drag, water vs air, at 1.38 m/s
RHO_W, RHO_A = 1000.0, 1.225          # kg/m^3, the values S32 uses
MU_W, MU_A = 1.0e-3, 1.81e-5          # Pa s, water ~20 C, air ~15-20 C (textbook constants)
A, U, L = 24e-6, 1.38, 0.030          # frontal area (S28), burst speed, body length (S32: fin height 9 mm = 0.3 SL)

q = lambda rho: 0.5 * rho * U * U
print(f"rho_w/rho_a = {RHO_W / RHO_A:.1f}")
print(f"S32's quoted pair: water Cd 0.2 -> {q(RHO_W)*0.2*A*1e3:.2f} mN ; air Cd 0.3 -> {q(RHO_A)*0.3*A*1e6:.2f} uN ; "
      f"ratio {(q(RHO_W)*0.2)/(q(RHO_A)*0.3):.0f}")
print(f"same Cd 0.2 both media: air {q(RHO_A)*0.2*A*1e6:.2f} uN ; ratio {RHO_W/RHO_A:.0f}")
nu_w, nu_a = MU_W / RHO_W, MU_A / RHO_A
print(f"body Re: water {U*L/nu_w:,.0f}, air {U*L/nu_a:,.0f} (factor {nu_a/nu_w:.1f} lower in air)")
print(f"laminar-friction-dominated drag ratio sqrt(rho_w mu_w / rho_a mu_a) = {math.sqrt(RHO_W*MU_W/(RHO_A*MU_A)):.0f}")
for cw in (0.1, 0.2, 0.3):
    ca = cw * math.sqrt(nu_a / nu_w)
    print(f"  Cd_w {cw}: friction-scaled Cd_air {ca:.2f} -> air drag {q(RHO_A)*ca*A*1e6:.1f} uN")

# ---------------------------------------------------------------- B. S32's own model, one input changed
ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(sys.argv[1]).read(), ns)
S, zf, Gc, forces, u_eq = ns["SCEN"], ns["zf_params"], ns["G_calibrated"], ns["forces"], ns["u_eq"]


def params(name, cd_air=0.3, kappa=1.0):
    s = S[name]
    p = zf(s["m"], s["phi"], kappa * Gc(s["Cdb"], s["cdmode"]), s["cdmode"], s["CD0"], s["costh"], s["dcos"])
    p["Cd_body"] = cd_air
    return p


def doubling_strokes(p, U0=1.38, f=52.0, dt=2e-5):
    Uc, t = U0, 0.0
    a = lambda u: forces(u, p)["net"] / p["m"]
    while t < 3.0:
        k1 = a(Uc); k2 = a(Uc + .5 * dt * k1); k3 = a(Uc + .5 * dt * k2); k4 = a(Uc + dt * k3)
        Uc += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; t += dt
        if Uc >= 2 * U0:
            return t * f
    return None


for name in ("GENEROUS", "CENTRAL"):
    for cd_air in (0.3, 0.78, 1.17):
        p = params(name, cd_air)
        F = forces(1.38, p)
        drag = F["D_w"] + F["D_b"] + F["D_i"] + F["Fsh"]
        n = doubling_strokes(p)
        print(f"{name:8s} Cd_air {cd_air:.2f}: T {F['T']*1e3:.3f} mN / total drag {drag*1e3:.3f} mN = {F['T']/drag:.1f}x ; "
              f"U_eq {u_eq(p):.2f} m/s ; doubling {'never' if n is None else f'{n:.1f} strokes'}")
    lo, hi = 0.0, 1.0
    for _ in range(60):
        k = (lo + hi) / 2
        lo, hi = (lo, k) if forces(1.38, params(name, kappa=k))["net"] > 0 else (k, hi)
    print(f"{name:8s} thrust factor kappa at which net force at 1.38 m/s reaches zero: {hi:.2f}")
