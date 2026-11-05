#!/usr/bin/env python3
"""Which OPEN cross-scale entailments could be closed with evidence this project already holds?

MERGED 2026-11-05 from two modules that were written for the same job, `entailment_candidates.py`
and `entailment_match.py`, the second by an author who did not check whether the first existed.
Neither was a superset. What each contributed is recorded at the bottom of this docstring so the
choice can be disagreed with.

THIS PROPOSES, IT DOES NOT SATISFY. Matching an entailment's quantity to a claim's value is a
judgement about whether two things are the SAME quantity, and units agreeing is weak evidence for
that -- m/s is m/s whether it is a launch speed or a wind speed. Auto-satisfying on a unit match
would manufacture a satisfied chain, which is the failure this project is organised against.

THE NULL CONTROL DECIDES WHETHER ANYTHING MAY BE WRITTEN, and it runs on every invocation rather
than on request. Each entailment is re-paired with another entailment's quantity TEXT, keeping its
own units, and the matcher re-runs. If shuffled nonsense matches nearly as often as the real
pairing, the matcher is keying on units and common words rather than on meaning. Measured:

    any shared token          30 shuffled / 46 real = 65%   (ceiling 34%)  refuses
    IDF-weighted, 2 rare       5 shuffled / 18 real = 28%                  permits
    plus the guards below      5 shuffled / 11 real = 45%                  refuses

So on zebrafish-flight today NOTHING is written, and that is the module working.

FIVE FAILURE MODES, worked by hand over five candidates of which ALL FIVE failed (claim 1094).
Three are now guarded; two cannot be, and that is why this never writes without the control:

    circular -- the bound was DERIVED from the candidate             (e88)   guarded
    same units, unrelated physics                                    (e281)  guarded by units sanity
    bound equals the candidate's value exactly                       (e268)  guarded
    conditions the bound does not carry -- regime mismatch           (e180)  NOT guardable
    WRONG SIDE: the candidate is the REQUIREMENT, not the capability (e123)  NOT guardable
    the candidate's OWN TEXT forbids the use                         (e54)   NOT guardable

e54 is the one to remember: claim 238 exists specifically to say its 2.5 g is a DIFFERENT quantity
and must not be conflated -- and the tool proposed exactly that conflation. A corpus that records
its own refusals will have them offered back by any naive matcher, and no numeric filter can read
"do not use X for Y".

e180 is the subtler one and it is worth stating in full, because it is the reason a passing null
control still would not be enough on its own: it requires pectoral muscle to deliver net CYCLIC
power >= 50 W/kg, and claim 309 measures 142.7 W/kg -- non-circular, right units, three times the
bound. Still not a satisfaction. The measurement is Scorpaena notata MYOTOMAL fibres at 20 C under
FAST-START strain, not pectoral muscle cycling at flapping frequency, and power trades off against
frequency in muscle. A power figure without its frequency is not comparable to a cyclic-power
requirement.

WHAT THE MERGE TOOK FROM EACH, so nothing is silently dropped:
  from entailment_candidates.py  project parameterisation via SWARM_PROJECT (the newer module had
                                 hardcoded one project, which is worse for a repo whose goal is to
                                 replicate across projects); the circularity guard that checks
                                 whether the VALUE APPEARS IN THE SOURCE CLAIM'S TEXT, which is
                                 broader than comparing ids; the five-mode taxonomy and both
                                 worked examples above.
  from entailment_match.py       the shuffled-quantity null control and its ceiling; IDF weighting
                                 with a two-rare-term floor; the unit-sanity guard (a quantity
                                 reading as a time cannot be in m/s); reporting candidate
                                 VIOLATIONS separately from candidate satisfactions; the --write
                                 path, inert while the control fails.
  dropped                        the newer module's leading-token-only unit normaliser was kept and
                                 the older three-token one dropped: on claim units, which are prose
                                 beginning with the unit ("W/kg, the highest power output ..."),
                                 the three-token form yields "w/kg the highest" and cannot match a
                                 bare "W/kg". Parenthetical-stripping from the older one was kept.
"""

from __future__ import annotations

import os
import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from dbq import q, lit  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
STOP = {"the", "a", "of", "in", "at", "to", "for", "and", "or", "per", "by", "its", "that",
        "must", "be", "is", "are", "with", "from", "on", "it", "this", "an", "as"}
NULL_CEILING = 0.34   #: a shuffled run may not exceed this fraction of the real run's matches
RARE_DF = 12          #: a term in more than this many claims carries no discriminating power
TIMEWORDS = {"latency", "duration", "time", "fwhm", "onset", "interval", "period"}
#: THE "WRONG SIDE" MODE, promoted from unguardable to partly guardable 2026-11-05. The docstring
#: lists e123 as uncatchable: "the candidate is the REQUIREMENT, not the capability". After the
#: merge the matcher offered e123 again -- entailment "the immersed propulsor MUST SUSTAIN about
#: 52 Hz" matched by claim 84, whose own text reads "REQUIRED tail-beat frequency at 1.95 m/s is
#: 72-83 Hz". Using a requirement to satisfy a capability constraint is the same error as
#: circularity wearing different words. The heuristic is crude and one-directional: it only fires
#: when the entailment demands a capability AND the claim announces itself as a requirement, so a
#: capability claim that happens to use the word "required" in passing is the false positive to
#: watch for. It does not catch the reverse case.
CAPABILITY = {"sustain", "deliver", "produce", "generate", "achieve", "supply", "withstand"}
REQUIREMENT = {"required", "requirement", "requires", "needed", "needs"}

DF: dict[str, int] = {}
REJECTS: list[tuple] = []


def norm_unit(u: str) -> str:
    """Leading unit token, normalised. Claim units are prose that STARTS with the unit."""
    if not u:
        return ""
    u = re.sub(r"\(.*?\)", "", u)                      # drop parentheticals
    head = u.strip().split(",")[0].split(" ")[0].strip().rstrip(";:")
    head = head.replace("^", "").replace(" ", "").lower()
    return {"ms": "m/s", "w/kgmuscle": "w/kg", "percent": "%"}.get(head, head)


def toks(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in STOP and len(w) > 2}


def build_df(claims) -> None:
    DF.clear()
    for _cid, _v, cunits, cstmt, _ev in claims:
        for t in toks(cunits) | toks(cstmt):
            DF[t] = DF.get(t, 0) + 1


def load():
    ents = q(f"""select e.id, coalesce(e.quantity,''), coalesce(e.units,''),
                 coalesce(e.lo::text,''), coalesce(e.hi::text,''),
                 replace(coalesce(e.statement,''), chr(10), ' '),
                 coalesce(e.source_claim::text,''),
                 replace(left(coalesce(c.statement,''),1600), chr(10), ' ')
                 from constraint_entailed e
                 left join claim c on c.id = e.source_claim
                 where e.project_id = {lit(PROJECT)} and e.status = 'open'
                   and e.quantity is not null and e.units is not null
                   and (e.lo is not null or e.hi is not null)""")
    claims = q(f"""select id, value_num::text, replace(coalesce(units,''), chr(10), ' '),
                   replace(left(coalesce(statement,''),300), chr(10), ' '), coalesce(evidence,'')
                   from claim
                   where project_id = {lit(PROJECT)} and superseded_by is null
                     and value_num is not null and units is not null
                     and evidence in ('measured','literature','derived')""")
    return ents, claims


def match(ents, claims, shuffle_quantities=False):
    qtexts = [e[1] for e in ents]
    if shuffle_quantities:
        rng = random.Random(20261105)
        qtexts = qtexts[:]
        rng.shuffle(qtexts)
    out = []
    for i in range(len(ents)):
        eid, _qty, eunits, lo, hi, estmt, esrc, esrctext = ents[i]
        qty = qtexts[i]
        eu = norm_unit(eunits)
        if not eu:
            continue
        want = toks(qty)
        best = None
        for cid, val, cunits, cstmt, ev in claims:
            if norm_unit(cunits) != eu:
                continue
            shared = want & (toks(cunits) | toks(cstmt))
            rare = {t for t in shared if DF.get(t, 0) <= RARE_DF}
            if len(rare) < 2:
                continue
            score = sum(1.0 / (1 + DF.get(t, 0)) for t in rare)
            if best is None or score > best[4]:
                best = (cid, float(val), rare, ev, score)
        if not best:
            continue
        cid, val, shared, ev, _score = best
        lof = float(lo) if lo else None
        hif = float(hi) if hi else None
        if str(cid) == esrc:
            REJECTS.append((eid, cid, "closed by its own source claim"))
            continue
        if f"{val:g}" and f"{val:g}" in (esrctext or ""):
            REJECTS.append((eid, cid, f"the value {val:g} already appears in its source claim"))
            continue
        if (lof is not None and val == lof) or (hif is not None and val == hif):
            REJECTS.append((eid, cid, f"bound equals the claim's value ({val:g}) exactly"))
            continue
        if TIMEWORDS & toks(qty) and eu not in ("s", "ms", "us", "min", "h"):
            REJECTS.append((eid, cid, f"quantity reads as a time but units are {eu!r}"))
            continue
        cstmt_t = next((toks(c[3]) | toks(c[2]) for c in claims if c[0] == cid), set())
        if (CAPABILITY & toks(estmt)) and (REQUIREMENT & cstmt_t):
            REJECTS.append((eid, cid, "WRONG SIDE: the entailment demands a capability and the "
                                      "claim states a requirement"))
            continue
        inside = (lof is None or val >= lof) and (hif is None or val <= hif)
        out.append((eid, qty, eu, lof, hif, cid, val, sorted(shared), ev, inside, estmt))
    return out


def main() -> int:
    write = "--write" in sys.argv
    ents, claims = load()
    print(f"  project {PROJECT}: {len(ents)} open entailments with quantity+units+bound; "
          f"{len(claims)} live valued claims\n")
    if not ents or not claims:
        print("  nothing to match. A project with no entailments has no cross-scale constraints "
              "to close, which is a structural gap rather than an empty result.")
        return 0

    build_df(claims)
    REJECTS.clear()
    real = match(ents, claims)
    rejects = list(REJECTS)
    REJECTS.clear()
    null = match(ents, claims, shuffle_quantities=True)
    ratio = len(null) / len(real) if real else 1.0
    print(f"  CONTROL, shuffled quantities: {len(null)} matches against {len(real)} real "
          f"= {ratio:.0%} of the real rate (ceiling {NULL_CEILING:.0%})")
    blocked = ratio > NULL_CEILING
    if blocked:
        print("  REFUSING TO WRITE -- shuffled nonsense matches nearly as often, so these "
              "matches are driven by units and common words rather than by meaning.")
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
        for eid, qty, eu, lo, hi, cid, val, shared, ev, _ins, _st in rows[:14]:
            b = f"[{lo if lo is not None else '-'}, {hi if hi is not None else '-'}]"
            print(f"   e{eid:<4} {qty[:34]:34s} {eu:9s} {b:16s} claim {cid} = {val:g} "
                  f"({ev}) via {','.join(shared[:3])}")
        if len(rows) > 14:
            print(f"   ... and {len(rows)-14} more")
        print()

    print("  A UNIT MATCH IS NOT A QUANTITY MATCH, and two of the five failure modes in this")
    print("  module's docstring -- regime mismatch, and the candidate being the REQUIREMENT")
    print("  rather than the capability -- cannot be caught by any numeric filter. Every row")
    print("  above needs a person.")
    if not write:
        print("\n  Nothing written. Re-run with --write to record candidate satisfactions, "
              "which never includes a violation.")
        return 0
    if blocked:
        print("\n  --write ignored: the null control failed above.")
        return 1
    n = 0
    for eid, _qty, eu, lo, hi, cid, val, shared, ev, _ins, _st in sat:
        why = (f"claim {cid} gives {val:g} {eu}, inside "
               f"[{lo if lo is not None else '-'}, {hi if hi is not None else '-'}]; matched on "
               f"units equality and rare shared terms {','.join(shared[:4])}; proposed by "
               f"entailment_candidates.py with its shuffled null at {ratio:.0%}")
        q(f"update constraint_entailed set status='satisfied', satisfied_by={lit(why)}, "
          f"satisfied_evidence={lit(ev)} where id={eid} and status='open'")
        n += 1
    print(f"\n  recorded {n} entailment(s) as satisfied, each citing the claim and the value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
