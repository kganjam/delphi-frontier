#!/bin/bash
# collect.sh <aijob-id>: fetch log parts, install runs under results/xenomorph/runs, post-hoc metrics, verdicts.
# Run from the repo root with .venv-xm. Large raw logs stay outside the repo (scratch), only receipts are kept.
set -u
J=$1
PY=${PY:-.venv-xm/bin/python}
SCR=${SCR:-/tmp/xenomorph-collect}
mkdir -p $SCR/$J results/xenomorph/nebius/$J results/xenomorph/runs
if [ ! -s $SCR/$J/full.log ]; then
  python3 engineering/xenomorph/nebius/dump_log.py $J ${SINCE:?set SINCE} ${UNTIL:?set UNTIL} $SCR/$J/full.log
fi
python3 engineering/xenomorph/nebius/fetch_parts.py $J $SCR/$J $SCR/$J/full.log
python3 - "$SCR/$J" "results/xenomorph/nebius/$J" <<'PY'
import hashlib, json, sys, pathlib
src, dst = map(pathlib.Path, sys.argv[1:])
r = json.loads((src / "fetch_receipt.json").read_text())
log = (src / "job.log.txt").read_bytes()
r["job_log_sha256"] = hashlib.sha256(log).hexdigest(); r["job_log_bytes"] = len(log)
r["job_log_note"] = "raw log (base64 parts) not committed; decoded parts are under results/xenomorph/runs and results/xenomorph/sweeps"
(dst / "fetch_receipt.json").write_text(json.dumps(r, indent=1) + "\n")
PY
for d in $SCR/$J/parts/*-x*; do
  [ -d "$d" ] || continue
  n=$(basename $d)
  rm -rf results/xenomorph/runs/$n && cp -r $d results/xenomorph/runs/$n
  OMP_NUM_THREADS=1 $PY -m engineering.xenomorph.posthoc results/xenomorph/runs/$n > /dev/null || echo "posthoc failed $n"
done
if [ -d $SCR/$J/parts/sweepret ]; then
  name=$(grep -q sizesweep $SCR/$J/fetch_receipt.json && echo size || echo main)
  mkdir -p results/xenomorph/sweeps/$name && cp -r $SCR/$J/parts/sweepret/* results/xenomorph/sweeps/$name/
fi
ls results/xenomorph/runs
