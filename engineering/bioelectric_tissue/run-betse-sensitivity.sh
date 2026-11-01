#!/usr/bin/env bash
set -euo pipefail

ROOT=/work/frontier
SOURCE="$ROOT/src"
VENV="$ROOT/betse-venv"
WORK="$ROOT/betse-work"

test -n "${COPS_OUT:-}"
test -n "${FRONTIER_SOURCE_COMMIT:-}"
test -n "${FRONTIER_SOURCE_ARCHIVE_SHA256:-}"
mkdir -p "$COPS_OUT" "$WORK"

if ! command -v ffmpeg >/dev/null 2>&1; then
  apt-get update
  apt-get install -y --no-install-recommends ffmpeg
fi

python3.12 -m venv "$VENV"
"$VENV/bin/python" -m pip install --disable-pip-version-check --no-input \
  --requirement "$SOURCE/engineering/bioelectric_tissue/requirements-betse.txt"

"$VENV/bin/python" -m engineering.bioelectric_tissue.sensitivity \
  --betse-python "$VENV/bin/python" --work "$WORK/preflight" --preflight

exec "$VENV/bin/python" -m engineering.bioelectric_tissue.sensitivity \
  --betse-python "$VENV/bin/python" --work "$WORK/runs" --out "$COPS_OUT" \
  --source-commit "$FRONTIER_SOURCE_COMMIT"
