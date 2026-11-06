#!/usr/bin/env python3
"""Run every claim in the graph past the GXL evidence API, and record what comes back.

This is an INDEPENDENT check. Our own challenges are agents re-reasoning over the same material;
this queries a separate corpus with a separate engine, so agreement between them is worth something
that agreement among our own agents is not.

The zero is only informative because the engine discriminates: the same endpoint returns 28
supporting passages for "potassium channel mutations regulate fin size in zebrafish" and 0 for the
open constraint we were testing. That control is re-run every pass (--control) rather than assumed,
because a search that silently stops working returns the same zeros as a search that found nothing.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request

API = "https://paperclip.gxl.ai/api/v1/claims/support"
SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm", "-tAq", "-F", SEP]
# A claim we know the corpus supports. If this stops returning supports, the engine is broken and
# every zero in the same pass is meaningless.
CONTROL = "Potassium channel mutations regulate fin size in zebrafish"
CONTROL_MIN = 5
# The five sibling tools (harvest, generate, swarm, check_specs, check_grader_use) all read
# SWARM_PROJECT. This one hardcoded 'zebrafish-flight' INSIDE ITS SQL, so running the pipeline for
# another project would have silently scored the fish's claims against that project's evidence and
# reported a clean pass. A replicable pipeline cannot have one tool that ignores the switch.
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

# The domain whitelist keeps the engine away from claims it cannot judge. It was a FISH TERM LIST
# written into the SQL, which is the same replicability defect as the hardcoded project id and a
# worse one: for a coral or insect project nearly every claim would fail this filter, the query
# would return 0 rows, and the pass would print "0 checked" -- indistinguishable from "checked
# everything and found nothing". A mechanism walking an empty set, in a new place.
DOMAIN_TERMS = os.environ.get(
    "SWARM_DOMAIN_TERMS",
    "zebrafish|danio|fish|fin|muscle|channel|protein|ray|flight|glide|exocoet|actinodin|kcn|"
    "lift|drag|scal")


def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def key():
    for line in open(os.path.expanduser("~/.config/morphoswarm/paperclip.env")):
        if line.startswith("PAPERCLIP_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no PAPERCLIP_API_KEY")


def q(sql):
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [l.split(SEP) for l in r.stdout.strip().split("\n") if l]


def lit(s):
    return "'" + str(s).replace("'", "''") + "'"


def ask(claim, k, top_n=10, timeout=150, tries=4):
    """Query with backoff. The API rate-limits, and an unhandled 429 on the CONTROL call killed a
    whole pass -- the run died before checking a single claim. A rate limit is back-pressure, not a
    failure, and must be distinguished from a claim having no evidence."""
    body = json.dumps({"claim": claim[:1200], "top_n": top_n}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {k}", "Content-Type": "application/json"})
    delay = 5
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == tries - 1:
                raise
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("unreachable")


def main():
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    k = key()

    # The control, every pass. A broken search and an unsupported claim both return zero.
    try:
        c = ask(CONTROL, k)["counts"]
    except Exception as e:
        print(f"  control call failed ({type(e).__name__}) -- the engine is unreachable or rate "
              f"limited. Recording nothing: a pass that cannot run its control produces zeros "
              f"indistinguishable from real absences.")
        return 2
    print(f"  control: {c['supports']} supports (floor {CONTROL_MIN})")
    if c["supports"] < CONTROL_MIN:
        print("  CONTROL FAILED -- the engine is not discriminating. Recording nothing this pass.")
        return 2

    # EXCLUDE claims the engine cannot judge. Two measured limitations:
    #  * It scores the claim text AS GIVEN, so a concessive clause ("NOT collagen-like DESPITE
    #    being termed elastoidin") gets scored as refuting the claim it belongs to. Claim 14 showed
    #    2/6 with the clause and 0/35 without it.
    #  * It is a LITERATURE engine. A claim about our own method or search scope ("the no-homolog
    #    result is scoped to PDB70") has no literature to support or refute, so its verdict is
    #    meaningless and must not be aggregated with the rest.
    rows = q(f"""select c.id, c.statement from claim c
                 where c.project_id={lit(PROJECT)} and c.superseded_by is null
                 and length(c.statement) between 40 and 1200
                 and c.statement !~* '(scope|scoped|could not|we searched|this project|recomputed here|verified here|limitation|was found|does not resolve|positive control|reproduced here|holds [0-9]+ sequences|our own|here from)'
                 and c.statement !~* '(despite|although|notwithstanding)'
                 -- Only WORLD-CLAIMS. Measured on 39 claims: the engine returned 0 supports for
                 -- every claim about our own method, search or computation, because there is no
                 -- literature to support "no measurement was found" or "the a3m holds 76
                 -- sequences". Those zeros are not evidence of anything and must not accumulate.
                 and c.evidence in ('literature','measured','derived')
                 and c.statement ~* {lit('(' + DOMAIN_TERMS + ')')} 
                 and not exists (select 1 from artifact_signal s
                                 where s.entity_type='claim' and s.entity_id=c.id::text
                                 and s.voter_id='gxl-evidence')
                 order by c.id limit {n_max}""")
    # POSITIVE CONTROL ON THE FILTER ITSELF. If the domain whitelist admits nothing while the
    # project has claims, that is a misconfigured filter, not an absence of work -- and the two
    # print the same "0 checked". Refuse rather than report a clean pass over an empty set.
    if not rows:
        total = q(f"select count(*) from claim where project_id={lit(PROJECT)} "
                  f"and superseded_by is null")[0][0]
        if int(total) > 0:
            print(f"  REFUSING: the domain whitelist admitted 0 of {total} live claims for "
                  f"project {PROJECT!r}. Either every claim is already scored, or "
                  f"SWARM_DOMAIN_TERMS does not match this project's vocabulary. Set it to this "
                  f"project's terms. Recording nothing: a filter that excludes everything and a "
                  f"project with nothing to check both print '0 checked'.")
            return 2
        print(f"  project {PROJECT!r} has no live claims at all; nothing to check.")
        return 0

    agree = disagree = 0
    for cid, stmt in rows:
        try:
            d = ask(stmt, k)
        except Exception as e:
            print(f"  claim {cid}: {type(e).__name__}")
            continue
        time.sleep(2)   # pace against the rate limit rather than discovering it
        cc = d.get("counts", {})
        sup, ref, neu = cc.get("supports", 0), cc.get("refutes", 0), cc.get("neutral", 0)
        retr = cc.get("supports_retracted", 0) + cc.get("refutes_retracted", 0)
        # A signal, not a verdict. value is supports minus refutes; weight is the pool size.
        q(f"""insert into artifact_signal (entity_type, entity_id, kind, dimension, voter_id,
                 voter_kind, value, weight, unit, reason, metadata)
              values ('claim', {lit(str(cid))}, 'external-evidence', 'literature-support',
                      'gxl-evidence', 'literature', {sup - ref}, {sup + ref + neu}, 'passages',
                      {lit(f'GXL claims/support: {sup} support, {ref} refute, {neu} neutral'
                            + (f', {retr} RETRACTED' if retr else '')
                            + '. Control passed this pass.')},
                      {lit(json.dumps(cc))})""")
        flag = ""
        if ref > sup and ref > 0:
            disagree += 1
            flag = "  <-- MORE REFUTING THAN SUPPORTING"
        elif sup > 0:
            agree += 1
        if retr:
            flag += f"  [{retr} RETRACTED]"
        print(f"  claim {cid:>4}: {sup:>2} sup / {ref:>2} ref / {neu:>2} neu{flag}")
    print(f"\n  {len(rows)} checked: {agree} with supporting literature, {disagree} where "
          f"refuting evidence outweighs supporting")
    print("  These are SIGNALS, not verdicts: an engine finding no support is not the same as a "
          "claim being false, and our claims are often more specific than any single passage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
