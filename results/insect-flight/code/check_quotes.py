#!/usr/bin/env python3
"""Check every quoted fragment in routes.json against the stored source text.

WHY THIS EXISTS
    A citation can be verified - the PMID resolves, the journal and year are
    right - and the SENTENCE attributed to it can still be invented. Nothing
    else on this page would catch that. This script takes every single-quoted
    run of >= 12 characters inside an evidence row's `finding`, and requires
    it to appear verbatim in that PMID's stored title + abstract (or full
    text, where we have one).

    Rows whose read_level is `listing` are skipped: they carry a NOT-READ
    note by construction and quote nothing.

POSITIVE AND NEGATIVE CONTROLS
    Both are run every time, because a checker that passes everything and a
    checker that is not running look identical:
      - a sentence no paper contains must NOT be found;
      - a sentence taken verbatim from a stored abstract MUST be found.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FULL_TEXT_FILES = {
    "34001903": ROOT / "data" / "paul2021-PMC8129201-fulltext.xml",
    "34783648": ROOT / "data" / "deora2021-PMC8629423-fulltext.xml",
}
MIN_LEN = 12


def strip_xml(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))


def norm(x):
    x = (x.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"')
          .replace("–", "-").replace("—", "-")
          .replace("′", "'").replace(" ", " "))
    # Quote characters and the degree sign are typographic, not content: a
    # source that writes 2 deg and a quote that writes 2 degrees are the same
    # claim, and a nested "four-winged fly" inside an abstract is too.
    x = x.replace("\u00b0", " degrees").replace('"', " ").replace("'", " ")
    return re.sub(r"\s+", " ", x).lower()


def sources():
    verified = json.loads((ROOT / "data" / "pmid_verified.json").read_text())
    abstracts = json.loads((ROOT / "data" / "pmid_abstracts.json").read_text())
    out = {}
    for pmid, rec in verified.items():
        if rec is None:
            continue
        # TITLES COUNT. Several findings quote the paper's title, which is a
        # legitimate thing to quote and is not in the abstract text.
        out[pmid] = norm(rec.get("title", "") + " . " + abstracts.get(pmid, ""))
    # PubMed and PMC do not always hold the SAME abstract. For Ristroph
    # et al. 2010 the PubMed record stops short of the sentence this page's
    # whole control criterion rests on - "recover their heading to within 2
    # degrees in < 60 ms" - which the PMC version carries. Both are stored
    # and both are searched. The discrepancy was found by this checker.
    pmc = ROOT / "data" / "pmc_abstracts.json"
    if pmc.exists():
        for pmid, txt in json.loads(pmc.read_text()).items():
            out[pmid] = norm(txt) + " " + out.get(pmid, "")
    for pmid, path in FULL_TEXT_FILES.items():
        if path.exists():
            out[pmid] = norm(strip_xml(path.read_text(encoding="utf-8",
                                                      errors="replace"))) \
                + " " + out.get(pmid, "")
    return out


def fragments(finding):
    """Quoted runs, split on ellipses, with [bracketed completions] removed."""
    # An opening quote must start a word and a closing quote must end one,
    # otherwise every possessive apostrophe ("study 1's model") is read as a
    # quote delimiter. That artifact produced 2 of the first 17 flags.
    pat = r"(?:(?<=^)|(?<=[\s(\[]))'([^']{%d,}?)'(?=[\s.,;:)\]]|$)" % MIN_LEN
    for frag in re.findall(pat, finding):
        for part in re.split(r"\s*\.\.\.\s*", frag):
            part = re.sub(r"\[[^\]]*\]", "", part).strip(" .,;:")
            if len(part) >= MIN_LEN:
                yield part


def main():
    src = sources()
    d = json.loads((ROOT / "routes.json").read_text())
    bad, checked, no_source = [], 0, []
    for r in d["routes"]:
        for e in r["evidence"]:
            if e["read_level"] == "listing":
                continue
            s = src.get(e["pmid"], "")
            if not s.strip():
                no_source.append((r["id"], e["pmid"]))
                continue
            for part in fragments(e["finding"]):
                checked += 1
                if norm(part) not in s:
                    bad.append((r["id"], e["pmid"], part))

    # --- controls ---------------------------------------------------------
    neg = norm("the haltere is a small purple trombone")
    neg_found = any(neg in v for v in src.values())
    pos_src = src["18936482"]
    pos = "lepidopterans can still fly when their hindwings are cut off"
    pos_found = norm(pos) in pos_src

    print(f"checked {checked} quoted fragments across "
          f"{sum(len(r['evidence']) for r in d['routes'])} evidence rows")
    print(f"control NEGATIVE (a sentence no paper contains): "
          f"found={neg_found} (must be False)")
    print(f"control POSITIVE (a sentence from a stored abstract): "
          f"found={pos_found} (must be True)")
    if no_source:
        print(f"{len(no_source)} rows had no stored source: {no_source}")
    print(f"{len(bad)} fragments NOT found verbatim:")
    for rid, pmid, part in bad:
        print(f"  {rid}  PMID {pmid}\n      {part[:150]}")
    ok = (not bad) and (not neg_found) and pos_found and not no_source
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
