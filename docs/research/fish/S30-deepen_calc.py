"""S30-D -- deepen S30 by attacking its most sensitive input.

Every number in docs/research/fish/S30-deepen.md is printed by this script.
Parent: S30 (branch claude/s30-launch-budget-mass-k71prf, commit 59f421da),
whose crossover is  m* = m0 * R0^(1/(beta-alpha)),  R0 = f*w*eta_s*eta_h / need.
Labels: PROJECT (inherited), LIT (literature value, read level in the .md),
DERIVED (calculated here). Nothing here is a measurement.
Run: python3 docs/research/fish/S30-deepen_calc.py
"""
import math

line = "-" * 78
def h(t):
    print("\n" + line + "\n" + t + "\n" + line)

# ---------------------------------------------------------------- S30 central case (PROJECT)
M0 = 0.25e-3      # kg, S28 anchor
M_ZF = 0.40e-3    # kg
NEED = 10.17      # J/kg body delivered (S29)
F = 0.30          # one-side axial muscle fraction (S29, assumed)
W = 53.0          # J/kg muscle, Mendoza & Azizi 2021 Cuban tree frog mean
ETA_S = 0.93      # tendon return (Ker 1981 via S29)
ETA_H = 0.37      # pike C-start (Frith & Blake via S29)
BETA = 1 / 3
ALPHA = 0.0
SL0, CHORD0, V0 = 0.030, 0.0062, 4.37
NU_AIR = 1.5e-5

def r0(f=F, w=W, es=ETA_S, eh=ETA_H, need=NEED):
    return f * w * es * eh / need

def mstar(r, beta=BETA, alpha=ALPHA, m0=M0):
    return m0 * r ** (1 / (beta - alpha))

def design_at(m):
    s = (m / M0) ** (1 / 3)
    v = V0 * (m / M0) ** (1 / 6)
    return SL0 * s * 1e3, CHORD0 * s * 1e3, v, v * CHORD0 * s / NU_AIR

base = mstar(r0())
h("0. Reproduce S30 central case")
print(f"R0 = {F}*{W}*{ETA_S}*{ETA_H}/{NEED} = {r0():.4f};  m* = {base*1e6:.1f} mg; "
      f"zebrafish/m* = {M_ZF/base:.1f}x")

# ---------------------------------------------------------------- 1. sensitivity
h("1. Sensitivity: each input x2 and /2, all else central (m* in mg)")
cases = [
    ("w (53 J/kg muscle)", lambda k: mstar(r0(w=W * k))),
    ("eta_h (0.37)", lambda k: mstar(r0(eh=ETA_H * k))),
    ("f (0.30)", lambda k: mstar(r0(f=F * k))),
    ("eta_s (0.93)", lambda k: mstar(r0(es=min(ETA_S * k, 1.0)))),
    ("need (10.17 J/kg)", lambda k: mstar(r0(need=NEED * k))),
    ("beta (1/3)", lambda k: mstar(r0(), beta=BETA * k)),
    ("m0 anchor (0.25 g)", lambda k: mstar(r0(), m0=M0 * k)),
]
for name, fn in cases:
    up, dn = fn(2.0), fn(0.5)
    print(f"{name:22s} x2: {up*1e6:9.2f} mg ({up/base:7.3f}x)   /2: {dn*1e6:9.3f} mg ({dn/base:7.4f}x)")
print("note eta_s x2 is capped at 1.0 (physical); f x2 = 0.60 is the S29 all-muscle ceiling")
print(f"elasticity of m* to any R0 factor = 1/(beta-alpha) = {1/(BETA-ALPHA):.1f}")
# what a x2 error does to the conclusion
for k in (2.0, 0.5):
    m = mstar(r0(w=W * k))
    sl, c, v, re = design_at(m)
    print(f"  w x{k}: m* {m*1e6:.1f} mg -> scaled design SL {sl:.1f} mm, chord {c:.2f} mm, V {v:.2f} m/s, Re_air {re:.0f}")

# ---------------------------------------------------------------- 2. the frog numbers themselves
h("2. Frog spring-loading values (Mendoza & Azizi 2021, full text) and Sutton 2019 model")
for lab, w in (("cane toad mean", 22), ("bullfrog mean", 37), ("Cuban tree frog mean", 53),
               ("Cuban tree frog min", 32), ("Cuban tree frog max", 81), ("Sutton model spring", 4.2)):
    m = mstar(r0(w=w))
    print(f"{lab:22s} w = {w:5.1f} J/kg -> R0 {r0(w=w):.3f}, m* {m*1e6:8.3f} mg")

# ---------------------------------------------------------------- 3. teleost estimate (DERIVED)
h("3. Teleost fast muscle: upper bound on energy stored in a series spring in one contraction")
# A muscle whose force is capped at F0 = sigma0*A, shortening by dL = eps*Lf, stores at most
# 1/2 F0 dL in a linear (Hookean) spring, and less in a stiffening (J-shaped) one.
# Per kg muscle: w_max = 0.5 * sigma0 * eps / rho.
RHO_M = 1060.0  # kg/m^3, ASSUMED muscle density
SIG = {"200 kPa": 200e3, "250 kPa": 250e3, "300 kPa": 300e3}          # LIT: fish fast fibre P0 200-300 kN/m2
EPS = {"0.10": 0.10, "0.113 (trout)": 0.113, "0.13": 0.13, "0.15": 0.15, "0.24 (carp, curvature)": 0.24}
print(f"{'eps \\ sigma0':24s}" + "".join(f"{k:>10s}" for k in SIG))
wf = {}
for ek, e in EPS.items():
    row = []
    for sk, s in SIG.items():
        w = 0.5 * s * e / RHO_M
        wf[(ek, sk)] = w
        row.append(w)
    print(f"{ek:24s}" + "".join(f"{w:10.1f}" for w in row))
W_LO = wf[("0.10", "200 kPa")]
W_C = wf[("0.13", "250 kPa")]
W_HI = wf[("0.15", "300 kPa")]
W_CEIL = wf[("0.24 (carp, curvature)", "300 kPa")]
print(f"teleost w: central {W_C:.1f}, sonomicrometry range {W_LO:.1f}-{W_HI:.1f}, ceiling {W_CEIL:.1f} J/kg muscle")
print(f"frog 53 / teleost central = {53/W_C:.1f}x;  Sutton 4.2 / teleost central = {4.2/W_C:.2f}x")
# what (sigma*eps) the frog value implies, for comparison only
print(f"frog 53 J/kg implies sigma0*eps = {2*53*RHO_M/1e3:.0f} kJ/m3, e.g. eps = {2*53*RHO_M/300e3:.2f} at 300 kPa (DERIVED, not reported by the authors)")
# cross-check with S29: today's burst implies 8.6 J/kg muscle per stroke
print("cross-check: S29 back-calculated 8.6 J/kg muscle per stroke from the 1.38 m/s burst (with eta_h 0.37)")

# ---------------------------------------------------------------- 4. recompute S30
h("4. Recompute S30 m* with the teleost w (eta chain as S30)")
BETAS = (1 / 3, 0.36, 0.40, 0.533)
print(f"{'w (J/kg muscle)':26s}" + "".join(f"  beta={b:.3f}" for b in BETAS))
grid = []
for lab, w, f in (("teleost low", W_LO, F), ("teleost central", W_C, F), ("teleost high", W_HI, F),
                  ("teleost ceiling", W_CEIL, F), ("central, all muscle f=0.6", W_C, 0.60),
                  ("ceiling, all muscle f=0.6", W_CEIL, 0.60)):
    row = [mstar(r0(f=f, w=w), beta=b) for b in BETAS]
    if f == F and "ceiling" not in lab:
        grid += row
    print(f"{lab:26s}" + "".join(f"  {m*1e6:9.3f} mg" for m in row) + f"   (R0 {r0(f=f, w=w):.3f})")
mc = mstar(r0(w=W_C))
print(f"central m* {mc*1e6:.2f} mg (S30: {base*1e6:.1f} mg, ratio {mc/base:.3f}); "
      f"one-side sonomicrometry range {min(grid)*1e6:.2f}-{max(grid)*1e6:.1f} mg")
print(f"zebrafish 0.40 g / m*: central {M_ZF/mc:.0f}x too large; range {M_ZF/max(grid):.0f}-{M_ZF/min(grid):.0f}x")
for lab, m in (("central", mc), ("high-w, beta .533", max(grid)), ("ceiling w, beta 1/3", mstar(r0(w=W_CEIL)))):
    sl, c, v, re = design_at(m)
    print(f"  scaled design at {lab} m* = {m*1e6:.2f} mg: SL {sl:.1f} mm, chord {c:.2f} mm, V {v:.2f} m/s, Re_air {re:.0f}")
print("S30's own validity limit: it declared 'no realisable crossover' for m* <= 4 mg "
      "(SL ~7.6 mm, Re_air ~230), below CL_max data (Re 700-2400)")
sl, c, v, re = design_at(39e-6)
print(f"  S30 window check: 39 mg -> Re_air {re:.0f};  Re_air >= 700 needs m >= ", end="")
# solve Re_air(m)=700: Re ~ m^(1/2)
re0 = design_at(M0)[3]
print(f"{M0*(700/re0)**2*1e6:.1f} mg")

# ---------------------------------------------------------------- 5. with S29-D's chain
h("5. Compounded with S29-D (spring-release chain KE/E_stored 0.10 measured analogue, vs 0.323)")
# S29-D: S29's eta_s*eta_h/(1+drag) = 0.323; Conte 2010 measured 0.10 -> scale R0 by 0.10/0.323
k = 0.10 / (ETA_S * ETA_H / 1.065)
for lab, w in (("frog 53", 53), ("teleost central", W_C), ("teleost ceiling", W_CEIL)):
    for f in (F, 0.60):
        m = mstar(r0(f=f, w=w) * k)
        print(f"{lab:16s} f={f:.2f}: R0 {r0(f=f, w=w)*k:.4f} -> m* {m*1e6:.4f} mg")
