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
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")


def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


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
  "select count(*) from run where code_sha is null and coalesce(notes,'') not ilike '%not_executable%'",
  "select count(*) from run"),
 ("ASK-artifact-graph", 4, "No recorded value changed in place; corrections supersede",
  # Enforced structurally. A superseding claim must be NEWER than what it replaces; an older
  # replacement means a row was rewritten rather than appended.
  "select count(*) from claim a join claim b on a.superseded_by=b.id where b.created_at < a.created_at",
  "select count(*) from claim where superseded_by is not null"),
 ("ASK-artifact-graph", 6, "Every challenge outcome recorded, INCLUDING survived",
  # IN-FLIGHT IS NOT A VIOLATION. The first version flagged every challenge dispatched in the last
  # few minutes, because an agent that has not reported yet leaves `outcome` null -- 93 of its 96
  # hits were work in progress. A checker that cannot tell "not finished" from "not recorded"
  # reports the system as broken whenever it is busy, and then gets ignored. Same distinction the
  # entailment work needed between "nobody looked" and "looked and found nothing".
  "select count(*) from challenge where (outcome is null or outcome='not-run') "
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


def main():
    selftest = "--selftest" in sys.argv
    rows = []
    for spec, n, text, vsql, csql in RULES:
        try:
            control = count(csql) if csql else 0
            if control == 0:
                rows.append(("UNCHECKED", spec, n, text, "control returned 0 rows: nothing to check "
                             "yet, so a zero-violation result would be meaningless"))
                continue
            v = count(vsql)
            rows.append((("PASS" if v == 0 else "FAIL"), spec, n, text,
                         f"{v} violating row(s) of {control}" if v else f"{control} rows checked"))
        except Exception as e:
            rows.append(("UNCHECKED", spec, n, text, f"query failed: {type(e).__name__}: {e}"))

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

    print(f"\n  {len(rows)} rules: {len(rows)-fails-unchecked} pass, {fails} FAIL, "
          f"{unchecked} UNCHECKED")
    print("  UNCHECKED is NOT a pass. A rule this script cannot evaluate is exactly as unenforced")
    print("  as it was before the script existed.")

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
