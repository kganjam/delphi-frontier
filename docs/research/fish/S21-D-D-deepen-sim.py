# S21-D-D-D: what rise time would a 120 fps, max-of-4 reading need for the fastest Miln fish's
# TRUE peak to reach the stall threshold, and what muscle power would that rise time demand?
# EVERY OUTPUT IS CALCULATED OR SIMULATED, NOT OBSERVED.  numpy only, seed fixed.
# Run: python3 -I S21-D-D-deepen-sim.py
import numpy as np
rng = np.random.default_rng(21)
g, rho_air = 9.80665, 1.2

def Vs(m=4e-4, S=3.2e-4, CL=1.07):
    return np.sqrt(2*m*g/(rho_air*S*CL))

print("== 1. Threshold and margin (calculated) ==")
for CL in (0.6, 0.9, 1.07, 1.15, 1.5, 1.6):
    print(f"CL_max={CL:4.2f}  V_s={Vs(CL=CL):.2f} m/s  M(U=1.38)={Vs(CL=CL)/1.38:.2f}  M(U=1.58)={Vs(CL=CL)/1.58:.2f}")

print("\n== 2. Joint 2x errors (calculated), central V_s=4.37, U=1.38 ==")
base = Vs()/1.38
for name, fac in [("U x2", 1/2), ("U x2 & m /2", 1/2/np.sqrt(2)), ("U x2 & CL x2", 1/2/np.sqrt(2)),
                  ("U x2 & m/2 & CL x2", 1/4), ("m/2 & CL x2 & S x2", 1/np.sqrt(8))]:
    print(f"{name:22s} M={base*fac:.2f}")

def alpha_x(tp, V, T=0.25, dt=2e-6):
    t = np.arange(0, T, dt); v = V*(t/tp)*np.exp(1-t/tp)
    return t, np.cumsum(v)*dt

def read_120(tp, V=1.0, sx=0.0, ntrial=4, nsim=3000, fps=120):
    t, x = alpha_x(tp, V); dt = 1/fps; out = np.empty(nsim)
    for i in range(nsim):
        best = 0.0
        for _ in range(ntrial):
            ts = np.arange(rng.uniform(0, dt), 0.2, dt)
            xs = np.interp(ts, t, x) + rng.normal(0, sx, ts.size)
            best = max(best, np.max(np.abs(np.diff(xs)))/dt)
        out[i] = best
    return out.mean()/V

print("\n== 3. Under-read of a smooth alpha pulse, 120 fps, max of 4, no noise (simulated) ==")
tps = [0.5e-3, 1e-3, 1.5e-3, 2e-3, 2.5e-3, 3e-3, 4e-3, 5e-3]
ratios = {}
for tp in tps:
    ratios[tp] = read_120(tp); print(f"t_p={tp*1e3:4.1f} ms  measured/true={ratios[tp]:.3f}")

# Required reading ratio to close the gap: measured 1.38 / true V_s
for VsT in (Vs(CL=1.15), Vs(), Vs(CL=1.6)):
    need = 1.38/VsT
    xs = np.array([ratios[t] for t in tps]); ts = np.array(tps)
    tp_need = np.interp(need, xs, ts)   # ratio increases with tp
    # alpha pulse: a(0) = e*V/tp ; mass-specific power P/m = v*a, max over s of V^2/tp * s(1-s)e^(2-2s)
    s = np.linspace(0, 1, 100001); pk = np.max(s*(1-s)*np.exp(2-2*s))
    a0 = np.e*VsT/tp_need; Pbody = VsT**2/tp_need*pk
    print(f"\nTo close at V_s={VsT:.2f}: need reading ratio <= {need:.3f} -> t_p <= {tp_need*1e3:.2f} ms")
    print(f"  peak acceleration e*V/t_p = {a0:.0f} m/s^2 = {a0/g:.0f} g")
    print(f"  peak KE-rate power, body mass, no added mass, no drag (LOWER BOUND) = {Pbody:.0f} W/kg body")
    for mf in (0.3, 0.45, 0.6):
        print(f"    muscle fraction {mf:.2f} (assumed) -> {Pbody/mf:.0f} W/kg muscle")

print("\n== 4. Same power test for the S21-D-D lower rise-time bound, V=1.58, t_p=5 ms ==")
P = 1.58**2/5e-3*pk
print(f"  {P:.0f} W/kg body; /0.45 -> {P/0.45:.0f} W/kg muscle")

print("\n== 5. Self-consistent bound (calculated/simulated): true peak V = 1.38 / r(t_p) AND the")
print("   rise time must satisfy power demand V^2*pk/t_p <= P_ceiling * muscle_fraction ==")
grid = np.array([1.0,1.5,2,2.5,3,3.5,4,5,6,7,8,10,12,15,20])*1e-3
rg = np.array([read_120(t, nsim=1500) for t in grid])
for Pc, lab in [(461, "frog plantaris 28C-adjusted (Marsh 2022, law lib)"),
                (1200, "quail instantaneous record (UNVERIFIED secondary)")]:
    for mf in (0.3, 0.45, 0.6):
        fine = np.linspace(grid[0], grid[-1], 20000); r = np.interp(fine, grid, rg)
        V = 1.38/r; ok = V**2*pk/fine <= Pc*mf
        Vmax = V[ok].max(); tpm = fine[ok][np.argmax(V[ok])]
        print(f"P_c={Pc:5d} W/kg ({lab}), mf={mf:.2f}: max true peak {Vmax:.2f} m/s at t_p={tpm*1e3:.1f} ms;"
              f" M at V_s 3.57/4.21/4.37 = {3.57/Vmax:.2f}/{4.21/Vmax:.2f}/{4.37/Vmax:.2f}")
