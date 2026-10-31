"""UCSC Genome Browser API — an independent second read of reference sequence.

Ensembl and UCSC distribute the *same* zebrafish assembly under two names
(GRCz11 and danRer11). Fetching a region from both and requiring agreement
checks that the coordinates being used mean what they are assumed to mean. It
is the same discipline the Kir2.1 work applied by checking a DMS-derived
reference against UniProt: a single source can only ever be self-consistent.

The two differ in convention, which is exactly what makes the check worth
running rather than assuming:

- UCSC is **0-based, half-open**; Ensembl is **1-based, inclusive**.
- UCSC always returns the forward strand; Ensembl orients by requested strand.

Both are handled here, so a disagreement means a real disagreement.
"""

from __future__ import annotations

import json
import urllib.request

BASE = "https://api.genome.ucsc.edu"
USER_AGENT = "delphi-frontier-bioservices/0.1 (public-data design study)"
_COMPLEMENT = str.maketrans("ACGTN", "TGCAN")


class UcscError(RuntimeError):
    pass


def reverse_complement(seq: str) -> str:
    return seq.translate(_COMPLEMENT)[::-1]


def sequence(genome: str, chromosome: str, lo_1based: int, hi_1based: int,
             strand: int = 1, timeout: int = 60) -> str:
    """Reference sequence for a 1-based inclusive interval, oriented by strand.

    Takes Ensembl-style coordinates and converts them, so a caller never has to
    remember which end is half-open.
    """
    chrom = chromosome if chromosome.startswith("chr") else f"chr{chromosome}"
    start = lo_1based - 1            # 1-based inclusive -> 0-based half-open
    url = f"{BASE}/getData/sequence?genome={genome};chrom={chrom};start={start};end={hi_1based}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode())
    if "dna" not in payload:
        raise UcscError(f"{url}: no dna field; keys were {sorted(payload)}")
    seq = payload["dna"].upper()
    expected = hi_1based - lo_1based + 1
    if len(seq) != expected:
        raise UcscError(f"{url}: expected {expected} bases, received {len(seq)}")
    return reverse_complement(seq) if strand == -1 else seq


def agrees(ensembl_seq: str, ucsc_seq: str) -> dict:
    """Compare two reads of the same region without deciding what a mismatch means."""
    identical = ensembl_seq == ucsc_seq
    out = {"identical": identical, "length_ensembl": len(ensembl_seq), "length_ucsc": len(ucsc_seq)}
    if not identical and len(ensembl_seq) == len(ucsc_seq):
        diffs = [i + 1 for i, (a, b) in enumerate(zip(ensembl_seq, ucsc_seq)) if a != b]
        out["n_differences"] = len(diffs)
        out["first_difference_offsets"] = diffs[:10]
    return out
