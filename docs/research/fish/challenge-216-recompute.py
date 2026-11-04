#!/usr/bin/env python3
"""Challenge 216 — independent recomputation for the adversarial review of claim 216.

Dependency-free.  Run with:  python3 -I docs/research/fish/challenge-216-recompute.py

Every number in challenge-216.md that is *computed* is produced here.  Nothing here is a
measurement.  Retrieved inputs are the AFDB summary band fractions and the S14-D model
parameters; all are named where they are used.  Exact rationals are used throughout so that
none of the agreement with the challenger is floating-point luck.
"""
from fractions import Fraction as F

SEP = "=" * 78

# ---------------------------------------------------------------- model, derived from scratch
# Two parallel ohmic branches, K and background B.  At rest the net current is zero:
#     I = g_K (Vm - E_K) + g_B (Vm - E_B) = 0
#  => Vm = (g_K E_K + g_B E_B) / (g_K + g_B)
#  => dividing through by g_B, with x = g_K/g_B:
E_K, E_B = F(-100), F(0)          # mV; E_K from Perathoner (oocyte), E_B assumed by S14-D


def Vm(x):
    """Resting potential, mV, as a function of the conductance ratio x = g_K/g_B."""
    return (x * E_K + E_B) / (x + 1)


def x_of(V):
    """Invert Vm(x)."""
    return (V - E_B) / (E_K - V)


print(SEP)
print("A. The window, and the setpoint count (challenge-216.md section 1)")
print(SEP)
V_WT, R = F(-40), F(2)
x0 = x_of(V_WT)
W = abs(Vm(x0 * R) - V_WT)
print(f"x0 = {x0} = {float(x0):.6f}")
print(f"Vm at R=2         = {Vm(x0*R)} = {float(Vm(x0*R)):.6f} mV")
print(f"W = |dVm|         = {W} = {float(W):.6f} mV        <- reproduces 17.1429")
print(f"W/sigma at 5 mV   = {W/5} = {float(W/5):.6f}       <- reproduces 3.4286")
print(f"W/sigma + 1       = {float(W/5)+1:.6f}             <- the challenger's 4.4286")
print()
print("  A count of distinguishable positions is an integer.  Spacing convention matters:")
print(f"  {'sigma_V':>8} {'W/sigma':>10} {'1-sigma: floor+1':>18} {'2-sigma (d=2): floor+1':>24}")
for s in (2, 5, 10, 15):
    iv = W / s
    print(f"  {s:>8} {float(iv):>10.4f} {int(iv)+1:>18} {int(iv/2)+1:>24}")
print("\n  At sigma_V = 5 mV: 4 setpoints at 1-sigma spacing, 2 at the conventional 2-sigma")
print("  criterion.  That 2-4 spread is wider than the 3.43 -> 4.43 fencepost correction.")

print()
print(SEP)
print("B. Vm_wt = -40 mV is the ARGMAX of the 2-fold window (section 6.3)")
print(SEP)
best = max(((F(-i, 10), abs(Vm(2 * x_of(F(-i, 10))) - F(-i, 10))) for i in range(1, 1000)),
           key=lambda t: t[1])
print(f"  max window over Vm_wt in [-99.9, -0.1] mV: {float(best[1]):.6f} mV "
      f"at Vm_wt = {float(best[0]):.1f} mV")
print("  So 17.143 mV is essentially the largest window the model can produce -- generous to")
print("  feasibility, i.e. conservative for a FALLS verdict.  A point in claim 91's favour.")
print("\n  The S14-D Vm_wt sweep, reproduced (all entries lie at or below the headline):")
for v in (-20, -30, -40, -50, -60):
    vv = F(v)
    d = abs(Vm(2 * x_of(vv)) - vv)
    swing = abs(E_K - vv)
    print(f"    Vm_wt={v:>4} mV  window={float(d):>7.3f} mV  = {float(d/swing)*100:>5.2f}% of swing")

print()
print(SEP)
print("C. The window is a SIMULATED proxy; the measurement disagrees (section 2)")
print(SEP)
print("  Retrieved, Perathoner et al. 2014 (PMC3894163, full-text): the mutant channels cause")
print("  'a shift in the membrane potential towards -90 to -100 mV'.  The divider at Vm_wt=-40")
print(f"  predicts an endpoint of {float(Vm(x0*R)):.1f} mV.  Inverting the model at R=2:")
print(f"  {'endpoint':>9} {'x_mut':>8} {'x_wt':>8} {'implied Vm_wt':>14} {'implied W':>11}")
for tgt in (-90, -95, -99):
    x2 = x_of(F(tgt)); xw = x2 / 2
    print(f"  {tgt:>9} {float(x2):>8.3f} {float(xw):>8.3f} {float(Vm(xw)):>14.2f} "
          f"{float(abs(F(tgt)-Vm(xw))):>11.2f}")
print("\n  The wild-type-injected oocyte Vm is in Figure 5D only and is could-not-access, so")
print("  the baseline is SWEPT here, not asserted:")
print(f"  {'baseline':>9} {'endpoint':>9} {'W (mV)':>8} {'setpoints @5mV, 1-sigma':>24}")
for wt in (-40, -50, -60, -70, -80):
    for mut in (-90, -100):
        w = abs(mut - wt)
        print(f"  {wt:>9} {mut:>9} {w:>8} {int(F(w,5))+1:>24}")
print("\n  => W is unpinned across roughly 8 to 60 mV before sigma_V is considered at all.")
print("  Mechanistic reason from the same paper not to trust the scalar divider: the mutants")
print("  show 'reduced outward rectification', an I-V SHAPE change a single ratio cannot carry.")

print()
print(SEP)
print("D. The pLDDT band arithmetic, and how little the global mean adds (section 3)")
print(SEP)
# Retrieved: AFDB AF-Q6PFU3-F1 v6 summary record (HTTP 200).
N, GLOBAL_MEAN = 448, F(695, 10)
f_vh, f_cf, f_lo, f_vl = F(353, 1000), F(248, 1000), F(60, 1000), F(339, 1000)
assert f_vh + f_cf + f_lo + f_vl == 1, "band fractions must sum to 1"
n_vh, n_cf, n_lo, n_vl = (f * N for f in (f_vh, f_cf, f_lo, f_vl))
n_rest = N - n_vl
total = GLOBAL_MEAN * N
bound = (total - 50 * n_vl) / n_rest          # very-low band is <50 by definition
print(f"  total pLDDT sum              = {float(total):,.0f}")
print(f"  n(very low) = 0.339*448      = {float(n_vl):.3f}")
print(f"  n(rest)                      = {float(n_rest):.3f}")
print(f"  lower bound on mean of rest  = {float(bound):.4f}   <- reproduces the 79.5 figure")
# What do the band DEFINITIONS alone force, with no use of the global mean?
band_min = (n_vh * 90 + n_cf * 70 + n_lo * 50) / n_rest
band_max = (n_vh * 100 + n_cf * 90 + n_lo * 70) / n_rest
print(f"\n  bands alone force mean of rest into [{float(band_min):.4f}, {float(band_max):.4f}]")
print(f"  information contributed by the global mean = {float(bound - band_min):.4f} pLDDT")
print("  => the 'hard lower bound' is a restatement of the band definitions, not a finding.")
g_min = (n_vh * 90 + n_cf * 70 + n_lo * 50 + n_vl * 0) / N
g_max = (n_vh * 100 + n_cf * 90 + n_lo * 70 + n_vl * 50) / N
print(f"\n  consistency check: global mean must lie in "
      f"[{float(g_min):.3f}, {float(g_max):.3f}]; observed {float(GLOBAL_MEAN)}  -> consistent")
print(f"\n  residues below 70  = {float(n_lo + n_vl):.1f} = {float((n_lo+n_vl)/N)*100:.1f}% of chain")
print(f"  residues that COULD be below 90 = {float(n_lo + n_vl + n_cf):.1f} = "
      f"{float((n_lo+n_cf+n_vl)/N)*100:.1f}%")
print("  => ten filter residues can sit anywhere in that mass.  A 296-residue mean speaks to")
print("     them no better than the 448-residue mean claim 91 was correctly faulted for using.")
print(f"\n  where the low-confidence mass could sit: C-terminus 251-448 = {448-250} residues "
      f"({(448-250)/448*100:.1f}%) vs very-low band {float(n_vl):.1f} ({float(f_vl)*100:.1f}%)")

print()
print(SEP)
print("E. Compressiveness, rerun independently (section 8)")
print(SEP)
x, prev = x0, V_WT
print(f"  start Vm = {float(prev):.2f} mV")
for k in range(5):
    x *= 2
    v = Vm(x)
    print(f"  doubling {k+1}: Vm = {float(v):>7.2f} mV   step = {float(v-prev):>7.2f} mV")
    prev = v
print("  Reproduces the challenger's sequence to the digit; the saturation is a real property")
print("  of the divider, not an artifact.")

print()
print(SEP)
print("Nothing above is a measurement.  Retrieved inputs: AFDB band fractions and global mean;")
print("E_K = -100 mV and the -90/-100 mV endpoint from Perathoner et al. (full-text).  E_B = 0,")
print("Vm_wt and sigma_V are S14-D assumptions.  Per-residue pLDDT: could-not-access (6 routes).")
print(SEP)
