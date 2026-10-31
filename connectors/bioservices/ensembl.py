"""Ensembl REST: gene coordinates and genomic sequence, with receipts.

Used here to assemble a *frozen, public, benign* input set for sequence design.
Only reference genome coordinates and reference sequence are read; no variant,
sample or individual-level data is touched.

Strand is handled by Ensembl itself: a region requested with the gene's strand
comes back oriented 5'->3' in gene orientation, so "upstream" means upstream of
the transcription start site regardless of which strand the gene sits on. That
is the detail most likely to be silently wrong, so it is requested explicitly
rather than reverse-complemented by hand.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from connectors.bioservices.receipts import RetrievalReceipt, sha256_text, utc_now

BASE = "https://rest.ensembl.org"
USER_AGENT = "delphi-frontier-bioservices/0.1 (public-data design study)"
# Ensembl data is distributed under a no-restriction licence (Apache-2.0 for code).
ENSEMBL_LICENSE = "Ensembl data: free and unrestricted use (EMBL-EBI terms)"
VALID_BASES = set("ACGT")


class EnsemblError(RuntimeError):
    pass


@dataclass(frozen=True)
class Gene:
    symbol: str
    gene_id: str
    chromosome: str
    start: int
    end: int
    strand: int
    description: str

    @property
    def tss(self) -> int:
        """Forward-strand coordinate of the transcription start site."""
        return self.start if self.strand == 1 else self.end

    def upstream_region(self, distance: int) -> tuple[int, int]:
        """Forward-strand (lo, hi) of the ``distance`` bp immediately 5' of the TSS."""
        if self.strand == 1:
            return self.start - distance, self.start - 1
        return self.end + 1, self.end + distance


_last_request = 0.0
MIN_INTERVAL = 0.35  # Ensembl asks callers to stay well under 15 requests/second.


TRANSIENT = (429, 500, 502, 503, 504)


def _get(path: str, accept: str = "application/json", retries: int = 2,
         timeout: int = 20) -> str:
    """A few bounded, backed-off retries on a transient failure.

    Ensembl answers 429 when a caller is too fast and 500/502/503/504 when it is
    unwell; all were observed from this host within minutes of each other, with
    the same request succeeding in between. Retries are capped and spaced, and
    Retry-After is honoured, so this stays polite to someone else's public
    service rather than becoming a retry storm.

    **This applies to input acquisition only.** A measured run retries nothing:
    a fetch that fails there stops the run and is reported, because a result
    that needed coaxing out of a flaky service should say so.
    """
    global _last_request
    import time

    for attempt in range(retries + 1):
        gap = time.time() - _last_request
        if gap < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - gap)
        req = urllib.request.Request(
            f"{BASE}{path}", headers={"Accept": accept, "User-Agent": USER_AGENT}
        )
        try:
            _last_request = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode()
        except urllib.error.HTTPError as exc:
            if exc.code not in TRANSIENT or attempt == retries:
                raise
            wait = float(exc.headers.get("Retry-After", 0) or 0)
            time.sleep(min(max(wait, 2.0 * (attempt + 1)), 15.0))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            # A read timeout is the same transient condition as a 503 and arrives
            # as a different exception type. Observed from this host alongside
            # 500 and 503 on the same endpoint within minutes.
            if attempt == retries:
                raise EnsemblError(f"{path}: {type(exc).__name__}: {exc}") from exc
            time.sleep(2.0 * (attempt + 1))
    raise EnsemblError(f"{path}: unreachable")  # pragma: no cover


def assembly(species: str = "danio_rerio") -> dict:
    return json.loads(_get(f"/info/assembly/{species}?content-type=application/json"))


def lookup_symbol(symbol: str, species: str = "danio_rerio") -> Gene:
    j = json.loads(
        _get(f"/lookup/symbol/{species}/{symbol}?expand=0;content-type=application/json")
    )
    return Gene(
        symbol=symbol, gene_id=j["id"], chromosome=str(j["seq_region_name"]),
        start=int(j["start"]), end=int(j["end"]), strand=int(j["strand"]),
        description=j.get("description", ""),
    )


def sequence(chromosome: str, lo: int, hi: int, strand: int,
             species: str = "danio_rerio", retries: int = 2,
             timeout: int = 20) -> tuple[str, RetrievalReceipt]:
    """Reference sequence for a region, oriented by ``strand``.

    Refuses a sequence containing anything but ACGT. An assembly gap arrives as
    a run of N, which would otherwise be generated from or scored as if it were
    real sequence.
    """
    query = f"{chromosome}:{lo}..{hi}:{strand}"
    path = f"/sequence/region/{species}/{query}?content-type=application/json"
    j = json.loads(_get(path, retries=retries, timeout=timeout))
    seq = j["seq"].upper()
    if len(seq) != hi - lo + 1:
        raise EnsemblError(f"{query}: expected {hi - lo + 1} bases, received {len(seq)}")
    bad = sorted(set(seq) - VALID_BASES)
    if bad:
        raise EnsemblError(f"{query}: sequence contains non-ACGT characters {bad}")
    receipt = RetrievalReceipt(
        source_id=f"ensembl.sequence.{species}",
        url=f"{BASE}{path}",
        state="retrieved",
        retrieved_utc=utc_now(),
        size_bytes=len(seq),
        sha256=sha256_text(seq),
        media_type="application/json",
        license=ENSEMBL_LICENSE,
        version=None,
        notes=[j.get("id", ""), f"molecule={j.get('molecule')}"],
    )
    return seq, receipt


def gc_fraction(seq: str) -> float:
    return (seq.count("G") + seq.count("C")) / len(seq) if seq else 0.0
