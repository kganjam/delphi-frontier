"""S1-D sensitivity calculation. Every output of this script is CALCULATED, not observed."""
import math
g, rho_air = 9.81, 1.20          # m s^-2, kg m^-3 (standard values)
m = 0.4e-3                        # kg, given by the S1 question
SL = 0.035                        # m, assumed adult standard length (assumption, not retrieved)

def v_glide(S, CL):               # minimum airspeed for lift = weight
    return math.sqrt(2*m*g/(rho_air*S*CL))

def lift_over_weight(v, S, CL):
    return rho_air*S*CL*v**2/(2*m*g)

def ballistic_height(v):          # drag-free, no entrained water: an UPPER bound
    return v**2/(2*g)

print("A. Aerial takeoff (lift >= weight)")
for S_cm2 in (1.0, 2.0, 4.0):
    for CL in (0.5, 1.0, 1.5):
        print(f"  S={S_cm2} cm^2 CL={CL}: v_req = {v_glide(S_cm2*1e-4, CL):.2f} m/s")
base = dict(S=2e-4, CL=1.0)
for label, v in (("Ucrit 0.56", 0.56), ("2x Ucrit 1.12", 1.12), ("4x Ucrit 2.24", 2.24)):
    print(f"  L/W at {label} m/s (S=2 cm^2, CL=1): {lift_over_weight(v, **base):.3f}")
print(f"  factor on S*CL*v^2 needed to reach L/W=1 at Ucrit: {1/lift_over_weight(0.56, **base):.0f}x")

print("B. Ballistic exit (clear a height h with vertical exit speed v)")
for label, v in (("Ucrit/2", 0.28), ("Ucrit", 0.56), ("2x Ucrit", 1.12), ("4x Ucrit", 2.24)):
    h = ballistic_height(v)
    print(f"  {label:9s} v={v:.2f} m/s -> h_max = {h*100:.1f} cm = {h/SL:.2f} SL")
print(f"  v needed to clear 1 SL (whole body out, CoM rises ~1 SL): {math.sqrt(2*g*SL):.2f} m/s")
print(f"  v needed to clear 0.5 SL: {math.sqrt(2*g*0.5*SL):.2f} m/s")

print("C. Recompute with the improved input (Demesmay et al. 2025, adult wild-type controls)")
v_peak, v_peak_sd = 1.57, 0.27     # m/s, author-reported 'calculated maximal speed', mean +/- SD
d40, t40 = 0.038, 0.040            # m, s: author-reported distance in first 40 ms
v_mean40 = d40/t40                 # CALCULATED: a noise-robust lower bound on peak speed
print(f"  mean speed over first 40 ms = {v_mean40:.2f} m/s (peak must be >= this)")
for label, v in (("mean40 lower bound", v_mean40), ("peak mean", v_peak), ("peak +1SD", v_peak+v_peak_sd)):
    h = ballistic_height(v)
    print(f"  {label:18s} v={v:.2f}: L/W(S=2,CL=1)={lift_over_weight(v, **base):.3f}  "
          f"L/W(S=4,CL=1.5)={lift_over_weight(v, 4e-4, 1.5):.3f}  ballistic h_max={h*100:.1f} cm = {h/SL:.1f} SL")
for v in (v_peak, v_peak+v_peak_sd):
    S_need = 2*m*g/(rho_air*1.0*v**2)
    print(f"  lifting area needed at v={v:.2f}, CL=1: {S_need*1e4:.1f} cm^2")
print(f"  speed shortfall v_req(S=2,CL=1)/v_peak = {v_glide(2e-4,1.0)/v_peak:.1f}x")
