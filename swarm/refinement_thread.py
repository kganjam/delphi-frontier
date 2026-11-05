#!/usr/bin/env python3
"""Trace a DESIGN QUESTION through every round that corrected it -- the refinement process.

show_refinement_loop.py renders one attack-and-answer pair, and --chains walks supersession.
Neither shows what the goal asks for: a question pursued across rounds where each round acts on
the last, including rounds that WEAKEN rather than replace. Most corrections in this project are
not supersessions -- a claim qualifies, restricts the scope of, or predicts-and-fails-against an
earlier one while both stay live. Supersession misses all of those.

THIS FOLLOWS EXPLICIT REFERENCES. A claim that says "claim 1083" is acting on claim 1083, and the
verb it uses says how. The thread is therefore read from what the claims assert about each other,
not from a status column.

HONEST LIMIT: the verbs are matched from a fixed list and a claim may act on another without
using one of them, so a thread is a LOWER BOUND on the refinement that happened.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env, flat  # noqa: E402

#: How one claim can act on another, strongest first. Order matters: the first match wins.
VERBS = [
    ("REFUTES", r"\bREFUTES?\b|\bDOES NOT SURVIVE\b|\bIS WRONG\b|\bNOT SUPPORTED\b"),
    ("CORRECTS", r"\bCORRECTS?\b|\bCORRECTION TO\b|\bOVERTURNS?\b"),
    ("SUPERSEDES", r"\bSUPERSEDES\b"),
    ("QUALIFIES", r"\bQUALIFIES\b|\bRESTRICTS?\b|\bLIMITS\b|\bWEAKENS?\b"),
    ("CONFIRMS", r"\bCONFIRMS?\b|\bSTRENGTHENS?\b|\bUPHELD\b"),
    ("EXTENDS", r"\bEXTENDS?\b|\bREFINES?\b|\bCLOSES\b|\bANSWERS\b"),
]
REF = re.compile(r"\bclaims?\s+(\d{3,4})", re.I)


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.strip().split("\n") if ln]


def verb_for(stmt: str) -> str:
    head = stmt[:320]
    for name, pat in VERBS:
        if re.search(pat, head, re.I):
            return name
    return "builds on"


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    seed = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1079
    rows = q(f"""select id::text, {flat('statement', 2600)} from claim
                 where project_id = '{proj}' order by id""")
    text = {r[0]: r[1] for r in rows if len(r) > 1}

    # forward edges: a claim naming an earlier one is acting on it
    acts_on: dict[str, list[tuple[str, str]]] = {}
    for cid, stmt in text.items():
        for ref in set(REF.findall(stmt)):
            if ref in text and int(ref) < int(cid):
                acts_on.setdefault(ref, []).append((cid, verb_for(stmt)))

    print(f"  REFINEMENT THREAD from claim {seed}\n")
    seen, frontier, depth = set(), [str(seed)], 0
    while frontier and depth < 9:
        nxt = []
        for cid in frontier:
            if cid in seen:
                continue
            seen.add(cid)
            stmt = text.get(cid, "")
            title = stmt.split("]")[0].lstrip("[")[:88] if stmt.startswith("[") else stmt[:88]
            print(f"  {'  ' * depth}claim {cid}: {title}")
            for child, verb in sorted(acts_on.get(cid, []), key=lambda x: int(x[0]))[:3]:
                print(f"  {'  ' * depth}   `-- {verb} -> {child}")
                nxt.append(child)
        frontier = nxt
        depth += 1
    print(f"\n  {len(seen)} claims in the thread, {depth} rounds deep.")
    print("  Each arrow is one claim ASSERTING something about an earlier one, read from the")
    print("  statement rather than from a status column -- so rounds that QUALIFY or REFUTE")
    print("  without superseding are included, and those are most of them.")
    print("  LOWER BOUND: a claim may act on another without using one of the matched verbs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
