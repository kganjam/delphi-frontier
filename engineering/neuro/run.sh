#!/usr/bin/env bash
# Capped run of one engineering.neuro model; writes artifacts/neuro/<rid>/run_receipt.json with the exit code.
# usage: engineering/neuro/run.sh <module> <rid> [args...]
set -u
mod=$1; rid=$2; shift 2
cd "$(dirname "$0")/../.."
mkdir -p artifacts/neuro/$rid
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg TZ=America/Los_Angeles \
  systemd-run --user --scope --quiet -p TasksMax=256 -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=1800 \
  /home/ubuntu/miniconda3/bin/python -m engineering.neuro.$mod "$@" > artifacts/neuro/$rid/stdout.log 2> artifacts/neuro/$rid/stderr.log
code=$?
end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 - "$rid" "$mod" "$code" "$start" "$end" "$*" <<'PY'
import json,sys,hashlib,pathlib
rid,mod,code,s,e,args=sys.argv[1:]
d=pathlib.Path("artifacts/neuro")/rid
m=d/"manifest.json"
r={"command":f"engineering/neuro/run.sh {mod} {rid} {args}".strip(),"python_module":f"engineering.neuro.{mod}","exit_code":int(code),
   "start_utc":s,"end_utc":e,"caps":"systemd-run --user --scope TasksMax=256 MemoryMax=6G MemorySwapMax=0 RuntimeMaxSec=1800; OMP_NUM_THREADS=1",
   "manifest_sha256":hashlib.sha256(m.read_bytes()).hexdigest() if m.exists() else None}
(d/"run_receipt.json").write_text(json.dumps(r,indent=1))
print(json.dumps(r))
PY
exit $code
