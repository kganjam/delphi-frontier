#!/usr/bin/env python3
"""Assemble the voxcraft-sim build probe receipt from all attempts.

A build failure on ONE toolkit is not a verdict on the engine. This file keeps
every attempt and its exact blocker so a reader can see which failures are the
project's and which were ours.
"""
import json, os, re
ROOT = "/data/scratch/designspaces/xenobot"


def scan(path):
    if not os.path.exists(path):
        return None
    t = open(path, errors="replace").read()
    return {
        "cuda": (re.search(r"Cuda compilation tools, release [0-9.]+, V[0-9.]+", t) or [None])
                if False else (re.search(r"Cuda compilation tools, release [0-9.]+, V[0-9.]+", t).group(0)
                               if re.search(r"Cuda compilation tools, release [0-9.]+, V[0-9.]+", t) else None),
        "cmake_lines": re.findall(r"cmake version [0-9.]+", t),
        "boost": (re.search(r'BOOST_LIB_VERSION "([0-9_]+)"', t).group(1)
                  if re.search(r'BOOST_LIB_VERSION "([0-9_]+)"', t) else None),
        "gcc": (re.search(r"gcc \(Ubuntu [^)]*\) [0-9.]+", t).group(0)
                if re.search(r"gcc \(Ubuntu [^)]*\) [0-9.]+", t) else None),
        "pin_ok": "PIN-OK" in t,
        "cmake_rcs": re.findall(r"cmake rc=(\d+)", t),
        "make_exits": re.findall(r"MAKE-EXIT=(\d+)", t),
        "verdict_line": (re.search(r"PROBE-VERDICT=\S+", t).group(0)
                         if re.search(r"PROBE-VERDICT=\S+", t) else None),
        "cmake_min_error": "CMake Error at CMakeLists.txt:1 (cmake_minimum_required)" in t,
        "cuda_sync_sites": sorted(set(re.findall(r"VX3_VoxelyzeKernel\.cu\((\d+)\)", t)), key=int),
        "boost_asio_error": "static_query.hpp:85" in t,
        "built": "BUILD OK" in t}


attempts = [
    {"attempt": 1, "job_id": "aijob-e00n37n2d6cn00af86",
     "image": "nvidia/cuda:12.4.1-devel-ubuntu22.04",
     "rationale": "modern toolkit, forcing the target arch rather than autodetecting",
     "log": "logs/voxcraft-probe-full.log"},
    {"attempt": 2, "job_id": "aijob-e00p5x2y3fd2veyhsh",
     "image": "nvcr.io/nvidia/cuda:10.2-devel-ubuntu18.04",
     "rationale": "the image voxcraft-sim's own Dockerfile pins, so the Boost and GCC the code was written against",
     "log": "logs/voxcraft-pinned.log"},
    {"attempt": 3, "job_id": "aijob-e00bn8ykdhsqdnrrvq",
     "image": "nvcr.io/nvidia/cuda:10.2-devel-ubuntu18.04 + Kitware CMake 3.22.1",
     "rationale": "attempt 2 could not configure because Ubuntu 18.04 ships CMake 3.10.2 and CMakeLists requires >= 3.12; this supplies a new enough CMake on the pinned toolchain",
     "log": "logs/voxcraft-pinned-cmake.log"},
]
for a in attempts:
    a["observed"] = scan(os.path.join(ROOT, a["log"]))

built = [a for a in attempts if a["observed"] and a["observed"]["built"]]
D = {
    "schema": "design-space-probe/0.2", "id": "voxcraft-sim-build-probe",
    "why_it_matters": ("voxcraft-sim is the GPU engine the computationally designed organism literature actually "
                       "uses; Kriegman et al. 2021 describe their simulator as 'a version of a voxel-based "
                       "soft-body simulator modified to run on highly parallelized (GPU-based) computing "
                       "platforms'. Building it would have been the strongest available check on everything else here."),
    "target": {"repo": "https://github.com/voxcraft/voxcraft-sim",
               "pin": "dd8668f99ff74fb2fc2ee60deb91287a3b519d8f",
               "pin_verified": "git rev-parse HEAD matched; PIN-OK printed in every attempt",
               "licence_of_record": "CC0-1.0, read from the LICENSE file bytes at that commit: 'Creative Commons Legal Code / CC0 1.0 Universal'",
               "licence_conflict": ("the project website cdorgs.github.io/code states the code is under "
                                    "Attribution-NonCommercial Creative Commons; the repository's own LICENSE "
                                    "file says CC0-1.0. Both are quoted; the conflict is NOT resolved in our "
                                    "favour, and a lawyer should look at it before anything from those "
                                    "repositories is redistributed. It does not block this page: we redistribute "
                                    "nothing, linking upstream and committing only our own driver and recipe.")},
    "platform": "Nebius AI job, gpu-l40s-a, 1gpu-8vcpu-32gb, NVIDIA L40S",
    "attempts": attempts,
    "any_attempt_built": bool(built),
    "blockers_by_attempt": {
        "1_modern_toolkit": {
            "blocker_a_cuda": {
                "what": "voxcraft-sim calls cudaDeviceSynchronize() from __device__ functions, which CUDA 12 removed.",
                "first_error_verbatim": "/tmp/voxcraft-sim/src/VX3/VX3_VoxelyzeKernel.cu(269): error: calling a __host__ function(\"cudaDeviceSynchronize\") from a __device__ function(\"VX3_VoxelyzeKernel::doTimeStep\") is not allowed",
                "affected_device_functions": ["doTimeStep", "updateTemperature", "updateAttach"]},
            "blocker_b_boost": {
                "what": "independently, nvcc cannot compile Boost.Asio's trait machinery reached through boost::process when building VX3_SimulationManager.cu. This is an old-Boost-against-modern-GCC failure and is NOT a CUDA or GPU problem.",
                "error_verbatim": "/usr/include/boost/asio/traits/static_query.hpp:85:47: error: ''indirect_ref' not supported by dump_decl<declaration error>' is not a template [-fpermissive]",
                "failing_target": "CMakeFiles/voxelyze.3.0.dir/src/VX3/VX3_SimulationManager.cu.o"},
            "note": "both blockers are present in the same log; they are separate failures, not one described two ways."},
        "2_pinned_image_as_shipped": {
            "what": "could not even CONFIGURE. The pinned base image supplies exactly the stack the README names - CUDA 10.2.89, Boost 1.65.1, GCC 7.5.0 - but Ubuntu 18.04 ships CMake 3.10.2 while voxcraft-sim's CMakeLists requires >= 3.12.",
            "error_verbatim": "CMake Error at CMakeLists.txt:1 (cmake_minimum_required)",
            "ours_or_theirs": "OURS. This is a gap in our environment setup, not a defect in the project, and it is why attempt 3 exists."}},
    "what_this_does_not_establish": [
        "that voxcraft-sim cannot be built. See attempts for exactly which toolkits were tried.",
        "anything about whether its results agree with ours. No comparison was run and none is implied."],
    "acceptance_as_declared": "./voxcraft-sim -i demos/basic/ -o output.xml -f produces a non-empty history file and exits 0.",
    "process_note": ("Attempt 1's job reported COMPLETED while every build inside it failed, because the script ran "
                     "to the end. The probe script now sets PROBE-VERDICT and exits 42 on a failed build, so the "
                     "job's own status carries the result - attempt 2 duly reported FAILED. A COMPLETED job is not "
                     "a result anyone has read."),
}
json.dump(D, open(f"{ROOT}/data/voxcraft-probe.json", "w"), indent=2)
for a in attempts:
    o = a["observed"]
    print(f"attempt {a['attempt']}: {'BUILT' if o and o['built'] else 'failed' if o else 'no log'}"
          f"  cmake_rc={o['cmake_rcs'] if o else '-'} make={o['make_exits'] if o else '-'}"
          f"  {o['verdict_line'] if o else ''}")
print("any built:", bool(built))
