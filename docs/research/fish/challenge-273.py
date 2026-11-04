"""challenge-273: independent re-derivation of the S32 exocoetid taxi test.
Reimplemented from the stated equations in S32-organism.md section 1 (not imported from S32_taxi.py)."""
import math
rw, ra, nu, g, sig = 1000.0, 1.225, 1.0e-6, 9.81, 0.072
c6, c8, c9, CDF = 2.55, 7.78, 4.89, 0.08          # Floryan 2017 pitching (as quoted by S32)
M, f, c, phi = 0.191, 50.0, 0.025, 0.5
WL = 285.015 * M**0.4; Sw = M*g/WL; Sh = 0.003*M**0.65; S = phi*Sh; d = S/c
W = M*g; Vto = math.sqrt(2*W/(ra*Sw*1.07))
Af = (0.6*0.46*M**0.355*0.15)**2
k = 1/(math.pi*0.8*5)

def other_drag(U):
    q = 0.5*ra*U*U
    CL = min(1.07, W/(q*Sw)); L = q*Sw*CL
    Dw = q*Sw*(0.08 + k*CL*CL); Db = q*0.3*Af
    qw = 0.5*rw*U*U; CLz = max(0.0, W + 2*sig*c - L)/(qw*S)
    Di = qw*S*CLz**2/(math.pi*0.8*2*d*d/S)
    return Dw + Db + Di + 2*sig*c*0.3

def thrust(U, App, CD, freq=f):
    return 0.5*rw*S*(c6*(freq*App)**2 - CD*U*U)

def power(U, App, freq=f):
    St = freq*App/U; fs = freq*c/U
    return 0.5*rw*U**3*S*(c8*St**2 + c9*St**2*fs)

def CD_steady(U, App, freq=f):
    # C_D that makes thrust = all other drag at U  (steady taxi)
    return (c6*(freq*App)**2 - other_drag(U)/(0.5*rw*S))/(U*U)

def App_for_power(P, U, freq=f):
    St2 = P/(0.5*rw*U**3*S*(c8 + c9*freq*c/U))
    return math.sqrt(St2)*U/freq

print(f"geometry: Sw {Sw*1e4:.1f} cm2, S_hypo {Sh*1e4:.2f} cm2, S_imm {S*1e4:.2f} cm2, V_to {Vto:.2f} m/s, W {W:.3f} N")
Re = lambda U: U*c/nu
print(f"Re at 10 / 15 / 16.5 m/s: {Re(10):.3g} / {Re(15):.3g} / {Re(16.5):.3g}")

print("\n[T1] ceiling U_max = f A sqrt(c6/C_D) by hand, A_pp 2.6 cm, 50 Hz")
for CD in (0.08, 0.0112, 0.03, 0.05):
    print(f"  C_D {CD:.4f}: U_max {f*0.026*math.sqrt(c6/CD):.2f} m/s")
print(f"  laminar Re^-1/2 extrap of 0.08 from 9560 to 2.5e5: {0.08*math.sqrt(9560/2.5e5):.4f}")

print("\n[T2] Deng 2019 abstract: STEADY taxi at 10 m/s needs 36 W at 50 Hz, 15 deg. Steady => net = 0.")
A36 = App_for_power(36, 10)
print(f"  A_pp giving 36 W at 10 m/s (Floryan power law, phi 0.5): {A36*100:.2f} cm")
for name, CD in (("const 0.08", 0.08), ("scaled", 0.08*math.sqrt(9560/Re(10)))):
    print(f"  net force at 10 m/s, {name} C_D={CD:.4f}: {thrust(10,A36,CD)-other_drag(10):+.3f} N")
cs = CD_steady(10, A36)
print(f"  C_D that makes the 36-W kinematics STEADY at 10 m/s: {cs:.4f}  (other drag {other_drag(10):.3f} N)")
print(f"  -> with that C_D held, ceiling = {f*A36*math.sqrt(c6/cs):.2f} m/s (foil alone)")

print("\n  Deng: 350 W -> 16.5 m/s (read as steady at 16.5).")
A350 = App_for_power(350, 16.5)
print(f"  A_pp giving 350 W at 16.5 m/s: {A350*100:.2f} cm (St {f*A350/16.5:.2f}); at 50 Hz/15 deg needs lobe {A350/2/math.sin(math.radians(15))*100:.1f} cm")
cs2 = CD_steady(16.5, A350)
print(f"  C_D for steady 16.5 m/s at 350 W: {cs2:.4f}; scaled branch gives {0.08*math.sqrt(9560/Re(16.5)):.4f}")
# what power does the scaled branch say steady 16.5 needs?
CDsc = 0.08*math.sqrt(9560/Re(16.5))
lo, hi = 0.001, 0.2
for _ in range(100):
    m = (lo+hi)/2
    lo, hi = (m, hi) if thrust(16.5, m, CDsc) - other_drag(16.5) < 0 else (lo, m)
print(f"  scaled branch: steady 16.5 m/s needs A_pp {hi*100:.2f} cm -> P = {power(16.5, hi):.0f} W (Deng CFD: 350 W)")
CDc = 0.08
lo, hi = 0.001, 0.5
for _ in range(100):
    m = (lo+hi)/2
    lo, hi = (m, hi) if thrust(16.5, m, CDc) - other_drag(16.5) < 0 else (lo, m)
print(f"  const branch : steady 16.5 m/s needs A_pp {hi*100:.2f} cm -> P = {power(16.5, hi):.0f} W (Deng CFD: 350 W)")
# steady 10 m/s power each branch
for name, CD in (("scaled", 0.08*math.sqrt(9560/Re(10))), ("const", 0.08)):
    lo, hi = 0.001, 0.5
    for _ in range(100):
        m = (lo+hi)/2
        lo, hi = (m, hi) if thrust(10, m, CD) - other_drag(10) < 0 else (lo, m)
    print(f"  {name:6s} branch: steady 10 m/s needs A_pp {hi*100:.2f} cm -> P = {power(10, hi):.0f} W (Deng CFD: 36 W)")

print("\n[T3] physically split extrapolation: C_D = C_f(Re) two-sided + constant form residual")
for lab, cf in (("laminar Blasius", lambda R: 2*1.328/math.sqrt(R)), ("turbulent 0.074Re^-0.2", lambda R: 2*0.074*R**-0.2)):
    form = 0.08 - cf(7000)
    for U in (10, 15):
        CD = form + cf(Re(U))
        print(f"  {lab:24s}: friction@7000 {cf(7000):.4f}, form {form:.4f}; C_D@{U} m/s = {CD:.4f}; ceiling(A 2.6 cm) {f*0.026*math.sqrt(c6/CD):.1f} m/s;"
              f" net@10 {thrust(10,0.026,form+cf(Re(10)))-other_drag(10):+.3f} N")

print("\n[T4] tail-beat frequency 13.5 Hz (APS 2024 abstract, search-summary) instead of 50 Hz")
for App in (0.026, 0.06, 0.10):
    for name, CD in (("scaled", 0.08*math.sqrt(9560/Re(10))), ("const", 0.08)):
        print(f"  A_pp {App*100:.1f} cm, {name}: ceiling {13.5*App*math.sqrt(c6/CD):.2f} m/s, net@10 {thrust(10,App,CD,13.5)-other_drag(10):+.3f} N")
Aneed = 1.0*Vto/13.5*math.sqrt(CDF/c6)
print(f"  A_pp needed at 13.5 Hz for ceiling = V_to with const C_D: {Aneed*100:.1f} cm; scaled: {Vto/13.5*math.sqrt(0.08*math.sqrt(9560/Re(15))/c6)*100:.1f} cm")
print(f"  A_pp needed at 50 Hz for ceiling = V_to, const C_D (foil alone): {Vto/50*math.sqrt(CDF/c6)*100:.2f} cm")

print("\n[T5] run length of the 'reproduction' (A_pp 2.6, scaled): integrate")
U, x, t, dt = 10.0, 0.0, 0.0, 1e-4
while U < Vto and t < 10:
    CD = 0.08*math.sqrt(9560/Re(U)) if Re(U) > 9560 else 0.08
    a = (thrust(U, 0.026, CD) - other_drag(U))/M
    U += a*dt; x += U*dt; t += dt
print(f"  reaches {U:.2f} m/s at t {t:.2f} s, x {x:.1f} m, {t*50:.0f} strokes")
