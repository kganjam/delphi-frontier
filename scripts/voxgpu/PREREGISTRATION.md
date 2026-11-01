# voxcraft-sim endpoint sweep: preregistered evaluation (frozen before any sweep output exists)
Written 2026-11-01 PDT by claude-voxgpu, committed before the sweep job is submitted. Thresholds below are
not to be changed after data; any later analysis is labelled POST-HOC.

Displacement d = COM(t=6 s) - COM(t=1 s) in the xy (floor) plane, metres, from the voxcraft report
(`currentCenterOfMass - initialCenterOfMass`, initial re-zeroed at t=1 s by
`ReinitializeInitialPositionAfterThisManySeconds`). Body: solid 8x4x3 block at 10 mm (80x40x30 mm envelope),
refinements: DtFrac 0.9 (base) / 0.45 / 0.225 at 10 mm; 16x8x6 at 5 mm with DtFrac 0.9 (mesh).
"Equal total actuation" = every voxel active, same commanded amplitude, only the phase field differs.

E1 passive-control: pattern `passive_cte0` (same block, CTE=0). PASS iff |d| < 1e-5 m (10 um = 0.1% of a
   voxel) in EVERY refinement batch and every replicate. Failure -> no other endpoint may be read as
   a pattern-to-motion statement until diagnosed (reported regardless).
E2 pattern-dependence: primary pair (wave_px, sync). Delta = |d_wave - d_sync| at base. R = max over the
   three refinements (dt045, dt0225, mesh) and both patterns of |d_P(refined) - d_P(base)|. PASS iff Delta > R.
   Secondary pairs reported the same way: (wave_px, checker), (split_px, sync).
E3 mirror-symmetry: pairs with their mirror operator: (wave_px, wave_mx; x->-x), (split_px, split_mx; x->-x),
   (wave_py, wave_my; y->-y), (diag_pxpy, diag_pxmy; y->-y). e = |d_mirror - M d_original|.
   PASS iff e < max(1e-5 m, 0.01 |d_original|) for every pair at base; reported at every refinement.
D  determinism: spread across the 3 identical replicates, reported per pattern (no threshold).
Population (1000 random bodies x {act, pas, mir, rep}): reported as distributions, no pass/fail:
   fraction of passive controls with |d| >= 1e-5 m; mirror error e vs duplicate error |d_rep - d_act|;
   relative mirror error only where |d_act| > 10x the 95th percentile passive |d|; divergence count.
Scope: generic soft-voxel ground-contact mechanics, not tissue-calibrated, no fluid, contraction only.

## Addendum A (2026-11-01 ~09:45 PST, written BEFORE any cilia run exists): cilia arm
Same 8x4x3 block at 10 mm, gravity + floor + friction, but material "ciliated" (CTE 0, Cilia 1) and VXA EnableCilia=1:
each surface voxel gets a constant body-frame force vector f (voxcraft BaseCiliaForce), |f| = F identical for every voxel
in every pattern (equal total commanded cilia force). Patterns: cilia_off (F=0), cilia_px, cilia_mx, cilia_py, cilia_my,
cilia_dpp (+x+y)/sqrt2, cilia_dpm (+x-y)/sqrt2, cilia_swirl (tangential about the vertical axis, zero net force),
cilia_rand (seeded random xy directions) and cilia_randmy (its y-mirror). F in {0.005, 0.01, 0.02} N per voxel
(84 surface voxels; body weight 0.94 N, mu_s = 1). DtFrac 0.9 and 0.45. 3 replicates of each.
C1 passive: cilia_off |d| < 1e-5 m in every run.
C2 pattern-dependence (at F = 0.02): |d_px - d_swirl| > max over dt change of |d_P(0.45) - d_P(0.9)| for P in {px, swirl}.
C3 mirror (at every F, DtFrac 0.9): pairs (px,mx; x), (py,my; y), (dpp,dpm; y), (rand,randmy; y):
   e < max(1e-5 m, 0.01 |d|).
Descriptive (no threshold): displacement vs F (a Coulomb threshold is expected but not quantitatively predicted).
Interpretation rule fixed in advance: if C3 passes under cilia while E3 failed under contraction, that is consistent with
(not proof of) the stick-slip amplification explanation of E3; if C3 also fails, the asymmetry is not specific to
contraction-driven stick-slip.
