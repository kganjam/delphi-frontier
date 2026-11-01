#!/usr/bin/env bash
# Build Voxelyze @4287e365 (FLAGS without -DPARDISO_5, as scripts/voxel_actuation/build.sh) and the parity driver.
set -euo pipefail
PIN=4287e365e11416dd108f2f361e9ec4c5a011a16c
ROOT="${1:?usage: build.sh <work-dir>}"; HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$ROOT"; cd "$ROOT"
[ -d Voxelyze ] || git clone -q https://github.com/jonhiller/Voxelyze.git Voxelyze
cd Voxelyze && git checkout -q "$PIN"; test "$(git rev-parse HEAD)" = "$PIN"
make -j1 clean >/dev/null 2>&1 || true
make -j1 FLAGS="-O3 -std=c++11 -Wall -I./include" >/dev/null
cd "$ROOT"
g++ -O2 -std=c++11 -I Voxelyze/include "$HERE/parity_actuation.cpp" -L Voxelyze/lib -lvoxelyze.0.9 -o parity_actuation
sha256sum parity_actuation
