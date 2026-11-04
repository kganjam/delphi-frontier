"""Independent re-derivation for claim 273 (S32 sec 4.2: run the taxi equations on a flying fish).

Written from the equations in S32-organism.md sec 1 and primary inputs only; S32_taxi.py was NOT read or run.
All outputs are CALCULATED, not observed.
  python3 docs/research/fish/replicate_273_taxi.py
"""
import itertools, math

RHO_W, RHO_A, NU, G0, SIGMA = 1025.0, 1.225, 1.0e-6, 9.81, 0.072
C6, CD_FLORYAN, RE_FLORYAN = 2.55, 0.08, 4780.0  # Floryan et al. 2017 pitching, measured at 60 mm/s, c = 80 mm (full text)
CLMAX = 1.07

def cyps(M):  # Fish 1990, Cypselurus, M in kg (project transcription of page images)
    return dict(S_lobe=0.003 * M ** 0.650, WL=285.015 * M ** 0.400, AR=12.717 * M ** 0.163)

def run(M, App, phi, CD0, cd_mode, AR_wing, f=50.0, chord=0.025, A_front=5.9e-4, kappa=1.0,
        U0=10.0, dcos=0.3, t_end=30.0, dt=1e-4):
    p = cyps(M); W = M * G0
    S_w = W / p["WL"]; Vto = math.sqrt(2 * p["WL"] / (RHO_A * CLMAX))
    S_imm = phi * p["S_lobe"]; span = p["S_lobe"] / chord; d = phi * span
    AR_eff = 2 * d * d / S_imm
    k = 1 / (math.pi * 0.8 * AR_wing)
    Gk = kappa * C6 * (f * App) ** 2
    def cd(U):
        if cd_mode == "const":
            return CD_FLORYAN
        Re = U * chord / NU
        return CD_FLORYAN * math.sqrt(RE_FLORYAN / Re) if Re > RE_FLORYAN else CD_FLORYAN
    def acc(U):
        q_a = 0.5 * RHO_A * U * U; q_w = 0.5 * RHO_W * U * U
        CL = min(CLMAX, W / (q_a * S_w)); L = q_a * S_w * CL
        need = max(0.0, W + 2 * SIGMA * chord - L)  # meniscus pull-down bound, cos(theta)=1
        CLz = need / (q_w * S_imm)
        T = 0.5 * RHO_W * S_imm * (Gk - cd(U) * U * U)
        D = q_a * S_w * (CD0 + k * CL * CL) + 0.5 * RHO_A * 0.3 * A_front * U * U \
            + q_w * S_imm * CLz ** 2 / (math.pi * 0.8 * AR_eff) + 2 * SIGMA * chord * dcos
        return (T - D) / M, CLz
    ceil = None  # highest speed in [2, 40] m/s at which net horizontal force is still >= 0
    for i in range(4000, 199, -1):
        U = i * 0.01
        if acc(U)[0] >= 0:
            ceil = round(U, 2); break
    t, U, x = 0.0, U0, 0.0
    a0 = acc(U0)[0]
    while t < t_end:
        if U >= Vto:
            return dict(Vto=Vto, ceil=ceil, a0=a0, t=t, x=x, reached=True)
        if acc(U)[1] > 1.0:
            return dict(Vto=Vto, ceil=ceil, a0=a0, t=t, x=x, reached=False, why="CLz>1")
        k1 = acc(U)[0]; k2 = acc(U + 0.5 * dt * k1)[0]; k3 = acc(U + 0.5 * dt * k2)[0]; k4 = acc(U + dt * k3)[0]
        x += U * dt; U += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; t += dt
        if abs(k1) < 1e-3 * G0 and U < Vto:
            return dict(Vto=Vto, ceil=ceil, a0=a0, t=t, x=x, reached=False, why="equilibrium")
    return dict(Vto=Vto, ceil=ceil, a0=a0, t=t, x=x, reached=False, why="timeout")

if __name__ == "__main__":
    for M in (0.191, 0.300):
        p = cyps(M)
        print(f"M={M} kg: S_lobe={p['S_lobe']*1e4:.2f} cm2  WL={p['WL']:.1f} N/m2  V_to={math.sqrt(2*p['WL']/(RHO_A*CLMAX)):.2f} m/s  AR_fish={p['AR']:.2f}")
    print("M     App   phi  CD0   cd     ARw   | a0[g]   ceil[m/s] reached t[s]  x[m]")
    for M, App, phi, CD0, mode, arw in itertools.product((0.191, 0.300), (0.020, 0.031, 0.013), (0.5, 1.0),
                                                         (0.08, 0.20), ("scaled", "const"), ("5",)):
        AR = 5.0 if arw == "5" else cyps(M)["AR"]
        r = run(M, App, phi, CD0, mode, AR)
        print(f"{M:.3f} {App*100:4.1f}cm {phi:.2f} {CD0:.2f} {mode:6s} {arw:4s} | {r['a0']/G0:+.3f}  {str(r['ceil']):8s} "
              f"{str(r['reached']):5s} {r['t']:.3f} {r['x']:.2f} {r.get('why','')}")
    # Variant matching S32's stated conventions (rho_w/rho_a = 816 -> rho_w = 1000; C_D held at 0.08 up to Re 9,560,
    # the top of the span S32 quotes) -- added AFTER the independent grid above, for the comparison only.
    print("\nS32-convention variant (rho_w 1000, Re_ref 9560), M 0.191, phi 0.5:")
    RHO_W, RE_FLORYAN = 1000.0, 9560.0
    globals().update(RHO_W=RHO_W, RE_FLORYAN=RE_FLORYAN)
    for App, mode, CD0 in itertools.product((0.026, 0.031), ("const", "scaled"), (0.08, 0.20)):
        r = run(0.191, App, 0.5, CD0, mode, 5.0)
        print(f"  A_pp {App*100:.1f} cm {mode:6s} CD0 {CD0:.2f}: ceiling {r['ceil']} m/s, reached V_to={r['reached']}, "
              f"t {r['t']:.2f} s, x {r['x']:.1f} m, strokes {r['t']*50:.0f}")
    # Floryan pitching power law, C_P = c8 St^2 + c9 St^2 f*, at 10 m/s, 50 Hz, A_pp 2.6 cm, phi 0.5, c 2.5 cm
    U, f, App, c = 10.0, 50.0, 0.026, 0.025
    St, fs, S = f * App / U, f * c / U, 0.5 * cyps(0.191)["S_lobe"]
    print(f"\nPower at 10 m/s: St {St:.3f}, f* {fs:.3f}, C_P {St**2*(7.78+4.89*fs):.4f}, P {St**2*(7.78+4.89*fs)*0.5*RHO_W*U**3*S:.1f} W")
