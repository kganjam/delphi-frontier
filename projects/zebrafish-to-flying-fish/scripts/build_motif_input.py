#!/usr/bin/env python3
"""Build the motif-scan input: the Evo 2 harness's 19 held-out windows and their own scrambles.

The handoff (`messages/evo-to-zf2ff.md` §2) states that beating a dinucleotide shuffle shows
structure above k = 2 and nothing more specific, and names the missing follow-up: a motif scan of
these windows against the shuffles. This builds that input from their frozen input set, reusing
**their** sequences so the comparison is on the same objects their likelihood measure used.

Pre-registered before the job runs (written here, in the file that creates the input):
  - Unit of analysis: one window. n = 19 real, each with its own paired scramble.
  - Statistic: per sequence, the number of distinct motifs whose best two-strand log-odds score
    exceeds that motif's threshold. Thresholds are calibrated on the 38 GC-matched random
    sequences ONLY; the comparison is the 19 real windows vs the 38 dinucleotide shuffles. Using
    two separate control classes keeps the threshold out of the comparison.
  - Direction: if the windows carry motif-level structure, real > scramble. A null result is
    reportable and expected to be reported.
  - No per-gene or per-motif ranking will be treated as inferential: 19 windows, no power.
  - The flying-fish and zebrafish windows are NEVER compared to each other, per the handoff's
    §3 warning that the cross-species comparison is confounded three ways.

Run: python3 build_motif_input.py EVO_INPUT_SET.json EVO_SCORES.json OUT_FASTA OUT_LEDGER EVO_CONTROLS.json
"""
import hashlib
import json
import pathlib
import sys

EVOSET, SCORES = sys.argv[1], sys.argv[2]
OUT_FA, OUT_LED = pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4])
OUT_FA.parent.mkdir(parents=True, exist_ok=True)

evo = json.load(open(EVOSET))
scores = json.load(open(SCORES))

recs, ledger = [], []
by_label = {}
for t in evo["targets"]:
    sp = "dan" if t["assembly"].startswith("GRCz11") else "hir"  # match claude-evo's own label prefixes
    label = f"{sp}:{t['symbol']}"
    seq = t["held_out_seq"].upper()
    sha = hashlib.sha256(seq.encode()).hexdigest()
    assert sha == t["held_out_sha256"], (label, sha, t["held_out_sha256"])
    name = f"REAL|{label}|{t['region']}|strand{t['strand']:+d}"
    recs.append((name, seq))
    by_label[label] = sha
    ledger.append({"name": name, "kind": "real_held_out", "label": label, "species": t["species"],
                   "region": t["region"], "strand": t["strand"], "len": len(seq),
                   "sha256": sha, "gc": t.get("held_out_gc"),
                   "source": "claude-evo input set fin-scale-regulatory-2kb/v1, verbatim"})

# their control sequences, reused verbatim: 38 dinucleotide shuffles (the COMPARISON set) and
# 38 GC-matched random sequences (the independent THRESHOLD-CALIBRATION set, so that thresholds are
# never calibrated on the same sequences the real windows are compared against).
controls = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else []
counts = {"dinucleotide_shuffle": 0, "gc_matched_random": 0}
for i, c in enumerate(controls):
    k = c["kind"]
    if k not in counts:
        continue
    counts[k] += 1
    seq = c["sequence"].upper()
    name = f"{'SHUF' if k == 'dinucleotide_shuffle' else 'GCRAND'}|{c['target']}|{counts[k]}"
    recs.append((name, seq))
    ledger.append({"name": name, "kind": k, "label": c["target"], "species": c.get("species"),
                   "len": len(seq), "sha256": hashlib.sha256(seq.encode()).hexdigest(),
                   "their_of_field": c.get("of"),
                   "source": "claude-evo armA controls.json, verbatim"})
ledger.append({"note": "control counts reused", **counts})

OUT_FA.write_text("".join(f">{n}\n{s}\n" for n, s in recs))
blob = OUT_FA.read_bytes()
doc = {
    "scope": ("Input for a motif scan. The windows are claude-evo's, reused verbatim and hash-verified. "
              "A motif match is a sequence-pattern match, not a bound transcription factor, not an "
              "enhancer, and not evidence of expression or function."),
    "prereg": {
        "unit": "one window",
        "n_real": sum(1 for e in ledger if e.get("kind") == "real_held_out"),
        "statistic": "count of distinct motifs whose best two-strand log-odds score exceeds that motif's threshold, per sequence",
        "threshold_calibration_set": "the 38 GC-matched random sequences only, at the 95th percentile per motif",
        "comparison": "the 19 real windows vs the 38 dinucleotide shuffles, paired per window against the mean of its own 2 shuffles",
        "why_two_control_classes": "calibrating thresholds on the same shuffles the real windows are compared against would be circular, so calibration uses the GC-matched set and comparison uses the shuffles",
        "background_for_log_odds": "each sequence's own mononucleotide composition, so a composition difference cannot create a score difference",
        "direction_if_structure_present": "real > scramble",
        "null_result_is_reportable": True,
        "no_cross_species_comparison": "per the handoff's three stated confounds",
        "no_per_gene_or_per_motif_inference": "19 windows, no multiple-comparison power",
    },
    "n_sequences": len(recs),
    "fasta_bytes": len(blob),
    "fasta_sha256": hashlib.sha256(blob).hexdigest(),
    "entries": ledger,
}
OUT_LED.write_text(json.dumps(doc, indent=1) + "\n")
print(f"{len(recs)} sequences total ({sum(1 for e in ledger if e.get('kind') == 'real_held_out')} real), "
      f"{len(blob)} bytes, sha256 {doc['fasta_sha256']}")
print("their score-record kinds:", sorted({s.get('kind') for s in scores}))
print("sequences by kind:", {k: sum(1 for e in ledger if e.get('kind') == k)
                             for k in ('real_held_out', 'dinucleotide_shuffle', 'gc_matched_random')})
