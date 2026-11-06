#!/bin/bash
# Kill processes matching a pattern WITHOUT killing the caller.
#
# WHY THIS EXISTS: `pkill -f foo` matches any command line containing "foo" -- including the
# shell that is running the pkill, because that shell's own command line contains the pattern.
# The caller dies with exit 144 and the target often survives. This happened three times in one
# session, on a trap already written down, because the fix was "remember not to" rather than a
# command to reach for.
#
# It excludes: this script, its own pid, its parent, and anything whose command line mentions
# this script's path. An ancestry walk alone is NOT enough -- process substitution creates a
# child whose /proc/<pid>/cmdline is the caller's.
#
#   bash swarm/killpat.sh 'swarm/api_challenge.py'        # report what would be killed
#   bash swarm/killpat.sh 'swarm/api_challenge.py' --kill
set -u
PAT="${1:?usage: killpat.sh PATTERN [--kill]}"
DO_KILL="${2:-}"
SELF="$(basename "$0")"
ME=$$
PARENT=$PPID

mapfile -t HITS < <(
  ps -eo pid=,args= | while read -r pid args; do
    case "$pid" in "$ME"|"$PARENT") continue;; esac
    case "$args" in *"$SELF"*) continue;; esac
    case "$args" in *"$PAT"*) printf '%s\t%s\n' "$pid" "$args";; esac
  done
)

if [ "${#HITS[@]}" -eq 0 ]; then
  echo "  no process matches: $PAT"
  exit 0
fi
printf '  %d match(es) for %s\n' "${#HITS[@]}" "$PAT"
for h in "${HITS[@]}"; do printf '    %s\n' "${h:0:140}"; done
if [ "$DO_KILL" != "--kill" ]; then
  echo "  dry run; pass --kill to terminate"
  exit 0
fi
for h in "${HITS[@]}"; do kill "${h%%	*}" 2>/dev/null; done
sleep 2
alive=0
for h in "${HITS[@]}"; do kill -0 "${h%%	*}" 2>/dev/null && alive=$((alive+1)); done
echo "  killed; $alive still alive"
echo "  caller (pid $ME) survived"
