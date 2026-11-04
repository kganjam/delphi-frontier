# Independent recomputation for challenge 283 (claim from S15-dna.md §3.1-3.2).
# All outputs are CALCULATIONS, not observations.
rho, g, m = 1.225, 9.81, 4.0e-4          # kg/m3, m/s2, kg (inputs as stated by author)
W = m * g
sil = 4.0 * 0.5 * 0.7                    # cm2, author's assumed dorsal silhouette
def S(V, CL): return 2 * W / (rho * V**2 * CL) * 1e4   # cm2
print(f"W = {W*1e3:.4f} mN, silhouette = {sil:.2f} cm2")
for V in (1, 2, 3.9, 5.2, 7.56, 10):
    for CL in (0.5, 0.8, 1.2, 1.5):
        s = S(V, CL); print(f"V={V:5.2f} CL={CL:3.1f}  S={s:7.2f} cm2  S/sil={s/sil:6.2f}")
Vpar = (2 * W / (rho * sil * 1e-4 * 0.8)) ** 0.5
print(f"silhouette parity speed (CL 0.8) = {Vpar:.2f} m/s")
# glide-angle relaxation: L = W cos(theta); L/D=2 -> theta=26.6 deg
import math
for LD in (2, 3, 4.4):
    th = math.atan(1 / LD); print(f"L/D={LD}: cos(theta)={math.cos(th):.3f} -> S@2m/s = {S(2,0.8)*math.cos(th):.1f} cm2")
