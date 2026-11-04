"""S24 surface-taxiing arithmetic. Every output is a CALCULATION, not an observation.

Inputs tagged M = measured (literature), A = assumption. See S24-behaviour.md for sources.
Run: python3 S24_calcs.py
"""
import math

g = 9.81
rho_w, mu_w = 1000.0, 1.0e-3        # water ~20-28 C (A)
nu_w = mu_w / rho_w
rho_a = 1.2                          # air (A)
m = 0.4e-3                           # kg, project premise
W = m * g
TL = 0.04                            # m, project premise

print("W = %.3f mN" % (W * 1e3))

# 1. Adult burst speed back-calculated from Danos & Lauder 2012 Re (M: Re 27,800 +/- 2140 sem,
#    TL 33.0 mm, 1 mPa s). Length basis stated only as "fish length"; TL assumed, SL=0.8TL bracket (A).
print("\n1. Burst speed from Danos & Lauder Reynolds numbers")
for mu, Re, sem in ((1e-3, 27800, 2140), (10e-3, 2350, 160), (20e-3, 820, 60)):
    for Lname, L in (("TL 33 mm", 0.033), ("SL ~26.4 mm (A)", 0.033 * 0.8)):
        U = Re * mu / (rho_w * L)
        dU = sem * mu / (rho_w * L)
        print("  mu=%4.0f mPa s  L=%-16s U=%.3f +/- %.3f m/s  (%.1f L/s)" % (mu * 1e3, Lname, U, dU, U / L))
U_burst = 27800 * 1e-3 / (rho_w * 0.033)

targets = {"3-BL wing": 1.95, "1-BL wing": 5.84}

# 2. Strouhal (kinematic) ceiling: thrust-producing flapping needs St = fA/U ~ 0.2-0.4 (M, Taylor 2003);
#    0.15 used as a generous lower edge (A). A = peak-to-peak tail amplitude, 0.15-0.25 TL (A).
print("\n2. Tail-beat frequency needed, f = St*U/A")
fA_ucrit = [(St, St * 0.548) for St in (0.2, 0.3, 0.4)]
for St, fA in fA_ucrit:
    print("  at Ucrit 0.548 m/s, St %.1f -> fA = %.3f m/s -> at 21 Hz A = %.1f mm (%.2f TL)" % (St, fA, fA / 21 * 1e3, fA / 21 / TL))
for name, U in targets.items():
    for A_frac in (0.15, 0.20, 0.25):
        A = A_frac * TL
        row = ["St %.2f: %5.0f Hz" % (St, St * U / A) for St in (0.15, 0.2, 0.3, 0.4)]
        print("  %s U=%.2f  A=%.2f TL (%.0f mm): %s" % (name, U, A_frac, A * 1e3, " | ".join(row)))
# Inverse: max taxi speed at the measured frequency ceilings
print("  Max U = f*A/St:")
for f in (21, 52):
    for A_frac, St in ((0.20, 0.3), (0.25, 0.15), (0.15, 0.4)):
        print("    f=%d Hz A=%.2f TL St=%.2f -> U=%.2f m/s" % (f, A_frac, St, f * A_frac * TL / St))
# Exocoetid consistency check: 0.25 m fish at 10 m/s, A = 0.2 L, St 0.3
print("  exocoetid check: f = 0.3*10/(0.2*0.25) = %.0f Hz" % (0.3 * 10 / (0.2 * 0.25)))

# 3. Steady thrust capacity at Ucrit = whole-body drag at Ucrit (A: wetted area 6 cm^2,
#    laminar Blasius Cf, form factor 1.2, undulation drag multiplier 1-3).
print("\n3. Thrust at Ucrit (= drag)")
S_wet, L_body = 6e-4, 0.032
for U in (0.548, 0.236):   # Palstra 2010 and Wakamatsu 2019 (26 C, PET) Ucrit
    Re = U * L_body / nu_w
    Cf = 1.328 / math.sqrt(Re)
    D = 0.5 * rho_w * U**2 * S_wet * Cf * 1.2
    print("  U=%.3f Re=%.0f Cf=%.4f D_rigid=%.2f mN, x3 undulation=%.2f mN" % (U, Re, Cf, D * 1e3, 3 * D * 1e3))

# 4. Force budget at end of taxi (wings carry W). Air drag = W/(L/D), L/D 4-8 (A).
#    Submerged lower caudal lobe: chord 6 mm (M: Wakamatsu caudal fin length 5.6-6.5 mm, short-fin strains),
#    area per side 0.15-0.30 cm^2 (A), laminar two-sided friction only (pressure/ventilation/spray omitted).
print("\n4. Thrust needed at taxi end speed")
c = 0.006
for name, U in targets.items():
    q = 0.5 * rho_w * U**2
    Re = U * c / nu_w
    Cf2 = 2 * 1.328 / math.sqrt(Re)
    for LD in (8, 4):
        for S_lobe in (0.15e-4, 0.30e-4):
            D_air = W / LD
            D_lobe = q * S_lobe * Cf2
            T = D_air + D_lobe
            P = [T * U / eta for eta in (0.5, 0.2)]
            print("  %s U=%.2f L/D=%d lobe=%.2f cm2: D_air=%.2f D_lobe=%.2f T=%.2f mN; P(eta .5/.2)=%.1f/%.1f mW = %.0f/%.0f W/kg body"
                  % (name, U, LD, S_lobe * 1e4, D_air * 1e3, D_lobe * 1e3, T * 1e3, P[0] * 1e3, P[1] * 1e3, P[0] / m, P[1] / m))

# 5. Weight the wings carry during the taxi, fraction (U/Vg)^2 (level-flight lift scaling).
print("\n5. Wing-borne fraction of weight at taxi start")
for U0 in (0.548, U_burst):
    for name, Vg in targets.items():
        print("  U0=%.3f %s: %.1f %% of W; tail/planing must carry %.1f %%" % (U0, name, 100 * (U0 / Vg)**2, 100 * (1 - (U0 / Vg)**2)))

# 6. Taxi run length and time for an assumed constant NET force (A: 0.5, 1, 2 mN).
print("\n6. Taxi distance/time, U_burst -> target, constant net force")
for name, U in targets.items():
    for F in (0.5e-3, 1e-3, 2e-3):
        d = m * (U**2 - U_burst**2) / (2 * F)
        t = m * (U - U_burst) / F
        print("  %s F_net=%.1f mN: %.2f m (%.0f BL), %.2f s, %.0f tail beats at 52 Hz" % (name, F * 1e3, d, d / TL, t, 52 * t))

# 7. Ratios used in the text
print("\n7. Ratios")
for name, U in targets.items():
    print("  %s: U/Ucrit(0.548)=%.2f  U/U_burst(%.3f)=%.2f  KE ratio vs burst=%.1f" % (name, U / 0.548, U_burst, U / U_burst, (U / U_burst)**2))
print("  Makiguchi leap 3.9-5.2 m/s; 52 Hz/21 Hz = %.2f" % (52 / 21))
print("  Froude U/sqrt(gL): zebrafish 1.95 m/s L=0.04: %.2f; 5.84: %.2f; exocoetid 10 m/s L=0.25: %.2f"
      % (1.95 / math.sqrt(g * 0.04), 5.84 / math.sqrt(g * 0.04), 10 / math.sqrt(g * 0.25)))
