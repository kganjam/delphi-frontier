#!/bin/bash
# Keeps the swarm fed and records what it is doing. BOUNDED: it stops at the deadline or the iteration
# cap, never on a condition that something else has to produce -- an `until` loop whose producer dies
# waits forever, which is how 14 watchers held a goal open for 17 hours on 2026-11-03.
DEADLINE=${DEADLINE:-$(date -d '2026-11-04 23:50 PST' +%s)}   # cloud credit expiry
MAXITER=${MAXITER:-400}
SLEEP=${SLEEP:-300}
LOG=/data/swarm/monitor.log
cd /data/swarm || exit 1
for i in $(seq 1 "$MAXITER"); do
  now=$(date +%s)
  if [ "$now" -ge "$DEADLINE" ]; then echo "$(date '+%F %T %Z') DEADLINE reached, stopping" >> $LOG; break; fi
  left=$(( (DEADLINE - now) / 60 ))
  echo "=== $(date '+%F %T %Z')  iter $i/$MAXITER  ${left} min to credit expiry ===" >> $LOG
  timeout 1500 python3 /data/swarm/swarm.py loop 12 >> $LOG 2>&1
  echo "LOOP-EXIT=$?" >> $LOG
  timeout 300 python3 /data/swarm/swarm.py status >> $LOG 2>&1
  sleep "$SLEEP"
done
echo "$(date '+%F %T %Z') monitor finished after $i iterations" >> $LOG
