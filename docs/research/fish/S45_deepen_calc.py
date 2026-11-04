"""S45-D: sensitivity of S45's deciding computation to each of its inputs.
Every number printed here is a COMPUTATION (Euler-Bernoulli, stepped cantilever), not an observation.
Run: python3 -I docs/research/fish/S45_deepen_calc.py"""
import numpy as np

L0, K0, FLAM0 = 0.0403, 1.98, 565e-6      # Alben 2007 ray length & slope; Flammang 2013 abstract EI
B_LO, B_HI = 1e-6, 1e-5                    # Alben 2007 §3.3 measured bending rigidity bracket
N = 200001

def compliance(EI_p, EI_d, f, L, conv):
    """deflection per unit load; load at a = 2L/3; conv = 'tip' or 'load'"""
    a = 2 * L / 3
    s = np.linspace(0.0, L, N)
    EI = np.where(s < f * L, EI_p, EI_d)
    M = np.where(s < a, (a - s), 0.0)
    kap = M / EI
    th = np.concatenate(([0.0], np.cumsum(0.5 * (kap[1:] + kap[:-1]) * np.diff(s))))
    if conv == "tip":
        return np.trapezoid(th, s)
    m = s <= a
    return np.trapezoid(th[m], s[m])

def distal_EI(f, k=K0, EI_p=FLAM0, L=L0, conv="tip"):
    lo, hi = 1e-12, 1e-2
    for _ in range(120):
        mid = (lo * hi) ** 0.5
        if 1.0 / compliance(EI_p, mid, f, L, conv) < k: lo = mid
        else: hi = mid
    return (lo * hi) ** 0.5

def f_at(target, **kw):
    """proximal fraction at which the reconciling distal EI equals `target`"""
    lo, hi = 0.0, 0.66
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if distal_EI(mid, **kw) > target: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

print("== A. Baseline (reproduces S45 §3.2) ==")
for f in (0.40, 0.50, 0.60):
    print(f"  f={f:.2f}: distal EI = {distal_EI(f):.3e} N m^2")

print("\n== B. Admissible window in f (distal EI inside Alben's measured 1e-6..1e-5) ==")
f_hi = f_at(B_HI); f_lo_edge = f_at(B_LO)
print(f"  distal EI = 1e-5 at f = {f_hi:.3f};  distal EI = 1e-6 at f = {f_lo_edge:.3f}")
print(f"  => reconciliation admissible for {f_hi:.3f} < f < {f_lo_edge:.3f}")

print("\n== C. Factor-of-two (and convention) perturbations at f = 0.40 ==")
base = distal_EI(0.40)
cases = {
    "baseline": {},
    "k x2 (3.96 N/m)": dict(k=2 * K0), "k /2 (0.99 N/m)": dict(k=K0 / 2),
    "M3 x2 (1.13e-3)": dict(EI_p=2 * FLAM0), "M3 /2 (2.83e-4)": dict(EI_p=FLAM0 / 2),
    "M3 /10 (5.65e-5)": dict(EI_p=FLAM0 / 10),
    "L x1.02 (+0.8mm s.e.)": dict(L=L0 * 1.02), "L /1.02": dict(L=L0 / 1.02),
    "load-point convention": dict(conv="load"),
}
for name, kw in cases.items():
    d = distal_EI(0.40, **kw)
    print(f"  {name:24s} distal EI = {d:.3e}  in-bracket={B_LO <= d <= B_HI}  ratio to base {d/base:.2f}")
print("  f perturbations:")
for f in (0.20, 0.30, 0.40, 0.45, 0.48, 0.50, 0.80):
    d = distal_EI(f) if f < 0.66 else float('nan')
    if f >= 0.66:
        print(f"  f={f:.2f}: step lies beyond load point -> ray stiffer than M3 between load and base; "
              f"k = {1/compliance(FLAM0, FLAM0, 0, L0, 'tip'):.1f} N/m regardless of distal EI")
    else:
        print(f"  f={f:.2f}: distal EI = {d:.3e}  in-bracket={B_LO <= d <= B_HI}")

print("\n== D. If M3 is a WHOLE-RAY uniform EI (the reading that would make S45 a refutation) ==")
k_uni = 1 / compliance(FLAM0, FLAM0, 0.0, L0, "tip")
print(f"  predicted slope with uniform EI = 565e-6: k = {k_uni:.1f} N/m vs measured 1.98 N/m "
      f"-> {k_uni/K0:.1f}x too stiff")

print("\n== E. Margin at the improved input f = 0.40 ==")
print(f"  distal EI / Alben lower bound = {base/B_LO:.2f}x ; f margin to window edge = "
      f"{f_lo_edge-0.40:+.3f} (i.e. {100*(f_lo_edge-0.40)*L0*1e3/100:.1f} mm of a 40.3 mm ray)")
