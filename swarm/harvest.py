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
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    # A re-sweep for one kind uses its OWN skip list, so re-running it cannot disturb or
    # duplicate what the general harvest already recorded.
    # work_log.kind is a CLOSED vocabulary (check constraint). A one-kind re-sweep needs its
    # own skip list, so it namespaces the free-text REF rather than widening a shared schema.
    wl_kind = "harvested"
    ref_prefix = "" if not only else f"{only}:"
    subprocess.run(["git", "-C", REPO, "fetch", "-q", "origin"], timeout=180)
    done = {r[0] for r in q(f"select ref from work_log where kind='{wl_kind}'"
                            f" and ref like {lit(ref_prefix + '%')}")
            if not ref_prefix or r[0].startswith(ref_prefix)}
    done = {r[len(ref_prefix):] for r in done} if ref_prefix else done
    branches = [b.strip() for b in git("branch", "-r", "--sort=-committerdate").split("\n")
                if "origin/claude/" in b][:limit * 3]

    found = recorded = edges = 0
    dropped_challenges = []
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
                if only and kind != only:
                    continue
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
                    # READ_LEVEL. SPEC-ASK-artifact-graph §2 requires a literature claim to
                    # carry one, and this INSERT did not have the column -- so every literature
                    # claim harvest ever wrote violated that rule by construction (7 of 316 live
                    # rows when this was found, all of them harvest-sourced).
                    #
                    # The gap is two-sided and this fixes only the recording half. The agent
                    # prompt asks for read_level in the DEEPEN template alone (generate.py ~line
                    # 291, "required when your evidence is `literature`"); the general result
                    # template does not, and 0 of 40 branches sampled carried the field. So most
                    # blocks still cannot supply it and those rows stay NULL.
                    #
                    # NULL IS THE HONEST ENCODING FOR "THE BLOCK DID NOT SAY" and the vocabulary
                    # is closed to §5b's five levels, so nothing is invented here: an unrecognised
                    # or absent value becomes NULL rather than a guess. Inferring the level from
                    # the answer's prose is exactly what §5b forbids.
                    rl = str(d.get("read_level") or "").strip().lower()
                    rl = rl if rl in ("full-text", "abstract", "listing", "search-summary",
                                      "could-not-access") else None
                    q(f"""insert into claim (project_id, subproblem_id, statement, evidence,
                                             read_level, source)
                          select {lit(PROJECT)},
                                 (select id from subproblem where id={lit(sid)}),
                                 {lit(stmt)}, {lit(lvl)},
                                 {"null" if rl is None else lit(rl)}, {lit(tag)}
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
                    # AND THE ANSWER ITSELF. `ans` is parsed above and was written only into the
                    # claim, never into the subproblem row -- so 68 of 81 `answered` subproblems
                    # had no answer text, which SPEC-subproblem-lifecycle rule 1 forbids and
                    # claims is "enforced in code". Same shape as the answer_kind and depends_on
                    # bugs: the value is in hand and goes nowhere.
                    if sid and ans:
                        q(f"""update subproblem set answer={lit(ans[:1400])}, updated_at=now()
                              where id={lit(sid)} and coalesce(btrim(answer),'')=''""")
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
                elif kind == "replication":
                    # THE BLOCK TYPE THE REGEX MATCHED AND NOTHING HANDLED. 134 replication blocks
                    # were parsed, counted in `found`, and dropped -- 17 of them independent
                    # re-derivations that DISAGREED with the claim they checked. generate.py calls
                    # this arm "the cheapest hallucination detector there is"; its entire output
                    # went into the void because the dispatch had three branches and four kinds.
                    #
                    # A replication is a SIGNAL about a claim, not a claim: an independent agent
                    # recomputed the number and says whether it reproduces. It goes to
                    # artifact_signal with voter_kind 'agent' -- never pooled with a measurement.
                    cid = d.get("claim_id")
                    agrees = d.get("agrees")
                    if str(cid).isdigit() and agrees is not None and q(
                            f"select 1 from claim where id={int(cid)}"):
                        val = 1 if agrees is True else (-1 if agrees is False else 0)
                        myv = str(d.get("my_value") or "")[:300]
                        note = str(d.get("note") or "")[:900]
                        reason = (f"independent re-derivation {'AGREES' if val > 0 else 'DISAGREES'}"
                                  + (f"; their value: {myv}" if myv else "")
                                  + (f". {note}" if note else ""))
                        q(f"""insert into artifact_signal (entity_type, entity_id, kind, dimension,
                                 voter_id, voter_kind, value, weight, unit, reason, metadata)
                              select 'claim', {lit(str(cid))}, 'replication', 'reproducibility',
                                     {lit(tag)}, 'agent', {val}, 1, 'verdict', {lit(reason[:1400])},
                                     {lit(json.dumps({'my_value': myv, 'agrees': agrees}))}
                              where not exists (select 1 from artifact_signal s
                                                where s.entity_type='claim'
                                                and s.entity_id={lit(str(cid))}
                                                and s.voter_id={lit(tag)}
                                                and s.kind='replication')""")
                        recorded += 1
                elif kind == "challenge":
                    # TWO DEFECTS LIVED HERE AND THE SECOND HID THE FIRST.
                    #
                    # (1) It was an UPDATE and nothing else, gated on
                    #     `outcome is null or outcome='not-run'`. So a challenge landed ONLY if
                    #     somebody had already created an unresolved row for that claim. A
                    #     challenge of a claim with no row, or -- far more common -- a SECOND
                    #     challenge of a claim some earlier arm had already resolved, matched
                    #     zero rows and was discarded. That second case is multi-round
                    #     adversarial review, which is the thing this swarm exists to do:
                    #     an independent agent re-attacking a claim that already survived once
                    #     is the most informative block the fleet produces, and it was the one
                    #     guaranteed to be thrown away. swarm-challenge is also the MOST COMMON
                    #     block kind on the branches -- 28 of 42 in a 45-branch sample.
                    #
                    # (2) `recorded += 1` ran whether or not the UPDATE touched a row, so the
                    #     harvest summary counted every dropped block as recorded. A silent
                    #     drop that increments a success counter is indistinguishable from
                    #     success, which is why this survived 732 branches.
                    #
                    # Now: resolve an outstanding row if there is one, otherwise INSERT a new
                    # challenge. Both paths use RETURNING, and `recorded` counts only real rows.
                    cid = d.get("claim_id")
                    out = str(d.get("outcome") or "")
                    reason = str(d.get("reason") or "")[:900]
                    attack = str(d.get("attack") or d.get("objection") or reason or
                                 "(no attack text in block)")[:900]
                    if (str(cid).isdigit() and out in ("survived", "refuted", "weakened")
                            and q(f"select 1 from claim where id={int(cid)}")):
                        hit = q(f"""update challenge set outcome={lit(out)},
                                       evidence={lit(reason)}
                                     where claim_id={int(cid)}
                                       and (outcome is null or outcome='not-run')
                                     returning id""")
                        if not hit:
                            hit = q(f"""insert into challenge
                                          (claim_id, challenger, attack, outcome, evidence)
                                        select {int(cid)}, {lit(tag)}, {lit(attack)},
                                               {lit(out)}, {lit(reason)}
                                        where not exists (select 1 from challenge
                                                          where claim_id={int(cid)}
                                                            and challenger={lit(tag)})
                                        returning id""")
                        if hit:
                            recorded += 1
                        else:
                            # Distinguish the two reasons, because they mean opposite things:
                            # a duplicate is the idempotency guard WORKING, while a missing
                            # claim is a block that genuinely has nowhere to land.
                            dup = q(f"""select 1 from challenge where claim_id={int(cid)}
                                        and challenger={lit(tag)}""")
                            dropped_challenges.append(
                                f"{b.split('/')[-1]} claim {cid} "
                                + ("(already recorded by this branch -- idempotent, not a loss)"
                                   if dup else "(NO LANDING SPOT -- investigate)"))
        # Bookkeeping goes in work_log, NOT in claim. It went in claim twice tonight -- LAWENTRY
        # dispatch markers, then HARVESTED branch markers introduced twenty minutes after the first
        # batch was deleted -- because deleting the rows fixed the symptom and left the need with
        # nowhere to go. `claim` is for assertions about the world.
        q(f"""insert into work_log (project_id, kind, ref, detail)
              values ({lit(PROJECT)},{lit(wl_kind)},{lit(ref_prefix + b)},{lit(tag)})
              on conflict do nothing""")
    print(f"  branches scanned: {len(branches)}  blocks found: {found}  recorded: {recorded}")
    print(f"  dependency edges written: {edges}   unresolvable depends_on entries: "
          f"{len(unresolved_deps)}")
    if unresolved_deps:
        print("  (free-text premises that name no claim id; reported, not dropped silently)")
        for u in unresolved_deps[:5]:
            print(f"    - {u}")
    if dropped_challenges:
        real = [x for x in dropped_challenges if "NO LANDING SPOT" in x]
        print(f"  challenge blocks not newly recorded: {len(dropped_challenges)}"
              f"  (of which genuine losses: {len(real)}; the rest are idempotent re-runs)")
        for x in dropped_challenges[:5]:
            print(f"    - {x}")
    print("  every row lands UNVERIFIED: an agent asserting a number is not evidence it is right")
    return 0


if __name__ == "__main__":
    sys.exit(main())
