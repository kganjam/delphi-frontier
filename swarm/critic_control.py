#!/usr/bin/env python3
"""Does the adversarial reviewer READ the claim, or does it weaken everything regardless?

WHY THIS EXISTS. Over 84 claims the panel's sonnet arm returned `weakened` 77 times -- 92%. A
critic whose verdict barely depends on its input measures nothing, and the project's goal is to
SHOW adversarial agents refining designs. The production prompt already says SURVIVED is a correct
answer and that inventing a weakness is worse than reporting none, so prompt wording is not the
explanation and the question is whether the reviewer is reading at all.

THE TEST IS MUTATION, which is the discipline this repo already applies to code and to Lean
proofs: break the thing on purpose and require the checker to notice. Each pair below is one
claim sent twice --

  ORIGINAL : exactly as recorded, which must NOT draw an arithmetic objection
  MUTANT   : one number changed so the statement CONTRADICTS ITSELF or becomes physically
             impossible, using only what is on the page -- no outside knowledge needed

A reviewer that reads catches the mutant. One that pattern-matches scientific prose produces the
same generic objection for both, and that is visible in the text rather than only in the verdict.

The ORIGINAL arm is the negative control and it is the half people skip: without it, a reviewer
that shouts "arithmetic error" at everything would score a perfect detection rate.

THE PRODUCTION PROMPT IS SENT UNCHANGED. Asking "is there an arithmetic error here?" would test a
different system than the one in use.

Usage:  python3 critic_control.py [--models opus,sonnet] [--write]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_challenge import PROMPT, TENANTS, call, q  # noqa: E402

MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5"}

# (claim id, exact substring to replace, replacement, what the reviewer must notice)
# Every mutation is checkable FROM THE PAGE: it contradicts another number in the same claim,
# or it breaks a bounded scale. None requires the reviewer to know the subject matter.
MUTATIONS = [
    (522, "a factor of 47", "a factor of 4",
     "5.87 / 0.13 is about 45, so 'a factor of 4' contradicts its own two operands"),
    (521, "2.2 times the threshold", "0.5 times the threshold",
     "3.33 against a 1.5 threshold is 2.2x; 0.5x would mean it PASSED, contradicting "
     "the claim's own verdict of falsified"),
    (522, "BY 9.99 AT SITE 200", "BY 99.9 AT SITE 200",
     "pLDDT is bounded 0-100 and the wild type is 97.65, so a 99.9 drop is impossible"),
    (520, "is 0.95 cm", "is 9.5 cm",
     "9.5 cm against the claim's own 2 cm threshold would SETTLE IT POSITIVELY, "
     "contradicting the verdict in the same sentence"),
    (519, "DEFICIT is r", "DEFICIT is r",   # anchor only; mutation applied below by number
     "placeholder"),
]
# the fifth pair is built from the claim's own value_num rather than a hand-written anchor
NUMERIC_PAIR = (519, "deficit", 2.29, 0.29,
                "a deficit below 1.0 means the requirement IS met, which contradicts the "
                "claim's own headline that the launch does not close")

ARITH_MARKERS = re.compile(
    r"arithmetic|does not follow|doesn'?t follow|inconsisten|contradict|"
    r"divid|ratio|factor of|exceed|impossible|bounded|0\s*[-to]+\s*100|"
    r"cannot exceed|miscalcul|wrong by|should be|internally",
    re.I)


def fetch(cid: int) -> tuple[str, str]:
    # flat() OR THIS CANNOT READ 74.6 PER CENT OF THE CORPUS. dbq.q() splits its output on
    # line boundaries, so a bare `select statement` on a multi-line claim returns one list per
    # LINE and rows[0][1] raises IndexError -- not a truncation anyone would notice, a crash.
    # Measured 2026-11-06: 1170 of 1568 live claims contain a newline, so this function could
    # only ever run on the single-line quarter, and the mutation control it implements was
    # necessarily measured on that subset.
    rows = q("select replace(replace(statement, chr(10), ' '), chr(1), ' '), evidence "
             f"from claim where id = {cid};")
    if not rows:
        raise SystemExit(f"claim {cid} not found")
    return rows[0][0], rows[0][1]


def build_pairs() -> list[dict]:
    pairs = []
    for cid, old, new, must_notice in MUTATIONS[:4]:
        stmt, ev = fetch(cid)
        n = stmt.count(old)
        if n != 1:
            raise SystemExit(
                f"claim {cid}: anchor {old!r} occurs {n} times, not once -- refusing to guess "
                "which one to mutate")
        pairs.append({"cid": cid, "ev": ev, "original": stmt,
                      "mutant": stmt.replace(old, new),
                      "change": f"{old!r} -> {new!r}", "must_notice": must_notice})

    cid, _, was, now, must_notice = NUMERIC_PAIR
    stmt, ev = fetch(cid)
    tok = f"{was}"
    if stmt.count(tok) < 1:
        raise SystemExit(f"claim {cid}: {tok!r} not present; cannot build the numeric mutant")
    pairs.append({"cid": cid, "ev": ev, "original": stmt,
                  "mutant": stmt.replace(tok, f"{now}"),
                  "change": f"every {tok} -> {now}", "must_notice": must_notice})
    return pairs


def ask(model: str, tenant: str, cid: int, ev: str, stmt: str) -> dict:
    text = PROMPT.format(cid=cid, ev=ev, stmt=stmt)
    out = call(tenant, text, max_tokens=1200, model=model)
    body = out.get("text") or out.get("content") or ""
    if isinstance(body, list):
        body = " ".join(b.get("text", "") for b in body if isinstance(b, dict))
    outs = re.findall(r"OUTCOME:\s*([a-z-]+)", body, re.I)
    atks = re.findall(r"ATTACK:\s*(.+)", body)
    return {"outcome": (outs[-1].lower() if outs else "no-verdict"),
            "attack": (atks[-1].strip() if atks else body.strip()[:300]),
            "cost": float(out.get("cost_usd") or 0.0)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="opus,sonnet")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    pairs = build_pairs()
    print(f"{len(pairs)} mutation pairs built; every anchor matched exactly once\n")

    rng = random.Random(7)
    results, spend = [], 0.0
    for key in a.models.split(","):
        model = MODELS[key.strip()]
        print(f"================ {model} ================")
        for p in pairs:
            arms = [("ORIGINAL", p["original"]), ("MUTANT", p["mutant"])]
            rng.shuffle(arms)                      # order must not leak which is which
            for arm, stmt in arms:
                t = TENANTS[len(results) % len(TENANTS)]
                try:
                    r = ask(model, t, p["cid"], p["ev"], stmt)
                except Exception as e:
                    r = {"outcome": "ERROR", "attack": str(e)[:200], "cost": 0.0}
                spend += r["cost"]
                flagged = bool(ARITH_MARKERS.search(r["attack"]))
                results.append({"model": model, "cid": p["cid"], "arm": arm,
                                "outcome": r["outcome"], "attack": r["attack"],
                                "flagged": flagged, "change": p["change"],
                                "must_notice": p["must_notice"]})
                print(f"  claim {p['cid']:>4} {arm:<9} {r['outcome']:<10} "
                      f"{'FLAGGED-ARITH' if flagged else '             '} {r['attack'][:92]}")
            print()

    # ---- scoring -----------------------------------------------------------
    print("=" * 78)
    for key in a.models.split(","):
        model = MODELS[key.strip()]
        mine = [r for r in results if r["model"] == model]
        mut = [r for r in mine if r["arm"] == "MUTANT"]
        orig = [r for r in mine if r["arm"] == "ORIGINAL"]
        det = sum(1 for r in mut if r["flagged"])
        fa = sum(1 for r in orig if r["flagged"])
        print(f"\n{model}")
        print(f"  mutants caught (sensitivity) : {det}/{len(mut)}")
        print(f"  originals wrongly flagged    : {fa}/{len(orig)}   <- the negative control")
        print(f"  weakened on MUTANT  : {sum(1 for r in mut if r['outcome'] == 'weakened')}"
              f"/{len(mut)}")
        print(f"  weakened on ORIGINAL: {sum(1 for r in orig if r['outcome'] == 'weakened')}"
              f"/{len(orig)}")
        if det == len(mut) and fa == 0:
            print("  -> READS THE CLAIM: every corruption caught, no false alarm")
        elif det == 0:
            print("  -> DOES NOT READ THE NUMBERS: caught none of the corruptions")
        else:
            print("  -> PARTIAL. The verdict alone cannot distinguish reading from a prior;")
            print("     the attack TEXT below is the evidence and has to be read by hand.")

    print(f"\ntotal spend: ${spend:.4f}")
    print("\nNOTE ON THE GRADER: `flagged` is a regex over the attack text and is a SCREEN, not a")
    print("verdict. It cannot tell a reviewer that spotted the arithmetic from one that used the")
    print("word 'ratio' about something else. Every line above is printed in full for that reason.")

    out = Path(__file__).resolve().parent.parent / "results/critic_control.json"
    if a.write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, indent=2))
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
