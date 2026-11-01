# FORK: voxcraft-sim dd8668f with serial child work (NOT the published engine)

**Why it exists.** Arm B (unmodified, pinned CUDA 10.2, PTX JIT) runs on L40S but cannot run on H100:
the driver's JIT refuses device-side `cudaDeviceSynchronize` on sm_90+ (error 225,
`ptxas fatal: Unsupported Function 'cudaDeviceSynchronize' on arch 'sm_90' or higher`;
receipt `artifacts/voxcraft-gpu/h100-diag/job.log`). No toolchain choice fixes that; only a source change does.

**What it changes.** One file, `src/VX3/VX3_VoxelyzeKernel.cu`, transformed by `make_fork.py` (every
substitution asserted to hit the expected count). Each former child `__global__` kernel becomes a
`__device__` function taking its former global thread index explicitly; each child-grid launch becomes a
serial loop, in the calling per-simulation thread, over exactly the index range the kernel's guard
admitted; the 8 device-side `cudaDeviceSynchronize` calls after those launches are removed (the work is
already complete when the loop returns); the 8 `cudaOccupancyMaxPotentialBlockSize` calls that only sized
the removed grids are replaced by constants. Physics code (link forces, voxel integration, temperature,
collision/attachment handlers) is untouched. Full diff: `voxcraft-cdp-serial.diff` (306 lines, sha256 `763cd2f6...`).

**What it can change in results.** Work that ran as parallel threads now runs in index order. Where the
original had unsynchronised concurrent writes (e.g. `gpu_update_voxels` updates `k->gridLowerBound`, used
only in a dead branch; collision handlers write contact forces of both voxels of a pair), the original's
result could depend on thread scheduling and the fork's does not. So fork and original need not agree
bitwise. **How it is validated:** the same seeded sweep runs (a) unmodified on L40S, (b) fork on H100,
(c) fork on L40S. (a) vs (c) isolates the fork; (b) vs (c) isolates the GPU. Any result computed with the
fork is labelled `engine=voxcraft-sim-dd8668f+FORK-cdp-serial`.
