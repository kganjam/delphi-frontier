# Fork validation: FORK on H100 == UNMODIFIED on L40S, bitwise, 33/33 bodies (lite config)
- unmodified: voxcraft-sim dd8668f, job claude-voxgpu-unmod-l40s-lite1 (aijob-e00btpzyyxrgps71kz), NVIDIA L40S, 48.05 s
- fork v3: dd8668f + FORK-cdp-serial (fork/make_fork.py: serial child loops, stack 32 KiB, 64 threads/block), job
  claude-voxgpu-fork-h100-lite2 (aijob-e00ex2xwetgsg9vfw1), NVIDIA H100 80GB HBM3, 102.46 s
- Same image (cuda:10.2 @sha256:8bd2ef1f), same PTX compute_75, same generator inputs (`gen_sweep.py --lite`, 11 patterns x 3 reps).
- Result: max |d_fork - d_unmodified| = 0.0 m over all 33 bodies (every reported COM coordinate identical).
Scope of the validation: lite config only (E=1e5, self-collision OFF, so the collision/attachment child grids never run). The fork's
equivalence with collision ON is NOT established here. Any fork number is still labelled voxcraft-sim-dd8668f+FORK-cdp-serial.
