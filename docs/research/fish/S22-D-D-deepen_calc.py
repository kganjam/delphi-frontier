"""S22-D-D-D calculations. Every number printed is CALCULATED, not observed.

Inputs are carried over from S22-D-D (branch claude/s22-d-sensitive-input-pwechp,
docs/research/fish/S22-D-deepen.md). There they are figure-reads (D18 Fig 1A), a proxy
(kcnk5b alf/+ overgrowth) and search-summary values (flying-fish target). No new
measurement enters this script. See S22-D-D-deepen.md for sources and read-levels.

S22-D-D's conclusion is a shortfall: S = FF / (p0 * f)
  p0 = wild-type zebrafish pectoral/SL        (figure-read + inference, 0.208 central)
  f  = pectoral fold overgrowth, double mutant (proxy: alf/+ 1.74x pectoral, 2.05x caudal)
  FF = flying-fish pectoral/SL target          (search-summary, 0.65-0.77)
"""
P0, F_LO, F_HI, FF_LO, FF_HI = 0.208, 1.74, 2.05, 0.65, 0.77
WT_LINE = 0.104      # D18 Fig 1A wild-type dashed line, Growth/STL (figure-read)
SOF_LINE = 0.043     # D18 Fig 1A cx43 sof dashed line (figure-read)


def shortfall(p0, flo, fhi, fflo, ffhi):
    """Best-case and worst-case shortfall over the stated ranges."""
    return fflo / (p0 * fhi), ffhi / (p0 * flo)


def verdict(s):
    if s[1] <= 1:
        return "MATCH or overshoot: conclusion flips"
    if s[0] > 1:
        return "still short: conclusion holds"
    return "straddles 1: conclusion no longer determined"


base = shortfall(P0, F_LO, F_HI, FF_LO, FF_HI)
print(f"Baseline (S22-D-D): shortfall {base[0]:.2f}-{base[1]:.2f}x\n")

print("Factor-of-two test, one input at a time:")
cases = {
    "p0 x2": (2 * P0, F_LO, F_HI, FF_LO, FF_HI),
    "p0 /2": (P0 / 2, F_LO, F_HI, FF_LO, FF_HI),
    "f  x2": (P0, 2 * F_LO, 2 * F_HI, FF_LO, FF_HI),
    "f  /2": (P0, F_LO / 2, F_HI / 2, FF_LO, FF_HI),
    "FF x2": (P0, F_LO, F_HI, 2 * FF_LO, 2 * FF_HI),
    "FF /2": (P0, F_LO, F_HI, FF_LO / 2, FF_HI / 2),
}
for name, args in cases.items():
    s = shortfall(*args)
    print(f"  {name}: shortfall {s[0]:.2f}-{s[1]:.2f}x -> {verdict(s)}")

print("\nBreak-even values (shortfall = 1), holding the other two inputs at baseline:")
print(f"  p0 needed: {FF_LO / F_HI:.3f}-{FF_HI / F_LO:.3f} SL"
      f" (implies only {WT_LINE / (FF_HI / F_LO):.2f}-{WT_LINE / (FF_LO / F_HI):.2f} of the fin"
      " resected in D18 Fig 1A, against the legend's ~0.5)")
print(f"  f needed:  {FF_LO / P0:.2f}-{FF_HI / P0:.2f}x")
print(f"  FF needed (size-matched flying-fish target): <= {P0 * F_LO:.2f}-{P0 * F_HI:.2f} SL")

print("\nThe real quantity Rz = p0*f (double-mutant pectoral/SL), predicted from the proxy:")
print(f"  {P0 * F_LO:.2f}-{P0 * F_HI:.2f} SL. A direct read of Daane 2021 Fig 4B / preprint Fig 8B"
      " replaces p0 and f at once.")

print("\nCross-check of the D18 Fig 1A ratio method (independent of resection fraction):")
print(f"  sof/wt pectoral = {SOF_LINE / WT_LINE:.2f}; Iovine & Johnson 2000 abstract says sof fins are"
      " 'one-half the length of wild-type fins' (caudal; author's claim)")

print("\nlat4a nr21/+ shortening (author's claim: shortens all fins alone; magnitude unknown).")
print("If it shortens the pectoral by a factor s<1 in the double mutant, break-even f rises to:")
for s in (1.0, 0.9, 0.8):
    print(f"  s={s:.1f}: f needed {FF_LO / (P0 * s):.2f}-{FF_HI / (P0 * s):.2f}x (s values illustrative, not measured)")
