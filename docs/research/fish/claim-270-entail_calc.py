"""Claim 270 entailment checks. All outputs are CALCULATED from S32 inputs plus
one figure read-off (Azevedo et al. 2011 Fig 2B/C). Nothing here is an observation."""
rho, g, U = 998.0, 9.81, 0.45
q = 0.5 * rho * U**2
s2c = 2 * 0.072 * 0.006            # meniscus bound 2*sigma*c, N
cases = {  # name: (mass kg, V_to, phi, cos theta, S32 net horiz force at 0.45 m/s, N)
    "generous": (0.25e-3, 4.41, 1.0, 0.0, +4.09e-3),
    "central":  (0.25e-3, 4.41, 0.5, 0.5, -1.50e-3),
    "stingy":   (0.40e-3, 5.58, 0.25, 1.0, -34.9e-3),
}
# C1: immersed area bound at CL_z = 1, and CL_z needed with the measured fin area
print("C1  q = %.1f Pa" % q)
for n, (m, V, phi, c, _) in cases.items():
    need = m * g * (1 - (U / V) ** 2) + s2c * c
    print(f"  {n}: need {need*1e3:.3f} mN -> S_imm bound {need/q*1e6:.1f} mm2")
for whole in (29.5, 33.0, 40.0):       # mm2, Azevedo Fig 2 read-off (mean ~29.5-33, top of SD bar ~40)
    lobe = whole / 2                   # ASSUMED symmetric lobes
    need = 0.25e-3 * g * (1 - (U / 4.41) ** 2)
    print(f"  whole fin {whole} mm2 -> lobe {lobe:.1f} mm2 -> generous CL_z needed {need/(q*lobe*1e-6):.2f};"
          f" U_min(CLz=1) {((0.25e-3*g)/(0.5*rho*lobe*1e-6 + 0.25e-3*g/4.41**2))**0.5:.3f} m/s")
# C4: time to accelerate to U_min vs time to sink, S32 lobe area 18.9 mm2
S_lobe = 18.9e-6
for n, (m, V, phi, c, Fnet) in cases.items():
    W = m * g; F = s2c * c; S = phi * S_lobe
    Umin = ((W + F) / (0.5 * rho * S + W / V**2)) ** 0.5
    deficit = W * (1 - (U / V) ** 2) + F - q * S        # vertical shortfall at CL_z = 1, N
    a_down = deficit / m
    if Fnet > 0:
        t_acc = m * (Umin - U) / Fnet                   # upper bound-ish: holds S32's net at 0.45
        drop = 0.5 * a_down * t_acc**2                  # upper bound: deficit shrinks as U rises
        print(f"C4 {n}: U_min {Umin:.3f}, t_acc {t_acc*1e3:.1f} ms, drop in t_acc <= {drop*1e6:.0f} um,"
              f" drop in one 52 Hz stroke <= {0.5*a_down*(1/52)**2*1e3:.2f} mm")
    else:
        print(f"C4 {n}: net {Fnet*1e3:+.2f} mN -> never reaches U_min {Umin:.3f};"
              f" sinks 1 mm in {(2*1e-3/a_down)**0.5*1e3:.1f} ms")
