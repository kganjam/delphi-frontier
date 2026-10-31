"""Analysis of the full 6,789-variant run — PREREGISTRATION-full.md §5-§6.

Reuses the statistical functions of ``analyze.py`` unchanged. Nothing about the
evaluator is retuned for more data; the same code path runs on a bigger set,
which is the point of preregistering it.

What it adds is the sensitivity reporting §5 requires, because the interesting
question is not only what Δρ is but how much the extra data actually bought —
and the √n expectation is an approximation that assumes variants are
independent, which they are not.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import proteingym  # noqa: E402
from connectors.bioservices.receipts import environment_fingerprint, git_sha, utc_now, write_json  # noqa: E402
from experiments.bioservices.baselines import blosum62  # noqa: E402
from experiments.bioservices.kir21_esm2_assay_agreement import analyze, common  # noqa: E402


def _arm(predictor, surf, func, positions, an, label):
    rho_s = analyze._spearman(predictor, surf)
    rho_f = analyze._spearman(predictor, func)
    bs, bf, bd, _ = analyze._paired_bootstrap(
        predictor, surf, func, an["bootstrap_resamples"], an["bootstrap_seed"], an["ci"])
    bs["point"], bf["point"], bd["point"] = rho_s, rho_f, rho_s - rho_f
    cluster = analyze._cluster_bootstrap(
        predictor, surf, func, positions, an["bootstrap_resamples"], an["bootstrap_seed"], an["ci"])
    verdict, why = analyze._verdict(bd)

    # The governing interval is the wider of the two, per the parent protocol.
    variant_width = bd["ci_high"] - bd["ci_low"]
    cluster_width = cluster["delta_ci_high"] - cluster["delta_ci_low"]
    if cluster_width >= variant_width:
        governing, gv = "position_clustered", analyze._verdict(
            {"ci_low": cluster["delta_ci_low"], "ci_high": cluster["delta_ci_high"]})
    else:
        governing, gv = "variant_level", (verdict, why)

    return {
        "rho_surface": bs, "rho_function": bf,
        "delta_rho_surface_minus_function": bd,
        "cluster_bootstrap_by_position": cluster,
        "paired_permutation_delta": analyze._paired_permutation_delta(
            predictor, surf, func, an["permutation_resamples"], an["permutation_seed"], rho_s - rho_f),
        "williams_test": analyze._williams_test(predictor, surf, func),
        "permutation_p_surface": analyze._permutation_p(
            predictor, surf, rho_s, an["permutation_resamples"], an["permutation_seed"]),
        "permutation_p_function": analyze._permutation_p(
            predictor, func, rho_f, an["permutation_resamples"], an["permutation_seed"]),
        "verdict_variant_level": verdict,
        "governing_interval": governing,
        "verdict_on_H1": gv[0],
        "verdict_reason": f"governing interval is the {governing} one (the wider); {gv[1]}",
        "interval_widths": {"variant_level": variant_width, "position_clustered": cluster_width},
        "label": label,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Kir2.1 ESM-2: full matched-set analysis")
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--full-scores", required=True)
    ap.add_argument("--subset-result", required=True, help="the committed 256-variant analysis")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-csv", required=True)
    args = ap.parse_args()

    started = time.time()
    protocol = common.load_protocol()
    an = protocol["analysis"]
    surface, function, checks = common.load_assays(protocol, args.data_dir)
    matched = proteingym.matched_variants(surface, function)

    full = json.load(open(args.full_scores))
    scores = full["scores"]
    subset_result = json.load(open(args.subset_result))

    def complete(k):
        return (k in scores and np.isfinite(scores[k])
                and np.isfinite(surface.variants[k].dms_score)
                and np.isfinite(function.variants[k].dms_score))

    usable = [k for k in matched if complete(k)]
    pred = np.array([scores[k] for k in usable])
    surf = np.array([surface.variants[k].dms_score for k in usable])
    func = np.array([function.variants[k].dms_score for k in usable])
    blos = np.array([float(blosum62(surface.variants[k].wt_aa, surface.variants[k].mut_aa))
                     for k in usable])
    positions = [surface.variants[k].position for k in usable]

    with open(args.out_csv, "w") as fh:
        fh.write("mutant,position,wt_aa,mut_aa,esm2_masked_marginal,blosum62,"
                 "surface_dms_score,function_dms_score\n")
        for k in usable:
            v = surface.variants[k]
            fh.write(f"{k},{v.position},{v.wt_aa},{v.mut_aa},{scores[k]:.6f},"
                     f"{blosum62(v.wt_aa, v.mut_aa)},{v.dms_score:.6f},"
                     f"{function.variants[k].dms_score:.6f}\n")

    results = {
        "esm2_masked_marginal": _arm(pred, surf, func, positions, an, "esm2_masked_marginal"),
        "blosum62": _arm(blos, surf, func, positions, an, "blosum62"),
    }

    # --- §5 sensitivity reporting ---
    per_position: dict[int, int] = {}
    for p in positions:
        per_position[p] = per_position.get(p, 0) + 1
    counts = sorted(per_position.values())

    sub_esm = subset_result["results"]["esm2_masked_marginal"]
    sub_d = sub_esm["delta_rho_surface_minus_function"]
    sub_variant_hw = (sub_d["ci_high"] - sub_d["ci_low"]) / 2
    sub_cluster = sub_esm["cluster_bootstrap_by_position"]
    sub_cluster_hw = (sub_cluster["delta_ci_high"] - sub_cluster["delta_ci_low"]) / 2

    full_d = results["esm2_masked_marginal"]["delta_rho_surface_minus_function"]
    full_variant_hw = (full_d["ci_high"] - full_d["ci_low"]) / 2
    full_cluster = results["esm2_masked_marginal"]["cluster_bootstrap_by_position"]
    full_cluster_hw = (full_cluster["delta_ci_high"] - full_cluster["delta_ci_low"]) / 2

    # Cluster-count sensitivity: the clustered interval recomputed on the SAME
    # 193 positions the subset covered, so the change attributable to the added
    # positions is measured rather than inferred from a sqrt(n) rule.
    # The positions the 256-variant subset covered, read from its committed CSV
    # rather than re-derived, so this cannot drift from what was actually scored.
    subset_positions, idx_193 = None, None
    sub_csv = os.path.join(os.path.dirname(args.subset_result),
                           "kir21_predictions_vs_measurements.csv")
    if os.path.exists(sub_csv):
        import csv as _csv

        with open(sub_csv) as fh:
            subset_positions = sorted({int(r["position"]) for r in _csv.DictReader(fh)})
        keep = set(subset_positions)
        idx_193 = [i for i, p in enumerate(positions) if p in keep]

    cluster_sensitivity = {
        "clusters_full": full_cluster["n_clusters"],
        "clusters_subset_covered": len(subset_positions) if subset_positions else None,
    }
    if idx_193:
        i = np.array(idx_193)
        restricted = analyze._cluster_bootstrap(
            pred[i], surf[i], func[i], [positions[j] for j in idx_193],
            an["bootstrap_resamples"], an["bootstrap_seed"], an["ci"])
        cluster_sensitivity["restricted_to_subset_positions"] = {
            "n_variants": len(idx_193),
            "n_clusters": restricted["n_clusters"],
            "delta_ci": [restricted["delta_ci_low"], restricted["delta_ci_high"]],
            "half_width": (restricted["delta_ci_high"] - restricted["delta_ci_low"]) / 2,
            "note": ("all variants at the 193 positions the 256-variant subset covered; "
                     "isolates added POSITIONS from added variants at known positions"),
        }

    sensitivity = {
        "measured_vs_predicted_narrowing": {
            "variant_level": {
                "subset_half_width": sub_variant_hw, "full_half_width": full_variant_hw,
                "n_subset": subset_result["n_usable"], "n_full": len(usable),
                "measured_narrowing": sub_variant_hw / full_variant_hw if full_variant_hw else None,
                "predicted_narrowing_sqrt_n": (len(usable) / subset_result["n_usable"]) ** 0.5,
                "caveat": "the sqrt(n) prediction assumes independent variants; they are not independent",
            },
            "position_clustered": {
                "subset_half_width": sub_cluster_hw, "full_half_width": full_cluster_hw,
                "measured_narrowing": sub_cluster_hw / full_cluster_hw if full_cluster_hw else None,
                "predicted_narrowing_sqrt_clusters": (full_cluster["n_clusters"] / 193) ** 0.5,
            },
        },
        "cluster_count_sensitivity": cluster_sensitivity,
        "per_position_variant_counts": {
            "n_positions": len(per_position),
            "min": counts[0], "max": counts[-1],
            "mean": statistics.fmean(counts), "median": statistics.median(counts),
            "sd": statistics.pstdev(counts) if len(counts) > 1 else 0.0,
            "note": "an unbalanced design changes what cluster resampling does",
        },
        "subset_versus_full": {
            "subset_rho_surface": sub_esm["rho_surface"]["point"],
            "subset_rho_function": sub_esm["rho_function"]["point"],
            "subset_delta": sub_d["point"],
            "full_rho_surface": results["esm2_masked_marginal"]["rho_surface"]["point"],
            "full_rho_function": results["esm2_masked_marginal"]["rho_function"]["point"],
            "full_delta": full_d["point"],
            "note": "subset figures are read from the committed 256-variant analysis, not recomputed",
        },
    }

    receipt = {
        "stage": "analysis_full",
        "protocol_id": protocol["protocol_id"],
        "preregistration": "PREREGISTRATION-full.md",
        "analysed_utc": utc_now(),
        "git_sha": git_sha(os.path.dirname(os.path.abspath(__file__))),
        "environment": environment_fingerprint(),
        "checkpoint_used": full.get("checkpoint"),
        "reproduction_control": full.get("reproduction_control"),
        "scoring_invocations": full.get("invocations", []),
        "reference_checks": checks,
        "n_matched": len(matched), "n_usable": len(usable),
        "n_positions": len(per_position),
        "external_reference": protocol["external_reference"],
        "external_reference_status": (
            "an OBSERVED external comparison on a different variant sample computed with a "
            "different pipeline, carrying its own unreported uncertainty; not a known true "
            "difference and not a target to be recovered"),
        "results": results,
        "sensitivity": sensitivity,
        "independent_review": (
            "none; F1-F5 are this harness checking its own run against criteria fixed in "
            "advance. Under SPEC-005 the executor cannot certify its own work, so this is a "
            "proposed contribution carrying a self-assessment, not a Frontier-accepted result."),
        "elapsed_seconds": round(time.time() - started, 1),
    }
    digest = write_json(args.out_json, receipt)

    print(f"analysis receipt {args.out_json} sha256={digest}")
    print(f"usable {len(usable)}/{len(matched)} over {len(per_position)} positions")
    rc = full.get("reproduction_control", {})
    print(f"reproduction control: bit_for_bit={rc.get('bit_for_bit')} "
          f"({rc.get('n_mismatched')} mismatched of {rc.get('n_original')})")
    for label, r in results.items():
        d = r["delta_rho_surface_minus_function"]
        c = r["cluster_bootstrap_by_position"]
        print(f"\n{label}")
        print(f"  rho surface  = {r['rho_surface']['point']:+.3f} "
              f"[{r['rho_surface']['ci_low']:+.3f}, {r['rho_surface']['ci_high']:+.3f}]")
        print(f"  rho function = {r['rho_function']['point']:+.3f} "
              f"[{r['rho_function']['ci_low']:+.3f}, {r['rho_function']['ci_high']:+.3f}]")
        print(f"  delta variant-level = {d['point']:+.3f} [{d['ci_low']:+.3f}, {d['ci_high']:+.3f}]")
        print(f"  delta clustered     = [{c['delta_ci_low']:+.3f}, {c['delta_ci_high']:+.3f}] "
              f"({c['n_clusters']} clusters)")
        print(f"  governing = {r['governing_interval']}  -> H1 {r['verdict_on_H1'].upper()}")
    m = sensitivity["measured_vs_predicted_narrowing"]
    print(f"\nnarrowing, variant-level: measured "
          f"{m['variant_level']['measured_narrowing']:.2f}x vs sqrt(n) "
          f"{m['variant_level']['predicted_narrowing_sqrt_n']:.2f}x")
    print(f"narrowing, clustered:     measured "
          f"{m['position_clustered']['measured_narrowing']:.2f}x vs sqrt(clusters) "
          f"{m['position_clustered']['predicted_narrowing_sqrt_clusters']:.2f}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
