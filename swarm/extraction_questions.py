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
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbq  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
MODEL = "claude-opus-4-5-20251101"

# Units that mean "a paper could state this". A bare ratio is almost always ours; see docstring.
GAP_SCALE: dict[str, str] = {}      # gap sentence -> the scale of the constraint that raised it
STOP = {"the", "and", "for", "per", "with", "during", "from", "its", "both", "that"}
MERGE_AT = 0.25          # with the subset guard in same_need(); see its docstring
_RATIO_FOLD = 9    #: measured 8.94, claim 2769
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


def evidence_gaps(limit: int = 60) -> list[tuple[str, str, int]]:
    """The evidence each open constraint is WAITING ON, in the evaluator's own words.

    WHY THIS BEATS THE QUANTITY LIST. A quantity says what number is wanted; a gap says why the
    numbers already held do not answer it, which is what a search actually has to fix. Measured
    2026-11-05, constraint e28: the quantity is "A_pp / body length", and the project had just
    harvested four values for exactly that quantity (claims 1190-1193, 0.19-0.25 BL). The
    evaluator still returned INSUFFICIENT, because those values are juvenile grass carp in flume
    tests and the constraint is about adult zebrafish escape kinematics. A search built on the
    quantity would have re-found the same inapplicable papers; a search built on the gap looks
    for the adult escape-kinematics paper.

    These sentences exist only because insufficient verdicts are now persisted. Until today they
    were printed and discarded, and the run that produced 30 of them in one batch -- 0 satisfied,
    0 unsatisfied, $0.79 -- is the point at which evaluating existing claims stops paying and
    retrieval has to take over.

    The constraints' own `note` field was the obvious alternative and was measured first: of 139
    open constraints carrying a note, only 6 name missing evidence under a
    needs/requires/no-claim pattern, and 3 of the 4 inspected are false matches. The evaluator
    writes a usable sentence for every insufficient verdict instead.
    """
    rows = dbq.q(
        "select replace(replace(missing_evidence, chr(1), ' '), chr(10), ' '), "
        "coalesce(quantity,''), coalesce(units,''), id::text, coalesce(target_scale,'') "
        f"from constraint_entailed where project_id = {dbq.lit(PROJECT)} and status = 'open' "
        f"and missing_evidence is not null order by missing_evidence_at desc limit {int(limit)}")
    # dbq.q() ALREADY splits each line on chr(1) -- that is its field separator -- so the row
    # arrives as a list of columns, not as one string to split again. Splitting it a second time
    # silently produced zero usable rows from 29 real ones.
    out = []
    for r in rows:
        parts = list(r) if isinstance(r, (list, tuple)) else [str(r)]
        if len(parts) >= 3 and parts[0].strip():
            out.append((parts[0].strip(), parts[2].strip(), 1))
            # A gap inherits the scale of the constraint that raised it. Unlike the quantity
            # route, that is a ONE-TO-ONE link -- this sentence came from exactly this row -- so
            # there is no disagreement between constraints to resolve, and no guessing.
            GAP_SCALE[parts[0].strip()] = parts[4].strip() if len(parts) > 4 else ""
    return out


def open_quantities(limit: int = 400) -> list[tuple[str, str, int]]:
    rows = dbq.q(
        "select quantity, coalesce(units,''), count(*)::text from constraint_entailed "
        f"where project_id = {dbq.lit(PROJECT)} and status = 'open' and quantity is not null "
        f"group by 1,2 order by 3 desc, 1 limit {int(limit)}")
    return [(r[0], r[1], int(r[2])) for r in rows if r and r[0]]


def is_physical(units: str) -> bool:
    return units.strip().lower() not in DIMENSIONLESS


#: dimensionless phrases that merely NAME a ratio; these are pure numbers, not quotients of units
_DIMLESS_PHRASE = re.compile(r'^(fraction|proportion|ratio|percent|percentage|%)\b', re.I)


#: Ratios that papers DO report directly, so decomposing them would cost rather than gain.
#: MEASURED per question: `m/s` matches at 12.9 per cent over 186 values, while the other eight
#: ratio-unit questions in this database -- S/cm^2, W/kg body mass, mol m^-2 s^-1 (twice),
#: degC/generation (twice), degC/year, degC-weeks/year -- sit at 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
#: 0.0 and 6.8 per cent, seven of them at LITERALLY ZERO across 786 values. The distinction is
#: not dimensional: it is whether the quotient is a quantity a paper names in its own right.
#: Speed is; mass-specific power is not.
STANDARD_RATIOS = {
    "m/s", "cm/s", "mm/s", "km/h", "m/s^2", "m/s2", "rad/s", "deg/s", "rev/s",
    "kg/m^3", "g/cm^3", "g/ml", "mg/ml", "mol/l", "ml/min", "l/min", "m^2/s", "mm^2/s",
}


def ratio_unit(units: str) -> tuple[str, str] | None:
    """If the unit DIVIDES one dimension by another, return (numerator, denominator).

    MEASURED, and it is the sharpest predictor of a wasted question this project has: over all
    52 question-sets and 4710 compared values, questions asking a RATIO unit had their answer
    come back in the units they asked for 2.9 per cent of the time, against 26.2 per cent for
    every other question -- a 8.9-fold difference (claim 2769). Papers report masses and powers;
    they rarely report mass-specific power. Asking for the quotient is close to futile.

    So a ratio question is split into its two factors, each asked in its own simple unit, and
    the quotient is computed afterwards rather than searched for. `W/kg body mass` becomes a
    question for W and a question for kg.

    Recognises a slash, the word `per`, and negative-exponent notation, because `mol m^-2 s^-1`
    is a ratio with no slash in it -- a case the first version of this classifier missed and
    which diluted the measured effect from 8.9-fold to 3.2.
    """
    t = (units or "").strip()
    if not t or _DIMLESS_PHRASE.match(t):
        return None
    if t.lower() in {"body lengths", "body weights", "tail beats", "dimensionless"}:
        return None
    if t.lower().replace(" ", "") in STANDARD_RATIOS:
        return None                    # a quantity papers name in its own right -- see above
    m = re.match(r'^\s*([^/]+?)\s*/\s*(.+?)\s*$', t)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    m = re.match(r'^\s*(.+?)\s+per\s+(.+?)\s*$', t, re.I)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    if re.search(r'\^\s*-|[\u207b]', t):
        return (t, "")            # negative-exponent form: flag it, do not try to split blindly
    return None


def build(keep_dimensionless: bool = False, cap: int = 18,
          source: str = "quantities") -> tuple[str, int, int, int]:
    qs = evidence_gaps() if source == "gaps" else open_quantities()
    # The units filter exists to drop ratios of THIS project's own numbers. A gap sentence is a
    # research question whatever its units are -- "no zebrafish study links a membrane-potential
    # change to fin-ray growth" has no units at all and is still the most searchable item here --
    # so it does not apply to that source.
    kept = [q for q in qs if source == "gaps" or keep_dimensionless or is_physical(q[1])]
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
        # THE DECOMPOSITION INSTRUCTION WAS REMOVED AFTER BEING MEASURED. It asked the
        # extractor to also accept the numerator or denominator on its own, on the reasoning
        # that a paper states parts more often than quotients. Tested over four ratio questions
        # in one harvest: Q5 (W/kg muscle) returned 5 values in the requested factors out of
        # 222; Q6 (S/cm^2) 0 of 306; Q14 (J/kg muscle) 0 of 52; Q16 (m/s) 0 of 52. Asking for
        # the parts did not make the literature yield the parts, so the instruction was clutter
        # in every question that carried it.
        #
        # ratio_unit() SURVIVES AS A PREDICTOR, which is the half that measured true: a
        # ratio-unit question returns a usable value far less often than a non-ratio one
        # (claim 2769), so the flag is worth printing for whoever reads the question list and
        # decides what to spend a harvest on. It no longer tells the extractor what to do.
        split = ratio_unit(units)
        hint = ("\n   [LOW-YIELD: this asks for a RATIO. Ratio-unit questions have returned a "
                "value in the units asked for far less often than other questions in this "
                "project -- see claim 2769. Expect the paper's own units and be prepared to "
                "convert.]" if split else "")
        lines.append(f"{i}. {quantity}.{u}{many}{hint}\n   Report the species and the body "
                     f"length or life stage if the paper states them.")
    return "\n".join(lines), len(kept[:cap]), dropped, collapsed


GENERALISE = """These are quantities a research project currently cannot answer. Each was written
for that project's own argument, so many are phrased as ITS arithmetic rather than as something a
published paper would ever state.

Rewrite each one as a QUANTITY that the METHODS or RESULTS section of a real paper could state,
and drop the ones no paper could.

PHRASE EACH AS A NOUN PHRASE NAMING A MEASURABLE QUANTITY, never as a yes/no or a relationship
question. The downstream step extracts NUMBERS WITH UNITS from paper text; a question it cannot
answer with a number returns nothing however relevant the paper is. Measured 2026-11-05: gap
sentences rewritten as "Does membrane-potential change in fin cells correlate with fin-ray growth
rate?" and "What is the spatial relationship between Lat4a- and Kcnh2a-expressing cells?"
returned ZERO values from roughly 80 on-topic papers, because neither has a single number as its
answer.

    NOT  "Does membrane-potential change correlate with fin-ray growth rate?"
    YES  "Fin-ray outgrowth rate in regenerating fins under depolarising or hyperpolarising
          treatment, in um/day"
    NOT  "What is the spatial relationship between Lat4a- and Kcnh2a-expressing cells?"
    YES  "Distance between the two expression domains in a regenerating fin ray, in um"

A relationship an underlying paper reports is still reachable: name the MEASURED QUANTITY on each
side, and let the extractor return both.

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

Widen the organism, but INFER WHAT IT IS FROM THE QUANTITIES THEMSELVES -- the list below is the
only thing that tells you what this project studies. A value from a related organism, or from
another system where the physiology carries over, is wanted; say so in the question.

NEVER NAME AN ORGANISM THE QUANTITIES DO NOT IMPLY. Measured 2026-11-05: this instruction
previously read "this project works on zebrafish", and for the insect-flight project it turned
the quantity `lift-to-weight ratio of the four-wing configuration` into "Lift force produced by
flying fish or gliding fish during aerial locomotion". A four-wing configuration is an insect.
The question was well-formed, searchable, and about the wrong animal, and it would have harvested
fish papers into an insect project.

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
    from api_challenge import call_first_live
    r = call_first_live(tenant_list, GENERALISE.format(items=numbered), max_tokens=4000,
                        model=model)
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
    source = "gaps" if "--from-gaps" in sys.argv else "quantities"
    cap = 18
    if "--cap" in sys.argv:
        cap = int(sys.argv[sys.argv.index("--cap") + 1])
    qs_for_control = evidence_gaps() if source == "gaps" else open_quantities()
    text, n, dropped, collapsed = build(keep, cap, source)

    gen_note, gen_map = "", {}
    if "--generalise" in sys.argv:
        from api_challenge import TENANTS, call      # api_allen excluded in exactly one place
        items = ([(q, u, c) for q, u, c in evidence_gaps()][:40] if source == "gaps"
                 else [(q, u, c) for q, u, c in open_quantities() if keep or is_physical(u)][:40])
        qs, err = generalise(items, TENANTS, call, MODEL)
        if qs is None:
            print(f"  generalisation FAILED ({err}); keeping the verbatim quantities")
        else:
            kept_q = [q for q in qs if q.get("keep") and q.get("question")]
            # TWO-SIDED CONTROL on the generalisation, not just on the filter. A step that
            # keeps everything and a step that drops everything both "work" on one example.
            joined = " ".join(str(q.get("question", "")).lower() for q in kept_q)
            dropped_n = {q.get("n") for q in qs if not q.get("keep")}
            # Project-agnostic, for the same reason as the final control below: the previous
            # test was `"muscle" in joined and ("mass" in joined or "power" in joined)`, which
            # is zebrafish-flight vocabulary. Coral has no muscle, so the generalisation control
            # failed for it and the module silently fell back to the verbatim quantities -- a
            # degraded result that announces itself only as one line of output. Same bug as the
            # final control, in a second place, and fixing one did not fix the other.
            src_w: set = set()
            for quantity, _u, _c in items:
                src_w |= words(quantity)
            must_keep = bool(src_w & words(joined))
            must_drop = source == "gaps" or any("available minus required" in items[n - 1][0].lower()
                            for n in dropped_n if isinstance(n, int) and 1 <= n <= len(items))
            # A yes/no or relationship phrasing returns nothing from a numeric extractor
            # however relevant the paper is, and it is invisible in the output -- it looks
            # exactly like a question the literature has not answered.
            YESNO = ("does ", "do ", "is ", "are ", "can ", "has ", "have ", "whether ",
                     "what is the relationship", "what is the spatial relationship")
            yesno = [q["question"] for q in kept_q
                     if str(q["question"]).strip().lower().startswith(YESNO)]
            if yesno:
                print(f"  {len(yesno)} question(s) phrased as yes/no or a relationship; a "
                      f"numeric extractor cannot answer these. First: {yesno[0][:70]}")
                kept_q = [q for q in kept_q if q["question"] not in yesno]
            if not (kept_q and must_keep):
                print("  generalisation CONTROL FAILED -- keeping the verbatim quantities")
            else:
                lines, qmap = [], {}
                for i, q in enumerate(kept_q[:cap], 1):
                    u = f" Units wanted: {q['units']}." if q.get("units") else ""
                    lines.append(f"{i}. {q['question']}.{u}\n   Report the species and the body "
                                 f"length or life stage if the paper states them.")
                    # Carry the originating constraint's SCALE through the generalisation.
                    # Without this the question is a good literature question that has forgotten
                    # which scale of the model it was asked for, and every value extracted with
                    # it lands with scale_id NULL -- which is exactly why the project's
                    # measured-with-a-scale row cannot move even when real values arrive.
                    src_n = q.get("n")
                    if source == "gaps":
                        if isinstance(src_n, int) and 1 <= src_n <= len(items):
                            sc = GAP_SCALE.get(items[src_n - 1][0], "")
                            qmap[str(i)] = {"question": q["question"],
                                            "units": q.get("units", ""),
                                            "from_quantity": items[src_n - 1][0][:200],
                                            "scales": [sc] if sc else []}
                    elif isinstance(src_n, int) and 1 <= src_n <= len(items):
                        quantity = items[src_n - 1][0]
                        scales = [r[0] for r in dbq.q(
                            "select distinct target_scale from constraint_entailed where "
                            f"project_id = {dbq.lit(PROJECT)} and status = 'open' and "
                            f"quantity = {dbq.lit(quantity)} and target_scale is not null")]
                        qmap[str(i)] = {"question": q["question"], "units": q.get("units", ""),
                                        "from_quantity": quantity, "scales": sorted(scales)}
                text, n = "\n".join(lines), len(lines)
                gen_map = qmap
                gen_note = (f"  generalised by model: {len(kept_q)} kept, "
                            f"{len(dropped_n)} dropped as project-internal arithmetic "
                            f"[{'ok' if must_drop else 'WEAK'}] control: dropped a known "
                            f"internal difference = {must_drop}")

    # TWO-SIDED CONTROL. A generator that emits nothing and a generator pointed at an empty
    # database print the same thing, and a filter that drops everything looks like a strict one.
    # THE CONTROL MUST NOT NAME THIS PROJECT'S SUBJECT MATTER. The previous version asserted
    # that the output mentioned "water-exit speed", "tail-beat frequency" or "muscle", and that
    # it did NOT mention "frame interval". Both are zebrafish-flight vocabulary, so the module
    # reported FAIL for every other project in the database -- and because --out returns 2 on a
    # failed control, it could not be run for coral, insect-flight, limbless-mouse or xenobot at
    # all. Measured 2026-11-05: coral and insect-flight each produce six sensible questions
    # ("generation time, years"; "sensory feedback latency, ms") and each reported FAIL.
    #
    # What the control is actually for is that the output DERIVES FROM THE INPUT rather than
    # from the model's priors, and that is testable without knowing the subject: the generated
    # questions must share content words with the quantities they were generated from.
    low = text.lower()
    src_words: set[str] = set()
    for quantity, _u, _c in qs_for_control:
        src_words |= words(quantity)
    out_words = words(low)
    shared = src_words & out_words
    must_find = bool(shared)
    # And the units filter must actually have run when there was anything for it to drop.
    must_drop = dropped > 0 or not any(not is_physical(u) for _q, u, _c in qs_for_control)
    ok = n > 0 and (must_find or source == "gaps") and (must_drop or keep or source == "gaps")
    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        if not ok:
            print("CONTROL FAILED -- refusing to write a question list that cannot be trusted")
            print(f"  questions={n} must_find={must_find} must_drop={must_drop}")
            return 2
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {path}")
        if gen_map:
            import json as _json
            mpath = path + ".map.json"
            with open(mpath, "w", encoding="utf-8") as fh:
                _json.dump(gen_map, fh, indent=1)
            one = sum(1 for v in gen_map.values() if len(v["scales"]) == 1)
            print(f"wrote {mpath}: {len(gen_map)} question(s), {one} with exactly ONE scale "
                  f"(the rest stay NULL rather than being guessed)")
    if gen_note:
        print(gen_note)
    print(f"  {n} question(s) from OPEN constraints; {dropped} dropped as dimensionless "
          f"(ours, not a paper's), {collapsed} collapsed as restatements of another")
    print(f"  [{'ok' if ok else 'FAIL'}] control: output shares {len(shared)} content word(s) "
          f"with the quantities it was generated from, so it derives from this project's own "
          f"constraints and not from the model's priors; units filter ran ({dropped} dropped)")
    print()
    print(text)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
