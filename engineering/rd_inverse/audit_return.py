"""Return audit: recomputes every reported metric from the returned raw fields and checks it against the job's own JSON.
Reads an output directory; criteria are the frozen protocol's. Statuses stay separate: transport, numerical validity, design success, biology (unknown)."""
import argparse, hashlib, json
from pathlib import Path

import numpy as np

from engineering.rd_inverse import design as d


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rms(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))


def audit(out):
    out = Path(out)
    rec = json.loads((out / "receipt.json").read_text())
    res = {"schema": "frontier.rd-inverse.return-audit/1", "protocol_sha256_expected": d.sha(d.PROTOCOL)}
    t = {"receipt_complete": bool(rec.get("complete")), "protocol_sha256_matches": rec.get("protocol_sha256") == res["protocol_sha256_expected"],
         "phases_present": sorted(rec.get("phases", {})), "status": rec.get("status"), "stopped_at_cap_after": rec.get("stopped_at_cap_after")}
    bad = [f for ph in rec.get("phases", {}).values() for f, h in ph["files"].items() if not (out / f).exists() or sha(out / f) != h]
    t["files_hash_mismatch_or_missing"] = bad
    res["transport"] = t
    if not (out / "traces.json").exists():
        res["note"] = "search phase absent; later checks not run"
        return res
    tr = json.loads((out / "traces.json").read_text())
    tf = np.load(out / "targets.npz")["fields"]
    ef = np.load(out / "evaluated_fields.npz")
    counts = tr["evaluation_counts"]
    num = {"all_counts_64": all(v == d.BUDGET for v in counts.values()) and len(counts) == 12}
    worst = 0.0; mism = 0
    for m in ("baseline", "optimizer"):
        for i in range(len(tf)):
            for k, row in enumerate(tr["traces"][m][i]):
                got = None if not np.isfinite(ef[f"{m}_{i}"][k]).all() or np.abs(ef[f"{m}_{i}"][k]).max() > d.FAIL_ABS else rms(ef[f"{m}_{i}"][k], tf[i])
                if (got is None) != (row["score"] is None):
                    mism += 1
                elif got is not None:
                    worst = max(worst, abs(got - row["score"]))
    num["trace_score_recompute_max_abs_diff"] = worst; num["trace_validity_mismatches"] = mism
    sel = json.loads((out / "selection.json").read_text())
    ok_sel = True
    for m in ("baseline", "optimizer"):
        for i, row in enumerate(sel["selection"][m]):
            idx = d.select([x["score"] for x in tr["traces"][m][i]])
            ok_sel &= row.get("index") == idx
    num["selection_recomputed_equal"] = bool(ok_sel)
    vc = json.loads((out / "validation_controls.json").read_text())
    num["oracle_ok"], num["negative_ok_on_patterned"], num["wrong_ic_ok"] = vc["oracle_ok"], vc["negative_ok_on_patterned"], vc["wrong_ic_ok"]
    vf = np.load(out / "validation_fields.npz")
    num["oracle_recompute_max_abs"] = float(max(rms(vf["oracle"][i], vf["target"][i]) for i in range(len(tf))))
    if (out / "independent_fields.npz").exists():
        z = np.load(out / "independent_fields.npz"); ic = json.loads((out / "independent_checks.json").read_text()); wd = 0.0
        for row in ic["seed_generalisation"]:
            for i, s in enumerate(row["rms_vs_true_params"]):
                a, b = z[f"seed{row['seed_slot']}_{row['method']}"][i], z[f"seed{row['seed_slot']}_true"][i]
                wd = max(wd, abs(rms(a, b) - s)) if s is not None else wd
        num["seed_check_recompute_max_abs_diff"] = wd
    res["numerical_validity"] = num
    cs = json.loads((out / "concentration_stats.json").read_text()) if (out / "concentration_stats.json").exists() else {}
    res["raw_concentration_negative_cells"] = {k: (sum(v.get("negative_cells_u", 0) + v.get("negative_cells_v", 0) for v in vs.values()) if "cells" not in vs else vs["negative_cells_u"] + vs["negative_cells_v"]) for k, vs in cs.items() if isinstance(vs, dict)}
    res["design_success"] = {m: [{"target": r["target"], "gate_A_met": r["gate_A_met"], "gate_B_success": r["gate_B_success"], "score": r.get("score"), "status": r.get("status")} for r in sel["selection"][m]] for m in sel["selection"]}
    res["design_success"]["n_B_success"] = {m: sum(bool(r["gate_B_success"]) for r in sel["selection"][m]) for m in sel["selection"]}
    res["display_status"] = {"scope": "display label only; the booleans above are unchanged native/audit values",
                             "targets": [{"target": r["target"], "status": "unpatterned; amplitude gate failed; design success undefined" if not r["gate_A_met"] else "patterned; gate B evaluated"} for r in sel["selection"]["optimizer"]]}
    res["biology"] = "unknown; synthetic model-unit exercise, n=6, no DDPM acceleration claim, optimizer worse or failed is a legitimate outcome"
    res["unaudited"] = "GPU runtime and CUDA parity are read from receipt/control.json, not recomputed here"
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--write", default=None)
    a = ap.parse_args(); r = audit(a.out); s = json.dumps(d.clean(r), indent=1, sort_keys=True)
    if a.write:
        Path(a.write).write_text(s + "\n")
    print(s)
