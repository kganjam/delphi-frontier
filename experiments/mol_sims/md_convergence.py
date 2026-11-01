"""Block-wise convergence test across the ShhN MD replicas (claude-mol, 2026-11-01).

The two 10 ns replicas agreed on which residues move (RMSF Spearman 0.91) but disagreed on drift
(-0.11 vs +0.98 A/ns over the last 2 ns), so 10 ns was not converged. This compares every available
replica on three criteria that a longer run can actually settle:

  1. per-5-ns-block mean CA RMSD and its slope -> does the drift go to zero as the window moves out?
  2. RMSF agreement between every pair of replicas (Spearman) -> is the flexibility pattern
     seed-independent, and does it stay so at 4x the length?
  3. RMSF-vs-start-pLDDT Spearman per replica -> is the one positive macromolecular finding stable
     at 40 ns, or was it an artefact of a short window?

A within-replica first-half/second-half RMSF test is NOT possible here: only the whole-trajectory
RMSF vector is returned through the job log, not the frames, so stationarity within one run is not
tested and is not claimed.

Usage: python md_convergence.py <start_model_cif> <dir1> <dir2> ...   (each dir holds md_summary.json)
Writes md_convergence_report.json next to the first directory's parent. SIMULATED, not observed.
"""
import hashlib, json, sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

cif = Path(sys.argv[1])
dirs = [Path(d) for d in sys.argv[2:]]
plddt = np.array([float(l.split()[-2]) for l in cif.read_text().splitlines()
                  if l.startswith("ATOM") and l.split()[3] == "CA"])

reps, out = {}, {}
for d in dirs:
    s = json.loads((d / "md_summary.json").read_text())
    r = np.array(s["rmsd_ca_A_every_10ps"])
    ns = len(r) * 0.01
    t = np.arange(len(r)) * 0.01
    blocks = []
    for b0 in range(0, int(ns), 5):
        m = (t >= b0) & (t < b0 + 5)
        if m.sum() < 50:
            continue
        sl = float(np.polyfit(t[m], r[m], 1)[0])
        blocks.append({"ns": [b0, b0 + 5], "mean_rmsd_A": round(float(r[m].mean()), 3),
                       "slope_A_per_ns": round(sl, 3)})
    rmsf_full = np.array(s["rmsf_ca_A_after_20pct"])
    reps[d.name] = {"rmsf_full": rmsf_full, "prod_ns": ns}
    n = len(plddt) if len(plddt) <= len(rmsf_full) else len(rmsf_full)
    rho = spearmanr(rmsf_full[:n], plddt[:n])
    out[d.name] = {"prod_ns": ns, "seed": s["seed"], "n_atoms": s["n_atoms"],
                   "ns_per_day": round(s["ns_per_day"], 1), "all_finite": s["all_finite"],
                   "blocks_5ns": blocks,
                   "last_block_slope_A_per_ns": blocks[-1]["slope_A_per_ns"] if blocks else None,
                   "rmsf_vs_start_plddt": {"rho": round(float(rho.statistic), 3), "p": float(rho.pvalue)},
                   "md_summary_sha256": hashlib.sha256((d / "md_summary.json").read_bytes()).hexdigest()}

# cross-replica RMSF agreement, every pair, on the shared residue range
pairs = {}
names = list(reps)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = reps[names[i]]["rmsf_full"], reps[names[j]]["rmsf_full"]
        k = min(len(a), len(b))
        pr = spearmanr(a[:k], b[:k])
        pairs[f"{names[i]} vs {names[j]}"] = {"rmsf_spearman_rho": round(float(pr.statistic), 3),
                                              "p": float(pr.pvalue), "n_residues": int(k)}

slopes = {k: v["last_block_slope_A_per_ns"] for k, v in out.items() if v["last_block_slope_A_per_ns"] is not None}
long_slopes = {k: v for k, v in slopes.items() if out[k]["prod_ns"] >= 30}
verdict = ("not enough long replicas to judge" if len(long_slopes) < 2 else
           "the long replicas agree that the final 5 ns block is flat (|slope| < 0.1 A/ns): the fold has stopped drifting"
           if all(abs(v) < 0.1 for v in long_slopes.values()) else
           "the long replicas still drift in their final block, so even this length is not converged; "
           "only the ranking of mobile residues may be quoted")
rep = {"scope": "SIMULATED classical MD of a PREDICTED structure (apo, no Zn2+/Ca2+); convergence of the simulation, "
                "not accuracy of the structure; nothing observed",
       "start_model_cif_sha256": hashlib.sha256(cif.read_bytes()).hexdigest(),
       "replicas": out, "cross_replica_rmsf": pairs,
       "final_block_slopes_A_per_ns": slopes, "verdict": verdict}
p = dirs[0].parent / "md_convergence_report.json"
p.write_text(json.dumps(rep, indent=1, sort_keys=True))
print(json.dumps({"verdict": verdict, "final_block_slopes_A_per_ns": slopes,
                  "rho": {k: v["rmsf_vs_start_plddt"] for k, v in out.items()},
                  "cross_replica_rmsf": pairs}, indent=1))
print("wrote", p)
