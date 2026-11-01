#!/bin/bash
# Arm B of docs/handoff/xenobot-packet-to-infra.md: build voxcraft-sim at its pin, UNMODIFIED,
# in the project's own pinned image nvcr.io/nvidia/cuda:10.2-devel-ubuntu18.04, with an explicit
# PTX-only gencode (arch=compute_75,code=compute_75) so the modern driver must JIT forward.
# Acceptance (handoff): ./voxcraft-sim -i demos/basic/ -o output.xml -f -> non-empty history, exit 0.
# Note: voxcraft-sim.cpp returns 0 even if the worker fails, so exit 0 alone is NOT acceptance;
# we additionally require a non-empty output.xml and a non-empty history.
set -u
PIN=dd8668f99ff74fb2fc2ee60deb91287a3b519d8f
SRC_SHA=0a0f4fd105a8df21df8b62a7d00e5178096d28415f2fb9f1679f6c78fd2c6546
GENCODE=${GENCODE:-arch=compute_75,code=compute_75}
CMAKE_URL=https://github.com/Kitware/CMake/releases/download/v3.18.6/cmake-3.18.6-Linux-x86_64.tar.gz
O=/out; mkdir -p $O; W=/work; mkdir -p $W; cd $W
R=$O/receipt.txt
log(){ echo "[$(date -u +%FT%TZ)] $*" | tee -a $R; }
step(){ local name=$1; shift; local t0=$(date +%s.%N); "$@" > $O/$name.log 2>&1; local rc=$?; local t1=$(date +%s.%N);
  log "STEP $name rc=$rc wall_s=$(python3 -c "print(round($t1-$t0,2))" 2>/dev/null || echo ?)"; return $rc; }
log "VOXGPU_ARMB start host=$(hostname) gencode=$GENCODE"
nvidia-smi > $O/nvidia-smi.txt 2>&1; log "nvidia-smi rc=$?"
nvidia-smi --query-gpu=name,driver_version,compute_cap,memory.total --format=csv >> $R 2>&1
cat /etc/os-release | head -2 >> $R; ls -l /usr/local/ | grep cuda >> $R
/usr/local/cuda/bin/nvcc --version >> $R 2>&1
export DEBIAN_FRONTEND=noninteractive
step apt bash -c "apt-get update && apt-get install -y --no-install-recommends ca-certificates wget libboost-filesystem-dev libboost-thread-dev libboost-chrono-dev libboost-program-options-dev libboost-dev python3" || { log "APT_FAIL"; }
dpkg -l | grep -E "libboost[0-9.]*-dev|libboost-dev " >> $R
gcc --version | head -1 >> $R
step cmake_dl bash -c "wget -q -O cmake.tgz $CMAKE_URL && tar xzf cmake.tgz" ; sha256sum cmake.tgz >> $R
export PATH=$W/cmake-3.18.6-Linux-x86_64/bin:$PATH; cmake --version | head -1 >> $R
step src_dl wget -q -O vx.tar.gz https://codeload.github.com/voxcraft/voxcraft-sim/tar.gz/$PIN
GOT=$(sha256sum vx.tar.gz | cut -d' ' -f1); log "src bytes=$(stat -c %s vx.tar.gz) sha256=$GOT"
if [ "$GOT" != "$SRC_SHA" ]; then log "SOURCE_MISMATCH"; STATUS=SOURCE_MISMATCH; else
tar xzf vx.tar.gz; cd voxcraft-sim-$PIN; mkdir -p build; cd build
step configure cmake .. -DCUDA_ARCH=$GENCODE; CRC=$?
step build make -j16 VERBOSE=1; BRC=$?
grep -n -m5 -E "error|Error" $O/build.log >> $R
ls -l voxcraft-sim vx3_node_worker vx3_node_daemon vx3_test >> $R 2>&1
if [ $CRC -ne 0 ]; then STATUS=CONFIGURE_FAIL; elif [ $BRC -ne 0 ]; then STATUS=COMPILE_FAIL; else
  sha256sum voxcraft-sim vx3_node_worker >> $R
  /usr/local/cuda/bin/cuobjdump --list-ptx vx3_node_worker > $O/cuobjdump_ptx.txt 2>&1
  /usr/local/cuda/bin/cuobjdump --list-elf vx3_node_worker > $O/cuobjdump_elf.txt 2>&1
  log "ptx_entries=$(grep -c ptx $O/cuobjdump_ptx.txt) elf_entries=$(grep -c -i elf $O/cuobjdump_elf.txt)"
  # tiny body first: the unmodified stock demo (2 voxels, 1 s)
  t0=$(date +%s.%N)
  timeout 600 ./voxcraft-sim -i ../demos/basic/ -o output.xml -f > a.history 2> demo.stderr; DRC=$?
  t1=$(date +%s.%N)
  log "DEMO rc=$DRC wall_s=$(python3 -c "print(round($t1-$t0,2))") history_bytes=$(stat -c %s a.history) output_bytes=$(stat -c %s output.xml 2>/dev/null || echo 0)"
  cp demo.stderr $O/; head -c 200000 a.history > $O/a.history.head; cp output.xml $O/ 2>/dev/null
  sha256sum a.history output.xml >> $R 2>&1
  ls -lR workspace >> $R 2>&1
  # worker directly with stderr, to capture any CUDA/JIT error text
  VXT=$(ls workspace/locally/*.vxt 2>/dev/null | head -1)
  if [ -n "$VXT" ]; then timeout 600 ./vx3_node_worker -i $VXT -o direct.vxr > $O/worker_direct.stdout.txt 2> $O/worker_direct.stderr.txt; log "WORKER_DIRECT rc=$?"; head -c 100000 $O/worker_direct.stdout.txt > $O/worker_direct.stdout.head; rm $O/worker_direct.stdout.txt; cp direct.vxr $O/ 2>/dev/null; fi
  if [ $DRC -eq 0 ] && [ -s a.history ] && [ -s output.xml ] && grep -q -i "fitness\|detail" output.xml; then STATUS=PASS; else STATUS=RUN_FAIL; fi
  if [ -n "${EXTRA:-}" ] && [ -f "$EXTRA" ] && [ "$STATUS" = PASS ]; then step extra bash "$EXTRA" "$PWD"; fi
fi; fi
log "STATUS=$STATUS"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader >> $R 2>&1
cd /; tar czf /tmp/ret.tgz -C $O . ; log "RETURN bytes=$(stat -c %s /tmp/ret.tgz) sha256=$(sha256sum /tmp/ret.tgz | cut -d' ' -f1)"
echo "VOXGPU_B64_BEGIN"; base64 -w 4000 /tmp/ret.tgz; echo "VOXGPU_B64_END"
cat $R
