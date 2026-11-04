"""S28-D-D: recompute S28-D with the pectoral fin length READ from Daane et al. 2021 Fig 8B (preprint)
= Fig 4B (Curr Biol), and test the next input (spread-fin area rule).
Model and constants are copied unchanged from S28-D (docs/research/fish/S28-deepen_calc.py @ 511ecf7b).
All outputs are CALCULATIONS on stated inputs, not observations. Run: python3 -I S28-D-D_calc.py"""
import math
g = 9.81; rho = 1.225; CL = 1.07; CD0 = 0.08; CDb = 0.3

def fly(V, th, S, span, m, Af, wing=True, dt=2e-6, ascent_only=False):
    th = math.radians(th); AR = span**2 / S; k = 1 / (math.pi * 0.8 * AR)
    vx, vy = V * math.cos(th), V * math.sin(th); x = y = t = 0.0; ymax = 0
    while True:
        U = math.hypot(vx, vy); q = 0.5 * rho * U * U; ux, uy = vx / U, vy / U
        D = q * Af * CDb; L = 0.0
        if wing:
            L = q * S * CL; D += q * S * (CD0 + k * CL**2)
        ax = (-D * ux - L * uy) / m; ay = (-D * uy + L * ux) / m - g
        vx += ax * dt; vy += ay * dt; x += vx * dt; y += vy * dt; t += dt; ymax = max(ymax, y)
        if ascent_only and vy <= 0: return dict(t_up=t, apex=y)
        if y < 0: return dict(R=x, apex=ymax)

SL0, m0 = 0.030, 0.25e-3     # S28 assumed body (back-solved)
def geom(frac, rule, SL=SL0, kspread=1.0):
    """per-fin length frac*SL. rule C: AR 5 at span=2L+bw (S28 headline). rule A: 0.7*L*0.1SL per fin.
    rule F: folded-outline shape factor 0.134*L^2 per fin (Fig 8A read) times an UNMEASURED spread factor."""
    Lf = frac * SL; bw = 0.004 * SL / 0.030; span = 2 * Lf + bw
    if rule == 'C': S = span**2 / 5
    elif rule == 'A': S = 2 * 0.7 * Lf * 0.1 * SL
    elif rule == 'F': S = 2 * 0.134 * Lf**2 * kspread
    return span, S

def phen(frac, V, rule, kspread=1.0, SL=SL0, m=m0, th=45):
    Af = 2.4e-5 * (SL / 0.030)**2
    span, S = geom(frac, rule, SL, kspread)
    wt = fly(V, th, S, span, m, Af, False, ascent_only=True)
    mu = fly(V, th, S, span, m, Af, True, ascent_only=True)
    red = 1 - wt['t_up'] / mu['t_up']
    R0 = fly(V, th, S, span, m, Af, False, dt=1e-5)['R']; R1 = fly(V, th, S, span, m, Af, True, dt=1e-5)['R']
    Vto = math.sqrt(2 * m * g / (rho * S * CL))
    LW = 0.5 * rho * V**2 * S * CL / (m * g)
    return dict(S=S * 1e6, AR=span**2 / S, red=red, dapex=(mu['apex'] - wt['apex']) * 1e3,
                gain=R1 / R0 - 1, Vto=Vto, LW=LW)

FRACS = [("Q1 0.449", 0.449), ("median 0.463", 0.463), ("Q3 0.488", 0.488),
         ("min dot 0.434", 0.434), ("max dot 0.534", 0.534), ("S28 assumed 0.45", 0.45)]
SPEEDS = [0.95, 1.38, 1.57, 2.11]

print("== 1. S28-D's phenotype recomputed at the FIGURE-READ fin length (45 deg, SL 3.0 cm, 0.25 g) ==")
for rule in ('C', 'A'):
    print(f"-- rule {rule}")
    for name, fr in FRACS:
        cells = []
        for V in SPEEDS:
            r = phen(fr, V, rule)
            cells.append(f"{V:.2f}: {100*r['red']:4.2f}%")
        r = phen(fr, 1.38, rule)
        print(f"  L/SL {name:16s} S {r['S']:5.0f} mm2 AR {r['AR']:5.1f} Vto {r['Vto']:4.2f} | " + " | ".join(cells))

print("\n== 2. Sensitivity of the recomputed phenotype (median L, 1.38 m/s) to each remaining input ==")
base = phen(0.463, 1.38, 'C'); print(f"  baseline rule C: red {100*base['red']:.2f}%  range gain {100*base['gain']:.2f}%  flight deficit x{base['Vto']/1.38:.2f}")
for lab, kw in [("fin length IQR 0.449", dict(frac=0.449)), ("fin length IQR 0.488", dict(frac=0.488)),
                ("V x0.5", dict(V=0.69)), ("V x2", dict(V=2.76)),
                ("mass x0.5", dict(m=m0 * 0.5)), ("mass x2", dict(m=m0 * 2)),
                ("area rule A (length-only)", dict(rule='A')),
                ("area rule F, folded outline, spread x1", dict(rule='F', kspread=1.0)),
                ("area rule F, spread x2", dict(rule='F', kspread=2.0)),
                ("SL 3.6 cm, m 0.43 g (isometric)", dict(SL=0.036, m=m0 * (3.6 / 3.0)**3))]:
    a = dict(frac=0.463, V=1.38, rule='C'); a.update(kw)
    r = phen(**a)
    print(f"  {lab:40s} S {r['S']:5.0f} mm2  L/W exit {100*r['LW']:5.1f}%  red {100*r['red']:5.2f}%  "
          f"range gain {100*r['gain']:5.2f}%  Vto {r['Vto']:.2f} (x{r['Vto']/a['V']:.2f})")

print("\n== 3. Spread factor k (spread planform / folded lateral outline) needed to reach rule-C area, and the 2% / 5% thresholds ==")
SC = phen(0.463, 1.38, 'C')['S']; SF = phen(0.463, 1.38, 'F', 1.0)['S']
print(f"  rule C area {SC:.0f} mm2; folded outline {SF:.0f} mm2; k for rule C = {SC/SF:.2f}")
for V in (1.38, 1.57):
    for target in (0.02, 0.05):
        lo, hi = 0.3, 12.0
        for _ in range(28):
            mid = (lo + hi) / 2
            if phen(0.463, V, 'F', mid)['red'] < target: lo = mid
            else: hi = mid
        print(f"  V {V:.2f} m/s: {100*target:.0f}% reduction needs spread factor k = {(lo+hi)/2:.2f} (S = {SF*(lo+hi)/2:.0f} mm2)")
for k in (1.0, 1.5, 2.0, 3.0, 3.9):
    r1 = phen(0.463, 1.38, 'F', k); r2 = phen(0.463, 1.57, 'F', k)
    print(f"  k {k:.1f}: S {r1['S']:5.0f} mm2 AR {r1['AR']:5.1f}  red {100*r1['red']:.2f}% @1.38, {100*r2['red']:.2f}% @1.57;"
          f" apex +{r1['dapex']:.2f} mm @1.38; Vto {r1['Vto']:.2f} m/s")

print("\n== 4. Negative clause at the measured length: flight speed and best case ==")
for rule, k in (('C', 1), ('A', 1), ('F', 1)):
    for name, fr in (("median", 0.463), ("max dot", 0.534)):
        r = phen(fr, 2.11, rule, k)
        print(f"  rule {rule} {name} {fr}: Vto {r['Vto']:.2f} m/s; deficit vs 1.57 x{r['Vto']/1.57:.2f}, vs 2.11 x{r['Vto']/2.11:.2f}; range gain @2.11 {100*r['gain']:.2f}%")

print("\n== 5. Area from the partly abducted fin (Fig 8A dorsal panel): A/L^2 = 0.150-0.250 per fin (figure-read) ==")
print("   rule C requires A/L^2 per fin =", round(geom(0.463, 'C')[1] / 2 / (0.463 * SL0)**2, 3),
      "; rule A gives", round(geom(0.463, 'A')[1] / 2 / (0.463 * SL0)**2, 3), "; folded outline 0.134")
for shape in (0.150, 0.188, 0.216, 0.250):
    k = shape / 0.134
    r1 = phen(0.463, 1.38, 'F', k); r2 = phen(0.463, 1.57, 'F', k); r3 = phen(0.463, 2.11, 'F', k)
    print(f"  A/L^2 {shape:.3f} (k {k:.2f}): S {r1['S']:4.0f} mm2 AR {r1['AR']:4.1f} | red {100*r1['red']:.2f}% @1.38,"
          f" {100*r2['red']:.2f}% @1.57, {100*r3['red']:.2f}% @2.11 | range gain {100*r1['gain']:.2f}% @1.38 | Vto {r1['Vto']:.2f}")
