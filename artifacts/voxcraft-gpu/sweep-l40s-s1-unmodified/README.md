# voxcraft-sim UNMODIFIED (dd8668f), L40S, sweep s1: PARTIAL (3 of 4 endpoint batches)
Job `claude-voxgpu-sweep-l40s-s1` aijob-e00ydw18ymxt8k271n, image cuda:10.2-devel-ubuntu18.04 @sha256:8bd2ef1f, PTX compute_75 JIT on
NVIDIA L40S driver 580.173.02. Inputs from `scripts/voxgpu/gen_sweep.py` seed 20261101 (commit b564513), evaluated with
`scripts/voxgpu/analyze.py` against `scripts/voxgpu/PREREGISTRATION.md` (committed before the job was submitted).
Batches returned (streamed per batch, sha256 verified): endpoints_dt0225 (1042.6 s), endpoints_dt045 (521.6 s), endpoints_dt090 (261.5 s); 33 bodies each, rc 0, 0 diverged.
Missing at time of writing: endpoints_mesh and the population batches (Nebius token expired, logs unreadable).

Scope: generic soft-voxel ground-contact mechanics, E=1e6 Pa, 10 mm voxels, contraction-only thermal actuation; NOT tissue-calibrated,
no fluid, not a Xenopus construct. A simulation, not an observation.
