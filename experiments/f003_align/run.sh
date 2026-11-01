#!/bin/bash
cd /data/worktrees/delphi-frontier/claude-fseries
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=frontier_compute/vendor:.
for i in 1 2 3; do
systemd-run --user --scope -q -p TasksMax=256 -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=1800 python3 experiments/f003_align/align.py run experiments/f003_align/results/base /data/artifacts/claude-fseries/f003/spectra --workers 3; echo "base pass $i exit $?"
ls experiments/f003_align/results/base/*.jsonl | wc -l
done
systemd-run --user --scope -q -p TasksMax=256 -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=1800 python3 experiments/f003_align/align.py run experiments/f003_align/results/grid2 /data/artifacts/claude-fseries/f003/spectra_unused --arm grid2 --workers 3; echo "grid2 exit $?"
