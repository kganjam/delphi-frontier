#!/usr/bin/env bash
# Packet controller. PREFLIGHT=1 verifies source hashes only. Otherwise: preflight, CUDA control gate, then the full run (CUDA required, no CPU fallback).
set -euo pipefail
cd "$(dirname "$0")/../.."; OUT="${OUT:-out}"; mkdir -p "$OUT"
python3 -m engineering.rd_inverse.design preflight
[ "${PREFLIGHT:-0}" = "1" ] && exit 0
timeout -k 10 900 python3 -m engineering.rd_inverse.design run --out "$OUT" --device cuda --require-cuda && rc=0 || rc=$?; echo "run exit=$rc (partial outputs retained)"
tar -czf "$OUT/rd_inverse_outputs.tgz" -C "$OUT" $(cd "$OUT" && ls *.json *.npz)
ls -l "$OUT"/rd_inverse_outputs.tgz; sha256sum "$OUT"/rd_inverse_outputs.tgz
exit "$rc"
