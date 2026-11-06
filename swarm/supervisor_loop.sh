#!/bin/bash
# Credit supervisor heartbeat. Bounded: exits after MAXITER cycles so it cannot outlive the
# credit window it exists to serve. Each cycle is one supervisor run plus a sleep.
#
# COMMITTED 2026-11-06 BECAUSE IT DIED SILENTLY AND LIVED ONLY IN /tmp. MAXITER was 140 with a
# comment reading "140 x 15 min = 35 h, just past the api_outlook2 expiry", while the sleep
# below is 300 seconds. 140 x 5 min is 11.7 h, so the loop exited at 03:00 UTC after starting
# at 15:07, and took the credit-spending arms with it: burn went from ~$16/h to $0.00/h and
# nothing reported it. The check-ins kept being written until the same moment, so the record
# showed a healthy loop right up to the point it stopped existing.
#
# KEEP THE ARITHMETIC NEXT TO THE SLEEP. The two numbers were 23 lines apart and disagreed by
# a factor of three. swarm/credit_trajectory.py is the independent check: it reads the
# check-in history and reports IDLE when a spendable tenant stops draining.
cd /data/worktrees/delphi-frontier/swarm-arch || exit 1
MAXITER=288          # 288 x 5 min (the sleep below) = 24 h. The previous value said "140 x 15 min = 35 h" while sleeping 300s, so it ran 11.7 h and died silently at 03:00 UTC on 2026-11-06, taking the credit-spending arms with it.
for i in $(seq 1 $MAXITER); do
  echo "=== cycle $i  $(date -u +%FT%TZ) ==="
  timeout 600 python3 swarm/credit_supervisor.py 2>&1
  if [ $((i % 4)) -eq 1 ]; then
    echo "--- goal status (every 4th cycle, ~1h) ---"
    STAMP=$(date -u +%Y%m%dT%H%M%SZ)
    OUT="results/checkins/goal-${STAMP}.txt"
    { echo "# automated check-in, $STAMP UTC, heartbeat cycle $i"
      echo "# written by ms-supervisor-loop.sh; no human composed this file"
      timeout 600 python3 swarm/goal_status.py 2>&1
      echo
      echo "--- credit at this check-in ---"
      timeout 240 orchestra api-credits list 2>&1 | head -6
    } > "$OUT" 2>&1
    tail -30 "$OUT"
    echo "  [written to $OUT]"
  fi
  sleep 300
done
echo "=== supervisor loop finished after $MAXITER cycles ==="
