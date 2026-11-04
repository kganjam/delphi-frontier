# Independent calc for claim 196 (S24 surface taxiing). Run: python3 -I docs/research/fish/replicate-196_calc.py
TL = 0.036          # m, Palstra et al. 2010 (PLoS ONE) adult zebrafish total length
m = 0.43e-3         # kg, Palstra et al. 2010 body mass
g, rho = 9.81, 1.2
Ucrit = 0.548       # m/s, Palstra et al. 2010
targets = {"3-BL": 1.95, "1-BL": 5.84}
print("ratio 1-BL/3-BL target:", round(5.84/1.95, 3))
# implied C_L*S for lift = weight at each target, and implied AR at C_L=1 for span b=n*TL
for k, V in targets.items():
    n = 3 if k == "3-BL" else 1
    CLS = 2*m*g/(rho*V**2)
    b = n*TL
    print(k, "C_L*S =", f"{CLS*1e4:.2f} cm^2", " implied AR at C_L=1:", round(b**2/CLS, 2))
# Strouhal-required tail-beat frequency f = St*U/A (A = peak-to-peak tail amplitude)
for k, V in targets.items():
    for Afrac in (0.15, 0.20, 0.25):
        row = [f"{St*V/(Afrac*TL):6.1f}" for St in (0.2, 0.3, 0.4)]
        print(k, f"U={V}", f"A={Afrac}TL", "f(St=.2,.3,.4) Hz:", row)
# Speed reachable at f=21 Hz (review upper range), A=0.2TL, St 0.2-0.4: U = f*A/St
for St in (0.2, 0.3, 0.4):
    print("U at 21 Hz, A=0.2TL, St", St, "=", round(21*0.2*TL/St, 3), "m/s")
# Gap from exit-speed candidates
for name, u0 in (("Ucrit Palstra", 0.548), ("S20 Re-inversion", 0.84)):
    for k, V in targets.items():
        print(name, k, "gap dV =", round(V-u0, 2), "m/s; KE ratio =", round((V/u0)**2, 1))
