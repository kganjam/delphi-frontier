#!/usr/bin/env bash
# Factorial sweep (not preregistered; descriptive). usage: sweep.sh <binary> <outroot>
B=$1; R=$2; mkdir -p $R
for lam in 0 40 80 160 320; do for dir in 1 -1; do
 [ $lam = 0 ] && [ $dir = -1 ] && continue
 for eps in 0.05 0.1 0.2; do for per in 6 30 150; do for r in 1 1.5 3 10; do
  echo "$lam $dir $eps $per $r"
 done; done; done; done; done | xargs -P 3 -L 1 bash -c 'lam=$0 dir=$1 eps=$2 per=$3 r=$4; id=lam${lam}_dir${dir}_eps${eps}_T${per}_r${r}; [ -f '"$R"'/$id/receipt.json ] && exit 0; python3 '"$(pwd)"'/run_arm.py '"$B"' '"$R"'/$id 0.1 XM_GEOM=strip XM_NX=10 XM_NY=3 XM_LAMBDA=$lam XM_DIR=$dir XM_EPS=$eps XM_PERIOD=$per XM_XIP=1 XM_XIM=$r XM_MAXTIME=$(python3 -c "print(10*$per)") >/dev/null; echo $id $?'
