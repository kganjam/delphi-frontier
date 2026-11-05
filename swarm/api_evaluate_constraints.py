#!/usr/bin/env python3
"""Decide whether an OPEN cross-scale constraint is met by the evidence this project holds.

THE PIPELINE GAP THIS FILLS, measured 2026-11-05. zebrafish-flight has 230 of its 381
constraints evaluated -- 130 satisfied, 92 unsatisfied, 7 unsatisfiable, 1 assumed -- accumulated
over months of agent work. coral, insect-flight, limbless-mouse and xenobot have 52 constraints
between them and ZERO evaluated: every one is `open`. That is why swarm/api_design_refine.py,
run on coral, correctly answers "no blockers recorded; nothing to refine against" -- a design
cannot be refined against constraints nobody has judged.

WHY A MODEL AND NOT A MATCHER. swarm/entailment_candidates.py tries to close these mechanically
by matching a constraint's bound to a claim's value. Its own shuffled-quantity null control
refuses to let it write (claim 1131): units agreeing is not quantities agreeing, and five
hand-worked candidates failed in five distinct ways no numeric filter catches -- a bound derived
from the very claim offered to close it, a regime mismatch the bound does not carry, a candidate
that is the REQUIREMENT rather than the capability. Those are reading tasks.

THE GUARD THAT MATTERS, and it is the whole design: THREE OUTCOMES, NOT TWO.

    satisfied     the evidence meets the constraint -- REQUIRES a cited claim id, and the id
                  must exist in this project, or the verdict is discarded
    unsatisfied   the evidence bears on the constraint and does NOT meet it
    insufficient  nobody has looked, or what exists does not bear on it -- the constraint STAYS
                  OPEN and nothing is written

Without the third outcome every constraint gets a verdict, and a corpus where everything is
decided is a corpus where nothing was checked. `insufficient` must be the easy answer, so the
prompt says so and the parser treats a missing or unparseable verdict as insufficient rather
than guessing.

A `satisfied` VERDICT IS VERIFIED BEFORE IT IS WRITTEN. The cited claim id is looked up; if it
does not exist, is superseded, or belongs to another project, the verdict is dropped and the drop
is printed. A model that invents a plausible claim number is the obvious failure mode here, and
it is cheap to make impossible rather than unlikely.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import api_challenge as ac  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

PROMPT = """You are judging whether a design constraint is met by the evidence a project holds.

THE CONSTRAINT ({eid}):
  {statement}
  quantity: {quantity}   bound: [{lo}, {hi}] {units}
  scales: {ss} -> {ts}

THE EVIDENCE THIS PROJECT HOLDS (claim id, evidence level, value, statement):
{claims}

Decide ONE of three verdicts. Reply in EXACTLY this form:

VERDICT: <satisfied|unsatisfied|insufficient>
CLAIM: <the id of the claim that settles it, or "none">
WHY: <two sentences at most, naming the quantity and the comparison>

RULES:
- `satisfied` REQUIRES a real claim id from the list above whose value or statement meets the
  constraint. No id, no satisfied.
- `unsatisfied` means evidence above BEARS on the constraint and fails it. Cite the claim.
- `insufficient` is the RIGHT answer whenever nobody has measured the quantity, or when the
  claims that look relevant are about a different regime, a different species, or the
  REQUIREMENT rather than the capability. It is not a failure to say insufficient; it is the
  honest answer most of the time, and a wrong `satisfied` is far more costly than a missed one.
- Units agreeing is NOT quantities agreeing. A speed in m/s may be a launch speed, a wind speed
  or a swimming speed."""


def _all_claims():
    return ac.q(f"""select id, coalesce(evidence,'-'), coalesce(value_num::text,'-'),
                replace(left(coalesce(units,''),70), chr(10), ' '),
                replace(left(coalesce(statement,''),220), chr(10), ' ')
                from claim where project_id = {ac.lit(PROJECT)} and superseded_by is null""")


def claims_block(constraint_text: str = "", limit=40) -> str:
    """Claims RELEVANT to this constraint, not the 40 most recent.

    THE FIRST VERSION SORTED `(evidence='measured') desc, id desc` AND WAS USELESS. Measured
    2026-11-05: it fed the evaluator forty of this session's own PROCESS claims -- pLDDT scores,
    PDB70 alignment depths, entailment bookkeeping -- and NONE of the biology. Claim 443 (the
    measured 1.57 m/s escape speed), claim 309 (142.7 W/kg), claim 21, claim 1 and claim 2 were
    all absent. Every verdict came back `insufficient`, correctly about the context supplied and
    uselessly about the project, and the giveaway was a verdict saying no claim reports a
    measured water-exit speed when claim 443 is exactly that.

    Two causes, both mine: recency is not relevance, and I have been labelling measurements OF
    THIS PROJECT'S OWN PROCESS as `measured`, which is defensible per claim and poisons any
    measured-first ordering with non-biology.

    Selection is now by rare-term overlap with the constraint -- the same IDF scheme
    swarm/claim_precedent.py uses, which has its own shuffled-term null control -- with an
    exact-units match counted heavily, since a constraint in m/s is settled by a claim in m/s.
    """
    rows = _all_claims()
    if not constraint_text:
        return "\n".join(f"  {r[0]} [{r[1]}] {r[2]} {r[3]} :: {r[4]}" for r in rows[:limit])
    import re as _re
    STOP = {"the","a","of","in","at","to","for","and","or","per","by","its","that","must","be",
            "is","are","with","from","on","it","this","an","as","not","than","which"}
    def tok(t):
        return {w for w in _re.findall(r"[a-z0-9]+", (t or "").lower())
                if w not in STOP and len(w) > 3}
    df: dict[str, int] = {}
    for r in rows:
        for w in tok(r[3] + " " + r[4]):
            df[w] = df.get(w, 0) + 1
    want = tok(constraint_text)
    # A CONSTRAINT MAY HAVE NO UNITS -- `existence` rows carry none -- and the first version
    # called .split()[0] on the empty remainder and raised IndexError on the SECOND constraint
    # it saw. Guard rather than assume every row is a range.
    tail = constraint_text.split("bound:")[-1].split("]")[-1].strip() if "bound:" in constraint_text else ""
    cunit = tail.split()[0].lower() if tail else ""
    scored = []
    for r in rows:
        shared = want & tok(r[3] + " " + r[4])
        score = sum(1.0 / (1 + df.get(w, 0)) for w in shared)
        if cunit and cunit in (r[3] or "").lower():
            score += 1.0                      # an exact unit match outranks any word overlap
        scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return "\n".join(f"  {r[0]} [{r[1]}] {r[2]} {r[3]} :: {r[4]}"
                      for sc, r in scored[:limit] if sc > 0) or \
           "\n".join(f"  {r[0]} [{r[1]}] {r[2]} {r[3]} :: {r[4]}" for r in rows[:limit])


def open_constraints(limit):
    return ac.q(f"""select id, replace(coalesce(statement,''), chr(10), ' '),
                coalesce(quantity,'-'), coalesce(lo::text,'-'), coalesce(hi::text,'-'),
                coalesce(units,''), coalesce(source_scale,'?'), coalesce(target_scale,'?')
                from constraint_entailed
                where project_id = {ac.lit(PROJECT)} and status = 'open'
                order by id limit {limit}""")


def parse(text: str) -> tuple[str, str, str]:
    def grab(f):
        m = re.search(rf"^{f}:\s*(.+)$", text, re.M)
        return m.group(1).strip() if m else ""
    v = grab("VERDICT").lower().split()[0] if grab("VERDICT") else ""
    if v not in ("satisfied", "unsatisfied", "insufficient"):
        v = "insufficient"          # unparseable is NOT a licence to guess
    return v, grab("CLAIM"), grab("WHY")


def claim_exists(cid: str) -> bool:
    if not cid.isdigit():
        return False
    rows = ac.q(f"select id from claim where id = {cid} and project_id = {ac.lit(PROJECT)} "
                f"and superseded_by is null")
    return bool(rows)


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
    write = "--write" in sys.argv
    pin = sys.argv[sys.argv.index("--tenant") + 1] if "--tenant" in sys.argv else None
    cons = open_constraints(n)
    if not cons:
        print(f"  {PROJECT}: no open constraints.")
        return 0
    if not _all_claims():
        print(f"  {PROJECT}: no live claims to judge against.")
        return 0
    print(f"  {PROJECT}: judging {len(cons)} open constraint(s)\n")

    tally = {"satisfied": 0, "unsatisfied": 0, "insufficient": 0, "dropped": 0}
    spent = 0.0
    for eid, stmt, qty, lo, hi, units, ss, ts in cons:
        claims = claims_block(f"{stmt} {qty} bound: [{lo}, {hi}] {units}")
        r = ac.call_live_with_fallback([pin] if pin else ac.TENANTS, PROMPT.format(
            eid=f"e{eid}", statement=stmt[:400], quantity=qty, lo=lo, hi=hi, units=units,
            ss=ss, ts=ts, claims=claims[:9000]), max_tokens=700)
        spent += float(r.get("cost_usd") or 0)
        v, cid, why = parse(r.get("text", ""))
        if v == "satisfied" and not claim_exists(cid):
            print(f"  e{eid}  DROPPED: verdict `satisfied` cites claim {cid!r}, which is not a "
                  f"live claim in this project")
            tally["dropped"] += 1
            continue
        tally[v] += 1
        print(f"  e{eid}  {v.upper():12s} {('claim ' + cid) if cid and cid != 'none' else '':12s} "
              f"{why[:88]}")
        # A SATISFIED VERDICT MUST SURVIVE A SECOND, INDEPENDENT RUN. Measured 2026-11-05: on
        # consecutive runs of the identical six constraints, e11 came back `satisfied` citing
        # claim 443 (a measured 1.57 m/s escape speed) and then `insufficient`, on the ground
        # that "no claim measures the actual water-exit (launch) speed" -- an escape speed in
        # water is not a launch speed, and the SECOND verdict is the better one. e5's stated
        # reasoning also reversed between runs on whether a measured decay length fell inside
        # its bound. One run is a sample, not a verdict; closing a constraint on a sample is how
        # a corpus fills with closures nobody checked. Confirmation costs one extra call and is
        # only spent on the verdicts that would WRITE.
        if write and v == "satisfied":
            r2 = ac.call_live_with_fallback([pin] if pin else ac.TENANTS, PROMPT.format(
                eid=f"e{eid}", statement=stmt[:400], quantity=qty, lo=lo, hi=hi, units=units,
                ss=ss, ts=ts, claims=claims[:9000]), max_tokens=700)
            spent += float(r2.get("cost_usd") or 0)
            v2, cid2, _why2 = parse(r2.get("text", ""))
            if v2 != "satisfied" or cid2 != cid:
                print(f"         NOT WRITTEN: a second run said {v2!r} citing {cid2!r}; "
                      f"a satisfied verdict must be reproducible")
                tally["satisfied"] -= 1
                tally["unstable"] = tally.get("unstable", 0) + 1
                continue
        if write and v == "insufficient":
            # PERSIST THE GAP. An insufficient verdict is the most actionable thing this module
            # produces: it names, in one sentence, the evidence a constraint is waiting on. Until
            # now it was printed and discarded, so every run paid a call to recompute a sentence
            # nothing had kept -- the same dead end as an extraction pipeline writing to a file
            # no reader opens. Stored here, it becomes the input to the next literature search,
            # which is what closes the loop from evaluation back to retrieval.
            ac.q(f"""update constraint_entailed set missing_evidence = {ac.lit(why[:900])},
                 missing_evidence_at = now() where id = {eid} and status = 'open'""")
        if write and v in ("satisfied", "unsatisfied"):
            ev = ac.q(f"select coalesce(evidence,'literature') from claim where id = {cid}")
            note = (f"{why[:600]} [evaluated by api_evaluate_constraints.py against claim {cid}]")
            ac.q(f"""update constraint_entailed set status = {ac.lit(v)},
                 satisfied_by = {ac.lit(note)},
                 satisfied_evidence = {ac.lit(ev[0][0] if ev else 'literature')}
                 where id = {eid} and status = 'open'""")
    print(f"\n  {tally['satisfied']} satisfied, {tally['unsatisfied']} unsatisfied, "
          f"{tally['insufficient']} insufficient (left open), {tally['dropped']} dropped for a "
          f"bad citation, {tally.get('unstable', 0)} dropped as IRREPRODUCIBLE.  ${spent:.4f}")
    if not write:
        print("  NOT written. Re-run with --write to record the verdicts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
