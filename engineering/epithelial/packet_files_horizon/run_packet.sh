#!/usr/bin/env bash
# Bounded Morpheus observation-horizon packet. CPU only, one thread per arm, no git.
#
#   bash run_packet.sh [OUTDIR] [WORKERS]
#
# Needs: curl, sha256sum, tar, python3, timeout, setsid, xargs.
# Carries forward every repair from the reviewed sweep packet: BIN is exported, the solver and
# all scratch live outside the output tree, each arm runs in its own process group, and the
# runner NEVER decides its own success.
set -u -o pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-$HERE/out}
WORKERS=${2:-8}

ARM_TIMEOUT_S=${ARM_TIMEOUT_S:-600}          # soft, per arm; measured basis ~55 s at StopTime 8000
ARM_KILL_GRACE_S=30
JOB_TIMEOUT_S=${JOB_TIMEOUT_S:-1800}         # hard, whole scientific tree
OUTPUT_CAP_MB=${OUTPUT_CAP_MB:-100}
DOWNLOAD_CAP_BYTES=${DOWNLOAD_CAP_BYTES:-67108864}
TIMING_GATE_FACTOR=${TIMING_GATE_FACTOR:-2.0}   # refuse if measured rate is this much worse
BIN_URL=https://gitlab.com/morpheus.lab/morpheus/-/package_files/178666119/download
BIN_SHA=3d9a6e5a4cb86824b745500df1474596d39cce5deed24f767c0841df0f94d5ad

WORKSPACE=${PACKET_WORKSPACE:-$(mktemp -d -t epi-horizon-XXXXXX)}
mkdir -p "$OUT" "$WORKSPACE"
BIN=${PACKET_BIN:-$WORKSPACE/morpheus-2.3.9}

echo "workspace (not collected): $WORKSPACE"
echo "output    (collected)    : $OUT"

python3 "$HERE/verify_packet.py" --dir "$HERE" || { echo "packet verification failed; refusing"; exit 3; }

if [ -z "${PACKET_BIN:-}" ]; then
  if [ ! -x "$BIN" ]; then
    code=$(curl -sS -L -m 600 --max-filesize "$DOWNLOAD_CAP_BYTES" \
                -w '%{http_code}' -o "$BIN.part" "$BIN_URL") || {
      echo "download failed (curl exit $?, http $code); refusing"; exit 3; }
    [ "$code" = "200" ] || { echo "download HTTP $code, expected 200; refusing"; exit 3; }
    mv "$BIN.part" "$BIN"
  fi
  got=$(sha256sum "$BIN" | cut -d' ' -f1)
  [ "$got" = "$BIN_SHA" ] || { echo "binary sha256 $got, pinned $BIN_SHA; refusing"; exit 3; }
  chmod +x "$BIN"
fi
python3 - "$BIN" "$BIN_URL" "$OUT/binary-receipt.json" <<'PY'
import hashlib, json, platform, sys, os
b, url, out = sys.argv[1], sys.argv[2], sys.argv[3]
d = open(b, 'rb').read()
json.dump({"url": url, "bytes": len(d), "sha256": hashlib.sha256(d).hexdigest(),
           "note": "the binary itself is deliberately NOT in this output tree",
           "uname": platform.uname()._asdict(), "python": sys.version.split()[0],
           "nproc": os.cpu_count()}, open(out, 'w'), indent=1)
PY

# ---- timing gate: one SHORT probe in the workspace, before the scientific tree -------------
# Measures the real rate here instead of trusting the packet's projection. The probe writes to
# the workspace, never to OUT, so it cannot be mistaken for a result.
GATE=$WORKSPACE/timing-gate
mkdir -p "$GATE"
FIRST=$(python3 -c "import json;print(json.load(open('$HERE/arms.json'))[0]['id'])")
sed 's|<StopTime value="8000"/>|<StopTime value="500"/>|' "$HERE/models/$FIRST.xml" > "$GATE/model.xml"
S=$(date +%s.%N)
( cd "$GATE" && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
    timeout --kill-after=30 300 "$BIN" -f model.xml --no-gnuplot --num-threads 1 >stdout.log 2>&1 )
E=$(date +%s.%N)
python3 - "$S" "$E" "$HERE/arms.json" "$TIMING_GATE_FACTOR" "$JOB_TIMEOUT_S" "$WORKERS" "$OUT/timing-gate.json" <<'PY'
import json, sys
s, e, arms, factor, job_s, workers, out = sys.argv[1:]
el = float(e) - float(s)
n = len(json.load(open(arms)))
rate = el / 500.0                      # seconds per 1000 model-time units is rate*1000
per_arm = rate * 8000
total_cpu = per_arm * n
wall = total_cpu / max(int(workers), 1)
declared = 55.0
ok = per_arm <= declared * float(factor) and wall <= float(job_s)
json.dump({"probe_stop_time": 500, "probe_wall_s": round(el, 2),
           "projected_per_arm_s": round(per_arm, 1), "declared_per_arm_s": declared,
           "projected_total_cpu_s": round(total_cpu, 1),
           "projected_wall_s_at_workers": round(wall, 1), "workers": int(workers),
           "job_timeout_s": float(job_s), "passed": ok,
           "rule": "refuse if the measured per-arm projection exceeds declared x factor, or if "
                   "the projected wall time exceeds the whole-tree bound"}, open(out, "w"), indent=1)
print(f"timing gate: probe {el:.1f}s -> {per_arm:.0f}s/arm, {wall:.0f}s wall at {workers} workers; "
      f"{'PASS' if ok else 'REFUSE'}")
sys.exit(0 if ok else 4)
PY
[ $? -eq 0 ] || { echo "timing gate refused; not starting the scientific tree"; exit 4; }

# ---- the arms -------------------------------------------------------------------------------
run_one() {
  a=$1
  d="$OUT/$a"
  mkdir -p "$d"
  cp "$HERE/models/$a.xml" "$d/model.xml"
  ( cd "$d" && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
      setsid timeout --kill-after="$ARM_KILL_GRACE_S" --signal=TERM "$ARM_TIMEOUT_S" \
        "$BIN" -f model.xml --no-gnuplot --num-threads 1 > stdout.log 2>&1
    echo "exit=$?" > exit.txt )
  rm -f "$d"/*.tif "$d"/*.tiff "$d"/model_graph.dot 2>/dev/null
  return 0          # per-arm success is decided by the audit, never here
}
export -f run_one
export BIN OUT HERE ARM_TIMEOUT_S ARM_KILL_GRACE_S

ARMS=$(python3 -c "import json;print('\n'.join(a['id'] for a in json.load(open('$HERE/arms.json'))))")
echo "$ARMS" | timeout --kill-after=60 "$JOB_TIMEOUT_S" \
  xargs -P "$WORKERS" -I{} bash -c 'run_one "$@"' _ {}
job_rc=$?
echo "xargs/job wrapper exit=$job_rc (NOT the result)"

SZ=$(du -sm "$OUT" | cut -f1)
echo "scientific output: ${SZ} MB (cap ${OUTPUT_CAP_MB} MB)"
[ "$SZ" -gt "$OUTPUT_CAP_MB" ] && { echo "output cap exceeded; refusing to package"; exit 5; }

# ---- controls and audit: these decide the result ---------------------------------------------
python3 "$HERE/check_reproduction.py" --pins "$HERE/reproduction-pins.json" --out "$OUT" \
        --report "$OUT/reproduction.json"; repro_rc=$?
python3 "$HERE/audit_completeness.py" --arms "$HERE/arms.json" --out "$OUT" \
        --job-wrapper-exit "$job_rc" --report "$OUT/completeness.json"; audit_rc=$?
[ -s "$OUT/completeness.json" ] || { echo "completeness audit produced NO report (it crashed); refusing"; audit_rc=6; }
python3 "$HERE/analyze_horizon.py" --protocol "$HERE/horizon-protocol.json" --out "$OUT" \
        --reproduction "$OUT/reproduction.json" --report "$OUT/horizon-result.json"; sci_rc=$?

python3 - "$OUT" "$job_rc" "$repro_rc" "$audit_rc" "$sci_rc" <<'PY'
import json, sys
out, *rcs = sys.argv[1:]
j, r, a, s = (int(x) for x in rcs)
json.dump({"job_wrapper": j, "reproduction": r, "completeness": a, "horizon_analysis": s,
           "note": "all four preserved. completeness is the transport verdict; reproduction "
                   "gates interpretation; horizon_analysis is the scientific reading."},
          open(out + "/exit-codes.json", "w"), indent=1)
PY
cp "$HERE/horizon-protocol.json" "$OUT/horizon-protocol.json"
tar czf "$OUT/../epithelial-horizon-result.tgz" -C "$OUT" .
echo "result tarball sha256: $(sha256sum "$OUT/../epithelial-horizon-result.tgz" | cut -d' ' -f1)"
echo "exits: reproduction=$repro_rc completeness=$audit_rc horizon=$sci_rc"
exit "$audit_rc"
