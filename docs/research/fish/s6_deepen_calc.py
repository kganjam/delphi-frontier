"""S6-D: passive-cantilever check of a lepidotrichial ray under glide load.

CALCULATION ONLY. Nothing here is an observation. Scenario inputs marked ASSUMPTION
are not sourced for any flying-fish species; they are a reference point for the
sensitivity analysis, and the conclusions are stated as functions of them.

Model: each load-bearing pectoral ray is a uniform Euler-Bernoulli cantilever
carrying an equal share P of the lift as a uniform distributed load.
    P      = n * W / (2 * N)          (two pectoral fins, N rays each)
    delta  = P L^3 / (8 EI)           (tip deflection, uniform load)
    delta/L = P L^2 / (8 EI)
    M_base = P L / 2
"""
import math

g = 9.81
# ---- reference scenario: ASSUMPTIONS, not measurements ----
m = 0.10      # kg body mass                          ASSUMPTION
N = 14        # load-bearing rays per pectoral fin    ASSUMPTION
L = 0.12      # m effective ray span                  ASSUMPTION
n = 1.0       # load factor (steady glide, lift = weight)
LIMIT = 0.10  # delta/L above which the ray is treated as "not carrying" (ASSUMPTION)

# ---- candidate flexural stiffness values (sourced; read-levels in S6-deepen.md) ----
EI = {
    "Flammang2013 abstract (bluegill ray)":            565e-6,
    "Flammang2013 as relayed by Puri2018 (bluegill)":   3.8e-6,
    "Aiello2018 labrid max (1.5109 uN m^2)":           1.5109e-6,
    "Aiello2018 labrid min (0.0001 uN m^2)":           1e-10,
}

def dl(EI_, m_=m, N_=N, L_=L, n_=n):
    P = n_ * m_ * g / (2 * N_)
    return P * L_**2 / (8 * EI_)

P = n * m * g / (2 * N)
print(f"per-ray load P = {P:.4f} N ; base moment M = {P*L/2:.3e} N m")
EI_req = P * L**2 / (8 * LIMIT)
print(f"EI required for delta/L <= {LIMIT}: {EI_req:.3e} N m^2\n")
for k, v in EI.items():
    print(f"{k:50s} EI={v:.3e}  delta/L={dl(v):9.3g}  {'carries' if dl(v)<=LIMIT else 'FAILS'}")

print("\nSensitivity (factor-2 perturbations around the passing case EI=565e-6):")
base = 565e-6
for name, kw in [("EI/2", dict(EI_=base/2)), ("EI*2", dict(EI_=base*2)),
                 ("L*2", dict(EI_=base, L_=L*2)), ("L/2", dict(EI_=base, L_=L/2)),
                 ("m*2", dict(EI_=base, m_=m*2)), ("N/2", dict(EI_=base, N_=N/2)),
                 ("n=2", dict(EI_=base, n_=2))]:
    print(f"  {name:6s} delta/L = {dl(**kw):.3f}")

print("\nWhat stiffening factor would rescue the relayed value 3.8e-6?",
      f"{EI_req/3.8e-6:.0f}x ; Alben2007 base actuation '>10x', Lauder2011 hemitrich lock '~12x'")
print("3.8e-6 x 12 ->", f"delta/L = {dl(3.8e-6*12):.2f}")

print("\nGeometry cross-check (solid circular section, E = 1 GPa 'order of' per Das2024):")
E = 1e9
for d in (1e-3, 2e-3):
    I = math.pi * d**4 / 64
    print(f"  d={d*1e3:.0f} mm -> EI = {E*I:.2e} N m^2")
for v in (565e-6, 3.8e-6):
    d = (64 * v / E / math.pi) ** 0.25
    print(f"  EI={v:.1e} -> equivalent solid d = {d*1e3:.2f} mm")
d_req = (64 * EI_req / E / math.pi) ** 0.25
I = math.pi * d_req**4 / 64
print(f"  required EI -> d = {d_req*1e3:.2f} mm ; base bending stress = {P*L/2*(d_req/2)/I/1e6:.1f} MPa")
