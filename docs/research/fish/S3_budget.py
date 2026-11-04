#!/usr/bin/env python3
"""S3 (organism): mass and power budget for a winged Danio rerio.

Everything printed here is COMPUTATION on stated inputs. Nothing is a measurement.
Inputs and their read-levels are documented in S3-organism.md, section 2.

Run: python3 docs/research/fish/S3_budget.py
"""
from math import sqrt, pi

g = 9.81            # m s^-2
rho_air = 1.225     # kg m^-3
CL = 1.07           # project CL_max (S2/S28, derived), used unchanged
m_body = 0.40e-3    # kg, brief

# --- fin tissue areal density sigma = rho_fin * t_mean (kg m^-2) -------------
# thickness: Puri 2018 caliper 200 -> 40 um proximal->distal (measured);
#            Murciano 2018 central inter-ray 82.4 um, marginal 276-281 um (measured)
# density:   1.05 g/cm3 zebrafish body w/o swimbladder (Robertson 2008, measured, proxy for soft fin);
#            1.557 g/cm3 hydrated albacore bone (Tont 1977 via S9, proxy for ray bone)
RHO_SOFT, RHO_BONE = 1050.0, 1557.0
rho_central = 0.8 * RHO_SOFT + 0.2 * RHO_BONE   # ASSUMED 20 % ray volume fraction
TISSUE = {
    "low (40 um, 1.05)":       RHO_SOFT * 40e-6,
    "central (120 um, 1.15)":  rho_central * 120e-6,   # 120 um = mean of a linear 200->40 taper (assumed)
    "high (200 um, 1.56)":     RHO_BONE * 200e-6,
    "high+ (281 um, 1.56)":    RHO_BONE * 281e-6,       # marginal inter-ray thickness, all-bone density
}

# --- designed planforms taken from sibling subproblems (mm^2, semispan per fin mm) ---
PLANFORMS = [
    ("S28 case A (length-only)",        57,   13.5),
    ("S28 case B (isometric)",          125,  13.5),
    ("S28 case C (AR 5, headline)",     192,  13.5),
    ("S2 small",                        450,  None),
    ("S2 mid (2 x 3 cm x 1.5 cm)",      900,  30.0),
    ("S10 R=4 cm, AR 6",                1070, 40.0),
    ("S2 large",                        1800, None),
    ("S28 'fly at 1.38 m/s'",           1925, None),
]


def vto(M, S):
    return sqrt(2 * M * g / (rho_air * S * CL))


def hr(t):
    print("\n" + t + "\n" + "-" * len(t))


hr("1. Fin tissue areal density sigma (kg/m^2) and self-carry speed V_self = sqrt(2 sigma g / (rho CL))")
for k, s in TISSUE.items():
    print(f"{k:26s} sigma = {s:.4f} kg/m^2  (= {s:.4f} mg/mm^2)  V_self = {sqrt(2*s*g/(rho_air*CL)):.3f} m/s")
q138 = 0.5 * rho_air * 1.38**2 * CL / g
print(f"lift per area at 1.38 m/s, CL 1.07: {q138:.4f} kg/m^2 (a fin can carry anything beyond itself only if sigma < this)")

hr("2. Wing mass and V_to with wing mass charged (m_body = 0.40 g)")
print(f"{'planform':32s} {'S mm2':>6s} " + " ".join(f"{k.split()[0]:>16s}" for k in TISSUE))
for name, S_mm2, _ in PLANFORMS:
    S = S_mm2 * 1e-6
    cells = []
    for s in TISSUE.values():
        mw = s * S
        cells.append(f"{mw*1e6:6.1f}mg {100*mw/m_body:5.1f}%")
    print(f"{name:32s} {S_mm2:6d} " + " ".join(f"{c:>16s}" for c in cells))

print("\nV_to (m/s): wing-free -> with central wing mass -> with high wing mass")
for name, S_mm2, _ in PLANFORMS:
    S = S_mm2 * 1e-6
    v0 = vto(m_body, S)
    vc = vto(m_body + TISSUE["central (120 um, 1.15)"] * S, S)
    vh = vto(m_body + TISSUE["high (200 um, 1.56)"] * S, S)
    print(f"{name:32s} {v0:5.2f} -> {vc:5.2f} -> {vh:5.2f}")

hr("3. Planform needed to take off at a given speed, wing mass charged: S = m_body / (q CL/g - sigma)")
for V in (1.38, 2.0, 3.0, 4.37):
    lpa = 0.5 * rho_air * V**2 * CL / g
    row = []
    for k, s in TISSUE.items():
        row.append("no solution" if lpa <= s else f"{m_body/(lpa-s)*1e6:7.0f} mm2 (wing {s*m_body/(lpa-s)*1e3:.2f} g)")
    print(f"V = {V:4.2f} m/s, lift/area {lpa:.3f}: " + " | ".join(row))

hr("4. Structural spar: one solid circular bone rod per fin, uniform lift, tip deflection 10 % of semispan")
# EI_req = (n W_total/2) L^2 / (8 * 0.1); rod: EI = E pi r^4/4, mass = rho pi r^2 L
for name, S_mm2, L_mm in PLANFORMS:
    if L_mm is None:
        continue
    L = L_mm * 1e-3
    M = m_body + TISSUE["central (120 um, 1.15)"] * S_mm2 * 1e-6
    for n in (1, 3):
        EI = (n * M * g / 2) * L**2 / (8 * 0.1)
        for E in (0.11e9, 1.34e9, 6.48e9):
            r = (4 * EI / (pi * E)) ** 0.25
            ms = RHO_BONE * pi * r**2 * L
            print(f"{name:30s} n={n} EI_req={EI:.2e} N m2  E={E/1e9:5.2f} GPa  rod d={2*r*1e6:6.0f} um  "
                  f"spar mass (2 fins) {2*ms*1e6:6.2f} mg = {100*2*ms/m_body:5.2f}% body")
print("Measured whole caudal-fin EI (Puri 2018): 1.5e-9 to 4e-9 N m2; measured ray diameter 0.1-0.2 mm")

hr("5. Launch power: accelerate total mass to V_to over distance s from rest, constant acceleration")
# P_body = (V^2/2) / t / eta_h, t = 2 s / V ; per kg muscle: / (f_m * m_body / M)
WM = 142.7  # W/kg, Wakeling & Johnston 1998, fast-start fast muscle, 20 C (measured, abstract)
for name, S_mm2, _ in [PLANFORMS[2], PLANFORMS[4], PLANFORMS[5]]:
    S = S_mm2 * 1e-6
    for tissue in ("central (120 um, 1.15)",):
        M = m_body + TISSUE[tissue] * S
        V = vto(M, S)
        for s_bl in (0.5, 1.0, 2.0):
            s = s_bl * 0.04
            t = 2 * s / V
            for eta in (1.0, 0.37):
                Pb = (V**2 / 2) / t / eta
                for fm in (0.3, 0.6):
                    Pm = Pb * M / (fm * m_body)
                    print(f"{name:28s} V_to {V:4.2f}  s={s_bl:3.1f} BL t={t*1e3:5.1f} ms eta={eta:4.2f} f_m={fm:.1f}: "
                          f"{Pb:7.0f} W/kg total, {Pm:7.0f} W/kg muscle = {Pm/WM:5.1f}x the 142.7 W/kg measured")

print("\nToday's fish for reference: 1.38 m/s burst, 0.4 g, no wing, s = 1 BL, eta 1, f_m 0.3:")
V = 1.38; t = 2 * 0.04 / V
print(f"  t = {t*1e3:.1f} ms, {(V**2/2)/t:.0f} W/kg body, {(V**2/2)/t/0.3:.0f} W/kg muscle (eta 1), "
      f"{(V**2/2)/t/0.3/0.37:.0f} W/kg muscle (eta 0.37) vs {WM} measured: consistency check, not validation")

hr("6. Flapping (S10 planform R = 4 cm): what wing mass does to S10's hover numbers")
S = 1070e-6; R = 0.04
for k in ("low (40 um, 1.05)", "central (120 um, 1.15)", "high (200 um, 1.56)"):
    mw = TISSUE[k] * S; M = m_body + mw
    W = M * g; A = pi * R**2
    Pind = 1.2 * sqrt(W**3 / (2 * rho_air * A))
    # inertial: two rectangular wings, I = mw R^2 / 3, sinusoidal stroke amplitude 120 deg, f = 22 Hz
    I = mw * R**2 / 3; f = 22.0; Phi = 2 * pi / 3
    wmax = 2 * pi * f * Phi / 2
    KE = 0.5 * I * wmax**2
    Pin = 2 * f * KE   # if the wing's KE is lost every half-stroke (no elastic storage)
    print(f"{k:26s} wing {mw*1e3:.3f} g, M {M*1e3:.3f} g, P_ind {Pind*1e3:.2f} mW "
          f"(x{(M/m_body)**1.5:.2f} vs wingless), inertial (no storage) {Pin*1e3:.1f} mW = {Pin/Pind:.1f}x P_ind")
