# Cilia arm (PREREGISTRATION.md Addendum A), UNMODIFIED voxcraft-sim dd8668f on L40S
Job `claude-voxgpu-ens-cilia-l40s-e2` aijob-e00arkvn9b6qh733mk; batches cilia_dt045 (84 bodies, 1177.4 s) and cilia_dt090 (84 bodies, 582.2 s), rc 0, 0 diverged.
voxcraft's own cilia model (EnableCilia=1, per-voxel BaseCiliaForce, constant body-frame thrust on surface voxels) on the same
8x4x3 block on a frictional floor. Evaluated by `scripts/voxgpu/analyze_cilia.py` -> cilia_endpoints.json.

| endpoint | verdict | numbers |
|---|---|---|
| C1 passive (F=0) | PASS | max abs d 2.5e-9 m, 6 runs |
| C2 pattern-dependence (F=0.02 N: +x vs swirl) | PASS | 762.9 mm vs dt change 0.0035 mm |
| C3 mirror (all F, DtFrac 0.9) | **FAIL** | 23/24 pairs pass (most < 1e-5 relative); F=0.01 N +y vs -y: +y stuck at 11.71 mm, -y slid 71.14 mm (at DtFrac 0.45 both 71.14 mm) |

Displacement vs per-voxel force (DtFrac 0.9, +x): 0.005 N -> 0; 0.010 N -> 71.2 mm; 0.020 N -> 762.9 mm in 5 s. Swirl and
random-direction fields (net force ~0) do not translate. Replicate spread <= 1.1e-16 m.
Reading, per the rule fixed in advance: C3 also fails, so the mirror asymmetry is NOT specific to contraction-driven stick-slip.
The single failure sits at the stick/slip threshold (F=0.005 N diagonal also slides 3.2 mm at DtFrac 0.9 but 0 at 0.45), i.e.
near the Coulomb threshold the outcome is dt-sensitive and mirror-sensitive; away from it the solver is mirror-symmetric to ~2e-5.
Scope: frictional sliding under a prescribed thrust; no fluid, so this is NOT ciliary swimming; force magnitudes are arbitrary.
