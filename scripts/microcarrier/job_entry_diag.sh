#!/usr/bin/env bash
# Container entry for a remote CPU batch of the frozen microcarrier plan.
# env: GROUPS_SEL (comma list), NJOBS, PLAN_SHA (expected), UPLOAD_FINAL, UPLOAD_PARTIAL (resumable-session URIs; never logged)
set -uo pipefail
export OMP_NUM_THREADS=1
echo "start $(date -u +%FT%TZ) host=$(hostname) nproc=$(nproc)"
mkdir -p /w/src && cp /in/* /w/src/ && cd /w/src
pip install -q numpy==2.1.3 2>&1 | tail -1
bash build.sh /w/build > /w/build.log 2>&1; echo "build_rc=$?"; tail -1 /w/build.log
cp /in/plan-diag.jsonl /w/plan.jsonl
GOT=$(sha256sum /w/plan.jsonl | cut -d' ' -f1); echo "plan_sha=$GOT"
[ "$GOT" = "$PLAN_SHA" ] || { echo "PLAN HASH MISMATCH"; exit 4; }
sha256sum /w/src/* /w/build/mc_runner > /w/out-hashes.txt
python3 mc_job.py --plan /w/plan.jsonl --runner /w/build/mc_runner --out /w/out --groups "$GROUPS_SEL" --jobs "$NJOBS" ${DUMP_IDS:+--dump "$DUMP_IDS"} > /w/job.log 2>&1 &
JP=$!
( sleep "${PARTIAL_AT_S:-1500}"; cd /w && tar -cJf partial.tar.xz out-hashes.txt job.log build.log out/*.json 2>/dev/null; \
  curl -s -o /dev/null -w "partial_upload_http=%{http_code}\n" -X PUT --upload-file partial.tar.xz "$UPLOAD_PARTIAL" ) &
while kill -0 $JP 2>/dev/null; do sleep 60; echo "$(date -u +%T) done=$(grep -c ' rc=' /w/job.log) fail=$(grep ' rc=' /w/job.log | grep -vc ' rc=0')"; done
wait $JP; echo "job_rc=$?"
cd /w && cp plan.jsonl out/ && tar -cJf final.tar.xz out-hashes.txt job.log build.log out
echo "final_sha256=$(sha256sum final.tar.xz | cut -d' ' -f1) bytes=$(stat -c %s final.tar.xz)"
curl -s -o /dev/null -w "final_upload_http=%{http_code}\n" -X PUT --upload-file final.tar.xz "$UPLOAD_FINAL"
# fallback: compact summaries in the log
tar -cJf - out/*.receipt.json 2>/dev/null | base64 -w 120 | sed 's/^/B64 /' | head -c 3000000
echo "end $(date -u +%FT%TZ)"
