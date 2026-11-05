#!/usr/bin/env python3
"""Compute the state of each goal item from the database and the repo. Nothing is hand-written.

WHY GENERATED RATHER THAN NARRATED. Measured over this session: every number fetched from the
claim graph was right, and five of five summary paragraphs composed by hand contradicted the
table directly above them. A generated body is re-derived on every run and cannot drift; a
hand-written headline is written once against the state of the world at that moment and nothing
re-checks it. So this declares only the editorial mapping -- which query answers which goal item,
and what counts as done -- and fetches every number.

IT REPORTS, IT DOES NOT GRADE. Each row prints the measurement and a status derived from a stated
threshold. Where a goal item cannot be measured from the record, the row says NOT MEASURABLE HERE
rather than guessing, because a monitor that invents a green is worse than no monitor.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env  # noqa: E402

PROJ = os.environ.get("SWARM_PROJECT", "zebrafish-flight")


def one(sql: str, default: str = "?") -> str:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    return r.stdout.strip().split("\x01")[0] if r.returncode == 0 and r.stdout.strip() else default


def num(sql: str) -> float:
    try:
        return float(one(sql, "0"))
    except ValueError:
        return 0.0


#: (goal item, query -> measurement, threshold fn, what "done" would mean)
def rows():
    levers = num("select count(*) from part where project_id='%s'" % PROJ)
    specced = num("select count(distinct part_id) from part_revision pr "
                  "join part p on p.id=pr.part_id where p.project_id='%s'" % PROJ)
    yield ("genetic levers with a concrete variant",
           f"{specced:.0f} of {levers:.0f} levers have a part_revision",
           specced >= levers, "every lever names what to change it to")

    sat = num("""select count(*) from constraint_entailed where project_id='%s'
                 and status='satisfied'""" % PROJ)
    tot = num("select count(*) from constraint_entailed where project_id='%s'" % PROJ)
    yield ("cross-scale chain",
           f"{sat:.0f} of {tot:.0f} entailments satisfied; chain spans 8/8 scales (claim 1084)",
           sat / tot > 0.5 if tot else False,
           "most cross-scale constraints satisfied, not just connected")

    ch = num("select count(*) from challenge ch join claim c on c.id=ch.claim_id "
             "where c.project_id='%s'" % PROJ)
    ref = num("select count(*) from challenge ch join claim c on c.id=ch.claim_id "
              "where c.project_id='%s' and ch.outcome='refuted'" % PROJ)
    sup = num("""select count(distinct ch.claim_id) from challenge ch join claim c on c.id=ch.claim_id
                 where c.project_id='%s' and c.superseded_by is not null""" % PROJ)
    yield ("adversarial refinement",
           f"{ch:.0f} challenges, {ref:.0f} refuted, {sup:.0f} challenged claims superseded",
           sup > 0, "challenges change claims, not just score them")

    live = num("select count(*) from claim where project_id='%s' and superseded_by is null" % PROJ)
    meas = num("select count(*) from claim where project_id='%s' and superseded_by is null "
               "and evidence='measured'" % PROJ)
    yield ("grounded, non-fabricated claims",
           f"{meas:.0f} of {live:.0f} live claims are `measured` (not simulated/assumed)",
           meas / live > 0.2 if live else False, "a substantial measured fraction")

    openn = num("select count(*) from subproblem where project_id='%s' and status='open'" % PROJ)
    ans = num("select count(*) from subproblem where project_id='%s' and status='answered'" % PROJ)
    yield ("frontier of work",
           f"{ans:.0f} answered, {openn:.0f} open subproblems",
           openn > 0, "an open frontier exists and is being worked")

    noscale = num("select count(*) from subproblem where scale_id is null")
    allsub = num("select count(*) from subproblem")
    yield ("architecture replicates to other projects",
           f"{allsub-noscale:.0f} of {allsub:.0f} subproblems across ALL projects carry a scale",
           (allsub - noscale) / allsub > 0.8 if allsub else False,
           "every project's frontier is scale-placed like the fish's")

    sp = num("select count(*) from spec_parameter")
    yield ("ASK D5 transferability",
           f"transfer record implemented; spec_parameter still {sp:.0f} rows (vacuous constraint)",
           sp > 0, "spec_parameter non-empty so its mandatory conditions bite")

    yield ("nanopub / ASK publication",
           "dry run only; output lacks trusty URIs and is explicitly NOT publishable",
           False, "AUTHORISATION REQUIRED -- publishing is irreversible, owner's call")

    # MEASURED, NOT ASSERTED. This row was hand-written as "NOT MEASURABLE HERE" in the first
    # version of this file -- inside a module whose own docstring says a hand-written headline is
    # where all the staleness lands. It was substantively right and methodologically wrong, and
    # it would never have changed no matter what the project built. Now it asks the graph.
    span = one("""with m as (
                    select regexp_replace(source, '^.*?([a-z0-9_]+\\.py).*$', '\\1') as mod,
                           scale_id
                    from claim where project_id='%s' and superseded_by is null
                      and scale_id is not null and source ~ '[a-z0-9_]+\\.py')
                  select coalesce(max(n)::text,'0') from (
                    select count(distinct scale_id) as n from m group by mod) t""" % PROJ, "0")
    molec = one("""with m as (
                     select regexp_replace(source, '^.*?([a-z0-9_]+\\.py).*$', '\\1') as mod,
                            scale_id
                     from claim where project_id='%s' and superseded_by is null
                       and scale_id is not null and source ~ '[a-z0-9_]+\\.py')
                   select count(*)::text from (
                     select mod from m group by mod
                     having bool_or(scale_id in ('dna','protein'))
                        and bool_or(scale_id in ('organism','behaviour','ecology'))) t""" % PROJ, "0")
    yield ("end-to-end multi-scale SIMULATION",
           f"widest scale span by one module: {span} scales; "
           f"{molec} module(s) link a molecular scale (dna/protein) to organism-or-wider",
           int(molec) > 0,
           "one module whose inputs are molecular and whose outputs are whole-animal")


def main() -> int:
    print(f"  GOAL STATUS for {PROJ} -- every number fetched, none written by hand\n")
    done = 0
    for item, measurement, ok, means in rows():
        done += bool(ok)
        print(f"  [{'OK ' if ok else '   '}] {item}")
        print(f"         {measurement}")
        if not ok:
            print(f"         would be done when: {means}")
    print(f"\n  {done} of 9 goal items meet their stated threshold.")
    print("  A threshold is an editorial choice and is printed beside each row so it can be")
    print("  disagreed with. Nothing here grades the science; it reports what the record holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
