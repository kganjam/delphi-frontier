"""Collect a finished Nebius AI MD job from its logs (claude-mol, 2026-11-01).

Reads `nebius ai job logs <id>` (token read by the CLI from ~/.nebius/token at call time), extracts the JSON
summary and the final protein frame between markers, saves them with hashes, and compares per-residue RMSF to the
Boltz-2 pLDDT of the starting model (Spearman). SIMULATED, not observed.
Usage: python collect_md.py <aijob-id> <outdir> <start_model_cif>
"""
import base64, gzip, hashlib, json, subprocess, sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

job, outdir, cif = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
NEB = str(Path.home() / ".nebius/bin/nebius")
p = subprocess.run([NEB, "--profile", "hackathon", "ai", "job", "logs", job], capture_output=True, text=True, timeout=300)
log = p.stdout
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "job_log.txt").write_text(log)
state = subprocess.run([NEB, "--profile", "hackathon", "ai", "job", "get", job], capture_output=True, text=True, timeout=120).stdout
lines = log.splitlines()


def between(a, b):
    """Chunks between two markers. The log service splits long lines at 16 KiB and can return the pieces
    out of order, so the caller reassembles by trying permutations and checking the result parses."""
    i = next(k for k, l in enumerate(lines) if l.strip().endswith(a))
    j = next(k for k, l in enumerate(lines) if l.strip().endswith(b))
    return [l.strip() for l in lines[i + 1:j]]


def reassemble(chunks, check, max_perm=5040):
    import itertools
    if len(chunks) > 8:                    # too many to permute: rely on log order
        return check("".join(chunks))
    for perm in itertools.permutations(range(len(chunks))):
        try:
            return check("".join(chunks[k] for k in perm))
        except Exception:
            continue
    raise SystemExit("could not reassemble log chunks")


summ = reassemble(between("@@SUMMARY_BEGIN@@", "@@SUMMARY_END@@"), json.loads)
pdb = reassemble(between("@@FINAL_PDB_GZ_B64_BEGIN@@", "@@FINAL_PDB_GZ_B64_END@@"), lambda t: gzip.decompress(base64.b64decode(t)))
(outdir / "final_frame_protein.pdb").write_bytes(pdb)
pl = [float(l.split()[-2]) for l in cif.read_text().splitlines() if l.startswith("ATOM") and l.split()[3] == "CA"]
rmsf = np.array(summ["rmsf_ca_A_after_20pct"])
rho = spearmanr(rmsf, np.array(pl)[:len(rmsf)]) if len(pl) >= len(rmsf) else None
r = np.array(summ["rmsd_ca_A_every_10ps"])
n = len(r)
analysis = {"job_id": job, "job_state_text": [l.strip() for l in state.splitlines() if "State" in l][:2],
            "rmsd_ca_A": {"first_ns_mean": float(r[:100].mean()), "last_2ns_mean": float(r[-200:].mean()), "max": float(r.max()),
                          "last_2ns_slope_A_per_ns": float(np.polyfit(np.arange(200) * 0.01, r[-200:], 1)[0]) if n >= 200 else None},
            "rg_ca_A_first_last": [summ["rg_ca_A_every_10ps"][0], summ["rg_ca_A_every_10ps"][-1]],
            "rmsf_vs_start_plddt_spearman": {"rho": float(rho.statistic), "p": float(rho.pvalue)} if rho is not None else None,
            "top10_rmsf_residues_1based": [int(i) + 1 for i in np.argsort(-rmsf)[:10]],
            "ns_per_day": summ["ns_per_day"], "all_finite": summ["all_finite"], "n_atoms": summ["n_atoms"], "seed": summ["seed"]}
if summ.get("interface"):
    fr = np.array(summ["interface"]["fraction_initial_pairs_retained_every_10ps"])
    analysis["interface"] = {"n_initial_ca_pairs_lt8A": summ["interface"]["n_initial_ca_pairs_lt8A"],
                             "retained_fraction_last_2ns_mean": float(fr[-200:].mean()), "retained_fraction_min": float(fr.min()),
                             "min_interchain_ca_distance_last": summ["interface"]["min_interchain_ca_distance_A_every_10ps"][-1]}
(outdir / "md_summary.json").write_text(json.dumps(summ))
rec = {"command": f"python experiments/mol_sims/collect_md.py {job} {outdir} {cif}", "exit_code": 0, "evidence_kind": "simulated",
       "scope": "SIMULATED classical MD of a PREDICTED structure; 10 ns single replica; not observed; no equilibrium or binding claim",
       "sha256": {"job_log": hashlib.sha256(log.encode()).hexdigest(), "final_frame": hashlib.sha256(pdb).hexdigest(),
                  "start_cif": hashlib.sha256(cif.read_bytes()).hexdigest()}, "analysis": analysis}
(outdir / "md_receipt.json").write_text(json.dumps(rec, indent=1, sort_keys=True))
print(json.dumps(analysis, indent=1))
