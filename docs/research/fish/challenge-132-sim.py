# challenge-132: independent re-check of S21-D-D-D. ALL OUTPUT IS CALCULATED/SIMULATED, NOT OBSERVED.
# Analytic displacement of the alpha pulse (no numerical integration), so it is independent of the author's cumsum.
import numpy as np
rng = np.random.default_rng(132)
g = 9.80665
def Vs(CL, m=4e-4, S=3.2e-4, rho=1.2): return np.sqrt(2*m*g/(rho*S*CL))
def X(t, tp, V):  # integral of V(t/tp)e^{1-t/tp}
    s = t/tp; return V*tp*np.e*(1-(1+s)*np.exp(-s))
def readings(tp, scheme, n=4000, fps=120, ntr=4, others=1.0):
    dt = 1/fps; out = np.empty(n)
    for i in range(n):
        best = 0
        for k in range(ntr):
            Vk = 1.0 if k == 0 else others
            ts = np.arange(rng.uniform(0, dt), 0.25, dt); xs = X(ts, tp, Vk)
            if scheme == "fwd": v = np.diff(xs)/dt
            else: v = (xs[2:]-xs[:-2])/(2*dt)       # Tracker-style central difference
            best = max(best, v.max())
        out[i] = best
    return out
s = np.linspace(0, 1, 200001); pk = np.max(s*(1-s)*np.exp(2-2*s))
print(f"pk = {pk:.4f} (analytic 1-1/sqrt2 -> {(1-2**-.5)*(2**-.5)*np.exp(2**.5):.4f})")
for CL in (1.07, 1.15, 1.6): print(f"V_s(CL={CL}) = {Vs(CL):.3f} m/s")
grid = np.array([1,1.25,1.5,1.75,2,2.5,3,4,5,6,7,8,10,12,15,20,30])*1e-3
cases = [("fwd, 4 equal trials, mean", "fwd", 1.0, "mean"),
         ("fwd, 4 equal trials, 5th pct", "fwd", 1.0, "p5"),
         ("fwd, 1 trial at V (others 0.8V), mean", "fwd", 0.8, "mean"),
         ("central, 4 equal trials, mean", "cen", 1.0, "mean"),
         ("central, 1 at V others 0.8V, 5th pct", "cen", 0.8, "p5")]
for lab, sch, oth, stat in cases:
    r = []
    for tp in grid:
        R = readings(tp, sch, n=1500, others=oth); r.append(R.mean() if stat == "mean" else np.percentile(R, 5))
    r = np.array(r); fine = np.linspace(grid[0], grid[-1], 40000); rf = np.interp(fine, grid, r)
    print(f"\n== {lab} ==")
    print("  r(tp): " + "  ".join(f"{t*1e3:g}ms:{x:.3f}" for t, x in zip(grid, r)))
    for CL in (1.07, 1.6):
        V = Vs(CL); need = 1.38/V; tpn = np.interp(need, r, grid)
        P = pk*V**2/tpn
        print(f"  close at V_s={V:.2f}: t_p<={tpn*1e3:.2f} ms, a0={np.e*V/tpn/g:.0f} g, {P:.0f} W/kg body, {P/0.6:.0f} W/kg muscle@0.6")
    Vt = 1.38/rf
    for Pc in (461, 1200):
        for mf in (0.3, 0.6):
            ok = pk*Vt**2/fine <= Pc*mf; j = np.argmax(np.where(ok, Vt, 0))
            print(f"  P_c={Pc} mf={mf}: max true peak {Vt[j]:.2f} m/s at t_p={fine[j]*1e3:.1f} ms; M(3.57/4.37)={3.57/Vt[j]:.2f}/{4.37/Vt[j]:.2f}")
