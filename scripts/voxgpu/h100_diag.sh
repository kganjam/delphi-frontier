#!/bin/bash
# H100 arm-B failure discriminator. Same pinned image as arm B. No voxcraft source is modified or run here.
set -u; O=/out; mkdir -p $O; cd /out; exec > >(tee -a $O/diag.txt) 2>&1
NV=/usr/local/cuda/bin/nvcc; G=-gencode=arch=compute_75,code=compute_75
nvidia-smi --query-gpu=name,driver_version,compute_cap --format=csv
cp /job/cdp_probe.cu /job/jit_probe.cu .
$NV $G -o plain_ptx cdp_probe.cu && echo "== plain (no CDP), PTX-only compute_75" && ./plain_ptx; echo "rc=$?"
$NV $G -rdc=true -DWITH_CDP -o cdp_ptx cdp_probe.cu -lcudadevrt && echo "== CDP1 (device cudaDeviceSynchronize), PTX-only compute_75, rdc" && ./cdp_ptx; echo "rc=$?"
$NV -gencode=arch=compute_75,code=sm_75 -rdc=true -DWITH_CDP -o cdp_sass75 cdp_probe.cu -lcudadevrt && echo "== CDP1, SASS sm_75 only (expected: no kernel image for sm_90)" && ./cdp_sass75; echo "rc=$?"
$NV $G -rdc=true -DWITH_CDP -ptx -o cdp.ptx cdp_probe.cu; $NV -o jit_probe jit_probe.cu -lcuda && echo "== driver JIT link of CDP1 PTX + libcudadevrt.a" && ./jit_probe cdp.ptx /usr/local/cuda/lib64/libcudadevrt.a; echo "rc=$?"
echo "== cuobjdump -all of cdp_ptx"; /usr/local/cuda/bin/cuobjdump -all -lptx -lelf cdp_ptx
echo DIAG_DONE
