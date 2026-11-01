#!/bin/bash
# Nebius job wrapper for organ-sims runs (claude-organ). Usage inside the container:
#   bash /work/run_job.sh <commit_sha> <run_id> <module> [args...]
# Clones the public branch sparsely at the pinned commit (refuses any other HEAD), installs pinned packages, runs the
# module under `timeout`, then prints the run directory + logs as a gzip tarball in base64 between markers with its sha256.
set -uo pipefail
SHA="$1"; RID="$2"; MOD="$3"; shift 3
echo "ORGAN-JOB start $(date -u +%FT%TZ) sha=$SHA rid=$RID mod=$MOD args=$*"
nproc; python3 --version
cd /tmp && git clone -q --filter=blob:none --no-checkout https://github.com/kganjam/delphi-frontier.git repo && cd repo || exit 20
# non-cone sparse set: every input any organ-sims module reads (a1 of r6 failed on a missing r3-daane input)
git sparse-checkout set --no-cone '/engineering/' '/artifacts/organ-sims/' '/artifacts/glider/r4-daane-printfix/' '/artifacts/glider/r3-daane/*.json' \
  '/artifacts/cfd3d/vlm/' '/artifacts/fish3d/fish3d-v3a-fan/' '/artifacts/fish3d/fish3d-v3b-glide-pose/panels.json' \
  '/artifacts/fish3d/fish3d-v3c-daane-length/*.json' '/artifacts/aeroelastic/protocol.json' '/artifacts/scales/erk-wave/receipt.json' || exit 21
git checkout -q "$SHA" || exit 22
[ "$(git rev-parse HEAD)" = "$SHA" ] || { echo "HEAD mismatch"; exit 23; }
python3 -m pip install -q --no-cache-dir numpy==2.2.6 matplotlib==3.10.3 pybullet==3.2.7 manifold3d==3.5.4 trimesh==5.2.0 2>&1 | tail -2
python3 -c "import numpy, matplotlib, pybullet; print('pkgs', numpy.__version__, matplotlib.__version__)"
mkdir -p artifacts/organ-sims/logs
T0=$(date +%s)
OMP_NUM_THREADS=1 PYTHONPATH=. timeout 6600 python3 -m "$MOD" "$@" > "artifacts/organ-sims/logs/$RID.log" 2>&1
RC=$?
echo "ORGAN-JOB science rc=$RC wall_s=$(( $(date +%s) - T0 ))"
tail -5 "artifacts/organ-sims/logs/$RID.log"
printf '{"rc": %d, "sha": "%s", "rid": "%s", "module": "%s", "args": "%s", "end_utc": "%s", "nproc": %d}\n' "$RC" "$SHA" "$RID" "$MOD" "$*" "$(date -u +%FT%TZ)" "$(nproc)" > "artifacts/organ-sims/logs/$RID.job.json"
tar czf /tmp/out.tgz "artifacts/organ-sims/$RID" "artifacts/organ-sims/logs/$RID.log" "artifacts/organ-sims/logs/$RID.job.json" 2>/dev/null
echo "ORGAN-OUT-BEGIN sha256=$(sha256sum /tmp/out.tgz | cut -d' ' -f1) bytes=$(stat -c %s /tmp/out.tgz)"
base64 -w 120 /tmp/out.tgz
echo "ORGAN-OUT-END"
exit $RC
