#!/usr/bin/env python3
"""Recover the dependency edges the harvester discarded before it learned to store them.

The generator has demanded `depends_on` from every agent for most of this project's life. The
harvester never parsed it, so the edges exist in the committed branch files and nowhere else. This
re-reads the branches -- it does NOT re-record claims, which are already present -- and writes only
the edges, matching each block back to the claim row it produced.

Re-runnable: every insert is `on conflict do nothing`.
"""
import json, os, re, subprocess, sys

sys.path.insert(0, "/data/swarm")
from harvest import BASE, REPO, env, git, lit, q, BLOCK   # noqa: E402


def main():
    branches = [b.strip() for b in git("branch", "-r", "--sort=-committerdate").split("\n")
                if "origin/claude/" in b]
    edges = scanned = blocks = 0
    unresolved = []
    for b in branches:
        tag = f"harvest:{b.split('/')[-1]}"
        files = [f for f in git("diff", "--name-only", f"{BASE}...{b}").split("\n")
                 if f.endswith(".md")]
        scanned += 1
        for f in files[:3]:
            try:
                text = git("show", f"{b}:{f}")
            except Exception:
                continue
            for kind, body in BLOCK.findall(text):
                if kind != "result":
                    continue
                try:
                    d = json.loads(body)
                except json.JSONDecodeError:
                    continue
                dep = d.get("depends_on") or []
                if not isinstance(dep, list) or not dep:
                    continue
                blocks += 1
                # Find the claim this block produced. The harvester writes source=tag and a
                # statement built from the block, so match on source plus the answer text.
                ans = str(d.get("answer") or "")[:60].replace("'", "''")
                rows = q(f"""select id from claim where source={lit(tag)}
                             and statement like '%{ans}%' limit 1""")
                if not rows:
                    continue
                cid = int(rows[0][0])
                for item in dep[:12]:
                    txt = str(item)[:300]
                    targets = []
                    # 1. An explicit claim id. Measured share of real agent output: 0.0%.
                    #    Agents write their block BEFORE the harvester assigns a claim id, so they
                    #    cannot name one. The schema asked for something unobtainable.
                    m = (re.search(r"(?:claim|#)\s*(\d{1,6})", txt, re.I)
                         or re.fullmatch(r"\s*(\d{1,6})\s*", txt))
                    if m and q(f"select 1 from claim where id={int(m.group(1))}"):
                        targets = [int(m.group(1))]
                    else:
                        # 2. A SUBPROBLEM id, which is what agents actually write (23.3% of 636
                        #    entries). These ARE resolvable, through claim.subproblem_id -- the
                        #    link existed the whole time and nothing used it. Capped at 4 so one
                        #    broad citation cannot flood the graph.
                        sm = re.match(r"\s*(S\d+(?:-D)*)\b", txt)
                        if sm:
                            rows2 = q(f"""select id from claim where subproblem_id={lit(sm.group(1))}
                                          and superseded_by is null order by id limit 4""")
                            targets = [int(r[0]) for r in rows2]
                    if not targets:
                        unresolved.append(txt[:70]); continue
                    for tgt in targets:
                        if tgt == cid:
                            continue
                        # COUNT ROWS INSERTED, NOT ATTEMPTS. `on conflict do nothing` silently
                        # drops a repeat (claim_id, depends_on) pair, and counting attempts
                        # overstated the first run by 369 against 236 actually stored -- a 56%
                        # overstatement in a number reported as a result.
                        got = q(f"""insert into claim_depends (claim_id, depends_on, how)
                                    values ({cid}, {tgt}, {lit(txt)})
                                    on conflict do nothing returning 1""")
                        if got:
                            edges += 1
    print(f"  branches {scanned}  blocks with depends_on {blocks}  edges written {edges}")
    print(f"  unresolvable (free text naming no claim id): {len(unresolved)}")
    for u in unresolved[:6]:
        print(f"    - {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
