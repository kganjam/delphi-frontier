"""S6-D-D: attack the weakest input of S6-D (passive lepidotrichial ray under glide load).

CALCULATION ONLY. Nothing in this script is an observation. Every printed number is
computed from (a) S6-D's scenario ASSUMPTIONS, or (b) values quoted from sources whose
read-levels are given in S6-D-deepen.md.

S6-D model (reused unchanged): each of N rays per pectoral fin is a uniform
Euler-Bernoulli cantilever carrying an equal share of lift as a uniform load.
    P = n m g / (2N);  delta/L = P L^2 / (8 EI);  EI_req = P L^2 / (8 * LIMIT)
"""
import math

g = 9.81
# S6-D scenario: ASSUMPTIONS (not measured for any flying fish)
m, N, L, n, LIMIT = 0.10, 14, 0.12, 1.0, 0.10


def dl(EI, m_=m, N_=N, L_=L, n_=n):
    return (n_ * m_ * g / (2 * N_)) * L_**2 / (8 * EI)


P = n * m * g / (2 * N)
EI_req = P * L**2 / (8 * LIMIT)
print(f"[S6-D reproduced] P={P:.4f} N  EI_req={EI_req:.3e} N m^2")

# ---------------------------------------------------------------- 1. sensitivity
print("\n1. Sensitivity of S6-D's verdict metric R = EI_req/EI (R>1 means fails)")
EI0 = 3.8e-6  # the value S6-D's 'falls' rests on
R0 = EI_req / EI0
print(f"   baseline R at EI=3.8e-6: {R0:.0f}")
for name, f in [("EI x2", dict(EI=EI0 * 2)), ("EI /2", dict(EI=EI0 / 2)),
                ("L x2", dict(EI=EI0, L_=L * 2)), ("L /2", dict(EI=EI0, L_=L / 2)),
                ("m x2", dict(EI=EI0, m_=m * 2)), ("m /2", dict(EI=EI0, m_=m / 2)),
                ("N x2", dict(EI=EI0, N_=N * 2)), ("N /2", dict(EI=EI0, N_=N / 2))]:
    print(f"   {name:6s} R = {dl(**f)/LIMIT:7.1f}")
print("   -> no factor-2 change flips R=166 below 1. Factor-2 is not the threat; the")
print("      threat is the EI value itself (source choice x149) and its size transfer.")
print(f"   source choice: R at 565e-6 = {EI_req/565e-6:.2f} ; at 3.8e-6 = {EI_req/3.8e-6:.0f} ; ratio {565e-6/3.8e-6:.1f}x")

# ------------------------------------------------- 2. improved input: Alben 2007
# Quoted from Alben, Madden & Lauder 2007 (full-text, PMC2359861):
#   bluegill pectoral rays, maximum ray length 40.3 +/- 0.8 mm (mean +/- s.e., 6 fish)
#   three-point bending 'composite' E ~ 1e8 - 1e9 N m^-2, average I ~ 1e-6 cm^4
#   point force at 2/3 of ray length, force vs TIP deflection; both hemitrich
#   bases clamped: slope 1.98 N/m, 'about 12 times' the one-base-free value.
L_bg = 40.3e-3
I_bg = 1e-6 * 1e-8  # cm^4 -> m^4
EI_alben_lo, EI_alben_hi = 1e8 * I_bg, 1e9 * I_bg
print(f"\n2. Alben 2007 composite EI = E*I = {EI_alben_lo:.1e} .. {EI_alben_hi:.1e} N m^2 (order of magnitude)")
# Back-calculate EI from k = 1.98 N/m. Uniform cantilever, point load at a = 2L/3,
# tip deflection = F a^2 (3L - a) / (6 EI)  ->  EI = k a^2 (3L - a) / 6
# ASSUMPTIONS: uniform beam; tested length = 40.3 mm (the reported MAXIMUM, so an upper
# bound on L and hence on EI); linear part of the curve; the 12x ratio applies exactly.
for Lt in (L_bg, 0.75 * L_bg):
    a = 2 * Lt / 3
    EI_cl = 1.98 * a**2 * (3 * Lt - a) / 6
    print(f"   back-calc at tested L={Lt*1e3:.1f} mm: clamped EI={EI_cl:.2e}, free-base EI={EI_cl/12:.2e} N m^2")
a = 2 * L_bg / 3
EI_clamp = 1.98 * a**2 * (3 * L_bg - a) / 6
EI_free = EI_clamp / 12
for nm, v in [("Puri-relayed 3.8e-6", 3.8e-6), ("Flammang abstract 565e-6", 565e-6)]:
    lo, hi = v / max(EI_alben_hi, EI_clamp), v / EI_alben_lo
    print(f"   {nm}: {v/EI_alben_hi:.2g}x .. {v/EI_alben_lo:.3g}x the Alben E*I range")

# ---------------------------------------------- 3. size transfer to the 12 cm ray
print("\n3. Size-normalised comparison: EI/L^4 (Pa) = E (pi/64)(d/L)^4 for a solid section")
req_idx = EI_req / L**4
print(f"   requirement: EI_req/L^4 = {req_idx:.2f} Pa  (L = {L*1e3:.0f} mm)")
cands = {
    "Alben E*I low (1e-6)": EI_alben_lo,
    "Alben E*I high (1e-5)": EI_alben_hi,
    "Alben back-calc, one base free (passive)": EI_free,
    "Alben back-calc, both bases clamped (locked)": EI_clamp,
    "Puri-relayed 3.8e-6 (if a ~40 mm ray; length ASSUMED)": 3.8e-6,
    "Flammang abstract 565e-6 (if a ~40 mm ray; length ASSUMED)": 565e-6,
}
print(f"   {'candidate (bluegill, L_ray = 40.3 mm)':58s} EI/L^4   R_unscaled  R_isometric  dl_iso   b_flip")
for k, v in cands.items():
    idx = v / L_bg**4
    R_un = EI_req / v
    R_iso = req_idx / idx
    b_flip = math.log(R_un) / math.log(L / L_bg) if R_un > 1 else float("nan")
    print(f"   {k:58s} {idx:6.2f}  {R_un:9.1f}  {R_iso:10.2f}  {LIMIT*R_iso:6.3f}  {b_flip:6.2f}")
print("   R_isometric assumes EI scales as L^4 (geometric similarity, same tissue modulus).")
print("   b_flip = exponent in EI ~ L^b above which the scaled ray would meet the requirement.")

# solid-equivalent slenderness
for nm, v in [("required", EI_req)]:
    for E in (1e8, 1e9):
        d = (64 * v / (math.pi * E)) ** 0.25
        print(f"   {nm} solid-equivalent d at E={E:.0e}: {d*1e3:.2f} mm, d/L = {d/L*100:.2f} %")
d_bg = (64 * I_bg / math.pi) ** 0.25
print(f"   Alben I=1e-14 m^4 -> solid-equivalent d = {d_bg*1e3:.2f} mm, d/L = {d_bg/L_bg*100:.2f} % of 40.3 mm")

# ----------------------------------------- 4. load-distribution band (challenge 72)
print("\n4. With challenge-72 load-distribution factor 0.53 .. 1.47 on EI_req (isometric):")
for k in ("Alben back-calc, one base free (passive)", "Alben E*I low (1e-6)", "Alben E*I high (1e-5)"):
    R_iso = req_idx / (cands[k] / L_bg**4)
    print(f"   {k:45s} R_iso = {0.53*R_iso:.2f} .. {1.47*R_iso:.2f}")
