#!/usr/bin/env python3
"""
check_claims.py — bind prose claims about control outcomes to the fields they describe.

WHY THIS EXISTS. `colony-morphology.json` shipped a headline saying "Both pre-declared
controls pass" while `control_arm` in the same file recorded six checks with one
failing — and it offered the FAILING measurement (box-counting dimension 2.43) as
evidence that the control had passed. Nothing was relaxed and no number was wrong; a
sentence written before the final run simply was not regenerated with it, and prose has
no caller, no test selection and nothing that notices when it goes stale.

This binds the two together. For every result file it finds the control block, counts the
checks, and then reads every string in the file for an assertion about control outcomes.
A string that says the controls passed, while a check is recorded as failed, is an error.

WHAT IT DELIBERATELY DOES NOT DO. It does not try to parse arbitrary prose. A
forbidden-string matcher cannot tell claiming from quoting or asserting from denying, so
this checks ONE narrow family of claim — "the controls passed" and its variants — and is
anchored on phrasings this project actually uses. It is a backstop, not a proof. The real
fix is the one applied alongside it: generate the sentence FROM the data so it cannot
drift.

Usage
  python3 check_claims.py            # check the result files
  python3 check_claims.py --self-test   # run the positive and negative controls
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Phrasings that ASSERT every control passed. Anchored on what this project writes.
PASS_ASSERTION = re.compile(
    r"\b(all|both|every)\s+(?:\w+\s+){0,3}controls?\s+(?:arms?\s+)?pass"
    r"|\bcontrol\s+arm\s+passe[sd]\b"
    r"|\bcontrols?\s+all\s+pass",
    re.I)

# "N of M ... controls pass" — a counted claim, which we can check exactly.
COUNTED = re.compile(
    r"\b(\d+)\s+of\s+(\d+)\s+(?:\w+\s+){0,3}controls?\s+pass", re.I)

# Phrasings that explicitly report a failure. A string containing one of these is
# reporting, not over-claiming, even if it also contains the word "pass".
FAILURE_ACKNOWLEDGED = re.compile(
    r"\bFAILS?\b|\bfailed\b|\bfailing\b|\bdoes not pass\b|\bn_failed\b", re.I)


def walk_strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")


def check_doc(doc, name="<doc>"):
    """Return a list of problems. Empty list means the claims bind."""
    errs = []
    ctrl = doc.get("control_arm")
    if not isinstance(ctrl, dict) or "checks" not in ctrl:
        return errs                       # no control block, nothing to bind
    checks = ctrl["checks"]
    n_ck = len(checks)
    failed = [k for k, v in checks.items() if not v]
    n_fail = len(failed)
    n_pass = n_ck - n_fail

    # 1. the aggregate field must not disagree with its own checks
    declared = ctrl.get("declared_before_the_run") or list(checks)
    strict = all(checks[k] for k in declared if k in checks)
    if "passed" in ctrl and bool(ctrl["passed"]) != strict:
        errs.append(f"{name}: control_arm.passed is {ctrl['passed']} but the checks "
                    f"declared before the run give {strict}")

    # 2. no string may assert the controls passed while one is recorded failed
    for path, text in walk_strings(doc):
        if path.startswith("control_arm.note") or "exclusion_rule" in path:
            continue                      # the field whose job is to explain the failure
        m = COUNTED.search(text)
        if m:
            a, b_ = int(m.group(1)), int(m.group(2))
            if b_ != n_ck or a != n_pass:
                errs.append(f"{name}: {path} claims '{a} of {b_} controls pass' but the "
                            f"control block records {n_pass} of {n_ck}")
            continue
        if PASS_ASSERTION.search(text) and n_fail > 0:
            if not FAILURE_ACKNOWLEDGED.search(text):
                snippet = PASS_ASSERTION.search(text).group(0)
                errs.append(f"{name}: {path} asserts '{snippet}...' but "
                            f"{n_fail} control(s) failed: {', '.join(failed)}")

    # 3. if a control failed, the headline must name it
    if n_fail > 0:
        head = doc.get("headline", "")
        if not any(f in head for f in failed):
            errs.append(f"{name}: a control failed ({', '.join(failed)}) and the headline "
                        f"does not name it")
    return errs


def self_test():
    """Positive and negative controls for this checker.

    A check whose subject includes the check is not a check, so this one is run against a
    case it MUST flag and a case it must NOT.
    """
    failing_doc = dict(
        headline="Both pre-declared controls pass and the model works beautifully.",
        control_arm=dict(checks=dict(a=True, b=False, c=True), passed=True))
    clean_doc = dict(
        headline="2 of 3 pre-declared controls pass and 1 FAILS: `b`.",
        control_arm=dict(checks=dict(a=True, b=False, c=True), passed=False))
    all_pass_doc = dict(
        headline="All 3 pre-declared controls pass.",
        control_arm=dict(checks=dict(a=True, b=True, c=True), passed=True))
    neg = check_doc(failing_doc, "MUST-FLAG")
    pos = check_doc(clean_doc, "MUST-NOT-FLAG")
    pos2 = check_doc(all_pass_doc, "MUST-NOT-FLAG-all-pass")
    ok = True
    print(f"positive control (a doc that MUST be flagged): {len(neg)} problem(s)")
    for e in neg:
        print("   " + e)
    if len(neg) < 3:
        print("   SELF-TEST FAILED: expected the passed-field, the prose claim and the "
              "unnamed failure to all be caught")
        ok = False
    print(f"negative control (a correct doc): {len(pos)} problem(s) {pos}")
    if pos:
        ok = False
    print(f"negative control (all controls genuinely pass): {len(pos2)} problem(s) {pos2}")
    if pos2:
        ok = False
    print("SELF-TEST " + ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())

    problems = []
    checked = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "*.json"))):
        if os.path.basename(path).endswith("-cache.json"):
            continue
        with open(path) as fh:
            doc = json.load(fh)
        checked += 1
        problems += check_doc(doc, os.path.basename(path))
    print(f"checked {checked} result files")
    if problems:
        print("CLAIM BINDING FAILED:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print("all control-outcome claims bind to their control blocks")


if __name__ == "__main__":
    main()
