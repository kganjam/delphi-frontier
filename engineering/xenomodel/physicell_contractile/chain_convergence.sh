#!/usr/bin/env bash
# Post-review N-node convergence check (gemini-4-argon review item 6). Chain (NY=1) of fixed length 128 um,
# r0 = 128/(NX-1); continuum scaling: node drag xi = xi0*(r0/16), spring k = 0.5*(16/r0); dt = 0.1*(r0/16)^2.
# usage: chain_convergence.sh <binary> <outroot>
B=$1; R=$2; mkdir -p $R
for nx in 5 9 17 33 65; do for pat in stand trav+ trav-; do echo $nx $pat; done; done | xargs -P 3 -L 1 bash -c '
nx=$0; pat=$1
read r0 s k dt <<< $(python3 -c "r0=128/($nx-1); s=r0/16; print(r0, s, 0.5/s, 0.1*s*s)")
case $pat in stand) W="XM_LAMBDA=0";; trav+) W="XM_LAMBDA=64 XM_DIR=1";; trav-) W="XM_LAMBDA=64 XM_DIR=-1";; esac
id=chain_nx${nx}_${pat}
python3 '"$(pwd)"'/run_arm.py '"$B"' '"$R"'/$id $dt XM_DTDIFF=$dt XM_GEOM=strip XM_NX=$nx XM_NY=1 XM_R0=$r0 XM_K=$k XM_XIP=$s XM_XIM=$(python3 -c "print(3*$s)") $W >/dev/null; echo $id $?'
