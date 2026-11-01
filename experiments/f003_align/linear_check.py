"""Q1/Q5: compare the independent linear calculation with the frozen rows on all 2,520 cells. Usage:
  PYTHONPATH=frontier_compute/vendor:. python3 experiments/f003_align/linear_check.py ROWS.jsonl OUT.json"""
import collections, hashlib, json, sys
from scopedesk.oracles.nonlinear_sweep import ensemble as E, run as R
from experiments.f003_align import linear_indep as LI

rows_path, out_path = sys.argv[1:3]
rows = {r["id"]: r for r in map(json.loads, open(rows_path))}
cells = E.build(10)
dis, bdiff, per = [], [], []
for c in cells:
    r = rows[c["id"]]
    L, NA, NB, K = R.grid_for(c)
    s = LI.linear_summary(c["model"], c["params"], c["Dv"], L, NA, NB)
    ok = (s["verdict"] == r["linear"] and s["fastest_mode"] == r["linear_fastest_mode"] and s["n_unstable"] == r["n_unstable_linear"]
          and abs(s["sigma_fast"] - r["sigma_fast"]) <= 1e-9 * (1 + abs(s["sigma_fast"])))
    if not ok:
        dis.append({"id": c["id"], "mine": {k: s[k] for k in ("verdict", "fastest_mode", "n_unstable", "sigma_fast")},
                    "frozen": {k: r[k] for k in ("linear", "linear_fastest_mode", "n_unstable_linear", "sigma_fast")}})
    bset = s["unstable_modes_B"] != s["unstable_modes"]
    per.append({"id": c["id"], "fastest_mode": s["fastest_mode"], "unstable_modes": s["unstable_modes"], "unstable_modes_B": s["unstable_modes_B"],
                "fastest_mode_B": s["fastest_mode_B"], "B_set_differs": bset, "B_verdict_differs": bool(s["unstable_modes_B"]) != bool(s["unstable_modes"]),
                "K": K, "fastest_beyond_K": bool(s["fastest_mode"] and s["fastest_mode"] > K), "tail": s["tail_unstable_beyond_grid"],
                "cf_vs_eig": s["closed_form_vs_eigvals_maxabs"]})
    if bset:
        bdiff.append((c["model"], c["rho"], c["x"], r["category"], r["why"], bool(s["unstable_modes_B"]) != bool(s["unstable_modes"])))
tab = lambda key: dict(sorted(collections.Counter(key(b) for b in bdiff).items(), key=str))
res = {"rows_sha256": hashlib.sha256(open(rows_path, "rb").read()).hexdigest(), "n_cells": len(cells), "n_disagree_with_frozen_linear": len(dis),
       "disagreements": dis[:50], "max_closed_form_vs_eigvals": max(p["cf_vs_eig"] for p in per),
       "n_fastest_mode_beyond_IC_K": sum(p["fastest_beyond_K"] for p in per), "n_tail_unstable": sum(p["tail"] for p in per),
       "solver_B_discrete_set_differs": {"n": len(bdiff), "verdict_differs": sum(b[5] for b in bdiff), "by_rho": tab(lambda b: b[1]),
                                         "by_model": tab(lambda b: b[0]), "by_frozen_category_why": tab(lambda b: f"{b[3]}/{b[4]}")},
       "fastest_mode_B_differs": sum(1 for p in per if p["fastest_mode"] != p["fastest_mode_B"]),
       "fastest_mode_B_differs_by_rho": dict(collections.Counter(rows[p["id"]]["rho"] for p in per if p["fastest_mode"] != p["fastest_mode_B"])),
       "cells": per}
json.dump(res, open(out_path, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("cells", "disagreements")}, indent=1))
