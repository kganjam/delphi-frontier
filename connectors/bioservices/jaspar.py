"""JASPAR CORE position frequency matrices.

Supplies the motif models for a composition diagnostic that runs with **no
sequence model in the loop**. That independence is the point: Evo 2 scoring its
own generations is not an independent assessment of them, and a PWM scan is.

A motif hit is a statement about sequence composition. It is **not** evidence of
binding, of expression, or of regulatory function.
"""

from __future__ import annotations

import os
import urllib.request

from connectors.bioservices.receipts import RetrievalReceipt, sha256_file, utc_now

RELEASE = "JASPAR2024_CORE_vertebrates_non-redundant"
URL = f"https://jaspar.elixir.no/download/data/2024/CORE/{RELEASE}_pfms_jaspar.txt"
USER_AGENT = "delphi-frontier-bioservices/0.1 (public-data design study)"
# JASPAR data is released under CC BY-NC 4.0.
JASPAR_LICENSE = "CC BY-NC 4.0 (JASPAR)"
BASES = "ACGT"


class JasparError(RuntimeError):
    pass


def fetch_pfms(dest_dir: str, timeout: int = 120) -> tuple[str, RetrievalReceipt]:
    """Download the bulk PFM file once; reuse it if already present."""
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, f"{RELEASE}_pfms_jaspar.txt")
    reused = os.path.exists(path) and os.path.getsize(path) > 0
    if not reused:
        req = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(path, "wb") as out:
            out.write(resp.read())
    receipt = RetrievalReceipt(
        source_id="jaspar.core.vertebrates",
        url=URL, state="retrieved", retrieved_utc=utc_now(),
        size_bytes=os.path.getsize(path), sha256=sha256_file(path),
        media_type="text/plain", license=JASPAR_LICENSE, version=RELEASE,
        notes=["reused cached file" if reused else "downloaded over anonymous HTTPS"],
    )
    return path, receipt


def parse_pfms(path: str) -> dict[str, dict]:
    """Parse the JASPAR flat format into {matrix_id: {name, counts}}.

    ``counts`` is a list of per-position dicts over ACGT. The four rows of a
    matrix must have equal length, which is checked rather than assumed: a
    ragged matrix would silently truncate a motif.
    """
    out: dict[str, dict] = {}
    matrix_id = name = None
    rows: dict[str, list[float]] = {}
    with open(path) as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if matrix_id:
                    out[matrix_id] = _finish(matrix_id, name, rows)
                parts = line[1:].split()
                matrix_id = parts[0]
                name = parts[1] if len(parts) > 1 else parts[0]
                rows = {}
                continue
            base = line[0].upper()
            if base not in BASES:
                raise JasparError(f"{matrix_id}: unexpected row label {line[0]!r}")
            inner = line[line.index("[") + 1 : line.rindex("]")] if "[" in line else line[1:]
            rows[base] = [float(v) for v in inner.split()]
    if matrix_id:
        out[matrix_id] = _finish(matrix_id, name, rows)
    if not out:
        raise JasparError(f"{path}: no matrices parsed")
    return out


def _finish(matrix_id: str, name: str | None, rows: dict[str, list[float]]) -> dict:
    if set(rows) != set(BASES):
        raise JasparError(f"{matrix_id}: rows {sorted(rows)} but expected {list(BASES)}")
    widths = {len(v) for v in rows.values()}
    if len(widths) != 1:
        raise JasparError(f"{matrix_id}: ragged rows with widths {sorted(widths)}")
    width = widths.pop()
    counts = [{b: rows[b][i] for b in BASES} for i in range(width)]
    return {"matrix_id": matrix_id, "name": name, "width": width, "counts": counts}
