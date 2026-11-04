"""Replicate 246: ascent-averaged vertical lift / W for the S28 case-C wing. CALCULATION, not measurement."""
import math
g, rho = 9.81, 1.225
m = 0.25e-3; W = m * g                  # S28 §1 (assumed mass)
CL = 1.07                               # S28 §1 (project-derived)
def vto(S): return math.sqrt(2 * W / (rho * S * CL))

def ascent(V0, th_deg, S, cd_over_cl=0.0, dt=1e-6):
    """Integrate climb with gravity + wing lift (perp. to v) + optional wing drag; no body drag
    (body drag is common to wild type and fish-with-fins, so it is not part of the *reduction*).
    Returns time-averaged vertical lift/W, vertical net wing force/W, exit and apex lift/W."""
    th = math.radians(th_deg); u, w = V0*math.cos(th), V0*math.sin(th)
    Vt2 = vto(S)**2; t = 0; acc_L = acc_N = 0
    while w > 0:
        V = math.hypot(u, w); k = g * V*V / Vt2          # lift accel magnitude
        aLx, aLz = -k*w/V, k*u/V                          # perpendicular, tilted back
        aDx, aDz = -k*cd_over_cl*u/V, -k*cd_over_cl*w/V
        acc_L += aLz/g*dt; acc_N += (aLz+aDz)/g*dt
        u += (aLx+aDx)*dt; w += (aLz+aDz-g)*dt; t += dt
    return acc_L/t, acc_N/t, (V0**2/Vt2), (u*u/Vt2)

print(f"W = {W:.4e} N; V_to(case C, 192 mm2) = {vto(192e-6):.3f} m/s")
for S, lab in [(192e-6,'C'), (125e-6,'B'), (57e-6,'A')]:
    for V0 in (1.38, 0.45):
        for th in (30, 45, 60):
            L, N, Lex, Lap = ascent(V0, th, S)
            _, N17, _, _ = ascent(V0, th, S, cd_over_cl=0.17)
            print(f"case {lab} V0={V0} th={th}: |L|/W exit={Lex*100:.2f}% apex={Lap*100:.2f}% | "
                  f"mean vertical lift={L*100:.2f}% | net incl wing drag CD/CL=0.17: {N17*100:.2f}%")
