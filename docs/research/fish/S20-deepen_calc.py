"""S20-D arithmetic. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/S20-deepen_calc.py"""
from math import sqrt, sin, radians
g, rho_air = 9.81, 1.2
m = 4e-4            # kg, S20 assumption (4 cm adult)
eta = 0.10          # S20 assumed overall launch efficiency
E_smr = (15.0, 37.0)  # J/day, S20 C2 readings B and A
CL = 1.0

def ke(v): return 0.5*m*v*v
def rng(v): return v*v/g                     # 45 deg, no drag, launch at surface
def apex45(v): return (v*sin(radians(45)))**2/(2*g)
def tair(v): return 2*v*sin(radians(45))/g
def S_glide(v): return 2*m*g/(rho_air*CL*v*v)
def frac(v, e=eta, E=E_smr): return tuple(ke(v)/e/x for x in E)

print("== 1. Sensitivity of S20's two conclusions to x0.5 / x2 on each input ==")
v1m = sqrt(g*1.0)
base = frac(v1m)
print(f"baseline 1 m launch: v={v1m:.2f} m/s, cost/SMR = {base[0]:.2e}..{base[1]:.2e}")
for name, f in [("efficiency", lambda k: frac(v1m, e=eta*k)),
                ("SMR", lambda k: frac(v1m, E=tuple(x*k for x in E_smr))),
                ("mass(cost only)", lambda k: tuple(k*x for x in base)),
                ("range d", lambda k: frac(sqrt(g*1.0*k)))]:
    for k in (0.5, 2):
        lo, hi = f(k); print(f"  {name:16s} x{k}: cost/SMR {hi:.2e}..{lo:.2e}")
print("  -> worst case 2.6e-3 of daily SMR per launch: 'almost free' never flips at x2.")
for v in (3.13, 1.565, 0.84, 0.42, 1.68):
    print(f"  exit speed {v:5.3f} m/s: range {rng(v)*100:6.1f} cm, apex {apex45(v)*100:5.2f} cm, "
          f"aloft {tair(v):.3f} s, glide area (CL=1) {S_glide(v)*1e4:6.1f} cm^2")
print("  -> x2 on exit speed = x4 on reach and on required glide area.")

print("\n== 2. Improved input: adult peak escape speed ==")
Re, se, L, nu = 27800, 2140, 0.0330, 1.0e-6
for lab, R in (("mean", Re), ("-1sem", Re-se), ("+1sem", Re+se)):
    U = R*nu/L; print(f"  {lab}: U = {U:.3f} m/s ({U/L:.1f} TL/s)")
cands = [("Ucrit Palstra 2010 (lower bound)", 0.548),
         ("burst, inverted from Danos&Lauder Re", 0.842),
         ("min v for M8 0.10 m land jump", sqrt(g*0.10)),
         ("guppy-class 3.5 BL vertical jump, L=33 mm", sqrt(2*g*3.5*0.033)),
         ("S20 1 m launch", sqrt(g*1.0))]
for lab, v in cands:
    c = ke(v)/eta
    print(f"  {lab:42s} v={v:.3f}  range {rng(v)*100:5.1f} cm  apex45 {apex45(v)*100:4.2f} cm "
          f" vert.apex {v*v/2/g*100:4.1f} cm  cost {c:.2e} J = {c/E_smr[1]:.1e}..{c/E_smr[0]:.1e} SMR "
          f" 1m-deficit x{sqrt(g)/v:.2f} speed, x{g/v/v:.1f} KE")
