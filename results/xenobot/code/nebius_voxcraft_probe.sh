#!/usr/bin/env bash
# voxcraft-sim build probe. Time-boxed. A stated build failure is the result.
set -x
PIN=dd8668f99ff74fb2fc2ee60deb91287a3b519d8f
echo "=== HOST FACTS ==="
nvidia-smi || echo "NO nvidia-smi"
nvcc --version || echo "NO nvcc"
ls -d /usr/local/cuda* || echo "NO /usr/local/cuda*"
echo "=== DEPS ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq curl wget ca-certificates git cmake build-essential \
  libboost-filesystem-dev libboost-thread-dev libboost-chrono-dev \
  libboost-program-options-dev > /tmp/apt.log 2>&1 || { echo "APT FAILED"; tail -40 /tmp/apt.log; }
echo "=== DISTRO CMAKE ==="; cmake --version 2>&1 | head -1 || echo "NO CMAKE"
# voxcraft-sim's CMakeLists requires >= 3.12; Ubuntu 18.04 ships 3.10.2, so the
# pinned base image cannot configure the project as shipped. Install the official
# Kitware binary rather than concluding a blocker that is one download away.
CMV=3.22.1
CMURL="https://github.com/Kitware/CMake/releases/download/v${CMV}/cmake-${CMV}-linux-x86_64.tar.gz"
if curl -fsSL -o /tmp/cmake.tgz "$CMURL" || wget -q -O /tmp/cmake.tgz "$CMURL"; then
  mkdir -p /opt/cmake && tar -xzf /tmp/cmake.tgz -C /opt/cmake --strip-components=1 \
    && export PATH=/opt/cmake/bin:$PATH && echo "=== INSTALLED CMAKE ===" && cmake --version | head -1
else
  echo "CMAKE DOWNLOAD FAILED"
fi
export PATH=/opt/cmake/bin:$PATH
# Hard gate: CMakeLists requires >= 3.12. Proceeding with an older cmake only
# produces a self-inflicted blocker that looks like a project defect.
CMV_NOW=$(cmake --version 2>/dev/null | head -1 | grep -oE "[0-9]+\.[0-9]+" | head -1)
CMV_MAJ=${CMV_NOW%%.*}; CMV_MIN=${CMV_NOW##*.}
if [ "$CMV_MAJ" -lt 3 ] || { [ "$CMV_MAJ" -eq 3 ] && [ "$CMV_MIN" -lt 12 ]; }; then
  echo "ENVIRONMENT-NOT-READY: cmake $CMV_NOW is older than the 3.12 CMakeLists requires."
  echo "This is OUR environment, not a defect in voxcraft-sim. Aborting rather than"
  echo "recording a blocker we manufactured."
  exit 43
fi
echo "CMAKE-GATE-OK $CMV_NOW"
echo "BOOST VERSION:"; grep -h "define BOOST_LIB_VERSION\|define BOOST_VERSION " /usr/include/boost/version.hpp 2>/dev/null
gcc --version | head -1
echo "=== CLONE AT PIN ==="
cd /tmp && git clone -q https://github.com/voxcraft/voxcraft-sim.git && cd voxcraft-sim
git checkout -q "$PIN" && echo "HEAD=$(git rev-parse HEAD)"
test "$(git rev-parse HEAD)" = "$PIN" && echo "PIN-OK" || echo "PIN-MISMATCH"
echo "=== LICENCE OF RECORD (read the bytes, do not assume) ==="
head -5 LICENSE 2>/dev/null; sha256sum LICENSE 2>/dev/null
echo "=== UPSTREAM DOCKERFILE, verbatim (what the project itself does) ==="
cat Dockerfile 2>/dev/null || echo "no Dockerfile"
echo "=== README build section ==="
grep -n -A6 -i "cuda\|boost\|cmake" README.md 2>/dev/null | head -30
echo "=== CMakeLists facts ==="
grep -n "CUDA_ARCH\|CMAKE_CUDA_COMPILER\|CMAKE_CXX_STANDARD\|Boost" CMakeLists.txt | head -30
mkdir -p build && cd build
for ARCH in "arch=compute_89,code=sm_89" "arch=compute_75,code=compute_75"; do
  echo "=== ARM: CUDA_ARCH=$ARCH ==="
  rm -rf CMakeCache.txt CMakeFiles
  cmake .. -DCUDA_ARCH="$ARCH" > /tmp/cm.log 2>&1
  echo "cmake rc=$?"; tail -25 /tmp/cm.log
  timeout 2400 make -j8 > /tmp/make.log 2>&1
  rc=$?; echo "MAKE-EXIT=$rc"
  if [ $rc -ne 0 ]; then
    echo "--- FIRST COMPILER ERROR, VERBATIM ---"
    grep -n -m1 -B4 -A25 -E "error:|Error " /tmp/make.log || tail -60 /tmp/make.log
    echo "--- tail of make.log ---"; tail -25 /tmp/make.log
    continue
  fi
  echo "BUILD OK for $ARCH"; BUILT_OK=1; ls -la voxcraft-sim vx3_node_worker 2>/dev/null
  echo "=== RUN demos/basic ==="
  cd /tmp/voxcraft-sim/build
  timeout 900 ./voxcraft-sim -i ../demos/basic/ -o /tmp/output_$RANDOM.xml -f > /tmp/run.log 2>&1
  echo "RUN-EXIT=$?"; tail -30 /tmp/run.log
  ls -la /tmp/output_*.xml && wc -c /tmp/output_*.xml
  break
done
echo "=== COPY ARTIFACTS ==="
mkdir -p /output/voxcraft-probe
cp /tmp/cm.log /tmp/make.log /output/voxcraft-probe/ 2>/dev/null
cp /tmp/run.log /output/voxcraft-probe/ 2>/dev/null
cp /tmp/output_*.xml /output/voxcraft-probe/ 2>/dev/null
nvidia-smi > /output/voxcraft-probe/nvidia-smi.txt 2>&1
echo "=== PROBE COMPLETE ==="
# A COMPLETED job is not a result anyone has read. Make the exit code carry the
# verdict so the job's own status reflects whether the build succeeded.
if [ "${BUILT_OK:-0}" = "1" ]; then
  echo "PROBE-VERDICT=BUILT"; exit 0
else
  echo "PROBE-VERDICT=BUILD-FAILED"; exit 42
fi
