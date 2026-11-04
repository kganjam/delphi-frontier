#!/bin/bash
# Keeps the swarm SATURATED.
#
# The previous version only CONSUMED a fixed frontier of 19 subproblems. It ran dry in five hours
# and then politely polled an empty queue while ~$928 of expiring credit sat unused. A loop that
# cannot create work is a batch job with a cron, not a swarm. It now GENERATES work every pass.
#
# Bounded by a deadline and an iteration cap, never by a condition something else must produce:
# an `until` loop waiting on a log whose producer has died waits forever, which is how fourteen
# watchers held a goal open for seventeen hours on 2026-11-03.
DEADLINE=${DEADLINE:-$(date -d '2026-11-04 23:45 PST' +%s)}
TARGET=${TARGET:-40}          # concurrent cloud sessions to hold open
MAXITER=${MAXITER:-900}
SLEEP=${SLEEP:-180}
LOG=/data/swarm/monitor.log
cd /data/swarm || exit 1
for i in $(seq 1 "$MAXITER"); do
  now=$(date +%s)
  if [ "$now" -ge "$DEADLINE" ]; then echo "$(date '+%F %T %Z') DEADLINE reached, stopping" >> "$LOG"; break; fi
  left=$(( (DEADLINE - now) / 60 ))
  echo "=== $(date '+%F %T %Z')  iter $i  ${left} min to credit expiry ===" >> "$LOG"
  timeout 900  python3 /data/swarm/swarm.py poll          >> "$LOG" 2>&1; echo "POLL-EXIT=$?" >> "$LOG"
  timeout 1800 python3 /data/swarm/generate.py "$TARGET"  >> "$LOG" 2>&1; echo "GEN-EXIT=$?"  >> "$LOG"
  timeout 600  python3 /data/swarm/swarm.py loop "$TARGET" >> "$LOG" 2>&1; echo "LOOP-EXIT=$?" >> "$LOG"
  timeout 300  orchestra cloud credit 2>/dev/null | grep usable >> "$LOG"
  sleep "$SLEEP"
done
echo "$(date '+%F %T %Z') monitor finished after $i iterations" >> "$LOG"
