"""S9-D-D sensitivity and recomputation. EVERY output of this script is a CALCULATION, not an observation.

It re-uses S9-D's beam models (docs/research/fish/S9-deepen_calc.py on branch
origin/claude/deepen-s9-fin-ray-ixdx5u) unchanged, and swaps in one improved input.

Inputs and read-levels:
  EI_fin   1.5e-9 .. 4e-9 N m^2   whole caudal fin, in vivo      Puri et al. 2018 JEB, PMC5868929, full-text
  N_rays   16 .. 18                                               Puri et al. 2018, full-text
  D_ray    100 .. 200 um           ray diameter                   Puri et al. 2018, full-text
  t_dorsal ~11 .. ~16.5 um         WT DORSAL hemiray thickness    hox13 PLoS Genet 2026, PMC12956070 Fig 7E (S9-D's
                                                                  plot reading); micro-CT voxel 7.1 um (methods, full-text)
  t_caudal ~20.4 (+-4.9) proximal  WT CAUDAL hemiray bone         Azevedo et al. 2011 PLoS One 6:e22820, PMC3145768,
           ~19.0 (+-2.7) distal    thickness, uncut controls      Fig 4L/4M, confocal on 12 um cryosections. Values are
                                                                  MY pixel readings of the bar chart (+-~0.5 um);
                                                                  the error-bar type (SD or SEM) is not stated.
  E_bone   ~23 .. 25 GPa           zebrafish VERTEBRA nanoindent. S9 B3/B4, search-summary only
"""
from math import pi

EI_FIN = (1.5e-9, 4e-9)
N = (16, 18)
EI_RAY = (EI_FIN[0] / N[1], EI_FIN[1] / N[0])
E_BONE_LO = 23e9


def I_flat_pair(w, t):
    return 2 * w * t**3 / 12


def I_solid_rod(D):
    return pi * D**4 / 64


def E_flat(ei, w, t):
    return ei / I_flat_pair(w, t)


print(f"per-ray EI (calc) = {EI_RAY[0]:.2e} .. {EI_RAY[1]:.2e} N m^2\n")

# ---------------------------------------------------------------------------
# 1. Sensitivity of S9-D's two numerical conclusions to each input (x0.5, x2)
#    C1: uncoupled flat-plate upper-bound E envelope (S9-D: ~0.6-11 GPa)
#    C2: the flat-plate bound sits BELOW vertebral tissue E (>=23 GPa), i.e.
#        in-vivo EI cannot be reproduced with tissue E -> extra compliance / E not transferable
# ---------------------------------------------------------------------------
base = dict(EI_hi=EI_RAY[1], w=100e-6, t=11e-6, E_bone=E_BONE_LO)  # S9-D's most-generous corner


def c1_max(p):
    return E_flat(p["EI_hi"], p["w"], p["t"])


b = c1_max(base)
print(f"S9-D baseline, most generous corner (EI/ray={base['EI_hi']:.2e}, w=100um, t=11um): "
      f"E_max = {b/1e9:.1f} GPa; margin below 23 GPa = {E_BONE_LO/b:.2f}x")
print("input          x0.5 -> E_max (GPa)  C2 holds?     x2 -> E_max (GPa)  C2 holds?")
for k in ("EI_hi", "w", "t", "E_bone"):
    out = []
    for f in (0.5, 2.0):
        p = dict(base)
        p[k] = base[k] * f
        e = c1_max(p)
        out.append((e, e < p["E_bone"]))
    print(f"  {k:8s}  {out[0][0]/1e9:8.1f}            {str(out[0][1]):5s}       "
          f"{out[1][0]/1e9:8.1f}            {str(out[1][1]):5s}")
print("  (N enters only through EI/ray, so it is covered by EI_hi; D enters as w)\n")

# ---------------------------------------------------------------------------
# 2. Recompute with the caudal-fin thickness
# ---------------------------------------------------------------------------
cases = {
    "S9-D t (dorsal, micro-CT)": (11e-6, 16.5e-6),
    "caudal means (Azevedo)": (19.0e-6, 20.4e-6),
    "caudal mean +- bar": (19.0e-6 - 2.7e-6, 20.4e-6 + 4.9e-6),
}
for name, (tlo, thi) in cases.items():
    lo = min(E_flat(EI_RAY[0], w, thi) for w in (100e-6, 150e-6, 200e-6))
    hi = max(E_flat(EI_RAY[1], w, tlo) for w in (100e-6, 150e-6, 200e-6))
    mid = (E_flat(EI_RAY[0], 150e-6, thi), E_flat(EI_RAY[1], 150e-6, tlo))
    print(f"{name:28s} t={tlo*1e6:4.1f}-{thi*1e6:4.1f} um  flat-plate E envelope "
          f"(D=100-200) = {lo/1e9:5.2f} .. {hi/1e9:5.2f} GPa ; at D=150: "
          f"{mid[0]/1e9:5.2f} .. {mid[1]/1e9:5.2f} GPa ; margin below 23 GPa >= {E_BONE_LO/hi:4.1f}x")

# ratio of E implied by dorsal vs caudal t (E ~ t^-3)
for td, tc in ((11e-6, 19.0e-6), (16.5e-6, 20.4e-6), (15e-6, 19.7e-6)):
    print(f"E(t={td*1e6:.1f}) / E(t={tc*1e6:.1f}) = {(tc/td)**3:.2f}")

# t at which flat plates would need >= 23 GPa (upper EI, w = 100 um = most generous)
t_crit = (12 * EI_RAY[1] / (2 * 100e-6 * E_BONE_LO)) ** (1 / 3)
print(f"\nflat plates need E >= 23 GPa only if t < {t_crit*1e6:.1f} um (w=100um, upper EI)")

# forward check: tissue E (23 GPa) x caudal t, flat plates, 17 rays -> predicted whole-fin EI
for t in (16.3e-6, 19.7e-6, 25.3e-6):
    for w in (100e-6, 200e-6):
        print(f"  forward (calc): E=23 GPa, t={t*1e6:.1f} um, w={w*1e6:.0f} um, 17 rays -> "
              f"EI_fin = {23e9*I_flat_pair(w, t)*17:.2e} N m^2 "
              f"(measured 1.5e-9..4e-9; ratio {23e9*I_flat_pair(w, t)*17/4e-9:.0f}-"
              f"{23e9*I_flat_pair(w, t)*17/1.5e-9:.0f}x)")

# internal-consistency check on Azevedo geometry (my readings of Fig 4N-Q, uncut):
# fin thickness ~= 2 t + intra-ray space
for lab, t, intra, fin in (("proximal", 20.4, 85, 125), ("distal", 19.0, 63, 104)):
    print(f"Azevedo {lab}: 2t + intra-ray = {2*t+intra:.0f} um vs fin thickness read {fin} um")
