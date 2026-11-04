"""Claim 21 entailment arithmetic. Run with: python3 -I claim-21-entail_calc.py

Everything printed here is a CALCULATION. Inputs are labelled with their origin.
"""

# Claim 21 (S21, derived): U = Re * nu / L
RE, RE_SEM = 27_800, 2_140          # Danos & Lauder 2012, measured (relayed via S21, full-text there)
L = 0.033                            # m, mean TL, same source
NU = 1.0e-6                          # m^2/s, S21's assumption (1 mPa s / 1000 kg m^-3)

U = {k: r * NU / L for k, r in [("lo", RE - RE_SEM), ("mid", RE), ("hi", RE + RE_SEM)]}
print("U (m/s):", {k: round(v, 3) for k, v in U.items()})

# --- O1 energetic: kinetic-energy-only floor on mean muscle power during acceleration ---
# P_muscle >= 0.5 * U^2 * (1 + k_added) / (f_muscle * t_acc)
# t_acc bracket from Demesmay et al. 2025 (adult zebrafish, 240 fps; author values):
#   first movement -> max head turn 13 +/- 5 ms; "latency to attain maximal speed" 8 +/- 4 ms
#   (reference point of the 8 ms is ambiguous in the text read; bracket 8 .. 21 ms)
# f_muscle (axial fast muscle / body mass): ASSUMED 0.4 .. 0.6 (no zebrafish value found)
# k_added: set 0 for the floor (any added mass or wake loss only raises the requirement)
cases = []
for u_key in ("lo", "mid", "hi"):
    for t in (0.021, 0.013, 0.008):
        for f in (0.6, 0.4):
            p = 0.5 * U[u_key] ** 2 / (f * t)
            cases.append((u_key, t, f, p))
ps = [c[3] for c in cases]
print(f"O1 KE-only floor, W/kg muscle: min {min(ps):.0f}, max {max(ps):.0f}")
for u_key, t, f, p in cases:
    if u_key == "mid":
        print(f"   U=mid t={t*1e3:.0f} ms f={f}: {p:.0f} W/kg")
print("   body-specific KE at U_mid (J/kg):", round(0.5 * U["mid"] ** 2, 3))
# Comparator: Mead et al. 2020, 5-dpf LARVAL tail, 28 C, net work-loop power 134.4 +/- 19.9 W/kg (80 Hz)
for eff in (1.0, 0.5, 0.3):
    lo_req = min(ps) / eff
    hi_req = max(ps) / eff
    print(f"   if only {eff:.0%} of muscle work becomes body KE: requirement {lo_req:.0f}-{hi_req:.0f} W/kg")

# Same arithmetic at the OTHER adult measurement, for contrast (Demesmay 1.57 m/s mean, author value)
p_dem = [0.5 * 1.57 ** 2 / (f * t) for t in (0.021, 0.008) for f in (0.6, 0.4)]
print(f"   (contrast) at 1.57 m/s: {min(p_dem):.0f}-{max(p_dem):.0f} W/kg")

# --- O3 conservation: impulse per kg body that must be shed to the water ---
for k in (0.0, 0.2):
    print(f"O3 impulse/mass with k_added={k}: {(1+k)*U['lo']:.2f}-{(1+k)*U['hi']:.2f} N s/kg")

# --- E1 range: factor-2 tolerance around the claim's mid value ---
print("E1 band (m/s):", round(U["mid"] / 2, 2), "-", round(U["mid"] * 2, 2))
