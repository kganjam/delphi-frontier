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
OUT = pathlib.Path(__file__).resolve().parent.parent / "results" / "extract"
PAUSE_S = 0.4

QUERY_PROMPT = """Write a PubMed Central search query for each question below.

The query will be sent to NCBI esearch against PMC. Use the vocabulary a paper would use, not the
question's wording. Prefer a few strong terms joined with AND over a long disjunction, and do not
restrict to one species unless the question does.

QUESTIONS:
{items}

Reply with JSON only:
{{"queries": [{{"n": <question number>, "query": "..."}}]}}
"""


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
    r = call(TENANTS[0], QUERY_PROMPT.format(items=items), max_tokens=3000, model=MODEL)
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
            if q and len(q) > 15 and q in hay:
                item["verified_quote"] = True
                kept.append(item)
            else:
                item["verified_quote"] = False
                bad.append(item)
    return kept, bad


def main() -> int:
    qpath = pathlib.Path(sys.argv[sys.argv.index("--questions") + 1]) if "--questions" in sys.argv \
        else OUT / "questions_gen.txt"
    per = int(os.environ.get("HARVEST_PER_QUERY", "6"))
    write = "--write" in sys.argv
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0

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
        dest = OUT / "targeted.json"
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
