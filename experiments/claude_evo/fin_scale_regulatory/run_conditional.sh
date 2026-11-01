#!/bin/bash
# Everything is injected gzip+base64, including the job script.
#
# The --inject-file cap is 65536 bytes of *base64-encoded* payload, i.e. only
# ~49152 bytes of raw plaintext across all files. A 53,124 B set was rejected
# (53124*4/3 = 70832 > 65536) while 43,314 B and 33,054 B sets were accepted.
# Compressing the script buys back the headroom; its sha256 is printed so the
# log proves which code ran.
set -x
base64 -d /work/evo2_conditional_job.py.gz.b64 | gunzip > /work/evo2_conditional_job.py || exit 1
base64 -d /work/input_set.json.gz.b64          | gunzip > /work/input_set.json || exit 1
base64 -d /work/candidates_slim.json.gz.b64    | gunzip > /work/candidates.json || exit 1
sha256sum /work/evo2_conditional_job.py /work/input_set.json /work/candidates.json
pip install -q --no-deps evo2 vtx || exit 1
pip install -q biopython huggingface_hub || exit 1
python3 /work/evo2_conditional_job.py --input-set /work/input_set.json --candidates /work/candidates.json --out-dir /work/out --model evo2_7b --budget-seconds 1800
echo "EVOCD_RC=$?"
