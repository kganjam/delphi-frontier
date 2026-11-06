#!/usr/bin/env python3
"""The design swarm: dispatch subproblems to Claude cloud sessions, record what came back, and keep going.

Project-agnostic by construction -- it reads the frontier out of Postgres and knows nothing about fish. A second
project is a row in `project`, a ladder in `scale` and its own subproblems; the loop below is unchanged.

The honesty floor is enforced at dispatch, not hoped for afterwards: every prompt carries it, and a result is
recorded with the evidence level it earned rather than the one it claims.
"""
import json
import os
import subprocess
import sys
import textwrap

RESEARCH_DIR = "docs/research/" + (
    "fish" if os.environ.get("SWARM_PROJECT", "zebrafish-flight") == "zebrafish-flight"
    else os.environ.get("SWARM_PROJECT", "zebrafish-flight").split("-")[0])
# See generate.py for why this is derived rather than literal.


# -F with a control character: the default field separator is `|`, and a claim statement containing
# one silently splits a row into extra fields. That crashed gen_challenges with "too many values to
# unpack", which stopped the generator refilling and let concurrency fall from 40 to 8 unnoticed --
# the failure looked like "no work to do" rather than like a crash.
SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
ENV = dict(os.environ)
if "PGPASSWORD" not in ENV:
    for line in open("/home/ubuntu/git/morphoswarm/.env"):
        if line.startswith("MORPHOSWARM_PG_PASSWORD="):
            ENV["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")

HONESTY = textwrap.dedent("""
    HONESTY FLOOR -- these are hard rules, and breaking one invalidates the work:
    - Never present a calculated or simulated result as an observation. Say which it is, in the sentence.
    - Never invent a number, a citation, a gene symbol, an allele or an accession. If it is unavailable, write
      `unknown` and say what you tried.
    - Every source carries a read-level: full-text | abstract | listing | search-summary | could-not-access.
    - Separate the author's claim from your inference in the sentence where you draw it.
    - State the scope of every negative search beside the finding.
    - Preserve disagreement between sources. Do not average it away.
    - A negative result, stated precisely, is a successful deliverable. Never manufacture feasibility.
""").strip()


def q(sql):
    # timeout is NOT optional: without it a lock wait or a contended DB hangs the caller
    # forever with no error. generate.py imports this q(), so that hang is silent and
    # unbounded. Measured 2026-11-05: corpus_gap.py's equivalent select exceeded 120 s
    # under load on a 916-row table that answers in 0.04 s idle.
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=ENV, timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def sql_lit(s):
    return "'" + str(s).replace("'", "''") + "'"


def accounts_with_credit():
    """Accounts with unexpired credit, RICHEST FIRST.

    Round-robin drains them unevenly -- measured at 09:5x, max_gmail was at $78 while max_allen
    held $158. An account that empties early stops contributing, so the remaining credit finishes
    later than it needs to. Sorting by balance biases dispatch toward the fullest account and the
    four drain together.
    """
    r = subprocess.run(["orchestra", "cloud", "credit"], capture_output=True, text=True, timeout=180)
    out = []
    for line in r.stdout.strip().split("\n"):
        p = line.split()
        if len(p) >= 2 and p[1] not in ("-",) and "usable" in line:
            try:
                out.append((p[0], float(p[1])))
            except ValueError:
                pass
    return sorted(out, key=lambda x: -x[1])


def ready_subproblems(project):
    """Open rows whose dependencies are all answered -- what an autonomous worker may pick up next."""
    return q(f"""select sp.id, sp.scale_id, sp.question, sp.acceptance, sp.falsifier, sp.why_it_matters
                 from subproblem sp where sp.project_id={sql_lit(project)} and sp.status='open'
                 and not exists (select 1 from subproblem_dep d join subproblem p2 on p2.id=d.depends_on
                                 where d.subproblem_id=sp.id and p2.status not in ('answered','refuted'))
                 order by sp.id""")


def build_prompt(project, sid, scale, question, acceptance, falsifier, why):
    goal = q(f"select goal from project where id={sql_lit(project)}")[0][0]
    return textwrap.dedent(f"""
        SUBPROBLEM {sid} (scale: {scale}) of project `{project}`.

        PROJECT GOAL. {goal}

        THE QUESTION. {question}

        WHY IT MATTERS. {why}

        WHAT WOULD SETTLE IT. {acceptance}

        WHAT WOULD REFUTE THE ANSWER. {falsifier}

        {HONESTY}

        DELIVERABLE. Write `{RESEARCH_DIR}/{sid}-{scale}.md` on a new branch and COMMIT it. Structure:
          1. The question, restated precisely with the numbers that make it hard.
          2. What is measured -- every value with source, year and read-level. Preserve disagreement.
          3. What you computed -- show the arithmetic, state the assumptions, mark it as computation.
          4. The answer, with its evidence level: measured | simulated | derived | literature | refused | unknown.
          5. What this does NOT establish. Be specific and generous here; it is read as carefully as the answer.
          6. What would change the answer -- the measurement or design change that moves it.

        End the file with a machine-readable block, so the swarm can record your result:

        ```swarm-result
        {{"subproblem": "{sid}", "evidence": "<one of: measured|simulated|derived|literature|refused|unknown>",
          "answer": "<one sentence>", "key_number": "<the single number that decides it, with units, or null>",
          "read_level": "<full-text|abstract|listing|search-summary|could-not-access, or null>",
          "blocked_on": "<what you could not get, or null>"}}
        ```

        `read_level` is REQUIRED when your evidence is `literature`, and it is how you actually
        read the source -- not how thoroughly you believe you understand it. Listing a paper is
        not reading it, and a search summary is a lead rather than evidence. "abstract" is an
        honest answer and a common one; say it rather than implying more.

        This field was MISSING from this template until 2026-11-04 and the harvest path had no
        column for it either, so every literature claim the swarm recorded failed
        SPEC-ASK-artifact-graph rule 2 by construction -- 7 of 316 live rows, none of them the
        fault of the agent that wrote them. If you leave it out, the row lands with a NULL and
        stays non-conformant; nothing downstream will guess a level for you, deliberately,
        because inferring how a source was read from how confidently it is described is the
        exact failure that vocabulary exists to prevent.
    """).strip()


def dispatch(project, sid, account, workdir="/data/worktrees/delphi-frontier/foundation"):
    row = q(f"""select id, scale_id, question, acceptance, coalesce(falsifier,''), coalesce(why_it_matters,'')
                from subproblem where id={sql_lit(sid)} and project_id={sql_lit(project)}""")
    if not row:
        raise SystemExit(f"no such subproblem {sid}")
    _, scale, question, acceptance, falsifier, why = row[0]
    prompt = build_prompt(project, sid, scale, question, acceptance, falsifier, why)
    r = subprocess.run(["orchestra", "cloud", "start", "--account", account, "--dir", workdir, "--prompt", prompt],
                       capture_output=True, text=True, timeout=300)
    try:
        d = json.loads(r.stdout)
    except Exception:
        raise SystemExit(f"dispatch failed for {sid} on {account}: {r.stdout[:300]} {r.stderr[:300]}")
    q(f"""insert into agent_session (id, project_id, subproblem_id, harness, account, status, credit_before)
          values ({sql_lit(d['session_id'])}, {sql_lit(project)}, {sql_lit(sid)}, 'cloud',
                  {sql_lit(account)}, 'running', {d.get('credit_before') or 'null'})
          on conflict (id) do nothing""")
    q(f"update subproblem set status='running', updated_at=now() where id={sql_lit(sid)}")
    print(f"dispatched {sid:>4}  {account:<13} {d['session_id']}")
    return d["session_id"]


def poll(project):
    rows = q(f"""select id, account, subproblem_id from agent_session
                 where project_id={sql_lit(project)} and status in ('running','working')""")
    for sess, account, sid in rows:
        r = subprocess.run(["orchestra", "cloud", "status", "--account", account, "--session", sess],
                           capture_output=True, text=True, timeout=180)
        try:
            d = json.loads(r.stdout)
        except Exception:
            continue
        # `session_status` is the raw state; `status_bucket` is the one that says whether it FINISHED.
        # A finished session reports session_status 'idle' with status_bucket 'completed' -- reading the raw
        # field alone leaves every done session looking like it is still working, and the loop never refills.
        bucket = d.get("status_bucket") or ""
        st = "completed" if bucket == "completed" else (d.get("session_status") or "")
        cost = d.get("cost_usd")
        q(f"""update agent_session set status={sql_lit(st)}, model={sql_lit(d.get('model') or '')},
              branch={sql_lit(d.get('branch') or '')}, cost_usd={cost if cost is not None else 'null'},
              result={sql_lit((d.get('result') or '')[:4000])},
              finished_at = case when {sql_lit(st)} in ('completed','failed','stopped') then now() else null end
              where id={sql_lit(sess)}""")
        # 'idle' is how a finished cloud session reports itself; status_bucket 'completed' is the
        # authoritative signal. Rows written before that mapping existed sat in `running` forever
        # with a dead session behind them, silently blocking every dependent -- S15, the minimal
        # edit stack and the project's key genetic deliverable, was held for three hours by one.
        if st in ("completed", "idle") and sid and not d.get("is_error"):
            q(f"update subproblem set status='answered', updated_at=now() where id={sql_lit(sid)} and status='running'")
        elif st in ("failed", "stopped") and sid:
            q(f"update subproblem set status='open', updated_at=now() where id={sql_lit(sid)} and status='running'")
        print(f"  {sid or '-':>4} {account:<13} {st:<10} cost={cost}")


def status(project):
    print("== subproblem frontier ==")
    for r in q(f"""select s.ord, sp.status, count(*) from subproblem sp join scale s on s.id=sp.scale_id
                   where sp.project_id={sql_lit(project)} group by 1,2 order by 1,2"""):
        pass
    for r in q(f"""select sp.status, count(*) from subproblem sp
                   where sp.project_id={sql_lit(project)} group by 1 order by 1"""):
        print(f"  {r[0]:<10} {r[1]}")
    print("== sessions ==")
    for r in q(f"""select status, count(*), coalesce(sum(cost_usd),0) from agent_session
                   where project_id={sql_lit(project)} group by 1 order by 1"""):
        print(f"  {r[0]:<12} n={r[1]:<3} cost=${float(r[2]):.2f}")
    print("== cloud credit ==")
    for a, c in accounts_with_credit():
        print(f"  {a:<13} ${c:.2f}")


def loop(project, max_concurrent=8):
    """One pass: poll what is running, then fill every free slot with a ready subproblem."""
    poll(project)
    running = int(q(f"""select count(*) from agent_session where project_id={sql_lit(project)}
                        and status in ('running','working')""")[0][0])
    ready = ready_subproblems(project)
    accts = accounts_with_credit()
    if not accts:
        print("no account has unexpired cloud credit; not dispatching")
        return
    i = 0
    for row in ready:
        if running >= max_concurrent:
            break
        acct = accts[i % len(accts)][0]
        i += 1
        try:
            dispatch(project, row[0], acct)
            running += 1
        except SystemExit as e:
            print(e)


# ---------------------------------------------------------------------------------------------------
# Adversarial arm. A design that only ever gets elaborated drifts into wishful thinking; the swarm needs
# something whose JOB is to break the headline claim. A challenge is dispatched against a specific claim,
# told what would count as refuting it, and its verdict is recorded whether or not the claim survives.
# Crucially the challenger is NOT told to find a problem -- it is told to try, and to report honestly if
# the claim holds. An agent rewarded for finding faults will manufacture them.

CHALLENGE_PROMPT = """ADVERSARIAL REVIEW. You are not the author of this claim and you are not here to agree with it.

THE CLAIM UNDER ATTACK:
  "{statement}"
  evidence level as recorded: {evidence}
  value: {value} {units}
  source: {source}

PROJECT CONTEXT. {goal}

YOUR JOB. Try hard to break it. Specifically:
  1. Is the arithmetic right? Redo it independently from the stated inputs. Do not copy the author's working.
  2. Is the INPUT data right? The author may have used a proxy quantity for the one that matters
     (for instance a sustained swimming speed where a burst speed is required). Name any such substitution
     and find the correct quantity if it exists.
  3. Is a hidden assumption doing the work? Name it and test what happens when it is relaxed.
  4. Is there a regime, mechanism or published counter-example the author missed?
  5. Is the claim's EVIDENCE LEVEL honest? A derived number presented as measured is a defect even when the
     number is right.

{honesty}

THE RULE THAT MATTERS MOST: if after genuinely trying you cannot break the claim, SAY SO. A challenge that
manufactures a fault is worse than no challenge, because it will be believed. Report `survived` with your
reasoning. Your value is in the honest verdict, not in the body count.

DELIVERABLE. Write `{RESEARCH_DIR}/challenge-{cid}.md` on a new branch and commit it, ending with:

```swarm-challenge
{{"claim_id": {cid}, "outcome": "<survived|refuted|weakened>", "reason": "<one sentence>",
  "corrected_value": "<the value you believe is right, with units, or null>"}}
```
"""


def challenge(project, claim_id, account, workdir="/data/worktrees/delphi-frontier/foundation"):
    # flat() on every free-text column: dbq.q() splits on line boundaries, so a multi-line
    # statement or source silently becomes several rows and row[0] holds only the first line.
    row = q(f"""select replace(replace(statement, chr(10), ' '), chr(1), ' '),
                       evidence, coalesce(value_num::text,'n/a'), coalesce(units,''),
                       replace(replace(coalesce(source,''), chr(10), ' '), chr(1), ' ')
                from claim where id={claim_id}""")
    if not row:
        raise SystemExit(f"no claim {claim_id}")
    st, ev, val, un, src = row[0]
    goal = q(f"select goal from project where id={sql_lit(project)}")[0][0]
    prompt = CHALLENGE_PROMPT.format(statement=st, evidence=ev, value=val, units=un, source=src,
                                     goal=goal, honesty=HONESTY, cid=claim_id)
    r = subprocess.run(["orchestra", "cloud", "start", "--account", account, "--dir", workdir,
                        "--prompt", prompt], capture_output=True, text=True, timeout=300)
    d = json.loads(r.stdout)
    q(f"""insert into challenge (claim_id, challenger, attack, outcome)
          values ({claim_id}, {sql_lit(d['session_id'])}, 'adversarial cloud review', 'not-run')""")
    q(f"""insert into agent_session (id, project_id, harness, account, status)
          values ({sql_lit(d['session_id'])}, {sql_lit(project)}, 'cloud', {sql_lit(account)}, 'running')
          on conflict (id) do nothing""")
    print(f"challenged claim {claim_id} on {account}: {d['session_id']}")
    return d["session_id"]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    if cmd == "status":
        status(proj)
    elif cmd == "poll":
        poll(proj)
    elif cmd == "ready":
        for r in ready_subproblems(proj):
            print(r[0], r[1], r[2][:70])
    elif cmd == "loop":
        loop(proj, int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    elif cmd == "dispatch":
        dispatch(proj, sys.argv[2], sys.argv[3])
    elif cmd == "challenge":
        challenge(proj, int(sys.argv[2]), sys.argv[3])
    else:
        raise SystemExit(f"unknown command {cmd}")
