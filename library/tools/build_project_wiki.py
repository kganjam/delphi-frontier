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
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


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
            "- [Parameters](parameters.md) — every number with its provenance and assumptions",
            "- [Subproblem board](board.md) — every question as an issue, with a dependency graph",
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


def parameters():
    """A page per parameter: where the number came from, what it rests on, and what it assumes.

    A simulation parameter is not a number, it is a posterior. The page shows the derivation route,
    the DAG of parent estimates, and the STRUCTURAL assumptions separately from the value --
    because "this process follows law L" can be wrong in ways no parameter refinement reveals.
    """
    ps = q(f"""select id, symbol, name, description, coalesce(units,''), coalesce(point::text,''),
                      coalesce(lo::text,''), coalesce(hi::text,''), coalesce(interval_kind,''),
                      derivation, how, coalesce(conditions,''), coalesce(source,''), coalesce(read_level,'')
               from parameter where project_id='{PROJECT}' and superseded_by is null order by id""")
    deps = q("select parameter_id, depends_on, relation, coalesce(sensitivity,'') from parameter_depends")
    sas = q("""select ps.parameter_id, sa.id, replace(replace(sa.statement, chr(10), ' '), chr(1), ' '), sa.evidence, coalesce(sa.alternatives,''),
                      sa.consequence_if_wrong
                 from parameter_structural ps join structural_assumption sa on sa.id=ps.assumption_id""")
    DER = {"measured": "🟢 measured", "derived": "🟡 derived", "fitted": "🟡 fitted",
           "borrowed": "🔵 borrowed from another system", "assumed": "🟠 assumed", "unknown": "⚪ unknown"}
    out = ["---\ntitle: Parameters\n---\n",
           "Every simulation parameter with its provenance. A parameter is a **posterior**, not a "
           "number: the route that produced it, the estimates it rests on, and the structural "
           "assumptions that license it are all part of the value.\n",
           "## The dependency graph\n", "```{mermaid}", "graph TD"]
    for pid, sym, *_ in ps:
        out.append(f'  {pid}["{sym}"]')
    for a, b, rel, _s in deps:
        out.append(f'  {b} -->|{rel}| {a}')
    out += ["```\n", "*An arrow runs from an input to the estimate that uses it.*\n"]
    for pid, sym, name, desc, un, pt, lo, hi, ik, der, how, cond, src, rl in ps:
        out += [f"## `{sym}` — {name}\n", f"{desc}\n",
                "| | |", "|---|---|",
                f"| Value | **{pt} {un}**" + (f" (range {lo}–{hi}, *{ik}*)" if lo else " — **no interval**") + " |",
                f"| Derivation | {DER.get(der, der)} |",
                f"| How | {esc(how)} |",
                f"| Conditions | {esc(cond) or '**not stated**'} |",
                f"| Source | {esc(src)}" + (f" *[{rl}]*" if rl else "") + " |", ""]
        d = [x for x in deps if x[0] == pid]
        if d:
            out.append("**Rests on:**\n")
            out += [f"- `{b}` ({rel}) — {esc(sv)}" for _a, b, rel, sv in d] + [""]
        sa = [x for x in sas if x[0] == pid]
        for _p, sid, st, ev, alt, cons in sa:
            out += [f":::{{warning}} Structural assumption: {esc(st)}",
                    f"**Evidence:** {ev}. **Alternatives:** {esc(alt) or 'none stated'}.",
                    f"**If wrong:** {esc(cons)}", ":::", ""]
    return "\n".join(out)


def board():
    """A GitHub-issues-style board plus a Mermaid dependency graph.

    The table alone cannot show what a subproblem is BLOCKED ON, and that is the question anyone
    picking up work actually asks. The graph shows the dependency edges; the board shows state.
    """
    rows = q(f"""select sp.id, coalesce(sp.scale_id,''), sp.status, sp.question,
                        coalesce(sp.answer_kind,''), coalesce(s.ord::text,'9')
                 from subproblem sp left join scale s on s.id=sp.scale_id
                 where sp.project_id='{PROJECT}' order by sp.id""")
    deps = q("select subproblem_id, depends_on from subproblem_dep")
    flags = {r[0] for r in q("select distinct subproblem_id from review_flag where status='open' and subproblem_id is not null")}
    nclaim = {r[0]: int(r[1]) for r in q(f"""select subproblem_id, count(*) from claim
                 where project_id='{PROJECT}' and subproblem_id is not null and superseded_by is null
                 group by 1""")}

    MARK = {"open": "🔵 open", "running": "🟡 running", "answered": "🟢 answered",
            "refuted": "🔴 refuted", "blocked": "⛔ blocked", "superseded": "⚫ superseded"}
    out = ["---\ntitle: Subproblem board\n---\n",
           "Every question as an issue: its state, its scale, how many claims it carries, and "
           "whether anything it depends on has been superseded.\n"]

    # The dependency graph. Only subproblems with an edge are drawn -- a graph of 50 isolated
    # nodes communicates nothing.
    linked = {a for a, b in deps} | {b for a, b in deps}
    if deps:
        out += ["## Dependencies\n", "```{mermaid}", "graph LR"]
        cls = {"answered": "done", "refuted": "ref", "running": "run", "open": "opn"}
        for sid, scale, st, qn, _k, _o in rows:
            if sid in linked:
                out.append(f'  {sid}["{sid}<br/>{scale}"]:::{cls.get(st,"opn")}')
        for a, b in deps:
            out.append(f"  {b} --> {a}")
        out += ["  classDef done fill:#d4f4d4,stroke:#2a7",
                "  classDef ref fill:#f9d4d4,stroke:#a22",
                "  classDef run fill:#fdf2c4,stroke:#aa2",
                "  classDef opn fill:#d4e4f9,stroke:#27a", "```\n",
                "*An arrow runs from a prerequisite to the question it unblocks.*\n"]

    for st in ("open", "running", "answered", "refuted"):
        g = [r for r in rows if r[2] == st]
        if not g:
            continue
        out.append(f"## {MARK.get(st, st)} — {len(g)}\n")
        out.append("| id | scale | claims | blocked on | question |")
        out.append("|---|---|---|---|---|")
        for sid, scale, _s, qn, _k, _o in sorted(g, key=lambda r: (r[5], r[0])):
            on = ", ".join(b for a, b in deps if a == sid) or "—"
            warn = " ⚠️" if sid in flags else ""
            out.append(f"| **{sid}**{warn} | {scale or '—'} | {nclaim.get(sid,0)} | {on} | {esc(qn)[:96]} |")
        out.append("")
    out.append("⚠️ marks a subproblem with an open review flag: something it rests on was superseded.\n")
    return "\n".join(out)


def claims():
    rows = q(f"""select c.id, coalesce(c.subproblem_id,''), coalesce(c.scale_id,''),
                        replace(replace(c.statement, chr(10), ' '), chr(1), ' '),
                        c.evidence, coalesce(c.value_num::text,''), coalesce(c.units,''),
                        replace(replace(coalesce(c.source,''), chr(10), ' '), chr(1), ' '),
                        coalesce(c.read_level,''),
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
    for name, fn in (("index", index), ("frontier", frontier), ("board", board), ("parameters", parameters),
                     ("claims", claims), ("corrections", corrections)):
        (OUT / f"{name}.md").write_text(fn())
        print(f"  wrote {name}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
