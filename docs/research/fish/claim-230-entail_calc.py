"""Arithmetic behind claim-230-entail.md. Every output is CALCULATED, not measured."""
need_body = 10.17          # J/kg body, S29 central case (derived by S29)
f, eta_s, eta_h = 0.30, 0.93, 0.37
rho_m = 1060.0             # kg/m^3 muscle density, ASSUMED
w_thr = need_body / (f * eta_s * eta_h)
print(f"C1 threshold w = {w_thr:.1f} J/kg muscle")
print(f"   with measured spring-release chain 0.10 (Conte 2010): w = {need_body/(f*0.10):.0f} J/kg muscle")
for name, s0 in [("sculpin fast fibre 281 kPa", 281e3), ("larval zebrafish tail 76 kPa", 76e3)]:
    e_const = w_thr * rho_m / s0
    print(f"C2 {name}: strain needed constant-force {e_const:.2f}, linear-spring {2*e_const:.2f}")
print(f"C3 f needed at w=81 (frog max): {need_body/(81*eta_s*eta_h):.2f}; at w=53: {need_body/(53*eta_s*eta_h):.2f}")
for name, p in [("vertebrate instantaneous max 1121 W/kg", 1121), ("scorpionfish fast-start 142.7 W/kg", 142.7), ("larval zebrafish work loop 134 W/kg", 134)]:
    print(f"C5 t_load >= {w_thr/p*1000:.0f} ms  ({name})")
print(f"C5 ratio t_load/t_release: {w_thr/1121/0.01373:.1f} (fastest load, slowest 13.7 ms release) to {w_thr/134/0.00229:.0f}")
