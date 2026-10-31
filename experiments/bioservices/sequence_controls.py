"""Composition-matched negative controls for DNA sequences.

Shared by the GPU generation job and the CPU diagnostics so both arms build
their controls with exactly the same code. A control computed two slightly
different ways is not a control.
"""

from __future__ import annotations

import random


def dinucleotide_shuffle(seq: str, rng: random.Random, max_attempts: int = 200) -> str:
    """Shuffle preserving EXACT dinucleotide counts, by Eulerian-walk rejection.

    A mononucleotide shuffle preserves only base composition, which is too weak
    a control for DNA: dinucleotide content, CpG above all, carries much of what
    a motif scan responds to. Preserving it means a surviving difference is not
    merely a difference in dinucleotide composition.

    **A naive version of this is wrong and was used here before being caught.**
    Treating the dinucleotides as edges of a multigraph and walking them in
    random order gets stuck whenever a vertex runs out of outgoing edges early;
    falling back to a random base at that point silently breaks the very
    property the control exists to preserve. Measured on a real 1 kb promoter:
    the naive version deviated by up to 6 of 999 dinucleotides and did not even
    preserve mononucleotide composition.

    The fix is rejection sampling. A random edge ordering is accepted only if
    the walk from ``seq[0]`` consumes every edge, which is exactly the condition
    for an Eulerian path and therefore for identical dinucleotide counts. A walk
    that stalls is discarded, not patched. The result is verified before being
    returned, so the guarantee is checked rather than argued.
    """
    if len(seq) < 2:
        return seq
    for _ in range(max_attempts):
        edges: dict[str, list[str]] = {}
        for a, b in zip(seq, seq[1:]):
            edges.setdefault(a, []).append(b)
        for v in edges.values():
            rng.shuffle(v)
        out, cur = [seq[0]], seq[0]
        for _ in range(len(seq) - 1):
            bucket = edges.get(cur)
            if not bucket:
                break           # stalled: this ordering is not an Eulerian path
            nxt = bucket.pop()
            out.append(nxt)
            cur = nxt
        if len(out) == len(seq):
            candidate = "".join(out)
            if _dinucleotide_counts(candidate) == _dinucleotide_counts(seq):
                return candidate
    raise RuntimeError(
        f"no dinucleotide-preserving shuffle found in {max_attempts} attempts "
        f"for a {len(seq)} bp sequence"
    )


def _dinucleotide_counts(seq: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for i in range(len(seq) - 1):
        k = seq[i : i + 2]
        counts[k] = counts.get(k, 0) + 1
    return counts


def gc_matched_random(length: int, gc: float, rng: random.Random) -> str:
    """Independent bases drawn at a target GC fraction."""
    half_gc, half_at = gc / 2, (1 - gc) / 2
    return "".join(rng.choices("GCAT", weights=[half_gc, half_gc, half_at, half_at], k=length))


def gc_fraction(seq: str) -> float:
    return (seq.count("G") + seq.count("C")) / len(seq) if seq else 0.0
