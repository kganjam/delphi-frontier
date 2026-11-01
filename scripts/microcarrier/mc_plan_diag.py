#!/usr/bin/env python3
"""DIAGNOSIS of the E1 failure (mesh-3 passive creep), written after E1 failed and before E2/E3
were read. Each run changes ONE factor from E1-passive-m3-dt0.5. Not preregistered claims."""
import json
from mc_plan import run
def d(rid, dt=0.5, policy="consistent", extra=None):
    r = run(rid, "off", 3, "none", dt, passive=1, group="E1-diag", policy=policy); r["extra"] = extra or {}; return r
out = [d("D-m3-constzeta", policy="constant"),
       d("D-m3-mu0", extra={"muS": 0.0, "muK": 0.0}),
       d("D-m3-settle1", extra={"settle": 1.0}),
       d("D-m3-dt0.25", dt=0.25),
       d("D-m3-zcoll2", extra={"zetaColl": 2.0}),
       d("D-m3-cycles12", extra={"cycles": 12}),
       d("D-m2-cycles12", extra={"cycles": 12}),
       d("D-m3-nograv", extra={"gravity": 0.0})]
out[6]["mesh"] = 2; out[6]["zetaGlob"], out[6]["zetaInt"] = 0.05, 2.0
for r in out: print(json.dumps(r, sort_keys=True))
