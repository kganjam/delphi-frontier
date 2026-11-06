#!/usr/bin/env python3
"""Trace a connected chain of entailments across the scales, DNA to behaviour and back.

The goal asks to show the project "going from all scales back down to DNA". The cross-scale
edges exist -- `constraint_entailed` holds 381 for zebrafish-flight, spanning all eight scales --
but nothing has ever walked them end to end, so nobody can tell a CONNECTED chain from a pile of
edges that merely happen to mention every scale.

THE DISTINCTION THIS ENFORCES, which is the whole point. An entailment's `status` says whether
the constraint it imposes has been SATISFIED by evidence. A path through satisfied edges is a
chain the project has demonstrated. A path through open edges is a chain the project has
PROPOSED. They look identical in a diagram and they are not the same claim, so this prints them
separately and never merges the counts.

It also refuses to invent connectivity: an edge joins two scales, and a CHAIN requires that the
claim entailed at one step is the claim that sources the next. Where that link is absent the
chain is reported as scale-connected only, and said so.
"""
from __future__ import annotations

import collections
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env, flat  # noqa: E402

ORDER = ["dna", "protein", "cell", "tissue", "organ", "organism", "behaviour", "ecology"]


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.strip().split("\n") if ln]


def edges(proj: str, satisfied_only: bool):
    cond = "and status = 'satisfied'" if satisfied_only else ""
    rows = q(f"select source_scale, target_scale, id::text, coalesce(source_claim::text,''), "
             f"{flat('statement', 150)}, coalesce(status,'') "
             f"from constraint_entailed where project_id = '{proj}' "
             f"and source_scale is not null and target_scale is not null {cond}")
    g = collections.defaultdict(list)
    for r in rows:
        if len(r) >= 6:
            g[r[0]].append(r)
    return g


def walk(g, start: str) -> list:
    """Greedy forward walk along ORDER, taking one edge per scale step."""
    chain, seen = [], {start}
    cur = start
    while True:
        nxt = None
        for cand in ORDER[ORDER.index(cur) + 1:] if cur in ORDER else []:
            hit = [e for e in g.get(cur, []) if e[1] == cand]
            if hit:
                nxt = hit[0]
                break
        if not nxt or nxt[1] in seen:
            return chain
        chain.append(nxt)
        seen.add(nxt[1])
        cur = nxt[1]


def report(proj: str, satisfied_only: bool) -> int:
    label = "SATISFIED (demonstrated)" if satisfied_only else "ANY STATUS (proposed)"
    g = edges(proj, satisfied_only)
    chain = walk(g, "dna")
    span = ["dna"] + [e[1] for e in chain]
    print(f"\n  === {label} ===")
    print(f"  chain: {' -> '.join(span)}   ({len(chain)} steps of {len(ORDER)-1} possible)")
    for e in chain:
        src, tgt, eid, claim, stmt, status = e[:6]
        print(f"    {src:>9} -> {tgt:<9} entailment {eid:>4}  claim {claim or '-':>5}  [{status}]")
        print(f"              {stmt[:96]}")
    return len(chain)


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    print(f"  project {proj}; scale order {' -> '.join(ORDER)}")
    n_dem = report(proj, True)
    n_pro = report(proj, False)
    print(f"\n  DEMONSTRATED chain reaches {n_dem+1} of {len(ORDER)} scales; "
          f"PROPOSED chain reaches {n_pro+1}.")
    print("  These are different claims and are not merged. A proposed chain is a plan.")
    print("\n  NOT established by this walk: that the claim entailed at one step is the claim")
    print("  sourcing the next. This is SCALE connectivity, which is weaker than causal")
    print("  connectivity, and the difference is not cosmetic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
