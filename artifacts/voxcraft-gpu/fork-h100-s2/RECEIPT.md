# FORK v2 on H100: claude-voxgpu-fork-h100-s2 (aijob-e00z25vcmc0w9yhcwd), CANCELLED by me 2026-11-01 ~09:36 PST
Engine: voxcraft-sim dd8668f + FORK-cdp-serial (fork/make_fork.py incl. cudaLimitStackSize 32 KiB). NOT the published engine.
Image/toolchain identical to arm B (cuda:10.2 @sha256:8bd2ef1f, PTX compute_75, JIT to sm_90). GPU: NVIDIA H100 80GB HBM3, driver 580.173.02.

Lines below were read from the live job log earlier in this session (the provider returned only the tail after the
cancel, and my fetch overwrote the earlier copy, so the full log is NOT retained; transcribed, not re-fetched):
- `DEMO rc=0 wall_s=5.45 history_bytes=10780 output_bytes=628` (stock demo PASSES on H100 with the fork;
  unmodified on L40S: rc 0, 14.09-14.19 s, same history size 10780 B)
- `WORKER_DIRECT rc=0`
- `VOXGPU_GEN generated 4132 bodies ... gen rc=0`
Retained verbatim (batches.txt, streamed part sha256 888cfe04... verified):
- `BATCH endpoints_dt0225 n_vxd=33 rc=124 wall_s=3600.0 report_bytes=0` -> the 33-body, 530k-step batch did NOT finish in the
  3600 s batch timeout; the unmodified engine on L40S finished the identical batch in 1042.6 s.

Result: the fork makes the engine run on Hopper (error 225 gone, demo passes) but executing the former child grids serially
in one thread per simulation is >3.4x slower than the unmodified engine on L40S for this workload (O(n^2) surface-pair
collision checks dominate). It is a functional port, not a throughput path. No physics result from the fork is reported.
