"""Replicate-298: convert Fish (1990) whole-wing AR to a single-fin span^2/area. Every printed number is CALCULATED.

Fish 1990 (full text, Methods p.392):  AR_F = b^2 / S,  b = 2*l + w   (l = fin base->tip, w = body width at base)
                                       S = 2*A_pect + 2*A_pelv + body rectangles
Single-fin AR (S5-D protocol):         AR_1 = l^2 / A_pect
=> R = AR_F / AR_1 = 2 * P * (b/2l)^2,  with P = 2*A_pect/S  (Fish Table IV, read as fins-only share)
"""
TABLE_I = {  # Fish 1990 Table I r.m.a., M in kg, metres: (a, b)
    "Cypselurus": {"SL": (0.460, 0.355), "span": (0.651, 0.375), "area": (0.039, 0.642)},
    "Exocoetus":  {"SL": (0.462, 0.347), "span": (0.774, 0.380), "area": (0.046, 0.741)},
}
TABLE_III = {"Cypselurus": (12.717, 0.163), "Exocoetus": (23.410, 0.195)}  # AR = a M^b (Exocoetus r n.s.)
P = {"Cypselurus": 0.7599, "Exocoetus": 0.9183}                            # Table IV
PECT_SL = {"Cypselurus": (0.606, 0.714),   # 1.4-1.65 'in SL' -> 1/1.65..1/1.4 (search-summary, Plazi/Zootaxa)
           "Exocoetus": (0.732, 0.771)}    # 73.2-77.1 % SL (search-summary, FishBase/Fishes of Texas)
MASS = {"Cypselurus": (0.003, 0.01, 0.1, 0.3), "Exocoetus": (0.01, 0.03, 0.1)}  # ASSUMED evaluation masses

pw = lambda ab, M: ab[0] * M ** ab[1]
R = {}
for g in TABLE_I:
    lo, hi = 1e9, 0
    print(f"== {g}")
    for M in MASS[g]:
        bSL = pw(TABLE_I[g]["span"], M) / pw(TABLE_I[g]["SL"], M)
        for p in PECT_SL[g]:
            k = max(1.0, bSL / (2 * p))          # w >= 0 floor
            r = 2 * P[g] * k ** 2
            lo, hi = min(lo, r), max(hi, r)
            print(f"  M={M:<6} b/SL={bSL:.3f} l/SL={p:.3f} -> w/SL={bSL-2*p:+.3f} (b/2l)^2={k**2:.3f} R={r:.3f}")
    R[g] = (lo, hi)
    print(f"  R range {lo:.2f}-{hi:.2f}")

print("\n== Bar 1: Fish 1990 low end 3.0 (a Cypselurus; Table III Cypselurus range 3.0-12.2)")
lo, hi = R["Cypselurus"]; print(f"  A0 >= {3.0/hi:.2f} - {3.0/lo:.2f}")
allr = (min(R["Cypselurus"][0], R["Exocoetus"][0]), max(R["Cypselurus"][1], R["Exocoetus"][1]))
print(f"  (pooled R {allr[0]:.2f}-{allr[1]:.2f} -> A0 >= {3.0/allr[1]:.2f} - {3.0/allr[0]:.2f})")

print("\n== Bar 2: typical Fish-convention AR at M = 0.1 kg (assumed adult mass) -> single-fin")
for g in TABLE_I:
    t3 = pw(TABLE_III[g], 0.1)
    t1 = pw(TABLE_I[g]["span"], 0.1) ** 2 / pw(TABLE_I[g]["area"], 0.1)
    a, b = sorted((t1, t3)); lo, hi = R[g]
    print(f"  {g}: AR_F Table I {t1:.2f}, Table III {t3:.2f} -> single-fin {a/hi:.2f} - {b/lo:.2f}")
print("\n== Park & Choi 9.0 IF it is in Fish's convention (convention unknown, could-not-access)")
lo, hi = R["Cypselurus"]; print(f"  9.0 -> {9.0/hi:.2f} - {9.0/lo:.2f}; if already single-fin, stays 9.0")
