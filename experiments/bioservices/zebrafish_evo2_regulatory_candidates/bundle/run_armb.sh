#!/bin/bash
# Arm B: few-shot in-context generation, then scoring of what it produced.
#
# The command lives in a FILE because repeated --args does not accumulate on
# this CLI: `--args "-c" --args "<script>"` silently drops the -c and bash then
# tries to execute the script text as a filename. One injected file, one --args.
#
# --armb-seconds is a deadline, not a target. The job writes candidates
# incrementally and stops cleanly when it expires, so a short pull still yields
# usable output instead of nothing.
set -x
pip install -q --no-deps evo2 vtx || exit 1
pip install -q biopython huggingface_hub || exit 1
python3 /work/evo2_score_job.py \
  --payload /work/score_payload.b64 \
  --out-dir /work/out \
  --model evo2_7b \
  --budget-seconds 1500 \
  --armb-seconds 800
echo "SCOREJOB_RC=$?"
