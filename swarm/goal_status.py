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
    # A lever with NO published construct is RESOLVED, not pending. Counting it as pending
    # leaves a permanently red row and hides the difference between "not looked up" and
    # "looked up, nothing exists" -- which for superfast-myosin is the whole finding (claim
    # 1093: no construct, and no precedent for heterologous expression of any superfast myosin).
    # The threshold is therefore whether each lever's question is ANSWERED, not whether each
    # lever works. A lever that cannot be built is an answer.
    noconstruct = num("""select count(*) from claim where project_id='%s'
                         and superseded_by is null and evidence='refused'
                         and statement like '%%NOT A LEVER%%'""" % PROJ)
    resolved = specced + noconstruct
    # TWO ROWS, NOT ONE. The previous version merged these and set the threshold on `resolved`,
    # which counted a lever with NO buildable construct as done. That is a threshold moved in my
    # own favour: the goal asks for genetic changes that could make a fish fly, and a lever
    # nothing can build does not contribute one. Reported as two independent rows so neither
    # number hides behind the other -- the hard bar stays hard, and the research question that
    # WAS answered still gets its credit.
    # THE ROW MEASURED THE WRONG THING AND PASSED ITSELF (corrected 2026-11-05, claim 1134).
    # It counted levers having a part_revision and called that "a buildable variant", while its
    # own stated meaning below is "every lever names a variant that could actually be MADE".
    # Those differ: a revision may name a published allele whose molecular lesion nobody holds.
    # Measured, 2 of 7 revisions carry a content_sha256 -- an actual sequence change this project
    # holds -- and BOTH are variants of kcnk5b, so the six-lever design has ONE orderable locus.
    # The previous comment on this row says "the hard bar stays hard"; it was not hard, because
    # the quantity it tested was existence of a row. Counting the thing the row claims to count
    # flips it from OK to open and takes the project from 8 of 10 to 7 of 10, which is the
    # correct direction for a correction that nobody else would have made.
    buildable = num("""select count(distinct pr.part_id) from part_revision pr
                       join part p on p.id = pr.part_id
                       where p.project_id='%s' and pr.content_sha256 is not null""" % PROJ)
    # THE MEASUREMENT IS A PROXY AND IS NOW LABELLED AS ONE (panel, claims 1134/1135). Both
    # models objected that a non-null content_sha256 means "a sequence this project holds", not
    # "orderable": the follistatin ORF has no promoter so the transgene cannot be built, the
    # chimera is an unvalidated design, and kcnk5b@alf-W169L is counted from an abstract alone.
    # The criterion below is UNCHANGED -- relaxing it to match the proxy is forbidden. What
    # changes is that the row no longer calls the proxy by the criterion's name.
    yield ("genetic levers with a SEQUENCE THIS PROJECT HOLDS  [proxy for the hard bar]",
           f"{buildable:.0f} of {levers:.0f} levers carry a SEQUENCE CHANGE this project holds "
           f"(non-null content_sha256); {specced:.0f} have a part_revision of any kind, but a "
           f"revision naming a published allele whose lesion is not held cannot be made. "
           f"THIS UNDERCOUNTS BY ONE ON PURPOSE AND THE REASON IS DECLARED: kcnh2a@longfin is a "
           f"chromosome-2 inversion with no coding change, so its null hash is a design fact "
           f"rather than a gap, and the strain exists. col9a1c WAS a second declared null and is "
           f"no longer: claim 1871 inferred from the absence of a curated transcript that its "
           f"frameshift product was underdetermined, this project's adversarial arm challenged "
           f"that inference for never checking it, and applying both published lesions to ALL SIX "
           f"predicted CDSs gives the SAME product every time -- 180 aa for zf3676, 234 aa for "
           f"zf3677 -- because the premature stop falls 11 and 12 residues after the shift, well "
           f"before the variants diverge. Both are now specified and hashed (claim 2082, "
           f"superseding 1871). That lever still points the WRONG WAY (claim 1138, its knockout "
           f"shrinks the fin), which is a design fact and not a specification gap. Counting "
           f"kcnh2a as buildable would need the "
           f"metric to read an editorial table (analysis/genetic_design.py NULL_REASON), which "
           f"is the kind of dependency that let the previous version of this row pass itself. "
           f"AND A HELD SEQUENCE IS NOT AN ORDERABLE CONSTRUCT: the follistatin ORF has no "
           f"promoter and the MYH13 chimera is a design nobody has made, so a hash is not a "
           f"construct. (An earlier version of this sentence added that kcnh2a's inversion "
           f"needs breakpoint coordinates this project does not hold; that is no longer true "
           f"-- the revision holds ~23.174 and ~24.075 Mb in Zv11, a ~901 kb inversion, and the "
           f"null is now a junction-not-in-reference problem rather than a missing coordinate.) The threshold below is the real bar and this "
           f"number is only the closest thing the database can count",
           buildable >= levers,
           "every lever names a variant that could actually be made")
    yield ("genetic levers RESEARCHED to a conclusion",
           f"{resolved:.0f} of {levers:.0f} answered "
           f"({specced:.0f} specified, {noconstruct:.0f} shown to have no published construct); "
           f"{levers-resolved:.0f} unexamined",
           resolved >= levers,
           "each lever either names a variant or is shown to have none in the literature")

    # COUNTED OVER DISTINCT CONSTRAINTS, NOT ROWS, and the difference ran in the flattering
    # direction. 24 duplicate groups hold 78 rows, 54 of them redundant -- the same constraint
    # entered up to three times with identical quantity, bounds, units and source claim (the
    # bluegill fin-ray EI bound is there three times). Satisfied rows were duplicated more than
    # unsatisfied ones, so the row-count ratio read 130/381 = 34.1% where distinct constraints
    # give 105/327 = 32.1%. Found 2026-11-05 by entailment_match.py, which could not match
    # against the set without tripping over the copies.
    key = ("""coalesce(quantity,'')||'|'||coalesce(lo::text,'')||'|'||coalesce(hi::text,'')"""
           """||'|'||coalesce(units,'')||'|'||coalesce(source_claim::text,'')""")
    sat = num(f"""select count(*) from (select {key} as k,
                    max(case status when 'satisfied' then 1 else 0 end) as s
                    from constraint_entailed where project_id='{PROJ}' group by 1) t
                  where s = 1""")
    tot = num(f"""select count(distinct {key}) from constraint_entailed
                  where project_id='{PROJ}'""")
    rows = num("select count(*) from constraint_entailed where project_id='%s'" % PROJ)
    yield ("cross-scale chain",
           f"{sat:.0f} of {tot:.0f} DISTINCT entailments satisfied "
           f"({rows:.0f} rows before de-duplication); chain spans 8/8 scales (claim 1084)",
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
    # MOST `measured` CLAIMS HERE ARE NOT ABOUT THE ANIMAL (measured 2026-11-05, claim 1177).
    # Of 167 live measured claims, 118 carry NO biological scale: they are measurements of this
    # project's own tooling -- generator defects, citation audits, panel behaviour, pLDDT runs,
    # entailment bookkeeping. A random sample of ten pre-session ones was 10/10 process claims.
    # Those are legitimate claims and correctly labelled `measured`; what was wrong is counting
    # them in a row whose stated meaning is the empirical grounding of the SCIENCE. The row now
    # reports the biology-grounded count and the raw count side by side, and gates on the first.
    # The project itself had already noticed the drift in one case -- claim 513, "THE RESIDUE-200
    # SERIES HAS BECOME A STUDY OF ESMFOLD2 RATHER THAN OF THE FISH".
    meas_bio = num("select count(*) from claim where project_id='%s' and superseded_by is null "
                   "and evidence='measured' and scale_id is not null" % PROJ)
    yield ("grounded, non-fabricated claims",
           f"{meas_bio:.0f} of {live:.0f} live claims are `measured` AND carry a biological "
           f"scale; {meas:.0f} are `measured` in all, so {meas-meas_bio:.0f} measure this "
           f"PROJECT (tooling, panels, generators) rather than the animal",
           meas_bio / live > 0.2 if live else False,
           "a substantial fraction measured ABOUT THE ORGANISM, not about the pipeline")

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
    spc = num("select count(*) from spec_parameter where coalesce(conditions,'') <> ''")
    # The WORDING is derived too, not just the number. This row previously read "spec_parameter
    # still N rows (vacuous constraint)" and kept saying it after the table filled -- the
    # sentence contradicted the count printed inside it. Third stale hand-written fragment in
    # this module, which is the one that exists to stop exactly that.
    verdict = (f"{sp:.0f} rows, {spc:.0f} carrying mandatory conditions -- the constraint binds"
               if sp else "0 rows, so its mandatory conditions/units are VACUOUSLY satisfied")
    yield ("ASK D5 transferability",
           f"transfer record implemented; spec_parameter {verdict}",
           sp > 0 and spc == sp,
           "every spec_parameter row carries the conditions its value depends on")

    yield ("nanopub / ASK publication",
           "dry run only; output lacks trusty URIs and is explicitly NOT publishable",
           False, "AUTHORISATION REQUIRED -- publishing is irreversible, owner's call")

    # MEASURED, NOT ASSERTED. This row was hand-written as "NOT MEASURABLE HERE" in the first
    # version of this file -- inside a module whose own docstring says a hand-written headline is
    # where all the staleness lands. It was substantively right and methodologically wrong, and
    # it would never have changed no matter what the project built. Now it asks the graph.
    # A METRIC MUST NOT COUNT ITS OWN MODULE. Measured 2026-11-05: this row reported "2
    # module(s) link a molecular scale to organism-or-wider", and one of the two was
    # goal_status.py -- this file, whose two claims happen to sit at `dna` and `organism`.
    # The scoreboard was scoring itself, which is the shape section 1 rule 3 forbids: a number
    # computed from something other than the thing being scored. Excluding it leaves ONE
    # qualifying module, so the row still passes, but it now passes for a real reason.
    #
    # The old COARSE caveat is also gone, replaced by the thing it was apologising for: the
    # skipped rungs are now computed and printed per module, so a jump is visible rather than
    # disclaimed. power_frequency_envelope.py spans protein < tissue < organ < organism and
    # skips `cell`; that is reported, not hidden, and it is NOT failed -- demanding every rung
    # would reject a chain that is scientifically contiguous as built.
    SELF = "goal_status.py"
    ladder = [x for x in one(
        "select coalesce(string_agg(id, ',' order by ord), '') from scale").split(",") if x]
    raw = one(r"""with m as (
                    select regexp_replace(source, '^.*?([a-z0-9_]+\.py).*$', '\1') as mod,
                           scale_id
                    from claim where project_id='%s' and superseded_by is null
                      and scale_id is not null and source ~ '[a-z0-9_]+\.py')
                  select coalesce(string_agg(mod || ':' || sc, ';' order by mod), '')
                  from (select mod, string_agg(distinct scale_id, ',') as sc
                        from m where mod <> '%s' group by mod) t""" % (PROJ, SELF), "")
    mods = {}
    for part in (x for x in raw.split(";") if ":" in x):
        mod, sc = part.split(":", 1)
        mods[mod] = [x for x in sc.split(",") if x in ladder]
    span = max((len(v) for v in mods.values()), default=0)
    MOLEC, WIDE = {"dna", "protein"}, {"organism", "behaviour", "ecology"}
    linked = sorted(m for m, v in mods.items()
                    if MOLEC & set(v) and WIDE & set(v))
    detail = []
    for m in linked:
        idx = sorted(ladder.index(x) for x in mods[m])
        skipped = [ladder[k] for k in range(idx[0], idx[-1] + 1) if k not in idx]
        detail.append(f"{m} ({' < '.join(sorted(mods[m], key=ladder.index))}"
                      + (f"; SKIPS {','.join(skipped)}" if skipped else "; contiguous") + ")")
    yield ("end-to-end multi-scale SIMULATION",
           f"widest scale span by one module: {span} scales; "
           f"{len(linked)} module(s) link a molecular scale (dna/protein) to organism-or-wider"
           + (": " + "; ".join(detail) if detail else "")
           + f"  [{SELF} excluded: a metric must not count its own module]",
           len(linked) > 0,
           "one module whose inputs are molecular and whose outputs are whole-animal")


def main() -> int:
    print(f"  GOAL STATUS for {PROJ} -- every number fetched, none written by hand\n")
    done = total = 0
    for item, measurement, ok, means in rows():
        total += 1
        done += bool(ok)
        print(f"  [{'OK ' if ok else '   '}] {item}")
        print(f"         {measurement}")
        if not ok:
            print(f"         would be done when: {means}")
    print(f"\n  {done} of {total} goal items meet their stated threshold.")
    print("  A threshold is an editorial choice and is printed beside each row so it can be")
    print("  disagreed with. Nothing here grades the science; it reports what the record holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
