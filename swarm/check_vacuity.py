#!/usr/bin/env python3
"""Report every mechanism whose subject set is EMPTY, because a rule over nothing is always true.

THE FAILURE MODE THIS DETECTS, which recurred four times in one session before it was named:

  * SPEC-evaluation-kernel rules 1, 2 and 5 all read green. `grade` and `rubric` hold 0 rows, so
    they cannot fail. The green meant grading did not happen.
  * Dependency propagation "worked": the trigger was installed and correct, and it walked a
    `claim_depends` holding 6 edges across 330 claims. 29 of 35 superseded claims flagged nothing.
  * SPEC-ASK rule 7 -- the rule the spec calls "the one that makes the other six honest" -- was
    simply absent from the checker. Five implemented rules looked like a complete list.
  * A universally quantified acceptance clause over a collection the task itself produces
    ("every unmutated pair carries a review") is satisfied by producing no pairs.

In all four, a passing check and an absent check are the same two characters on screen. The only
defence is to count the subject set and say so out loud.

THIS IS NOT A GATE. It is a sweep to read. An empty table is often correct -- a mechanism that has
not been needed yet is not a defect, and failing a build over one would get the check switched off.
What is a defect is an empty table that something REPORTS ON as though it had looked.
"""
from __future__ import annotations

import os
import subprocess
import sys

PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm", "-tAq"]

# (table, what depends on it, why an empty set would be misread)
MECHANISMS = [
    ("grade",                "evaluation kernel: grading",      "SPEC-evaluation-kernel rules 1, 2, 5"),
    ("rubric",               "evaluation kernel: rubrics",      "SPEC-evaluation-kernel rules 1, 2"),
    ("candidate",            "evaluation kernel: candidates",   "anything ranking designs"),
    ("comparison",           "pairwise comparison",             "SPEC-evaluation-kernel rule 5"),
    ("claim_depends",        "dependency propagation",          "SPEC-subproblem-lifecycle rule 6, ASK D4"),
    ("review_flag",          "review flags",                    "SPEC-subproblem-lifecycle rule 6"),
    ("idea_score",           "idea scoring",                    "SPEC-idea-intake rule 3"),
    ("idea_check",           "idea checks",                     "SPEC-idea-intake rules 2, 3"),
    ("constraint_entailed",  "cross-scale constraints",         "the whole cross-scale argument"),
    ("run",                  "runs and executability",          "ASK rule 3; ALL simulation provenance"),
    ("artifact",             "artifacts",                       "ASK rule 1"),
    ("part",                 "parts / CAD library",             "the parts-library design"),
    ("need",                 "needs",                           "the needs/pressure loop"),
    ("regime_transition",    "representation change",           "the categorical-transition argument"),
    ("synthesis",            "multi-parent synthesis",          "the synthesis mechanism"),
    ("experiment",           "experiments",                     "anything proposing bench work"),
    ("benchmark_item",       "grader benchmark",                "grader calibration"),
    ("grader_calibration",   "grader calibration",              "SPEC-evaluation-kernel rule 3"),
    ("retraction",           "retractions",                     "ASK D4"),
    ("structural_assumption", "structural assumptions",         "parameter provenance"),
    ("parameter",            "parameters",                      "parameter provenance"),
]


def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def main():
    empty, live, broken = [], [], []
    print("  rows  table                     mechanism")
    for t, label, depends in MECHANISMS:
        r = subprocess.run(PG + ["-c", f"select count(*) from {t}"],
                           capture_output=True, text=True, env=env(), timeout=60)
        if r.returncode:
            broken.append((t, r.stderr.strip()[:60]))
            print(f"   ERR  {t:24}  {label}")
            continue
        n = int(r.stdout.strip())
        (empty if n == 0 else live).append((t, label, depends, n))
        mark = "  <-- EMPTY" if n == 0 else ""
        print(f"  {n:>5}  {t:24}  {label}{mark}")

    print(f"\n  {len(empty)} of {len(MECHANISMS)} mechanisms have NO subject set.")
    print("  Any rule quantified over these is VACUOUSLY TRUE and must not be read as a pass:\n")
    for t, label, depends, _ in empty:
        print(f"    {t:24} would silently satisfy: {depends}")
    if broken:
        print(f"\n  {len(broken)} table(s) could not be counted -- unknown, not empty:")
        for t, err in broken:
            print(f"    {t}: {err}")
    print("\n  An empty table is often CORRECT. What is never correct is a check reporting green")
    print("  over one. This sweep is to be read, not to gate a build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
