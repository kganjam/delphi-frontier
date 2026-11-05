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

    python3 api_challenge.py <n> [--tenant T] [--panel|--repanel|--no-opus] [--write]

`--tenant T` pins every call to one tenant, for draining the credit that expires first.
Without it the run rotates over all four in scope.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

from dbq import PG, PROJECT, SEP, env, flat, lit, q  # noqa: F401  (re-exported: api_frontier uses ac.q / ac.lit)
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


def call_with_fallback(tenant: str, prompt: str, max_tokens: int = 1200) -> dict:
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
        return call(tenant, prompt, max_tokens=max_tokens)
    except Exception as e:
        if "refused" not in str(e).lower():
            raise
        out = call(tenant, prompt, max_tokens=max_tokens, model=FALLBACK)
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


#: THE PANEL IS CLAUDE-ONLY BY CONSTRUCTION, and agreement between its members is therefore NOT
#: independent confirmation (claim 1117). call() routes through `orchestra api-credits call`,
#: the Anthropic Console API, which reaches Claude models and nothing else; varying --tenant
#: varies the billing account, so the challenger STRING changes while the model does not.
#: Two Claude models share training, alignment and failure modes: an objection both miss is one
#: this panel structurally cannot make, and repeated sampling never reveals it.
#: MEASURED 2026-11-05 (claim 1118), because the line above was asserted before it was checked:
#: opus and sonnet agree on 83.8% of claims they both review (31/37), against a 93.9%
#: within-model self-consistency baseline (62/66). They are PARTIALLY decorrelated, not one
#: viewpoint. And the six divergences are systematic -- opus more lenient, sonnet harsher, every
#: time -- so a single-model panel is biased in a knowable direction.
#: REPORT IT AS "two Claude models agreed", never as "N agents independently converged".
#: A free cross-family panelist exists -- nvidia/nemotron-3.5-super-vl:free, and AGENTS.md 7a
#: permits any model here because the data is public -- but reaching it needs a call path that
#: orchestra does not currently expose. That is the open work.
PANEL = ("claude-opus-5-5", FALLBACK)


def panel_call(tenant: str, prompt: str) -> list[tuple[str, dict]]:
    """Every claim to EVERY model, so the reviewer is not predicted by the topic.

    MEASURED 2026-11-04: opus passed 41% of the claims it judged; sonnet passed 0 of 18. Re-running
    sonnet on 8 claims opus had PASSED weakened 7 of them, so the asymmetry is the model. Because
    the fallback fires on a `category: bio` refusal, that made the protein claims systematically
    harsher-reviewed than the methodology claims -- topic selecting reviewer selecting verdict.
    Routing every claim through both costs about $0.02 against $0.013 and removes the confound
    rather than documenting it.
    """
    out = []
    for mdl in PANEL:
        try:
            r = call(tenant, prompt, model=mdl)
        except Exception as e:
            if "refused" in str(e).lower():
                out.append((mdl, {"_refused": True}))
                continue
            raise
        out.append((mdl, r))
    return out


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
    write = "--write" in sys.argv
    panel = "--panel" in sys.argv
    # --tenant PINS the spend to one tenant. The docstring has advertised this flag since the
    # file was written and main() never read it, so a run meant to drain the tenant expiring
    # soonest silently rotated across all four and looked exactly like a run that had not. The
    # name is checked against TENANTS so a typo -- or `api_allen`, which the owner's standing
    # instruction excludes -- refuses rather than falling back to the rotation.
    tenants = list(TENANTS)
    if "--tenant" in sys.argv:
        want = sys.argv[sys.argv.index("--tenant") + 1]
        if want not in TENANTS:
            print(f"  --tenant {want!r} is not one of {TENANTS}"
                  + ("  (api_allen is EXCLUDED by standing instruction)"
                     if want == "api_allen" else ""))
            return 2
        tenants = [want]
    if "--repanel" in sys.argv:
        # Claims that have been challenged by exactly ONE model. Those verdicts are confounded:
        # claim 497 measured that opus passes 41% of what it judges and sonnet 0 of 18, and that
        # re-running sonnet on opus-PASSED claims weakens 7 of 8 -- so a single-model verdict
        # records which model happened to see it as much as what it says. Re-running these through
        # the panel replaces one model's opinion with two, at about $0.02 a claim.
        rows = q(f"""select c.id, c.evidence, {flat('c.statement')}
                     from claim c
                     where c.project_id={lit(PROJECT)} and c.superseded_by is null
                     and length(c.statement) between 80 and 6000
                     and exists (select 1 from challenge ch where ch.claim_id = c.id
                                 and ch.challenger like 'api%')
                     and (select count(distinct split_part(
                              replace(replace(ch2.challenger,'api-panel:',''),'api:',''),'@',1))
                          from challenge ch2 where ch2.claim_id = c.id
                          and ch2.challenger like 'api%') = 1
                     order by c.id desc limit {n}""")
    elif "--no-opus" in sys.argv:
        # Claims NEVER judged by the arm that demonstrably reads them. The mutation control in
        # swarm/critic_control.py found opus catching 3 of 4 corrupted claims with no false
        # alarm, while sonnet returned near-identical attack text for a corrupted claim and its
        # clean original on 3 of 5 pairs and asserted an inconsistency in a claim that had none.
        # So a claim reviewed only by the fallback has been reviewed by a model not shown to
        # read it, and the panel's row count hides that. 244 live claims were in this state when
        # the mode was added. Fallback verdicts keep their distinct challenger label, so they
        # stay countable separately rather than merging into the panel.
        rows = q(f"""select c.id, c.evidence, {flat('c.statement')}
                     from claim c
                     where c.project_id={lit(PROJECT)} and c.superseded_by is null
                     and length(c.statement) between 80 and 6000
                     and not exists (select 1 from challenge ch
                                     where ch.claim_id = c.id
                                     and ch.challenger like '%claude-opus-5-5%'
                                     and ch.outcome in ('survived','weakened','refuted'))
                     order by c.id desc limit {n}""")
    else:
        rows = q(f"""select c.id, c.evidence, {flat('c.statement')}
                     from claim c where c.project_id={lit(PROJECT)} and c.superseded_by is null
                     and length(c.statement) between 80 and 6000
                     and not exists (select 1 from challenge ch where ch.claim_id = c.id)
                     order by c.id desc limit {n}""")
    if not rows:
        print("  no unchallenged live claims; nothing to do.")
        return 0
    print(f"  {len(rows)} claim(s); tenants {tenants} (api_allen EXCLUDED)"
          + (f"; PANEL mode, every claim to {PANEL}" if panel else "") + "\n")
    spent = 0.0
    refused_n = 0
    panel_sizes: dict[int, int] = {}
    tally: dict[str, int] = {}
    for i, (cid, ev, stmt) in enumerate(rows):
        t = tenants[i % len(tenants)]
        prompt = PROMPT.format(cid=cid, ev=ev, stmt=stmt[:6000])
        if panel:
            # Both models, recorded as separate challenge rows. A claim both weaken is a different
            # fact from one only the harsher model weakens, and only a panel can tell them apart.
            verdicts = []
            for mdl, rr in panel_call(t, prompt):
                if rr.get("_refused"):
                    # A REFUSAL IS DATA AND MUST LEAVE A ROW. Printing it and moving on is how
                    # the panel came to misreport itself: measured 2026-11-04 over 370 claims
                    # carrying api-panel rows, 61 had a verdict from only ONE model, and the
                    # lone voice was claude-sonnet-5-5 in 104 of 104 rows -- opus never once.
                    # Because both cases are labelled `api-panel:`, nothing downstream could
                    # tell a two-model panel from a one-model one. The consequence is not
                    # cosmetic: sonnet alone weakened 98 of 104 (94%) and passed 4 (3.8%),
                    # while a true panel weakened 479 of 640 (75%) and passed 157 (24.5%). So a
                    # claim that trips the refusal classifier is about SIX TIMES less likely to
                    # survive -- which is precisely the "topic selects reviewer selects verdict"
                    # confound this panel was built to remove, still running at the refusal rate.
                    # A separate challenger prefix keeps `like 'api-panel:%'` queries unchanged
                    # while making the gap countable.
                    refused_n += 1
                    print(f"  claim {cid:>4} {mdl:18} REFUSED   -> recorded as not-run")
                    if write:
                        q(f"""insert into challenge (claim_id, challenger, attack, outcome, evidence)
                              values ({int(cid)},
                                      {lit('api-panel-refused:' + mdl + '@' + t)},
                                      {lit('(no attack: the model refused the prompt)')},
                                      {lit('not-run')},
                                      {lit('REFUSAL, not a judgement. The model declined this '
                                           'prompt, so this claim was reviewed by the rest of '
                                           'the panel only. Counting it as unreviewed would be '
                                           'wrong; counting the panel as complete would be '
                                           'worse.')})""")
                    continue
                a2, o2, w2 = parse(rr.get("text", ""))
                spent += float(rr.get("cost_usd") or 0)
                verdicts.append((mdl, o2))
                tally[o2] = tally.get(o2, 0) + 1
                print(f"  claim {cid:>4} {mdl:18} {o2:9} ${rr.get('cost_usd',0):.5f}  {a2[:50]}")
                if write:
                    q(f"""insert into challenge (claim_id, challenger, attack, outcome, evidence)
                          values ({int(cid)}, {lit('api-panel:' + mdl + '@' + t)}, {lit(a2)},
                                  {lit(o2)}, {lit(w2)})""")
            panel_sizes[len(verdicts)] = panel_sizes.get(len(verdicts), 0) + 1
            if len(verdicts) == 2 and verdicts[0][1] != verdicts[1][1]:
                print(f"       -> PANEL SPLIT: {verdicts[0][1]} vs {verdicts[1][1]}")
            if len(verdicts) < 2:
                print(f"       -> DEGRADED PANEL: {len(verdicts)} of {len(PANEL)} models "
                      f"answered; this verdict is one model's opinion, not a panel's")
            continue
        try:
            r = call_with_fallback(t, prompt)
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
    if panel_sizes or refused_n:
        full = panel_sizes.get(len(PANEL), 0)
        part = sum(v for k, v in panel_sizes.items() if k < len(PANEL))
        print(f"  panel completeness: {full} claim(s) judged by all {len(PANEL)} models, "
              f"{part} by fewer ({refused_n} refusal(s) recorded as not-run)")
        if part:
            print("  A DEGRADED PANEL IS NOT A PANEL. Those verdicts are one model's opinion "
                  "and are labelled api-panel-refused: so they stay countable.")
    print(f"  spent ${spent:.4f} of Console API credit"
          + ("" if write else "  (report only; pass --write to record)"))
    if tally and len(tally) == 1 and "survived" not in tally:
        print("  WARNING: every verdict is the same. A challenge arm with one outcome measures "
              "nothing; check the prompt before trusting these.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
