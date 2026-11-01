# voxcraft-sim UNMODIFIED (dd8668f), L40S, sweep s1: endpoint set COMPLETE (population pending)
Job `claude-voxgpu-sweep-l40s-s1` aijob-e00ydw18ymxt8k271n, image cuda:10.2-devel-ubuntu18.04 @sha256:8bd2ef1f, PTX compute_75 JIT on
NVIDIA L40S driver 580.173.02. Inputs from `scripts/voxgpu/gen_sweep.py` seed 20261101 (commit b564513), evaluated with
`scripts/voxgpu/analyze.py` against `scripts/voxgpu/PREREGISTRATION.md` (committed before the job was submitted).
Batches returned (streamed per batch, sha256 verified): endpoints_dt0225 (1042.6 s), endpoints_dt045 (521.6 s), endpoints_dt090 (261.5 s); 33 bodies each, rc 0, 0 diverged.
endpoints_mesh (16x8x6 @ 5 mm) 1068.3 s, rc 0, 0 diverged. Population batches pending.

## Preregistered verdicts (analyze.py -> endpoints.json)
| endpoint | verdict | numbers |
|---|---|---|
| E1 passive-control | PASS | max abs d = 2.5e-9 m over 12 runs (4 refinements x 3 reps), tol 1e-5 m |
| E2 pattern-dependence (wave_px vs sync) | PASS | Delta 45.01 mm > R 6.40 mm (largest refinement change = mesh, wave 45.03 -> 51.44 mm, 14%) |
| E2 secondary wave_px vs checker / split_px vs sync | PASS / PASS | 45.04 > 6.40 mm / 14.83 > 2.33 mm |
| E3 mirror-symmetry (base) | **FAIL** | wave x-mirror 0.95% (ok); split x-mirror 1.48%; wave y-mirror 15.1%; diag y-mirror 1.39% (bound 1%) |

Not a convergence claim: the 14% mesh change of the wave and the 4.3x mesh change of the short-axis wave (5.2 -> 22.5 mm) show
the 10 mm lattice is not converged for these patterns. Replicates are bitwise identical (spread 0) in every case.

Scope: generic soft-voxel ground-contact mechanics, E=1e6 Pa, 10 mm voxels, contraction-only thermal actuation; NOT tissue-calibrated,
no fluid, not a Xenopus construct. A simulation, not an observation.
