"""Independent re-derivation for claim 140 (S20-D-D-D). All outputs are CALCULATED."""
from math import sqrt
g = 9.81
# Soares & Bierman 2013 (PLoS ONE 8:e61617), Table 1 / Discussion, full-text
v_air_mean, v_air_sd = 123.57, 30.0     # cm/s, max velocity in air, 20 jumps, 5 fish (measured)
v_water_mean = 102.36                   # cm/s, max velocity in water (Discussion says 100.16)
cstart_lo, cstart_hi = 70.0, 80.0       # cm/s, authors' EXTRAPOLATED burst speed (not measured)
cstart_mid = (cstart_lo + cstart_hi) / 2
# Danio C-start burst: 0.842 (0.78-0.91) m/s, from Re 27,800 at 33 mm TL (Danos & Lauder 2012) as
# inherited from upstream S20 doc; I could not access the paper to check Re. Check the inversion:
print(f"Re*nu/L = {27800*1.0e-6/0.033:.3f} m/s (nu=1.0e-6)  {27800*0.84e-6/0.033:.3f} m/s (nu=0.84e-6, 28C)")
vd, vd_lo, vd_hi = 0.842, 0.78, 0.91

def ratio(v, c): return v / c
r_mid, r_lo, r_hi = ratio(v_air_mean, cstart_mid), ratio(v_air_mean, cstart_hi), ratio(v_air_mean, cstart_lo)
up = v_air_mean + 2 * v_air_sd
u_mid, u_lo, u_hi = ratio(up, cstart_mid), ratio(up, cstart_hi), ratio(up, cstart_lo)
print(f"jump/C-start ratio (air mean): {r_mid:.3f} ({r_lo:.3f}-{r_hi:.3f})")
print(f"typical Danio exit: {vd*r_mid:.3f} ({vd_lo*r_lo:.3f}-{vd_hi*r_hi:.3f}) m/s")
print(f"upper tail (mean+2SD) ratio {u_mid:.3f}; Danio: {vd*u_mid:.3f} ({vd_lo*u_lo:.3f}-{vd_hi*u_hi:.3f}) m/s")
print(f"mean+1SD alternative: {vd*(v_air_mean+v_air_sd)/cstart_mid:.3f} m/s")
print(f"in-water ratio alternative: {v_water_mean/cstart_mid:.3f} -> {vd*v_water_mean/cstart_mid:.3f} m/s")
v1 = 3.13; print(f"range at 45deg for 3.13 m/s: {v1**2/g:.3f} m;  v for 1 m: {sqrt(g):.3f};  v for 0.5 m: {sqrt(0.5*g):.3f} m/s")
print(f"speed floor old 3.13/1.82 = {3.13/1.82:.2f}x; new 3.13/{vd_hi*u_hi:.2f} = {3.13/(vd_hi*u_hi):.2f}x; 3.13/{vd*u_mid:.2f} = {3.13/(vd*u_mid):.2f}x")
print(f"0.5 m need {sqrt(0.5*g)*3.13/sqrt(g):.3f} m/s (3.13/sqrt2) vs generous corner {vd_hi*u_hi:.2f}")
