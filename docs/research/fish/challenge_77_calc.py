"""Challenge 77: independent recomputation of S10-D, plus a forward-flight relaxation.
Every output here is a CALCULATION. Assumed inputs are labelled ASSUMPTION."""
import math
g, rho, k = 9.81, 1.2, 1.2
m = 0.4e-3; W = m * g                     # S10 input
f = 2 * (0.13 + 0.23 + 0.15 + 0.18) / 100  # Mansuit & Herrel 2021 Table 1, Abudefduf, per fin x2
print(f"per-fin sum = {0.13+0.23+0.15+0.18:.2f} %, two fins f = {f:.4f}")

def hover(R, M):
    return M * k * math.sqrt(W**3 / (2 * rho * math.pi * R**2))   # W

for R, M in ((0.04, 1.5), (0.04, 2.0), (0.02, 1.5), (0.02, 2.0)):
    P = hover(R, M)
    print(f"hover R={R*100:.0f}cm M={M}: {P*1e3:.2f} mW, {P/m:.2f} W/kg body, "
          f"{P/(m*f):.0f} W/kg muscle at f={f:.4f}, x{P/(m*f)/134.4:.1f} over 134.4, "
          f"threshold f={P/m/134.4:.3f}")

# Forward flight relaxation. ASSUMPTIONS: body frontal area Sb=2.2e-5 m^2 (7 x 4 mm ellipse),
# C_Db=0.4; wing area S=(2R)^2/6 (S10's AR=6); profile drag C_Dpro 0.05..0.2 (steady, low Re;
# flapping profile is higher); speed floor from C_L,max=1.5 (S10's own assumption).
Sb, CDb, CLmax = 2.2e-5, 0.4, 1.5
for R in (0.04, 0.02):
    S = (2 * R)**2 / 6; A = math.pi * R**2
    Vmin = math.sqrt(2 * W / (rho * CLmax * S))
    for CDp in (0.05, 0.1, 0.2):
        best = None
        for i in range(1, 2000):
            V = i * 0.005
            if V < Vmin: continue
            P = k * W**2 / (2 * rho * A * V) + 0.5 * rho * V**3 * (Sb * CDb + S * CDp)
            if best is None or P < best[1]: best = (V, P)
        V, P = best
        for M in (1.5, 2.0):
            ratio = P / hover(R, M)
            print(f"fwd R={R*100:.0f}cm CDpro={CDp}: Vmp={V:.2f} m/s (Vmin {Vmin:.2f}), "
                  f"P={P*1e3:.2f} mW = {ratio:.2f} x hover(M={M}); "
                  f"{P/(m*f):.0f} W/kg muscle, x{P/(m*f)/134.4:.1f} over 134.4")
