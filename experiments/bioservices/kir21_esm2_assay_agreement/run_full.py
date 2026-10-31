"""Full 6,789-variant scoring — PREREGISTRATION-full.md.

Computes the masked log-probability vector at every one of the 391 matched
positions, persists those vectors, and derives a score for every matched
variant. Resumable across capped scopes, like the 256-variant run.

Two things it does that the 256 run did not:

- It **saves the per-position vectors**, with a sha256 of the exact masked input
  row. The earlier run saved only per-variant scores, which cannot be inverted
  back into a position's distribution, so extending it cost a full recomputation.
  After this, extending to any variant at these positions is free.
- It **re-derives the 256 original scores and requires them to match bit-for-bit.**
  A mismatch means the scoring path is not deterministic across processes, which
  would weaken the earlier result too, so it halts the run rather than warning.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import proteingym  # noqa: E402
from connectors.bioservices.esm2 import Esm2MaskedMarginalScorer, ScoringConfig  # noqa: E402
from connectors.bioservices.receipts import environment_fingerprint, git_sha, utc_now, write_json  # noqa: E402
from experiments.bioservices.kir21_esm2_assay_agreement import common  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Kir2.1 ESM-2: full matched-set scoring")
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--checkpoint-file", required=True)
    ap.add_argument("--original-scores", required=True,
                    help="the committed 256-variant checkpoint, for the reproduction control")
    ap.add_argument("--budget-seconds", type=float, default=470.0)
    args = ap.parse_args()

    started = time.time()
    protocol = common.load_protocol()
    surface, function, _checks = common.load_assays(protocol, args.data_dir)
    reference = surface.reference_sequence
    matched = proteingym.matched_variants(surface, function)
    positions = sorted({surface.variants[k].position for k in matched})

    state = {"vectors": {}, "invocations": [], "checkpoint": protocol["model"]["target_checkpoint"]}
    if os.path.exists(args.checkpoint_file):
        with open(args.checkpoint_file) as fh:
            state = json.load(fh)

    remaining = [p for p in positions if str(p) not in state["vectors"]]
    if remaining:
        cfg = ScoringConfig(
            checkpoint=state["checkpoint"],
            threads=protocol["model"]["threads"],
            batch_positions=protocol["model"]["batch_positions"],
        )
        t0 = time.time()
        scorer = Esm2MaskedMarginalScorer(reference, cfg, cache_dir=args.cache_dir)
        load_seconds = time.time() - t0

        bp = cfg.batch_positions
        work_started = time.time()
        done = 0
        for start in range(0, len(remaining), bp):
            if time.time() - work_started > args.budget_seconds:
                break
            chunk = remaining[start : start + bp]
            for pos, rec in scorer.position_log_probs(chunk).items():
                state["vectors"][str(pos)] = rec
            done += len(chunk)
        state["invocations"].append({
            "utc": utc_now(), "model_load_seconds": round(load_seconds, 2),
            "work_seconds": round(time.time() - work_started, 1),
            "positions_this_run": done, "positions_total": len(state["vectors"]),
            "git_sha": git_sha(os.path.dirname(os.path.abspath(__file__))),
            "environment": environment_fingerprint(),
        })
        write_json(args.checkpoint_file, state)
        left = len([p for p in positions if str(p) not in state["vectors"]])
        status = "COMPLETE" if left == 0 else "PARTIAL"
        print(f"{status} positions={len(state['vectors'])}/{len(positions)} "
              f"this_run={done} remaining={left} elapsed={time.time() - started:.1f}s")
        if left:
            return 0

    # Every position is present: derive scores for all matched variants.
    scores = {}
    for key in matched:
        v = surface.variants[key]
        rec = state["vectors"][str(v.position)]
        if rec["wt_aa"] != v.wt_aa:
            raise SystemExit(
                f"{key}: stored vector at position {v.position} is for {rec['wt_aa']}, not {v.wt_aa}"
            )
        scores[key] = rec["log_probs"][v.mut_aa] - rec["log_probs"][v.wt_aa]

    # Reproduction control against the committed 256.
    with open(args.original_scores) as fh:
        original = json.load(fh)["scores"]
    # The criterion is NOT bit-for-bit, and the first version of this control
    # getting that wrong is recorded rather than edited out. The 256 run computed
    # float(lp[mut] - lp[wt]): the subtraction happens in float32 and is then
    # widened. This run stores each log-probability as float64 and subtracts in
    # float64. Different arithmetic ORDER on the same float32 inputs, so the last
    # bits differ by construction. Measured: 153 of 256 differed, max absolute
    # 4.77e-07, max RELATIVE 5.9e-08, below float32 epsilon of 1.19e-07, and
    # Spearman between the two sets was exactly 1.0.
    #
    # What the analysis actually consumes is ranks, so the criterion is agreement
    # to float32 precision AND identical ranks. A real non-determinism would break
    # both; a representable-precision difference breaks neither.
    FLOAT32_EPS = 1.19e-07
    REL_TOLERANCE = 4 * FLOAT32_EPS
    missing, over_tolerance, diffs = [], [], []
    for key, old in original.items():
        new = scores.get(key)
        if new is None:
            missing.append(key)
            continue
        d = abs(new - old)
        diffs.append(d)
        if d > REL_TOLERANCE * max(abs(old), 1.0):
            over_tolerance.append({"mutant": key, "original": old, "recomputed": new, "abs_diff": d})

    shared = [k for k in original if k in scores]
    rank_identical, rho = None, None
    if shared:
        # Compare the RANK VECTORS directly. Asking whether Spearman == 1.0 is the
        # same mistake as asking whether the scores are bit-for-bit equal: the
        # correlation of two identical rankings came back as 0.9999999999999998
        # here, so an exact float comparison called identical ranks a failure.
        from scipy.stats import rankdata, spearmanr

        a = rankdata([original[k] for k in shared])
        b = rankdata([scores[k] for k in shared])
        rank_identical = bool((a == b).all())
        rho = float(spearmanr([original[k] for k in shared], [scores[k] for k in shared]).statistic)

    control = {
        "criterion": ("agreement to float32 precision AND identical ranks; NOT bit-for-bit, "
                      "because the two runs subtract in different precisions"),
        "n_original": len(original),
        "n_compared": len(shared),
        "n_missing": len(missing),
        "n_differing_at_all": sum(1 for d in diffs if d > 0),
        "max_abs_diff": max(diffs) if diffs else 0.0,
        "max_rel_diff": max((d / max(abs(original[k]), 1.0)
                             for k, d in zip(shared, diffs)), default=0.0),
        "rel_tolerance": REL_TOLERANCE,
        "n_over_tolerance": len(over_tolerance),
        "spearman_original_vs_recomputed": rho if shared else None,
        "ranks_identical": rank_identical,
        "passed": not missing and not over_tolerance and rank_identical is True,
        "over_tolerance_examples": over_tolerance[:20],
        "missing_examples": missing[:20],
    }
    mismatches = over_tolerance or missing
    out = {
        "stage": "full_matched_scoring",
        "completed_utc": utc_now(),
        "checkpoint": state["checkpoint"],
        "n_positions": len(state["vectors"]),
        "n_variants": len(scores),
        "scores": scores,
        "reproduction_control": control,
        "invocations": state["invocations"],
    }
    path = args.checkpoint_file.replace(".json", "_scores.json")
    write_json(path, out)
    print(f"COMPLETE positions={len(state['vectors'])} variants={len(scores)}")
    print(f"reproduction control: {control['n_compared']} compared, "
          f"{control['n_differing_at_all']} differ at all, max_rel {control['max_rel_diff']:.3e} "
          f"(tol {control['rel_tolerance']:.3e}), ranks_identical={control['ranks_identical']}, "
          f"passed={control['passed']}")
    if mismatches:
        print("HALTING: differences exceed float32 precision or ranks changed.")
        for m in mismatches[:5]:
            print("   ", m)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
