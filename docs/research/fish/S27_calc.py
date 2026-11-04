"""S27 arithmetic. COMPUTATION, not observation. Inputs and provenance are in S27-organ.md.

Run: python3 docs/research/fish/S27_calc.py
"""
import math

EI_REQ = 6.3e-4   # N m^2, S6-D requirement (calculated there from assumptions m=0.1 kg, N=14, L=0.12 m, n=1, delta/L<=0.1)

# --- 1. Where reported rays sit against the floor (one-axis screen, as S6-D drew it) ---
rays = {
    "S6-D passive ray (3.8e-6, Puri 2018 relaying Flammang 2013; untraced per S25)": 3.8e-6,
    "labrid max (Aiello 2018 JEB abstract, proximal)": 1.51e-6,
    "labrid min (Aiello 2018 JEB abstract, distal)": 1.0e-10,
    "labrid high-AR mean at 50% ray length (Aiello 2017 PNAS, 210e-9)": 210e-9,
    "labrid low-AR mean at 50% ray length (Aiello 2017 PNAS, 20e-9)": 20e-9,
    "bluegill passive, back-calculated by S6-D-D from Alben 2007 k": 1.9e-6,
    "bluegill clamped-base upper bound, S6-D-D from Alben 2007 k": 4.3e-5,
    "Flammang 2013 abstract, 'calculated'": 565e-6,
}
print("1. Shortfall EI_req / EI (one axis)")
for k, v in rays.items():
    print(f"   {k:78s} EI={v:.2e}  shortfall x{EI_REQ / v:,.1f}")

# --- 2. Second axis candidate: engageable multiplier M = EI_max / EI_0 ---
# Feasibility on the 2-axis map: EI_0 * M >= EI_REQ, i.e. M >= EI_REQ / EI_0.
print("\n2. Multiplier needed on the 2-axis map, vs multipliers that are reported")
M_lock_meas = 12.0          # Alben 2007, clamped/one-base-free, n=1 bluegill ray (measured)
M_lock_model = 100.0        # Alben 2007 linear-model asymptote, G > 1e5 (model)
M_curv = (3.0, 7.0)         # Nguyen et al. 2017, mackerel, 1 + W^2/T^2 = 300-700 % (derived by authors from uCT geometry)
for name, EI0 in [("3.8e-6 passive (S6-D)", 3.8e-6), ("1.9e-6 passive bluegill (S6-D-D)", 1.9e-6),
                  ("1.51e-6 labrid max", 1.51e-6)]:
    need = EI_REQ / EI0
    best_meas = M_lock_meas * M_curv[1]          # ASSUMES the two mechanisms compound multiplicatively
    best_model = M_lock_model * M_curv[1]
    print(f"   EI_0={name:34s} M_needed={need:7.1f}  "
          f"lock(12) -> x{need / M_lock_meas:5.1f} short; lock*curv(12*7={best_meas:.0f}) -> x{need / best_meas:4.2f}; "
          f"model ceiling*curv({best_model:.0f}) -> x{need / best_model:5.3f}")

# S6-D-D size-normalised version: shortfall 4.3x (range 0.8-8x) after isometric transfer of a 40 mm ray to 120 mm
for s in (0.8, 4.3, 8.0):
    print(f"   S6-D-D normalised shortfall x{s:3.1f}: after measured 12x locking -> x{s / 12:.2f} "
          f"({'closes' if s / 12 <= 1 else 'short'})")

# --- 3. Fixed-mass trade-off implied by Nguyen et al. 2017 rectangular-ray formulas (my algebra) ---
# Bn ~ E T^3 W / 12 ; Bt ~ E T W^3 / 12 ; gamma = Bt/Bn = (W/T)^2 ; area A = W T held fixed (fixed bone mass per length)
# => Bn = E A^2 / (12 sqrt(gamma)) ; Bt = E A^2 sqrt(gamma) / 12
print("\n3. Fixed cross-section area (fixed bone mass): passive Bn vs curvature-engaged ceiling, normalised to gamma=1")
for g in (1, 2, 4, 6, 10, 100):
    Bn = 1 / math.sqrt(g)
    Rinf = Bn * (1 + g)        # R_inf / R0 = 1 + gamma (Nguyen eq. 7), times the passive Bn
    print(f"   gamma={g:4d}  passive Bn x{Bn:5.2f}   curvature ceiling (Bn*(1+gamma)) x{Rinf:6.2f}")

# --- 4. Stiffness vs mass is not a binding trade-off on the floor: EI ~ d^4, mass ~ d^2 ---
print("\n4. Solid rod, E = 1 GPa (assumed; S6-D's basis): diameter for EI_req, and the cost of 2x diameter")
E = 1e9
d_req = (64 * EI_REQ / (math.pi * E)) ** 0.25
print(f"   d_req = {d_req * 1e3:.2f} mm ; doubling d multiplies EI by 16 and mass per length by 4")

# --- 5. Bilaminar coupling cap (S26 C4, textbook parallel-axis algebra): R = 1 + 3 (d/t)^2 ---
print("\n5. Hemitrich spacing d/t needed for a given full-coupling gain R")
for R in (12, 100, 166):
    print(f"   R={R:4d}  d/t = {math.sqrt((R - 1) / 3):.2f}")
