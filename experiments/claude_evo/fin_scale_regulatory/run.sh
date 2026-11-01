#!/bin/bash
set -x
pip install -q --no-deps evo2 vtx || exit 1
pip install -q biopython huggingface_hub || exit 1
python3 /work/evo2_fin_scale_job.py --input-set /work/input_set.json --out-dir /work/out --model evo2_7b --budget-seconds 3000
echo "EVOFS_RC=$?"
