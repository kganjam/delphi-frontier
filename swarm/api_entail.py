#!/usr/bin/env python3
"""Propose CROSS-SCALE CONSTRAINTS for a project that has claims but no constraint layer.

THE GAP THIS FILLS, measured 2026-11-05. zebrafish-flight holds 381 entailments across 8 scales.
coral, insect-flight, limbless-mouse and xenobot hold ZERO -- between them 349 live claims, 2393
adversarial challenges, and not one cross-scale constraint. They replicated the claim layer and
the adversarial layer and not the layer that makes a project cross-scale rather than a list. The
pipeline was always parameterised (`harvest.py` reads SWARM_PROJECT); it is just that nothing has
ever emitted `swarm-entail` blocks for those projects, because entailments were only ever a
by-product of agent branch work on the fish.

WHAT AN ENTAILMENT IS, since generating the wrong thing here would be fabrication. It is a
CONSTRAINT that must hold if the design is to work -- "the gradient decay length must be
comparable to the structure it patterns" -- not a measurement and not a finding. Proposing one is
design reasoning, and it lands with status `open`, meaning nobody has yet shown it holds. That is
a legitimate and honest artifact: 151 of the fish's own 381 are `open`. What would be fabrication
is landing one as `satisfied`, and this module cannot do that -- the status is hardcoded.

IT SHIPS WITH THE GUARDS THE MATCHER TAUGHT ME, because the fish's own entailment set has three
defects that a generator should not reproduce (claim 1131):

  CIRCULARITY   8 of the fish's rows have a bound EQUAL to their own source claim's value_num, so
                the constraint is satisfied by the premise it was read off. Refused here.
  DUPLICATES    54 of 381 rows are redundant. harvest.py does de-duplicate, but on
                (source_claim, statement) -- and the duplicates have the same bounds with
                DIFFERENT wording, so that key cannot see them. This keys on
                (quantity, lo, hi, units, source_claim), which is what actually found them.
  UNIT ERRORS   two rows declare a latency and an FWHM in m/s. A quantity that reads as a time
                must carry a time unit.

A proposal that trips any guard is printed with the reason and dropped. The reasons are worth
more than the rows: a generator whose rejects are invisible is a generator nobody can audit.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import api_challenge as ac  # noqa: E402
from dbq import q, lit  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
SCALES = ("dna", "protein", "cell", "tissue", "organ", "organism", "behaviour", "ecology")
KINDS = ("range", "existence", "timescale", "spatial", "energetic", "conservation")
TIMEWORDS = {"latency", "duration", "time", "fwhm", "onset", "interval", "period", "half-life"}
#: YEARS AND DAYS BELONG HERE and the first version omitted them, so the guard rejected a
#: correct coral constraint ("the generation time of selective breeding ... units: years") as a
#: unit error. A guard that only ever fires on real errors is untested; this one was caught by
#: reading its first rejection rather than counting them. Biological timescales span ns to
#: centuries, so a time-unit allow-list that stops at hours is an organism-scale blind spot.
TIMEUNITS = {"s", "sec", "secs", "second", "seconds", "ms", "us", "ns", "ps", "min", "mins",
             "minute", "minutes", "h", "hr", "hrs", "hour", "hours", "d", "day", "days",
             "wk", "week", "weeks", "mo", "month", "months", "y", "yr", "yrs", "year",
             "years", "generation", "generations"}

PROMPT = """You are a design engineer for this project. Your job is to state CROSS-SCALE
CONSTRAINTS that must hold for the design to work.

PROJECT: {title}
GOAL: {goal}

CLAIMS THIS PROJECT HOLDS (id, scale, statement):
{claims}

A cross-scale constraint links one biological scale to a DIFFERENT one, and says what must be
true for the design to work. It is NOT a restatement of a claim and NOT a finding. Examples of
the form, from another project:
  "A conductance/leak balance must HOLD the gradient against dissipation, not merely create it"
      source_scale dna, target_scale cell, kind range, quantity "membrane conductance", units S/cm^2
  "The gradient decay length must be comparable to the structure it patterns"
      source_scale dna, target_scale tissue, kind spatial, quantity "decay length", lo 0.1, hi 120, units mm

RULES, all of them hard:
- source_scale and target_scale must DIFFER and both come from: {scales}
- kind must be one of: {kinds}
- source_claim must be the id of a real claim above that the constraint follows from
- If you give lo/hi, they must NOT simply repeat the source claim's own measured value. A
  constraint whose bound is read off its own premise proves nothing.
- If the quantity is a time (latency, duration, period, FWHM), its units must be a time unit.
- Omit lo/hi entirely rather than inventing a bound you cannot justify. `existence` constraints
  usually have no bound at all, and that is fine.

Return ONLY a JSON array, up to {n} objects, each with keys:
  source_claim, source_scale, target_scale, kind, statement, quantity, lo, hi, units, note
Use null for anything you cannot justify. No prose outside the JSON."""


def brief():
    rows = q(f"select coalesce(title,''), coalesce(goal,'') from project "
             f"where id = {lit(PROJECT)}")
    return (rows[0][0], rows[0][1]) if rows else (PROJECT, "")


def context(limit=70):
    rows = q(f"""select id, coalesce(scale_id,'?'),
              replace(left(coalesce(statement,''),190), chr(10), ' ')
              from claim where project_id = {lit(PROJECT)} and superseded_by is null
                and scale_id is not null order by id desc limit {limit}""")
    return "\n".join(f"  {r[0]} [{r[1]}] {r[2]}" for r in rows), {r[0] for r in rows}


def existing_keys() -> set[tuple]:
    rows = q(f"""select coalesce(quantity,''), coalesce(lo::text,''), coalesce(hi::text,''),
              coalesce(units,''), coalesce(source_claim::text,'')
              from constraint_entailed where project_id = {lit(PROJECT)}""")
    return {tuple(r) for r in rows}


def claim_value(cid: str) -> float | None:
    rows = q(f"select value_num::text from claim where id = {cid} and value_num is not null")
    return float(rows[0][0]) if rows and rows[0][0] else None


def parse(text: str) -> list[dict]:
    """Salvage complete objects from a possibly TRUNCATED JSON array.

    The first version matched the whole array with a greedy regex and returned nothing when the
    reply hit the token ceiling, because a truncated array has no closing bracket. Measured: a
    run that produced eight well-formed proposals parsed as ZERO, and the failure looked exactly
    like a model that had refused. Scanning balanced objects means a cut-off final object is the
    only thing lost.
    """
    out, depth, start, instr, esc = [], 0, None, False, False
    for i, ch in enumerate(text):
        if instr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                instr = False
            continue
        if ch == '"':
            instr = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    g = json.loads(text[start:i + 1])
                    if isinstance(g, dict):
                        out.append(g)
                except json.JSONDecodeError:
                    pass
                start = None
    return out


def vet(c: dict, valid_ids: set[str], seen: set[tuple]) -> tuple[bool, str, tuple]:
    src = str(c.get("source_claim") or "").strip()
    ss, ts = str(c.get("source_scale") or ""), str(c.get("target_scale") or "")
    kind = str(c.get("kind") or "")
    stmt = str(c.get("statement") or "").strip()
    qty = (str(c.get("quantity")) if c.get("quantity") else "") or ""
    units = (str(c.get("units")) if c.get("units") else "") or ""

    def f(x):
        try:
            return None if x is None else float(x)
        except (TypeError, ValueError):
            return None
    lo, hi = f(c.get("lo")), f(c.get("hi"))
    key = (qty[:200], "" if lo is None else repr(lo), "" if hi is None else repr(hi),
           units[:60], src)

    if not stmt:
        return False, "no statement", key
    if src not in valid_ids:
        return False, f"source_claim {src!r} is not a live scaled claim in this project", key
    if ss not in SCALES or ts not in SCALES:
        return False, f"scale outside the vocabulary ({ss!r} -> {ts!r})", key
    if ss == ts:
        return False, f"not cross-scale: {ss} -> {ts}", key
    if kind not in KINDS:
        return False, f"kind {kind!r} outside the vocabulary", key
    sv = claim_value(src)
    if sv is not None and ((lo is not None and lo == sv) or (hi is not None and hi == sv)):
        return False, f"CIRCULAR: bound equals source claim {src}'s own value ({sv:g})", key
    low = qty.lower()
    if any(w in low for w in TIMEWORDS):
        u = units.strip().lower().split()[0] if units.strip() else ""
        if u not in TIMEUNITS:
            return False, f"quantity reads as a time but units are {units!r}", key
    if key in seen:
        return False, "DUPLICATE of a constraint already held (quantity+bounds+units+source)", key
    return True, "", key


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8
    write = "--write" in sys.argv
    pin = sys.argv[sys.argv.index("--tenant") + 1] if "--tenant" in sys.argv else None
    title, goal = brief()
    ctx, valid_ids = context()
    valid_ids = {str(i) for i in valid_ids}
    if not valid_ids:
        print(f"  project {PROJECT} has no scaled claims to build constraints from.")
        return 0
    seen = existing_keys()
    print(f"  project {PROJECT}: {len(valid_ids)} scaled claims, "
          f"{len(seen)} constraints already held\n")

    t = pin or ac.TENANTS[0]
    r = ac.call_with_fallback(t, PROMPT.format(
        title=title[:120], goal=goal[:600], claims=ctx[:12000],
        scales=", ".join(SCALES), kinds=", ".join(KINDS), n=n), max_tokens=4000)
    spent = float(r.get("cost_usd") or 0)
    cands = parse(r.get("text", ""))
    print(f"  {len(cands)} proposal(s) returned, ${spent:.4f}\n")

    good, bad = [], []
    for c in cands:
        ok, why, key = vet(c, valid_ids, seen)
        (good if ok else bad).append((c, why, key))
        if ok:
            seen.add(key)
    for c, why, _k in bad:
        print(f"  REJECTED  {why}")
        print(f"            {str(c.get('statement'))[:88]}")
    if bad:
        print()
    for c, _w, _k in good:
        print(f"  [{c['source_scale']}->{c['target_scale']}] {c['kind']}  "
              f"(from claim {c['source_claim']})")
        print(f"     {str(c['statement'])[:100]}")
        if c.get("quantity"):
            print(f"     quantity {c['quantity']}  [{c.get('lo')}, {c.get('hi')}] "
                  f"{c.get('units') or ''}")
    print(f"\n  {len(good)} accepted, {len(bad)} rejected.")

    if not write:
        print("  NOT written. Re-run with --write to record them as `open` constraints.")
        return 0

    def num(x):
        return "null" if x is None else repr(float(x))
    for c, _w, _k in good:
        q(f"""insert into constraint_entailed (project_id, source_claim, source_scale,
              target_scale, kind, statement, quantity, lo, hi, units, status, note)
              values ({lit(PROJECT)}, {int(c['source_claim'])}, {lit(c['source_scale'])},
              {lit(c['target_scale'])}, {lit(c['kind'])}, {lit(str(c['statement'])[:900])},
              {lit(str(c['quantity'])[:200]) if c.get('quantity') else 'null'},
              {num(c.get('lo'))}, {num(c.get('hi'))},
              {lit(str(c['units'])[:60]) if c.get('units') else 'null'},
              'open', {lit('proposed by api_entail.py; ' + str(c.get('note') or '')[:600])})""")
    print(f"  wrote {len(good)} constraint(s) at status `open`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
