#!/usr/bin/env bash
# Packet controller. PREFLIGHT=1 verifies source hashes only. Otherwise: preflight, CUDA control gate, then the full run (CUDA required, no CPU fallback).
set -euo pipefail
cd "$(dirname "$0")/../.."; OUT="${OUT:-out}"; mkdir -p "$OUT"
python3 -m engineering.rd_inverse.design preflight
[ "${PREFLIGHT:-0}" = "1" ] && exit 0
python3 -m engineering.rd_inverse.design run --out "$OUT" --device cuda --require-cuda
tar -czf "$OUT/rd_inverse_outputs.tgz" -C "$OUT" control.json targets.json targets.npz traces.json evaluated_fields.npz selection.json validation_controls.json independent_checks.json receipt.json
ls -l "$OUT"/rd_inverse_outputs.tgz; sha256sum "$OUT"/rd_inverse_outputs.tgz
