#!/usr/bin/env python3
"""Retrieve full text for the cited corpus via NCBI efetch, which is the route that works.

WHY THIS EXISTS. Across 2026-11-04 this project and four peer sessions failed to retrieve PMC
full text by every route they tried: curl to pmc.ncbi.nlm.nih.gov returns a reCAPTCHA
interstitial, r.jina.ai faithfully relays that same challenge page, headless Playwright never
clears it, publisher sites sit behind Cloudflare, and Europe PMC's fullTextXML endpoint returned
HTTP 500 on every attempt by two different sessions. The conclusion drifting through the project
was that PMC full text was simply unavailable here.

It is not. NCBI's E-utilities endpoint serves the same articles as XML with no challenge:

    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=<PMCID>&retmode=xml

Found by a peer session (morphoswarm-fc) while verifying quotes it had obtained through a
WebFetch summariser -- i.e. found by someone checking their own weakest link, which is the
habit worth copying from this episode.

WHAT IT DOES NOT DO. It does not reach articles outside PMC's OPEN-ACCESS subset. A PMC id is
not enough: Young & Rome 2001 (PMC1088836) is deposited and indexed but not OA, and efetch
returns 5,799 bytes of metadata with NO <body> element, against 157,838 bytes WITH one for an OA
paper. That distinction is the whole value of the <body> check below -- without it a metadata
stub looks exactly like a successful retrieval, which is this project's recurring failure shape.
"""
from __future__ import annotations

import os
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EFETCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
          "?db=pmc&id={pmcid}&retmode=xml")
OUT = Path(__file__).resolve().parent.parent / "results" / "fulltext"
PAUSE_S = 1.0          # NCBI asks for <= 3 requests/second unauthenticated; stay well under

# A known-OA article, fetched first as a POSITIVE CONTROL. If this one comes back without a
# body, the route itself is broken and every "no body" below would be a false negative.
CONTROL_PMCID = "PMC7235970"


def fetch(pmcid: str) -> tuple[int, int, str]:
    """Return (bytes, body_chars, text). body_chars == 0 means metadata only, not OA."""
    req = urllib.request.Request(EFETCH.format(pmcid=pmcid),
                                 headers={"User-Agent": "morphoswarm-research/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read().decode("utf-8", errors="replace")
    m = re.search(r"<body>(.*)</body>", raw, re.S)
    body = m.group(1) if m else ""
    fg = re.search(r"<floats-group>(.*)</floats-group>", raw, re.S)
    if fg:
        body += "\n\nFIGURES AND TABLES\n" + fg.group(1)
    return len(raw), len(body), raw


def strip_tags(xml_body: str) -> str:
    t = re.sub(r"<[^>]+>", " ", xml_body)
    return re.sub(r"\s+", " ", t).strip()


def main() -> int:
    from figure_sweep import CORPUS

    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 78)
    print("FULL-TEXT RETRIEVAL VIA NCBI EFETCH")
    print("=" * 78)

    # ---- positive control first; everything after it is meaningless without it ----
    n, bodyn, _ = fetch(CONTROL_PMCID)
    if bodyn == 0:
        print(f"  CONTROL FAILED: {CONTROL_PMCID} returned {n} bytes and no <body>.")
        print("  The route is broken. Every 'no body' result would be a false negative,")
        print("  so nothing further is attempted.")
        return 2
    print(f"  control ok: {CONTROL_PMCID} -> {n:,} bytes, {bodyn:,} body chars\n")
    time.sleep(PAUSE_S)

    got, meta_only, no_pmc, failed = [], [], [], []
    for doi, (pmcid, desc) in sorted(CORPUS.items()):
        if not pmcid or not pmcid.startswith("PMC") or not pmcid[3:].isdigit():
            no_pmc.append((doi, desc))
            continue
        try:
            n, bodyn, raw = fetch(pmcid)
        except Exception as e:                       # noqa: BLE001
            failed.append((pmcid, desc, type(e).__name__))
            print(f"  {pmcid:<14} FETCH FAILED  {type(e).__name__}  {desc[:40]}")
            time.sleep(PAUSE_S)
            continue
        if bodyn == 0:
            meta_only.append((pmcid, desc))
            print(f"  {pmcid:<14} metadata only ({n:,} B, no body -- NOT in the OA subset)"
                  f"  {desc[:36]}")
        else:
            body = re.search(r"<body>(.*)</body>", raw, re.S).group(1)
            fg = re.search(r"<floats-group>(.*)</floats-group>", raw, re.S)
            if fg:
                body += "\n\nFIGURES AND TABLES\n" + fg.group(1)
            p = OUT / f"{pmcid}.txt"
            saved = strip_tags(body)
            p.write_text(saved, encoding="utf-8")
            got.append((pmcid, len(saved), desc))
            print(f"  {pmcid:<14} FULL TEXT  {len(saved):>7,} chars saved "
                  f"(from {bodyn:,} of XML) -> {p.name}  {desc[:28]}")
        time.sleep(PAUSE_S)

    print("\n" + "-" * 78)
    print(f"  {len(got)} full texts retrieved and saved under results/fulltext/")
    print(f"  {len(meta_only)} in PMC but NOT open access (metadata only -- a real limit,")
    print(f"     not a retrieval failure, and the control above is what distinguishes them)")
    print(f"  {len(no_pmc)} with no PMC record at all")
    if failed:
        print(f"  {len(failed)} fetch errors: {', '.join(p for p, _, _ in failed)}")
    for pmcid, desc in meta_only:
        print(f"     not OA: {pmcid}  {desc}")
    print("-" * 78)
    print("  Having the text is not having read it. These are now READABLE, not read.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
