#!/usr/bin/env python3
"""Verify PMIDs against NCBI eutils, and optionally store their abstracts.

Two modes:
  verify_pmids.py <pmids.txt> [out.json]              esummary records
  verify_pmids.py --abstracts <pmids.txt> <out.json>  efetch abstracts

The second mode exists so that a citation's `read_level` can be set honestly.
A record from esummary gives a title and a journal and nothing else, which is
a LISTING. An abstract fetched here and read is an ABSTRACT. Neither is a
full text, and the design-space JSON says which of the three it is for every
source.

Prints one compact line per PMID so every citation on the page can be checked
against the record NCBI actually returns, rather than against a model's memory.
A PMID that does not resolve prints MISSING and must not be used.

Usage: verify_pmids.py <file-with-one-pmid-per-line> [out.json]
"""
import json
import sys
import time
import urllib.parse
import urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch_abstracts(pmids):
    """efetch the abstract text for a batch of PMIDs, as {pmid: text}."""
    import re
    import xml.etree.ElementTree as ET

    q = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    )
    req = urllib.request.Request(
        EFETCH + "?" + q, headers={"User-Agent": "morphoswarm-designspace/0.1"}
    )
    with urllib.request.urlopen(req, timeout=120) as fh:
        root = ET.parse(fh).getroot()
    out = {}
    for art in root.iter("PubmedArticle"):
        pid = art.findtext(".//PMID")
        parts = []
        for ab in art.iter("AbstractText"):
            lab = ab.get("Label")
            txt = "".join(ab.itertext()).strip()
            parts.append(f"{lab}: {txt}" if lab else txt)
        out[pid] = re.sub(r"\s+", " ", " ".join(parts)).strip()
    return out


def abstracts_main():
    pmids = [
        ln.strip() for ln in open(sys.argv[2])
        if ln.strip() and not ln.startswith("#")
    ]
    seen = set()
    uniq = [p for p in pmids if not (p in seen or seen.add(p))]
    out = {}
    for i in range(0, len(uniq), 40):
        out.update(fetch_abstracts(uniq[i : i + 40]))
        time.sleep(0.4)
    empty = sorted(p for p in uniq if not out.get(p))
    json.dump(out, open(sys.argv[3], "w"), indent=1)
    print(f"{sum(1 for v in out.values() if v)} abstracts, "
          f"{len(empty)} with NO abstract in PubMed: {empty}")


def fetch(pmids):
    q = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}
    )
    req = urllib.request.Request(
        EUTILS + "?" + q, headers={"User-Agent": "morphoswarm-designspace/0.1"}
    )
    with urllib.request.urlopen(req, timeout=60) as fh:
        return json.load(fh)


def main():
    pmids = [
        ln.strip()
        for ln in open(sys.argv[1])
        if ln.strip() and not ln.startswith("#")
    ]
    seen, out = set(), {}
    uniq = [p for p in pmids if not (p in seen or seen.add(p))]
    for i in range(0, len(uniq), 50):
        chunk = uniq[i : i + 50]
        res = fetch(chunk)["result"]
        for p in chunk:
            r = res.get(p)
            if not r or "error" in r:
                print(f"{p}\tMISSING")
                out[p] = None
                continue
            au = r.get("authors") or [{}]
            rec = {
                "pmid": p,
                "first_author": au[0].get("name", "?"),
                "year": (r.get("pubdate") or "?").split()[0],
                "journal": r.get("source", "?"),
                "volume": r.get("volume", ""),
                "pages": r.get("pages", ""),
                "title": (r.get("title") or "").rstrip("."),
                "doi": next(
                    (
                        a["value"]
                        for a in r.get("articleids", [])
                        if a.get("idtype") == "doi"
                    ),
                    "",
                ),
            }
            out[p] = rec
            print(
                f"{p}\t{rec['first_author']}\t{rec['year']}\t"
                f"{rec['journal']} {rec['volume']}:{rec['pages']}\t{rec['title']}"
            )
        time.sleep(0.4)
    if len(sys.argv) > 2:
        json.dump(out, open(sys.argv[2], "w"), indent=1)
    missing = [p for p, v in out.items() if v is None]
    print(f"\n# {len(out) - len(missing)} resolved, {len(missing)} MISSING: {missing}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--abstracts":
        abstracts_main()
    else:
        main()
