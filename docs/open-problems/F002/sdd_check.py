#!/usr/bin/env python3
"""F002 internal-consistency check of published zebrafish blastula transport measurements.

This is arithmetic on literature values, not a new measurement and not a model fit.
Inputs are the pinned values in assay-audit-v1.json (copied here as constants so the
script runs with the standard library only).

Checks
 1. Steady-state SDD decay length lambda = sqrt(D_eff / k1).
 2. How far from steady state the measured gradients are: k1 * t at t = 60 min
    (steady state needs k1 * t >> 1).
 3. Transient 1D surrogate: semi-infinite domain, source held at fixed concentration
    c0 at x = 0 from t = 0, uniform D and first-order clearance k1. Exact solution
      c/c0 = 0.5*[exp(-x/L) erfc((x - 2 sqrt(D k) t)/(2 sqrt(D t)))
                + exp(+x/L) erfc((x + 2 sqrt(D k) t)/(2 sqrt(D t)))],  L = sqrt(D/k).
    Report x50(t=60 min), the distance where c falls to 50 % of the source value,
    and compare with the reported 50 % distances (Pomreinke 2017, Fig. 3H+I).
    This is a crude surrogate for the authors' 3D embryo-geometry model, so it is
    a plausibility check only; the tolerance is set before looking (factor 1.5).
 4. Inverse: the D that the 1D surrogate needs to hit the reported x50 band,
    given the measured k1. Compared with FRAP D (held out from the gradient data).
"""
import math, json, sys

MIN = 60.0

def conc(x, t, D, k):
    L = math.sqrt(D / k)
    a = 2.0 * math.sqrt(D * t)
    v = 2.0 * math.sqrt(D * k) * t
    # use log-space for the exp(+x/L) term to avoid overflow
    t1 = math.exp(-x / L) * math.erfc((x - v) / a)
    t2 = math.exp(x / L) * math.erfc((x + v) / a) if x / L < 700 else 0.0
    return 0.5 * (t1 + t2)

def x50(t, D, k):
    lo, hi = 0.0, 5000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if conc(mid, t, D, k) > 0.5: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def D_for_x50(target, t, k):
    lo, hi = 1e-3, 1e3
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if x50(t, mid, k) < target: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

# Pinned literature values (see assay-audit-v1.json for quotes and locators)
POM = {  # Pomreinke et al. 2017 eLife 6:e25861, PMC5658070
  "BMP2b-Dendra2": dict(D=2.0, Dse=0.4, k=8.9e-5, kse=0.1e-5),
  "BMP2b-sfGFP":   dict(D=2.6, Dse=0.7, k=8.9e-5, kse=0.1e-5, note="k from Dendra2 fusion"),
  "BMP2b gradient-fit D (authors, 3D)": dict(D=4.0, Dse=None, k=8.9e-5, kse=0.1e-5),
  "Chordin-Dendra2": dict(D=6.0, Dse=0.7, k=9.6e-5, kse=0.3e-5),
  "Chordin-sfGFP":   dict(D=7.3, Dse=3.9, k=9.6e-5, kse=0.3e-5, note="k from Dendra2 fusion"),
  "Chordin gradient-fit D (authors, 3D)": dict(D=6.0, Dse=None, k=9.6e-5, kse=0.3e-5),
}
X50_REPORTED = {"BMP2b": (30.0, 40.0), "Chordin": (50.0, 60.0)}  # um at 60 min post-transplant
MUL = {  # Mueller et al. 2012 Science 336:721, PMC3525670 (D: FRAP GFP fusions; k1: FDAP Dendra2 fusions)
  "Cyclops": dict(D=0.7, Dse=0.2, k=1.22e-4, kse=0.13e-4),
  "Squint":  dict(D=3.2, Dse=0.5, k=1.00e-4, kse=0.06e-4),
  "Lefty1":  dict(D=11.1, Dse=0.6, k=0.53e-4, kse=0.05e-4),
  "Lefty2":  dict(D=18.9, Dse=3.0, k=0.69e-4, kse=0.07e-4),
}
TOL = 1.5  # pre-set multiplicative tolerance for the 1D surrogate vs reported x50

def lam_with_err(D, Dse, k, kse):
    lam = math.sqrt(D / k)
    if Dse is None: return lam, None
    rel = 0.5 * math.sqrt((Dse / D) ** 2 + (kse / k) ** 2)  # first-order propagation of SE
    return lam, lam * rel

out = {"schema": "f002-sdd-check/v1", "t_min": 60, "tolerance_factor": TOL, "rows": []}
print("Check 1-3: steady-state lambda, k*t at 60 min, 1D transient x50 at 60 min")
print(f"{'construct':40s} {'D um2/s':>8s} {'k 1/s':>9s} {'lambda um':>12s} {'k*t':>5s} {'x50_1D um':>9s}")
for src, table in (("Pomreinke2017", POM), ("Mueller2012", MUL)):
    for name, p in table.items():
        lam, se = lam_with_err(p["D"], p["Dse"], p["k"], p["kse"])
        kt = p["k"] * 60 * MIN
        xx = x50(60 * MIN, p["D"], p["k"])
        row = dict(source=src, construct=name, D_um2_s=p["D"], D_se=p["Dse"], k1_per_s=p["k"],
                   k1_se=p["kse"], lambda_ss_um=round(lam, 1), lambda_ss_se_um=None if se is None else round(se, 1),
                   k1_t_at_60min=round(kt, 3), x50_1D_60min_um=round(xx, 1))
        fam = "BMP2b" if name.startswith("BMP2b") else ("Chordin" if name.startswith("Chordin") else None)
        if fam:
            lo, hi = X50_REPORTED[fam]
            row["x50_reported_um"] = [lo, hi]
            row["within_tolerance"] = (lo / TOL) <= xx <= (hi * TOL)
        out["rows"].append(row)
        s = f"{lam:7.1f}" + (f"+/-{se:4.1f}" if se is not None else "      ")
        print(f"{src+':'+name:40s} {p['D']:8.1f} {p['k']:9.2e} {s:>12s} {kt:5.2f} {xx:9.1f}"
              + (f"  reported {X50_REPORTED[fam]} within x{TOL}: {row['within_tolerance']}" if fam else ""))

print("\nCheck 4: D the 1D surrogate needs to reach the reported x50 band (given measured k1)")
out["inverse"] = []
for fam, k, frap in (("BMP2b", 8.9e-5, "2.0-2.6"), ("Chordin", 9.6e-5, "6.0-7.3")):
    lo, hi = X50_REPORTED[fam]
    Dlo, Dhi = D_for_x50(lo, 60 * MIN, k), D_for_x50(hi, 60 * MIN, k)
    out["inverse"].append(dict(family=fam, x50_band_um=[lo, hi], D_required_um2_s=[round(Dlo, 2), round(Dhi, 2)], D_FRAP_um2_s=frap))
    print(f"{fam:8s} x50 {lo:.0f}-{hi:.0f} um needs D = {Dlo:.2f}-{Dhi:.2f} um2/s ; FRAP D = {frap} um2/s")

print("\nCheck 3b (geometry sensitivity, ASSUMED clone radius R): spherical source held at c0 on r = R,")
print("same kinetics; u = r*c obeys the 1D equation, so c/c0 = (R/r) * [1D solution at s = r - R].")
print("R is not reported in the text read (only '50-75 cells'); R values below are assumptions.")
print("A compact clone of 50-75 cells of 15-20 um diameter (unverified cell size) gives R ~ 28-42 um.")
print("The Dirichlet source is a surrogate: the real clone is a volumetric production source whose")
print("concentration rises over time, and sfGFP maturation and receptor saturation are ignored.")
def x50_sph(t, D, k, R):
    lo, hi = 0.0, 5000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (R / (R + mid)) * conc(mid, t, D, k) > 0.5: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)
out["sphere_sensitivity"] = []
for name, D, k in (("BMP2b-Dendra2", 2.0, 8.9e-5), ("BMP2b-sfGFP", 2.6, 8.9e-5), ("Chordin-Dendra2", 6.0, 9.6e-5), ("Chordin-sfGFP", 7.3, 9.6e-5)):
    fam = "BMP2b" if name.startswith("BMP2b") else "Chordin"
    vals = {R: round(x50_sph(60 * MIN, D, k, R), 1) for R in (25.0, 35.0, 50.0, 75.0)}
    lo, hi = X50_REPORTED[fam]
    ok = {R: (lo / TOL) <= v <= (hi * TOL) for R, v in vals.items()}
    out["sphere_sensitivity"].append(dict(construct=name, x50_um_by_R_um=vals, within_tolerance_by_R=ok, x50_reported_um=[lo, hi]))
    print(f"{name:16s} x50 at R=25/35/50/75 um: {vals[25.0]}/{vals[35.0]}/{vals[50.0]}/{vals[75.0]} um ; reported {lo:.0f}-{hi:.0f} ; within x{TOL}: {ok}")

print("\nRatio checks (published numbers only)")
r = dict(BMP2b_Dfree_over_Deff=46 / 2.0, Chordin_Dfree_over_Deff=59 / 6.0,
         BMP2b_gradfitD_over_FRAP_D_Dendra2=4.0 / 2.0, BMP2b_gradfitD_over_FRAP_D_sfGFP=4.0 / 2.6)
for k_, v in r.items(): print(f"{k_:40s} {v:6.2f}")
out["ratios"] = {k_: round(v, 3) for k_, v in r.items()}
if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], "w"), indent=1)
