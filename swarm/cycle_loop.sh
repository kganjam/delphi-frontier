#!/bin/bash
# Runs the full swarm cycle repeatedly: gap, challenge, evaluate, questions, harvest, record,
# synthesis, the checkers, publish, progress.
#
# WHY THIS EXISTS AS A COMMITTED FILE. On 2026-11-06 the cycles had not run for six hours while
# the credit supervisor kept launching adversarial-challenge arms, so credit was being spent and
# the pipeline that moves the goal rows -- evaluate and record above all -- was not running at
# all. Nothing reported it: the check-ins described credit, not cycles. The supervisor loop had
# died from its own MAXITER arithmetic (see swarm/supervisor_loop.sh) and only it was restarted.
#
# PERIOD AND BOUND ARE STATED AGAINST EACH OTHER, which is the mistake that killed the other
# loop: its comment said "140 x 15 min = 35 h" beside a `sleep 300`.
SLEEP_S=600          # 10 minutes
MAXITER=144          # 144 x 600 s = 24 h exactly
cd /data/worktrees/delphi-frontier/swarm-arch || exit 1
for i in $(seq 1 $MAXITER); do
  echo "=== cycle $i of $MAXITER  $(date -u +%FT%TZ) ==="
  # cycle.py takes its own flock and exits 0 when another cycle holds it, so overlapping ticks
  # are safe and do not stack.
  timeout 3000 python3 swarm/cycle.py --cycles 1 --write 2>&1 | tail -40
  echo "  [cycle $i exit ${PIPESTATUS[0]}]"
  sleep "$SLEEP_S"
done
echo "=== cycle loop finished after $MAXITER iterations ==="
