"""Independent, CPU-only assessment of Evo 2 candidates.

No sequence model is involved. Evo 2 scoring its own generations would not be an
independent assessment of them — generations are high-likelihood by construction
— so the diagnostic here is a PWM scan against each sequence's own
dinucleotide-shuffle null, on the same scale as the baseline computed before any
candidate existed.

Composition diagnostics only. Not binding, not expression, not regulatory
function, and nothing here says a candidate works.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import jaspar  # noqa: E402
from connectors.bioservices.receipts import environment_fingerprint, git_sha, utc_now, write_json  # noqa: E402
from experiments.bioservices import motifs  # noqa: E402

SEED = 0


def summarise(rows, group):
    sel = [r for r in rows if r["group"] == group]
    if not sel:
        return {}

    def stat(key, sub):
        vals = [r[key][sub] for r in sel if r[key].get(sub) is not None]
        if not vals:
            return {"n": 0}
        n = len(vals)
        sd = statistics.pstdev(vals) if n > 1 else 0.0
        se = sd / (n ** 0.5) if n > 1 else float("nan")
        return {"n": n, "mean": statistics.fmean(vals), "sd": sd, "se": se,
                "ci95": [statistics.fmean(vals) - 1.96 * se, statistics.fmean(vals) + 1.96 * se],
                "min": min(vals), "max": max(vals)}

    return {"gc": stat("composition", "gc"),
            "cpg_obs_exp": stat("composition", "cpg_obs_exp"),
            "enrichment_z": stat("shuffle_null_enrichment", "z"),
            "enrichment_ratio": stat("shuffle_null_enrichment", "ratio")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Motif diagnostics on Evo 2 candidates")
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--controls", required=True)
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--jaspar-dir", required=True)
    ap.add_argument("--baseline", required=True, help="the pre-candidate baseline, for the scale")
    ap.add_argument("--out", required=True)
    ap.add_argument("--threshold", type=float, default=0.90)
    ap.add_argument("--top-fraction", type=float, default=0.25)
    ap.add_argument("--n-shuffles", type=int, default=8)
    args = ap.parse_args()

    started = time.time()
    pfm_path, pfm_receipt = jaspar.fetch_pfms(args.jaspar_dir)
    pfms = jaspar.parse_pfms(pfm_path)
    informative = motifs.select_by_information(pfms, args.top_fraction)

    cands = json.load(open(args.candidates))
    ctrls = json.load(open(args.controls))
    frozen = json.load(open(args.input_set))
    held = {t["symbol"]: t["held_out_seq"] for t in frozen["targets"]}

    rows = []
    for c in cands:
        rows.append({"group": f"evo2_{c['arm']}", "label": f"{c['target']}:s{c['sample']}",
                     "sha256": c["sha256"], "sequence": c["sequence"]})
    for c in ctrls:
        rows.append({"group": f"control_{c['kind']}", "label": c["target"],
                     "sha256": c["sha256"], "sequence": c["sequence"]})
    for sym in sorted({c["target"] for c in cands}):
        rows.append({"group": "real_held_out", "label": sym,
                     "sha256": None, "sequence": held[sym]})

    rng = random.Random(SEED + 1)
    print(f"{len(rows)} sequences; {len(informative)} informative matrices of {len(pfms)}")
    for r in rows:
        seq = r["sequence"]
        r["composition"] = motifs.composition(seq)
        r["shuffle_null_enrichment"] = motifs.shuffle_null_enrichment(
            seq, informative, rng, n_shuffles=args.n_shuffles, threshold=args.threshold)
        z = r["shuffle_null_enrichment"]["z"]
        print(f"  {r['group']:28s} {r['label']:14s} gc={r['composition']['gc']:.3f} "
              f"cpg={r['composition']['cpg_obs_exp'] or float('nan'):.3f} "
              f"z={'  n/a' if z is None else format(z, '+5.2f')}")
        del r["sequence"]

    groups = sorted({r["group"] for r in rows})
    summary = {g: summarise(rows, g) for g in groups}
    baseline = json.load(open(args.baseline))

    payload = {
        "stage": "evo2_candidate_diagnostics",
        "kind": ("composition diagnostics with NO sequence model in the loop; not binding, "
                 "expression or regulatory function"),
        "computed_utc": utc_now(),
        "git_sha": git_sha(os.path.dirname(os.path.abspath(__file__))),
        "environment": environment_fingerprint(),
        "jaspar": {"release": jaspar.RELEASE, "n_matrices": len(pfms),
                   "n_informative": len(informative), "receipt": pfm_receipt.to_dict()},
        "settings": {"threshold": args.threshold, "top_fraction": args.top_fraction,
                     "n_shuffles": args.n_shuffles, "seed": SEED},
        "baseline_scale_from": {
            "file": os.path.basename(args.baseline),
            "computed_utc": baseline.get("computed_utc"),
            "group_summary": baseline.get("group_summary"),
            "note": "computed BEFORE any candidate existed, so the scale was not fitted to them",
        },
        "group_summary": summary,
        "rows": rows,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    digest = write_json(args.out, payload)
    print(f"\nreceipt {args.out} sha256={digest}")
    print(f"\n{'group':28s} {'n':>3s} {'gc':>6s} {'CpG o/e':>8s} {'mean z':>8s}  95% CI")
    for g in groups:
        s = summary[g]
        if s and s["enrichment_z"].get("n"):
            z = s["enrichment_z"]
            print(f"{g:28s} {z['n']:3d} {s['gc']['mean']:6.3f} {s['cpg_obs_exp']['mean']:8.3f} "
                  f"{z['mean']:+8.2f}  [{z['ci95'][0]:+.2f}, {z['ci95'][1]:+.2f}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
