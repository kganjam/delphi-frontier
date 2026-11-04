#!/usr/bin/env python3
"""Pull the machine-readable result blocks out of claude/* branches and into the graph.

The audit that prompted this: 92 sessions costing $86.82 produced a recorded claim or challenge,
while 50 sessions costing $97.09 were assigned work and recorded NOTHING. That second bucket is not
waste -- the work was done and committed -- it is simply unread. More than half the money spent on
useful work is sitting on branches nobody has opened.

This does the mechanical half: find the blocks, parse them, record them. It does NOT do the
judgement half. Every row lands with `needs_verification` set, because an agent asserting a number
is not evidence that the number is right -- two numbers have already been wrong tonight in ways only
recomputation caught (a thick-airfoil CL_max in the wrong Reynolds regime, and a 40 mm ray compared
to a 120 mm requirement without scaling).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

REPO = "/data/worktrees/delphi-frontier/foundation"
SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm", "-tAq", "-F", SEP]
BASE = "origin/work/frontier-foundation"
BLOCK = re.compile(r"```swarm-(result|challenge|replication|entail)\s*\n(.*?)\n```", re.S)


PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")


def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql):
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [l.split(SEP) for l in r.stdout.strip().split("\n") if l]


def lit(s):
    return "'" + str(s).replace("'", "''") + "'"


def git(*a, timeout=90):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True,
                          timeout=timeout).stdout


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    subprocess.run(["git", "-C", REPO, "fetch", "-q", "origin"], timeout=180)
    done = {r[0] for r in q("select ref from work_log where kind='harvested'")}
    branches = [b.strip() for b in git("branch", "-r", "--sort=-committerdate").split("\n")
                if "origin/claude/" in b][:limit * 3]

    found = recorded = edges = 0
    unresolved_deps = []
    for b in branches:
        tag = f"harvest:{b.split('/')[-1]}"
        if b in done:
            continue
        files = [f for f in git("diff", "--name-only", f"{BASE}...{b}").split("\n")
                 if f.endswith(".md")]
        for f in files[:3]:
            text = git("show", f"{b}:{f}")
            for kind, body in BLOCK.findall(text):
                found += 1
                try:
                    d = json.loads(body)
                except json.JSONDecodeError:
                    continue
                if kind == "result":
                    sid = str(d.get("subproblem") or "")[:40]
                    ans = str(d.get("answer") or "")[:1400]
                    ev = str(d.get("evidence") or "unknown")
                    # The evidence vocabulary is closed. An agent writing "low: calculation on a
                    # proxy" is being honest, but it is not a level -- map it and keep the original
                    # words in the statement so nothing is lost.
                    lvl = next((x for x in ("measured", "simulated", "derived", "literature",
                                            "assumed", "refused", "unknown") if x in ev.lower()),
                               "unknown")
                    key = str(d.get("key_number") or "")[:260]
                    verdict = str(d.get("verdict") or "")
                    stmt = (f"[{sid}] {ans}" + (f" KEY: {key}" if key else "")
                            + (f" VERDICT: {verdict}" if verdict else "")
                            + (f" [agent evidence note: {ev[:160]}]" if lvl == "unknown" and ev else ""))
                    q(f"""insert into claim (project_id, subproblem_id, statement, evidence, source)
                          select {lit(PROJECT)},
                                 (select id from subproblem where id={lit(sid)}),
                                 {lit(stmt)}, {lit(lvl)}, {lit(tag)}
                          where not exists (select 1 from claim where source={lit(tag)}
                                            and statement={lit(stmt)})""")
                    # SET answer_kind ON THE SUBPROBLEM. The harvester has always known the
                    # evidence level -- it is parsed two lines above -- and simply never wrote it
                    # to the subproblem, so 75 of 86 `answered` rows carried a null answer_kind
                    # while SPEC-subproblem-lifecycle rule 1 forbids exactly that and claims to be
                    # "enforced in code". It was not enforced anywhere.
                    # `answer_kind` and `evidence` draw on the same vocabulary, minus 'unknown':
                    # an unclassifiable level stays NULL rather than being coerced, because a
                    # wrong kind is worse than a missing one.
                    if sid and lvl in ("measured", "simulated", "derived", "literature"):
                        q(f"""update subproblem set answer_kind={lit(lvl)}, updated_at=now()
                              where id={lit(sid)} and answer_kind is null""")
                    # A literature claim needs a read_level (SPEC-ASK rule 2). The agent now
                    # reports it; when it does not, the row is left null and the checker flags it.
                    rl = str(d.get("read_level") or "").strip().lower()
                    if lvl == "literature" and rl in ("full-text", "abstract", "listing",
                                                      "search-summary", "could-not-access"):
                        q(f"""update claim set read_level={lit(rl)} where source={lit(tag)}
                              and statement={lit(stmt)} and read_level is null""")
                    # STORE depends_on. The generator prompt has demanded this field in four
                    # places, with the warning that "an omitted edge means your conclusion keeps
                    # standing on a premise that has been withdrawn, and nothing will notice".
                    # Agents have been supplying it. NOTHING EVER PARSED IT, and nothing has ever
                    # written claim_depends -- 6 edges exist across 330 claims, all three of the
                    # original ones wired by hand. So the supersession trigger fires, walks an
                    # empty graph and flags nothing, and 29 of 35 superseded claims produced no
                    # review flag. The warning described what was happening; the edges were not
                    # omitted by agents, they were discarded here.
                    #
                    # depends_on is FREE TEXT and the column is an FK to claim.id, so only
                    # explicit claim references can become edges. Everything else is counted and
                    # reported rather than dropped quietly -- an unresolvable premise is still a
                    # premise, and silently losing it is the defect this field exists to prevent.
                    dep = d.get("depends_on") or []
                    if sid and isinstance(dep, list):
                        new_id = q(f"""select id from claim where source={lit(tag)}
                                       and statement={lit(stmt)} limit 1""")
                        if new_id:
                            cid_new = int(new_id[0][0])
                            for item in dep[:12]:
                                txt = str(item)[:300]
                                m = re.search(r"(?:claim|#)\s*(\d{1,6})", txt, re.I) \
                                    or re.fullmatch(r"\s*(\d{1,6})\s*", txt)
                                if not m:
                                    unresolved_deps.append(txt[:60]); continue
                                tgt = int(m.group(1))
                                if tgt == cid_new:
                                    continue
                                ok = q(f"select 1 from claim where id={tgt}")
                                if not ok:
                                    unresolved_deps.append(txt[:60]); continue
                                q(f"""insert into claim_depends (claim_id, depends_on, how)
                                      values ({cid_new}, {tgt}, {lit(txt)})
                                      on conflict do nothing""")
                                edges += 1
                    recorded += 1
                elif kind == "entail":
                    # Cross-scale constraints. The vocabulary is CLOSED by a CHECK constraint on
                    # both columns, so an out-of-vocabulary kind or status would abort the whole
                    # harvest with a FK/CHECK error rather than skip one row. Filter here.
                    KINDS = ("existence", "range", "timescale", "spatial", "energetic",
                             "conservation")
                    STATUS = ("open", "satisfied", "unsatisfied", "unsatisfiable", "assumed")
                    EV = ("measured", "simulated", "derived", "literature", "assumed", "unknown")
                    SCALES = ("dna", "protein", "cell", "tissue", "organ", "organism",
                              "behaviour", "ecology")
                    src = d.get("source_claim")
                    ssc = str(d.get("source_scale") or "")
                    for c in (d.get("constraints") or [])[:8]:
                        k = str(c.get("kind") or "").strip().lower()
                        st = str(c.get("status") or "open").strip().lower()
                        ts = str(c.get("target_scale") or "").strip().lower()
                        if k not in KINDS or st not in STATUS or ts not in SCALES:
                            continue
                        ev2 = str(c.get("satisfied_evidence") or "").strip().lower()
                        ev2 = ev2 if ev2 in EV else None
                        def num(x):
                            try:
                                v = float(x)
                                return "null" if v != v or v in (float("inf"), float("-inf")) else repr(v)
                            except (TypeError, ValueError):
                                return "null"
                        stmt2 = str(c.get("statement") or "")[:900]
                        if not stmt2:
                            continue
                        q(f"""insert into constraint_entailed (project_id, source_claim,
                                 source_scale, target_scale, kind, statement, quantity, lo, hi,
                                 units, status, satisfied_by, satisfied_evidence, note)
                              select {lit(PROJECT)},
                                 {int(src) if str(src).isdigit() else 'null'},
                                 {lit(ssc) if ssc in SCALES else 'null'}, {lit(ts)}, {lit(k)},
                                 {lit(stmt2)}, {lit(str(c.get('quantity') or '')[:200]) if c.get('quantity') else 'null'},
                                 {num(c.get('lo'))}, {num(c.get('hi'))},
                                 {lit(str(c.get('units') or '')[:60]) if c.get('units') else 'null'},
                                 {lit(st)},
                                 {lit(str(c.get('satisfied_by') or '')[:900]) if c.get('satisfied_by') else 'null'},
                                 {lit(ev2) if ev2 else 'null'},
                                 {lit((str(c.get('note') or '')[:900]) + f' [{tag}]')}
                              where not exists (select 1 from constraint_entailed
                                                where source_claim is not distinct from
                                                      {int(src) if str(src).isdigit() else 'null'}
                                                and statement={lit(stmt2)})""")
                        recorded += 1
                elif kind == "challenge":
                    cid = d.get("claim_id")
                    out = str(d.get("outcome") or "")
                    if cid and out in ("survived", "refuted", "weakened"):
                        q(f"""update challenge set outcome={lit(out)},
                                 evidence={lit(str(d.get('reason') or '')[:900])}
                               where claim_id={int(cid)} and (outcome is null or outcome='not-run')""")
                        recorded += 1
        # Bookkeeping goes in work_log, NOT in claim. It went in claim twice tonight -- LAWENTRY
        # dispatch markers, then HARVESTED branch markers introduced twenty minutes after the first
        # batch was deleted -- because deleting the rows fixed the symptom and left the need with
        # nowhere to go. `claim` is for assertions about the world.
        q(f"""insert into work_log (project_id, kind, ref, detail)
              values ({lit(PROJECT)},'harvested',{lit(b)},{lit(tag)})
              on conflict do nothing""")
    print(f"  branches scanned: {len(branches)}  blocks found: {found}  recorded: {recorded}")
    print(f"  dependency edges written: {edges}   unresolvable depends_on entries: "
          f"{len(unresolved_deps)}")
    if unresolved_deps:
        print("  (free-text premises that name no claim id; reported, not dropped silently)")
        for u in unresolved_deps[:5]:
            print(f"    - {u}")
    print("  every row lands UNVERIFIED: an agent asserting a number is not evidence it is right")
    return 0


if __name__ == "__main__":
    sys.exit(main())
