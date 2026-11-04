"""Challenge 247: independent arithmetic. CALCULATED, not observed.
Written without reusing replicate-203_calc.py; closed-form minimum where possible."""
import math
g, rho = 9.81, 1.225

def pmin_closed(m, b, k, CDb, X1):
    # P = A/V + B V^3 ; dP/dV=0 -> V^4 = A/(3B); Pmin_am = (4/3) A / V
    W = m*g; Sd = math.pi*b*b/4; Sb = 0.00813*m**0.666
    A = k*W*W/(2*rho*Sd); B = 0.5*rho*Sb*CDb
    V = (A/(3*B))**0.25
    return (4/3)*A/V*(1+X1), V

print("1. blind central case m=0.1 kg b=0.3 m k=1.2 CDb=0.1 X1=1.2")
P, V = pmin_closed(0.1, 0.3, 1.2, 0.1, 1.2)
print("   Pmin %.3f W = %.2f W/kg body, Vmp %.2f m/s" % (P, P/0.1, V))
for f in (0.10, 0.25): print("   f=%.2f -> %.0f W/kg muscle" % (f, P/0.1/f))

print("2. 0.4 g forward flight, author's Pennycuick-style model")
for CDb in (0.1, 0.4):
    P, V = pmin_closed(0.0004, 0.08, 1.2, CDb, 1.2)
    print("   b=0.08 CDb=%.1f: %.2f W/kg body Vmp %.2f m/s; f=0.3 -> %.1f; f=0.2 -> %.1f; f=0.014 -> %.0f W/kg muscle"
          % (CDb, P/0.0004, V, P/0.0004/0.3, P/0.0004/0.2, P/0.0004/0.014))

print("3. 0.4 g hover, momentum theory")
W = 0.0004*g
for R, k, M in ((0.04,1.2,1.5),(0.04,1.0,1.0),(0.02,1.2,1.5)):
    Pi = k*math.sqrt(W**3/(2*rho*math.pi*R*R))
    print("   R=%.2f k=%.1f M=%.1f: induced %.2f W/kg body; total/0.3 -> %.1f W/kg muscle" % (R,k,M,Pi/0.0004, M*Pi/0.0004/0.3))

print("4. wingbeat frequency, Pennycuick allometric form, b=0.08 m S=1.07e-3 m2")
m, b, S = 0.0004, 0.08, 1.07e-3
fw = m**(3/8)*g**0.5*b**(-23/24)*S**(-1/3)*rho**(-3/8)
print("   f_wing = %.1f Hz" % fw)

print("5. temperature shift of scup red-muscle optimum, Q10(Vmax)=1.8, Q10(power)=2.29 (search-summary)")
fopt28 = 2.5*1.8**0.8
print("   scup optimum 2.5 Hz at 20 C -> %.1f Hz at 28 C; wingbeat/optimum = %.1f" % (fopt28, fw/fopt28))
print("   scup max power at 28 C: %.1f W/kg (extrapolation, valid only near %.1f Hz)" % (27.9*2.29**0.8, fopt28))
