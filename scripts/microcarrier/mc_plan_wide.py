#!/usr/bin/env python3
"""EXPLORATORY (not preregistered), written after the endpoint freeze and before any E2/E3 or sweep
result was read. (1) A population of 800 smooth random phase fields (seeds 81-880, equal L2 budget):
what fraction of random contraction patterns produce net motion, and how large? (2) Frictionless
controls (muS = muK = 0) for 12 patterns: with isotropic absolute-frame damping and no horizontal
contact force, the COM cannot translate horizontally (a theorem being formalised by claude-xenomodel);
any motion above numerical tolerance would falsify that prediction for this engine."""
import json
from mc_plan import run
from mc_plan_robust import PATS
out = [run(f"W-rsmooth-{s}", f"rsmooth:seed={s},K=4", group="wide-random") for s in range(81, 881)]
for tag, spec in PATS:
    r = run(f"W-mu0-{tag}", spec, group="wide-mu0"); r["extra"] = {"muS": 0.0, "muK": 0.0}; out.append(r)
for r in out:
    print(json.dumps(r, sort_keys=True))
