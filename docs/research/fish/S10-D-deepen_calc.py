"""S10-D-D: sensitivity of S10-D's burst verdict, and recompute with the improved f.
All outputs are CALCULATIONS (Rankine-Froude momentum theory, same model as S10/S10-D).
Nothing printed here is an observation."""
import math
g, rho, k = 9.81, 1.2, 1.2
P_FAST = 134.4   # W/kg, larval zebrafish fast muscle, 80 Hz, 28 C (Mead et al. 2020, measured; carried from S10)
P_FAST_40 = 2.63 * 40  # W/kg, computed in S10 from measured 2.63 J/kg/cycle at 40 Hz

def p_ind(m=0.4e-3, R=0.04):
    W = m * g
    return k * math.sqrt(W**3 / (2 * rho * math.pi * R**2))

def req(m=0.4e-3, R=0.04, M=1.5, f=0.0138):
    return M * p_ind(m, R) / (m * f)      # W per kg flight muscle

base = dict(m=0.4e-3, R=0.04, M=1.5, f=0.0138)   # S10-D generous case
r0 = req(**base)
print(f"S10-D generous requirement: {r0:.0f} W/kg muscle; margin vs {P_FAST} = x{r0/P_FAST:.2f}")
print("\nOne-at-a-time x0.5 / x2 (W/kg muscle), and factor needed to flip burst verdict:")
for key in base:
    out = []
    for fac in (0.5, 2.0):
        p = dict(base); p[key] *= fac; out.append(req(**p))
    # factor needed to bring requirement to P_FAST
    need = r0 / P_FAST
    flip = need**2 if key == 'm' else need   # req ~ m^0.5, linear in 1/R, M, 1/f
    print(f"  {key}: x0.5 -> {out[0]:6.0f}, x2 -> {out[1]:6.0f}; flips at x{1/flip if key=='m' else (1/flip if key=='M' else flip):.3g}")
print(f"  muscle power density: flips only if real power >= x{r0/P_FAST:.2f} the measured {P_FAST}")

print("\nImproved f bracket (both fins):")
cases = {
 "S10-D four-group sum (0.69%/fin)": 2*0.0069,
 "bluegill 'two largest = half girdle' rule applied to Abudefduf two largest (0.23+0.18)": 2*2*(0.0023+0.0018),
 "bluegill rule applied to the whole four-group sum (upper bracket)": 2*2*0.0069,
}
for lab, f in cases.items():
    out = [req(f=f), req(f=f, M=2.0), req(f=f, R=0.02), req(f=f, R=0.02, M=2.0)]
    print(f"  f={f:.4f}  {lab}")
    print("     req W/kg [R4M1.5, R4M2, R2M1.5, R2M2] = " + ", ".join(f"{x:.0f}" for x in out)
          + f" | generous shortfall vs 134.4: x{out[0]/P_FAST:.2f}; vs 105 (40 Hz): x{out[0]/P_FAST_40:.2f}")

print("\nf-independent check: whole-body power (W/kg body)")
pb = 1.5 * p_ind() / 0.4e-3
print(f"  generous hover requirement M*P_ind/m = {pb:.1f} W/kg body")
for pm in (0.15, 0.21):
    print(f"  vs bluegill max labriform Pmech {pm} W/kg body (Jones et al. 2007, abstract): x{pb/pm:.0f}")

print("\nStacked generous errors (f x2 bluegill-upper, forward flight halves power):")
f_up = 2*2*0.0069
for fwd in (1.0, 0.5):
    r = req(f=f_up) * fwd
    print(f"  forward-flight factor {fwd}: {r:.0f} W/kg; vs 134.4 x{r/P_FAST:.2f}")
print(f"\nMarden threshold f 0.114-0.182 vs bracket {2*0.0069:.4f}-{f_up:.4f}: "
      f"short by x{0.114/f_up:.1f} to x{0.182/(2*0.0069):.1f}")
