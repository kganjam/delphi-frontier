#!/bin/bash
# Nebius job body: Morpheus 2.3.9 production batch for the frozen xenomorph protocol.
# Inputs injected under /in. Output streamed to the job log as sha256-checked base64 parts.
set -u
echo "XM_START $(date -u +%FT%TZ) nproc=$(nproc)"
mkdir -p /w/engineering/xenomorph && cd /w
cp /in/__init__.py engineering/__init__.py
for f in __init__.py cpm_model.py analyze.py pack_fields.py protocol.json; do cp /in/$f engineering/xenomorph/$f; done
sha256sum engineering/xenomorph/* | sed 's/^/XM_INPUT /'
export DEBIAN_FRONTEND=noninteractive
(apt-get update -qq && apt-get install -y -qq curl ca-certificates >/dev/null) 2>&1 | tail -2
pip install -q numpy==2.4.4 scipy scikit-image tifffile 2>&1 | tail -2
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
mkdir -p /w/runs
xargs -P 16 -L 1 bash -c 'one $0 $1 $2' < runs.txt
echo "XM_ALL_DONE $(date -u +%FT%TZ)"
