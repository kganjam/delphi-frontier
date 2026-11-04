"""S23-D-D reproduction. Every number printed here is COMPUTED, not observed.

Uniform-load cantilever of span L, bending stiffness EI(s) with s measured from the TIP.
Tip deflection  delta = integral_0^L M(s) * s / EI(s) ds,  M(s) = w s^2 / 2.
If the distal segment s < a (where actinotrichia sit) is made infinitely rigid, the
deflection that remains is  1 - phi,  phi = share of tip compliance contributed by s < a.
To meet S6 the deflection must fall by the shortfall factor S, i.e. phi >= 1 - 1/S.
"""
g = 9.81; m = 0.4e-3; W = m * g

def EIreq(L, tol):
    return (W / 2) * L**2 / (8 * tol)

def phi(a, L, n=0.0, load="uniform"):
    # EI(s) ∝ s^n (n = 0: uniform beam; n > 0: tapers toward the tip)
    p = 3 if load == "uniform" else 2      # M*s ∝ s^3 (uniform load) or s^2 (tip point load)
    k = p + 1 - n
    if k <= 0:
        return float("nan")                # tip compliance diverges: unphysical
    return (a / L) ** k

cases = {"central (L=4 cm, tol 10%, EI 4e-9)": (0.04, 0.10, 4e-9),
         "lenient (L=2 cm, tol 50%, EI 5e-9)": (0.02, 0.50, 5e-9)}
A = {"measured low 200 um": 200e-6, "measured high 300 um": 300e-6,
     "x2 of high (600 um)": 600e-6, "x10 of high (3 mm)": 3e-3}

for cname, (L, tol, EI) in cases.items():
    S = EIreq(L, tol) / EI
    need = 1 - 1 / S
    print(f"\n{cname}: EI_req={EIreq(L, tol):.3g} N m^2, S={S:.1f}, need phi >= {need:.4f}")
    print(f"  a/L required (uniform EI, uniform load, rigid tip segment): {need ** 0.25:.4f}"
          f"  -> a >= {need ** 0.25 * L * 1e3:.2f} mm")
    print(f"  a/L required (uniform EI, tip point load):                  {need ** (1/3):.4f}")
    for an, a in A.items():
        f0 = phi(a, L); fp = phi(a, L, load="point")
        best = 1 / (1 - f0)
        print(f"  a={an:22s} a/L={a/L:.4f}  phi={f0:.2e} (point load {fp:.2e})"
              f"  max deflection reduction x{best:.8f}  margin S/that = {S / best:.1f}")
    print("  taper sensitivity, a = 300 um, EI(s) ∝ s^n:")
    for n in (1, 2, 3, 3.5, 3.9, 3.99):
        f = phi(300e-6, L, n)
        print(f"    n={n:<5} phi={f:.4f}  flips={'yes' if f >= need else 'no'}")
    import math
    n_star = 4 - math.log(need) / math.log(300e-6 / L)
    print(f"  taper exponent needed to flip at a=300 um: n >= {n_star:.4f} (n >= 4 is a divergent tip)")
