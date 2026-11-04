"""Independent re-derivation for claim 203 ([S10] sustained flapping).
CALCULATED, not observed. Minimum mechanical power for level flapping flight
(Pennycuick-style actuator-disc model) vs sustainable fish-muscle power."""
import itertools, math
g, rho = 9.81, 1.225          # SI; sea-level air
def pmin(m, b, k=1.2, CDb=0.1, X1=1.2):
    Sd = math.pi*b*b/4                 # disc area from span
    Sb = 0.00813*m**0.666              # body frontal area (Pennycuick allometry, recalled)
    W = m*g
    best = None
    for i in range(1, 4000):
        V = i*0.005
        Pind = k*W*W/(2*rho*Sd*V)
        Ppar = 0.5*rho*V**3*Sb*CDb
        if best is None or Pind+Ppar < best[0]:
            best = (Pind+Ppar, V)
    Pam, V = best
    return Pam*(1+X1), V               # profile power = X1 * absolute-minimum power
rows = []
for m, b, k, CDb, X1 in itertools.product([0.05,0.1,0.3],[0.2,0.3,0.45],[1.1,1.2,1.3],[0.1,0.25,0.4],[0.8,1.2,1.6]):
    P, V = pmin(m,b,k,CDb,X1); rows.append((P/m, m, b, k, CDb, X1, V))
rows.sort()
print("n=%d  body-specific Pmin: min %.1f  median %.1f  max %.1f W/kg" % (len(rows), rows[0][0], rows[len(rows)//2][0], rows[-1][0]))
P, V = pmin(0.1, 0.3); print("central case m=0.1 kg b=0.3 m: Pmin=%.2f W = %.1f W/kg body at V=%.1f m/s" % (P, P/0.1, V))
# Required muscle-mass-specific power = (P/m)/f for muscle fraction f
for f in (0.05, 0.10, 0.17, 0.25):
    print("f=%.2f: required %.0f W/kg muscle (central); range %.0f-%.0f" % (f, P/0.1/f, rows[0][0]/f, rows[-1][0]/f))

# --- Added AFTER reading the recorded claim's scale (m = 0.4 g; span ~8 cm) ---
# Same model, unchanged; only the mass/span inputs were taken from the claim's framing.
print("post-read scale check, m=0.4 g:")
for b in (0.04, 0.08):
    for CDb in (0.1, 0.4):
        P, V = pmin(0.0004, b, 1.2, CDb, 1.2)
        print("  b=%.2f m CDb=%.1f: %.1f W/kg body, V=%.1f m/s; f=0.3 -> %.0f W/kg muscle" % (b, CDb, P/0.0004, V, P/0.0004/0.3))
# hover, ideal-ish, own form: P = k*sqrt(W^3/(2 rho A)), A = pi R^2, plus profile X1
for R in (0.02, 0.04):
    W = 0.0004*g; Pi = 1.2*math.sqrt(W**3/(2*rho*math.pi*R*R))
    print("  hover R=%.2f: induced %.1f W/kg body; x(1+0.5 profile)/0.3 -> %.0f W/kg muscle" % (R, Pi/0.0004, Pi/0.0004*1.5/0.3))
