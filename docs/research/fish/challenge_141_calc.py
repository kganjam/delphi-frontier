"""Challenge 141: independent recompute. Every printed number is CALCULATED, not observed."""
import math
g, rho_a, m = 9.81, 1.20, 0.4e-3
k = lambda S, CL: rho_a*S*CL/(2*m*g)          # L/W = k * v^2
for v in (0.84, 0.95, 1.05, 1.57, 1.84):
    print(f"v={v}: L/W central={k(2e-4,1)*v*v:.3f} generous={k(4e-4,1.5)*v*v:.3f} apex={v*v/(2*g)*100:.2f} cm")
print("v to clear 3.5 cm:", round(math.sqrt(2*g*0.035), 3), "ratio to 0.95:", round(math.sqrt(2*g*0.035)/0.95, 3))
U = 27800*1e-3/(1000*0.033); print("Danos U (TL, mu=1 mPa s):", round(U, 3))
print("Danos U if mu=0.83 mPa s (water ~28 C, ASSUMED temp; not reported):", round(27800*0.83e-3/(1000*0.033), 3))
for nu_mu, Re in ((10e-3, 2350), (20e-3, 820)):
    print(f"internal check, mu={nu_mu}: U={Re*nu_mu/(1000*0.033):.2f} m/s (rho=1000 assumed)")
# size mismatch: Danos fish SL = 0.8*33 mm (assumed ratio, the author's own)
SLd, SLa = 0.8*0.033, 0.035
h = U*U/(2*g)
print(f"Danos apex {h*100:.2f} cm = {h/SLa:.2f} x 3.5-cm SL (claim) but {h/SLd:.2f} x Danos's own SL {SLd*100:.2f} cm")
for a in (0.0, 0.5, 1.0):                     # v ~ L^a, scaled from Danos fish to 3.5 cm SL fish
    v = U*(SLa/SLd)**a; print(f"  scaling exponent {a}: v={v:.3f} apex={v*v/(2*g)/SLa:.2f} SL")
