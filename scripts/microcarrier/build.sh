#!/usr/bin/env bash
# Build Voxelyze at its pin and the microcarrier runner. Nothing installed system-wide.
# Upstream: https://github.com/jonhiller/Voxelyze @ 4287e365e11416dd108f2f361e9ec4c5a011a16c
# Licence: LGPL-3.0-or-later per source headers (no LICENSE file at that commit).
# The default makefile FLAGS contain -DPARDISO_5=1 (undefined pardiso symbols at link); we override.
# -ffp-contract=off: no FMA contraction, so results do not depend on the host's FMA support.
set -euo pipefail
PIN=4287e365e11416dd108f2f361e9ec4c5a011a16c
ROOT="${1:?usage: build.sh <work-dir> [voxelyze-src-tarball]}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FL="-O3 -ffp-contract=off -fno-fast-math -std=c++11"
mkdir -p "$ROOT"; cd "$ROOT"
if [ -n "${2:-}" ]; then mkdir -p Voxelyze && tar -xf "$2" -C Voxelyze;
else [ -d Voxelyze ] || git clone -q https://github.com/jonhiller/Voxelyze.git Voxelyze
     (cd Voxelyze && git checkout -q "$PIN" && test "$(git rev-parse HEAD)" = "$PIN"); fi
make -C Voxelyze -j"$(nproc)" FLAGS="$FL -Wall -I./include" >/dev/null
g++ $FL -I Voxelyze/include "$HERE/mc_runner.cpp" -L Voxelyze/lib -lvoxelyze.0.9 -o mc_runner
echo "built $ROOT/mc_runner"
