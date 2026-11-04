"""Challenge 135: independent recomputation of S6-D-D. CALCULATION ONLY -- nothing here is an observation."""
import math
g = 9.81
# --- inputs exactly as stated in the claim / S6-D model ---
k, Lbg = 1.98, 40.3e-3                 # Alben 2007 (relayed), N/m and m
m, L, N, c = 0.10, 0.12, 14, 0.10      # S6-D scenario (assumptions)
P = m * g / (2 * N)                     # per-ray share of weight, N
EIreq = P * L**2 / (8 * c)              # uniform load cantilever: delta = P L^3/(8EI)
lam = L / Lbg
print(f"P per ray = {P:.4f} N ; EI_req = {EIreq:.3e} N m^2 ; lambda = {lam:.3f}")

EIb = k * Lbg**3 / 3                    # rigid-root tip point load: largest lever -> UPPER bound
print(f"k-bound EI <= {EIb:.3e}")
print(f"delta/L (linear) at bound = {P*L**2/(8*EIb):.3f}  (linear theory, invalid above ~0.3)")
print(f"beta needed from bound = {math.log(EIreq/EIb)/math.log(lam):.3f}")
for name, EI in [("k-bound (UPPER)", EIb), ("k-bound/12 free-base (UPPER)", EIb/12),
                 ("Alben hi 1e-5", 1e-5), ("Puri-quoted 3.8e-6", 3.8e-6), ("Alben lo 1e-6", 1e-6)]:
    iso = EI * lam**4
    print(f"{name:30s} iso(beta=4)->{iso:.2e}  delta/L={P*L**2/(8*iso):.3f}  "
          f"beta_needed={math.log(EIreq/EI)/math.log(lam):.2f}")
# --- effective solid-equivalent modulus of a bluegill ray (Puri 2018: diameter 1-2 mm) ---
for EI in (EIb, 1e-5, 3.8e-6, 1e-6):
    E = [EI * 64 / (math.pi * d**4) / 1e6 for d in (1e-3, 2e-3)]
    print(f"bluegill EI {EI:.1e}: solid-equivalent E_eff = {E[0]:.1f} MPa (d=1mm) .. {E[1]:.2f} MPa (d=2mm)")
# --- outer diameter a flying-fish ray needs if built like a bluegill ray (EI ~ d^4) ---
for req in (1.8e-4, EIreq, 3.1e-3):
    for EI in (EIb, 1e-5, 3.8e-6):
        f = (req / EI) ** 0.25
        print(f"EI_req {req:.1e}, bluegill EI {EI:.1e}: d_ff = {1*f:.1f}-{2*f:.1f} mm")
# --- the claim's solid threshold at 1 GPa, for comparison ---
for req in (1.8e-4, EIreq, 3.1e-3):
    print(f"solid d at E=1GPa for {req:.1e}: {(64*req/(math.pi*1e9))**0.25*1e3:.2f} mm")
