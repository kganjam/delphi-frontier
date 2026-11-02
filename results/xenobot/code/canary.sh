#!/usr/bin/env bash
echo "CANARY-ARGV-OK: $0 | $# args"
uname -a
nvidia-smi --query-gpu=name --format=csv,noheader || echo no-gpu
echo CANARY-DONE
