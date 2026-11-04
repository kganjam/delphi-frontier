"""S20-D-D-D arithmetic. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/S20-D-D-deepen_calc.py"""
from math import sqrt

g = 9.81
m, eta, E_smr = 4e-4, 0.10, (15.0, 37.0)  # S20 assumptions (kg, -, J/day)
L_dr = 0.033                              # Danos & Lauder 2012 mean TL (m)
v_need = sqrt(g * 1.0)                    # exit speed for a 1 m range at 45 deg, drag-free


def rng(v): return v * v / g              # 45 deg range, drag-free
def apex(v): return v * v / (2 * g)       # vertical apex
def cost(v): return 0.5 * m * v * v / eta  # J per launch


def line(lab, v):
    print(f"  {lab:46s} v={v:.2f} m/s  range45 {rng(v)*100:5.1f} cm ({rng(v)/L_dr:4.1f} TL)"
          f"  apex {apex(v)*100:5.1f} cm  1m-deficit x{v_need/v:.2f}  KE x{(v_need/v)**2:.1f}")


print("== 1. Sensitivity of S20-D-D's conclusions: x0.5 / x1 / x2 on each speed input ==")
Lg = 0.0185
chang = (L_dr / Lg) ** (1 / 3)
inputs = {
    "D&L Re inversion (0.842)": 0.842,
    "guppy mean, Chang-scaled (S20-D-D central)": 1.13 * chang,
    "guppy fastest air, Chang-scaled (S20-D-D floor)": 1.50 * chang,
}
for lab, v0 in inputs.items():
    for k in (0.5, 1, 2):
        print(f"  {lab:48s} x{k:<3}: v={v0*k:.2f}  1m-deficit x{v_need/(v0*k):.2f}"
              f"  {'FLIPS' if v0*k >= v_need else ''}")
print("  Chang exponent b in H/L ~ L^b; v ~ L^((1+b)/2):")
for b in (-0.47, -0.35, -1 / 3, -0.23, 0.0):
    s = (L_dr / Lg) ** ((1 + b) / 2)
    print(f"    b={b:+.2f}: scale x{s:.3f}  central {1.13*s:.2f}  extreme {1.50*s:.2f}")
print("  Required range R (S20 framing): v_need = sqrt(gR)")
for R in (1.0, 0.5, 0.25):
    print(f"    R={R:.2f} m -> v_need {sqrt(g*R):.2f} m/s")

print("\n== 2. Demesmay et al. 2025 adult D. rerio escape (author values, PLoS Biol e3003484) ==")
v_c, sd_c = 1.57, 0.27     # controls, max speed, mean +/- SD
v_m, sd_m = 1.61, 0.33     # scn4aa/scn4ab double mutants (not different, author claim)
d40 = 0.038                # distance in first 40 ms, controls
print(f"  mean speed over first 40 ms = {d40/0.040:.2f} m/s (noise-robust lower bound on the peak)")
print(f"  peak in TL/s at TL 2.6 / 3.3 / 3.6 cm: {v_c/0.026:.0f} / {v_c/0.033:.0f} / {v_c/0.036:.0f}")
print(f"  ratio to D&L Re inversion: x{v_c/0.842:.2f}")
print(f"  SDs above control mean needed to reach {v_need:.2f}: {(v_need-v_c)/sd_c:.1f}")
boost = 1.24 / 1.02        # guppy air/water peak ratio (Soares & Bierman 2013), applied as an INFERENCE
print(f"  with guppy-style in-air boost x{boost:.2f}: SDs needed {(v_need/boost-v_c)/sd_c:.1f}")
print("  Frame-noise sensitivity of a manually tracked peak at 240 fps (per-axis sigma_v = sqrt2*e*fps):")
for e_mm in (0.25, 0.5, 1.0):
    print(f"    click error {e_mm} mm -> per-axis velocity noise {sqrt(2)*e_mm*1e-3*240:.2f} m/s")

print("\n== 3. Lines of evidence for adult Danio exit speed, kept separate ==")
for lab, v in [("D&L Re inversion (S20-D)", 0.842),
               ("Demesmay 40-ms mean speed (lower bound)", d40 / 0.040),
               ("S20-D-D guppy central, Chang-scaled", 1.13 * chang),
               ("Demesmay control peak, mean", v_c),
               ("Demesmay mutant peak, mean", v_m),
               ("S20-D-D guppy extreme, Chang-scaled", 1.50 * chang),
               ("Demesmay control peak, +1 SD", v_c + sd_c),
               ("Demesmay peak x guppy air boost (inference)", v_c * boost),
               ("Demesmay control peak, +2 SD", v_c + 2 * sd_c),
               ("Demesmay +2 SD x air boost (inference)", (v_c + 2 * sd_c) * boost),
               ("S20 1 m launch", v_need)]:
    line(lab, v)

print("\n== 4. Downstream checks at v = 1.57 m/s ==")
v = v_c
print(f"  launch cost {cost(v):.2e} J = {cost(v)/E_smr[1]:.1e}..{cost(v)/E_smr[0]:.1e} of daily SMR")
S = 2 * m * g / (1.2 * 1.0 * v * v)
print(f"  glide area at C_L=1: {S*1e4:.1f} cm^2 (vs ~3 cm^2 planform: x{S*1e4/3:.0f})")
