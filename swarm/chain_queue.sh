#!/bin/bash
# Wait for the running nebius_queue to exit, THEN start the next job file.
#
# The single Nebius slot is serial. Launching a second queue while the first holds it is the error
# in claim 495: the second job sat at an opaque ADMISSION_PENDING for 861 s. Chaining keeps the slot
# continuously fed WITHOUT overlapping.
#
# THE WAIT USES scripts/wait_until_gone.sh RATHER THAN A pgrep LOOP, and that is not a style
# preference. A `pgrep -f nebius_queue.py` inside a command whose own text contains that string
# MATCHES ITSELF and waits forever -- AGENTS.md section 6b, which this repository hit six times,
# three of them AFTER the warning was written. Measured again here while writing this file: the
# first draft's control returned TWO pids for one running queue, the second being the shell command
# that was creating the script. The helper excludes its own ancestry by construction, so it is used
# instead of advice.
#
#   chain_queue.sh <next-jobs.jsonl> <logfile> [max_wait_s]
set -u
NEXT="$1"; LOG="$2"; MAXW="${3:-5400}"
WAIT=/home/ubuntu/git/morphoswarm/scripts/wait_until_gone.sh

# Write to STDOUT, not to $LOG. The launcher already redirects stdout here, and appending
# separately raced with that redirect: a chain message and a queue poll line interleaved mid-word
# and produced "nl at 2026-11-04 07:38:06 PST" in a log used for status. Harmless to the run,
# corrupting to the thing that reports on it.
"$WAIT" "swarm/nebius_queue.py" "$MAXW"
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "chain: wait_until_gone exited $rc (2 = timeout); NOT starting $NEXT"
  exit "$rc"
fi
echo "chain: slot free; starting $NEXT at $(date '+%F %T %Z')"
exec python3 -u /data/worktrees/delphi-frontier/swarm-arch/swarm/nebius_queue.py "$NEXT" --write
