"""Challenge 97: independent recomputation. Every output is CALCULATED; nothing here is measured.
Run: python3 -I challenge-97_calc.py"""
from math import log
EI_REQ, EI_P, F_A, L_REQ, L_BG = 6.3e-4, 3.8e-6, 12.0, 0.120, 0.0403
s4 = (L_REQ / L_BG) ** 4
need = EI_REQ / (EI_P * s4)
print(f"1. isometric scale x{s4:.2f}; scaled passive EI {EI_P*s4:.3e}; factor needed {need:.3f}; 12x margin {F_A/need:.2f}")
print(f"   break-even source length {L_REQ/(EI_REQ/(EI_P*F_A))**0.25*1e3:.1f} mm")
# 2. relax isometry: d ~ L^alpha at constant E and shape -> EI ~ L^(4 alpha)
r = L_REQ / L_BG
alpha = log(EI_REQ / (EI_P * F_A)) / (4 * log(r))
print(f"2. 12x closes only if d scales as L^alpha with alpha >= {alpha:.3f}")
for a in (0.0, 0.5, 0.6, 0.75, 1.0):
    print(f"   alpha={a:4.2f}: 12x margin {EI_P*r**(4*a)*F_A/EI_REQ:6.2f}")
# 3. stacking check: Alben 1.98 N/m clamped, point load at 2/3 L, uniform cantilever k=3EI/a^3
for L in (0.0403, 0.030, 0.020):
    a = 2 * L / 3; ei_cl = 1.98 * a**3 / 3; sc = (L_REQ / L) ** 4
    print(f"3. tested L={L*1e3:4.1f} mm: EI_clamped {ei_cl:.3e}; 3.8e-6*12 = {EI_P*F_A:.2e} is x{EI_P*F_A/ei_cl:.1f} of it;"
          f" clamped scaled to 120 mm {ei_cl*sc:.3e}; margin vs 6.3e-4 {ei_cl*sc/EI_REQ:.2f},"
          f" vs x1.47 {ei_cl*sc/(EI_REQ*1.47):.2f}, vs 3.1e-3 {ei_cl*sc/3.1e-3:.2f}")
# 4. Puri 2018 zebrafish in vivo whole caudal fin EI 1.5e-9..4e-9 N m^2, 16-18 rays, interray negligible
lo, hi = 1.5e-9 / 18, 4e-9 / 16
print(f"4. zebrafish per-ray EI (parallel-sum assumption) {lo:.2e} .. {hi:.2e} N m^2")
rlo, rhi = EI_P / hi, EI_P / lo
print(f"   bluegill/zebrafish per-ray ratio {rlo:.2e} .. {rhi:.2e}")
print(f"   implied exponent on d at nominal d ratio 10: {log(rlo)/log(10):.2f} .. {log(rhi)/log(10):.2f};"
      f" over d ratio 5..20: {log(rlo)/log(20):.2f} .. {log(rhi)/log(5):.2f}")
