#!/usr/bin/env python3
"""Generate the full-text extraction question list from the project's OPEN needs.

WHY THIS EXISTS, and it is a measured failure rather than a tidiness argument.
`extract_values.py` shipped with six hard-coded questions about fin stiffness, muscle W/kg and
lift coefficients. Run on 2026-11-05 over nine papers that this project ALREADY CITES for a
numeric value, it returned ZERO verified values -- and on the whole 225-paper corpus, zero as
well. The extractor was not broken and the papers were not empty. The questions were stale.

The decisive case is Sutton et al. 2019 (PMC6907395). Four live claims draw on it, for a muscle
energy density of 15 J/kg and a 2.5 g crossover. Question 2 of the hard-coded list asks for
muscle power in W/kg. A paper reporting J/kg answers no question on that list, so an honest
extractor correctly reported nothing, and the project read its own silence as "the corpus has
no values in it".

So the questions are now derived from what the project currently CANNOT answer: the quantities
named by `constraint_entailed` rows still `open`. Those move as the work moves -- the hard-coded
list was written for fin mechanics and the frontier has since gone to water exit, taxi speed,
phosphagen stores and pectoral muscle fraction -- and nothing but this file has to be edited
when they do.

WHAT IT DELIBERATELY DROPS, and why that is a judgement rather than a cleanup.
A constraint whose units are `dimensionless` is nearly always a ratio of two numbers THIS
PROJECT derived -- `frame interval / stage-1 duration`, `curvature-derived strain / directly
measured strain`. No paper contains those; they are our own arithmetic, and asking a literature
extractor for them spends a call to be told no. Quantities carrying a physical unit are the ones
a published methods or results section can actually hold. The filter is therefore on UNITS, not
on wording, and `--keep-dimensionless` turns it off so the choice can be disagreed with.

It does not judge whether a question is ANSWERABLE, only whether it is the kind of thing a paper
states. An open constraint nobody has published on will simply return nothing, which is the
correct answer and costs one call to establish.
"""
from __future__ import annotations

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbq  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
MODEL = "claude-opus-4-5-20251101"

# Units that mean "a paper could state this". A bare ratio is almost always ours; see docstring.
STOP = {"the", "and", "for", "per", "with", "during", "from", "its", "both", "that"}
MERGE_AT = 0.25          # with the subset guard in same_need(); see its docstring
DIMENSIONLESS = {"", "dimensionless", "ratio", "dimensionless ratio", "fraction", "-", "none"}


def words(quantity: str) -> frozenset:
    """Content words. `M_pectoral/M_body` has to yield {pectoral, body}, so underscores and
    slashes are separators: without that it shares no token with `bilateral pectoral muscle
    mass / body mass`, and the two never collapse."""
    flat = "".join(c if c.isalnum() or c.isspace() else " " for c in quantity.lower())
    out = frozenset(w for w in flat.split() if len(w) > 2 and w not in STOP and not w.isdigit())
    return out or frozenset([quantity.lower()])


def jaccard(a: frozenset, b: frozenset) -> float:
    return len(a & b) / len(a | b) if (a | b) else 0.0


def same_need(a: frozenset, b: frozenset) -> bool:
    """Whether two quantity spellings name one need.

    A plain word-overlap score CANNOT do this, and the control is what showed it: `body mass`
    against `bilateral pectoral muscle mass / body mass` scores 0.400, HIGHER than two of the
    four spellings that genuinely are one quantity (0.286 and 0.250). A short quantity is a
    subset of every ratio built from it, so no threshold separates the two cases.

    The subset itself is the discriminator. `body mass` is a DIFFERENT, simpler quantity than a
    ratio that contains it, and a paper answering one does not answer the other. So a strict
    subset is refused outright, and the threshold then only has to separate genuine restatements
    from unrelated quantities, which it does (0.000 for both unrelated pairs tested)."""
    if a <= b or b <= a:
        return False
    return jaccard(a, b) >= MERGE_AT


def open_quantities(limit: int = 400) -> list[tuple[str, str, int]]:
    rows = dbq.q(
        "select quantity, coalesce(units,''), count(*)::text from constraint_entailed "
        f"where project_id = {dbq.lit(PROJECT)} and status = 'open' and quantity is not null "
        f"group by 1,2 order by 3 desc, 1 limit {int(limit)}")
    return [(r[0], r[1], int(r[2])) for r in rows if r and r[0]]


def is_physical(units: str) -> bool:
    return units.strip().lower() not in DIMENSIONLESS


def build(keep_dimensionless: bool = False, cap: int = 18) -> tuple[str, int, int]:
    qs = open_quantities()
    kept = [q for q in qs if keep_dimensionless or is_physical(q[1])]
    dropped = len(qs) - len(kept)

    # DEDUPE. Four of the first eighteen were the same quantity under four spellings
    # (`M_pectoral/M_body in aerial teleosts`, `adult zebrafish pectoral muscle mass / body
    # mass`, `bilateral pectoral muscle mass / body mass`, `M_pectoral(both fins)/M_body`), which
    # spends four questions on one need. Collapse on the content words, keep the wording that the
    # most constraints used, and carry the combined demand so ranking still sees it.
    merged: dict[frozenset, list] = {}
    for quantity, units, n in kept:
        key = words(quantity)
        hit = None
        for k in merged:
            if same_need(k, key):
                hit = k
                break
        if hit is not None:
            merged[hit][2] += n
            if n > merged[hit][3]:
                merged[hit][0], merged[hit][1], merged[hit][3] = quantity, units, n
        else:
            merged[key] = [quantity, units, n, n]
    collapsed = len(kept) - len(merged)
    kept = [(v[0], v[1], v[2]) for v in merged.values()]

    # Most-wanted first. The tie-break is a stable HASH, not the quantity text: sorting ties
    # alphabetically truncated an 18-question list at the letter "b" and never showed the
    # extractor anything past it.
    kept.sort(key=lambda t: (-t[2], hashlib.sha256(t[0].encode()).hexdigest()))
    lines = []
    for i, (quantity, units, n) in enumerate(kept[:cap], 1):
        u = f" Units wanted: {units}." if units.strip() else ""
        many = f" ({n} open constraints need this.)" if n > 1 else ""
        lines.append(f"{i}. {quantity}.{u}{many}\n   Report the species and the body length or "
                     f"life stage if the paper states them.")
    return "\n".join(lines), len(kept[:cap]), dropped, collapsed


GENERALISE = """These are quantities a research project currently cannot answer. Each was written
for that project's own argument, so many are phrased as ITS arithmetic rather than as something a
published paper would ever state.

Rewrite each one as a question the METHODS or RESULTS section of a real paper could answer, and
drop the ones that no paper could.

    KEEP and generalise:  "phosphagen free-energy store per kg fast muscle, compared with the
                          cost of one start (about 57 J/kg, derived assuming 0.1 s and
                          efficiency 0.25)"  ->  "phosphagen (PCr/ATP) free-energy store per kg
                          of fast/white muscle, in J/kg"
    KEEP and generalise:  "M_pectoral/M_body in aerial teleosts"  ->  "pectoral muscle mass as a
                          fraction of body mass, in any teleost fish"
    DROP:                 "available minus required mass-specific power"  -- a difference between
                          two numbers THIS project computed; no paper reports it.
    DROP:                 "time to reach U_min from 0.45 m/s compared with the fall-back time"
                          -- a comparison internal to this project's model.

Widen the species: this project works on zebrafish, but a value from any fish, or from another
animal where the physiology carries over, is wanted. Say so in the question.

QUANTITIES:
{items}

Reply with JSON only:
{{"questions": [{{"n": <the number above>, "question": "...", "units": "...", "keep": true}},
                {{"n": <number>, "keep": false, "why": "..."}}]}}
"""


def generalise(items: list[tuple[str, str, int]], tenant_list, call_fn, model: str):
    """Turn project-internal quantities into questions a paper could answer.

    WHY. With the quantities used verbatim, extraction returned zero verified values from nine
    papers in three separate runs. The decisive example: Sutton et al. 2019 states a muscle
    energy density of 15.0 J/kg in plain words, and NO question on the verbatim list asks for
    muscle energy density -- the nearest was "phosphagen free-energy store per kg fast muscle,
    compared with the cost of one start (about 57 J/kg, derived assuming ...)", which names this
    project's own comparison and not the paper's quantity. The filter on units removed ratios;
    it could not remove a derived quantity that happens to carry W/kg.
    """
    numbered = "\n".join(f"{i}. {q} [units: {u or 'unstated'}]" for i, (q, u, _) in enumerate(items, 1))
    r = call_fn(tenant_list[0], GENERALISE.format(items=numbered), max_tokens=4000, model=model)
    body = r.get("text") if isinstance(r, dict) else str(r)
    import json as _json
    import re as _re
    m = _re.search(r"\{.*\}", body or "", _re.S)
    if not m:
        return None, "no JSON in reply"
    try:
        data = _json.loads(m.group(0))
    except Exception as e:                                    # noqa: BLE001
        return None, f"unparseable JSON: {e}"
    return data.get("questions"), ""


def main() -> int:
    keep = "--keep-dimensionless" in sys.argv
    cap = 18
    if "--cap" in sys.argv:
        cap = int(sys.argv[sys.argv.index("--cap") + 1])
    text, n, dropped, collapsed = build(keep, cap)

    gen_note = ""
    if "--generalise" in sys.argv:
        from api_challenge import TENANTS, call      # api_allen excluded in exactly one place
        items = [(q, u, c) for q, u, c in open_quantities()
                 if keep or is_physical(u)][:40]
        qs, err = generalise(items, TENANTS, call, MODEL)
        if qs is None:
            print(f"  generalisation FAILED ({err}); keeping the verbatim quantities")
        else:
            kept_q = [q for q in qs if q.get("keep") and q.get("question")]
            # TWO-SIDED CONTROL on the generalisation, not just on the filter. A step that
            # keeps everything and a step that drops everything both "work" on one example.
            joined = " ".join(str(q.get("question", "")).lower() for q in kept_q)
            dropped_n = {q.get("n") for q in qs if not q.get("keep")}
            must_keep = "muscle" in joined and ("mass" in joined or "power" in joined)
            must_drop = any("available minus required" in items[n - 1][0].lower()
                            for n in dropped_n if isinstance(n, int) and 1 <= n <= len(items))
            if not (kept_q and must_keep):
                print("  generalisation CONTROL FAILED -- keeping the verbatim quantities")
            else:
                lines = []
                for i, q in enumerate(kept_q[:cap], 1):
                    u = f" Units wanted: {q['units']}." if q.get("units") else ""
                    lines.append(f"{i}. {q['question']}.{u}\n   Report the species and the body "
                                 f"length or life stage if the paper states them.")
                text, n = "\n".join(lines), len(lines)
                gen_note = (f"  generalised by model: {len(kept_q)} kept, "
                            f"{len(dropped_n)} dropped as project-internal arithmetic "
                            f"[{'ok' if must_drop else 'WEAK'}] control: dropped a known "
                            f"internal difference = {must_drop}")

    # TWO-SIDED CONTROL. A generator that emits nothing and a generator pointed at an empty
    # database print the same thing, and a filter that drops everything looks like a strict one.
    low = text.lower()
    must_find = "water-exit speed" in low or "tail-beat frequency" in low or "muscle" in low
    must_drop = "frame interval" not in low          # a ratio of OUR OWN timings
    ok = n > 0 and must_find and (must_drop or keep)
    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        if not ok:
            print("CONTROL FAILED -- refusing to write a question list that cannot be trusted")
            print(f"  questions={n} must_find={must_find} must_drop={must_drop}")
            return 2
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {path}")
    if gen_note:
        print(gen_note)
    print(f"  {n} question(s) from OPEN constraints; {dropped} dropped as dimensionless "
          f"(ours, not a paper's), {collapsed} collapsed as restatements of another")
    print(f"  [{'ok' if ok else 'FAIL'}] control: finds a known live need, drops a known "
          f"internal ratio")
    print()
    print(text)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
