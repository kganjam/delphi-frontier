"""Transcription-factor motif density: a COMPOSITION DIAGNOSTIC, not a function.

What this computes and what it does not:

- It computes how often a sequence contains windows matching known vertebrate
  TF position weight matrices. That is a statement about **composition**.
- It is **not** binding. Binding depends on chromatin state, cofactors,
  concentration and cell type, none of which a PWM scan sees.
- It is **not** expression, accessibility or regulatory function. Nothing here
  licenses a functional claim, and none will be made without an assay.

Its value is independence: no sequence model is in the loop, so it can say
something about a generated candidate that the generating model's own
likelihood cannot. A model scoring its own output is not an assessment of it.

**The GC confound is made explicit rather than left implicit.** Motif density
rises with GC content for most vertebrate matrices, so density is reported under
two backgrounds: uniform (sensitive to GC, which is sometimes what you want) and
sequence-matched (GC-controlled). A difference that survives the second is not
merely a difference in base composition.
"""

from __future__ import annotations

import math

import numpy as np

BASES = "ACGT"
_INDEX = {b: i for i, b in enumerate(BASES)}
_COMPLEMENT = {0: 3, 1: 2, 2: 1, 3: 0}
PSEUDOCOUNT = 0.25
DEFAULT_THRESHOLD = 0.85


def encode(seq: str) -> np.ndarray:
    """Sequence to integer codes; anything outside ACGT becomes -1 and is skipped."""
    return np.array([_INDEX.get(c, -1) for c in seq.upper()], dtype=np.int8)


def background_from(seq: str) -> np.ndarray:
    """Per-sequence mononucleotide background, used for the GC-controlled read."""
    codes = encode(seq)
    counts = np.array([(codes == i).sum() for i in range(4)], dtype=float)
    if counts.sum() == 0:
        return np.full(4, 0.25)
    return counts / counts.sum()


def log_odds(pfm_counts: list[dict], background: np.ndarray) -> np.ndarray:
    """PFM counts to a log-odds matrix of shape (width, 4)."""
    w = len(pfm_counts)
    m = np.zeros((w, 4))
    for i, col in enumerate(pfm_counts):
        total = sum(col[b] for b in BASES) + 4 * PSEUDOCOUNT
        for j, b in enumerate(BASES):
            p = (col[b] + PSEUDOCOUNT) / total
            m[i, j] = math.log(p / background[j])
    return m


def _revcomp_matrix(m: np.ndarray) -> np.ndarray:
    out = np.empty_like(m)
    for j in range(4):
        out[:, j] = m[::-1, _COMPLEMENT[j]]
    return out


def scan(codes: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Best-strand score at every window position."""
    w = matrix.shape[0]
    n = codes.size - w + 1
    if n <= 0:
        return np.empty(0)
    windows = np.lib.stride_tricks.sliding_window_view(codes, w)
    valid = (windows >= 0).all(axis=1)
    rows = np.arange(w)
    fwd = np.where(valid, matrix[rows, np.clip(windows, 0, 3)].sum(axis=1), -np.inf)
    rc = _revcomp_matrix(matrix)
    rev = np.where(valid, rc[rows, np.clip(windows, 0, 3)].sum(axis=1), -np.inf)
    return np.maximum(fwd, rev)


def relative_hits(seq: str, pfms: dict, background: np.ndarray,
                  threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Count windows scoring at or above ``threshold`` of each matrix's range.

    The relative score is the standard (score − min) / (max − min), which makes
    matrices of different widths and information content comparable.
    """
    codes = encode(seq)
    total_hits, matrices_hit, per_matrix = 0, 0, {}
    for mid, pfm in pfms.items():
        m = log_odds(pfm["counts"], background)
        lo, hi = m.min(axis=1).sum(), m.max(axis=1).sum()
        if not np.isfinite(lo) or hi <= lo:
            continue
        scores = scan(codes, m)
        if scores.size == 0:
            continue
        rel = (scores - lo) / (hi - lo)
        n = int((rel >= threshold).sum())
        if n:
            total_hits += n
            matrices_hit += 1
            per_matrix[mid] = {"name": pfm["name"], "hits": n}
    kb = len(seq) / 1000.0
    return {
        "length": len(seq),
        "threshold": threshold,
        "total_hits": total_hits,
        "hits_per_kb": total_hits / kb if kb else 0.0,
        "distinct_matrices_hit": matrices_hit,
        "per_matrix": per_matrix,
    }


def composition(seq: str) -> dict:
    """GC and CpG observed/expected — the confounds a motif count rides on."""
    s = seq.upper()
    n = len(s)
    g, c = s.count("G"), s.count("C")
    cg = sum(1 for i in range(n - 1) if s[i] == "C" and s[i + 1] == "G")
    expected = (c * g) / (n - 1) if n > 1 and c and g else 0.0
    return {
        "length": n,
        "gc": (g + c) / n if n else 0.0,
        "cpg_count": cg,
        "cpg_obs_exp": (cg / expected) if expected else None,
    }


def diagnose(seq: str, pfms: dict, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Both reads: uniform background, and the sequence's own GC background."""
    uniform = relative_hits(seq, pfms, np.full(4, 0.25), threshold)
    matched = relative_hits(seq, pfms, background_from(seq), threshold)
    return {
        "composition": composition(seq),
        "uniform_background": {k: v for k, v in uniform.items() if k != "per_matrix"},
        "gc_matched_background": {k: v for k, v in matched.items() if k != "per_matrix"},
        "top_matrices_uniform": sorted(
            ({"matrix_id": k, **v} for k, v in uniform["per_matrix"].items()),
            key=lambda r: -r["hits"])[:15],
        "kind": "composition diagnostic; not binding, expression or function",
    }


def information_content(pfm: dict) -> float:
    """Total information content of a PFM in bits, against a uniform background."""
    total = 0.0
    for col in pfm["counts"]:
        n = sum(col.values())
        if n <= 0:
            continue
        for b in BASES:
            p = (col[b] + PSEUDOCOUNT) / (n + 4 * PSEUDOCOUNT)
            total += p * math.log2(p / 0.25)
    return total


def select_by_information(pfms: dict, top_fraction: float) -> dict:
    """The most informative ``top_fraction`` of matrices.

    Low-information matrices match almost anywhere, so including all 879 makes an
    aggregate count a measure of sequence length rather than of sequence content.
    """
    ics = sorted((information_content(p), k) for k, p in pfms.items())
    cut = ics[int((1 - top_fraction) * len(ics))][0]
    return {k: p for k, p in pfms.items() if information_content(p) >= cut}


def shuffle_null_enrichment(seq: str, pfms: dict, rng, n_shuffles: int = 10,
                            threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Motif density against the sequence's OWN dinucleotide-shuffle null.

    This is the form worth reporting. Raw density across a large matrix set does
    not distinguish real promoter-proximal zebrafish sequence from
    composition-matched controls -- measured here at eight thresholds from 0.85
    to 0.98, with real/control ratios of 1.02 to 1.09 throughout. An absolute
    count is therefore close to meaningless on its own.

    Comparing a sequence against shuffles of *itself* holds length, base
    composition and dinucleotide composition fixed, so what remains is motif
    content beyond composition. The z-score is reported with the null's spread,
    and a null with zero spread yields ``None`` rather than an infinite z.
    """
    from experiments.bioservices.sequence_controls import dinucleotide_shuffle

    bg = np.full(4, 0.25)
    observed = relative_hits(seq, pfms, bg, threshold)["total_hits"]
    null = [relative_hits(dinucleotide_shuffle(seq, rng), pfms, bg, threshold)["total_hits"]
            for _ in range(n_shuffles)]
    mean = float(np.mean(null))
    sd = float(np.std(null, ddof=1)) if len(null) > 1 else 0.0
    return {
        "observed_hits": observed,
        "null_mean": mean,
        "null_sd": sd,
        "n_shuffles": n_shuffles,
        "z": ((observed - mean) / sd) if sd > 0 else None,
        "ratio": (observed / mean) if mean else None,
        "n_matrices": len(pfms),
        "threshold": threshold,
        "kind": "composition diagnostic against a dinucleotide-preserving null; not function",
    }


def _np_uniform() -> np.ndarray:
    """Uniform background, exposed so callers need not import numpy themselves."""
    return np.full(4, 0.25)
