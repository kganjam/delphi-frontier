#!/usr/bin/env bash
# Grid refinement for the xenobot design space. Four levels, two gaits, on
# PARITY-MATCHED grids: the outer envelope and the physical actuation field are
# held fixed while the lattice is refined, so the only thing that changes is the
# discretisation. The artifact being re-examined refined a grid whose actuation
# split moved with the grid, which is the confound its own post-hoc identified.
set -x
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq git g++ make ca-certificates python3 time > /tmp/apt.log 2>&1
echo "APT-EXIT=$?"; g++ --version | head -1
PIN=4287e365e11416dd108f2f361e9ec4c5a011a16c
mkdir -p /work && cd /work
git clone -q https://github.com/jonhiller/Voxelyze.git Voxelyze && cd Voxelyze
git checkout -q "$PIN"
test "$(git rev-parse HEAD)" = "$PIN" && echo "PIN-OK" || { echo "PIN-MISMATCH"; exit 1; }
# upstream makefile defect: default FLAGS carry -DPARDISO_5=1, leaving undefined
# references to pardisoinit/pardiso. Override FLAGS to drop it.
make -j4 FLAGS="-O3 -std=c++11 -Wall -I./include" > /tmp/vox.log 2>&1
echo "VOX-MAKE-EXIT=$?"; ls -la lib/
cd /work
cp /inject/soft_actuation.cpp /work/soft_actuation.cpp
g++ -O2 -std=c++11 -I Voxelyze/include /work/soft_actuation.cpp -L Voxelyze/lib -lvoxelyze.0.9 -o soft_actuation
echo "DRIVER-BUILD-EXIT=$?"
mkdir -p /work/out
# regression control: reproduce the published travelling baseline bit-for-bit
./soft_actuation --pattern=travelling --out=/work/out/REGRESSION-baseline
cat /work/out/REGRESSION-baseline.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('REGRESSION net_disp_m =', d['result']['net_disp_m'], ' expected 0.014577281')"
cat > /work/jobs.txt <<'JOBS'
A1 travelling   5  3  3 0.01          0.5
A2 travelling  10  6  6 0.005         0.5
A3 travelling  15  9  9 0.0033333333  0.5
A4 travelling  20 12 12 0.0025        0.5
B1 longitudinal 4  3  3 0.01          0.5
B2 longitudinal 8  6  6 0.005         0.5
B3 longitudinal 12 9  9 0.0033333333  0.5
B4 longitudinal 16 12 12 0.0025       0.5
A1q travelling   5  3  3 0.01         0.25
A2q travelling  10  6  6 0.005        0.25
A3q travelling  15  9  9 0.0033333333 0.25
B1q longitudinal 4  3  3 0.01         0.25
B2q longitudinal 8  6  6 0.005        0.25
B3q longitudinal 12 9  9 0.0033333333 0.25
JOBS
run_one() {
  set -- $1
  tag=$1; pat=$2; nx=$3; ny=$4; nz=$5; vox=$6; dts=$7
  t0=$SECONDS
  /work/soft_actuation --pattern=$pat --nx=$nx --ny=$ny --nz=$nz \
      --voxel=$vox --dtScale=$dts --out=/work/out/$tag > /work/out/$tag.stdout 2>&1
  echo "$tag rc=$? wall=$(( SECONDS - t0 ))s"
}
export -f run_one
cat /work/jobs.txt | grep -v '^$' | xargs -d'\n' -I{} -P 8 bash -c 'run_one "{}"'
echo "=== ALL RUNS DONE ==="
for f in /work/out/*.json; do
  python3 -c "
import json,sys
d=json.load(open('$f'))
p=d['params']; r=d['result']; n=d['numerics']
print('$(basename $f .json)', p['nx'],p['ny'],p['nz'], p['voxel_m'], n['dt_scale'],
      'net_m=%.9f'%r['net_disp_m'], 'BL=%.6f'%r['disp_in_body_lengths'],
      'envelope=%.4f'%(p['nx']*p['voxel_m']), 'diverged=',n['diverged'])"
done
mkdir -p /output/refine
cp /work/out/*.json /work/out/*.stdout /output/refine/ 2>/dev/null
cp /work/out/*-com.csv /output/refine/ 2>/dev/null
ls -la /output/refine/ | head -40
echo "=== REFINE COMPLETE ==="
