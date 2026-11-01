"""Re-verify every collected MD run against its SAVED job log (claude-mol, 2026-11-01).

Why this exists: the Nebius log service splits long lines at 16 KiB and returns the pieces out of order.
collect_md.py originally accepted any ordering that parsed as JSON - which is too weak, because the
summary's long arrays are all plain floats, so swapping two interior chunks still parses and silently
splices potential energies (order -9e5 kJ/mol) into the RMSD and radius-of-gyration arrays. That
produced a 926209 A RMSD and a negative radius of gyration on one 40 ns run, which is how it was caught.

collect_md.py now validates the physics as well as the parse. This script re-runs that stronger check
over the job_log.txt saved beside each run and compares the result with the committed md_summary.json,
so every number already in the repo is either confirmed or flagged. It needs no network: the older
jobs' logs have expired server-side, and the saved copies are the only remaining source.

Usage: python verify_md_logs.py   -> results/.../md_log_verification.json
"""
import hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_md import reassemble, summary_is_sane   # noqa: E402  (the same code path collect_md uses)

R = Path(__file__).resolve().parents[2] / "results/mol-sims/claude-20261101"
RUNS = ["md_shhN", "md_shhN_rep2", "md_fgf_complex", "md_fgf_negctrl", "md_shhN_40ns_a", "md_shhN_40ns_b"]
FIELDS = ["rmsd_ca_A_every_10ps", "rg_ca_A_every_10ps", "rmsf_ca_A_after_20pct", "potential_kj_mol_every_10ps",
          "seed", "prod_ns", "n_atoms", "ns_per_day", "all_finite", "interface"]


def chunks_between(lines, a, b):
    i = next(k for k, l in enumerate(lines) if l.strip().endswith(a))
    j = next(k for k, l in enumerate(lines) if l.strip().endswith(b))
    return [l.strip() for l in lines[i + 1:j]]


out = {}
for run in RUNS:
    d = R / run
    log, comm = d / "job_log.txt", d / "md_summary.json"
    if not log.exists() or not comm.exists():
        out[run] = {"status": "SKIPPED", "reason": "no saved job_log.txt or md_summary.json"}
        continue
    rec = {"job_log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
           "committed_summary_sha256": hashlib.sha256(comm.read_bytes()).hexdigest()}
    try:
        ch = chunks_between(log.read_text().splitlines(), "@@SUMMARY_BEGIN@@", "@@SUMMARY_END@@")
        rec["n_log_chunks"] = len(ch)
        fresh = reassemble(ch, lambda t: summary_is_sane(json.loads(t)))
    except SystemExit as e:
        out[run] = {**rec, "status": "UNVERIFIABLE", "reason": str(e)}
        continue
    except Exception as e:
        out[run] = {**rec, "status": "ERROR", "reason": f"{type(e).__name__}: {e}"}
        continue
    old = json.loads(comm.read_text())
    diffs = {k: {"committed": old.get(k), "reverified": fresh.get(k)} for k in FIELDS
             if not isinstance(old.get(k), list) and old.get(k) != fresh.get(k)}
    for k in FIELDS:
        if isinstance(old.get(k), list):
            a, b = old.get(k), fresh.get(k)
            if a != b:
                bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
                diffs[k] = {"n_values": [len(a), len(b)], "n_differing": len(bad) + abs(len(a) - len(b)),
                            "first_differing_index": bad[0] if bad else None}
    rec.update({"status": "CONFIRMED" if not diffs else "MISMATCH",
                "sanity_checks_passed": True, "differences": diffs or None})
    out[run] = rec

summary = {s: [k for k, v in out.items() if v["status"] == s] for s in {v["status"] for v in out.values()}}
rep = {"scope": "an integrity check on saved logs, not a simulation result",
       "why": ("The log service returns 16 KiB pieces out of order. Accepting any ordering that parsed as JSON was "
               "too weak for arrays of plain floats; the check now also requires array lengths to match the production "
               "length, distances to be positive and under 500 A, and potential energies to be negative."),
       "per_run": out, "by_status": summary}
p = R / "md_log_verification.json"
p.write_text(json.dumps(rep, indent=1, sort_keys=True))
for k, v in out.items():
    print(f"{v['status']:>12}  {k}  chunks={v.get('n_log_chunks')}  {v.get('reason') or ''}")
    if v.get("differences"):
        print("              differences:", json.dumps(v["differences"])[:400])
print("wrote", p)
