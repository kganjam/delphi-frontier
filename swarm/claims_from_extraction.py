#!/usr/bin/env python3
"""Put verified extracted values into the claim graph, with the paper's provenance preserved.

WHY THIS EXISTS. `extract_values.py --write` wrote a JSON file and stopped. 225 retrieved full
texts, a working quote check and a correct refusal to fabricate all dead-ended in
`results/extracted-values.json`, which nothing read. A retrieval pipeline whose output no part
of the system consumes is indistinguishable from one that was never run -- and for a while it
was literally indistinguishable, because the file contained `{"verified": [], "discarded": []}`.

THE EVIDENCE LABEL IS THE WHOLE JOB, and it is NOT `measured`.
This project did not measure any of these numbers; a published paper did, or modelled it, or
quoted it from somewhere else. The extractor records which, in `provenance`, and that maps onto
this project's closed evidence vocabulary:

    measured-here  -> literature   the authors measured it and we READ that
    quoted         -> literature   the paper attributes it to an earlier study; attribution kept
    modelled-here  -> simulated    an output of that paper's model, not an observation
    assumed-here   -> assumed      a constant their model takes as input
    unclear        -> unknown      the excerpt did not say, and guessing is worse than not

Nothing here is written as `measured`. That matters because the project's own goal scoreboard
counts `measured` claims carrying a biological scale, and relabelling literature as measurement
would move that number without a single new observation existing. The row is supposed to be hard.

WHAT A `read_level: abstract` ROW IS AND IS NOT. Most of these come from abstracts, because the
measurements this project needs are in journals outside PMC's open-access subset. An abstract
gives the headline number with no methods, no table and no conditions. Each row carries the
label, and a value read in an abstract must never be written up in the voice of having read the
paper (docs/research/README.md). It is a lead with a number attached, and it is a great deal
better than the nothing that was there before.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbq  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
EXTRACT = pathlib.Path(__file__).resolve().parent.parent / "results" / "extract"

EVIDENCE = {
    "measured-here": "literature",
    "quoted": "literature",
    "modelled-here": "simulated",
    "assumed-here": "assumed",
    "unclear": "unknown",
    "": "unknown",
}


def numeric(value) -> float | None:
    """First number in the value string, or None. A range like '0.0001 to 1.5109' keeps its low
    end in value_num and its full text in the statement -- a range is not a scalar, and picking
    the midpoint would invent a number the paper never stated."""
    import re
    if isinstance(value, (int, float)):
        return float(value)
    m = re.search(r"-?\d[\d,]*\.?\d*(?:\s*[x×]\s*10\s*\(?-?\d+\)?)?", str(value or ""))
    if not m:
        return None
    raw = m.group(0).replace(",", "")
    exp = re.search(r"[x×]\s*10\s*\(?(-?\d+)\)?", raw)
    try:
        base = float(re.split(r"[x×]", raw)[0].strip())
        return base * (10 ** int(exp.group(1))) if exp else base
    except Exception:                                             # noqa: BLE001
        return None


def load(paths: list[pathlib.Path]) -> list[dict]:
    out = []
    for p in paths:
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:                                         # noqa: BLE001
            continue
        for v in d.get("verified", []):
            if v.get("verified_quote"):
                v["_file"] = p.name
                out.append(v)
    return out


def for_this_project(items: list[dict]) -> tuple[list[dict], int]:
    """Keep only values harvested FOR this project.

    Every harvest file sits in one directory and the bridge reads all of them, so a value's own
    record of which project it was gathered for is the only thing separating them. Without it,
    running this with SWARM_PROJECT=coral attributes zebrafish fin-ray stiffness to coral -- 43
    such rows were one keystroke from being written that way.

    A value with no `project` stamp predates the stamp, and every run before it was
    zebrafish-flight, so that is what it is treated as. The count of skipped rows is printed
    rather than hidden, because a project with no harvest of its own should show zero here and
    not silently inherit another project's corpus."""
    keep, skipped = [], 0
    for v in items:
        if str(v.get("project") or "zebrafish-flight") == PROJECT:
            keep.append(v)
        else:
            skipped += 1
    return keep, skipped


def source_string(it: dict) -> str:
    bits = [str(it.get("paper", "")).strip()]
    for key in ("journal", "year", "doi"):
        if it.get(key):
            bits.append(str(it[key]))
    if it.get("provenance") == "quoted" and it.get("attributed_to"):
        bits.append(f"value attributed by that paper to {it['attributed_to']}")
    bits.append(f'quote verified against the source: "{str(it.get("quote", ""))[:220]}"')
    return "; ".join(b for b in bits if b)


def load_question_text() -> dict[str, dict[str, str]]:
    """questions-file name -> {question number -> the question's own text}.

    WHY THE TEXT AND NOT JUST THE NUMBER. The statement used to end `asked: question 7 of the
    open-constraint question set`, which is unresolvable twice over. There are eight question
    files and they renumber independently, so a bare 7 does not identify a question at all --
    the same ambiguity load_scale_map() documents for the scale join, left in the prose. And
    even resolved, the number alone does not let a reader judge RELEVANCE, which is the thing
    most worth judging here: the harvester asks a paper for one quantity and the paper's tables
    contain many, so a value can be quote-verified, correctly attributed, and still not be an
    answer to what was asked. The husbandry temperatures pulled from PMC10503471 while asking
    for tail-beat amplitude are the worked example. Carrying the question lets that be seen
    instead of inferred.
    """
    out: dict[str, dict[str, str]] = {}
    for mp in sorted(EXTRACT.glob("*.map.json")):
        stem = mp.name[:-len(".map.json")]
        try:
            rows = json.loads(mp.read_text())
        except Exception:                                         # noqa: BLE001
            continue
        for k, v in rows.items():
            t = (v or {}).get("question")
            if t:
                out.setdefault(stem, {})[str(k)] = str(t)
    return out


def statement(it: dict, qtext: dict[str, dict[str, str]] | None = None) -> str:
    prov = str(it.get("provenance", "unclear"))
    how = {"measured-here": "MEASURED BY THAT PAPER",
           "modelled-here": "AN OUTPUT OF THAT PAPER'S MODEL, NOT AN OBSERVATION",
           "assumed-here": "A CONSTANT THAT PAPER'S MODEL ASSUMES",
           "quoted": "QUOTED BY THAT PAPER FROM AN EARLIER STUDY",
           "unclear": "PROVENANCE NOT DETERMINABLE FROM THE TEXT READ"}.get(prov, prov)
    sp = str(it.get("species") or "unstated")
    cond = str(it.get("conditions") or "unstated")
    lvl = str(it.get("read_level") or "full-text")
    return (f"[LITERATURE VALUE, {how}] {it.get('value')} {it.get('units') or ''}".strip()
            + f"\nspecies: {sp}\nconditions: {cond}\n"
            + f"read level: {lvl} -- "
            + ("an abstract states a number without its methods, table or conditions; this is a "
               "lead with a number attached and is not a reading of the paper"
               if lvl == "abstract" else "full text read")
            + f"\nasked: question {it.get('asked')} of {it.get('qfile') or 'an unrecorded question file'}"
            + (f"\nthe question was: {_qtext(qtext, it)}" if _qtext(qtext, it) else
               "\nthe question text was not recoverable, so RELEVANCE CANNOT BE JUDGED from this "
               "record alone -- the value is verified against its paper, not against the question")
            + _unit_note(qtext, it))


#: Strings that all denote a DIMENSIONLESS quantity. A fraction, a percentage and a
#: body-length-normalised ratio differ by a SCALE FACTOR, not by dimension, so for the question
#: this annotation asks -- does the value answer the question? -- they are the same quantity.
#:
#: MEASURED 2026-11-05, and the instrument was wrong on the project it had not been checked on.
#: The first version compared unit strings literally. On zebrafish-flight that gives 20.9 per
#: cent matching, and adding this equivalence set moves it to 20.8 -- no material change,
#: because that project's questions mostly want physical units. On insect-flight the literal
#: comparison gives 3.8 per cent and the equivalence set gives 23.0, because its questions ask
#: for fractions of body mass and body-length-normalised ratios, and the harvester answers in
#: `%`, `dimensionless` and `unitless`. A six-fold error, invisible on the project the check was
#: built against. Same shape as the borrowed control in classify_scale.py: an instrument
#: validated on one project and applied to another without being re-validated there.
DIMENSIONLESS = {
    "dimensionless", "unitless", "fraction", "ratio", "%", "percent", "percentage", "none", "-",
    "body lengths", "body weights", "body length", "body weight", "bl", "x", "fold", "times",
    "fraction of body mass", "fraction of body weight",
}


def _canon_unit(u: str) -> str:
    """Canonical form for the comparison: dimensionless synonyms collapse to one token."""
    flat = (u or "").strip().lower()
    if not flat:
        return ""
    if flat in DIMENSIONLESS or flat.replace(" ", "") in {d.replace(" ", "") for d in DIMENSIONLESS}:
        return "@dimensionless"
    return flat.replace(" ", "")


def _unit_note(qtext: dict | None, it: dict) -> str:
    """Do the value's units match the units the question asked for?

    MEASURED 2026-11-05 over 1833 verified values: 20.9 percent match, 71.5 percent do NOT, and
    7.6 percent have no units on one side. The mismatches are not formatting variants -- the
    commonest pairs are Hz wanted against cm found, N against W, g against p-Value, Pa against
    mm, and `W/kg body mass` against `Percentage of total blood flow`. The harvester asks a
    paper one question and extracts the numbers the paper contains, so a value can be
    quote-verified, correctly attributed and still be an answer to nothing that was asked.

    This ANNOTATES rather than filters. A unit string is a crude test: it cannot see that mm
    converts to body lengths given a length, and it would throw away a real answer written in
    an unexpected unit. Dropping rows on it would also hide the measurement above, which is
    worth keeping visible. So every claim carries the comparison and a reader or a downstream
    query can act on it.
    """
    want = ((_QUNITS.get(str(it.get("qfile")), {}) or {}).get(str(it.get("asked"))) or "").strip()
    got = str(it.get("units") or "").strip()
    if not want or not got:
        return ""
    w, g = _canon_unit(want), _canon_unit(got)
    # substring matching is for real units only -- "@dimensionless" must match exactly, or it
    # would absorb anything containing it.
    if w == g or (w != "@dimensionless" and g != "@dimensionless" and (w in g or g in w)):
        return f"\nunits asked for: {want} -- the value's units MATCH"
    return (f"\nunits asked for: {want} -- the value's units are {got}, which DO NOT MATCH. "
            f"This value is verified against its paper but may not answer the question above.")


_QUNITS: dict[str, dict[str, str]] = {}


def load_question_units() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for mp in sorted(EXTRACT.glob("*.map.json")):
        stem = mp.name[:-len(".map.json")]
        try:
            rows = json.loads(mp.read_text())
        except Exception:                                         # noqa: BLE001
            continue
        for k, v in rows.items():
            u = (v or {}).get("units")
            if u:
                out.setdefault(stem, {})[str(k)] = str(u)
    return out


def _qtext(qtext: dict | None, it: dict) -> str:
    if not qtext:
        return ""
    return (qtext.get(str(it.get("qfile")), {}) or {}).get(str(it.get("asked")), "")


def load_scale_map() -> dict:
    """questions-file name -> {question number -> the scale its ORIGINATING CONSTRAINT declared}.

    KEYED BY FILE, because a question number alone is not an identifier. Two question files
    generated from the same constraints renumber them differently, so joining a value stamped
    `asked: 7` to whichever map happened to sort first would attach a confident scale drawn from
    a different question. Values carry `qfile`; a value without one gets no scale.

    This is inherited provenance, not a judgement. The scale comes from whichever
    constraint_entailed row phrased the quantity, and those rows disagree with each other:
    fin-ray flexural stiffness is `tissue` on one constraint and `protein` on another, and
    membrane potential is `cell` on one and `protein` on another. Both pairs are the same
    physical quantity. So a scale here says "the constraint that wanted this called it X", which
    is worth recording and is NOT the same as this pipeline having decided the scale.

    A question whose quantity maps to more than one scale is left NULL rather than resolved,
    because picking one would turn an inherited disagreement into an assertion.
    """
    out: dict[str, dict[str, str]] = {}
    for mp in sorted(EXTRACT.glob("*.map.json")):
        stem = mp.name[:-len(".map.json")]
        try:
            rows = json.loads(mp.read_text())
        except Exception:                                         # noqa: BLE001
            continue
        for k, v in rows.items():
            sc = v.get("scales") or []
            if len(sc) == 1:
                out.setdefault(stem, {})[str(k)] = sc[0]
    return out


def main() -> int:
    write = "--write" in sys.argv
    # Every harvest file, because each run now writes its own (a fixed name let two concurrent
    # harvests overwrite each other). Sorted so the set read is reproducible.
    files = sorted(EXTRACT.glob("*.json"))
    files = [f for f in files if not f.name.endswith(".map.json")]
    files.append(EXTRACT.parent / "extracted-values.json")
    items = load(files)
    items, other_project = for_this_project(items)
    smap = load_scale_map()
    qtext = load_question_text()
    globals()["_QUNITS"] = load_question_units()
    print("=" * 78)
    print("EXTRACTED VALUES -> CLAIMS")
    print("=" * 78)
    print(f"  {len(items)} verified value(s) for project {PROJECT!r} in "
          f"{len([f for f in files if f.exists()])} file(s); {other_project} skipped as "
          f"belonging to another project")
    print("  scale maps: " + ", ".join(f"{k} ({len(v)} q)" for k, v in smap.items()) if smap
          else "  no scale map found; every row will be NULL")

    # Dedupe against what is already recorded. The source string carries the paper id and the
    # quote, so re-running the harvester cannot double-record the same sentence.
    existing = {r[0] for r in dbq.q(
        f"select source from claim where project_id = {dbq.lit(PROJECT)} "
        "and source like '%quote verified against the source%'")}
    rows, skipped, nonum = [], 0, 0
    for it in items:
        src = source_string(it)
        if src in existing:
            skipped += 1
            continue
        existing.add(src)
        if numeric(it.get("value")) is None:
            nonum += 1
        rows.append((it, src))

    by_ev: dict[str, int] = {}
    for it, _ in rows:
        ev = EVIDENCE.get(str(it.get("provenance", "")), "unknown")
        by_ev[ev] = by_ev.get(ev, 0) + 1
    print(f"  {len(rows)} new, {skipped} already recorded, {nonum} with no parseable number")
    print(f"  evidence mapping: {by_ev}")
    print("  NOTE: none of these is `measured`. This project measured none of them; the "
          "goal scoreboard's measured-with-a-scale row does NOT move, by design.")

    # TWO-SIDED CONTROL on the mapping itself, before anything is written.
    probe = {"provenance": "modelled-here", "value": "565 × 10(-6)", "units": "N m^2"}
    must_not_be_measured = EVIDENCE[probe["provenance"]] == "simulated"
    must_parse = abs((numeric(probe["value"]) or 0) - 565e-6) < 1e-9
    must_reject = numeric("no number here at all") is None
    ok = must_not_be_measured and must_parse and must_reject
    print(f"  [{'ok' if ok else 'FAIL'}] controls: a modelled value maps to `simulated` "
          f"({must_not_be_measured}); 565 x 10(-6) parses to 5.65e-4 ({must_parse}); "
          f"prose yields no number ({must_reject})")
    if not ok:
        print("\n  ABORTING: the mapping is what this module is for.")
        return 2

    for it, src in rows[:12]:
        print(f"    {str(it.get('paper'))[:13]:<13} {str(it.get('value'))[:22]:<22} "
              f"{str(it.get('units'))[:12]:<12} {EVIDENCE.get(str(it.get('provenance')), '?'):<11} "
              f"{str(it.get('read_level') or 'full-text')}")

    if not write:
        print("\n  (dry run; pass --write to record)")
        return 0

    n = 0
    for it, src in rows:
        scale = smap.get(str(it.get("qfile", "")), {}).get(str(it.get("asked")))
        # A NUMBER WITH NO UNIT IS NOT A QUANTITY, which is SPEC ASK-artifact-graph rule 5 in
        # its own words, and writing one here turned that rule red on 2026-11-05: 10 of the 411
        # claims this module wrote committed a value_num with an empty units string. All ten
        # were genuinely dimensionless -- seven conductivity anisotropy ratios and three Q10
        # coefficients -- but the extractor never said so, and asserting `dimensionless` on the
        # module's behalf would be this pipeline inventing a unit from a conditions string it
        # does not parse. So the number stays in the statement, where it is readable with its
        # conditions and its provenance, and value_num is left NULL: the row records what the
        # paper said without claiming to be a quantity the graph can compute on.
        units = str(it.get("units") or "").strip()[:400]
        cid = dbq.write_claim(PROJECT, scale, statement(it, qtext),
                              EVIDENCE.get(str(it.get("provenance", "")), "unknown"),
                              numeric(it.get("value")) if units else None, units,
                              src, str(it.get("read_level") or "full-text"))
        n += 1 if cid else 0
    withscale = sum(1 for it, _ in rows
                    if smap.get(str(it.get("qfile", "")), {}).get(str(it.get("asked"))))
    print(f"\n  recorded {n} claim(s); {withscale} carry a scale INHERITED from the "
          f"originating constraint, {n - withscale} are NULL")
    print("  An inherited scale is not this pipeline's judgement. The constraint rows disagree "
          "with each other -- fin-ray stiffness is `tissue` on one and `protein` on another -- "
          "so a question whose quantity maps to more than one scale is left NULL rather than "
          "resolved, because picking one would turn an inherited disagreement into an assertion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
