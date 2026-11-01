# voxcraft-sim arm B receipt (2026-11-01, run 09:07-09:08 PDT / 16:07-16:08 UTC)

Arm B of `docs/handoff/xenobot-packet-to-infra.md`, run as specified and **unmodified**.

| field | value |
|---|---|
| image | `nvcr.io/nvidia/cuda:10.2-devel-ubuntu18.04`, amd64 manifest `sha256:8bd2ef1f01eb80f39123e7fafba51aa50d2f91081ee24fe645b65617b2255292` (list digest `sha256:5896fefb...`) |
| toolchain | nvcc 10.2.89, gcc 7.5.0, Boost 1.65.1 (Ubuntu 18.04 apt), CMake 3.18.6 (Kitware binary, sha256 `87136646...`) |
| source | voxcraft/voxcraft-sim `dd8668f99ff74fb2fc2ee60deb91287a3b519d8f`, codeload tarball 1,247,489 bytes, sha256 `0a0f4fd105a8df21df8b62a7d00e5178096d28415f2fb9f1679f6c78fd2c6546` (verified in-job, no edits) |
| configure | `cmake .. -DCUDA_ARCH=arch=compute_75,code=compute_75` (PTX only, driver must JIT forward) |
| acceptance | `./voxcraft-sim -i ../demos/basic/ -o output.xml -f > a.history`, exit 0 **and** non-empty output.xml and history (voxcraft-sim.cpp returns 0 even when the worker dies, so exit 0 alone is not accepted) |
| script | `scripts/voxgpu/armb_build_probe.sh` at commit b564513 |

| job | GPU / driver | build | demo | verdict |
|---|---|---|---|---|
| `claude-voxgpu-armb-h100-b1` aijob-e00tgzwnrv40rxmrdh | NVIDIA H100 80GB HBM3, 580.173.02 | rc 0 | rc 134 (worker rc 139, segfault after errors); output.xml absent; first error `VX3_SimulationManager.cu(283)` = the first `cudaMalloc`: "CUDA Function Error: unrecognized error code" | **RUN_FAIL** |
| `claude-voxgpu-armb-l40s-b1` aijob-e00kjbjq08t1bwkn4n | NVIDIA L40S, 580.173.02 | rc 0 (26.1 s) | rc 0, 14.09 s wall, history 10,780 B, output.xml 628 B with a `<detail>` record | **PASS** |

Return archives: H100 8,747 B sha256 `0214328d...4955`; L40S 11,916 B sha256 `01f39774...6d77` (decoded from job logs, hash matched the in-job receipt).

Reading: the pinned CUDA-10.2 toolchain builds the published engine unmodified; the PTX JITs and runs on Ada (sm_89). On Hopper (sm_90) the very first runtime call fails with an error the 10.2 runtime cannot name. Hypothesis (NOT yet established, diagnostic job `claude-voxgpu-h100-diag-d1` submitted): the driver refuses CDP1 code (device-side `cudaDeviceSynchronize`) for compute capability >= 9.0. Nothing here is a scientific result about organisms; it is a build/run receipt.
