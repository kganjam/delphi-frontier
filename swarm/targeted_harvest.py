#!/usr/bin/env python3
"""Search for a paper BECAUSE it should answer one question, then ask it that question.

WHY THIS EXISTS -- a measured failure, 2026-11-05.
This project held 225 full texts (20.7 MB) and extraction returned ZERO verified values from
them. Four separate runs over nine papers the project already cites for numbers returned zero,
with zero discards, across two prompts and three question lists. The machinery was never broken:
given one question a paper demonstrably answers, it returned the value on the first call, with
the quote verified and the provenance correctly labelled `quoted` rather than `measured-here`
(Sutton et al. 2019, PMC6907395, muscle energy density 15.0 J/kg, bullfrog).

The corpus was the problem, and `corpus_expand.py` says so in its own docstring: "It does not
judge relevance." It was built from hand-typed queries, so it holds papers on alligator
phylogeny, pufferfish aquaculture, neurexins and Durban open space. Asking twenty good questions
of 225 off-topic papers costs 661 calls to be told, correctly, that the answer is not there.

So the pairing is inverted. Instead of a corpus crossed with a question list -- which is a
product, and nearly all of it empty -- each question drives its own search, and the papers that
search returns are asked THAT question and no other. The call count falls from
(papers x chunks) to (papers found per question x chunks), and every call is one where the
answer has a reason to be present.

WHAT IT DOES NOT DO. It does not establish that a returned value is right, or that it means what
the question meant. A verified quote means the sentence is real and the number is in it. The
`provenance` field says how the PAPER came by the number -- measured, modelled, assumed, or
quoted from somewhere else -- and that distinction is the point: a simulation output recorded as
a measurement is the exact failure this database exists to prevent.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_expand as ce                                        # noqa: E402
import extract_values as ev                                       # noqa: E402
import fetch_fulltext as ff                                       # noqa: E402
from api_challenge import TENANTS, call    # noqa: E402  api_allen excluded in one place

MODEL = "claude-opus-4-5-20251101"
# The question NUMBER is only meaningful beside the file that numbered it. Two question files
# renumber the same quantities differently, so a value stamped only with `asked: 7` cannot be
# joined to a scale map later without silently reading the wrong row.
QFILE_STEM = [""]
# Each run writes its OWN file. A fixed output path means two concurrent harvests -- which is the
# normal case here, since a run takes hours and the questions change -- silently overwrite each
# other, and the one that finishes last wins. Caught by the incremental flush above: with both
# runs writing after every question, the file visibly alternated between two sets of values.
OUTFILE = ["targeted.json"]
OUT = pathlib.Path(__file__).resolve().parent.parent / "results" / "extract"
PAUSE_S = 0.4

QUERY_PROMPT = """Write a literature search query for each question below.

KEEP IT SHORT: three to five plain keywords, no boolean operators, no quotes, no field tags. The
query goes to both NCBI esearch and Europe PMC, and Europe PMC ANDs every term it is given, so a
long or boolean query silently returns nothing. Measured 2026-11-05: longer model-written queries
returned 0 records for 11 of 20 questions, and the resulting "the literature has no numbers"
reading was an artifact of the query, not a fact about the literature. Short keyword queries over
the same questions returned 166 abstracts of which 37% carried a number with a unit.

Use the vocabulary a paper would use, not the question's wording. Do not restrict to one species
unless the question does -- a value from any fish, or from another animal whose physiology
carries over, is wanted.

QUESTIONS:
{items}

Reply with JSON only:
{{"queries": [{{"n": <question number>, "query": "..."}}]}}
"""


EPMC = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        "?query={q}&resultType=core&format=json&pageSize={n}")


def epmc_search(term: str, n: int = 25, tries: int = 4) -> list[dict]:
    """Europe PMC search, returning records WITH their abstract.

    WHY ABSTRACTS, AND WHY THIS IS NOT A WEAKER VERSION OF FULL TEXT. Measured 2026-11-05: PMC's
    open-access subset, searched on this project's own questions, returns theory and robotics
    papers and two medical-dictionary entries. PMC5454310 is squarely on topic -- ray-finned fish
    fin mechanics -- and says "stiffness" five times without stating a single value, because it
    is a modelling paper. The experimental measurements this project needs sit in J Exp Biol,
    Integrative and Comparative Biology and J Morphology, which are largely NOT in the OA subset,
    so no full-text route reaches them from here.

    Their abstracts are open, and a biomechanics abstract usually carries the headline number
    with its units. That is a genuinely weaker read than full text -- no methods, no table, no
    conditions -- which is exactly why `read_level` is a closed vocabulary in this project and
    why every value from here is labelled `abstract` and must never be written up in the voice of
    having read the paper (docs/research/README.md).
    """
    import json as _json
    import urllib.parse
    import urllib.request
    url = EPMC.format(q=urllib.parse.quote(term), n=int(n))
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "morphoswarm-research/1.0"})
            with urllib.request.urlopen(req, timeout=45) as fh:
                data = _json.loads(fh.read().decode("utf-8", "replace"))
            out = []
            for r in data.get("resultList", {}).get("result", []):
                if r.get("abstractText"):
                    out.append({"id": r.get("id"), "src": r.get("source"),
                                "title": r.get("title", ""), "doi": r.get("doi", ""),
                                "journal": (r.get("journalInfo") or {}).get("journal", {}).get("title", ""),
                                "year": r.get("pubYear", ""), "abstract": r["abstractText"]})
            return out
        except Exception as e:                                    # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    print(f"    epmc_search failed: {type(last).__name__}")
    return []


def ask_text(text: str, label: str, question: str, qnum: int, tenant: str) -> tuple[list, list]:
    """Ask one block of text one question. Shared by the full-text and abstract routes."""
    hay = ev.norm(text)
    kept, bad = [], []
    prompt = ev.PROMPT.format(questions=f"1. {question}", excerpt=text)
    try:
        r = call(tenant, prompt, max_tokens=2000, model=ev.MODEL)
    except Exception:                                             # noqa: BLE001
        return kept, bad
    body = r.get("text") if isinstance(r, dict) else str(r)
    data = ev.extract_json(body or "")
    for item in (data or {}).get("values", []) or []:
        q = ev.norm(str(item.get("quote", "")))
        item["paper"], item["asked"] = label, qnum
        item["qfile"] = QFILE_STEM[0]
        item["project"] = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
        if q and len(q) > 15 and q in hay:
            item["verified_quote"] = True
            kept.append(item)
        else:
            item["verified_quote"] = False
            bad.append(item)
    return kept, bad


def ask_confirmed(text: str, label: str, question: str, qnum: int,
                  t1: str, t2: str) -> tuple[list, list]:
    """Ask twice on two tenants and reconcile, because the provenance label is prompt-sensitive.

    MEASURED 2026-11-05: the same abstract (MED23720195) came back `modelled-here` under a
    one-question prompt and `measured-here` under the pooled prompt. Five repeats of each
    configuration were internally stable (5/5), so the label is not call-to-call noise -- it
    moves with what else the model was asked. The earlier label was also the wrong one.

    A field the record depends on cannot rest on one call. `api_evaluate_constraints.py` already
    refuses a `satisfied` verdict a second run does not reproduce; this is the same gate for the
    same reason. A value whose provenance does not repeat is recorded as `unclear` rather than as
    whichever label the first call happened to produce, and one that appears in only one of the
    two runs is kept with its provenance demoted and the disagreement written into the item.

    The value itself is NOT silently reconciled: two runs reporting different numbers for the
    same quantity is a disagreement about fact, and both are dropped with a note, because
    choosing between them here would be choosing which paper says what.
    """
    k1, b1 = ask_text(text, label, question, qnum, t1)
    k2, _b2 = ask_text(text, label, question, qnum, t2)
    second = {}
    for it in k2:
        second.setdefault((str(it.get("value")).strip(), str(it.get("units")).strip()), []).append(it)
    out = []
    for it in k1:
        key = (str(it.get("value")).strip(), str(it.get("units")).strip())
        twin = second.get(key)
        if not twin:
            it["provenance_confirmed"] = False
            it["provenance_note"] = "not reproduced by a second run; provenance demoted"
            it["provenance_first"] = it.get("provenance")
            it["provenance"] = "unclear"
        elif str(twin[0].get("provenance")) != str(it.get("provenance")):
            it["provenance_confirmed"] = False
            it["provenance_note"] = (f"two runs disagreed: {it.get('provenance')} vs "
                                     f"{twin[0].get('provenance')}; recorded as unclear")
            it["provenance_first"] = it.get("provenance")
            it["provenance"] = "unclear"
        else:
            it["provenance_confirmed"] = True
        out.append(it)
    return out, b1


def flush(dest: pathlib.Path, kept: list, bad: list) -> None:
    """Write what has been verified SO FAR, after every question.

    A multi-hour run that writes only at the end holds every value it has found in process
    memory, so a kill, a timeout or a machine restart loses all of it. That happened in this
    session's own workflow -- a run was stopped at question 5 of 20 holding verified values that
    existed nowhere else -- and it is the same shape as the dead ends this module was written to
    fix: work done correctly, output that never reaches a reader.

    Written whole each time rather than appended, so the file is always a valid document and a
    crash mid-write cannot leave a half-object behind.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp")
    tmp.write_text(json.dumps({"verified": kept, "discarded": bad}, indent=1))
    tmp.replace(dest)


def read_questions(path: pathlib.Path) -> list[str]:
    """One question per numbered block; the indented 'Report the species' line belongs to it."""
    out, cur = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line[:1].isdigit() and "." in line[:4]:
            if cur:
                out.append(" ".join(cur).strip())
            cur = [line.split(".", 1)[1].strip()]
        elif line.strip():
            cur.append(line.strip())
    if cur:
        out.append(" ".join(cur).strip())
    return out


def write_queries(questions: list[str]) -> dict[int, str]:
    items = "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1))
    from api_challenge import call_first_live
    r = call_first_live(TENANTS, QUERY_PROMPT.format(items=items), max_tokens=3000, model=MODEL)
    body = r.get("text") if isinstance(r, dict) else str(r)
    data = ev.extract_json(body or "")
    if not data or "queries" not in data:
        return {}
    return {int(q["n"]): q["query"] for q in data["queries"]
            if q.get("n") and q.get("query")}


def harvest(pmcid: str, store: pathlib.Path) -> pathlib.Path | None:
    """Fetch one PMC id if we do not hold it. Returns the text path, or None if not OA."""
    dest = store / f"{pmcid}.txt"
    if dest.exists():
        return dest
    try:
        _, bodyn, raw = ff.fetch(pmcid)
    except Exception:                                             # noqa: BLE001
        return None
    if bodyn == 0:                      # deposited but not in the OA subset: metadata only
        return None
    import re
    body = re.search(r"<body>(.*)</body>", raw, re.S)
    if not body:
        return None
    text = body.group(1)
    fg = re.search(r"<floats-group>(.*)</floats-group>", raw, re.S)
    if fg:
        text += "\n\nFIGURES AND TABLES\n" + fg.group(1)
    dest.write_text(ff.strip_tags(text), encoding="utf-8")
    return dest


def ask(path: pathlib.Path, question: str, qnum: int, tenant: str) -> tuple[list, list]:
    """Ask ONE paper ONE question. Every quote is checked against the text we sent."""
    text = path.read_text(encoding="utf-8")
    hay = ev.norm(text)
    kept, bad = [], []
    for chunk in [text[i:i + ev.CHUNK] for i in range(0, len(text), ev.CHUNK)]:
        prompt = ev.PROMPT.format(questions=f"1. {question}", excerpt=chunk)
        try:
            r = call(tenant, prompt, max_tokens=2000, model=ev.MODEL)
        except Exception:                                         # noqa: BLE001
            continue
        body = r.get("text") if isinstance(r, dict) else str(r)
        data = ev.extract_json(body or "")
        for item in (data or {}).get("values", []) or []:
            q = ev.norm(str(item.get("quote", "")))
            item["paper"], item["asked"] = path.stem, qnum
            item["qfile"] = QFILE_STEM[0]
            item["project"] = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
            if q and len(q) > 15 and q in hay:
                item["verified_quote"] = True
                kept.append(item)
            else:
                item["verified_quote"] = False
                bad.append(item)
    return kept, bad


def run_abstracts_all(questions, queries, per, write) -> int:
    """Fetch by question, then ask each abstract EVERY question in one call.

    WHY. The per-pair version asks one abstract one question, so a search that returns 25
    abstracts spends 25 calls to test 25 hypotheses -- and an abstract fetched for the fin-ray
    question is thrown away even when it states a body mass that another open constraint needs.
    Measured on the first run: 2 verified values from about 175 abstract-question pairs.

    The questions all fit in one prompt beside an abstract, which is a few hundred words, so the
    call costs essentially the same and tests twenty hypotheses instead of one. The search is
    still per-question -- that is what puts a relevant paper in front of the model at all -- only
    the asking is pooled.
    """
    qblock = "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1))
    kept_all, bad_all, asked, seen = [], [], 0, set()
    for i, question in enumerate(questions, 1):
        qstr = queries.get(i)
        if not qstr:
            continue
        recs = epmc_search(qstr, n=per)
        fresh = [r for r in recs if (r["src"], r["id"]) not in seen]
        for r in fresh:
            seen.add((r["src"], r["id"]))
        print(f"  Q{i:<2} {question[:46]:<46} {len(recs):>3} found, {len(fresh):>3} new")
        for rec in fresh:
            label = f"{rec['src']}{rec['id']}"
            blob = f"{rec['title']}\n\n{rec['abstract']}"
            t1 = TENANTS[asked % len(TENANTS)]
            t2 = TENANTS[(asked + 1) % len(TENANTS)]
            k, b = ask_confirmed(blob, label, qblock, i, t1, t2)
            asked += 1
            for it in k:
                it["read_level"] = "abstract"
                it["journal"], it["year"], it["doi"] = rec["journal"], rec["year"], rec["doi"]
                print(f"      {label:<13} Q{str(it.get('question'))[:2]:<3} "
                      f"{str(it.get('value'))[:22]:<22} {str(it.get('units'))[:13]:<13} "
                      f"{str(it.get('provenance'))[:13]:<13} {rec['journal'][:22]}")
            kept_all += k
            bad_all += b
        if write:
            flush(OUT / ("abstracts_" + OUTFILE[0]), kept_all, bad_all)
        time.sleep(PAUSE_S)

    print("\n" + "-" * 78)
    print(f"  {asked} abstract(s) asked, each against all {len(questions)} questions")
    print(f"  {len(kept_all)} value(s) with a quote VERIFIED; {len(bad_all)} DISCARDED")
    if kept_all or bad_all:
        print(f"  paraphrase/fabrication rate: "
              f"{100.0 * len(bad_all) / (len(kept_all) + len(bad_all)):.1f}%")
    prov: dict[str, int] = {}
    for it in kept_all:
        prov[str(it.get("provenance", "unstated"))] = prov.get(str(it.get("provenance", "unstated")), 0) + 1
    print(f"  provenance: {prov}")
    print("-" * 78)
    if write:
        OUT.mkdir(parents=True, exist_ok=True)
        dest = OUT / ("abstracts_" + OUTFILE[0])
        prev = {"verified": [], "discarded": []}
        if dest.exists():
            try:
                prev = json.loads(dest.read_text())
            except Exception:                                     # noqa: BLE001
                pass
        prev["verified"] += kept_all
        prev["discarded"] += bad_all
        dest.write_text(json.dumps(prev, indent=1))
        print(f"\n  wrote {dest} ({len(prev['verified'])} verified in all)")
    return 0


def run_abstracts(questions, queries, per, write) -> int:
    """The abstract route: Europe PMC covers journals PMC's OA subset does not.

    Every value from here is labelled `read_level: abstract`. That is weaker evidence than full
    text and the label is the whole point -- a number read in an abstract carries no methods and
    no conditions, and writing it up as though the paper had been read is the failure
    docs/research/README.md exists to prevent.
    """
    kept_all, bad_all, asked = [], [], 0
    for i, question in enumerate(questions, 1):
        qstr = queries.get(i)
        if not qstr:
            continue
        recs = epmc_search(qstr, n=per)
        print(f"  Q{i:<2} {question[:50]:<50} {len(recs):>3} abstract(s)")
        for rec in recs:
            label = f"{rec['src']}{rec['id']}"
            blob = f"{rec['title']}\n\n{rec['abstract']}"
            k, b = ask_text(blob, label, question, i, TENANTS[asked % len(TENANTS)])
            asked += 1
            for it in k:
                it["read_level"] = "abstract"
                it["journal"] = rec["journal"]
                it["year"] = rec["year"]
                it["doi"] = rec["doi"]
                print(f"      {label:<13} {str(it.get('value'))[:24]:<24} "
                      f"{str(it.get('units'))[:14]:<14} {str(it.get('provenance'))[:13]:<13} "
                      f"{rec['journal'][:24]}")
            kept_all += k
            bad_all += b
        time.sleep(PAUSE_S)

    print("\n" + "-" * 78)
    print(f"  {asked} abstract-question pair(s) asked")
    print(f"  {len(kept_all)} value(s) with a quote VERIFIED against the abstract")
    print(f"  {len(bad_all)} DISCARDED because the quote was not in it")
    if kept_all or bad_all:
        print(f"  paraphrase/fabrication rate: "
              f"{100.0 * len(bad_all) / (len(kept_all) + len(bad_all)):.1f}%")
    prov: dict[str, int] = {}
    for it in kept_all:
        prov[str(it.get("provenance", "unstated"))] = prov.get(str(it.get("provenance", "unstated")), 0) + 1
    print(f"  provenance: {prov}")
    print("-" * 78)
    if write:
        OUT.mkdir(parents=True, exist_ok=True)
        dest = OUT / ("abstracts_" + OUTFILE[0])
        prev = {"verified": [], "discarded": []}
        if dest.exists():
            try:
                prev = json.loads(dest.read_text())
            except Exception:                                     # noqa: BLE001
                pass
        prev["verified"] += kept_all
        prev["discarded"] += bad_all
        dest.write_text(json.dumps(prev, indent=1))
        print(f"\n  wrote {dest} ({len(prev['verified'])} verified in all)")
    return 0


def main() -> int:
    qpath = pathlib.Path(sys.argv[sys.argv.index("--questions") + 1]) if "--questions" in sys.argv \
        else OUT / "questions_gen.txt"
    per = int(os.environ.get("HARVEST_PER_QUERY", "6"))
    write = "--write" in sys.argv
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0

    QFILE_STEM[0] = qpath.name
    if "--out" in sys.argv:
        OUTFILE[0] = sys.argv[sys.argv.index("--out") + 1]
    else:
        OUTFILE[0] = f"harvest_{qpath.stem}.json"
    questions = read_questions(qpath)
    if limit:
        questions = questions[:limit]
    if not questions:
        print(f"no questions in {qpath}")
        return 1

    print("=" * 78)
    print("TARGETED HARVEST -- one search per question, then that question only")
    print("=" * 78)
    ok, why = ce.controls_pass()
    print(f"  [{'ok' if ok else 'FAIL'}] search controls: {why}")
    if not ok:
        print("\n  ABORTING: without both controls a zero haul and a broken search look alike.")
        return 2

    queries = write_queries(questions)
    print(f"  {len(questions)} question(s); {len(queries)} query(ies) written by the model\n")
    if not queries:
        print("  no queries came back; aborting rather than searching on the question text")
        return 2

    abstracts_mode = "--abstracts" in sys.argv
    if abstracts_mode:
        if "--one-question-each" in sys.argv:
            return run_abstracts(questions, queries, per, write)
        return run_abstracts_all(questions, queries, per, write)

    store = ff.OUT
    store.mkdir(parents=True, exist_ok=True)
    held_before = {p.stem for p in store.glob("*.txt")}
    kept_all, bad_all, asked, fetched = [], [], 0, 0

    for i, question in enumerate(questions, 1):
        qstr = queries.get(i)
        if not qstr:
            continue
        try:
            hits = ce.esearch(qstr, n=per)
        except Exception as e:                                    # noqa: BLE001
            print(f"  Q{i:<2} SEARCH FAILED {type(e).__name__}")
            continue
        print(f"  Q{i:<2} {question[:52]:<52} {len(hits):>2} hits  [{qstr[:40]}]")
        for pmcid in hits:
            p = harvest(pmcid, store)
            time.sleep(PAUSE_S)
            if p is None:
                continue
            if p.stem not in held_before:
                fetched += 1
            k, b = ask(p, question, i, TENANTS[asked % len(TENANTS)])
            asked += 1
            kept_all += k
            bad_all += b
            if k:
                for it in k:
                    print(f"      {pmcid:<13} {str(it.get('value'))[:26]:<26} "
                          f"{str(it.get('units'))[:16]:<16} {str(it.get('provenance'))[:14]}")
        if write:
            flush(OUT / OUTFILE[0], kept_all, bad_all)

    print("\n" + "-" * 78)
    print(f"  {asked} paper-question pair(s) asked, {fetched} paper(s) newly fetched")
    print(f"  {len(kept_all)} value(s) with a quote VERIFIED against the source")
    print(f"  {len(bad_all)} DISCARDED because the quote was not in the text")
    if kept_all or bad_all:
        rate = 100.0 * len(bad_all) / (len(kept_all) + len(bad_all))
        print(f"  paraphrase/fabrication rate: {rate:.1f}%")
    by_prov: dict[str, int] = {}
    for it in kept_all:
        by_prov[str(it.get("provenance", "unstated"))] = \
            by_prov.get(str(it.get("provenance", "unstated")), 0) + 1
    print(f"  provenance: {by_prov}")
    print("-" * 78)

    if write:
        dest = OUT / OUTFILE[0]
        OUT.mkdir(parents=True, exist_ok=True)
        prev = {"verified": [], "discarded": []}
        if dest.exists():
            try:
                prev = json.loads(dest.read_text())
            except Exception:                                     # noqa: BLE001
                pass
        prev["verified"] = prev.get("verified", []) + kept_all
        prev["discarded"] = prev.get("discarded", []) + bad_all
        dest.write_text(json.dumps(prev, indent=1))
        print(f"\n  wrote {dest} ({len(prev['verified'])} verified in all)")
    else:
        print("\n  (dry run; pass --write to save)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
