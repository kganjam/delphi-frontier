"""Europe PMC: primary-literature search and open-access full text.

Public, keyless REST. Used to fetch **primary sources directly** so a model's
summary can be checked against them rather than believed. Nothing here upgrades
a claim; it only retrieves what a claim can be checked against.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

from connectors.bioservices.receipts import RetrievalReceipt, sha256_text, utc_now

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
USER_AGENT = "delphi-frontier-bioservices/0.1 (public literature retrieval)"
LICENSE = "Europe PMC REST API; article rights belong to their publishers"
_last = 0.0
MIN_INTERVAL = 0.4


def _get(path: str, timeout: int = 45, retries: int = 2) -> str:
    global _last
    for attempt in range(retries + 1):
        gap = time.time() - _last
        if gap < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - gap)
        req = urllib.request.Request(f"{BASE}{path}", headers={"User-Agent": USER_AGENT})
        try:
            _last = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception:
            if attempt == retries:
                raise
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError("unreachable")  # pragma: no cover


def search(query: str, page_size: int = 25, result_type: str = "core") -> tuple[list[dict], RetrievalReceipt]:
    """Search; returns results and a receipt recording the EXACT query string."""
    q = urllib.parse.quote(query)
    path = f"/search?query={q}&format=json&pageSize={page_size}&resultType={result_type}"
    raw = _get(path)
    data = json.loads(raw)
    hits = data.get("resultList", {}).get("result", [])
    receipt = RetrievalReceipt(
        source_id="europepmc.search", url=f"{BASE}{path}", state="retrieved",
        retrieved_utc=utc_now(), size_bytes=len(raw), sha256=sha256_text(raw),
        media_type="application/json", license=LICENSE,
        version=str(data.get("version", "")),
        notes=[f"query={query}", f"hitCount={data.get('hitCount')}", f"returned={len(hits)}"],
    )
    return hits, receipt


def full_text_xml(pmcid: str) -> tuple[str, RetrievalReceipt]:
    """Open-access full text. Raises if the article is not in the OA subset."""
    pmcid = pmcid if pmcid.upper().startswith("PMC") else f"PMC{pmcid}"
    path = f"/{pmcid}/fullTextXML"
    raw = _get(path, timeout=90)
    receipt = RetrievalReceipt(
        source_id=f"europepmc.fulltext.{pmcid}", url=f"{BASE}{path}", state="retrieved",
        retrieved_utc=utc_now(), size_bytes=len(raw), sha256=sha256_text(raw),
        media_type="application/xml", license=LICENSE, version=None,
        notes=[f"pmcid={pmcid}"],
    )
    return raw, receipt


def brief(hit: dict) -> dict:
    """The identifying fields of a hit, without the bulk."""
    return {
        "pmid": hit.get("pmid"), "pmcid": hit.get("pmcid"), "doi": hit.get("doi"),
        "title": hit.get("title"), "journal": (hit.get("journalInfo") or {}).get("journal", {}).get("title"),
        "year": hit.get("pubYear"), "authorString": hit.get("authorString"),
        "isOpenAccess": hit.get("isOpenAccess"), "citedByCount": hit.get("citedByCount"),
    }
