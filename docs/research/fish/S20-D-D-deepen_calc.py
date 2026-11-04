"""S20-D-D-D arithmetic. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/S20-D-D-deepen_calc.py"""
from math import sqrt, sin, radians
g = 9.81
L_dr = 0.033                      # Danos & Lauder 2012 mean TL (m), author claim
v_need = sqrt(g * 1.0)            # 1 m range at 45 deg, drag-free (S20 framing)
def rng(v, a=45): return v * v * sin(radians(2 * a)) / g
def need(d): return sqrt(g * d)

# S20-D-D inputs
chang = (0.033 / 0.0185) ** (1 / 3)          # Chang H/L~L^-1/3 -> v~L^1/3
typ, ext = 1.13 * chang, 1.50 * chang        # S20-D-D typical (ballistic-from-H) and extreme
print("== 1. Sensitivity of S20-D-D's headline ('1 m out of reach, floor 1.7x') ==")
print(f"  baseline v_need {v_need:.2f}; typical {typ:.2f}; extreme {ext:.2f}; chang factor {chang:.3f}")
rows = [("extreme comparator (1.50 m/s x Chang)", lambda k: (ext * k, v_need)),
        ("typical comparator (1.37)",            lambda k: (typ * k, v_need)),
        ("Chang velocity exponent (1/3)",         lambda k: (1.50 * (0.033/0.0185) ** (k/3), v_need)),
        ("target distance (1 m)",                 lambda k: (ext, need(1.0 * k))),
        ("D&L burst inversion (0.842)",           lambda k: (0.842 * k, v_need))]
for lab, f in rows:
    out = []
    for k in (0.5, 2):
        v, vn = f(k)
        out.append(f"x{k}: v {v:.2f} vs need {vn:.2f} -> deficit x{vn/v:.2f}{' FLIPS' if v >= vn else ''}")
    print(f"  {lab:40s} " + " | ".join(out))

print("\n== 2. Improved transfer: guppy jump / guppy C-start ratio applied to Danio's own C-start ==")
gw, ga, gx = 1.0236, 1.2357, 1.50            # Soares & Bierman 2013 Table 1 / Fig 2 (measured)
ga_sd = 0.30
gtail = ga + 2 * ga_sd                       # mean + 2 s.d., air (normal assumption)
burst_g = (0.70, 0.80)                       # S&B 2013 author estimate, 'extrapolated from [45]'
burst_d = (0.78, 0.842, 0.91)                # D&L Re inversion, +/- 1 s.e.m. (S20-D)
for lab, vj in (("water mean", gw), ("air mean", ga), ("Fig2 single, air", gx), ("air mean+2sd", gtail)):
    r_lo, r_hi = vj / burst_g[1], vj / burst_g[0]
    lo, mid, hi = burst_d[0] * r_lo, burst_d[1] * vj / 0.75, burst_d[2] * r_hi
    print(f"  {lab:18s} guppy {vj:.2f}  ratio {r_lo:.2f}-{r_hi:.2f}  Danio {lo:.2f} / {mid:.2f} / {hi:.2f} m/s"
          f"  range45 {rng(lo)*100:.0f}-{rng(hi)*100:.0f} cm  1m-deficit x{v_need/hi:.2f}-x{v_need/lo:.2f}")
print(f"  Chang route, air mean+2sd: {gtail*chang:.2f} m/s -> deficit x{v_need/(gtail*chang):.2f}")

print("\n== 3. Checks ==")
print(f"  guppy ballistic v from H=6.54 cm at 77.4 deg: {sqrt(2*g*0.0654)/sin(radians(77.4)):.2f} m/s (measured air 1.24)")
print(f"  range at guppy mean attack angle 77.4 deg is {sin(radians(154.8)):.2f} of the 45-deg range")
m, A, Cd, rho = 4e-4, 2e-5, 0.5, 1.2         # ASSUMED frontal area and Cd
print(f"  air drag / weight at 3.13 m/s (assumed A=2e-5 m2, Cd=0.5): {0.5*rho*Cd*A*v_need**2/(m*g):.3f}")
# Chang 2019 power balance k M = 1/2 rho_w Cd U^3 S (k=16.9 W/kg, Cd=0.05); S definition ambiguous
def U(M, S): return (2 * 16.9 * M / (1000 * 0.05 * S)) ** (1 / 3)
for lab, M, S in (("Danio, S=frontal 2e-5 m2 (assumed)", 4e-4, 2e-5),
                  ("Danio, S=lateral 3e-4 m2 (S20-D planform)", 4e-4, 3e-4),
                  ("guppy, M=98 mg (if 'gm' is mg), S=frontal 9.4e-6 (assumed)", 9.8e-5, 9.4e-6)):
    print(f"  Chang power-balance U0, {lab}: {U(M,S):.2f} m/s")
cal = 1.2357 / U(9.8e-5, 9.4e-6)
print(f"  guppy calibration factor (measured air / model): {cal:.2f}; calibrated Danio frontal: {U(4e-4,2e-5)*cal:.2f} m/s")
print(f"\n  Distance reachable at the most generous corner (2.39 m/s, 45 deg): {rng(2.39)*100:.0f} cm;"
      f" v needed for 0.5 m: {need(0.5):.2f} m/s")
