#!/bin/bash
# The --inject-file cap is 65536 bytes of BASE64 payload, so only ~49152 bytes
# of raw plaintext across all files. Hence everything, including the script,
# arrives gzip+base64; the sha256 line proves which code ran.
set -x
base64 -d /work/motif_scan_job.py.gz.b64    | gunzip > /work/motif_scan_job.py || exit 1
base64 -d /work/input_set.json.gz.b64       | gunzip > /work/input_set.json || exit 1
base64 -d /work/candidates_slim.json.gz.b64 | gunzip > /work/candidates.json || exit 1
sha256sum /work/motif_scan_job.py /work/input_set.json /work/candidates.json
pip install -q pyjaspar biopython numpy || exit 1
python3 /work/motif_scan_job.py --input-set /work/input_set.json --candidates /work/candidates.json --out-dir /work/out --collection CORE --tax-group vertebrates --half prompt --skip-candidates --budget-seconds 2400
echo "MOTIF_RC=$?"
