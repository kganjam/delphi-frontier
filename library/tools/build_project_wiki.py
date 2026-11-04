#!/usr/bin/env python3
"""Render the project graph as a wiki: the frontier, the claims, the corrections, the open flags.

All of this work lives in Postgres and is invisible. Ninety claims, thirty subproblems, ten
supersessions and a regime transition are readable only by someone who knows the schema and has the
password — which means in practice nobody reads them, including us.

The design rule, which is the whole reason this is worth writing: **the page shows the evidence
level beside every number, and shows superseded values rather than hiding them.** A wiki that
rendered only current values would be a prettier way to lose the thing that makes this project
different from a pile of plausible assertions.

Generated. Never hand-edit; edit the database, re-run.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm", "-tAq", "-F", SEP]
OUT = Path(__file__).resolve().parent.parent / "pages" / "project"
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

# A reader should be able to see at a glance what is measured and what is assumed.
BADGE = {"measured": "🟢 measured", "simulated": "🟡 simulated", "derived": "🟡 derived",
         "literature": "🔵 literature", "assumed": "🟠 assumed", "refused": "🔴 refused",
         "unknown": "⚪ unknown"}


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
        raise RuntimeError(r.stderr.strip()[:400])
    return [l.split(SEP) for l in r.stdout.strip().split("\n") if l]


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def index():
    goal = q(f"select goal from project where id='{PROJECT}'")[0][0]
    n = {r[0]: int(r[1]) for r in q(f"""
        select 'claims', count(*) from claim where project_id='{PROJECT}' union all
        select 'superseded', count(*) from claim where project_id='{PROJECT}' and superseded_by is not null union all
        select 'sub', count(*) from subproblem where project_id='{PROJECT}' union all
        select 'answered', count(*) from subproblem where project_id='{PROJECT}' and status='answered' union all
        select 'refuted', count(*) from subproblem where project_id='{PROJECT}' and status='refuted' union all
        select 'open', count(*) from subproblem where project_id='{PROJECT}' and status='open' union all
        select 'chal', count(*) from challenge where outcome is not null and outcome<>'not-run' union all
        select 'flags', count(*) from review_flag where status='open'""")}
    ev = q(f"""select evidence, count(*) from claim where project_id='{PROJECT}'
               and superseded_by is null group by 1 order by 2 desc""")
    out = [f"---\ntitle: {PROJECT}\n---\n", f"{goal}\n", "## Where it stands\n",
           "| | |", "|---|---|",
           f"| Claims | {n['claims']} ({n['superseded']} superseded) |",
           f"| Subproblems | {n['sub']} — {n['answered']} answered, {n['refuted']} refuted, {n['open']} open |",
           f"| Challenges resolved | {n['chal']} |",
           f"| Open review flags | {n['flags']} |", "",
           "## What the evidence actually is\n",
           "This table is the point of the project. A claim is only as good as the row it sits in.\n",
           "| Evidence level | Live claims |", "|---|---|"]
    out += [f"| {BADGE.get(e, e)} | {c} |" for e, c in ev]
    out += ["", ":::{note}",
            "Superseded claims are **kept and shown**, not deleted. A correction creates a new row; "
            "the old one stays readable with a pointer to what replaced it.",
            ":::\n",
            "## Pages\n",
            "- [The frontier](frontier.md) — what is open, and what is blocked on what",
            "- [Claims](claims.md) — every claim with its evidence level and source",
            "- [Corrections](corrections.md) — what was superseded, and by what",
            ""]
    return "\n".join(out)


def frontier():
    rows = q(f"""select sp.id, s.ord, sp.scale_id, sp.question, sp.status, coalesce(sp.answer,''),
                        coalesce(sp.answer_kind,'')
                 from subproblem sp left join scale s on s.id=sp.scale_id
                 where sp.project_id='{PROJECT}' order by sp.status, s.ord nulls last, sp.id""")
    out = ["---\ntitle: The frontier\n---\n",
           "Every question this project has opened, with what settled it.\n"]
    for st in ("open", "running", "answered", "refuted"):
        g = [r for r in rows if r[4] == st]
        if not g:
            continue
        out.append(f"## {st} ({len(g)})\n")
        out.append("| id | scale | question | answer |")
        out.append("|---|---|---|---|")
        for sid, _o, scale, qn, _s, ans, kind in g:
            a = esc(ans)[:200] + (f" *({kind})*" if kind else "") if ans else "—"
            out.append(f"| **{sid}** | {scale or '—'} | {esc(qn)[:110]} | {a} |")
        out.append("")
    return "\n".join(out)


def claims():
    rows = q(f"""select c.id, coalesce(c.subproblem_id,''), coalesce(c.scale_id,''), c.statement,
                        c.evidence, coalesce(c.value_num::text,''), coalesce(c.units,''),
                        coalesce(c.source,''), coalesce(c.read_level,''),
                        coalesce(c.superseded_by::text,'')
                 from claim c where c.project_id='{PROJECT}' order by c.id""")
    live = [r for r in rows if not r[9]]
    out = ["---\ntitle: Claims\n---\n",
           f"{len(live)} live claims of {len(rows)} recorded. Superseded rows are on "
           "[Corrections](corrections.md) and are not deleted.\n",
           "| # | sub | claim | evidence | value | source |", "|---|---|---|---|---|---|"]
    for cid, sub, _sc, st, ev, val, un, src, rl, _sup in live:
        v = f"`{val} {un}`".strip() if val else ""
        s = esc(src)[:52] + (f" *[{rl}]*" if rl else "")
        out.append(f"| {cid} | {sub} | {esc(st)[:150]} | {BADGE.get(ev, ev)} | {v} | {s} |")
    return "\n".join(out) + "\n"


def corrections():
    sup = q(f"""select c.id, c.statement, coalesce(c.value_num::text,''), c.superseded_by,
                       coalesce(n.statement,''), coalesce(n.value_num::text,'')
                from claim c left join claim n on n.id=c.superseded_by
               where c.project_id='{PROJECT}' and c.superseded_by is not null order by c.id""")
    fl = q("""select f.id, coalesce(f.subproblem_id,'claim '||f.claim_id), f.triggered_by,
                     f.depth, f.status, f.reason from review_flag f order by f.id""")
    out = ["---\ntitle: Corrections\n---\n",
           "**Nothing here was deleted.** Each row is a value that was replaced, kept beside what "
           "replaced it. This page is the project's error record, and it getting longer is a sign "
           "the system is working rather than failing.\n",
           f"## Superseded ({len(sup)})\n",
           "| was | became | now |", "|---|---|---|"]
    for cid, st, val, nid, nst, nval in sup:
        out.append(f"| **#{cid}** {esc(st)[:110]}{(' `'+val+'`') if val else ''} | → #{nid} | "
                   f"{esc(nst)[:110]}{(' `'+nval+'`') if nval else ''} |")
    out += ["", f"## Open review flags ({len([f for f in fl if f[4]=='open'])})\n",
            "Raised automatically when a claim they depend on was superseded.\n",
            "| affected | triggered by | depth | status |", "|---|---|---|---|"]
    for _i, aff, trig, d, stt, _r in fl:
        out.append(f"| {aff} | claim #{trig} | {d} | {stt} |")
    return "\n".join(out) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("index", index), ("frontier", frontier), ("claims", claims),
                     ("corrections", corrections)):
        (OUT / f"{name}.md").write_text(fn())
        print(f"  wrote {name}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
