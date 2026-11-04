"""S20-D-D arithmetic. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/S20-D-deepen_calc.py"""
from math import sqrt
g = 9.81
m, eta, E_smr = 4e-4, 0.10, (15.0, 37.0)   # S20 assumptions (kg, -, J/day)
L_dr = 0.033                               # Danos & Lauder 2012 mean TL (m)
v_need = sqrt(g * 1.0)                     # exit speed for 1 m range at 45 deg
def rng(v): return v * v / g               # 45 deg, drag-free
def vert(v): return v * v / (2 * g)        # vertical apex
def cost(v): return 0.5 * m * v * v / eta

print("== 1. Sensitivity of S20-D's conclusions to x0.5 / x2 on each input ==")
base = {"burst v (D&L inversion)": 0.842, "guppy-class comparator (S20-D)": 1.51}
for lab, v0 in base.items():
    for k in (0.5, 1, 2):
        v = v0 * k
        print(f"  {lab:32s} x{k:<3}: v={v:.2f} m/s range {rng(v)*100:5.1f} cm "
              f"({rng(v)/L_dr:4.1f} TL) 1m-deficit x{v_need/v:.2f}")
print("  Re x2 / L x0.5 / nu x2 each -> v x2 (U = Re*nu/L, linear).")
print(f"  Factor on burst v needed to reach 1 m: x{v_need/0.842:.2f}")
print(f"  Factor on guppy-class v needed to reach 1 m: x{v_need/1.51:.2f}")
print(f"  Cost per 1 m launch / SMR stays {cost(v_need)/E_smr[1]:.1e}..{cost(v_need)/E_smr[0]:.1e}")

print("\n== 2. S20-D's guppy-class number, rebuilt from Soares & Bierman 2013 ==")
L_g, H_g, H_bl = 0.0185, 0.0654, 3.52       # SL (m), jump height (m), BL
print(f"  check: H/SL = {H_g/L_g:.2f} (paper: {H_bl})")
print(f"  S20-D route: 3.5 BL x 33 mm = {3.5*L_dr*100:.1f} cm -> v = {sqrt(2*g*3.5*L_dr):.2f} m/s")
v_g = sqrt(2 * g * H_g)
print(f"  ballistic v implied by guppy mean height: {v_g:.2f} m/s "
      f"(measured: 1.02 in water, 1.24 in air)")
for Lz, tag in ((0.033, "TL 33 mm"), (0.027, "assumed SL 27 mm")):
    s = (Lz / L_g) ** (1 / 3)               # Chang 2019: H/L ~ L^-1/3 -> v ~ L^1/3
    print(f"  Chang scaling to {tag}: H/L {H_bl/s:.2f}, H {H_bl/s*Lz*100:.1f} cm, "
          f"v {v_g*s:.2f} m/s")
cands = [("Ucrit Palstra 2010", 0.548),
         ("burst, D&L inversion", 0.842),
         ("guppy measured, in water (mean)", 1.02),
         ("guppy ballistic from mean H", v_g),
         ("guppy measured, in air (mean)", 1.24),
         ("guppy mean H, Chang-scaled to 33 mm", v_g * (0.033 / L_g) ** (1/3)),
         ("S20-D guppy-class (superseded)", 1.51),
         ("guppy fastest single, air (Fig 2)", 1.50),
         ("guppy fastest air, Chang-scaled 33 mm", 1.50 * (0.033 / L_g) ** (1/3)),
         ("S20 1 m launch", v_need)]
print("\n== 3. Lines of evidence, kept separate ==")
for lab, v in cands:
    print(f"  {lab:40s} v={v:.2f}  range45 {rng(v)*100:5.1f} cm ({rng(v)/L_dr:4.1f} TL)  "
          f"vert {vert(v)*100:5.1f} cm  1m-deficit x{v_need/v:.2f}  KE x{(v_need/v)**2:.1f}  "
          f"cost/SMR {cost(v)/E_smr[1]:.1e}..{cost(v)/E_smr[0]:.1e}")
print(f"\n  guppy exit speed in SL/s: {1.02/L_g:.0f}; Danio burst inversion in TL/s: {0.842/L_dr:.1f}")
