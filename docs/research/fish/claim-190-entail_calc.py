"""Bounds for the claim-190 entailment note. Every output is a CALCULATION, not an observation.
Inputs are S28's (m = 0.25 g, S = 192 mm2, CL 1.07, b = 31 mm, exit 1.38 m/s at 45 deg) unless stated."""
import math
g, rho = 9.81, 1.225
m, S, CL, b, V0 = 0.25e-3, 192e-6, 1.07, 0.031, 1.38
W = m * g
f = lambda V, S=S, m=m: 0.5 * rho * V * V * S * CL / (m * g)
print(f"W = {W:.4e} N; lift fraction at {V0} m/s = {f(V0):.4f}; apex (45 deg) = {f(V0*math.cos(math.pi/4)):.4f}")

# 1. Range on fin area for a launch fraction of 9-11 % at 1.38 m/s
for frac in (0.09, 0.10, 0.11):
    print(f"S for {frac:.0%} at 1.38 m/s: {frac*W/(0.5*rho*V0**2*CL)*1e6:.0f} mm2")

# 2. Range on exit speed for 9-11 % with S = 192 mm2
for frac in (0.09, 0.10, 0.11):
    print(f"V for {frac:.0%}: {math.sqrt(frac*W/(0.5*rho*S*CL)):.3f} m/s")

# 3. Span: per-fin length / SL for b within x1.2 of 1.0 SL (SL 30 mm, body width 4 mm)
SL, bw = 0.030, 0.004
for bb in (b/1.2, b, b*1.2):
    print(f"span {bb*1e3:.1f} mm -> fin length/SL = {(bb-bw)/2/SL:.3f}")

# 4. Stiffness: tip deflection <= 10 % of fin length, uniform load, cantilever, per fin
L = 0.0135
F_fin = 0.5 * f(V0) * W                 # lift carried by one fin at launch
q_air = 0.5 * rho * V0**2               # dynamic pressure
EI_req = F_fin * L**2 / (8 * 0.10)      # delta = F L^3 / (8 EI) <= 0.1 L
print(f"lift per fin {F_fin:.3e} N; wing loading of lift {F_fin/(S/2):.2f} Pa; q_air {q_air:.2f} Pa")
print(f"EI required (whole fin, delta/L<=0.1): {EI_req:.2e} N m2; S28 quotes 6.3e-5 -> ratio {6.3e-5/EI_req:.0f}x")
for t_um in (50, 100):
    w_mem = t_um * 1e-6 * 1100 * g
    print(f"membrane self-weight per area at {t_um} um: {w_mem:.2f} Pa")
print(f"water speed giving the same dynamic pressure as lift loading: {math.sqrt(2*F_fin/(S/2)/1000):.3f} m/s")

# 5. Timescale: airtime and apex time at 45 deg, vacuum
T = 2 * V0 * math.sin(math.pi/4) / g
print(f"airtime {T*1e3:.0f} ms, apex at {T/2*1e3:.0f} ms, 10 % of airtime = {T*100:.0f} ms")
print(f"larval fin beat 28 Hz -> half-cycle {1e3/28/2:.0f} ms")

# 6. Apex fraction 4-6 % -> launch angle band
for fa in (0.04, 0.05, 0.06):
    print(f"apex {fa:.0%} -> theta = {math.degrees(math.acos(math.sqrt(fa/f(V0)))):.1f} deg")

# 7. Mass sensitivity (organism-scale input, not an adjacent-scale constraint)
for mm in (0.25e-3, 0.40e-3, 0.50e-3):
    print(f"m = {mm*1e3:.2f} g -> launch fraction {f(V0, m=mm):.3f}")
