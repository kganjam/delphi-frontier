"""Challenge 140 arithmetic. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/challenge-140_calc.py"""
from math import sqrt
g = 9.81
need1, need05 = sqrt(g * 1.0), sqrt(g * 0.5)          # drag-free 45 deg range R = v^2/g
air_mean, air_sd = 1.2357, 0.300                      # Soares & Bierman 2013 Table 1 (measured, guppy)
tail = air_mean + 2 * air_sd
cg_lo, cg_mid, cg_hi = 0.70, 0.75, 0.80               # S&B guppy C-start, author 'extrapolated'
print(f"v needed: 1 m {need1:.3f} m/s; 0.5 m {need05:.3f} m/s")

print("\n1. Independent recompute with Danio burst = Danos & Lauder Re inversion 0.842 (0.78-0.91)")
for lab, vj in (("air mean", air_mean), ("air mean+2sd", tail)):
    lo, mid, hi = 0.78 * vj / cg_hi, 0.842 * vj / cg_mid, 0.91 * vj / cg_lo
    print(f"  {lab:13s} {lo:.3f} / {mid:.3f} / {hi:.3f} m/s; 1 m deficit x{need1/hi:.2f}-x{need1/lo:.2f};"
          f" mid deficit x{need1/mid:.2f}")

print("\n2. Flip threshold on the Danio C-start input (tail statistic)")
for lab, cg in (("mid ratio", cg_mid), ("generous ratio (guppy burst 0.70)", cg_lo), ("strict ratio (0.80)", cg_hi)):
    print(f"  {lab:34s}: 1 m flips if Danio burst >= {need1*cg/tail:.3f} m/s;"
          f" 0.5 m flips if >= {need05*cg/tail:.3f}; typical (mean) reaches 1 m if >= {need1*cg/air_mean:.3f}")

print("\n3. Same ratio route with directly measured adult Danio burst speeds")
for lab, vb in (("Demesmay 2025 control mean 1.57", 1.57), ("Demesmay mean-1sd 1.30", 1.30),
                ("Demesmay mutant mean 1.61", 1.61), ("Miln 2021 fastest fish 1.38 (digitised, ch.75)", 1.38),
                ("Miln 2021 centre ~0.80 (visual, ch.75)", 0.80)):
    t_mid, t_lo, t_hi = vb * tail / cg_mid, vb * tail / cg_hi, vb * tail / cg_lo
    m_mid = vb * air_mean / cg_mid
    print(f"  {lab:46s} typical {m_mid:.2f}; tail {t_lo:.2f}/{t_mid:.2f}/{t_hi:.2f} m/s;"
          f" tail-mid vs 3.13: x{need1/t_mid:.2f}{'  FLIPS' if t_mid >= need1 else ''}")

print("\n4. Floor comparison, like-for-like")
print(f"  S20-D-D point 1.82 -> x{need1/1.82:.2f}; claim tail mid 2.06 -> x{need1/2.061:.2f}; claim corner 2.39 -> x{need1/2.386:.2f}")
print(f"  Chang route with SAME air-mean statistic: {air_mean*(0.033/0.0185)**(1/3):.3f} m/s (claim compares 1.39 vs 1.37 built from 1.13)")

print("\n5. Normal tail beyond 2 sd, D&L burst mid ratio")
for k in (2, 3, 4):
    v = air_mean + k * air_sd
    print(f"  mean+{k}sd guppy {v:.2f}: Danio mid {0.842*v/cg_mid:.2f}, corner {0.91*v/cg_lo:.2f}")
print(f"  guppy jump needed for mid route to hit 3.13: {need1*cg_mid/0.842:.2f} m/s = mean+{(need1*cg_mid/0.842-air_mean)/air_sd:.1f} sd")
