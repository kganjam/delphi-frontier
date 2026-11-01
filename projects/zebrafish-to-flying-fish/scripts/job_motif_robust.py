#!/usr/bin/env python3
"""Robustness re-run of the motif scan, fixing two weaknesses of the first one.

Weakness 1: only 2 dinucleotide shuffles per window, and the shuffle-to-shuffle spread in the
first run (median 21, max 68 motifs) was comparable to the effect itself, so the per-window
pairing was underpowered.
Weakness 2: per-motif thresholds were calibrated on a POOLED set of 38 GC-matched random
sequences. A pooled threshold can make the effect SIZE scale with a window's GC even though the
real-vs-own-shuffle comparison is composition-controlled by construction.

This run: each real window gets its OWN null from N dinucleotide-preserving shuffles of itself.
Per motif and per window, the threshold is the 95th percentile over that window's own shuffles,
so no threshold is shared across windows and GC cannot leak in through the threshold. The
statistic is the per-window z-score of the real count against its own shuffle distribution.

Shuffling is Altschul-Erikson (Euler-path) with a declared seed, and the job VERIFIES that every
shuffle preserves the exact doublet counts of its source. If any shuffle fails that check the run
aborts rather than reporting.

Pre-registered before running: the comparison is within each species separately, never across
them. A null result is reportable.

Run: python3 motif_robust.py FASTA JASPAR N_SHUFFLES SEED
"""
import json
import math
import random
import sys
from collections import Counter, defaultdict

import numpy as np

FA, JAS, NSH, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
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


def doublets(s):
    return Counter(s[i:i + 2] for i in range(len(s) - 1))


def dinuc_shuffle(s, rng):
    """Altschul-Erikson: random Eulerian path through the doublet graph."""
    if len(s) < 3:
        return s
    first, last = s[0], s[-1]
    edges = defaultdict(list)
    for i in range(len(s) - 1):
        edges[s[i]].append(s[i + 1])
    verts = list(edges)
    for _ in range(2000):
        cand = {v: lst[:] for v, lst in edges.items()}
        for v in cand:
            rng.shuffle(cand[v])
        # the chosen last-edge of each vertex must lead to `last` (spanning tree condition)
        ok = True
        for v in verts:
            if v == last:
                continue
            seen, cur = set(), v
            while cur != last:
                if cur in seen or not cand.get(cur):
                    ok = False
                    break
                seen.add(cur)
                cur = cand[cur][-1]
            if not ok:
                break
        if not ok:
            continue
        walk, cur = [first], first
        pools = {v: lst[:] for v, lst in cand.items()}
        total = len(s) - 1
        for _ in range(total):
            nxt = pools[cur].pop(0) if len(pools[cur]) > 1 else pools[cur].pop()
            walk.append(nxt)
            cur = nxt
        out = "".join(walk)
        if len(out) == len(s) and doublets(out) == doublets(s):
            return out
    raise SystemExit("ZF2FF_FATAL=dinuc_shuffle_failed")


seqs = read_fasta(FA)
real = [(n, s) for n, s in seqs if n.startswith("REAL|")]
motifs = read_jaspar(JAS)
print(f"ZF2FF_N_REAL={len(real)} ZF2FF_N_MOTIFS={len(motifs)} ZF2FF_N_SHUFFLES={NSH} ZF2FF_SEED={SEED}")

PSEUDO = 0.25


def encode(s):
    a = np.full(len(s), -1, dtype=np.int8)
    raw = np.frombuffer(s.encode(), dtype=np.uint8)
    for b, i in IDX.items():
        a[raw == ord(b)] = i
    return a


def best_two_strand(arr, pwm_lo):
    def one(lo):
        w = lo.shape[1]
        n = len(arr) - w + 1
        if n <= 0:
            return -math.inf
        win = np.lib.stride_tricks.sliding_window_view(arr, w)
        ok = (win >= 0).all(axis=1)
        if not ok.any():
            return -math.inf
        return float(pwm_lo_sum(win[ok], lo))

    def pwm_lo_sum(win, lo):
        return lo[win, np.arange(lo.shape[1])].sum(axis=1).max()

    return max(one(pwm_lo), one(pwm_lo[::-1, ::-1]))


def scores_for(s):
    arr = encode(s)
    valid = arr[arr >= 0]
    bg = np.bincount(valid, minlength=4).astype(float)
    bg = np.maximum(bg / bg.sum(), 1e-6)
    out = np.empty(len(motifs))
    for k, (_, pfm) in enumerate(motifs):
        p = (pfm + PSEUDO) / (pfm.sum(axis=0) + 4 * PSEUDO)
        out[k] = best_two_strand(arr, np.log2(p / bg[:, None]))
    return out


rows = []
verified = 0
for name, s in real:
    rng = random.Random(SEED ^ (hash(name) & 0xFFFFFFFF))
    rng2 = random.Random(SEED + len(s))
    shuffles = []
    for i in range(NSH):
        sh = dinuc_shuffle(s, rng)
        assert doublets(sh) == doublets(s), name
        verified += 1
        shuffles.append(sh)
    rs = scores_for(s)
    ms = np.vstack([scores_for(x) for x in shuffles])
    thresh = np.percentile(ms, 95, axis=0)
    real_count = int((rs > thresh).sum())
    shuf_counts = [int((ms[i] > thresh).sum()) for i in range(NSH)]
    mu = float(np.mean(shuf_counts))
    sd = float(np.std(shuf_counts, ddof=1))
    z = (real_count - mu) / sd if sd > 0 else float("nan")
    label = name.split("|")[1]
    rows.append({"label": label, "real": real_count, "shuffle_mean": round(mu, 2),
                 "shuffle_sd": round(sd, 2), "z": round(z, 3) if z == z else None,
                 "diff": round(real_count - mu, 2)})
    print(f"ZF2FF_WINDOW {label} real={real_count} shuf_mean={mu:.1f} shuf_sd={sd:.1f} z={z:.2f}")

print(f"ZF2FF_SHUFFLES_DOUBLET_VERIFIED={verified}")


def agg(sel, tag):
    v = [r["diff"] for r in rows if r["label"].startswith(sel)]
    zs = [r["z"] for r in rows if r["label"].startswith(sel) and r["z"] is not None]
    n = len(v)
    m = sum(v) / n
    sd = (sum((x - m) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else float("nan")
    se = sd / math.sqrt(n) if n > 1 else float("nan")
    return {"set": tag, "n": n, "mean_diff": round(m, 3),
            "se": round(se, 3) if se == se else None,
            "t": round(m / se, 3) if se and se == se and se > 0 else None,
            "ci95": [round(m - 1.96 * se, 2), round(m + 1.96 * se, 2)] if se == se else None,
            "windows_positive": sum(1 for x in v if x > 0),
            "mean_z": round(sum(zs) / len(zs), 3) if zs else None,
            "windows_z_gt_2": sum(1 for x in zs if x > 2)}


print("ZF2FF_RESULT_BEGIN")
print(json.dumps({"per_window": rows,
                  "zebrafish_only": agg("dan", "zebrafish"),
                  "flyingfish_only": agg("hir", "flying fish"),
                  "note": ("Each window's null is its own dinucleotide shuffles, so no threshold is "
                           "shared between windows and composition cannot enter through the "
                           "threshold. The two species are aggregated separately and never compared, "
                           "per the handoff's stated confounds.")}, indent=1))
print("ZF2FF_RESULT_END")
