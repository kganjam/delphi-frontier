"""Combine the arm A and baseline Evo 2 outputs into the reportable numbers.

Design notes that matter for honesty:

* Group intervals are t-based, not 1.96*SEM. n is 9-19 per group here, where the
  normal approximation is visibly too narrow.
* The zebrafish-vs-flyingfish contrast is computed PAIRED by gene, because the
  two species sets are matched on gene identity (minus hoxd13a, zebrafish-only).
  An unpaired comparison would throw away that matching and conflate
  between-gene variance with the species difference.
* That contrast is still reported as confounded, not as a result. GRCz11 is in
  Evo 2's training corpus and GCA_018398805.1 almost certainly is not, so the
  expected direction is fixed before any biology enters.

Usage: summarize.py <armA_out_dir> <baseline_out_dir|-> <screen.json|-> <out.json>
"""
from __future__ import annotations
import json, sys, math
import statistics as st
from scipy import stats


def ci(vals):
    vals = [float(v) for v in vals]
    n = len(vals)
    m = st.mean(vals)
    if n < 2:
        return {"n": n, "mean": round(m, 4), "lo": None, "hi": None, "sd": None}
    sd = st.stdev(vals)
    half = stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)
    return {"n": n, "mean": round(m, 4), "lo": round(m - half, 4),
            "hi": round(m + half, 4), "sd": round(sd, 4)}


def load(p):
    return json.load(open(p)) if p and p != "-" else None


def main() -> int:
    arm_dir, base_dir, screen_p, out_p = sys.argv[1:5]
    scores = load(f"{arm_dir}/scores.json")
    base = load(f"{base_dir}/baseline_scores.json") if base_dir != "-" else None
    screen = load(screen_p) if screen_p != "-" else None
    rep = {"inputs_used": {"armA_scores": bool(scores), "baseline_scores": bool(base),
                           "artefact_screen": bool(screen)}}

    # ---- arm A groups, as scored by the generating model -------------------
    by_kind = {}
    for r in scores:
        by_kind.setdefault(r["kind"], []).append(r)
    rep["armA_groups"] = {k: ci([r["evo2_mean_logprob"] for r in v])
                          for k, v in sorted(by_kind.items())}
    rep["armA_groups_note"] = (
        "generated candidates were sampled as P(x|1kb prompt) but are scored "
        "here as unconditional P(x), the same treatment every other group gets")

    # ---- baseline: the unbiased row finally gets a control -----------------
    if base:
        bk = {}
        for r in base:
            bk.setdefault(r["kind"], []).append(r)
        rep["baseline_groups"] = {k: ci([r["evo2_mean_logprob"] for r in v])
                                  for k, v in sorted(bk.items())}
        real = {r["target"]: r["evo2_mean_logprob"] for r in bk.get("real_held_out", [])}
        shuf = {r["target"]: r["evo2_mean_logprob"] for r in bk.get("dinucleotide_shuffle_of_real", [])}
        both = sorted(set(real) & set(shuf))
        d = [real[t] - shuf[t] for t in both]
        rep["real_minus_own_dinuc_shuffle_paired"] = ci(d) if d else None
        rep["real_minus_own_dinuc_shuffle_note"] = (
            "the one comparison in this work that is neither circular nor "
            "cross-species: real sequence against its own composition-matched "
            "scramble, paired by window. A positive interval excluding zero "
            "means the model reads structure above dinucleotide composition. It "
            "does NOT mean the model read cis-regulatory syntax.")

        # ---- species contrast, paired by gene, reported as confounded -----
        zeb = {t.split(":")[1]: v for t, v in real.items() if t.startswith("dan:")}
        fly = {t.split(":")[1]: v for t, v in real.items() if t.startswith("hir:")}
        genes = sorted(set(zeb) & set(fly))
        pd = [zeb[g] - fly[g] for g in genes]
        rep["species_contrast_paired_zebrafish_minus_flyingfish"] = {
            "genes_paired": genes, **(ci(pd) if pd else {})}
        rep["species_contrast_VOID_FOR_BIOLOGY"] = (
            "Not interpretable as evolutionary or regulatory difference. Three "
            "confounds each independently predict zebrafish > flyingfish: (1) "
            "GRCz11 is in Evo 2's training corpus and GCA_018398805.1 almost "
            "certainly is not, so this contrasts memorisation against "
            "out-of-distribution generalisation; (2) the zebrafish windows are "
            "TSS-anchored while the flyingfish windows sit upstream of a "
            "predicted start codon from a CDS-only GeneWise model, with no "
            "TSS/UTR, so they may be UTR intron or intergenic sequence; (3) "
            "flyingfish GC runs systematically higher. The sign carries no "
            "information.")

    # ---- degeneracy gate on the candidate row -----------------------------
    if screen:
        rep["artefact_screen"] = {
            "n_candidates": screen["n_candidates"],
            "n_flagged_degenerate": screen["n_flagged_degenerate"],
            "flagged": screen["flagged"],
            "candidate_gzip_band": screen["candidate_bands"]["gzip_ratio"],
            "real_gzip_band": screen["real_heldout_reference_bands"]["gzip_ratio"],
            "max_local_identity_vs_heldout":
                screen["candidate_bands"]["best_local_identity_60bp_vs_heldout"]["max"]}
        flagged = set(s.split()[0] for s in screen["flagged"])
        clean = [r for r in by_kind.get("generated", [])
                 if r["sha256"][:12] not in flagged]
        rep["armA_generated_excluding_degenerate"] = ci([r["evo2_mean_logprob"] for r in clean])
        rep["armA_generated_excluding_degenerate_note"] = (
            "degenerate candidates score near zero log-prob and would inflate "
            "the candidate mean as a pure artefact, so the gated row is the one "
            "to read")

    json.dump(rep, open(out_p, "w"), indent=2)
    print(json.dumps(rep, indent=2)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
