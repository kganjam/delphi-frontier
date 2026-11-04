"""S30 -- at what body mass does the single-impulse launch budget close?

Every number in docs/research/fish/S30-organism.md is printed by this script.
Inputs are labelled MEASURED (source + read level), PROJECT (inherited from S28/S29),
GEOMETRIC (isometry) or ASSUMED.
Run: python3 docs/research/fish/S30_scaling.py
"""
import math

RHO_AIR = 1.225
CL_MAX = 1.07      # PROJECT (S2/S28): steady CL_max of thin wings, Re 700-2400
G = 9.81
NU_AIR = 1.5e-5
NU_W = 1.0e-6

line = "-" * 78


def h(t):
    print("\n" + line + "\n" + t + "\n" + line)


def v_to(wl, cl=CL_MAX):
    """Minimum (stall) speed for L = W: V = sqrt(2 WL / (rho CL))."""
    return math.sqrt(2 * wl / (RHO_AIR * cl))


# ------------------------------------------------------------------ anchor (S28/S29)
M0 = 0.25e-3        # PROJECT: S28 mass at which case-C fin gives V_to = 4.37 m/s
WL0 = 12.5          # PROJECT: S28 case-C wing loading, N/m^2
V0 = 4.37           # PROJECT
SL0 = 0.030         # PROJECT: standard length, m
CHORD0 = 0.0062     # PROJECT: case-C mean chord, m
E_FLOOR0 = 0.5 * V0 ** 2          # J/kg body, no losses
E_NEED0 = 10.17     # PROJECT (S29): J/kg delivered to body incl. 6.5% in-water drag
# S29 LaMSA supply, J/kg body delivered = f * w * 0.93 * 0.37
SUP = {"w=32 (min)": 3.30, "w=53 (mean)": 5.47, "w=81 (max)": 8.36}
SUP_ALLMUSCLE = 10.94   # PROJECT (S29): 60% of body loads one spring, w=53
V_BURST = 1.38      # MEASURED (Miln 2021 via S28): best adult zebrafish burst, ~0.4 g fish
M_ZF = 0.40e-3

h("0. Anchor")
print(f"S28 case C at m0 = {M0*1e3:.2f} g: WL = {WL0} N/m2 -> V_to = {v_to(WL0):.2f} m/s; "
      f"floor e = V^2/2 = {E_FLOOR0:.2f} J/kg; S29 delivered need {E_NEED0} J/kg")
for k, s in SUP.items():
    print(f"  LaMSA one-side supply {k:12s}: {s:.2f} J/kg -> R0 = supply/need = {s/E_NEED0:.3f}")
print(f"  LaMSA all-muscle (60%), w=53: {SUP_ALLMUSCLE:.2f} J/kg -> R0 = {SUP_ALLMUSCLE/E_NEED0:.3f}")

# ------------------------------------------------------------------ 1. exponents
h("1. Exponents (quantity proportional to m^x)")
# Fish 1990 Table II, wing loading N/m^2 = a M^b (M kg), RMA; transcribed from page images in
# connectors/fish_controls/fish1990.py on main (PROJECT transcription; paper not re-read here)
WL_FIT = {"Cypselurus": (285.015, 0.400, 0.372, 0.430), "Danichthyes": (276.484, 0.533, 0.464, 0.614),
          "Exocoetus": (300.101, 0.360, 0.262, 0.495), "Fodiator": (488.222, 0.434, 0.284, 0.663),
          "Hirundichthyes": (390.069, 0.526, 0.502, 0.551), "Parexocoetus": (458.083, 0.408, 0.257, 0.649)}
WA_B = {"Cypselurus": 0.642, "Danichthyes": 0.485, "Exocoetus": 0.741, "Fodiator": 0.630,
        "Hirundichthyes": 0.479, "Parexocoetus": 0.736}
bs = [v[1] for v in WL_FIT.values()]
print(f"wing loading: geometric 1/3; Fish 1990 genus b = {min(bs):.3f}-{max(bs):.3f} "
      f"(95% CI envelope {min(v[2] for v in WL_FIT.values()):.3f}-{max(v[3] for v in WL_FIT.values()):.3f})")
print(f"wing area:    geometric 2/3; Fish 1990 genus b = {min(WA_B.values()):.3f}-{max(WA_B.values()):.3f}")
# muscle-direct energy per kg: Sutton 2019 model two-point slope
a_sut = math.log(11.25 / 3.6) / math.log(1e3)
print(f"muscle-direct e: Hill work-limited 0; Sutton 2019 model 1 g -> 1 kg: "
      f"log(11.25/3.6)/log(1000) = {a_sut:.3f}; pure power-limited bound 2/9 = {2/9:.3f}")
print("  (power-limited: e = P*t, t ~ s/V ~ m^(1/3)/e^(1/2)  =>  e^(3/2) ~ m^(1/3)  =>  e ~ m^(2/9))")
print("LaMSA e per kg: 0 (Sutton 2019: spring-actuated jump height independent of size)")

# ------------------------------------------------------------------ 2. crossover
h("2. Crossover  R(m) = R0 (m/m0)^(alpha - beta) = 1  ->  m* = m0 * R0^(1/(beta - alpha))")


def mstar(m0, r0, alpha, beta):
    d = beta - alpha
    if d <= 0:
        return None if r0 < 1 else float("inf")
    return m0 * r0 ** (1 / d)


BETAS = (1 / 3, 0.36, 0.40, 0.533)
print("\n2a. LaMSA (alpha = 0), anchored at S28 m0 = 0.25 g; m* is an UPPER mass bound")
print(f"{'supply':14s}" + "".join(f"  beta={b:.3f}" for b in BETAS))
grid = []
for k, s in list(SUP.items()) + [("all-muscle", SUP_ALLMUSCLE)]:
    r0 = s / E_NEED0
    row = []
    for b in BETAS:
        ms = mstar(M0, r0, 0.0, b)
        row.append(ms)
        if k != "all-muscle":
            grid.append(ms)
    print(f"{k:14s}" + "".join(f"  {ms*1e6:8.1f} mg" for ms in row))
cen = mstar(M0, SUP["w=53 (mean)"] / E_NEED0, 0.0, 1 / 3)
print(f"central (w=53, isometric): m* = {cen*1e6:.1f} mg; range (one-side) "
      f"{min(grid)*1e6:.1f}-{max(grid)*1e6:.1f} mg")
print(f"zebrafish 0.40 g / m*: central {M_ZF/cen:.1f}x; range {M_ZF/max(grid):.1f}-{M_ZF/min(grid):.1f}x TOO LARGE")

# design scaled to m*: size, speed, Reynolds numbers
s_ = (cen / M0) ** (1 / 3)
L_s, c_s, V_s = SL0 * s_, CHORD0 * s_, V0 * (cen / M0) ** (1 / 6)
print(f"geometrically scaled design at m*: SL {L_s*1e3:.1f} mm, chord {c_s*1e3:.2f} mm, V_to {V_s:.2f} m/s, "
      f"wing Re_air {V_s*c_s/NU_AIR:.0f}, body Re_water {V_s*L_s/NU_W:.0f}")
ms_lo = min(grid)
s2 = (ms_lo / M0) ** (1 / 3)
V2 = V0 * (ms_lo / M0) ** (1 / 6)
print(f"at the low end m* = {ms_lo*1e6:.1f} mg: chord {CHORD0*s2*1e3:.2f} mm, V {V2:.2f} m/s, "
      f"Re_air {V2*CHORD0*s2/NU_AIR:.0f} (below the Re 700-2400 CL_max data)")

print("\n2b. Muscle-direct, anchored at the measured 1.38 m/s burst of a 0.40 g zebrafish")
V_req_zf = V0 * (M_ZF / M0) ** (1 / 6)
r0m = (V_BURST / V_req_zf) ** 2
print(f"geometric design at 0.40 g needs V = 4.37*(1.6)^(1/6) = {V_req_zf:.2f} m/s; R0 = (1.38/{V_req_zf:.2f})^2 = {r0m:.4f}")
for alpha in (0.0, a_sut, 2 / 9):
    for b in (1 / 3, 0.533):
        ms = mstar(M_ZF, r0m, alpha, b)
        print(f"  alpha {alpha:.3f} beta {b:.3f}: beta-alpha {b-alpha:.3f} -> m* = {ms*1e9:.3g} micrograms")

# ------------------------------------------------------------------ 3. reality check
h("3. Reality check against exocoetids (Fish 1990 fits; CL_max 1.07 ASSUMED for flying fish)")
for g, (a, b, lo, hi) in WL_FIT.items():
    for m in (0.001, 0.003, 0.1, 0.53):
        wl = a * m ** b
        v = v_to(wl)
        print(f"{g:15s} m {m*1e3:6.0f} g: WL {wl:6.1f} N/m2  V_to {v:5.2f} m/s  e {0.5*v*v:6.1f} J/kg")
print(f"Fish 1990 text: smallest WL 11.7 N/m2 ('0.001 kg Hirundichthyes') -> V_to {v_to(11.7):.2f} m/s, "
      f"e {0.5*v_to(11.7)**2:.2f} J/kg")
# length->mass for Davenport's ~50 mm flight onset (Fish 1990 Table I: L = a M^b)
for g, a, b in (("Cypselurus", 0.460, 0.355), ("Hirundichthyes", 0.429, 0.314)):
    m = (0.05 / a) ** (1 / b)
    print(f"50 mm {g}: M = (0.05/{a})^(1/{b}) = {m*1e3:.2f} g")
# adult: 0.3 m fish, ~10 m/s underwater (bioRxiv 765560 via search extract)
m30 = (0.30 / 0.460) ** (1 / 0.355)
wl30 = 285.015 * m30 ** 0.400
print(f"0.30 m Cypselurus: M {m30*1e3:.0f} g, WL {wl30:.0f} N/m2, V_to {v_to(wl30):.1f} m/s; "
      f"10 m/s exit gives R = {(10/v_to(wl30))**2:.2f} of the KE -> must taxi (reported 15-20 m/s)")
m1 = 0.001
print(f"1 g exocoetid at WL 11.7: needs {v_to(11.7):.2f} m/s; at 50 mm that is {v_to(11.7)/0.05:.0f} BL/s; "
      f"zebrafish best burst is {V_BURST/SL0:.0f} BL/s at 30 mm")

# ------------------------------------------------------------------ 4. Sutton's own numbers
h("4. Sutton 2019 model numbers against the launch requirement (ground, no water loss)")
for lab, e in (("spring, any size", 4.2), ("muscle, 1 g", 3.6), ("muscle, 1 kg", 11.25), ("muscle ceiling", 15.0)):
    print(f"{lab:18s} e = {e:5.2f} J/kg -> v = sqrt(2e) = {math.sqrt(2*e):.2f} m/s "
          f"(vs 4.37 m/s needed = {E_FLOOR0:.2f} J/kg)")
print(f"S29 LaMSA store density 53 J/kg (Mendoza & Azizi) vs Sutton's 4.2 J/kg: ratio {53/4.2:.1f}x")
r_sut = SUP["w=53 (mean)"] * 4.2 / 53 / E_NEED0
for b in (1 / 3, 0.533):
    print(f"  if Sutton's 4.2 J/kg muscle applied: R0 = {r_sut:.4f}; beta {b:.3f}: m* = {mstar(M0, r_sut, 0, b)*1e6:.3f} mg")

# ------------------------------------------------------------------ 5. other terms
h("5. Terms that do not set the crossover")
print("drag fraction W_d/KE = rho_w Cd A s / (2 m) ~ L^2 L / L^3 = m^0 (times Cd(Re)); S29 central 6.5%")
print("spring volume fraction ~ e_stored / u ~ m^beta: S29 1-4% at 0.4 g; at m* (central) "
      f"{(cen/M_ZF)**(1/3)*1.02:.2f}-{(cen/M_ZF)**(1/3)*4.10:.2f}% (mammal-grade tendon)")
print("LaMSA power per kg: e ~ m^(1/3), t ~ s/V ~ m^(1/3)/m^(1/6) = m^(1/6), so P = e/t ~ m^(1/6) "
      f"(falls {(cen/M_ZF)**(1/6):.2f}x from 0.40 g to m*)")
