# FORK lite1 on H100 (claude-voxgpu-fork-h100-lite1, aijob-e00bbpw90xyx73cf55): endpoints valid, population INVALID
Engine voxcraft-sim dd8668f + FORK-cdp-serial v2 (NOT the published engine). Lite config (E=1e5, self-collision off, T=4 s).
- endpoints_lite: 33 bodies, rc 0, 102.6 s, all reached t=4.0001 s -> valid fork output (for fork-vs-unmodified comparison).
- pop_00..03: 4 x 1000 bodies, "rc 0" in ~2 s each, but the kernel launch failed: `VX3_SimulationManager.cu(426): CUDA Function
  Error: too many resources requested for launch` (512 threads/block too many registers for the fork's inlined kernel). The worker
  nevertheless wrote a full report with currentTime = 0 for all 4000 bodies. **These reports are not data** and are not retained;
  analyze.py now rejects any body with t < 3.99 s. Fixed in fork v3 (threadsPerBlock 64), job claude-voxgpu-fork-h100-lite2.
Note for anyone using voxcraft-sim: process exit 0 and a non-empty report do NOT imply the simulation ran; check currentTime.
