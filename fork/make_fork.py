#!/usr/bin/env python3
"""FORK of voxcraft-sim dd8668f (NOT the published engine): replace every device-side child-kernel launch
(+ device-side cudaDeviceSynchronize, CDP1) in src/VX3/VX3_VoxelyzeKernel.cu with a serial loop executed by
the calling (per-simulation) thread. Reason: CUDA >=12 / sm_90 rejects device-side cudaDeviceSynchronize
(driver JIT: "Unsupported Function 'cudaDeviceSynchronize' on arch 'sm_90' or higher", error 225).
Each former __global__ child kernel becomes a __device__ function taking its former global thread index as
an explicit first argument; launch sites iterate that index over exactly the range the guard admitted.
Usage: make_fork.py <path to VX3_VoxelyzeKernel.cu>  (edits in place; asserts every substitution hits once)."""
import re, sys
p = sys.argv[1]; s = open(p).read(); n0 = len(s)

def once(old, new, count=1):
    global s
    c = s.count(old)
    assert c == count, (c, old[:80])
    s = s.replace(old, new)

K1 = ["gpu_update_links", "gpu_update_voxels", "gpu_update_temperature", "gpu_update_cilia_force",
      "gpu_clear_lookupgrid", "gpu_insert_lookupgrid", "gpu_collision_attachment_lookupgrid", "gpu_update_detach"]
# 1) forward declarations and definitions: __global__ void K(  ->  __device__ void K(int vx3_i,
for k in K1 + ["gpu_update_attach", "gpu_pairwise_detection"]:
    two = k in ("gpu_update_attach", "gpu_pairwise_detection")
    extra = "int vx3_i, int vx3_j, " if two else "int vx3_i, "
    c = s.count("__global__ void %s(" % k)
    assert c in (1, 2), (k, c)
    s = s.replace("__global__ void %s(" % k, "__device__ void %s(%s" % (k, extra))
# 2) inside the bodies, the builtin-derived index lines become the explicit index
for var in ("gindex", "index"):
    s = s.replace("int %s = threadIdx.x + blockIdx.x * blockDim.x;" % var, "int %s = vx3_i;" % var)
once("int first = threadIdx.x + blockIdx.x * blockDim.x;", "int first = vx3_i;")
once("int second = threadIdx.y + blockIdx.y * blockDim.y;", "int second = vx3_j;")
once("int index_x = threadIdx.x + blockIdx.x * blockDim.x;", "int index_x = vx3_i;")
once("int index_y = threadIdx.y + blockIdx.y * blockDim.y;", "int index_y = vx3_j;")
assert "threadIdx" not in s and "blockIdx" not in s, "leftover builtin index"
# 3) occupancy queries reference the (now non-kernel) symbols: drop them (they only sized the child grids)
s, nocc = re.subn(r"\n[ \t]*cudaOccupancyMaxPotentialBlockSize\([^;]*;[^\n]*", "\n        minGridSize = 0; blockSize = 256; /* FORK: occupancy query removed (no child launch); values only sized the unused grid */", s)
assert nocc == 8, nocc
# 4) launch sites: K<<<grid, block>>>(args)  ->  serial loop over the guarded range
def loop1(m):
    k, args = m.group(1), m.group(3)
    first = args.split(",")
    # range = the 'num' argument of each kernel
    rng = {"gpu_update_links": "d_v_links.size()", "gpu_update_voxels": "num_d_voxels", "gpu_update_temperature": "num_d_voxels",
           "gpu_update_cilia_force": "num_d_surface_voxels", "gpu_clear_lookupgrid": "num_lookupGrids",
           "gpu_insert_lookupgrid": "num_d_surface_voxels", "gpu_collision_attachment_lookupgrid": "num_lookupGrids",
           "gpu_update_detach": "d_v_links.size()"}[k]
    return "for (int vx3_i = 0; vx3_i < (int)(%s); vx3_i++) %s(vx3_i, %s); /* FORK: was a child-grid launch of %s (grid %s) */" % (rng, k, args, k, m.group(2).replace(",", " x"))
s, nl = re.subn(r"\b(%s)<<<([^>]*)>>>\(([^;]*)\);" % "|".join(K1), loop1, s)
assert nl == 8, nl
once("gpu_update_attach<<<dimGrid, dimBlock>>>(d_surface_voxels, num_d_surface_voxels, watchDistance,\n",
     "for (int vx3_i = 0; vx3_i < num_d_surface_voxels; vx3_i++) for (int vx3_j = 0; vx3_j < vx3_i; vx3_j++) /* FORK: was a 2D child-grid launch (dimGrid, dimBlock) */\n        gpu_update_attach(vx3_i, vx3_j, d_surface_voxels, num_d_surface_voxels, watchDistance,\n")
s, npw = re.subn(r"gpu_pairwise_detection<<<dimGrid, dimBlock>>>\(\s*([^;]*?)num_voxel_in_grid,\s*(num_voxel_in_grid(?:_2)?), watchDistance, k\);",
                 lambda m: "for (int vx3_i = 0; vx3_i < num_voxel_in_grid; vx3_i++) for (int vx3_j = 0; vx3_j < %s; vx3_j++) /* FORK */ gpu_pairwise_detection(vx3_i, vx3_j, %snum_voxel_in_grid, %s, watchDistance, k);" % (m.group(2), m.group(1), m.group(2)), s)
assert npw == 2, npw
# 5) device-side syncs after the (now synchronous) loops: remove
nsync = s.count("VcudaDeviceSynchronize();")
s = s.replace("VcudaDeviceSynchronize();", "/* FORK: device-side cudaDeviceSynchronize removed (work above is synchronous) */")
assert "<<<" not in s.replace('printf("<<<', ""), "leftover launch"
open(p, "w").write(s)
print("forked", p, "bytes", n0, "->", len(s), "launch sites", nl + 1 + npw, "syncs removed", nsync, "occupancy removed", nocc)
