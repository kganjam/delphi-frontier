"""S14-D-D: recomputation of the S14-D conclusion with a digitized sigma_V.

Every number printed here is a CALCULATION, not an observation. Two inputs come
from outside this file and are named at the point of use:

  (a) sigma_V values, from digitizing Perathoner et al. 2014 PLoS Genet Fig 5D
      (per-oocyte Vm scatter, calibrated mV axis). That digitization is a COMPUTED
      EXTRACTION from a published figure image -- not an author-reported table.
      It is reproduced by S14-D-D-digitize.py, committed beside this file.
  (b) the parallel-conductance model and R = 2.0, inherited unchanged from S14-D
      (docs/research/fish/S14-recompute.py) so that the two are comparable.

Run: python3 -I docs/research/fish/S14-D-D-recompute.py
"""
import math, statistics as st

EK, EB = -100.0, 0.0          # EK from Perathoner et al. 2014 text; EB = 0 is an ASSUMPTION
R      = 2.0                  # measured macroscopic fold-change, Perathoner et al. 2014
vm     = lambda r: (r*EK + EB)/(r + 1.0)
r_of   = lambda v: (v - EB)/(EK - v)

# --- digitized Perathoner Fig 5D, per-oocyte Vm in mV (see S14-D-D-digitize.py) -------
WT      = [-5.5, -27.0, -17.7, -37.0, -41.0]
W169L   = [-18.0, -12.1, -31.0, -46.0, -68.0, -81.0]
F241Y   = [-20.0, -32.0, -12.1, -24.0, -45.0, -30.0, -36.0, -55.0, -61.0]
SIGMA = {
    "S14-D assumed (no source)":            5.0,
    "digitized wild-type within-group SD": st.stdev(WT),
    "digitized all-genotype pooled SD":    st.stdev(WT + W169L + F241Y),
    "digitized residual SD at fixed I50":   7.8,   # pooled OLS residual, from the digitizer
}

print("CALCULATION, not an observation.\n")
print("A. Vm window a 2-fold gK increase buys, at the measured wild-type resting potential")
vwt_meas = st.mean(WT)
for v0, tag in ((-40.0, "S14-D's worked example"), (vwt_meas, "digitized wild-type mean")):
    w = abs(vm(r_of(v0)*R) - v0)
    print(f"   Vm_wt = {v0:6.1f} mV ({tag:24s}) -> window {w:5.1f} mV")

print("\nB. Distinguishable setpoints = window / sigma_V, at Vm_wt = -40 mV (window 17.1 mV)")
W40 = abs(vm(r_of(-40.0)*R) - (-40.0))
for name, s in SIGMA.items():
    print(f"   sigma_V = {s:5.1f} mV  ({name:35s}) -> {W40/s:5.2f} levels")

print("\nC. Same, at the digitized wild-type mean resting potential")
Wm = abs(vm(r_of(vwt_meas)*R) - vwt_meas)
for name, s in SIGMA.items():
    print(f"   sigma_V = {s:5.1f} mV  ({name:35s}) -> {Wm/s:5.2f} levels")

print("\nD. Factor-of-two test on the IMPROVED input (sigma_V = 14.5 mV, window 17.1 mV)")
base = st.stdev(WT)
for f in (0.25, 0.5, 1.0, 2.0, 4.0):
    s = base*f
    print(f"   sigma_V = {s:5.1f} mV  ({f:4.2f}x the digitized value) -> {W40/s:5.2f} levels")

print("\nE. Discriminability on the digitized Vm itself (Cohen's d, wild type vs each allele)")
def d(x, y):
    sp = math.sqrt(((len(x)-1)*st.stdev(x)**2 + (len(y)-1)*st.stdev(y)**2)/(len(x)+len(y)-2))
    return abs(st.mean(y)-st.mean(x))/sp, sp
for nm, v in (("W169L", W169L), ("F241Y", F241Y)):
    dd, sp = d(WT, v)
    print(f"   wt vs {nm}: d = {dd:4.2f} (pooled SD {sp:4.1f} mV) -> {dd:4.2f} setpoints at 1-SD spacing")

print("\nF. For comparison: discriminability measured on the OUTPUT variable by the authors")
print("   (Cohen's d computed by S14-D-D-authordata.py from Jiang et al. 2024 S1-S7 Data)")
for lab, dd in (("fin bud/eye area, GFP -> kcnk5b, 32 hpf", 2.60),
                ("fin bud/eye area, GFP -> kcnk5b, 48 hpf", 1.94),
                ("fin bud/eye area, GFP -> kcnk5b, 56 hpf", 2.56),
                ("fin bud/eye area, AB vs GFP (null control, 48 hpf)", 0.17),
                ("DiBAC2(3) Vm proxy, mCherry -> kcnk5b-Tg (Fig 5K)", 2.45),
                ("DiBAC2(3) Vm proxy, mCherry -> kcnk5b   (Fig 5L)", 1.35)):
    print(f"   {lab:52s} d = {dd:4.2f}")
