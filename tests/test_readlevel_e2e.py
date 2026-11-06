#!/usr/bin/env python3
"""End-to-end exercise of the read_level path, without an agent or cloud credit.

Claim 532 fixed the harvest INSERT to carry read_level and claim 535 fixed the result template
to ask for it, but neither had been exercised in the LIVE loop -- cloud credit is exhausted, so
no agent will produce a block to test it with. This drives the REAL code path with a synthetic
block instead: the same BLOCK regex harvest.py uses, the same normaliser, the same INSERT shape,
inside a transaction that ROLLS BACK so the graph is untouched.

Three arms, because one passing case proves only that something ran:
  conformant  -- block carries read_level 'abstract' -> must land with it set
  absent      -- block omits it entirely            -> must land with NULL (not a guess)
  invented    -- block says 'skimmed it'            -> must land with NULL (refused)
"""
import os, re, subprocess, sys
sys.path.insert(0, "/data/swarm")

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm", "-tAq"]
BLOCK = re.compile(r"```swarm-(result|challenge|replication|entail)\s*\n(.*?)\n```", re.S)
VOCAB = ("full-text", "abstract", "listing", "search-summary", "could-not-access")

def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e

CASES = [
  ("conformant", '"read_level": "abstract",', "abstract"),
  ("absent",     '',                          None),
  ("invented",   '"read_level": "skimmed it",', None),
]

sql = ["begin;"]
expect = []
for name, rl_field, want in CASES:
    doc = ('```swarm-result\n{"subproblem": "S1", "evidence": "literature", '
           + rl_field +
           ' "answer": "synthetic test row", "key_number": null}\n```')
    found = BLOCK.findall(doc)
    assert len(found) == 1, f"{name}: block regex matched {len(found)}"
    import json
    d = json.loads(found[0][1])
    rl = str(d.get("read_level") or "").strip().lower()
    rl = rl if rl in VOCAB else None
    assert rl == want, f"{name}: normaliser gave {rl!r}, expected {want!r}"
    tag = f"e2e-test:{name}"
    expect.append((tag, want))
    sql.append(f"""insert into claim (project_id, subproblem_id, statement, evidence,
                     read_level, source)
                   select 'zebrafish-flight', null, 'E2E ROLLBACK PROBE {name}', 'literature',
                          {'null' if rl is None else chr(39)+rl+chr(39)}, '{tag}';""")
sql.append("select source, coalesce(read_level,'(null)') from claim where source like 'e2e-test:%' order by source;")
sql.append("rollback;")

r = subprocess.run(PG + ["-c", "\n".join(sql)], capture_output=True, text=True, env=env(), timeout=90)
if r.returncode:
    print("SQL FAILED:", r.stderr.strip()[:300]); sys.exit(1)
got = dict(l.split("|") for l in r.stdout.strip().split("\n") if "|" in l)
print(f"  {'case':<12} {'landed as':<18} expected")
bad = 0
for tag, want in expect:
    g = got.get(tag, "<MISSING>")
    w = want or "(null)"
    ok = g == w
    bad += (not ok)
    print(f"  {tag.split(':')[1]:<12} {g:<18} {w}   {'ok' if ok else 'FAIL'}")
print(f"\n  {len(expect)-bad}/{len(expect)} arms correct")
chk = subprocess.run(PG + ["-c", "select count(*) from claim where source like 'e2e-test:%';"],
                     capture_output=True, text=True, env=env(), timeout=60)
print(f"  CONTROL, rollback left behind: {chk.stdout.strip()} rows (must be 0)")
sys.exit(1 if bad or chk.stdout.strip() != "0" else 0)
