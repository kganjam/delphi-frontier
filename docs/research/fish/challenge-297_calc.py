#!/usr/bin/env python3
"""Challenge 297: independent recompute of S3-D-D. CALCULATION ONLY, no measurement.
Model (S3 sec 3.5 as stated in S3-D-D): M = m + sigma*S_wing; V = sqrt(2Mg/(rho*S_lift*CL));
run-up from rest at constant accel over s: t = 2s/V; P_muscle = (V^2/2)/t/eta * M/(fm*m) = V^3 M/(4 s eta fm m).
Written from the formula, not copied from S3-D-deepen_calc.py."""
from math import sqrt
g, rho = 9.81, 1.225
m, P_av = 0.40e-3, 142.7
sig = (0.8*1050 + 0.2*1557)*120e-6
Sw, s0, eta0, fm0 = 1070e-6, 2*0.04, 0.37, 0.6

def short(CL, Sb=0.0, s=s0, eta=eta0, fm=fm0, P=P_av, sg=sig, mb=m):
    M = mb + sg*Sw
    V = sqrt(2*M*g/(rho*(Sw+Sb)*CL))
    return V**3*M/(4*s*eta*fm*mb)/P, V

def cl_need(**k):
    # shortfall ∝ CL^-1.5 exactly, so invert in closed form
    r, _ = short(1.0, **k); return r**(2/3)

print("baseline CL1.07 no body: %.3f x, V %.3f" % short(1.07))
print("CL needed no body: %.3f" % cl_need())
for Sb in (120e-6, 240e-6):
    print("body %3.0f mm2: CL needed %.3f; shortfall at CL1.10 %.3f" % (Sb*1e6, cl_need(Sb=Sb), short(1.10, Sb)[0]))

print("\nSensitivity re-run INSIDE the author's own revised (body 240 mm2) model; margin = CL_needed/1.10")
for name, kw in [("eta x2", dict(eta=2*eta0)), ("fm x2", dict(fm=2*fm0)), ("run-up x2", dict(s=2*s0)),
                 ("P x2", dict(P=2*P_av)), ("sigma x0.5", dict(sg=sig/2)), ("m_body x2", dict(mb=2*m)),
                 ("body 120 mm2 instead, eta x2", dict(eta=2*eta0))]:
    Sb = 120e-6 if "120" in name else 240e-6
    mg = cl_need(Sb=Sb, **kw)/1.10
    print(f"  {name:28s} margin {mg:.3f} -> {'STANDS' if mg>1 else 'FALLS'}")
print("  CL_best x2                  margin %.3f" % (cl_need(Sb=240e-6)/2.2))
r = short(1.10, 240e-6)[0]
print("run-up needed to close at CL1.10+240mm2: %.2f BL (%.1f cm)" % (2*r, 8*r))
print("single power-side factor that closes: %.3f; two inputs each by %.3f" % (r, sqrt(r)))

print("\nTransient (CL 1.98 + 240 mm2)")
c = Sw/0.08; d = 2*c
rt, Vt = short(1.98, 240e-6)
print("shortfall %.3f, V_parity %.3f m/s, 2 chords %.1f mm -> %.2f ms" % (rt, Vt, d*1e3, d/Vt*1e3))
Vmax = Vt*(1/rt)**(1/3)               # speed the available power actually reaches
exc = (Vmax/Vt)**2 - 1                # excess lift in units of weight at CL 1.98
t = d/Vmax; dv = exc*g*t
print("V reachable %.3f m/s; excess lift %.3f W; window %.2f ms; dv %.1f mm/s; apex %.4f mm" % (Vmax, exc, t*1e3, dv*1e3, dv*dv/2/g*1e3))
print("author's bound (1 g excess for %.2f ms): apex %.3f mm" % (d/Vt*1e3, (g*d/Vt)**2/2/g*1e3))
print("steady stay-up speed CL1.10+body: %.3f m/s" % short(1.10, 240e-6)[1])
