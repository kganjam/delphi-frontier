#!/bin/sh
set -eu
: "${CHROMIUM_BIN:?Set CHROMIUM_BIN to an installed Chromium/Chrome executable}"
cap="${CHROMIUM_MEMORY_MIB:-1536}"
case "$cap" in ''|*[!0-9]*) echo 'CHROMIUM_MEMORY_MIB must be a positive integer' >&2; exit 2;; esac
if [ "$cap" -lt 256 ]; then echo 'CHROMIUM_MEMORY_MIB must be at least 256' >&2; exit 2; fi
case "$(uname -s)" in
  Darwin) exec /usr/bin/taskpolicy -m "$cap" "$CHROMIUM_BIN" "$@" ;;
  Linux)
    # The scope covers this Chromium process and its descendants.
    exec systemd-run --user --scope --quiet -p "MemoryMax=${cap}M" -p MemorySwapMax=0 -p TasksMax=64 -p RuntimeMaxSec=300 "$CHROMIUM_BIN" "$@"
    ;;
  *) echo 'No memory/task cap configured for this platform; refusing browser launch.' >&2; exit 2 ;;
esac
