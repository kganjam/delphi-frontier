#!/bin/bash
# Nebius job body: Morpheus 2.3.9 production batch for the frozen xenomorph protocol.
# Inputs injected under /in. Output streamed to the job log as sha256-checked base64 parts.
set -u
echo "XM_START $(date -u +%FT%TZ) nproc=$(nproc)"
mkdir -p /w/engineering/xenomorph && cd /w
touch engineering/__init__.py
touch engineering/xenomorph/__init__.py
base64 -d /in/bundle.b64 | tar xz -C engineering/xenomorph
echo "XM_BUNDLE $(sha256sum /in/bundle.b64)"
sha256sum engineering/xenomorph/* | sed 's/^/XM_INPUT /'
export DEBIAN_FRONTEND=noninteractive
(apt-get update -qq && apt-get install -y -qq curl ca-certificates >/dev/null) 2>&1 | tail -2
pip install -q scipy scikit-image tifffile 2>&1 | tail -2
python -m engineering.xenomorph.offlattice --write-default engineering/xenomorph/offlattice_sweep.json
python -c 'import numpy,torch;print("XM_PY",numpy.__version__,torch.__version__,torch.cuda.is_available())'
curl -sL -o /w/morpheus-2.3.9 "https://gitlab.com/morpheus.lab/morpheus/-/package_files/178666119/download"
echo "XM_BINARY $(sha256sum /w/morpheus-2.3.9)"
echo "3d9a6e5a4cb86824b745500df1474596d39cce5deed24f767c0841df0f94d5ad  /w/morpheus-2.3.9" | sha256sum -c - || { echo XM_BINARY_HASH_FAIL; exit 3; }
chmod +x /w/morpheus-2.3.9
export MORPHEUS_BIN=/w/morpheus-2.3.9 OMP_NUM_THREADS=1
# run list: arm seed scale  (refinement scale-1.25 runs first: they are the longest)
cat > runs.txt <<EOF
dah 1 1.25
dah 2 1.25
dah 1 0.75
dah 2 0.75
dah 1 1.0
dah 2 1.0
dah 3 1.0
dah 4 1.0
equal 1 1.0
equal 2 1.0
equal 3 1.0
equal 4 1.0
zero 1 1.0
zero 2 1.0
zero 3 1.0
zero 4 1.0
EOF
emit() {  # emit one directory as a base64 part
  local name=$1 dir=$2
  tar czf /w/$name.tgz -C $(dirname $dir) $(basename $dir)
  local s=$(sha256sum /w/$name.tgz | cut -d' ' -f1)
  echo "XM_PART_BEGIN $name sha256=$s bytes=$(stat -c %s /w/$name.tgz)"
  base64 -w 120 /w/$name.tgz
  echo "XM_PART_END $name"
}
export -f emit
one() {
  local arm=$1 seed=$2 scale=$3 d=/w/runs/$1-s$2-x$3
  python -m engineering.xenomorph.cpm_model --arm $arm --seed $seed --scale $scale --out $d > $d.receipt.log 2>&1
  local rc=$?
  python -m engineering.xenomorph.analyze $d > $d/analyze.log 2>&1; local arc=$?
  if [ "$seed" = "1" ]; then every=2; else every=4; fi
  python -m engineering.xenomorph.pack_fields $d --every $every >> $d/analyze.log 2>&1; local prc=$?
  tail -c 2000 $d/stdout.log > $d/stdout.tail; rm -f $d/stdout.log
  echo "run_exit=$rc analyze_exit=$arc pack_exit=$prc" > $d/exit.txt
  rm -f $d/*.tif
  echo "XM_RUN_DONE $arm s$seed x$scale run=$rc analyze=$arc pack=$prc $(date -u +%T)"
  flock /w/emit.lock bash -c "emit $arm-s$seed-x$scale $d"
}
export -f one
# GPU sweep (separate engine) runs concurrently with the CPU Morpheus batch
nvidia-smi --query-gpu=timestamp,name,utilization.gpu,memory.used --format=csv -l 10 > /w/gpu_telemetry.csv 2>&1 &
TEL=$!
( python -m engineering.xenomorph.offlattice --sweep engineering/xenomorph/offlattice_sweep.json --out /w/sweep > /w/sweep.log 2>&1; echo "sweep_exit=$?" >> /w/sweep.log; echo "XM_SWEEP_DONE $(tail -1 /w/sweep.log) $(date -u +%T)" ) &
SWP=$!
mkdir -p /w/runs
xargs -P 16 -L 1 bash -c 'one $0 $1 $2' < runs.txt
wait $SWP; kill $TEL
mkdir -p /w/sweepret && cp -r /w/sweep /w/sweep.log /w/gpu_telemetry.csv /w/sweepret/ 2>/dev/null
emit sweep /w/sweepret
echo "XM_ALL_DONE $(date -u +%FT%TZ)"
