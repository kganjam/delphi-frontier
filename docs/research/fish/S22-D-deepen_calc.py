"""S22-D-D calculations. Every number printed here is CALCULATED from the inputs below.
Inputs are figure-reads (pixel-calibrated or by eye) or search-summary values; none is a
new observation. See S22-D-deepen.md for sources and read-levels."""

# Daane et al. 2018 Sci Rep Fig 1A, pixel-calibrated read of the dashed lines (Growth/STL).
WT_LINE, ALF_LINE, SOF_LINE = 0.104, 0.181, 0.043
# Legend: fins "resected to ~50% of pre-cut fin length"; bracket the fraction removed.
RESECT = {"40%": 0.40, "50%": 0.50, "60%": 0.60}
# Perathoner et al. 2014 Fig 1E, eye-read (+/- ~0.02): standardised caudal length.
CAUDAL_WT, CAUDAL_ALF = 0.19, 0.39
# Flying-fish target pectoral/SL, E. volitans, three search-summary sources (disagree).
FF_LO, FF_HI = 0.65, 0.77

fold_pec = ALF_LINE / WT_LINE
fold_caud = CAUDAL_ALF / CAUDAL_WT
print(f"alf/+ pectoral overgrowth (ratio of regrowth targets): {fold_pec:.2f}x")
print(f"alf/+ caudal overgrowth (Perathoner 1E, eye-read):     {fold_caud:.2f}x")

print("\np0 (wild-type pectoral/SL) under each reading of Fig 1A:")
print(f"  literal legend (dashed = whole pre-cut fin): p0 = {WT_LINE:.3f}")
p0s = {k: WT_LINE / v for k, v in RESECT.items()}
for k, v in p0s.items():
    print(f"  dashed = removed part, {k} resected:       p0 = {v:.3f}")

print("\nRequired fold overgrowth FF/p0:")
for label, p0 in [("literal 0.104", WT_LINE)] + [(f"resect {k}", v) for k, v in p0s.items()]:
    print(f"  {label:14s} p0={p0:.3f}: {FF_LO/p0:.2f}x - {FF_HI/p0:.2f}x")

print("\nPredicted double-mutant pectoral/SL IF kcnh2a lof/+ overgrowth ~ alf/+ (proxy)")
print("and lat4a nr21/+ leaves the pectoral untouched (assumption; text says nr21/+ shortens all fins):")
for k, p0 in p0s.items():
    lo, hi = p0 * fold_pec, p0 * fold_caud
    print(f"  resect {k}: {lo:.2f} - {hi:.2f} SL; shortfall vs target: {FF_LO/hi:.2f}x - {FF_HI/lo:.2f}x")

print("\nFactor-of-two test on the decisive input (double-mutant pectoral/SL, central 0.21*1.74-2.05):")
c_lo, c_hi = p0s["50%"] * fold_pec, p0s["50%"] * fold_caud
print(f"  central {c_lo:.2f}-{c_hi:.2f}; x2 -> {2*c_lo:.2f}-{2*c_hi:.2f} (inside/above target 0.65-0.77);"
      f" /2 -> {c_lo/2:.2f}-{c_hi/2:.2f} (wild-type range)")
