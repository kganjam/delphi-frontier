#!/bin/bash
# Runner for the Evo 2 scoring job.
#
# The command lives in a FILE, not in --args. A previous submission passed
# `--args "-c" --args "<script>"`; the repeated flag collapsed, `-c` was lost,
# and bash tried to execute the script text as a filename:
#   bash: set: No such file or directory
# That cost a full image pull. One injected file has no quoting surface.
set -x
pip install -q --no-deps evo2 vtx || exit 1
pip install -q biopython huggingface_hub || exit 1
python3 /work/evo2_score_job.py \
  --payload /work/score_payload.b64 \
  --out-dir /work/out \
  --model evo2_7b \
  --budget-seconds 900 \
  --armb-seconds 0
echo "SCOREJOB_RC=$?"
