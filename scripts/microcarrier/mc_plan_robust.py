#!/usr/bin/env python3
"""EXPLORATORY (not preregistered) robustness grid, written after the endpoint protocol froze
and before any actuated result was read. 12 patterns x 3 friction x 3 amplitude x 3 modulus
at mesh 1, dt 0.5, 10 Hz. Question: does the pattern ranking survive changes in the three
assumed, unmeasured parameters that matter most? No result here is a preregistered claim."""
import json
from mc_plan import run
PATS = [("A", "trav:k=1,theta=0,dir=bwd"), ("B", "trav:k=2,theta=0,dir=bwd"), ("M", "trav:k=1,theta=30,dir=fwd"),
        ("C", "seg:n=2,axis=x,mode=alt"), ("U", "uniform"), ("T05b", "trav:k=0.5,theta=0,dir=bwd"),
        ("T05f", "trav:k=0.5,theta=0,dir=fwd"), ("S4b", "seg:n=4,axis=x,mode=bwd"), ("St1", "stand:k=1,theta=0,ph0=0"),
        ("H1", "helix:k=1,m=1"), ("R1", "rsmooth:seed=1,K=4"), ("I1", "riid:seed=1")]
def plan():
  out = []
  for tag, spec in PATS:
    for mu in [0.3, 0.6, 1.0]:
        for amp in [5.0, 10.0, 15.0]:
            for E in [1e4, 2e4, 4e4]:
                r = run(f"X-{tag}-mu{mu}-amp{amp}-E{int(E)}", spec, group="robust")
                r["extra"] = {"muS": mu, "muK": round(0.8 * mu, 4), "amp": amp, "E": E}
                out.append(r)
  return out

if __name__ == "__main__":
    for r in plan():
        print(json.dumps(r, sort_keys=True))
