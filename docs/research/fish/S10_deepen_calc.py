"""S10-D sensitivity: recompute S10's hover requirement with each input halved/doubled.
All outputs are CALCULATIONS (Rankine-Froude momentum theory), not observations."""
import math
g, rho, k = 9.81, 1.2, 1.2
def req(m=0.4e-3, R=0.04, M=1.5, f=0.3):
    W = m*g; A = math.pi*R**2
    P = k*math.sqrt(W**3/(2*rho*A))
    return M*P/(m*f)            # W per kg flight muscle
base = dict(m=0.4e-3, R=0.04, M=1.5, f=0.3)   # S10 most generous case
print(f"baseline most-generous requirement: {req(**base):.1f} W/kg muscle")
SUSTAINED_MAX, BURST = 10.0, 134.4     # measured ceilings quoted by S10
for key in base:
    for fac in (0.5, 2.0):
        p = dict(base); p[key] *= fac
        r = req(**p)
        print(f"{key} x{fac}: {r:6.1f} W/kg | sustained(<=10) ok? {r<=SUSTAINED_MAX} | burst(134) ok? {r<=BURST}")
print("\nThreshold f for sustained at 10 W/kg (R=4cm,M=1.5):", round(req(f=1.0)/10,2))
print("Threshold f for burst at 134 W/kg (R=4cm,M=1.5):", round(req(f=1.0)/134.4,3))
print("Threshold f for burst at 134 W/kg (R=2cm,M=2.0):", round(req(R=0.02,M=2.0,f=1.0)/134.4,3))
print("\nRequirement vs f (R=4cm,M=1.5 | R=2cm,M=2):")
for f in (0.005,0.01,0.02,0.03,0.05,0.10,0.16,0.20,0.30):
    print(f"  f={f:5.3f}: {req(f=f):7.0f} | {req(R=0.02,M=2.0,f=f):7.0f} W/kg")

# --- Improved input (S10-D) ---
# Measured proxy: Abudefduf saxatilis pectoral abductor+adductor = 0.69 % body mass PER FIN
# (Mansuit & Herrel 2021 Table 1, compiled from Thorsen & Westneat 2005). Two fins -> 1.38 %.
f_proxy = 2*0.0069
print(f"\nImproved f (two-fin, labriform proxy) = {f_proxy:.4f}")
for lab, kw in (("most generous R=4cm M=1.5", dict(R=0.04, M=1.5)),
                ("R=4cm M=2.0", dict(R=0.04, M=2.0)),
                ("R=2cm M=1.5", dict(R=0.02, M=1.5)),
                ("realistic R=2cm M=2.0", dict(R=0.02, M=2.0))):
    r = req(f=f_proxy, **kw)
    print(f"  {lab}: {r:6.0f} W/kg muscle; x{r/134.4:4.1f} larval zebrafish fast (134.4); x{r/433:4.1f} best quail in vitro (433)")
# Independent empirical check: Marden 1987 max lift per flight-muscle mass 54-63 N/kg
for L in (54, 63, 86):
    print(f"  Marden: min flight-muscle fraction to lift own weight at {L} N/kg = {g/L:.3f}; enlargement vs proxy x{g/L/f_proxy:.1f}")
print(f"  f needed (generous 0.075 / realistic 0.20) vs proxy: x{0.075/f_proxy:.1f} / x{0.20/f_proxy:.1f}")
