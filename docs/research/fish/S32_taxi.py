"""S32 - multi-stroke (taxi) launch: equations of motion for the airborne-body / immersed-lobe phase, integrated.

Run:  python3 docs/research/fish/S32_taxi.py
Every number quoted in S32-organism.md is printed by this script. No external data files.

MODEL (horizontal speed U of a body that is in AIR; only part of the lower caudal lobe is in WATER):

  m dU/dt = T_lobe(U) - D_wing(U) - D_body,air(U) - D_ind,lobe(U) - F_sigma,h

  T_lobe   = 1/2 rho_w S_imm [ G - C_D(Re) U^2 ]                      (Floryan et al. 2017 pitching-foil law,
             G = kappa * c6 * (f * A_pp)^2,  c6 = 2.55, C_D = 0.08       measured, Re 4780-9560;  St = f A_pp / U)
  vertical:  L_wing + F_z,lobe = W + F_sigma,v                        (body held airborne)
  L_wing   = 1/2 rho_a S_w U^2 CL,  CL = min(CL_max, W / (1/2 rho_a S_w U^2))
  D_wing   = 1/2 rho_a S_w U^2 (CD0 + k CL^2)
  F_z,lobe = 1/2 rho_w U^2 S_imm CLz,  must have CLz <= CLz_max, else the body cannot be held out of the water
  D_ind    = 1/2 rho_w U^2 S_imm CLz^2 / (pi e AR_eff),  AR_eff = 2 d^2 / S_imm (free-surface mirror image)
  F_sigma,v = 2 sigma c cos(theta)   (meniscus pull-down on a surface-piercing plate, both faces)
  F_sigma,h = 2 sigma c dcos         (contact-angle-hysteresis drag bound)

G is either CALIBRATED from the measured zebrafish burst (whole caudal fin thrust = body water drag at the
burst speed peak, where dU/dt = 0) or set KINEMATICALLY from an assumed amplitude. Both are reported.
"""
import math

RHO_W, RHO_A, NU_W, G0, SIGMA = 1000.0, 1.225, 1.0e-6, 9.81, 0.072
C6, CD_FLORYAN, RE_LO, RE_HI = 2.55, 0.08, 4780.0, 9560.0   # Floryan et al. 2017: pitching c6, C_D; measured Re span


def cd_lobe(U, c, mode):
    """Foil residual drag coefficient. 'const': 0.08 everywhere (as measured, extrapolated flat).
    'scaled': 0.08 inside the measured Re span, laminar-friction scaling (Re^-1/2) outside it."""
    if mode == "const":
        return CD_FLORYAN
    Re = max(U, 1e-6) * c / NU_W
    if Re < RE_LO:
        return CD_FLORYAN * math.sqrt(RE_LO / Re)
    if Re > RE_HI:
        return CD_FLORYAN * math.sqrt(RE_HI / Re)
    return CD_FLORYAN


def forces(U, p):
    W = p["m"] * G0
    q_a = 0.5 * RHO_A * U * U
    q_w = 0.5 * RHO_W * U * U
    CL = min(p["CLmax"], W / (q_a * p["Sw"])) if U > 0 else 0.0
    L_w = q_a * p["Sw"] * CL
    D_w = q_a * p["Sw"] * (p["CD0"] + p["k"] * CL * CL)
    D_b = q_a * p["Cd_body"] * p["A_front"]
    Fsv = 2 * SIGMA * p["c"] * p["costh"]
    Fsh = 2 * SIGMA * p["c"] * p["dcos"]
    need_z = max(0.0, W + Fsv - L_w)
    CLz = need_z / (q_w * p["S_imm"])
    AR = 2 * p["d"] ** 2 / p["S_imm"]
    D_i = q_w * p["S_imm"] * CLz * CLz / (math.pi * 0.8 * AR)
    T = 0.5 * RHO_W * p["S_imm"] * (p["G"] - cd_lobe(U, p["c"], p["cdmode"]) * U * U)
    return dict(T=T, D_w=D_w, D_b=D_b, D_i=D_i, Fsh=Fsh, CLz=CLz, L_w=L_w, W=W,
                net=T - D_w - D_b - D_i - Fsh)


def integrate(p, U0, f, tmax=3.0, dt=2e-5):
    """Explicit RK4 on dU/dt; x tracked. Stops at glide speed, at support failure, at equilibrium, or tmax."""
    U, x, t = U0, 0.0, 0.0
    F0 = forces(U, p)
    if F0["CLz"] > p["CLzmax"]:
        return dict(outcome="SUPPORT FAILS AT EXIT", U=U, t=0, x=0, strokes=0, F0=F0)
    a = lambda u: forces(u, p)["net"] / p["m"]
    while t < tmax:
        k1 = a(U); k2 = a(U + 0.5 * dt * k1); k3 = a(U + 0.5 * dt * k2); k4 = a(U + dt * k3)
        dU = dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += dt * (U + 0.5 * dU); U += dU; t += dt
        if U >= p["Vto"]:
            return dict(outcome="REACHES GLIDE SPEED", U=U, t=t, x=x, strokes=f * t, F0=F0)
        if forces(U, p)["CLz"] > p["CLzmax"]:
            return dict(outcome="SUPPORT FAILS", U=U, t=t, x=x, strokes=f * t, F0=F0)
        if abs(k1) < 1e-3 * G0 and t > 0.01:   # |a| < 1 mg: equilibrium
            return dict(outcome="STALLS (thrust = drag)", U=U, t=t, x=x, strokes=f * t, F0=F0)
    return dict(outcome="tmax", U=U, t=t, x=x, strokes=f * t, F0=F0)


def u_eq(p, lo=0.05, hi=60.0):
    """Speed at which net force crosses zero (bisection on net force, ignoring the support constraint)."""
    if forces(hi, p)["net"] > 0:
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if forces(mid, p)["net"] > 0:
            lo = mid
        else:
            hi = mid
    return lo


def vto(m, Sw, CLmax):
    return math.sqrt(2 * m * G0 / (RHO_A * Sw * CLmax))


# ------------------------------------------------------------------------------------------------ zebrafish
F_ZF = 52.0                 # Hz, measured max (EMG, escape; Kyriakatos 2011 via S24)
UB = 1.38                   # m/s, measured max burst (Miln 2021 via S28)
A_FRONT = 24e-6             # m^2, S28
C_FIN = 6.0e-3              # m, caudal fin length 5.6-6.5 mm, Wakamatsu 2019 FULL via S24 (used as lobe chord)
H_FIN = 9.0e-3              # m, caudal fin dorsoventral height ASSUMED (0.3 SL); no measurement found
S_CAUDAL = 0.7 * C_FIN * H_FIN   # m^2, ASSUMED taper factor 0.7 -> 37.8 mm^2 both lobes
S_LOBE = S_CAUDAL / 2
SW = 192e-6                 # m^2, S28 case C designed wing
CLMAX = 1.07


def G_calibrated(Cd_body, cdmode="scaled"):
    """Whole caudal fin thrust = body water drag at the measured burst peak U_b (dU/dt = 0 there).
    1/2 rho S_c (G - C_D U_b^2) = 1/2 rho Cd A U_b^2  ->  G = (Cd A / S_c + C_D) U_b^2.
    Assigns ALL burst thrust to the caudal fin (generous to the taxi)."""
    return (Cd_body * A_FRONT / S_CAUDAL + cd_lobe(UB, C_FIN, cdmode)) * UB ** 2


def zf_params(m, phi, G, cdmode, CD0, costh, dcos, CLzmax=1.0):
    return dict(m=m, Sw=SW, CLmax=CLMAX, CD0=CD0, k=1 / (math.pi * 0.8 * 5.0), Cd_body=0.3, A_front=A_FRONT,
                c=C_FIN, d=phi * H_FIN / 2, S_imm=phi * S_LOBE, G=G, cdmode=cdmode, costh=costh, dcos=dcos,
                CLzmax=CLzmax, Vto=vto(m, SW, CLMAX))


def hr(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)


hr("1. Inputs and derived geometry (zebrafish)")
for m in (0.25e-3, 0.40e-3):
    print(f"m = {m*1e3:.2f} g : W = {m*G0*1e3:.3f} mN, V_to (S_w 192 mm2, CL 1.07) = {vto(m, SW, CLMAX):.2f} m/s")
print(f"caudal fin area (assumed) = {S_CAUDAL*1e6:.1f} mm2, lower lobe = {S_LOBE*1e6:.1f} mm2, lobe depth = {H_FIN/2*1e3:.1f} mm")
print(f"lobe chord Re at 0.45 / 1.38 / 4.37 / 5.53 m/s = " +
      " / ".join(f"{u*C_FIN/NU_W:,.0f}" for u in (0.45, 1.38, 4.37, 5.53)) + f"   (Floryan measured {RE_LO:.0f}-{RE_HI:.0f})")
print(f"Weber number rho U^2 c / sigma at 0.45 / 1.38 / 4.37 = " + " / ".join(f"{RHO_W*u*u*C_FIN/SIGMA:.0f}" for u in (0.45, 1.38, 4.37)))
print(f"meniscus force bound 2 sigma c = {2*SIGMA*C_FIN*1e3:.3f} mN = {2*SIGMA*C_FIN/(0.25e-3*G0)*100:.0f}% of W(0.25 g), "
      f"{2*SIGMA*C_FIN/(0.40e-3*G0)*100:.0f}% of W(0.40 g)")
print(f"density ratio rho_w/rho_a = {RHO_W/RHO_A:.0f}  (body drag collapse on leaving water)")
D_water = 0.5 * RHO_W * 0.2 * A_FRONT * UB ** 2
D_air = 0.5 * RHO_A * 0.3 * A_FRONT * UB ** 2
print(f"body drag at 1.38 m/s: in water (Cd 0.2) {D_water*1e3:.2f} mN ; in air (Cd 0.3) {D_air*1e6:.2f} uN")

hr("2. Thrust parameter G = kappa c6 (f A_pp)^2  [m^2/s^2]")
for Cdb in (0.1, 0.2, 0.3):
    for mode in ("const", "scaled"):
        G = G_calibrated(Cdb, mode)
        fA = math.sqrt(G / C6)
        print(f"calibrated from burst, Cd_body {Cdb}, C_D {mode:6s}: G = {G:.3f}  -> equivalent f*A_pp (kappa=1) = {fA:.3f} m/s"
              f" -> A_pp at 52 Hz = {fA/F_ZF*1e3:.1f} mm")
for App in (6e-3, 8e-3, 12e-3):
    print(f"kinematic, A_pp {App*1e3:.0f} mm, 52 Hz, kappa 1: G = {C6*(F_ZF*App)**2:.3f}")
print("check: kinematic A_pp 8 mm (0.2 L) gives in-water whole-fin max speed against Cd 0.2 body drag of", end=" ")
G8 = C6 * (F_ZF * 8e-3) ** 2
lo, hi = 0.1, 5.0
for _ in range(100):
    mid = (lo + hi) / 2
    net = 0.5 * RHO_W * S_CAUDAL * (G8 - cd_lobe(mid, C_FIN, "const") * mid ** 2) - 0.5 * RHO_W * 0.2 * A_FRONT * mid ** 2
    lo, hi = (mid, hi) if net > 0 else (lo, mid)
print(f"{lo:.2f} m/s (measured max burst 1.38 m/s)")

hr("3. STEP 3 FIRST: is net force positive at the exit speed? (generous / central / stingy)")
SCEN = {
    "GENEROUS": dict(Cdb=0.3, phi=1.0, cdmode="scaled", CD0=0.08, costh=0.0, dcos=0.0, m=0.25e-3),
    "CENTRAL":  dict(Cdb=0.2, phi=0.5, cdmode="scaled", CD0=0.12, costh=0.5, dcos=0.1, m=0.25e-3),
    "STINGY":   dict(Cdb=0.1, phi=0.25, cdmode="const", CD0=0.20, costh=1.0, dcos=0.3, m=0.40e-3),
}
for name, s in SCEN.items():
    G = G_calibrated(s["Cdb"], s["cdmode"])
    p = zf_params(s["m"], s["phi"], G, s["cdmode"], s["CD0"], s["costh"], s["dcos"])
    for U0 in (0.45, 1.38):
        F = forces(U0, p)
        print(f"{name:8s} U0 {U0:.2f}: T {F['T']*1e3:6.3f} mN | D_wing {F['D_w']*1e3:.3f} D_ind,lobe {F['D_i']*1e3:.3f} "
              f"F_sigma,h {F['Fsh']*1e3:.3f} D_body,air {F['D_b']*1e6:.2f}uN | NET {F['net']*1e3:+.3f} mN "
              f"| wing lift {F['L_w']/F['W']*100:4.1f}% W | lobe CLz needed {F['CLz']:.2f}")

hr("4. Integrated trajectories (RK4), calibrated thrust")
for name, s in SCEN.items():
    G = G_calibrated(s["Cdb"], s["cdmode"])
    p = zf_params(s["m"], s["phi"], G, s["cdmode"], s["CD0"], s["costh"], s["dcos"])
    for U0 in (0.45, 1.38):
        r = integrate(p, U0, F_ZF)
        print(f"{name:8s} m {s['m']*1e3:.2f} g V_to {p['Vto']:.2f}  U0 {U0:.2f}: {r['outcome']:28s} U_end {r['U']:.2f} m/s "
              f"t {r['t']*1e3:7.1f} ms  x {r['x']*100:6.1f} cm  strokes {r['strokes']:6.1f}  "
              f"wing lift at U_end {min(1,(r['U']/p['Vto'])**2)*100:4.1f}% W")
    print(f"{name:8s} equilibrium speed (support ignored) U_eq = {u_eq(p):.2f} m/s = {u_eq(p)/p['Vto']*100:.0f}% of V_to")

hr("4b. Trajectory table, GENEROUS, U0 1.38 (every 2 strokes)")
s = SCEN["GENEROUS"]; G = G_calibrated(s["Cdb"], s["cdmode"])
p = zf_params(s["m"], s["phi"], G, s["cdmode"], s["CD0"], s["costh"], s["dcos"])
U, x, t, dt = 1.38, 0.0, 0.0, 2e-5
nxt = 0
while t <= 40 / F_ZF + 1e-9:
    if t >= nxt / F_ZF - 1e-12:
        F = forces(U, p)
        print(f"stroke {nxt:3d}  t {t*1e3:6.1f} ms  x {x*100:6.2f} cm  U {U:.3f} m/s  T {F['T']*1e3:.3f}  net {F['net']*1e3:+.3f} mN"
              f"  lift {min(1,(U/p['Vto'])**2)*100:4.1f}% W")
        nxt += 2 if nxt < 10 else 10
    a = lambda u: forces(u, p)["net"] / p["m"]
    k1 = a(U); k2 = a(U + 0.5 * dt * k1); k3 = a(U + 0.5 * dt * k2); k4 = a(U + dt * k3)
    dU = dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; x += dt * (U + 0.5 * dU); U += dU; t += dt

hr("5. Sensitivity: equilibrium speed U_eq, one factor at a time from GENEROUS (m 0.25 g, V_to 4.37)")
base = SCEN["GENEROUS"]
def ueq_of(**kw):
    s = dict(base); s.update(kw)
    G = kw.get("G", G_calibrated(s["Cdb"], s["cdmode"]))
    p = zf_params(s["m"], s["phi"], G, s["cdmode"], s["CD0"], s["costh"], s["dcos"])
    return u_eq(p), p["Vto"]
print(f"GENEROUS base                       U_eq {ueq_of()[0]:.2f}")
for k, vals in dict(Cdb=(0.1, 0.2, 0.3), phi=(0.25, 0.5, 1.0), cdmode=("const", "scaled"), CD0=(0.08, 0.2),
                    costh=(0, 0.5, 1.0), dcos=(0, 0.3), m=(0.25e-3, 0.40e-3)).items():
    print(f"{k:7s}: " + "  ".join(f"{v}->{ueq_of(**{k: v})[0]:.2f}" for v in vals))
Gg = G_calibrated(0.3, "scaled")
print("thrust multiplier on calibrated G (airborne tail beating harder than in its best burst):")
for mult in (1.0, 1.5, 2.0, 3.0, 4.0):
    ue, V = ueq_of(G=Gg * mult)
    print(f"  G x {mult:.1f} (A_pp x {math.sqrt(mult):.2f}): U_eq {ue:.2f} m/s ({ue/V*100:.0f}% of V_to {V:.2f})")
# multiplier needed
for mname, m in (("0.25 g", 0.25e-3), ("0.40 g", 0.40e-3)):
    for mode in ("scaled", "const"):
        lo, hi = 1.0, 100.0
        for _ in range(100):
            mid = (lo + hi) / 2
            ue, V = ueq_of(G=G_calibrated(0.3, mode) * mid, m=m, cdmode=mode)
            lo, hi = (lo, mid) if ue >= V else (mid, hi)
        print(f"  {mname}, C_D {mode}: G multiplier needed for U_eq = V_to: x{hi:.2f}  (A_pp or f x {math.sqrt(hi):.2f})")

hr("5b. Kinematic thrust instead of calibrated (GENEROUS otherwise), kappa = 1 and 0.5")
for App in (6e-3, 8e-3, 12e-3, 15e-3):
    for kap in (1.0, 0.5):
        ue, V = ueq_of(G=kap * C6 * (F_ZF * App) ** 2)
        print(f"A_pp {App*1e3:4.0f} mm kappa {kap}: U_eq {ue:.2f} m/s ({ue/V*100:.0f}% V_to)")

hr("5c. Hypothetical: G x multiplier just sufficient (GENEROUS, 0.25 g) -> strokes, distance, time")
for mult in (2.0, 2.5, 3.0, 4.0):
    s = dict(base); p = zf_params(s["m"], s["phi"], Gg * mult, s["cdmode"], s["CD0"], s["costh"], s["dcos"])
    r = integrate(p, 1.38, F_ZF, tmax=5.0)
    print(f"G x {mult}: {r['outcome']:26s} U {r['U']:.2f}  t {r['t']*1e3:.0f} ms  x {r['x']:.2f} m  strokes {r['strokes']:.0f}")

hr("5d. Weight support alone: minimum speed at which the immersed lobe can hold the body up (CLz <= 1)")
for name, s in SCEN.items():
    G = G_calibrated(s["Cdb"], s["cdmode"])
    p = zf_params(s["m"], s["phi"], G, s["cdmode"], s["CD0"], s["costh"], s["dcos"])
    lo, hi = 0.01, 5.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if forces(mid, p)["CLz"] > 1.0 else (lo, mid)
    print(f"{name:8s}: U_support,min = {hi:.2f} m/s (S_imm {p['S_imm']*1e6:.1f} mm2)")

# ------------------------------------------------------------------------------------------------ exocoetid
hr("6. Exocoetid with the SAME equations (Cypselurus fits, Fish 1990 Tables I-II; kinematics assumed)")
def exo(M, phi, App, cdmode, f=50.0, c=0.025, U0=10.0, CD0=0.08):
    WL = 285.015 * M ** 0.400
    Sw = M * G0 / WL
    S_h = 0.003 * M ** 0.650                       # hypocaudal lobe area, Fish 1990 Table I (decimal restored)
    G = C6 * (f * App) ** 2
    d = phi * S_h / c                              # immersed depth if chord c (assumed)
    p = dict(m=M, Sw=Sw, CLmax=CLMAX, CD0=CD0, k=1 / (math.pi * 0.8 * 5.0), Cd_body=0.3,
             A_front=(0.6 * 0.46 * M ** 0.355 * 0.15) ** 2, c=c, d=d, S_imm=phi * S_h, G=G, cdmode=cdmode,
             costh=1.0, dcos=0.3, CLzmax=1.0, Vto=vto(M, Sw, CLMAX))
    return p, WL, S_h
for M in (0.191, 0.300):
    for App in (0.020, 0.026, 0.031):
        for mode in ("const", "scaled"):
            p, WL, S_h = exo(M, 0.5, App, mode)
            r = integrate(p, 10.0, 50.0, tmax=5.0, dt=1e-4)
            F = forces(10.0, p)
            print(f"M {M*1e3:.0f} g WL {WL:.0f} V_to {p['Vto']:.1f} S_hypo {S_h*1e4:.1f} cm2 | A_pp {App*100:.1f} cm C_D {mode:6s}"
                  f" | NET@10 {F['net']:+.3f} N (W {F['W']:.2f}) U_eq {u_eq(p):5.1f} | {r['outcome']:24s} t {r['t']:.2f} s"
                  f" x {r['x']:.1f} m strokes {r['strokes']:.0f}")
p, WL, S_h = exo(0.191, 0.5, 0.026, "scaled")
print(f"meniscus bound 2 sigma c for c 2.5 cm = {2*SIGMA*0.025*1e3:.1f} mN = {2*SIGMA*0.025/(0.191*G0)*100:.2f}% of W")
print(f"lobe Re at 10 / 16 m/s = {10*0.025/NU_W:,.0f} / {16*0.025/NU_W:,.0f}  (Floryan measured {RE_LO:.0f}-{RE_HI:.0f})")
# power consistency check against Deng 2019 abstract: 36 W at 10 m/s, 50 Hz, 15 deg
for App in (0.020, 0.026, 0.031):
    for phi in (0.25, 0.5):
        S = phi * 0.003 * 0.191 ** 0.65
        St = 50 * App / 10.0; fstar = 50 * 0.025 / 10.0
        CP = 7.78 * St ** 2 + 4.89 * St ** 2 * fstar          # Floryan pitching power law, c8, c9
        print(f"power check A_pp {App*100:.1f} cm phi {phi}: St {St:.2f} P = {0.5*RHO_W*10**3*S*CP:.0f} W (Deng CFD abstract: 36 W)")

hr("7. Dimensionless scaling of the taxi ceiling U_max = sqrt(G / C_D)  (foil alone, no other drag)")
for label, fApp, c, V in (("zebrafish 0.25 g, calibrated", math.sqrt(G_calibrated(0.3, 'scaled') / C6), C_FIN, 4.37),
                          ("zebrafish 0.25 g, A_pp 8 mm", F_ZF * 8e-3, C_FIN, 4.37),
                          ("exocoetid 191 g, A_pp 2.6 cm", 50 * 0.026, 0.025, vto(0.191, 0.191*G0/(285.015*0.191**0.4), CLMAX)),
                          ("exocoetid 300 g, A_pp 3.1 cm", 50 * 0.031, 0.025, vto(0.300, 0.300*G0/(285.015*0.300**0.4), CLMAX))):
    for mode in ("const", "scaled"):
        U = 1.0
        for _ in range(200):
            U = math.sqrt(C6 * fApp ** 2 / cd_lobe(U, c, mode))
        print(f"{label:30s} fA_pp/V_to {fApp/V:.3f}  C_D {mode:6s} {cd_lobe(U, c, mode):.4f}  U_max {U:5.2f} m/s = {U/V:.2f} V_to")
