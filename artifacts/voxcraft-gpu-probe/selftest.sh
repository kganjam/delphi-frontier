#!/usr/bin/env bash
# Controls for run_probe.sh itself. Runs on ANY host, GPU or not: every fixture below
# exercises a path that completes before a GPU is needed. A probe whose own failure
# handling has not been tested is not evidence.
#
# F1 first-failure excerpt     the receipt must carry the EXACT first-failure text
# F2 return archive            no self-member, extracts cleanly, failed receipt still written
# F3 outer deadline            a tiny HARD_DEADLINE_S must return DEADLINE_EXCEEDED ...
# F4 deadline negative control ... and the normal bound must NOT return it
# F5 env allow-list            a planted secret-looking variable must NOT be recorded ...
# F6 env allow-list positive   ... while an allow-listed variable must be
# F7 immutable science output   an oversized native history stays byte-identical, the run
#                               reports a transport failure and CANNOT exit 0
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="${1:-$(mktemp -d)}"; mkdir -p "$T"; PASS=0; FAIL=0
ok(){ printf '  PASS  %s\n' "$1"; PASS=$((PASS+1)); }
no(){ printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL+1)); }
jget(){ python3 -c "import json,sys;d=json.load(open(sys.argv[1]));v=d
for k in sys.argv[2].split('.'):v=v.get(k) if isinstance(v,dict) else None
print(v if v is not None else '')" "$1" "$2" 2>/dev/null; }

echo "F1/F2: run to a controlled failure, then inspect the receipt and the archive"
W="$T/f1"; rm -rf "$W"
CUDA_VERSION="12.9.0-selftest" NVIDIA_SELFTEST_TOKEN="sk-must-not-appear" CUDA_API_KEY="must-not-appear" \
  bash "$HERE/run_probe.sh" "$W" > "$T/f1.out" 2>&1
RC=$?
grep -q "PROBE-STATUS=" "$T/f1.out" && ok "runner emitted a status line" || no "no status line"
R="$W/out/receipt.json"
[ -f "$R" ] && ok "receipt written on failure" || no "no receipt"
ST=$(jget "$R" status); echo "        status=$ST rc=$RC"

# F1: the excerpt must be non-empty AND must contain the exact text from the first-failure file.
EX=$(python3 -c "import json;print(json.load(open('$R')).get('first_failure_excerpt',''))" 2>/dev/null)
if [ -n "$EX" ]; then ok "first_failure_excerpt is non-empty"; else no "first_failure_excerpt is EMPTY (the export-order bug)"; fi
FF=$(jget "$R" first_failure_file); echo "        first_failure_file=$FF"
if [ -n "$FF" ] && [ -f "$W/logs/$FF" ]; then
  if python3 - "$R" "$W/logs/$FF" <<'PY'
import json,sys
ex=json.load(open(sys.argv[1]))["first_failure_excerpt"]
head=open(sys.argv[2],errors="replace").read(4000)
sys.exit(0 if ex==head else 1)
PY
  then ok "excerpt is byte-exact against the first-failure file"; else no "excerpt does not match the file"; fi
else no "first_failure_file missing or not on disk"; fi

# F2: archive hygiene
A="$W/probe-return.tar.gz"
[ -f "$A" ] && ok "return archive exists" || no "no return archive"
SELF=$(tar tzf "$A" 2>/dev/null | grep -c 'probe-return.tar.gz')
[ "$SELF" = 0 ] && ok "archive contains NO self-member" || no "archive embeds itself ($SELF)"
rm -rf "$T/ex"; mkdir -p "$T/ex"
if tar xzf "$A" -C "$T/ex" 2>"$T/ex.err"; then ok "archive extracts cleanly (exit 0)"; else no "extraction failed: $(head -1 "$T/ex.err")"; fi
[ -f "$T/ex/out/receipt.json" ] && ok "extracted archive carries the failed receipt" || no "receipt missing from archive"
[ "$(jget "$T/ex/out/receipt.json" status)" = "$ST" ] && ok "receipt inside archive matches the on-disk status" || no "status mismatch inside archive"
B=$(stat -c%s "$A" 2>/dev/null || echo 0)
[ "$B" -le $((16*1024*1024)) ] && ok "return is within the 16 MiB cap ($B bytes)" || no "return exceeds 16 MiB ($B)"

echo "F5/F6: environment capture policy"
PF="$W/logs/00-preflight.txt"
if grep -qE 'sk-must-not-appear|NVIDIA_SELFTEST_TOKEN|CUDA_API_KEY' "$PF" 2>/dev/null; then
  no "a planted secret-looking variable LEAKED into the preflight log"
else ok "planted NVIDIA_*/CUDA_* secret-looking variables are NOT recorded"; fi
if grep -q 'CUDA_VERSION=12.9.0-selftest' "$PF" 2>/dev/null; then
  ok "allow-listed CUDA_VERSION IS recorded (so the capture is not simply empty)"
else no "allow-listed variable missing: the negative above would be vacuous"; fi

echo "F3: outer deadline fires"
W2="$T/f3"; rm -rf "$W2"
HARD_DEADLINE_S=20 bash "$HERE/run_probe.sh" "$W2" > "$T/f3.out" 2>&1
S2=$(jget "$W2/out/receipt.json" status)
[ "$S2" = "DEADLINE_EXCEEDED" ] && ok "tiny outer bound returns DEADLINE_EXCEEDED" || no "expected DEADLINE_EXCEEDED, got '$S2'"
[ -f "$W2/probe-return.tar.gz" ] && ok "partial logs are still packed on a deadline" || no "no archive on deadline"

echo "F4: deadline negative control"
[ "$ST" != "DEADLINE_EXCEEDED" ] && ok "normal 900s bound does NOT report DEADLINE_EXCEEDED (got $ST)" \
  || no "deadline fired spuriously at the normal bound"

echo "F7: oversized native history must stay byte-identical and must not pass"
W3="$T/f7"; rm -rf "$W3"; mkdir -p "$W3/out"
# plant a history larger than the cap we will impose, and remember its exact bytes
head -c 300000 /dev/urandom > "$W3/out/actuated.history"
BEFORE=$(sha256sum "$W3/out/actuated.history" | cut -d' ' -f1)
BEFORE_B=$(stat -c%s "$W3/out/actuated.history")
RETURN_MAX_BYTES_OVERRIDE=1 bash -c '
  sed "s/^RETURN_MAX_BYTES=.*/RETURN_MAX_BYTES=1024/" "'"$HERE"'/run_probe.sh" > "'"$T"'/tiny_cap_probe.sh"
  chmod +x "'"$T"'/tiny_cap_probe.sh"'
bash "$T/tiny_cap_probe.sh" "$W3" > "$T/f7.out" 2>&1; RC7=$?
AFTER=$(sha256sum "$W3/out/actuated.history" | cut -d' ' -f1)
AFTER_B=$(stat -c%s "$W3/out/actuated.history")
[ "$BEFORE" = "$AFTER" ] && ok "native history is byte-identical after the run ($BEFORE_B bytes)" \
  || no "NATIVE HISTORY WAS MUTATED ($BEFORE_B -> $AFTER_B bytes)"
TR=$(python3 -c "import json;print(json.load(open('$W3/out/receipt.json'))['transport']['status'])" 2>/dev/null)
case "$TR" in RETURN_TOO_LARGE*) ok "transport failure reported explicitly ($TR)";;
  *) no "expected RETURN_TOO_LARGE*, got '$TR'";; esac
[ "$RC7" -ne 0 ] && ok "oversized return exits non-zero (rc=$RC7)" || no "exited 0 despite a transport failure"
MUT=$(python3 -c "import json;print(json.load(open('$W3/out/receipt.json'))['transport']['scientific_output_mutated'])" 2>/dev/null)
[ "$MUT" = "False" ] && ok "receipt records scientific_output_mutated=False" || no "receipt says mutated=$MUT"
if grep -q "originals in .* are untouched" "$T/f7.out"; then ok "operator is told the originals are intact"; else no "no originals-intact message"; fi

echo
echo "SELFTEST: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
