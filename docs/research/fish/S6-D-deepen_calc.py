"""S6-D-D: attack S6-D's most sensitive input. CALCULATION ONLY -- nothing here is an observation.

Model (inherited unchanged from S6-D, s6_deepen_calc.py on branch claude/deepen-fin-ray-s6-cj2i2x):
uniform Euler-Bernoulli cantilever per ray, equal share of lift, uniform load.
    P = s*n*m*g/(2N);  delta/L = P L^2/(8 EI);  EI_req = P L^2/(8 c)
"""
import math
g = 9.81

def ei_req(m=0.10, L=0.12, N=14, n=1.0, s=1.0, c=0.10, k_dist=1.0):
    P = s * n * m * g / (2 * N)
    return k_dist * P * L**2 / (8 * c)

def dl_(EI, m=0.10, L=0.12, N=14, n=1.0, s=1.0, k_dist=1.0):
    P = s * n * m * g / (2 * N)
    return k_dist * P * L**2 / (8 * EI)

base = ei_req()
print(f"[1] S6-D baseline EI_req = {base:.3e} N m^2")

# ---------- 1. sensitivity: factor each input must move to flip the verdict, per candidate EI ----------
cands = {
    "Flammang2013 abstract, 'calculated' in vivo": 565e-6,
    "Alben2007 k-bound (this doc, calculated)":    None,   # filled below
    "Alben2007 stated range, upper":               1e-5,
    "Alben2007 stated range, lower":               1e-6,
    "3.8e-6 (Puri2018 relay; untraced per S25)":   3.8e-6,
    "Aiello2018 labrid max":                       1.5109e-6,
}
# ---------- 2/3. improve EI: bound from Alben 2007 measured point-load stiffness ----------
k = 1.98        # N/m, bluegill pectoral ray 4, both hemitrich bases clamped (Alben 2007, via S26 full-text summary)
Lbg = 40.3e-3   # m, bluegill max pectoral ray length, 6 fish (Alben 2007, via S26)
EI_bound = k * Lbg**3 / 3       # point load at the tip: the largest lever possible on this ray
cands["Alben2007 k-bound (this doc, calculated)"] = EI_bound
print(f"[3a] Alben k={k} N/m, L={Lbg*1e3} mm -> EI <= k L^3/3 = {EI_bound:.2e} N m^2 (if load at tip, rigid root)")
for a_mm in (10, 15, 20, 25, 30, 40.3):
    a = a_mm * 1e-3
    print(f"      load at a={a_mm:5.1f} mm -> EI = {k*a**3/3:.2e}")
a_565 = (3 * 565e-6 / k) ** (1 / 3)
print(f"      lever needed for EI=565e-6 at k=1.98: {a_565*1e3:.0f} mm (ray is {Lbg*1e3} mm)")
for lo, hi in ((1e-6, 1e-5),):
    print(f"      Alben stated EI {lo:.0e}-{hi:.0e} implies load point a = "
          f"{(3*lo/k)**(1/3)*1e3:.1f}-{(3*hi/k)**(1/3)*1e3:.1f} mm  (consistency check)")

print("\n[1] delta/L at S6-D baseline, and factor by which EACH single input must move to flip:")
for name, EI in cands.items():
    r = dl_(EI) / 0.10          # >1 fails
    flip_L = r ** -0.5          # L enters squared
    print(f"  {name:45s} EI={EI:.2e} delta/L={dl_(EI):7.3f}  need: EI x{r:6.1f} | L x{flip_L:.3f} | m or 1/N or c x{1/r:.3f}")

# ---------- 3b. load side with sourced morphometrics (search-summary level) ----------
print("\n[3b] EI_req over sourced/bracketed load inputs")
rows = []
for m in (0.089, 0.10, 0.188):            # H. affinis 89-188 g (Brazil, search-summary)
    for L in (0.105, 0.12, 0.16):         # C. hiraii semi-span ~105-118 mm; Davenport 0.78 SL ceiling ~160 mm
        for s in (0.8, 1.0):              # pectoral share (replicate-72: pelvics ~20% of wing area)
            for kd in (0.53, 1.0, 1.47):  # challenge-72 load-distribution factor
                rows.append((ei_req(m=m, L=L, s=s, k_dist=kd), m, L, s, kd))
rows.sort()
print(f"  min EI_req = {rows[0][0]:.2e}  at {rows[0][1:]}")
print(f"  max EI_req = {rows[-1][0]:.2e}  at {rows[-1][1:]}")
print(f"  central (m=0.10,L=0.12,s=1,kd=1) = {base:.2e};  max/min = {rows[-1][0]/rows[0][0]:.1f}x")
for N in (10, 14, 18):
    print(f"  N={N}: EI_req = {ei_req(N=N):.2e}")

# ---------- 3c. the transfer the verdict actually rests on: bluegill 40 mm ray -> flying-fish ray ----------
print("\n[3c] scale transfer EI_ff = EI_bg * (L_ff/L_bg)^beta ; beta needed to reach EI_req")
print("     beta=0: absolute transfer (what S6-D did implicitly); 4: isometric (d ~ L); 6: elastic similarity (d ~ L^1.5)")
for Lff in (0.105, 0.12, 0.16):
    lam = Lff / Lbg
    req = ei_req(L=Lff)
    out = []
    for name, EI in (("Alben lo", 1e-6), ("Alben hi", 1e-5), ("k-bound", EI_bound), ("Flammang", 565e-6)):
        beta = math.log(req / EI) / math.log(lam)
        out.append(f"{name} beta>={beta:4.2f}")
    print(f"  L_ff={Lff*1e3:.0f} mm (x{lam:.2f}), EI_req={req:.2e}: " + "; ".join(out))
    for beta in (0, 2, 4):
        print(f"      beta={beta}: Alben 1e-6..1e-5 -> {1e-6*lam**beta:.1e}..{1e-5*lam**beta:.1e};"
              f" k-bound -> {EI_bound*lam**beta:.1e}  (need {req:.1e})")

# ---------- 3d. cheapest decisive measurement: base diameter of a flying-fish ray ----------
print("\n[3d] solid-section diameter that meets EI_req, by modulus (E bracket 0.24-3.7 GPa, search-summary)")
for E in (0.24e9, 1e9, 3.7e9):
    for req in (rows[0][0], base, rows[-1][0]):
        d = (64 * req / (E * math.pi)) ** 0.25
        print(f"  E={E/1e9:4.2f} GPa EI_req={req:.1e} -> d = {d*1e3:.2f} mm")
