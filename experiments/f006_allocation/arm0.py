"""F006 Arm 0 (PREREG.md Part B): allocate scarce refinement checks across the 2,520 sweep cells under a cost budget; score against
ground truth that exists for every cell. Policies read only ex-ante signals (base run at dt 0.02 to T), never outcomes.
  PYTHONPATH=frontier_compute/vendor:. python3 experiments/f006_allocation/arm0.py ANALYSIS.json SPEC_DIR BASE_DIR ROWS.jsonl OUT.json
Implementation choices fixed before any policy was scored: greedy fill in policy order, skipping a task that does not fit and continuing;
`signal` orders by Phi(zsum/sqrt(3)) / c_i, where zsum is the sum of rank-normal scores of s1, s2, s3 (higher = less settled)."""
from __future__ import annotations

import collections
import glob
import hashlib
import json
import math
import random
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm, rankdata

from scopedesk.oracles.nonlinear_sweep import ensemble as E
from scopedesk.oracles.nonlinear_sweep import run as R

BUDGETS = [0.10, 0.25]
SEEDS = 200


def main():
    an_p, spec_dir, base_dir, rows_p, out_p = sys.argv[1:6]
    an = json.load(open(an_p))
    rows = {r["id"]: r for r in map(json.loads, open(rows_p))}
    base = {}
    for f in glob.glob(f"{base_dir}/*.jsonl"):
        for l in open(f):
            r = json.loads(l)
            base[r["id"]] = r
    cells = {c["id"]: c for c in E.build(10)}
    ids = sorted(cells)
    # ex-ante cost and signals
    cost, s1, s2, s3 = {}, {}, {}, {}
    for f in glob.glob(f"{spec_dir}/*.npz"):
        z = np.load(f)
        for k in z.files:
            if not k.startswith("spec_"):
                continue
            i = int(k[5:])
            sp = z[k].astype(float)[-1][1:]
            top = np.sort(sp)[::-1]
            s1[i] = float(top[1] / top[0]) if top[0] > 0 else 0.0
            a = z[f"std_{i}"].astype(float)
            j = int(round(0.9 * (len(a) - 1)))
            s2[i] = float(abs(a[-1] - a[j]) / max(a[-1], 1e-300))
    for i in ids:
        L, NA, NB, K = R.grid_for(cells[i])
        cost[i] = NA * rows[i]["T"] / 0.02          # horizon rule of the frozen sweep: known before any run
        d = base.get(i, {}).get("dudt_inf_T")
        s3[i] = float(d) if d is not None else float("inf")
        s1.setdefault(i, 1.0); s2.setdefault(i, float("inf"))      # diverged cells: maximally unsettled signals
    zsum = {}
    for s in (s1, s2, s3):
        v = np.array([s[i] for i in ids]); zz = norm.ppf((rankdata(v) - 0.5) / len(v))
        for i, x in zip(ids, zz):
            zsum[i] = zsum.get(i, 0.0) + float(x)
    pc = an["per_cell"]
    pos = {i: (pc[str(i)]["step"] == "step_sensitive" or pc[str(i)]["horizon"] == "horizon_changed") for i in ids}

    def in_numerator(i):
        r = rows[i]
        if r["category"] == "unresolved":
            return True
        if r["linear"] == "out_of_scope" and r["category"] == "pattern":
            return True
        if r["linear"] == "applies" and r["category"] == "no_pattern":
            return True
        return r["linear"] == "applies" and r["category"] == "pattern" and r["A"]["mode"] != r["linear_fastest_mode"]
    dec = {i: pos[i] and in_numerator(i) for i in ids}
    strata = {i: (cells[i]["model"], cells[i]["rho"], cells[i]["eps"]) for i in ids}
    n_strata = len(set(strata.values()))
    total = sum(cost.values())

    def fill(order, B, chosen=None):
        chosen = list(chosen or []); used = sum(cost[i] for i in chosen); seen = set(chosen)
        for i in order:
            if i in seen:
                continue
            if used + cost[i] <= B:
                chosen.append(i); used += cost[i]; seen.add(i)
        return chosen

    def score(ch):
        c = sum(cost[i] for i in ch)
        p = sum(pos[i] for i in ch); d = sum(dec[i] for i in ch)
        return {"n_checked": len(ch), "cost_cellsteps": c, "positives": p, "decision_positives": d,
                "positives_per_1e9": p / c * 1e9 if c else 0.0, "decision_positives_per_1e9": d / c * 1e9 if c else 0.0,
                "coverage_strata": len({strata[i] for i in ch}) / n_strata, "negative_checks": len(ch) - p,
                "negative_cost_cellsteps": sum(cost[i] for i in ch if not pos[i])}

    def stratified_order(rng):
        by = collections.defaultdict(list)
        for i in ids:
            by[strata[i]].append(i)
        keys = sorted(by); rng.shuffle(keys)
        for k in keys:
            rng.shuffle(by[k])
        out = []
        while any(by.values()):
            for k in keys:
                if by[k]:
                    out.append(by[k].pop())
        return out

    expert = sorted(ids, key=lambda i: (abs(cells[i]["rho"] - 1), cells[i]["model"] != "brusselator", cells[i]["eps"], i))
    cheapest = sorted(ids, key=lambda i: (cost[i], i))
    sig = sorted(ids, key=lambda i: (-norm.cdf(zsum[i] / math.sqrt(3)) / cost[i], i))
    res = {"inputs": {"analysis_sha256": hashlib.sha256(Path(an_p).read_bytes()).hexdigest(), "arm0_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
           "pool": {"n_tasks": len(ids), "total_cost_cellsteps": total, "n_positive": sum(pos.values()), "n_decision_positive": sum(dec.values()),
                    "n_strata": n_strata, "positive_by_kind": {"step_sensitive": sum(pc[str(i)]["step"] == "step_sensitive" for i in ids),
                                                               "horizon_changed": sum(pc[str(i)]["horizon"] == "horizon_changed" for i in ids)}},
           "budgets": {}}
    for bf in BUDGETS:
        B = bf * total
        rb = {"expert": score(fill(expert, B)), "cheapest": score(fill(cheapest, B)), "signal": score(fill(sig, B))}
        for name, mk in (("uniform", lambda rng: rng.sample(ids, len(ids))), ("stratified", stratified_order)):
            runs = [score(fill(mk(random.Random(1000 + s)), B)) for s in range(SEEDS)]
            rb[name] = {k: {"median": statistics.median(r[k] for r in runs), "p05": float(np.percentile([r[k] for r in runs], 5)),
                            "p95": float(np.percentile([r[k] for r in runs], 95))} for k in runs[0]}
        runs = []
        for s in range(SEEDS):
            floor = fill(stratified_order(random.Random(5000 + s)), 0.2 * B)
            runs.append(score(fill(sig, B, chosen=floor)))
        rb["signal+floor"] = {k: {"median": statistics.median(r[k] for r in runs), "p05": float(np.percentile([r[k] for r in runs], 5)),
                                  "p95": float(np.percentile([r[k] for r in runs], 95))} for k in runs[0]}
        rb["oracle_upper_bound"] = score(fill(sorted(ids, key=lambda i: (-pos[i] / cost[i], i)), B))
        res["budgets"][str(bf)] = rb
    json.dump(res, open(out_p, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
