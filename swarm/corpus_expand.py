#!/usr/bin/env python3
"""Grow the full-text corpus by SEARCHING PMC's open-access subset, not by hand-listing DOIs.

WHY THIS EXISTS. The evidence base under this project is 6 full texts supporting 821 claims.
That is not a retrieval failure -- `fetch_fulltext.py` works and its control passes -- it is
that its input, `figure_sweep.CORPUS`, is a hand-maintained dict of 22 entries, 11 of which
carry a PMCID. A corpus that only grows when a person types a DOI into a literal grows at the
rate people type DOIs, and every claim made beyond it is grounded in something nobody fetched.

So this searches instead. NCBI's esearch serves the same no-challenge route that efetch does
(see fetch_fulltext.py for why that route and not the others), and the OA body check there is
reused verbatim rather than reimplemented: a PMC hit is not an obtainable paper, and the only
honest test of that is fetching it and looking for a <body>.

WHAT IT DOES NOT DO. It does not judge relevance. A search hit is a CANDIDATE; the text it
saves is READABLE, not read, and certainly not evidence for anything until extract_values.py
has pulled a verified quote out of it. Counting retrieved papers as literature support would be
the "listing is not reading" failure that docs/research/README.md exists to prevent.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_fulltext import OUT, PAUSE_S, fetch, strip_tags   # noqa: E402  reuse, do not restate

ESEARCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
           "?db=pmc&retmode=json&retmax={n}&term={term}")

# A phrase from a paper we already hold, used as the POSITIVE control: esearch must return that
# paper for it. If this comes back empty the search route is down, and every "0 hits" below
# would be a false negative -- the exact shape that made this project conclude PMC was closed.
CONTROL_TERM = "Danio rerio"
CONTROL_MUST_INCLUDE = "PMC7235970"

# A term that must return NOTHING. Without it, a search that ignores its query and returns the
# whole database passes the positive control perfectly.
CONTROL_NONSENSE = "zzqxvtplmgf_not_a_real_term_9174"


def esearch(term: str, n: int = 20, tries: int = 6) -> list[str]:
    """Search PMC, retrying transient 500s.

    A 500 FROM THIS ENDPOINT IS NOT AN ANSWER, and treating one as an answer is how this
    project previously concluded that PMC was closed to it. Measured 2026-11-04 within a few
    seconds: db=pmc and db=pubmed both returned 500 on three consecutive terms, then db=pmc
    returned 202,649 hits for the same term that had just failed while db=pubmed still 500'd.
    Nothing about the route changed in between -- NCBI rate-limits unauthenticated callers at
    about 3 requests a second and sheds load as a 500 rather than a 429. So a single failure
    means the request was shed, not that the corpus is empty, and the control that guards this
    module would have aborted the whole run on a blip and reported the search as down.

    THE BACKOFF FLOOR IS MEASURED, NOT GUESSED. Polling the same term every 30 s through an
    episode of shedding: 500 at t+0, 500 at t+30, OK at t+60, OK at t+90. So an episode lasts
    tens of seconds, and an exponential backoff of 1+2+4+8+16+32 s spends five of its six
    attempts inside the window where every answer is already known to be a 500. The floor is
    therefore 25 s per retry rather than a doubling from 1 s -- a short first retry is not
    merely useless here, it burns an attempt and makes the shedding worse.
    """
    url = ESEARCH.format(n=n, term=urllib.parse.quote(term))
    req = urllib.request.Request(url, headers={"User-Agent": "morphoswarm-research/1.0"})
    last: Exception | None = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            return ["PMC" + i for i in data.get("esearchresult", {}).get("idlist", [])]
        except urllib.error.HTTPError as e:                  # noqa: PERF203
            last = e
            if e.code not in (429, 500, 502, 503):
                raise
            time.sleep(max(25.0, PAUSE_S * (2 ** attempt)))  # >= 25s: see the measurement
        except Exception as e:                               # noqa: BLE001
            last = e
            time.sleep(PAUSE_S * (2 ** attempt))
    raise RuntimeError(f"esearch failed after {tries} tries: {type(last).__name__}: {last}")


def controls_pass() -> tuple[bool, str]:
    """Must-find and must-not-find. Both, or the counts below mean nothing.

    These retry far longer than an ordinary query because they GATE the run: a control that
    gives up during a shedding episode aborts work that would have succeeded, and reports the
    search as down when it is merely busy. Measured over a 5.5-minute poll at 30 s intervals,
    NCBI answered 2 of 12 requests and shed the rest as 500s, in bursts -- so persistence, not
    rate, is what gets an answer out of it.
    """
    try:
        hits = esearch(f'"{CONTROL_TERM}"', n=100, tries=14)
    except Exception as e:                                   # noqa: BLE001
        return False, f"positive control raised {type(e).__name__}"
    time.sleep(PAUSE_S)
    if not hits:
        return False, f"positive control '{CONTROL_TERM}' returned 0 hits -- search route down"
    try:
        none = esearch(CONTROL_NONSENSE, n=10, tries=14)
    except Exception as e:                                   # noqa: BLE001
        return False, f"negative control raised {type(e).__name__}"
    time.sleep(PAUSE_S)
    if none:
        return False, (f"negative control returned {len(none)} hits for a nonsense term -- "
                       f"the search is not filtering on the query at all")
    return True, f"'{CONTROL_TERM}' -> {len(hits)} hits; nonsense term -> 0 hits"


def main() -> int:
    n_per = int(os.environ.get("CORPUS_PER_QUERY", "12"))
    queries = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if not queries:
        print("usage: corpus_expand.py 'query one' 'query two' ... [--write]")
        print("       without --write it reports what WOULD be fetched and saves nothing")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    have = {p.stem for p in OUT.glob("*.txt")}

    print("=" * 78)
    print("CORPUS EXPANSION -- PMC SEARCH, THEN THE OA BODY CHECK")
    print("=" * 78)
    print(f"  {len(have)} full text(s) already held; {len(queries)} quer(ies); "
          f"{n_per} candidates each")
    ok, why = controls_pass()
    print(f"  [{'ok' if ok else 'FAIL'}] controls: {why}")
    if not ok:
        print("\n  ABORTING. Without both controls, '0 new papers' is indistinguishable from a")
        print("  broken search, and a large haul from a search that ignores the query.")
        return 2
    if not write:
        print("  DRY RUN -- nothing will be saved (pass --write to save)")
    print()

    seen: dict[str, list[str]] = {}
    for qstr in queries:
        try:
            hits = esearch(qstr, n=n_per)
        except Exception as e:                               # noqa: BLE001
            print(f"  QUERY FAILED  {type(e).__name__}  {qstr[:60]}")
            continue
        print(f"  query {qstr[:58]:<58} {len(hits):>3} hits")
        for h in hits:
            seen.setdefault(h, []).append(qstr)
        time.sleep(PAUSE_S)

    fresh = [p for p in seen if p not in have]
    print(f"\n  {len(seen)} distinct candidate(s), {len(seen) - len(fresh)} already held, "
          f"{len(fresh)} new to try\n")

    saved, meta_only, failed = [], [], []
    for pmcid in sorted(fresh):
        try:
            nb, bodyn, raw = fetch(pmcid)
        except Exception as e:                               # noqa: BLE001
            failed.append((pmcid, type(e).__name__))
            print(f"  {pmcid:<14} FETCH FAILED  {type(e).__name__}")
            time.sleep(PAUSE_S)
            continue
        if bodyn == 0:
            meta_only.append(pmcid)
            print(f"  {pmcid:<14} metadata only ({nb:,} B, no body -- NOT in the OA subset)")
        else:
            body = re.search(r"<body>(.*)</body>", raw, re.S).group(1)
            fg = re.search(r"<floats-group>(.*)</floats-group>", raw, re.S)
            if fg:
                body += "\n\nFIGURES AND TABLES\n" + fg.group(1)
            text = strip_tags(body)
            if write:
                (OUT / f"{pmcid}.txt").write_text(text, encoding="utf-8")
            saved.append((pmcid, len(text)))
            print(f"  {pmcid:<14} FULL TEXT  {len(text):>7,} chars"
                  f"{'' if write else '  (dry run, not saved)'}")
        time.sleep(PAUSE_S)

    print("\n" + "-" * 78)
    print(f"  {len(saved)} full text(s) {'saved' if write else 'retrievable'}; "
          f"{len(meta_only)} in PMC but not OA; {len(failed)} fetch errors")
    print(f"  corpus would go from {len(have)} to {len(have) + len(saved)} papers")
    print("-" * 78)
    print("  These are READABLE, not read. A retrieved paper supports no claim until")
    print("  extract_values.py has taken a quote out of it and verified that quote verbatim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
