#!/usr/bin/env bash
# Controller. PREFLIGHT=1 checks source hashes only (the manifest is only tested for existence). Otherwise one bundled run; CUDA required.
# MANIFEST and MANIFEST_SHA256 are infra's sealed fresh test-seed manifest; this script never opens it.
set -euo pipefail
cd "$(dirname "$0")/../.."; OUT="${OUT:-out}"; mkdir -p "$OUT"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python3 -m engineering.rd_multiic.multiic preflight ${MANIFEST:+--manifest "$MANIFEST"}
[ "${PREFLIGHT:-0}" = "1" ] && exit 0
timeout -k 10 1800 python3 -m engineering.rd_multiic.multiic run --out "$OUT" --device cuda --require-cuda --manifest "$MANIFEST" --manifest-sha256 "$MANIFEST_SHA256" && rc=0 || rc=$?
echo "run exit=$rc (partial outputs retained)"
exit "$rc"
