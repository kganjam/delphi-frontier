#!/bin/bash
# --inject-file cap is 65536 B of BASE64, i.e. ~49152 B raw across all files.
set -x
base64 -d /work/evo2_prompt_replication_job.py.gz.b64 | gunzip > /work/job.py || exit 1
base64 -d /work/input_set.json.gz.b64 | gunzip > /work/input_set.json || exit 1
sha256sum /work/job.py /work/input_set.json
pip install -q --no-deps evo2 vtx || exit 1
pip install -q biopython huggingface_hub || exit 1
python3 /work/job.py --input-set /work/input_set.json --out-dir /work/out --model evo2_7b --replicates 5 --budget-seconds 1800
echo "EVOPR_RC=$?"
