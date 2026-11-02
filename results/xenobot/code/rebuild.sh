#!/usr/bin/env bash
# Rebuild every published artifact from the raw run data, IN ORDER.
# Three times during this work a hand-patch to a generated file was silently
# dropped by re-running its builder. Every post-hoc addition now lives in a
# script in this chain, and this is the only supported way to regenerate.
set -euo pipefail
cd /data/scratch/designspaces/xenobot
echo "== routes";      python3 -I code/build_routes.py      | tail -2
echo "== convergence"; python3 -I code/convergence.py       > /dev/null
echo "== cargo";       python3 -I code/cargo_assemble.py    | tail -1
echo "== onset";       python3 -I code/integrate_onset.py
[ -f data/cargo-arm3c.json ] && { echo "== cohesion"; python3 -I code/integrate_cohesion.py | head -3; } || echo "== cohesion: arm not run yet, skipped"
echo "== finalise";    python3 -I code/finalise.py          | tail -4
echo "== index";       python3 -I code/build_index.py       | tail -1
echo "== figures";     for f in figures_regime figures_convergence figures_series figures_cargo; do python3 -I code/$f.py > /dev/null; done; echo "6 figures rebuilt"
echo "== verify";      python3 -I code/verify_numbers.py | tail -1
