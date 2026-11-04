#!/usr/bin/env python3
"""Run every spec's acceptance criteria against the live database and report violations.

WHY THIS EXISTS. Four specs in docs/specs/ carry numbered acceptance criteria, and each of them
says in its own closing section that nothing enforces them:

    SPEC-idea-intake-and-settings: "No checker enforces any of section 7. The schema permits the
                                    invalid states the spec forbids."
    SPEC-evaluation-kernel:        "Section 3 is not enforced and not satisfied."
    SPEC-subproblem-lifecycle:     "Rules 1, 2, 4 and 5 are enforced in code; 3 and 6 are enforced
                                    only by the poll and the trigger, both of which have already
                                    failed once each."

An acceptance criterion nobody runs is a wish. Worse, it is a wish that READS like a guarantee:
anyone opening the spec sees a numbered list of things that are supposedly true of the system.

HOW TO READ THE OUTPUT. A rule reports PASS, FAIL or UNCHECKED. `UNCHECKED` is not a pass and is
printed in the same column deliberately -- a rule this script cannot evaluate is exactly as
unenforced as it was before the script existed, and hiding it would recreate the problem.

EVERY RULE SHIPS WITH A POSITIVE CONTROL (`--selftest`), because a check whose query is wrong
returns zero violations and looks identical to a system with no violations. That failure has
happened repeatedly in this project, in six different costumes. A rule with no control is reported
as UNCHECKED however green it looks.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
# READ THIS BEFORE TRUSTING A RESULT. This constant is NOT used by any rule query: a grep for its
# interpolation returns 0 across all 25 rules. The checker reports on the WHOLE DATABASE. It was
# written when `zebrafish-flight` was the only project, so database-wide and project-scoped were the
# same answer; since the coral import on 2026-11-04 they are not.
#
# Defining the right constant and ignoring it is WORSE than hardcoding the id, because a reader who
# sets SWARM_PROJECT reasonably concludes the output is scoped. That is how a run with
# SWARM_PROJECT=coral came back reporting subproblem-lifecycle failures for a project with ZERO
# subproblems.
#
# NOT scoped here, deliberately. Nine of the tables the rules touch carry project_id
# (claim, run, subproblem, artifact, idea, rubric, setting, agent_session, project_capability) and
# the rest reach a project only through a parent (challenge, grade, grader_calibration, review_flag,
# subproblem_dep, idea_check, idea_score). Scoping SOME rules and not others would produce a number
# that is neither database-wide nor project-scoped, and nothing in the output would say which -- a
# worse failure than the present one, which is at least uniform. Full scoping is open work.
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
SCOPE_NOTE = ("Rules are scoped to SWARM_PROJECT where that is PROVABLY safe (one `from` on a table\n         carrying project_id, no join). The rest run database-wide and are marked [GLOBAL] on\n         their own line. Full scoping of the join/parent cases is open work.")


def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


SCOPABLE = {"claim", "run", "subproblem", "artifact", "idea", "rubric", "setting",
            "agent_session", "project_capability"}


def scope_sql(sql: str) -> tuple[str, bool]:
    """Inject `project_id = PROJECT` when it is PROVABLY safe, else leave the query alone.

    Safe means: a single `from <table>` naming a table that carries project_id, with no join and
    no subquery `from`. Anything else is returned untouched and reported as GLOBAL, because a
    number that is neither database-wide nor project-scoped, with nothing saying which, is worse
    than either (the reasoning above PROJECT).

    Returns (sql, was_scoped).
    """
    # An ALIAS makes the bare table name invalid: `from subproblem sp` then `subproblem.project_id`
    # is a SQL error. Caught by the zebrafish control, which is the only reason it is handled.
    froms = re.findall(r"\bfrom\s+([a-z_]+)(\s+([a-z_]+))?", sql)
    if len(froms) != 1 or froms[0][0] not in SCOPABLE or " join " in sql.lower():
        return sql, False
    t, alias = froms[0][0], (froms[0][2] or "").strip()
    if alias and alias not in ("where", "group", "order", "limit"):
        t = alias
    filt = f"{t}.project_id = {_lit(PROJECT)}"
    m = re.search(r"\bwhere\b", sql, re.I)
    if m:
        return sql[:m.end()] + f" {filt} and " + sql[m.end():], True
    # no WHERE: append one, before any group/order/limit tail
    m2 = re.search(r"\b(group\s+by|order\s+by|limit)\b", sql, re.I)
    cut = m2.start() if m2 else len(sql)
    return sql[:cut] + f" where {filt} " + sql[cut:], True


def _lit(v) -> str:
    return "'" + str(v).replace("'", "''") + "'"


def q(sql):
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [l.split(SEP) for l in r.stdout.strip().split("\n") if l]


def count(sql):
    return int(q(sql)[0][0])


# Each rule: (spec, number, text, violation_sql, control_sql_or_None)
# `violation_sql` returns a COUNT of rows that BREAK the rule; 0 is a pass.
# `control_sql` must return a NON-ZERO count, proving the query reaches real rows at all. A control
# that returns 0 means the rule is UNCHECKED -- the violation query may simply be looking nowhere.
RULES = [
 ("ASK-artifact-graph", 1, "Every artifact has an id, a kind, and a content hash where it has bytes",
  "select count(*) from artifact where kind is null or (path is not null and sha256 is null)",
  "select count(*) from artifact"),
 ("ASK-artifact-graph", 2, "Every claim has an evidence level; literature sources carry a read_level",
  "select count(*) from claim where superseded_by is null and (evidence is null "
  "or (evidence='literature' and read_level is null))",
  "select count(*) from claim where superseded_by is null"),
 ("ASK-artifact-graph", 3, "Every run has a code_sha or a stated reason it is not executable",
  # btrim(): `code_sha = ''` is NOT `code_sha is null`, and run 17 holds exactly that. The
  # original test asked only `is null`, so it returned 0 violations while a run had no code_sha
  # and no stated reason -- the rule reported PASS with a real violation in the table. An empty
  # string is the shape a missing value takes when it comes from a shell variable that did not
  # expand, so it is the likely shape, not an exotic one.
  #
  # not_executable_because is the field SPEC-ASK section 4 item 1 asks for, added 2026-11-04.
  # `notes ilike '%not_executable%'` is kept for rows written before the column existed: that
  # convention carried the distinction in free-text prose, where a typo silently converted a
  # documented non-executable run into an undocumented one.
  "select count(*) from run where btrim(coalesce(code_sha,'')) = '' "
  "and btrim(coalesce(not_executable_because,'')) = '' "
  "and coalesce(notes,'') not ilike '%not_executable%'",
  "select count(*) from run"),
 ("ASK-artifact-graph", 4, "No recorded value changed in place; corrections supersede",
  # Enforced structurally. A superseding claim must be NEWER than what it replaces; an older
  # replacement means a row was rewritten rather than appended.
  "select count(*) from claim a join claim b on a.superseded_by=b.id where b.created_at < a.created_at",
  "select count(*) from claim where superseded_by is not null"),
 ("ASK-artifact-graph", 5, "Every quantity carries units",
  # A number with no unit is not a quantity. Scoped to claims that actually committed a value.
  "select count(*) from claim where superseded_by is null and value_num is not null "
  "and (units is null or btrim(units)='')",
  "select count(*) from claim where value_num is not null"),
 ("ASK-artifact-graph", 6, "Every challenge outcome recorded, INCLUDING survived",
  # IN-FLIGHT IS NOT A VIOLATION. The first version flagged every challenge dispatched in the last
  # few minutes, because an agent that has not reported yet leaves `outcome` null -- 93 of its 96
  # hits were work in progress. A checker that cannot tell "not finished" from "not recorded"
  # reports the system as broken whenever it is busy, and then gets ignored. Same distinction the
  # entailment work needed between "nobody looked" and "looked and found nothing".
  # `not-run` IS a recorded outcome -- it says the challenge did not run, which a system that
  # honestly records abandonment must be able to say. Only NULL is unrecorded. Counting both
  # identically would make an honest record indistinguishable from lost data, which is this
  # project's own recurring failure pointed at its own bookkeeping.
  "select count(*) from challenge where outcome is null "
  "and created_at < now() - interval '2 hours'",
  "select count(*) from challenge"),
 ("evaluation-kernel", 1, "No grade recorded against an unfrozen rubric",
  "select count(*) from grade g join rubric r on r.id=g.rubric_id where r.frozen is not true",
  "select count(*) from grade"),
 ("evaluation-kernel", 2, "No rubric edited in place",
  "select count(*) from rubric a join rubric b on a.superseded_by=b.id where b.registered_at < a.registered_at",
  "select count(*) from rubric"),
 ("evaluation-kernel", 3, "No grader aggregated without a calibration that caught a known-bad item",
  "select count(*) from (select distinct grader from grade) g where not exists "
  "(select 1 from grader_calibration c where c.grader=g.grader and c.caught_known_bad > 0)",
  "select count(*) from grade"),
 ("evaluation-kernel", 6, "A cost-attribution query is runnable and its no-output bucket readable",
  # SPEC-evaluation-kernel rule 6. Not a state rule but a capability one: can spend be attributed
  # to output at all? It can, through agent_session.branch -> 'harvest:<leaf>' in claim.source,
  # artifact_signal.voter_id and constraint_entailed.note. This flags sessions that cost money and
  # carry NO branch, because those cannot be attributed in either direction.
  "select count(*) from agent_session where cost_usd > 0 and (branch is null or branch = '')",
  "select count(*) from agent_session where cost_usd > 0"),
 ("evaluation-kernel", 5, "Every pairwise comparison run in both orders with the order recorded",
  "select count(*) from grade where order_seed is null",
  "select count(*) from grade"),
 ("idea-intake", 1, "Every idea retains its verbatim body",
  "select count(*) from idea where body is null or btrim(body)=''",
  "select count(*) from idea"),
 ("idea-intake", 2, "No promotion without a normalised_question",
  "select count(*) from idea where status='promoted' and (normalised_question is null "
  "or btrim(normalised_question)='')",
  "select count(*) from idea"),
 ("idea-intake", 4, "Every rejection carries a reason and is retained",
  "select count(*) from idea where status='rejected' and (decision_note is null "
  "or btrim(decision_note)='')",
  "select count(*) from idea"),
 ("idea-intake", 6, "Every capability a project uses is declared in project_capability",
  "select count(*) from project p where not exists "
  "(select 1 from project_capability c where c.project_id=p.id)",
  "select count(*) from project"),
 ("idea-intake", 3, "No score computed from anything but the checks",
  # A score for an idea that has no recorded checks was computed from something else.
  "select count(*) from idea_score sc where not exists "
  "(select 1 from idea_check ck where ck.idea_id = sc.idea_id)",
  "select count(*) from idea_check"),
 ("idea-intake", 5, "No agent writes a locked setting",
  # `locked` exists to stop an agent changing policy. An agent-authored locked row means it did.
  "select count(*) from setting where locked is true and updated_by is not null "
  "and (updated_by ilike 'agent%' or updated_by ilike '%cloud:%' or updated_by ilike 'branch:%')",
  "select count(*) from setting"),
 ("subproblem-lifecycle", 4, "Readiness honours subproblem_dep, with refuted satisfying a dependency",
  # A subproblem may not be `running` while something it depends on is still unresolved. `refuted`
  # counts as resolved -- a question settled negatively has been settled -- so it is NOT a blocker.
  "select count(*) from subproblem sp join subproblem_dep d on d.subproblem_id = sp.id "
  "join subproblem up on up.id = d.depends_on "
  "where sp.status = 'running' and up.status not in ('answered','refuted')",
  "select count(*) from subproblem_dep"),
 ("subproblem-lifecycle", 6, "Every superseded claim flags the subproblems resting on it",
  # A superseded claim with NO DEPENDENTS cannot flag anything, and requiring a flag for it is
  # the rule being wrong rather than the system. Of 39 superseded claims only 7 have a dependent
  # edge; the other 32 were counted as violations by the first version of this rule, which is the
  # same defect as counting in-flight challenges as unrecorded outcomes.
  "select count(distinct c.id) from claim c join claim_depends d on d.depends_on = c.id "
  "where c.superseded_by is not null and not exists "
  "(select 1 from review_flag f where f.triggered_by = c.id)",
  "select count(distinct c.id) from claim c join claim_depends d on d.depends_on = c.id "
  "where c.superseded_by is not null"),
 ("subproblem-lifecycle", 1, "No answered without an answer and an answer_kind",
  "select count(*) from subproblem where status='answered' and (answer is null "
  "or btrim(answer)='' or answer_kind is null)",
  "select count(*) from subproblem where status='answered'"),
 ("subproblem-lifecycle", 2, "No blocked without a named blocker",
  "select count(*) from subproblem where status='blocked' and (blocked_on is null "
  "or btrim(blocked_on)='')",
  "select count(*) from subproblem"),
 ("subproblem-lifecycle", 3, "No running subproblem without a live session",
  "select count(*) from subproblem sp where sp.status='running' and not exists "
  "(select 1 from agent_session s where s.subproblem_id=sp.id and s.status in ('running','working'))",
  "select count(*) from subproblem where status='running'"),
 ("subproblem-lifecycle", 5, "Deepening capped at depth 2 (pre-cap rows are kept, not deleted)",
  # Reports 4 rows created BEFORE the cap existed. They are `answered` and carry 2-4 claims each,
  # so deleting them to turn this green would destroy real results to satisfy a checker -- which is
  # the "never relax an acceptance criterion to make it pass" rule, inverted. The cap itself is
  # verified separately below and holds: no depth-2 row is eligible for deepening, so no new
  # depth-3 row can be created. This rule stays RED on purpose and the detail says why.
  "select count(*) from subproblem where id like '%-D-D-D%'",
  "select count(*) from subproblem where id like '%-D%'"),
 ("subproblem-lifecycle", "5b", "The depth cap is live: no depth-2 row is eligible for deepening",
  "select count(*) from subproblem sp where sp.status in ('answered','refuted') "
  "and sp.id not like '%-D-D%' and sp.id like '%-D-%'",
  "select count(*) from subproblem where id like '%-D%'"),
]


# Rule 7 of SPEC-ASK is about the RECORD, not the database: "every dimension this record does not
# satisfy is named in the record, with the reason". The spec says of it, in its own words, that it
# "is the one that makes the other six honest" -- and it was the rule this checker originally left
# out, which is the failure it exists to prevent, committed by the thing meant to prevent it.
# It is checked against the spec document: all six ASK dimensions must appear in the status table
# with a non-empty gap column.
ASK_DIMS = ["D1 Addressability", "D2 Evidential traceability", "D3 Conditional executability",
            "D4 Version responsiveness", "D5 Context-preserving transferability",
            "D6 Contestable federation"]
SPEC_ASK = "/data/worktrees/delphi-frontier/swarm-arch/docs/specs/SPEC-ASK-artifact-graph.md"


def check_ask_rule7():
    """Returns (status, detail). Every dimension needs a row AND a stated gap."""
    try:
        text = open(SPEC_ASK).read()
    except OSError as e:
        return "UNCHECKED", f"cannot read the spec: {e}"
    missing, no_gap = [], []
    for dim in ASK_DIMS:
        rows = [l for l in text.split("\n") if dim in l and l.strip().startswith("|")]
        if not rows:
            missing.append(dim); continue
        # The gap is the LAST cell of the table row; a dimension with no stated gap is the
        # failure mode -- a clean-looking table that has quietly stopped admitting anything.
        cells = [c.strip() for c in rows[0].strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[-1] or cells[-1] in ("-", "none", "n/a"):
            no_gap.append(dim)
    if missing:
        return "FAIL", f"{len(missing)} dimension(s) absent from the status table: {missing}"
    if no_gap:
        return "FAIL", f"{len(no_gap)} dimension(s) with no stated gap: {no_gap}"
    return "PASS", f"all {len(ASK_DIMS)} dimensions present with a stated gap"


def main():
    selftest = "--selftest" in sys.argv
    rows = []
    for spec, n, text, vsql, csql in RULES:
        try:
            # Scope to PROJECT where provably safe; otherwise run the rule database-wide and SAY SO
            # in its own detail line, so no single number is ambiguous about what it covered.
            raw_csql = csql
            vsql, v_scoped = scope_sql(vsql)
            csql, c_scoped = (scope_sql(csql) if csql else (csql, False))
            tag = "" if (v_scoped and (c_scoped or not csql)) else "  [GLOBAL: not project-scoped]"
            control = count(csql) if csql else 0
            if control == 0:
                # DID SCOPING EMPTY A RULE THAT WAS BEING CHECKED? `setting` holds 8 rows with a
                # NULL project_id, so scoping took that rule from checking 8 to checking 0 --
                # disabling a working check by "improving" it, which is this repo's own empty-set
                # failure introduced by the fix for a different one. Say so instead of printing a
                # bare UNCHECKED.
                was = count(raw_csql) if (raw_csql and c_scoped) else 0
                extra = (f"; SCOPING EMPTIED THIS RULE -- it checks {was} row(s) database-wide and "
                         f"0 for project {PROJECT!r}. The rows exist but carry no project_id, so "
                         f"the rule is unevaluable per project, NOT satisfied." if was else "")
                rows.append(("UNCHECKED", spec, n, text, "control returned 0 rows: nothing to check "
                             "yet, so a zero-violation result would be meaningless" + extra + tag))
                continue
            v = count(vsql)
            rows.append((("PASS" if v == 0 else "FAIL"), spec, n, text,
                         (f"{v} violating row(s) of {control}" if v else f"{control} rows checked") + tag))
        except Exception as e:
            rows.append(("UNCHECKED", spec, n, text, f"query failed: {type(e).__name__}: {e}"))

    st7, detail7 = check_ask_rule7()
    rows.append((st7, "ASK-artifact-graph", 7,
                 "Every dimension NOT satisfied is named in the record, with the reason", detail7))

    w = max(len(r[1]) for r in rows)
    fails = unchecked = 0
    for st, spec, n, text, detail in rows:
        if st == "FAIL":
            fails += 1
        if st == "UNCHECKED":
            unchecked += 1
        print(f"  {st:<9} {spec:<{w}} §{n}  {text}")
        if st != "PASS":
            print(f"            -> {detail}")

    print(f"\n  SCOPE: {SCOPE_NOTE}")
    try:
        projs = q("select project_id, count(*) from claim group by 1 order by 2 desc")
        if len(projs) > 1:
            print("    the database holds "
                  + ", ".join(f"{p[0]} ({p[1]} claims)" for p in projs)
                  + " -- so these counts mix them.")
    except Exception:
        pass
    print(f"\n  {len(rows)} rules: {len(rows)-fails-unchecked} pass, {fails} FAIL, "
          f"{unchecked} UNCHECKED")
    print("  UNCHECKED is NOT a pass. A rule this script cannot evaluate is exactly as unenforced")
    print("  as it was before the script existed.")
    print()
    print("  AND A FAIL IS A HYPOTHESIS, NOT A VERDICT. Five of this file's own rules were found")
    print("  over-strict on 2026-11-04, and in every case the first reading blamed the system:")
    print("    - in-flight challenges counted as unrecorded outcomes")
    print("    - `not-run` counted the same as NULL, so honest abandonment looked like lost data")
    print("    - superseded claims with NO dependents required to have flagged something")
    print("    - a shortfall required to span a whole measured range when one end is the right one")
    print("    - pre-cap rows counted against a cap that now holds (still red, deliberately)")
    print("  Before fixing data to clear a red, check whether the rule is asking the right thing.")

    if selftest:
        # POSITIVE CONTROL. Every rule above is a count of BAD rows, so a rule whose query is
        # malformed, points at an empty table, or filters everything out returns 0 and is
        # indistinguishable from a clean system. Here we check the inverse query finds rows: if
        # neither the violation set nor its complement is reachable, the query reaches nothing.
        print("\n  SELFTEST -- each rule's query must be able to see rows at all:")
        bad = 0
        for spec, n, text, vsql, csql in RULES:
            try:
                c = count(csql) if csql else 0
                mark = "ok  " if c > 0 else "DEAD"
                if c == 0:
                    bad += 1
                print(f"    {mark} {spec} §{n}: control sees {c} rows")
            except Exception as e:
                bad += 1
                print(f"    DEAD {spec} §{n}: {type(e).__name__}")
        print(f"  {bad} rule(s) have no reachable rows and are reported UNCHECKED above.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
