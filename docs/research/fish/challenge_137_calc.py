"""Challenge-137: independent checks on S10-D-D-D (branch claude/deepen-s10-d-d-juuuwn).
EVERY OUTPUT IS A CALCULATION. Measured inputs: Mead et al. 2020 (PMC7451861, full-text).

Part A re-derives hover, forward-flight and design-frequency numbers from scratch.
Part B recomputes the "strict" rectangular-loop bound. The 8% strain was imposed on the
PREPARATION. Work was computed from MEASURED MYOTOME length, and myotome length was "within
+/-5% of starting length". So myotome strain is <= ~10% peak-to-peak, and its exact value
was not reported.
Part C is a crude twitch-driven work-loop model. It FAILS calibration against the 40 Hz point
(see printed output), so no number from it is used as evidence.
"""
import math
import numpy as np, itertools

g, rho, k, m = 9.81, 1.2, 1.2, 0.4e-3
W = m * g
S0, TT, RHO_M = 76e3, 0.91, 1060.0
MEAS = {40: 2.63, 80: 134.4 / 80, 100: 122.9 / 100, 120: 0.43}  # J/kg per cycle

# ---- Part A: independent re-derivation
R = 0.04
A = math.pi * R**2
P_id = math.sqrt(W**3 / (2 * rho * A))
S = (2 * R)**2 / 6
U = math.sqrt(2 * W / (rho * 1.5 * S))
f_design = U / (2 * (2 * math.pi / 3) * 0.55 * R)
print(f"A. design f = {f_design:.2f} Hz")
for f_m in (0.0164, 0.0276):
    print(f"   hover M=1.5 f={f_m}: {1.5*k*P_id/(m*f_m):.0f} W/kg muscle")
Vstall = U
for CDp in (0.05, 0.10, 0.20):
    # analytic minimum of induced + parasite power, clipped at stall speed
    a = k * W**2 / (2 * rho * A); b = 0.5 * rho * (2.2e-5 * 0.4 + S * CDp)
    V = max((a / (3 * b))**0.25, Vstall)
    P = a / V + b * V**3
    print(f"   fwd CDpro={CDp}: V*={V:.2f} m/s, {P/(m*0.0276):.0f} W/kg (upper f), "
          f"ratio to hover {P/(1.5*k*P_id):.2f}")
W22 = {"plateau": 2.63, "linear": 2.63 + (2.63 - MEAS[80]) / 40 * (40 - f_design)}
for kk, w in W22.items():
    print(f"   {kk}: {w:.2f} J/kg -> {w*f_design:.1f} W/kg; SD-propagated plateau +/- {0.18*f_design:.1f}")

# ---- Part B: rectangle bound vs. myotome strain
print("B. rectangular-loop ceiling at 21.9 Hz vs. assumed myotome strain (p-p)")
for eps in (0.06, 0.08, 0.10):
    wb = S0 * eps / RHO_M
    print(f"   strain {eps:.2f}: {wb:.2f} J/kg -> {wb*f_design:.0f} W/kg; "
          f"implied 40 Hz loop fill {2.63/wb:.2f}")
print(f"   flip thresholds: 97 W/kg = {97/f_design:.2f} J/kg, 121 W/kg = {121/f_design:.2f} J/kg")

# ---- Part C: crude twitch model (sin^2 pulse of duration D, Hill shortening FV)
def work(f, D, vmax, ph, n=1, ipi=0.0, curv=0.25, N=600, nc=4):
    T = 1 / f; t = np.linspace(0, nc * T, nc * N, endpoint=False); dt = t[1] - t[0]
    eps = 0.04 * np.sin(2 * np.pi * f * t); v = np.gradient(eps, dt); act = np.zeros_like(t)
    for c in range(-3, nc):
        for p in range(n):
            x = (t - (c * T + ph * T + p * ipi)) / D
            act += np.where((x > 0) & (x < 1), np.sin(np.pi * x)**2, 0)
    act = np.minimum(act, 1 / TT if n > 1 else 1)
    vs = np.clip(-v / vmax, 0, .999); fv = np.where(v < 0, (1 - vs) / (1 + vs / curv), 1.)
    s = S0 * TT * act * fv; L = slice((nc - 1) * N, nc * N)
    return -np.sum(s[L] * v[L]) * dt / RHO_M

def best(f, D, vm, **kw):
    return max(work(f, D, vm, p, **kw) for p in np.linspace(0, 1, 48, endpoint=False))

res = []
for D, vm in itertools.product(np.arange(4, 26, 2) * 1e-3, [5, 8, 12, 20, 40]):
    pr = {f: best(f, D, vm) for f in MEAS}
    e = sum(np.log(max(pr[f], 1e-3) / MEAS[f])**2 for f in MEAS); res.append((e, D, vm, pr))
res.sort(key=lambda z: z[0])
print("C. crude model, best fits (predicted J/kg at 40/80/100/120 Hz; measured 2.63/1.68/1.23/0.43)")
for e, D, vm, pr in res[:3]:
    print(f"   err {e:.2f} D={D*1e3:.0f} ms Vmax={vm}: " + " ".join(f"{pr[f]:.2f}" for f in MEAS)
          + f" | 21.9 Hz: {best(21.9, D, vm):.2f} J/kg  -> CALIBRATION FAILED, not used")
