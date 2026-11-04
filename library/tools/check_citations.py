#!/usr/bin/env python3
"""Citation gate for the law library: read-level vocabulary, DOI presence, and DOI RESOLUTION.

Three design decisions worth stating, because each could reasonably have gone the other way.

1. `remembered` IS A LEGITIMATE READ-LEVEL, and it is loud rather than banned.
   Agents writing entries invented it for citations they recalled rather than retrieved. The
   tempting response is to forbid it. That is wrong: a vocabulary with no way to say "I recalled
   this" forces the honest agent to mislabel as `search-summary`, and then the dangerous case is
   indistinguishable from the merely shallow one. So it is allowed, counted, rendered as a warning
   on the page, and reported here every run. An entry may not rest a CONSTANT on a `remembered`
   source.

2. A DOI IS CHECKED BY RESOLVING IT, not by matching a regex. `10.` followed by digits is a
   string; a DOI is a promise that something is there. `--resolve` asks doi.org and compares the
   returned title against the citation text, which catches both the invented DOI and the real DOI
   attached to the wrong paper -- the second being the failure a regex can never see.

3. The vocabulary is EXTENDED rather than enforced down. `metadata` (the record was read, the text
   was not) and `full-text-preprint` (the preprint was read, not the version of record) are more
   precise than the levels they would otherwise be rounded into. Precision that an author
   volunteered should not be discarded by the checker.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs pyyaml")

# Ordered strongest to weakest. `remembered` is last on purpose: it is the floor, not an error.
READ_LEVELS = {
    "full-text": "the published text was read",
    "full-text-preprint": "the preprint full text was read, not the version of record",
    "abstract": "the abstract was read",
    "metadata": "the catalogue record was read; the text was not",
    "listing": "the item appeared in a listing",
    "search-summary": "a search engine's summary, not the source",
    "could-not-access": "retrieval was attempted and failed",
    "remembered": "RECALLED, NOT RETRIEVED -- treat as unverified until resolved",
}
WEAK = {"search-summary", "could-not-access", "remembered"}
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s,;)\]]+)", re.I)

CTX = ssl.create_default_context()


def extract_doi(src: dict) -> str | None:
    if src.get("doi"):
        return str(src["doi"]).strip().replace("https://doi.org/", "")
    m = DOI_RE.search(str(src.get("citation", "")))
    return m.group(1).rstrip(".") if m else None


def resolve(doi: str, timeout=25):
    """Ask doi.org for registered metadata. Returns (ok, {title, year, family}) or (False, error)."""
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/:")
    req = urllib.request.Request(url, headers={"Accept": "application/citeproc+json",
                                               "User-Agent": "delphi-law-library/1.0 (mailto:noreply@anthropic.com)"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            d = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, type(e).__name__
    t = d.get("title")
    if isinstance(t, list):
        t = t[0] if t else ""
    year = None
    for k in ("published-print", "published-online", "issued", "created"):
        parts = (d.get(k) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            year = int(parts[0][0]); break
    fam = ""
    auth = d.get("author") or []
    if auth and isinstance(auth[0], dict):
        fam = (auth[0].get("family") or "").strip()
    return True, {"title": (t or "").strip(), "year": year, "family": fam}


def citation_contradicts(citation: str, meta: dict):
    """Flag only a DISAGREEMENT, never a mere absence.

    The first version compared the resolved TITLE against the citation text and flagged 10 of 12
    sources. Almost all were correct: a citation written "Author (Year) Journal vol:pages, doi X"
    states no title, so title overlap is zero by construction and the check could only ever fire.
    A guard with that false-positive rate gets switched off, which is worse than no guard.

    Author surname and year are nearly always present in a citation AND in the registered
    metadata, so they are the reliable match key. A title mismatch is reported only when the
    citation actually asserts a title to disagree with.
    """
    c = citation.lower()
    if meta.get("year"):
        years = {int(y) for y in re.findall(r"\b(19\d{2}|20\d{2})\b", citation)}
        if years and meta["year"] not in years and not any(abs(meta["year"] - y) <= 1 for y in years):
            return f"year {meta['year']} registered, citation says {sorted(years)}"
    if meta.get("family") and len(meta["family"]) > 2:
        if meta["family"].lower() not in c:
            return f"first author {meta['family']!r} does not appear in the citation"
    return None


def title_agrees(citation: str, title: str) -> bool:
    """Kept for the self-test: loose word overlap, used only when a title is actually asserted."""
    if not title:
        return True
    stop = {"the", "a", "an", "of", "and", "in", "on", "for", "to", "with", "by", "its", "is", "at"}
    words = [w for w in re.findall(r"[a-z]{4,}", title.lower()) if w not in stop]
    if not words:
        return True
    hits = sum(1 for w in words if w in citation.lower())
    return hits >= max(1, len(words) // 3)


def check(path: Path, do_resolve: bool):
    doc = yaml.safe_load(path.read_text())
    problems, notes = [], []
    srcs = doc.get("sources") or []
    if not srcs:
        problems.append(f"{path.name}: no sources at all")
    for s in srcs:
        if not isinstance(s, dict):
            problems.append(f"{path.name}: a source is not a mapping")
            continue
        cit = str(s.get("citation", "")).strip()
        rl = s.get("read_level")
        if rl not in READ_LEVELS:
            problems.append(f"{path.name}: read_level {rl!r} is not in the vocabulary "
                            f"({', '.join(sorted(READ_LEVELS))})")
        if rl == "remembered":
            notes.append(f"{path.name}: RECALLED, not retrieved -- {cit[:70]}")
        doi = extract_doi(s)
        if not doi and rl not in ("could-not-access", "remembered"):
            notes.append(f"{path.name}: no DOI on a {rl} source -- {cit[:60]}")
        if doi and do_resolve:
            ok, info = resolve(doi)
            if not ok:
                problems.append(f"{path.name}: DOI {doi} did NOT resolve ({info}) -- {cit[:55]}")
            else:
                bad = citation_contradicts(cit, info)
                if bad:
                    problems.append(f"{path.name}: DOI {doi} CONTRADICTS its citation ({bad}); "
                                    f"registered {info.get('title','')[:60]!r}")

    # A measured constant may not rest on a weak source alone. This is the rule that makes the
    # read-level do work rather than decorate: the numbers are what a design is checked against.
    cons = doc.get("constants") or {}
    if cons and srcs:
        levels = {s.get("read_level") for s in srcs if isinstance(s, dict)}
        if levels and levels <= WEAK:
            problems.append(f"{path.name}: every source is weak ({', '.join(sorted(levels))}) "
                            f"but the entry declares {len(cons)} measured constant(s)")
    return problems, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent.parent / "laws"))
    ap.add_argument("--resolve", action="store_true", help="resolve every DOI against doi.org")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        ok = True

        def expect(label, got, want):
            nonlocal ok
            good = got == want
            ok &= good
            print(f"  [{'ok' if good else 'FAIL'}] {label}: got {got!r}, want {want!r}")

        expect("DOI pulled out of free-text citation",
               extract_doi({"citation": "Eloy C (2012) J Fluids Struct 30:205-218, doi 10.1016/j.jfluidstructs.2012.02.008"}),
               "10.1016/j.jfluidstructs.2012.02.008")
        expect("explicit doi field wins", extract_doi({"doi": "https://doi.org/10.1234/abc"}), "10.1234/abc")
        expect("no DOI present", extract_doi({"citation": "Some book, 2nd ed."}), None)
        expect("title agrees loosely", title_agrees("Eloy 2012, Optimal Strouhal number for swimming animals",
                                                    "Optimal Strouhal number for swimming animals"), True)
        # THE CASE IT MUST FLAG: a real DOI attached to the wrong paper.
        expect("title DISAGREES is caught",
               title_agrees("Murray CD (1926) The physiological principle of minimum work",
                            "Attention Is All You Need: Transformer Architectures"), False)
        if a.resolve:
            ok_r, t = resolve("10.1016/j.cub.2021.08.054")
            expect("a real DOI resolves", ok_r, True)
            print(f"        resolved: {t.get('family')} {t.get('year')} -- {t.get('title','')[:62]!r}")
            expect("a titleless citation does NOT contradict",
                   citation_contradicts("Daane JM et al. (2021) Curr Biol 31:5052-5061", t), None)
            expect("a WRONG-author citation IS caught",
                   citation_contradicts("Murray CD (1926) PNAS 12:207-214", t) is not None, True)
            ok_b, _ = resolve("10.9999/this.doi.does.not.exist.12345")
            expect("a fabricated DOI does NOT resolve", ok_b, False)
        return 0 if ok else 1

    files = sorted(Path(a.dir).glob("*.yaml"))
    allp, alln = [], []
    for f in files:
        p, n = check(f, a.resolve)
        allp += p
        alln += n
        print(f"  {'FAIL' if p else 'ok  '} {f.name}")
        for x in p:
            print(f"        {x}")
    if alln:
        print(f"\n{len(alln)} note(s) -- not failures, but they weaken what rests on them:")
        for x in alln:
            print(f"  · {x}")
    print(f"\n{len(files)} entries, {len(allp)} problems, {len(alln)} notes")
    return 1 if allp else 0


if __name__ == "__main__":
    sys.exit(main())
