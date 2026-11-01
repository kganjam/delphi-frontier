"""Evaluate the frozen gates (protocol.json + addendum 1) on collected runs and summarise the off-lattice sweep.

  python -m engineering.xenomorph.report --runs results/xenomorph/runs --out results/xenomorph
Writes verdicts.json and offlattice_summary.json (if sweep trajectories are present) under --out.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(runs: Path):
    out = []
    for m in sorted(runs.glob("*/metrics.json")):
        d = json.loads(m.read_text())
        d["name"] = m.parent.name
        d["cc"] = "cc-" in m.parent.name
        ex = m.parent / "exit.txt"
        d["exit"] = ex.read_text().strip() if ex.exists() else None
        ph = m.parent / "posthoc.json"
        d["posthoc"] = json.loads(ph.read_text())["rows"] if ph.exists() else None
        out.append(d)
    return out


def gates(group: dict) -> dict:
    """group: arm -> list of runs (same scale, same cc flag)."""
    res = {}
    first = lambda d: d["rows"][0]  # noqa: E731
    last = lambda d: d["rows"][-1]  # noqa: E731
    z = group.get("zero", [])
    if z:
        per = [{"seed": d["seed"], "rg0": first(d)["rg_norm"], "rg_end": last(d)["rg_norm"],
                "ratio": round(last(d)["rg_norm"] / first(d)["rg_norm"], 4),
                "lcf_end_reported_not_gated": last(d)["largest_cluster_fraction"]} for d in z]
        res["zero_adhesion"] = {"rule": "final rg_norm >= 0.95 * initial in every seed", "per_seed": per,
                                "pass": all(p["ratio"] >= 0.95 for p in per)}
    e = group.get("equal", [])
    if e:
        cs = [last(d)["core_shell_index"] for d in e]
        hs = [last(d)["sorting_index_homotypic"] for d in e]
        res["equal_adhesion"] = {"rule": "|mean final core_shell| < 0.1 AND mean final homotypic < 0.60",
                                 "core_shell_final": cs, "homotypic_final": hs,
                                 "mean_core_shell": round(float(np.mean(cs)), 4), "mean_homotypic": round(float(np.mean(hs)), 4),
                                 "pass": abs(float(np.mean(cs))) < 0.1 and float(np.mean(hs)) < 0.60}
    for arm in ("dah", "equal"):
        g = group.get(arm, [])
        if g:
            per = [{"seed": d["seed"], "lcf_end": last(d)["largest_cluster_fraction"],
                    "rg_drop": round(1 - last(d)["rg_norm"] / first(d)["rg_norm"], 4)} for d in g]
            res[f"{arm}_compaction"] = {"rule": "final largest_cluster_fraction >= 0.9 AND rg_norm drop >= 20% in every seed",
                                        "per_seed": per, "pass": all(p["lcf_end"] >= 0.9 and p["rg_drop"] >= 0.20 for p in per)}
    if group.get("dah") and group.get("equal"):
        d_cs = [last(d)["core_shell_index"] for d in group["dah"]]
        d_h = [last(d)["sorting_index_homotypic"] for d in group["dah"]]
        e_h = [last(d)["sorting_index_homotypic"] for d in group["equal"]]
        margin = (max(d_h) - min(d_h)) + (max(e_h) - min(e_h))
        res["dah_sorting"] = {"rule": "mean final core_shell > 0.1 AND mean dah homotypic - mean equal homotypic > (dah range + equal range)",
                              "dah_core_shell_final": d_cs, "dah_homotypic_final": d_h, "equal_homotypic_final": e_h,
                              "homotypic_difference": round(float(np.mean(d_h) - np.mean(e_h)), 4), "required_margin": round(margin, 4),
                              "pass": float(np.mean(d_cs)) > 0.1 and float(np.mean(d_h) - np.mean(e_h)) > margin}
    return res


def refinement(runs: list[dict], seed_spread_source: list[dict]) -> dict:
    keys = ["largest_cluster_fraction", "sphericity_largest", "sorting_index_homotypic", "core_shell_index", "rg_norm"]
    by = defaultdict(dict)
    for d in runs:
        if d["arm"] == "dah" and not d["cc"] and d["seed"] in (1, 2):
            by[d["seed"]][d["scale"]] = d["rows"][-1]
    spread = {k: (max(d["rows"][-1][k] for d in seed_spread_source) - min(d["rows"][-1][k] for d in seed_spread_source))
              for k in keys} if seed_spread_source else {}
    table = []
    for k in keys:
        row = {"metric": k, "seed_spread_scale1": round(spread.get(k, float("nan")), 4)}
        changes = []
        for s in (1, 2):
            vals = {sc: by[s][sc][k] for sc in by[s]}
            row[f"seed{s}"] = {str(sc): round(v, 4) for sc, v in sorted(vals.items())}
            if 1.0 in vals and 1.25 in vals:
                changes.append(vals[1.25] - vals[1.0])
        row["change_1.0_to_1.25"] = [round(c, 4) for c in changes]
        row["resolution_stable"] = bool(changes) and all(abs(c) < spread.get(k, 0) for c in changes)
        table.append(row)
    return {"rule": "metric resolution-stable iff |change 1.0->1.25| < seed spread (max-min, seeds 1-4, scale 1.0) "
                    "for both refinement seeds (protocol rule with addendum-1 erratum)",
            "limitation": "J, T, volume strength fixed across scales; s^2 time rescaling assumed (addendum 1)",
            "table": table}


def offlattice(traj: Path, cfg: dict) -> dict:
    z = np.load(traj)
    M, names = z["metrics"], [str(n) for n in z["metric_names"]]
    ix = {n: i for i, n in enumerate(names)}
    groups = defaultdict(list)
    for b, s in enumerate(cfg["systems"]):
        groups[(s["c_AA"], s["ratio"], s["D"], s["dt"])].append(b)
    rows = []
    for (cAA, ratio, D, dt), bs in sorted(groups.items()):
        f = M[-1, bs]
        i0 = M[0, bs]
        rows.append({"c_AA": cAA, "ratio": ratio, "D": D, "dt": dt, "n_seeds": len(bs),
                     **{f"final_{n}_mean": round(float(f[:, ix[n]].mean()), 4) for n in names},
                     **{f"final_{n}_range": round(float(np.ptp(f[:, ix[n]])), 4) for n in names},
                     "rg_ratio_mean": round(float((f[:, ix["rg_norm"]] / i0[:, ix["rg_norm"]]).mean()), 4)})
    # dt refinement: compare dt 0.02 vs 0.01 at same other params
    dtcmp = []
    for r in rows:
        if r["dt"] == 0.01:
            o = next((q for q in rows if q["dt"] == 0.02 and q["c_AA"] == r["c_AA"] and q["ratio"] == r["ratio"] and q["D"] == r["D"]), None)
            if o:
                dtcmp.append({"c_AA": r["c_AA"], "ratio": r["ratio"], "D": r["D"],
                              **{f"delta_{n}": round(r[f"final_{n}_mean"] - o[f"final_{n}_mean"], 4) for n in
                                 ("largest_cluster_fraction", "rg_norm", "core_shell_index", "sorting_index_homotypic")},
                              **{f"seedrange_{n}": round(max(r[f"final_{n}_range"], o[f"final_{n}_range"]), 4) for n in
                                 ("largest_cluster_fraction", "rg_norm", "core_shell_index", "sorting_index_homotypic")}})
    return {"trajectory_sha256": sha(traj), "n_cells": cfg["n_cells"], "groups": rows, "dt_refinement": dtcmp}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--sweeps", nargs="*", default=[], help="pairs DIR:CONFIG.json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    runs = load(Path(a.runs))
    out = Path(a.out)
    frozen = defaultdict(list)
    cc = defaultdict(list)
    for d in runs:
        if abs(d["scale"] - 1.0) < 1e-9:
            (cc if d["cc"] else frozen)[d["arm"]].append(d)
    v = {"schema": "frontier.xenomorph.verdicts/1",
         "protocol_sha256": sha(HERE / "protocol.json"), "addendum_1_sha256": sha(HERE / "protocol_addendum_1.json"),
         "runs": [{"name": d["name"], "arm": d["arm"], "seed": d["seed"], "scale": d["scale"], "connectivity": d["cc"],
                   "exit": d["exit"], "t0_all_cells_separate": d["t0_all_cells_separate"], "n_snapshots": len(d["rows"]),
                   "final_mcs": d["rows"][-1]["mcs"], "final": d["rows"][-1]} for d in runs],
         "frozen_gates_scale1": gates(frozen),
         "supplementary_connectivity_gates": gates(cc) if cc else None,
         "refinement": refinement(runs, frozen.get("dah", []))}
    zero = v["frozen_gates_scale1"].get("zero_adhesion")
    v["read_permission"] = ("zero-adhesion control PASSED: other arms may be read" if zero and zero["pass"] else
                            "zero-adhesion control FAILED or missing: no other arm may be read")
    out.mkdir(parents=True, exist_ok=True)
    (out / "verdicts.json").write_text(json.dumps(v, indent=1) + "\n")
    sw = {}
    for pair in a.sweeps:
        dpath, cpath = pair.split(":")
        cfg = json.loads(Path(cpath).read_text())
        sw[Path(dpath).parent.name] = offlattice(Path(dpath) / "trajectory.npz", cfg)
    if sw:
        (out / "offlattice_summary.json").write_text(json.dumps(sw, indent=1) + "\n")
    print(json.dumps({k: (g.get("pass") if isinstance(g, dict) else g) for k, g in v["frozen_gates_scale1"].items()}))
    print(v["read_permission"])


if __name__ == "__main__":
    main()
