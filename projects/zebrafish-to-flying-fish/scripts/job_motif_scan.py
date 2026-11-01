#!/usr/bin/env python3
"""Log-odds PWM scan, pre-registered design (see build_motif_input.py docstring).

Thresholds: per motif, the 95th percentile of best two-strand log-odds scores over the 38
GC-matched random sequences ONLY. Comparison: 19 real windows vs 38 dinucleotide shuffles,
paired per window against the mean of its own 2 shuffles. Background for the log-odds is each
sequence's own mononucleotide composition, so a composition difference cannot create a score
difference. No cross-species comparison. No per-gene or per-motif inference.
"""
import json
import math
import sys

import numpy as np

FA, JAS = sys.argv[1], sys.argv[2]
IDX = {"A": 0, "C": 1, "G": 2, "T": 3}


def read_fasta(p):
    out, name, buf = [], None, []
    for line in open(p):
        line = line.strip()
        if line.startswith(">"):
            if name:
                out.append((name, "".join(buf)))
            name, buf = line[1:], []
        else:
            buf.append(line)
    if name:
        out.append((name, "".join(buf)))
    return out


def read_jaspar(p):
    motifs, name, rows = [], None, []
    for line in open(p):
        line = line.rstrip()
        if line.startswith(">"):
            if name and len(rows) == 4:
                motifs.append((name, np.array(rows, dtype=float)))
            name, rows = line[1:].strip(), []
        elif line:
            nums = [float(x) for x in line.replace("[", " ").replace("]", " ").split()[1:]
                    if x.replace(".", "", 1).replace("-", "", 1).isdigit()]
            if nums:
                rows.append(nums)
    if name and len(rows) == 4:
        motifs.append((name, np.array(rows, dtype=float)))
    return motifs


seqs = read_fasta(FA)
motifs = read_jaspar(JAS)
print(f"ZF2FF_N_SEQS={len(seqs)} ZF2FF_N_MOTIFS={len(motifs)}")
widths = [m.shape[1] for _, m in motifs]
print(f"ZF2FF_MOTIF_WIDTH_MIN={min(widths)} MAX={max(widths)}")

# encode sequences; non-ACGT becomes -1 and any window containing one is skipped
enc = {}
for n, s in seqs:
    a = np.full(len(s), -1, dtype=np.int8)
    for b, i in IDX.items():
        a[np.frombuffer(s.encode(), dtype=np.uint8) == ord(b)] = i
    enc[n] = a

PSEUDO = 0.25


def best_score(arr, pwm_lo):
    w = pwm_lo.shape[1]
    n = len(arr) - w + 1
    if n <= 0:
        return -math.inf
    idx = np.lib.stride_tricks.sliding_window_view(arr, w)
    ok = (idx >= 0).all(axis=1)
    if not ok.any():
        return -math.inf
    idx = idx[ok]
    cols = np.arange(w)
    return float(pwm_lo[idx, cols].sum(axis=1).max())


def revcomp_lo(pwm_lo):
    return pwm_lo[::-1, ::-1]


best = {}  # (seq, motif) -> best two-strand score
for name, arr in enc.items():
    valid = arr[arr >= 0]
    bg = np.bincount(valid, minlength=4).astype(float)
    bg = np.maximum(bg / bg.sum(), 1e-6)
    scores = np.empty(len(motifs), dtype=float)
    for k, (mn, pfm) in enumerate(motifs):
        p = (pfm + PSEUDO) / (pfm.sum(axis=0) + 4 * PSEUDO)
        lo = np.log2(p / bg[:, None])
        scores[k] = max(best_score(arr, lo), best_score(arr, revcomp_lo(lo)))
    best[name] = scores

kinds = {}
for n in best:
    kinds[n] = "REAL" if n.startswith("REAL|") else ("SHUF" if n.startswith("SHUF|") else "GCRAND")
cal = [n for n in best if kinds[n] == "GCRAND"]
real = [n for n in best if kinds[n] == "REAL"]
shuf = [n for n in best if kinds[n] == "SHUF"]
print(f"ZF2FF_SET_SIZES real={len(real)} shuf={len(shuf)} gcrand={len(cal)}")

M = np.vstack([best[n] for n in cal])
thresh = np.percentile(M, 95, axis=0)
print(f"ZF2FF_THRESHOLD_SOURCE=gc_matched_random_p95 n={len(cal)}")


def count_pass(n):
    return int((best[n] > thresh).sum())


def label(n):
    return n.split("|")[1]


real_by_label = {label(n): count_pass(n) for n in real}
shuf_by_label = {}
for n in shuf:
    shuf_by_label.setdefault(label(n), []).append(count_pass(n))

pairs = []
for lab, rc in sorted(real_by_label.items()):
    sc = shuf_by_label.get(lab, [])
    if not sc:
        continue
    pairs.append({"label": lab, "real_motifs_passing": rc,
                  "shuffle_motifs_passing": sc,
                  "shuffle_mean": sum(sc) / len(sc),
                  "diff_real_minus_shuffle_mean": rc - sum(sc) / len(sc)})

d = np.array([p["diff_real_minus_shuffle_mean"] for p in pairs], dtype=float)
n = len(d)
mean = float(d.mean())
sd = float(d.std(ddof=1)) if n > 1 else float("nan")
se = sd / math.sqrt(n) if n > 1 else float("nan")
t = mean / se if se and se > 0 else float("nan")
pos = int((d > 0).sum())
neg = int((d < 0).sum())
print("ZF2FF_RESULT_BEGIN")
print(json.dumps({
    "n_paired_windows": n,
    "mean_diff_real_minus_shuffle": round(mean, 4),
    "sd": round(sd, 4) if sd == sd else None,
    "se": round(se, 4) if se == se else None,
    "t_statistic": round(t, 4) if t == t else None,
    "ci95_approx": [round(mean - 1.96 * se, 4), round(mean + 1.96 * se, 4)] if se == se else None,
    "windows_real_gt_shuffle": pos,
    "windows_real_lt_shuffle": neg,
    "windows_tied": n - pos - neg,
    "per_window": pairs,
}, indent=1))
print("ZF2FF_RESULT_END")
