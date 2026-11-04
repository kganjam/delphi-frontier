# Replicate 247: minimum mechanical power for level flapping flight (Pennycuick-style
# actuator-disc + parasite + profile), vs sustainable fish red-muscle power. CALCULATED, not observed.
import math
g, rho, k, CDb = 9.81, 1.225, 1.2, 0.10
def pmin(m, AR=7.0):
    b = 1.17 * m**0.39                 # bird span allometry (assumed)
    Sd = math.pi*b*b/4
    Sb = 0.00813 * m**0.666            # body frontal area (Pennycuick 2008)
    best = None
    for i in range(1, 4000):
        V = i*0.005
        Pi = k*(m*g)**2/(2*rho*V*Sd)
        Pp = 0.5*rho*V**3*Sb*CDb
        if best is None or Pi+Pp < best[0]: best = (Pi+Pp, V)
    Pam = 1.05*k**0.75*m**1.5*g**1.5*Sb**0.25*CDb**0.25/(rho**0.5*b**1.5)
    Ppro = (8.4/AR)*Pam
    return best[0]+Ppro, best[1], b
print("m_kg  span_m  Vmp_m/s  Pmin_W  Pmin_W/kgbody  req_W/kgmuscle(f=0.05,0.10,0.17,0.25)")
for m in (0.05, 0.1, 0.2, 0.3):
    P, V, b = pmin(m)
    print(f"{m:4.2f}  {b:5.3f}  {V:6.2f}  {P:6.3f}  {P/m:6.1f}   " + "  ".join(f"{P/m/f:6.0f}" for f in (0.05,0.10,0.17,0.25)))

# Sensitivity run, added AFTER comparison: span fixed at 0.3 m for 0.1 kg (short, flying-fish-like wing)
import math as _m
def pmin_b(m, b, AR=7.0):
    Sd=_m.pi*b*b/4; Sb=0.00813*m**0.666
    best=min(((k*(m*g)**2/(2*rho*V*Sd)+0.5*rho*V**3*Sb*CDb),V) for V in [i*0.005 for i in range(1,4000)])
    Pam=1.05*k**0.75*m**1.5*g**1.5*Sb**0.25*CDb**0.25/(rho**0.5*b**1.5)
    return best[0]+(8.4/AR)*Pam, best[1]
P,V=pmin_b(0.1,0.3); print(f"b=0.30 m, m=0.1 kg: Pmin={P:.3f} W, {P/0.1:.1f} W/kg body, Vmp={V:.2f}; f=0.10/0.25 -> {P/0.1/0.10:.0f}/{P/0.1/0.25:.0f} W/kg muscle")
