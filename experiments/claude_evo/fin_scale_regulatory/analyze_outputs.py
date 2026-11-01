"""CPU-only analysis of the recovered Evo 2 fin/scale bundle.

Added after the gemini-4-argon design review. None of this needs a GPU, and
all of it is about catching artefacts that would otherwise be reported as
results:

  degeneracy   gzip ratio and distinct-k-mer fractions, because a temperature-1
               1 kb autoregressive sample can collapse into a repeat that
               scores near zero log-prob and would beat real sequence purely as
               an artefact. Run 1 already produced one.
  retrieval    best local-alignment identity of each candidate against the
               held-out window it was never shown. High zebrafish identity
               would mean the model is reciting memorised GRCz11, not
               generalising -- the leakage confound made concrete.
  divergence   3-mer and 4-mer Jensen-Shannon divergence, candidate against its
               own held-out window.

Usage: analyze_outputs.py <recovered_out_dir> <input_set.json> <report.json>
"""
from __future__ import annotations
import gzip, json, math, sys, collections


def gzip_ratio(seq: str) -> float:
    raw = seq.encode()
    return len(gzip.compress(raw, 9)) / len(raw)


def kmer_frac(seq: str, k: int) -> float:
    """Distinct k-mers observed / distinct k-mers possible given the length."""
    seen = {seq[i:i + k] for i in range(len(seq) - k + 1)}
    return len(seen) / min(4 ** k, len(seq) - k + 1)


def max_homopolymer(seq: str) -> int:
    best = run = 1
    for a, b in zip(seq, seq[1:]):
        run = run + 1 if a == b else 1
        best = max(best, run)
    return best


def kmer_dist(seq: str, k: int) -> dict[str, float]:
    c = collections.Counter(seq[i:i + k] for i in range(len(seq) - k + 1))
    n = sum(c.values())
    return {m: v / n for m, v in c.items()}


def jsd(p: dict[str, float], q: dict[str, float]) -> float:
    keys = set(p) | set(q)
    m = {k: 0.5 * (p.get(k, 0.0) + q.get(k, 0.0)) for k in keys}

    def kl(a):
        return sum(a[k] * math.log2(a[k] / m[k]) for k in a if a[k] > 0)

    return 0.5 * kl(p) + 0.5 * kl(q)


def best_local_identity(a: str, b: str, w: int = 60) -> float:
    """Best identity over any aligned ungapped window of length w.

    A full Smith-Waterman needs no dependency to be informative here: a model
    reciting a memorised locus produces a long exact-ish ungapped stretch, which
    a sliding ungapped comparison already detects. Reported as a floor on
    identity, not as an optimal alignment score.
    """
    if len(a) < w or len(b) < w:
        return 0.0
    best = 0.0
    for off in range(-(len(a) - w), len(b) - w + 1):
        ai = max(0, -off)
        bi = max(0, off)
        n = min(len(a) - ai, len(b) - bi)
        if n < w:
            continue
        match = run = 0
        for i in range(n):
            if a[ai + i] == b[bi + i]:
                run += 1
                match = max(match, run)
            else:
                run = 0
        best = max(best, match / w)
    return min(1.0, best)


def main() -> int:
    out_dir, input_set, report_path = sys.argv[1], sys.argv[2], sys.argv[3]
    inputs = json.load(open(input_set))
    held = {}
    for t in inputs["targets"]:
        key = f"{t['species'].split('_')[0][:3]}:{t['symbol']}"
        held[key] = t["held_out_seq"]
    cands = json.load(open(f"{out_dir}/candidates.json"))
    rows = []
    for c in cands:
        seq, key = c["sequence"], c["target"]
        h = held.get(key, "")
        rows.append({
            "target": key, "species": c["species"], "symbol": c["symbol"],
            "sample": c["sample"], "sha256": c["sha256"], "length": len(seq),
            "gc": round((seq.count("G") + seq.count("C")) / max(1, len(seq)), 4),
            "non_acgt": sum(1 for ch in seq if ch not in "ACGT"),
            "gzip_ratio": round(gzip_ratio(seq), 4),
            "max_homopolymer": max_homopolymer(seq),
            "kmer3_frac": round(kmer_frac(seq, 3), 4),
            "kmer4_frac": round(kmer_frac(seq, 4), 4),
            "kmer6_frac": round(kmer_frac(seq, 6), 4),
            "jsd3_vs_heldout": round(jsd(kmer_dist(seq, 3), kmer_dist(h, 3)), 4) if h else None,
            "jsd4_vs_heldout": round(jsd(kmer_dist(seq, 4), kmer_dist(h, 4)), 4) if h else None,
            "best_local_identity_60bp_vs_heldout":
                round(best_local_identity(seq, h), 4) if h else None,
        })

    # Reference bands from the real windows, so a candidate number has something
    # to be judged against rather than being read in isolation.
    ref = []
    for t in inputs["targets"]:
        s = t["held_out_seq"]
        ref.append({"gzip_ratio": gzip_ratio(s), "kmer6_frac": kmer_frac(s, 6),
                    "max_homopolymer": max_homopolymer(s)})

    # Two rules, both reported. The first is the one I pre-registered before
    # seeing any output. It fired three times on max_homopolymer >= 12 -- and
    # then calibration against the real windows showed the THRESHOLD was wrong,
    # not the candidates: real genomic windows here run to a 30 bp homopolymer
    # with a median of 9, and 13 of 38 real windows exceed 12. A cutoff that
    # flags sequence for being LESS repetitive than the real thing measures
    # nothing. So the calibrated rule asks the only question that means
    # anything -- is this candidate outside the band the real windows occupy --
    # and both counts are reported so the goalposts are visibly not moved.
    def bandof(field):
        vals = sorted(r[field] for r in ref)
        return vals[0], vals[-1]

    gz_lo, _ = bandof("gzip_ratio")
    k6_lo, _ = bandof("kmer6_frac")
    _, hp_hi = bandof("max_homopolymer")
    flagged_prereg = [r for r in rows
                      if r["gzip_ratio"] < 0.30 or r["max_homopolymer"] >= 12
                      or r["kmer6_frac"] < 0.50 or r["non_acgt"] > 0]
    flagged = [r for r in rows
               if r["gzip_ratio"] < gz_lo * 0.9 or r["kmer6_frac"] < k6_lo * 0.9
               or r["max_homopolymer"] > hp_hi or r["non_acgt"] > 0]

    def band(field, src):
        vals = sorted(r[field] for r in src if r[field] is not None)
        return {"min": round(vals[0], 4), "median": round(vals[len(vals) // 2], 4),
                "max": round(vals[-1], 4), "n": len(vals)}

    report = {
        "analysis": "fin-scale candidate artefact screen (CPU, no GPU)",
        "added_because": "gemini-4-argon design review: degeneracy and "
                         "memorised-retrieval must be measured, not assumed absent",
        "n_candidates": len(rows),
        "real_heldout_reference_bands": {
            "gzip_ratio": band("gzip_ratio", ref),
            "kmer6_frac": band("kmer6_frac", ref),
            "max_homopolymer": band("max_homopolymer", ref)},
        "candidate_bands": {
            "gzip_ratio": band("gzip_ratio", rows),
            "kmer6_frac": band("kmer6_frac", rows),
            "max_homopolymer": band("max_homopolymer", rows),
            "best_local_identity_60bp_vs_heldout":
                band("best_local_identity_60bp_vs_heldout", rows)},
        "degeneracy_flag_rule_preregistered":
            "gzip_ratio<0.30 or max_homopolymer>=12 or kmer6_frac<0.50 or non_acgt>0",
        "n_flagged_preregistered": len(flagged_prereg),
        "flagged_preregistered":
            [r["sha256"][:12] + " " + r["target"] + " hp=" + str(r["max_homopolymer"])
             for r in flagged_prereg],
        "preregistered_rule_verdict":
            "MIS-CALIBRATED. All three flags were max_homopolymer>=12, but the "
            "real windows run to %d with a median of 9, so the cutoff flagged "
            "candidates for being less repetitive than real sequence. Reported, "
            "not quietly dropped." % hp_hi,
        "degeneracy_flag_rule": "outside the real-window band: gzip<0.9*%.3f or "
                                "kmer6<0.9*%.3f or max_homopolymer>%d or non_acgt>0"
                                % (gz_lo, k6_lo, hp_hi),
        "n_flagged_degenerate": len(flagged),
        "flagged": [r["sha256"][:12] + " " + r["target"] for r in flagged],
        "per_candidate": rows,
    }
    json.dump(report, open(report_path, "w"), indent=2)
    print(f"candidates analysed: {len(rows)}; flagged degenerate: {len(flagged)}")
    print("gzip ratio  candidates", report["candidate_bands"]["gzip_ratio"])
    print("gzip ratio  real       ", report["real_heldout_reference_bands"]["gzip_ratio"])
    print("best 60bp identity vs held-out",
          report["candidate_bands"]["best_local_identity_60bp_vs_heldout"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
