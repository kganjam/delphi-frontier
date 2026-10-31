"""Motif diagnostics on the REAL zebrafish sequences and their controls.

Runs before any Evo 2 candidate exists, so the control distribution a candidate
will be compared against is established in advance rather than fitted around
whatever the model produces. CPU only; no model is involved at any point.

These are composition diagnostics. They are not binding, expression or function.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import jaspar  # noqa: E402
from connectors.bioservices.receipts import environment_fingerprint, git_sha, utc_now, write_json  # noqa: E402
from experiments.bioservices import motifs  # noqa: E402
from experiments.bioservices.sequence_controls import (  # noqa: E402
    dinucleotide_shuffle, gc_fraction, gc_matched_random,
)

SEED = 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Motif diagnostics on real sequences and controls")
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--jaspar-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--threshold", type=float, default=0.90)
    ap.add_argument("--top-fraction", type=float, default=0.25)
    ap.add_argument("--n-shuffles", type=int, default=8)
    ap.add_argument("--include-raw-density", action="store_true",
                    help="also record the all-matrix density that was measured NOT to discriminate")
    args = ap.parse_args()

    started = time.time()
    frozen = json.load(open(args.input_set))
    pfm_path, pfm_receipt = jaspar.fetch_pfms(args.jaspar_dir)
    pfms = jaspar.parse_pfms(pfm_path)
    print(f"{len(pfms)} JASPAR matrices; {len(frozen['targets'])} targets")

    rng = random.Random(SEED)
    rows = []
    for t in frozen["targets"]:
        for half in ("prompt", "held_out"):
            seq = t[f"{half}_seq"]
            rows.append({"group": f"real_{half}", "symbol": t["symbol"], "sequence": seq})
        held = t["held_out_seq"]
        rows.append({"group": "control_dinuc_shuffle", "symbol": t["symbol"],
                     "sequence": dinucleotide_shuffle(held, rng)})
        rows.append({"group": "control_gc_random", "symbol": t["symbol"],
                     "sequence": gc_matched_random(len(held), gc_fraction(held), rng)})

    # Aggregate density over all 879 matrices does NOT discriminate: measured at
    # eight thresholds from 0.85 to 0.98, real/control ratios were 1.02-1.09
    # throughout. So the reported diagnostic is the enrichment of a sequence over
    # its OWN dinucleotide-shuffle null, restricted to the most informative
    # quarter of the matrix set. Low-information matrices match nearly anywhere.
    informative = motifs.select_by_information(pfms, args.top_fraction)
    print(f"using the top {args.top_fraction:.0%} most informative matrices: {len(informative)}")
    enrich_rng = random.Random(SEED + 1)
    for r in rows:
        seq = r["sequence"]
        r["composition"] = motifs.composition(seq)
        r["raw_density_all_matrices"] = {
            k: v for k, v in motifs.relative_hits(seq, pfms, motifs._np_uniform(), args.threshold).items()
            if k != "per_matrix"
        } if args.include_raw_density else None
        r["shuffle_null_enrichment"] = motifs.shuffle_null_enrichment(
            seq, informative, enrich_rng, n_shuffles=args.n_shuffles, threshold=args.threshold)
        e, c = r["shuffle_null_enrichment"], r["composition"]
        z = e["z"]
        print(f"  {r['group']:24s} {r['symbol']:9s} gc={c['gc']:.3f} "
              f"cpg_oe={c['cpg_obs_exp'] if c['cpg_obs_exp'] is None else round(c['cpg_obs_exp'],3):>5} "
              f"obs={e['observed_hits']:4d} null={e['null_mean']:6.1f} "
              f"z={'  n/a' if z is None else format(z, '+5.2f')} ratio={e['ratio']:.3f}")
        del r["sequence"]

    def summarise(group: str) -> dict:
        import statistics

        sel = [r for r in rows if r["group"] == group]
        if not sel:
            return {}
        def stat(key, sub):
            vals = [r[key][sub] for r in sel if r[key].get(sub) is not None]
            if not vals:
                return {"n": 0}
            return {"n": len(vals), "mean": statistics.fmean(vals),
                    "sd": statistics.pstdev(vals) if len(vals) > 1 else 0.0,
                    "min": min(vals), "max": max(vals)}
        return {
            "gc": stat("composition", "gc"),
            "cpg_obs_exp": stat("composition", "cpg_obs_exp"),
            "enrichment_z": stat("shuffle_null_enrichment", "z"),
            "enrichment_ratio": stat("shuffle_null_enrichment", "ratio"),
            "observed_hits": stat("shuffle_null_enrichment", "observed_hits"),
        }

    groups = ["real_prompt", "real_held_out", "control_dinuc_shuffle", "control_gc_random"]
    summary = {g: summarise(g) for g in groups}

    payload = {
        "stage": "motif_baseline_before_any_candidate",
        "kind": ("composition diagnostics; NOT binding, expression or regulatory function. "
                 "No sequence model is involved."),
        "computed_utc": utc_now(),
        "git_sha": git_sha(os.path.dirname(os.path.abspath(__file__))),
        "environment": environment_fingerprint(),
        "input_set_id": frozen["input_set_id"],
        "assembly": frozen["assembly"],
        "jaspar": {"release": jaspar.RELEASE, "n_matrices": len(pfms),
                   "receipt": pfm_receipt.to_dict()},
        "threshold": args.threshold,
        "top_fraction_by_information": args.top_fraction,
        "n_informative_matrices": len(informative),
        "n_shuffles": args.n_shuffles,
        "seed": SEED,
        "measured_negative": ("aggregate motif density over all 879 matrices does NOT "
                              "discriminate real promoter-proximal sequence from "
                              "composition-matched controls: real/control ratio 1.02-1.09 "
                              "across thresholds 0.85-0.98. Reported enrichment is against "
                              "each sequence's own dinucleotide-shuffle null instead."),
        "group_summary": summary,
        "rows": rows,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    digest = write_json(args.out, payload)
    print(f"\nreceipt {args.out} sha256={digest}")
    print(f"\n{'group':24s} {'gc':>6s} {'CpG o/e':>8s} {'mean z':>8s} {'ratio':>7s}")
    for g in groups:
        st = summary[g]
        if st and st["enrichment_z"].get("n"):
            print(f"{g:24s} {st['gc']['mean']:6.3f} {st['cpg_obs_exp']['mean']:8.3f} "
                  f"{st['enrichment_z']['mean']:+8.2f} {st['enrichment_ratio']['mean']:7.3f}")
    print("\nControls that must behave: control_dinuc_shuffle is scored against a "
          "dinucleotide-shuffle null, so its z must sit near 0 by construction; "
          "control_gc_random destroys CpG and should fall below the real groups.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
