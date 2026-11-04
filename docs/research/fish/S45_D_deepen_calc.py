"""S45-D-D: what whole-ray stiffness does S45's reconciled (stepped) ray present to S6-D's load case?
Every number printed is a COMPUTATION (Euler-Bernoulli, small deflection), not an observation.
Run: python3 -I docs/research/fish/S45_D_deepen_calc.py   (~1-2 min)"""
import numpy as np

L0, K0, M3 = 0.0403, 1.98, 565e-6     # Alben 2007 ray length (m) & cantilever slope (N/m); Flammang 2013 abstract EI
REQ_S6D = 6.3e-4                       # S6-D's computed requirement for delta/L <= 0.10 (uniform EI)
N = 100001
s_unit = np.linspace(0.0, 1.0, N)

def cumtrap(y, x):
    return np.concatenate(([0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))))

def deflection(EI, s, M):
    th = cumtrap(M / EI, s)
    return cumtrap(th, s)                # w(s), clamped at s=0

def profile(EIp, EId, f, L):
    s = s_unit * L
    return s, np.where(s < f * L, EIp, EId)

def k_point(EIp, EId, f, L, conv):
    """stiffness for a unit point load at a = 2L/3, deflection read at tip or load point"""
    s, EI = profile(EIp, EId, f, L)
    a = 2 * L / 3
    w = deflection(EI, s, np.where(s < a, a - s, 0.0))
    return 1.0 / (w[-1] if conv == "tip" else np.interp(a, s, w))

def distal_EI(f, conv="tip", k=K0, EIp=M3, L=L0):
    lo, hi = 1e-12, 1e-1
    for _ in range(100):
        mid = (lo * hi) ** 0.5
        if k_point(EIp, mid, f, L, conv) < k: lo = mid
        else: hi = mid
    return (lo * hi) ** 0.5

def EI_eff_uniform_load(EIp, EId, f, L):
    """effective uniform EI giving the same tip deflection under a uniformly distributed load:
       uniform beam: w_tip = q L^4 / (8 EI)"""
    s, EI = profile(EIp, EId, f, L)
    M = 0.5 * (L - s) ** 2              # q = 1
    w = deflection(EI, s, M)
    return L ** 4 / (8 * w[-1])

def EI_uniform_from_k(k, conv, L=L0):
    a = 2 * L / 3
    c = a**2 * (3*L - a) / 6 if conv == "tip" else a**3 / 3
    return k * c

print("== 0. Reproduce S45/S45-D baseline ==")
for f in (0.40, 0.50):
    print(f"  f={f:.2f} tip: distal EI = {distal_EI(f):.3e} N m^2")
print(f"  uniform 565e-6, tip convention: k = {k_point(M3, M3, 0, L0, 'tip'):.1f} N/m (measured 1.98)")

print("\n== 1. Uniform-equivalent EI implied directly by the measured slope (no stepped model) ==")
for conv in ("tip", "load"):
    e = EI_uniform_from_k(K0, conv)
    print(f"  {conv:4s}: EI_uniform = {e:.3e} N m^2 ; 565e-6 / this = {M3/e:.1f}x ; S6-D req / this = {REQ_S6D/e:.1f}x")

print("\n== 2. KEY: whole-ray effective EI of S45's reconciled stepped ray under S6-D's distributed load ==")
print("   (stepped ray: 565e-6 on proximal f, distal EI solved to reproduce k = 1.98 N/m)")
print("   f     conv  distal EI     EI_eff(udl)   EI_eff/565e-6   S6-D delta/L (=0.112*565e-6/EI_eff)")
rows = []
for conv in ("tip", "load"):
    for f in (0.19, 0.30, 0.40, 0.45, 0.486):
        d = distal_EI(f, conv)
        e = EI_eff_uniform_load(M3, d, f, L0)
        dl = 0.112 * M3 / e
        rows.append((f, conv, d, e, dl))
        print(f"  {f:5.3f} {conv:4s}  {d:.3e}    {e:.3e}     {e/M3:.4f}         {dl:.2f}")

print("\n== 3. Sensitivity of the key output to M3 itself (f = 0.40, tip) ==")
for name, ep in (("M3", M3), ("M3 x2", 2*M3), ("M3 /2", M3/2), ("M3 x10", 10*M3)):
    d = distal_EI(0.40, EIp=ep)
    e = EI_eff_uniform_load(ep, d, 0.40, L0)
    print(f"  {name:7s}: distal {d:.3e}, EI_eff {e:.3e} N m^2, S6-D delta/L = {0.112*M3/e:.2f}")

print("\n== 4. Sensitivity to the measured slope k (f = 0.40, tip) ==")
for name, k in (("k", K0), ("k x2", 2*K0), ("k /2", K0/2), ("k x10", 10*K0)):
    d = distal_EI(0.40, k=k)
    e = EI_eff_uniform_load(M3, d, 0.40, L0)
    print(f"  {name:6s}: EI_eff {e:.3e} N m^2, S6-D delta/L = {0.112*M3/e:.2f}")

print("\n== 5. Size scaling caveat: S6-D applies the EI number to a 120 mm ray unchanged.")
print("   Geometrically similar scaling EI ~ L^4 from 40.3 mm to 120 mm multiplies EI by "
      f"{(0.12/L0)**4:.1f}x (assumption, not a measurement)")
e40 = EI_eff_uniform_load(M3, distal_EI(0.40), 0.40, L0)
print(f"   EI_eff(f=0.40) x that = {e40*(0.12/L0)**4:.3e} N m^2 ; S6-D delta/L = {0.112*M3/(e40*(0.12/L0)**4):.3f}")
print(f"   same scaling applied to 565e-6: {M3*(0.12/L0)**4:.3e} N m^2 ; delta/L = {0.112/((0.12/L0)**4):.4f}")
