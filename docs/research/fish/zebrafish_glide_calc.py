"""Arithmetic behind docs/research/fish/zebrafish-glide-physics.md.

Every number printed here is CALCULATED from the stated inputs. None is observed.
Run: python3 docs/research/fish/zebrafish_glide_calc.py
"""
import math

NU = 1.5e-5      # m^2/s, kinematic viscosity of air (given in the brief)
RHO = 1.2        # kg/m^3, air density near sea level, ~20 C (assumed)
G = 9.81         # m/s^2
M = 0.4e-3       # kg, zebrafish mass (given in the brief)
W = M * G        # N
BL = 0.04        # m, standard length (given in the brief)

print(f"W = {M} kg * {G} m/s^2 = {W:.4e} N\n")

# ---- 1. Reynolds number grid -------------------------------------------
print("1. Re = V*c/nu")
chords = [0.005, 0.01, 0.02, 0.03]
speeds = [1, 2, 4, 8]
print("c (cm) | " + " | ".join(f"V={v} m/s" for v in speeds))
for c in chords:
    print(f"{c*100:.1f} | " + " | ".join(f"{v*c/NU:,.0f}" for v in speeds))
print()

# ---- 2. Wing loading ----------------------------------------------------
print("2. S = 2W/(rho V^2 CL); b = sqrt(AR*S); c = sqrt(S/AR)")
for CL in (0.6, 1.0):
    print(f"-- CL = {CL}")
    for v in speeds:
        q = 0.5 * RHO * v**2
        S = W / (q * CL)
        row = [f"V={v}: q={q:.2f} Pa, S={S*1e4:.2f} cm^2, W/S={W/S:.2f} N/m^2"]
        for AR in (3, 5, 8):
            b = math.sqrt(AR * S)
            c = math.sqrt(S / AR)
            row.append(f"AR{AR}: b={b*100:.2f} cm={b/BL:.2f} BL, c={c*100:.2f} cm, Re={v*c/NU:,.0f}")
        print("   " + "\n   ".join(row))
print()

# ---- 3. Ballistics ------------------------------------------------------
print("3. h_max = v^2/(2g) (vertical exit); R_max = v^2/g (45 deg, no drag)")
for label, v in [("Ucrit Tudorache", 0.548), ("Ucrit Plaut (secondary)", 0.560),
                 ("assumed 20 BL/s", 20 * BL), ("assumed 30 BL/s", 30 * BL)]:
    print(f"{label}: v={v:.3f} m/s, h={v**2/(2*G)*100:.2f} cm, R={v**2/G*100:.2f} cm, "
          f"KE={0.5*M*v**2*1e3:.3f} mJ")
print("Drop height needed to reach glide speed V from rest: h = V^2/(2g)")
for v in speeds:
    print(f"  V={v}: h={v**2/(2*G):.3f} m")
print("Speed needed to glide with span b (AR 5, CL 0.6): V = sqrt(2W/(rho S CL)), S=b^2/AR")
for nbl in (0.5, 1, 2, 3):
    b = nbl * BL
    S = b * b / 5
    V = math.sqrt(2 * W / (RHO * S * 0.6))
    print(f"  span {nbl} BL: S={S*1e4:.2f} cm^2, V={V:.2f} m/s, "
          f"V/0.56={V/0.56:.1f}, KE ratio={(V/0.56)**2:.0f}")
we = 1000 * 0.56**2 * BL / 0.072
print(f"Weber number at water exit, rho_w v^2 L / sigma = 1000*0.56^2*0.04/0.072 = {we:.0f}")
print()

# ---- 4. Power -----------------------------------------------------------
print("4. Forward flapping flight, quasi-steady lower bound")
K = 1.2          # induced-power factor (assumed)
CD_PRO = 0.08    # wing profile drag coeff at Re ~1e3-1e4 (assumed, see report)
A_BODY = 3.0e-5  # m^2 body frontal area (assumed: ~0.8 cm x 0.5 cm ellipse)
CD_BODY = 0.4    # (assumed)
AR = 5
for nbl in (1, 2, 3):
    b = nbl * BL
    S = b * b / AR
    best = None
    for i in range(1, 2001):
        V = i * 0.01
        CL = 2 * W / (RHO * S * V**2)
        if CL > 0.6:
            continue
        Pi = K * 2 * W**2 / (RHO * math.pi * b**2 * V)
        Pp = 0.5 * RHO * V**3 * S * CD_PRO
        Pb = 0.5 * RHO * V**3 * A_BODY * CD_BODY
        P = Pi + Pp + Pb
        if best is None or P < best[0]:
            best = (P, V, CL, Pi, Pp, Pb)
    P, V, CL, Pi, Pp, Pb = best
    print(f"span {nbl} BL (b={b*100:.0f} cm, S={S*1e4:.2f} cm^2): Pmin at V={V:.2f} m/s, CL={CL:.2f}; "
          f"Pind={Pi*1e3:.3f} mW, Ppro={Pp*1e3:.3f} mW, Ppar={Pb*1e3:.3f} mW, "
          f"total={P*1e3:.3f} mW = {P/M:.1f} W/kg body")
    for frac in (0.10, 0.25):
        print(f"    flight-muscle fraction {frac:.2f}: {P/(frac*M):.0f} W/kg muscle; "
              f"ratio vs 30 W/kg = {P/(frac*M)/30:.1f}; vs 142.7 W/kg = {P/(frac*M)/142.7:.2f}")

print("\nHover (takeoff from water exit at ~0.6 m/s requires near-hover lift)")
for nbl in (1, 2, 3):
    b = nbl * BL
    S = b * b / AR
    Ad = math.pi * b**2 / 4      # full actuator disc (stroke 180 deg) - most favourable
    Pi = K * math.sqrt(W**3 / (2 * RHO * Ad))
    # Wing must generate W at mean relative speed U: W = 0.5 rho U^2 S CL, CL = 1.0
    # (hover CL with leading-edge vortex, optimistic), profile power = 0.5 rho U^3 S CD,
    # CD_hover taken = 1.0 (separated flow at high angle of attack; assumed).
    U = math.sqrt(2 * W / (RHO * S * 1.0))
    Pp = 0.5 * RHO * U**3 * S * 1.0 * 0.5   # factor 0.5: crude stroke-averaging (assumed)
    P = Pi + Pp
    print(f"span {nbl} BL: Ad={Ad*1e4:.1f} cm^2, Pind={Pi*1e3:.2f} mW, U_wing={U:.2f} m/s, "
          f"Ppro={Pp*1e3:.2f} mW, total={P*1e3:.2f} mW = {P/M:.0f} W/kg body; "
          f"@25% muscle {P/(0.25*M):.0f} W/kg muscle, ratio vs 30 = {P/(0.25*M)/30:.1f}, "
          f"vs 142.7 = {P/(0.25*M)/142.7:.2f}")
