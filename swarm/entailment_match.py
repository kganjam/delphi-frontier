#!/usr/bin/env python3
"""Match OPEN range-entailments against measured claims, and say which way each one falls.

WHY THIS IS NOT THE SAME WORK AS THE 130 ALREADY CLOSED. Those were closed by a person or an
agent writing prose into `satisfied_by` with an evidence label -- mostly `existence` rows, mostly
with no `quantity` at all. This targets the other population: open rows that carry a QUANTITY,
UNITS and a numeric bound, where the claim graph may already hold a value that settles them. 136
of 151 open rows have a quantity and 135 have units, so the population is real.

THE DANGER IS MANUFACTURING CLOSURES, which is forbidden outright (a score computed from
anything but the thing being scored). Two things keep this honest:

  1. UNITS MUST MATCH EXACTLY after normalisation. Not "be similar" -- equal. A quantity in mm
     cannot be settled by a number in m/s however well the words line up, and word overlap alone
     is exactly how a matcher invents agreement.
  2. A SHUFFLED NULL RUNS EVERY TIME, not on request. Each entailment is re-paired with a random
     other entailment's quantity text, keeping its units, and the matcher is re-run. If the
     shuffled run finds matches at anything like the real rate, the matcher is matching units
     and noise rather than meaning, and this module says so and refuses to write.

WHAT IT DOES NOT DO. It does not set status='satisfied' on its own judgement. It proposes, with
the claim id and the value, and --write records only rows where a value sits inside the stated
bound with units equal and at least one distinctive token shared. A row whose value falls OUTSIDE
the bound is reported as a CANDIDATE VIOLATION and never written: a constraint the record
violates is a finding that deserves a person, not an automatic status flip.
"""

from __future__ import annotations

import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from dbq import q, lit  # noqa: E402

PROJECT = "zebrafish-flight"
STOP = {"the", "a", "of", "in", "at", "to", "for", "and", "or", "per", "by", "its", "that",
        "must", "be", "is", "are", "with", "from", "on", "it", "this", "an", "as"}
#: a shuffled run may not exceed this fraction of the real run's match count
NULL_CEILING = 0.34


def norm_unit(u: str) -> str:
    """Leading unit token, normalised. Claim units are prose that STARTS with the unit."""
    if not u:
        return ""
    head = u.strip().split(",")[0].split(" ")[0].strip().rstrip(";:")
    head = head.replace("^", "").replace(" ", "").lower()
    head = {"ms": "m/s", "w/kgmuscle": "w/kg", "percent": "%", "hz": "hz"}.get(head, head)
    return head


def toks(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in STOP and len(w) > 2}


def load():
    ents = q(f"""select id, coalesce(quantity,''), coalesce(units,''),
                 coalesce(lo::text,''), coalesce(hi::text,''),
                 replace(coalesce(statement,''), chr(10), ' '), coalesce(source_claim::text,'')
                 from constraint_entailed
                 where project_id = {lit(PROJECT)} and status = 'open'
                   and quantity is not null and units is not null
                   and (lo is not null or hi is not null)""")
    claims = q(f"""select id, value_num::text, replace(coalesce(units,''), chr(10), ' '),
                   replace(left(coalesce(statement,''),300), chr(10), ' '), coalesce(evidence,'')
                   from claim
                   where project_id = {lit(PROJECT)} and superseded_by is null
                     and value_num is not null and units is not null
                     and evidence in ('measured','literature','derived')""")
    return ents, claims


REJECTS: list[tuple] = []
TIMEWORDS = {"latency", "duration", "time", "fwhm", "onset", "interval", "period"}
DF: dict[str, int] = {}
RARE_DF = 12          #: a term in more than this many claims carries no discriminating power


def build_df(claims) -> None:
    DF.clear()
    for _cid, _v, cunits, cstmt, _ev in claims:
        for t in toks(cunits) | toks(cstmt):
            DF[t] = DF.get(t, 0) + 1


def match(ents, claims, shuffle_quantities=False):
    qtexts = [e[1] for e in ents]
    if shuffle_quantities:
        rng = random.Random(20261105)
        qtexts = qtexts[:]
        rng.shuffle(qtexts)
    out = []
    for e in range(len(ents)):
        eid, _qty, eunits, lo, hi, estmt, esrc = ents[e]
        qty = qtexts[e]
        eu = norm_unit(eunits)
        if not eu:
            continue
        want = toks(qty)
        best = None
        for cid, val, cunits, cstmt, ev in claims:
            if norm_unit(cunits) != eu:
                continue
            shared = want & (toks(cunits) | toks(cstmt))
            # RARE TERMS ONLY, AND AT LEAST TWO. The first version took any single shared token
            # and its shuffled null ran at 65% of the real rate -- it was matching "measured",
            # "body", "fin" and the units. Weighting by inverse document frequency and demanding
            # two distinctive terms is the difference between agreeing about a QUANTITY and
            # agreeing about vocabulary.
            rare = {t for t in shared if DF.get(t, 0) <= RARE_DF}
            if len(rare) < 2:
                continue
            score = sum(1.0 / (1 + DF.get(t, 0)) for t in rare)
            if best is None or score > best[4]:
                best = (cid, float(val), rare, ev, score)
        if best:
            cid, val, shared, ev, _score = best
            lof = float(lo) if lo else None
            hif = float(hi) if hi else None
            # CIRCULARITY. An entailment whose bound IS the claim's value was derived from that
            # claim, so satisfying it with the same claim proves nothing. Measured: e268 and e301
            # both carry lo = 142.7 and were matched by claim 309 = 142.7.
            if str(cid) == esrc:
                REJECTS.append((eid, cid, "closed by its own source claim"))
                continue
            if (lof is not None and val == lof) or (hif is not None and val == hif):
                REJECTS.append((eid, cid, f"bound equals the claim's value ({val:g}) exactly"))
                continue
            # A QUANTITY THAT IS A TIME CANNOT BE IN m/s. The entailment's own units are wrong
            # in these rows, and a wrong unit that happens to match is worse than no match.
            if TIMEWORDS & toks(qty) and eu not in ("s", "ms", "us", "min", "h"):
                REJECTS.append((eid, cid, f"quantity reads as a time but units are {eu!r}"))
                continue
            inside = (lof is None or val >= lof) and (hif is None or val <= hif)
            out.append((eid, qty, eu, lof, hif, cid, val, sorted(shared), ev, inside, estmt))
    return out


def main() -> int:
    write = "--write" in sys.argv
    ents, claims = load()
    print(f"  {len(ents)} open entailments with quantity+units+bound; "
          f"{len(claims)} live valued claims to match against\n")

    build_df(claims)
    REJECTS.clear()
    real = match(ents, claims)
    rejects = list(REJECTS)
    null = match(ents, claims, shuffle_quantities=True)
    ratio = len(null) / len(real) if real else 1.0
    print(f"  CONTROL, shuffled quantities: {len(null)} matches against {len(real)} real "
          f"= {ratio:.0%} of the real rate (ceiling {NULL_CEILING:.0%})")
    if ratio > NULL_CEILING:
        print("  REFUSING TO WRITE -- the shuffled null matches nearly as often as the real "
              "run, so these matches are driven by units and common words, not by meaning.")
    print()

    sat = [r for r in real if r[9]]
    vio = [r for r in real if not r[9]]
    print(f"  {len(sat)} candidate SATISFIED, {len(vio)} candidate VIOLATION, "
          f"{len(rejects)} REJECTED by the guards\n")
    if rejects:
        print("  --- REJECTED (a match the guards refused) ---")
        for eid, cid, why in rejects[:10]:
            print(f"   e{eid:<4} claim {cid}: {why}")
        print()
    for lbl, rows in (("CANDIDATE SATISFIED", sat), ("CANDIDATE VIOLATION", vio)):
        print(f"  --- {lbl} ---")
        for eid, qty, eu, lo, hi, cid, val, shared, ev, _ins, estmt in rows[:14]:
            b = f"[{lo if lo is not None else '-'}, {hi if hi is not None else '-'}]"
            print(f"   e{eid:<4} {qty[:34]:34s} {eu:9s} {b:16s} claim {cid} = {val:g} "
                  f"({ev}) via {','.join(shared[:3])}")
        if len(rows) > 14:
            print(f"   ... and {len(rows)-14} more")
        print()

    if not write:
        print("  NOT written. A candidate is a proposal; re-run with --write to record the "
              "satisfied ones, which never includes a violation.")
        return 0
    if ratio > NULL_CEILING:
        print("  --write ignored: the null control failed above.")
        return 1
    n = 0
    for eid, qty, eu, lo, hi, cid, val, shared, ev, _ins, _st in sat:
        why = (f"claim {cid} gives {val:g} {eu}, inside "
               f"[{lo if lo is not None else '-'}, {hi if hi is not None else '-'}]; matched on "
               f"units equality and shared terms {','.join(shared[:4])}; "
               f"proposed by entailment_match.py, shuffled-null control at {ratio:.0%}")
        q(f"update constraint_entailed set status='satisfied', satisfied_by={lit(why)}, "
          f"satisfied_evidence={lit(ev)} where id={eid} and status='open'")
        n += 1
    print(f"  recorded {n} entailment(s) as satisfied, each citing the claim and the value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
