#!/usr/bin/env python3
"""Descriptive summary of the (non-preregistered) strip factorial sweep. usage: analyze_sweep.py <sweep dir> <out json>"""
import csv, json, re, sys, statistics as st
from pathlib import Path
R, OUT = Path(sys.argv[1]), Path(sys.argv[2])
rows = []
for d in sorted(R.iterdir()):
    m = re.match(r"lam(\d+)_dir(-?1)_eps([\d.]+)_T(\d+)_r([\d.]+)", d.name)
    if not m or not (d / "xm_com.csv").exists(): continue
    rec = json.loads((d / "receipt.json").read_text())
    c = list(csv.DictReader(open(d / "xm_com.csv")))
    lam, dr, eps, T, r = int(m[1]), int(m[2]), float(m[3]), int(m[4]), float(m[5])
    dX = float(c[-1]["com_x_um"]) - float(c[0]["com_x_um"])
    ext = [float(x["extent_x_um"]) for x in c[-int(len(c) / 10):]]
    rows.append({"id": d.name, "lambda_um": lam, "dir": dr, "eps": eps, "period_min": T, "kT": 0.5 * T, "r": r, "exit": rec["exit"],
                 "dX_um": dX, "dX_per_cycle_um": dX / 10, "late_extent_range_um": max(ext) - min(ext), "com_csv_sha256": rec["com_csv_sha256"]})
iso = [x for x in rows if x["r"] == 1]
an = [x for x in rows if x["r"] > 1]
summ = {"n_runs": len(rows), "all_exit_zero": all(x["exit"] == 0 for x in rows),
        "isotropic_max_abs_dX_um": max(abs(x["dX_um"]) for x in iso), "isotropic_n": len(iso)}
# normalised displacement per cycle by (r-1)/(r+1) and eps: tests crawler-like scaling outside the 2-cell case
for x in an:
    x["norm"] = x["dX_per_cycle_um"] / (((x["r"] - 1) / (x["r"] + 1)) * x["eps"] * 16.0)
def grp(key):
    g = {}
    for x in an: g.setdefault(x[key], []).append(x["norm"])
    return {str(k): {"mean": st.mean(v), "min": min(v), "max": max(v), "n": len(v)} for k, v in sorted(g.items())}
summ["normalised_dX_per_cycle_by"] = {k: grp(k) for k in ("r", "eps", "period_min", "lambda_um")}
summ["norm_definition"] = "dX_per_cycle / ((r-1)/(r+1) * eps * r0), r0 = 16 um; equals 1 for an ideal 2-node crawler realising the full rest-length amplitude"
# direction effect
pairs = {}
for x in an:
    if x["lambda_um"] > 0: pairs.setdefault((x["lambda_um"], x["eps"], x["period_min"], x["r"]), {})[x["dir"]] = x["dX_um"]
rel = [abs(v[1] - v[-1]) / max(abs(v[1]), abs(v[-1])) for v in pairs.values() if 1 in v and -1 in v]
summ["direction_effect_rel_diff"] = {"median": st.median(rel), "max": max(rel), "n_pairs": len(rel)}
OUT.write_text(json.dumps({"schema": "claude-xenomodel.physicell-sweep/1", "preregistered": False, "scope": "descriptive sweep on a 29-cell strip, one size; not a convergence study; nominal units", "summary": summ, "runs": rows}, indent=1) + "\n")
print(json.dumps(summ, indent=1))
