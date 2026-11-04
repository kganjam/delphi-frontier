"""Independent re-derivation for challenge 191 (RK4, own code; not the S28 script)."""
import math
g, rho = 9.81, 1.225
def run(V0, th, m=0.25e-3, S=192e-6, AR=5.0, CD0=0.08, CL_up=1.07, CL_dn=1.07, wing=True,
        Af=2.4e-5, CDb=0.3, e=0.8, dt=2e-5):
    k = 1/(math.pi*e*AR)
    def f(s):
        x, y, vx, vy = s
        V = math.hypot(vx, vy); q = 0.5*rho*V*V
        ux, uy = vx/V, vy/V
        D = q*Af*CDb; L = 0.0
        if wing:
            CL = CL_up if vy > 0 else CL_dn
            L = q*S*CL; D += q*S*(CD0 + k*CL*CL)
        # lift = L * (-uy, ux): rotated +90 deg from velocity
        return (vx, vy, (-D*ux - L*uy)/m, (-D*uy + L*ux)/m - g)
    s = (0.0, 0.0, V0*math.cos(th), V0*math.sin(th)); ymax = 0
    while True:
        k1 = f(s); k2 = f(tuple(a+dt/2*b for a, b in zip(s, k1)))
        k3 = f(tuple(a+dt/2*b for a, b in zip(s, k2))); k4 = f(tuple(a+dt*b for a, b in zip(s, k3)))
        n = tuple(a+dt/6*(b+2*c+2*d+e_) for a, b, c, d, e_ in zip(s, k1, k2, k3, k4))
        if n[1] < 0:
            fr = s[1]/(s[1]-n[1]); return s[0]+fr*(n[0]-s[0]), ymax
        s = n; ymax = max(ymax, s[1])
def best(V0, **kw):
    return max((run(V0, math.radians(t/2), **kw)[0], t/2) for t in range(70, 110))
print("vacuum V^2/g:", {V: round(100*V*V/g, 3) for V in (0.45, 1.38)}, "cm")
WT = {V: best(V, wing=False)[0] for V in (0.45, 1.38)}
print("WT with body drag (cm):", {V: round(100*r, 3) for V, r in WT.items()})
cases = [("C CD0=.08", dict(S=192e-6, AR=5.0, CD0=0.08)),
         ("C CD0=.20", dict(S=192e-6, AR=5.0, CD0=0.20)),
         ("B CD0=.12", dict(S=125e-6, AR=7.69, CD0=0.12)),
         ("A CD0=.12", dict(S=57e-6, AR=16.86, CD0=0.12)),
         ("C drag-free", dict(S=192e-6, AR=1e9, CD0=0.0))]
def rep(tag, V, **kw):
    r, th = best(V, **kw); print(f"  {tag:34s} V={V}: {100*r:.3f} cm  gain {100*(r/WT[V]-1):+.2f}%  ({1000*(r-WT[V]):+.2f} mm) th={th}")
print("1) Reproduce S28 table (fixed CL 1.07):")
for tag, kw in cases:
    for V in (1.38, 0.45): rep(tag, V, **kw)
print("2) Relax: fish feathers fin on ascent (CL=0 up, 1.07 down) -- lift on ascent points backward")
for tag, kw in cases[:4]: rep(tag+" CL0-up", 1.38, CL_up=0.0, **kw)
print("3) Relax: unsteady/LEV CL=2.0 throughout and on descent only (case C, CD0 .08)")
rep("C CL2 all", 1.38, S=192e-6, AR=5, CD0=0.08, CL_up=2.0, CL_dn=2.0)
rep("C CL0 up / CL2 down", 1.38, S=192e-6, AR=5, CD0=0.08, CL_up=0.0, CL_dn=2.0)
print("4) Relax: mass 0.40 g (case C, CD0 .08)")
WT40 = best(1.38, wing=False, m=0.4e-3)[0]
r, _ = best(1.38, m=0.4e-3, S=192e-6, AR=5, CD0=0.08); print(f"  0.40 g: gain {100*(r/WT40-1):+.2f}%")
print("5) Sign check of lift direction: horizontal lift component at 45 deg ascent / descent")
for vy in (+1, -1):
    ux, uy = 1/math.sqrt(2), vy/math.sqrt(2); print("   vy", vy, "lift x-component sign", math.copysign(1, -uy))
