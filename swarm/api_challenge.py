#!/usr/bin/env python3
"""Adversarial challenge of live claims, paid from Claude Console API credit (not cloud sessions).

WHY THIS EXISTS. The four Max CLOUD-SESSION credits were driven to 0.00 and expire tonight. A
SECOND pool was sitting unused: Console API credit, $200 per Max plan, on five tenants. Four are
in scope -- api_outlook, api_outlook1, api_outlook2, api_gmail -- and `api_allen` is EXCLUDED by
the owner's standing instruction and is left disabled. The soonest expiry is 2026-11-07, so this
is spend-it-or-lose-it money that cloud-session tooling cannot reach: Console credit covers the
API, Batch API and Agent SDK, but NOT Claude Code.

WHAT IT DOES. Picks live claims with no challenge recorded, asks a model to attack each one, and
writes the verdict to `challenge`. 847 challenges already exist, so this extends an established
arm rather than inventing one.

THE DESIGN PROBLEM IS CONFIRMATION PRESSURE. A model asked to "find the flaw" finds one every
time, and a challenge arm whose outcome is always `weakened` measures nothing -- the empty-set
failure wearing a verdict. Three defences:

  * the prompt states that SURVIVED is a correct and expected answer, and that inventing a
    weakness is worse than reporting none;
  * the outcome vocabulary is CLOSED (survived / weakened / refuted) and a reply that does not
    name exactly one of them is recorded as `not-run`, never guessed at;
  * the `challenger` field names the model AND the tenant, so a later reader can ask whether one
    model produced all the refutations.

    python3 api_challenge.py <n> [--tenant T] [--write]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
OUTCOMES = ("survived", "weakened", "refuted")
TENANTS = ["api_outlook2", "api_outlook1", "api_outlook", "api_gmail"]   # api_allen EXCLUDED

PROMPT = """You are an adversarial reviewer for a scientific design project. Attack this claim.

CLAIM {cid} (evidence level: {ev}):
{stmt}

Find the strongest specific objection you can. Then judge honestly.

SURVIVED is a correct and expected answer. Many of these claims are careful and state their own
scope; if you cannot find a real objection, say SURVIVED. Inventing a weakness is worse than
reporting none, because a challenge arm whose verdict is always negative measures nothing.

Reply in EXACTLY this form and nothing else. OUTCOME FIRST -- if you run out of room, the
verdict must already be on the page:
OUTCOME: <survived|weakened|refuted>
ATTACK: <one sentence naming the specific weakness, or "none found">
WHY: <two sentences at most>
"""


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def lit(s) -> str:
    return "null" if s is None else "'" + str(s).replace("'", "''") + "'"


FALLBACK = "claude-sonnet-5-5"


def call(tenant: str, prompt: str, max_tokens: int = 1200, model: str | None = None) -> dict:
    args = ["orchestra", "api-credits", "call", "--tenant", tenant,
            "--prompt", prompt, "--max-tokens", str(max_tokens)]
    if model:
        args += ["--model", model]
    r = subprocess.run(args, capture_output=True, text=True, timeout=300)
    i = r.stdout.find("{")
    if i < 0:
        raise RuntimeError((r.stderr or r.stdout)[:300])
    return json.loads(r.stdout[i:])


def call_with_fallback(tenant: str, prompt: str) -> dict:
    """Try the default model; on a refusal, retry on FALLBACK.

    This is the API's OWN documented remedy -- a refusal reply says so in its explanation field:
    "API integrators: you can reduce refusals for your users by configuring a fallback model".
    It is a supported feature, not prompt engineering around a classifier, and the prompt is sent
    UNCHANGED to the fallback.

    It matters because the refusals are not confined to biology. Claim 465 is about an evaluation
    kernel and a claim graph, and was refused with category "bio" -- almost certainly because the
    project's claims quote protein names and variant ids in passing. claude-sonnet-5-5 answered the
    identical prompt, returned `weakened` with a substantive objection, and cost $0.00524 against
    opus's $0.016.
    """
    try:
        return call(tenant, prompt)
    except Exception as e:
        if "refused" not in str(e).lower():
            raise
        out = call(tenant, prompt, model=FALLBACK)
        out["_fallback_from_refusal"] = True
        return out


def parse(text: str) -> tuple[str, str, str]:
    """Closed vocabulary. A reply naming none of the three, or more than one, is NOT guessed at."""
    # LAST match, not first -- a self-correcting reply ("Correction: the verdict should be X")
    # otherwise records the model's discarded first thought. Measured on the recompute arm, which
    # shares this parser shape, and fixed in both.
    atts = re.findall(r"ATTACK:\s*(.+)", text)
    whys = re.findall(r"WHY:\s*(.+)", text)
    outs = re.findall(r"OUTCOME:\s*([a-z-]+)", text, re.I)
    att = type("M", (), {"group": lambda self, _n, v=(atts[-1] if atts else None): v})() if atts else None
    why = type("M", (), {"group": lambda self, _n, v=(whys[-1] if whys else None): v})() if whys else None
    out = (outs[-1].lower() if outs else "")
    if out not in OUTCOMES:
        named = [o for o in OUTCOMES if re.search(rf"\b{o}\b", text, re.I)]
        out = named[0] if len(named) == 1 else "not-run"
    return (att.group(1).strip()[:400] if att else "(no ATTACK line)"), out, \
           (why.group(1).strip()[:900] if why else "")


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
    write = "--write" in sys.argv
    rows = q(f"""select c.id, c.evidence, replace(c.statement, '{SEP}', ' ')
                 from claim c where c.project_id={lit(PROJECT)} and c.superseded_by is null
                 and length(c.statement) between 80 and 6000
                 and not exists (select 1 from challenge ch where ch.claim_id = c.id)
                 order by c.id desc limit {n}""")
    if not rows:
        print("  no unchallenged live claims; nothing to do.")
        return 0
    print(f"  {len(rows)} unchallenged claim(s); tenants {TENANTS} (api_allen EXCLUDED)\n")
    spent = 0.0
    tally: dict[str, int] = {}
    for i, (cid, ev, stmt) in enumerate(rows):
        t = TENANTS[i % len(TENANTS)]
        try:
            r = call_with_fallback(t, PROMPT.format(cid=cid, ev=ev, stmt=stmt[:6000]))
        except Exception as e:
            print(f"  claim {cid:>4} {t:13} CALL FAILED {type(e).__name__}: {str(e)[:90]}")
            continue
        att, out, why = parse(r.get("text", ""))
        # A truncated reply that still carried its OUTCOME is usable; one that did not is a BUDGET
        # failure, not a model judgement, and must say so. Measured on the first batch: 10 of 12
        # verdicts were `not-run` purely because stop_reason was max_tokens at 400 tokens, with the
        # ATTACK line present and the OUTCOME line cut off. Scoring that as "no verdict" spends
        # credit to record nothing and reads as the model declining.
        if r.get("stop_reason") == "max_tokens":
            att = "[reply truncated at max_tokens] " + att
            if out == "not-run":
                out = "not-run"
                why = ("TRUNCATED BEFORE THE VERDICT -- this is a token-budget failure of the "
                       "harness, not a judgement by the model. ") + why
        spent += float(r.get("cost_usd") or 0)
        tally[out] = tally.get(out, 0) + 1
        fb = " FB" if r.get("_fallback_from_refusal") else "   "
        print(f"  claim {cid:>4} {t:13}{fb} {out:9} ${r.get('cost_usd',0):.5f}  {att[:62]}")
        if write:
            who = f"api:{r.get('model','?')}@{t}" + ("  [fallback after a refusal]" if r.get("_fallback_from_refusal") else "")
            q(f"""insert into challenge (claim_id, challenger, attack, outcome, evidence)
                  values ({int(cid)}, {lit(who)}, {lit(att)}, {lit(out)}, {lit(why)})""")
    print(f"\n  outcomes: {tally}")
    print(f"  spent ${spent:.4f} of Console API credit"
          + ("" if write else "  (report only; pass --write to record)"))
    if tally and len(tally) == 1 and "survived" not in tally:
        print("  WARNING: every verdict is the same. A challenge arm with one outcome measures "
              "nothing; check the prompt before trusting these.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
