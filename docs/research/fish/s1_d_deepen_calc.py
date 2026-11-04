"""S1-D-D sensitivity and recompute. Every number printed here is CALCULATED, not observed.

Inputs and where they come from (see S1-D-deepen.md for read-levels):
  m = 0.4 g                        S1 question premise
  SL = 3.5 cm                      assumed (inherited from S1-D)
  S = 1-4 cm^2, CL = 0.5-1.5       assumed (inherited from S1-D)
  rho_air = 1.20 kg/m^3, g = 9.81  standard values
  Demesmay et al. 2025: peak 1.57 +/- 0.27 m/s (SD), 3.8 cm in first 40 ms  [author-reported]
  Danos & Lauder 2012: mean max Re 27,800 +/- 2140 (s.e.m.) at 1 mPa s, TL 33.0 mm, N = 5  [author-reported]
"""
import math
g, rho_air = 9.81, 1.20
m, SL = 0.4e-3, 0.035

def LW(v, S, CL, m=m):            # lift / weight at speed v (law: takeoff-stall-speed, inverted)
    return rho_air*S*CL*v**2/(2*m*g)

def h(v):                          # drag-free ballistic apex: an UPPER bound
    return v**2/(2*g)

CENTRAL = dict(S=2e-4, CL=1.0)
GENEROUS = dict(S=4e-4, CL=1.5)

print("1. Sensitivity of the S1-D conclusions at the S1-D key number v = 1.57 m/s")
for name, c in (("central", CENTRAL), ("generous", GENEROUS)):
    lw = LW(1.57, **c)
    print(f"  A/{name}: L/W={lw:.3f}; factor to flip: v x{(1/lw)**0.5:.2f}, S or CL x{1/lw:.1f}, m /{1/lw:.1f}")
    for lab, kw in (("v x2", dict(v=3.14, **c)), ("S x2", dict(v=1.57, S=2*c['S'], CL=c['CL'])),
                    ("CL x2", dict(v=1.57, S=c['S'], CL=2*c['CL'])), ("m /2", dict(v=1.57, m=m/2, **c))):
        print(f"     {lab}: L/W = {LW(**kw):.3f}")
vlb = 0.038/0.040
print(f"  B: at S1-D lower bound v={vlb:.2f}: h={h(vlb)*100:.2f} cm = {h(vlb)/SL:.2f} SL; "
      f"flips (<1 SL) if v falls by x{math.sqrt(2*g*SL)/vlb:.2f} (to {math.sqrt(2*g*SL):.2f} m/s) "
      f"or SL rises by x{(h(vlb)/SL):.2f}")
print(f"     v/2 -> {h(vlb/2)/SL:.2f} SL; SL x2 -> {h(vlb)/(2*SL):.2f} SL")

print("2. Danos & Lauder 2012: invert Re = rho_w U L / mu (derived, not stated by the authors)")
rho_w, mu = 1000.0, 1.0e-3
Re, Re_sem, TL, TL_sd = 27800, 2140, 0.0330, 0.0013
U = Re*mu/(rho_w*TL)
print(f"  U(TL) = {U:.3f} m/s  (+/- {Re_sem*mu/(rho_w*TL):.3f} from Re s.e.m.); "
      f"L range {TL-TL_sd:.4f}-{TL+TL_sd:.4f} -> {Re*mu/(rho_w*(TL+TL_sd)):.2f}-{Re*mu/(rho_w*(TL-TL_sd)):.2f} m/s")
U_SL = Re*mu/(rho_w*0.8*TL)       # if Re used SL ~ 0.8 TL (assumption)
print(f"  if Re used SL = 0.8 TL (assumed ratio): U = {U_SL:.2f} m/s")
print(f"  length-specific: {U/TL:.1f} TL/s")
print("  Demesmay length-specific: "
      f"{1.57/0.036:.0f} BL/s (3.6 cm fish) to {1.57/0.026:.0f} BL/s (2.6 cm fish)")
print(f"  source ratio Demesmay/Danos = {1.57/U:.2f} (TL basis), {1.57/U_SL:.2f} (SL basis)")

print("3. Recompute both readings across the disagreement (no averaging)")
rows = [("Danos-derived, TL basis", U), ("Danos-derived, SL basis", U_SL),
        ("Demesmay 40-ms mean", vlb), ("Demesmay peak", 1.57), ("Demesmay peak +1SD", 1.84)]
for lab, v in rows:
    print(f"  {lab:24s} v={v:.2f}: L/W central={LW(v, **CENTRAL):.3f} generous={LW(v, **GENEROUS):.3f} "
          f"| h={h(v)*100:.1f} cm = {h(v)/SL:.2f} SL")
v_req_c = math.sqrt(2*m*g/(rho_air*2e-4*1.0))
v_req_g = math.sqrt(2*m*g/(rho_air*4e-4*1.5))
print(f"  v_req central = {v_req_c:.2f} m/s, generous = {v_req_g:.2f} m/s")
for lab, v in rows:
    print(f"  shortfall {lab:24s}: central x{v_req_c/v:.2f}, generous x{v_req_g/v:.2f}")
print(f"  v to clear 1 SL (3.5 cm): {math.sqrt(2*g*SL):.3f} m/s")
