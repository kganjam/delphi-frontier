#!/usr/bin/env python3
"""Independently re-derive the project's numeric claims on Console API credit.

A claim carrying `value_num` asserts a number. This asks a model that has NOT seen the derivation
to recompute it from the claim's own prose, and flags a mismatch. It is the cheap half of SPEC
section 1b: a number repeated in several places needs its DERIVATION checked, not its copies
counted.

WHAT IT CANNOT DO, stated because the output would otherwise look stronger than it is: the model
sees the claim text only. If the claim states its inputs, the recomputation is real; if it merely
asserts a number, the model can only check internal consistency, and the tool records which of the
two happened rather than scoring both as "verified". A claim whose number cannot be recomputed from
its own words is reported as `underdetermined` -- which is itself a finding about the claim.

    python3 api_recompute.py <n> [--write]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_challenge as ac  # noqa: E402

PROMPT = """You are checking a single number in a scientific claim. Do not be agreeable.

CLAIM {cid} asserts the value: {val} {units}

Its text:
{stmt}

Recompute that number from the claim's OWN stated inputs. Do not use outside knowledge to fill a
gap -- if the claim does not state enough to recompute the value, say UNDERDETERMINED. That is a
useful answer, not a failure, and it is the honest one for a claim that merely asserts a figure.

Reply in EXACTLY this form, verdict first:
VERDICT: <reproduces|mismatch|underdetermined>
VALUE: <the number you got, or "n/a">
WHY: <two sentences at most>
"""
VERDICTS = ("reproduces", "mismatch", "underdetermined")


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
    write = "--write" in sys.argv
    rows = ac.q(f"""select id, value_num, coalesce(units,''), replace(statement,'{ac.SEP}',' ')
                    from claim where project_id={ac.lit(ac.PROJECT)} and superseded_by is null
                    and value_num is not null and length(statement) between 80 and 6000
                    order by id desc limit {n}""")
    print(f"  {len(rows)} numeric claim(s)\n")
    tally: dict[str, int] = {}
    spent = 0.0
    for i, (cid, val, units, stmt) in enumerate(rows):
        t = ac.TENANTS[i % len(ac.TENANTS)]
        try:
            r = ac.call_with_fallback(t, PROMPT.format(cid=cid, val=val, units=units, stmt=stmt[:6000]))
        except Exception as e:
            print(f"  claim {cid:>4} {t:13} FAILED {type(e).__name__}: {str(e)[:70]}")
            continue
        txt = r.get("text", "")
    # TAKE THE LAST VERDICT, NOT THE FIRST. Measured 2026-11-04: a reply read
    #   VERDICT: mismatch ... "Correction: on reflection, the verdict should be underdetermined."
    #   VERDICT: underdetermined
    # re.search returns the FIRST match, so the parser recorded `mismatch` -- the model's discarded
    # first thought -- and would have written a false challenge against the project's own claim.
    # A self-correcting reply is the model doing the right thing; reading only its opening is the
    # harness doing the wrong one.
        ms = re.findall(r"VERDICT:\s*([a-z]+)", txt, re.I)
        v = (ms[-1].lower() if ms else "")
        if v not in VERDICTS:
            v = "unparsed"
        gs = re.findall(r"VALUE:\s*(.+)", txt)
        got = (gs[-1] if gs else None)
        ws = re.findall(r"WHY:\s*(.+)", txt)
        why = (ws[-1] if ws else None)
        spent += float(r.get("cost_usd") or 0)
        tally[v] = tally.get(v, 0) + 1
        fb = " FB" if r.get("_fallback_from_refusal") else "   "
        print(f"  claim {cid:>4} {t:13}{fb} {v:15} stated={val} got={(got.strip()[:22] if got else '?')}")
        if write and v == "mismatch":
            ac.q(f"""insert into challenge (claim_id, challenger, attack, outcome, evidence)
                     values ({int(cid)}, {ac.lit('api-recompute:' + str(r.get('model')) + '@' + t)},
                             {ac.lit('independent recomputation disagrees with the stated value')},
                             'weakened', {ac.lit((why.strip()[:900] if why else txt[:900]))})""")
    print(f"\n  {tally}\n  spent ${spent:.4f}"
          + ("" if write else "   (report only; --write records mismatches as challenges)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
