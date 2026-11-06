#!/usr/bin/env python3
"""One bounded cycle of the design swarm: gap -> challenge -> synthesis -> conform -> publish.

WHY THIS EXISTS. Every stage of this project already works on its own, and nothing ran them as a
loop. The result was that each stage was invoked by hand when someone remembered it, which is how
the corpus drifted out from under the project for weeks (claim 603) and how the monitor came to be
watching a credit pool that no longer existed (claim 890). A loop is not more automation for its
own sake; it is the thing that makes an omission visible on the next pass instead of never.

PROJECT-AGNOSTIC BY CONSTRUCTION. Every stage reads SWARM_PROJECT, so this runs for coral,
insect-flight, xenobot or limbless-mouse by setting one variable. That was the point of today's
import work: four other projects are now in the graph, so the loop has somewhere to go.

THE DESIGN RULE THAT MATTERS, and it is this repository's oldest lesson: A STAGE THAT DID NOT RUN
MUST NOT LOOK LIKE A STAGE THAT PASSED. Every stage records one of RAN-OK / RAN-FAILED / SKIPPED /
ERRORED, never a bare boolean, and the cycle record carries the exit code and the reason. A cycle
in which four stages were skipped and one passed is NOT a green cycle, and the summary says so in
those words.

BOUNDEDNESS, because an unbounded loop on a shared host is how this fleet has hurt itself before:
  * one cycle per invocation by default; --cycles N is capped at MAX_CYCLES;
  * every stage runs under a timeout and, where available, a systemd scope with a memory and
    task cap, so a runaway stage cannot take the host down;
  * a sentinel env var makes a NESTED cycle refuse to start. AGENTS.md: "Never let a check
    invoke itself. A runner that executes recorded commands must refuse to run nested (set and
    check an env sentinel)". Setting a sentinel without checking it is not a guard, so this
    checks it first and sets it second.

    python3 cycle.py [--cycles N] [--challenge N] [--write] [--project P]
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "results" / "cycles"
SENTINEL = "MORPHOSWARM_CYCLE_RUNNING"
MAX_CYCLES = 6
STAGE_TIMEOUT = 900


def scope(cmd: list[str]) -> list[str]:
    """Bound the whole process tree where systemd-run is available.

    MemoryMax alone does NOT cap anything on this host -- it has 128 GB of swap and a scope's
    memory.swap.max defaults to max, so the overflow swaps instead of dying. MemorySwapMax=0 is
    what makes the cap real.
    """
    if subprocess.run(["which", "systemd-run"], capture_output=True).returncode != 0:
        return cmd
    return ["systemd-run", "--user", "--scope", "-q",
            "-p", "MemoryMax=4G", "-p", "MemorySwapMax=0",
            "-p", "TasksMax=256", "-p", f"RuntimeMaxSec={STAGE_TIMEOUT}"] + cmd


#: Volatile text that differs between two runs of an UNCHANGED check: wall-clock times, ISO
#: timestamps, durations, memory addresses, temp paths. Stripped before signing so the signature
#: changes when the FINDINGS change and not when the clock does.
_VOLATILE = [
    (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?([+-]\d{2}:?\d{2}|Z)?"), "<ts>"),
    (re.compile(r"\b\d+(\.\d+)?\s*(s|ms|sec|seconds|minutes)\b"), "<dur>"),
    (re.compile(r"0x[0-9a-f]{6,}"), "<addr>"),
    (re.compile(r"/tmp/[^\s'\"]+"), "<tmp>"),
    (re.compile(r"\$\d+\.\d+"), "<cost>"),
]


def signature(tail: str) -> str:
    """A digest of what a stage FOUND, stable across re-runs that find the same thing.

    A STAGE THAT IS ALWAYS RED HIDES A STAGE THAT JUST TURNED RED. Two of this loop's stages
    are deliberately red -- `specs` carries one documented FAIL, and `grader_use` exits 1 to
    register every claim resting on a provisional grader -- so `RAN-FAILED` has been the normal
    state for both and a NEW failure in either would have looked identical to the old one. That
    is this file's own opening rule ("a stage that was not run MUST NOT LOOK LIKE a stage that
    passed") with the sign flipped.

    Nothing is suppressed: a red stage stays RAN-FAILED. What the signature adds is whether the
    red is the SAME red, so the cycle can say CHANGED rather than only FAILED.
    """
    t = tail or ""
    for rx, repl in _VOLATILE:
        t = rx.sub(repl, t)
    return hashlib.sha256(t.encode()).hexdigest()[:12]


def run_stage(name: str, cmd: list[str], why_skip: str | None = None) -> dict:
    """Run one stage and classify it. Never returns a bare pass/fail."""
    rec = {"stage": name, "cmd": " ".join(cmd), "started": datetime.now(timezone.utc).isoformat()}
    if why_skip:
        rec.update(status="SKIPPED", exit=None, reason=why_skip, tail="")
        print(f"  {name:<12} SKIPPED   {why_skip}")
        return rec
    t0 = time.time()
    try:
        r = subprocess.run(scope(cmd), capture_output=True, text=True,
                           timeout=STAGE_TIMEOUT + 60, cwd=ROOT)
        out = (r.stdout or "") + (r.stderr or "")
        rec.update(status="RAN-OK" if r.returncode == 0 else "RAN-FAILED",
                   exit=r.returncode, reason="", tail=out.strip()[-600:])
    except subprocess.TimeoutExpired:
        rec.update(status="ERRORED", exit=None,
                   reason=f"timed out after {STAGE_TIMEOUT}s", tail="")
    except Exception as e:                                    # noqa: BLE001
        rec.update(status="ERRORED", exit=None, reason=f"{type(e).__name__}: {e}", tail="")
    rec["seconds"] = round(time.time() - t0, 1)
    rec["signature"] = signature(rec.get("tail", ""))
    mark = {"RAN-OK": "ok", "RAN-FAILED": "FAILED", "ERRORED": "ERROR"}[rec["status"]]
    print(f"  {name:<12} {rec['status']:<10} exit={rec['exit']} {rec['seconds']}s  {mark}")
    return rec


EXTRACT = HERE.parent / "results" / "extract"


def one_cycle(project: str, n_challenge: int, write: bool) -> dict:
    py = sys.executable
    stages = []
    # 1. Is the project reading the right literature at all?
    stages.append(run_stage("gap", [py, str(HERE / "corpus_gap.py")]))
    # 2. Adversarial review. The only stage that SPENDS, so it is the only one gated on --write.
    stages.append(run_stage(
        "challenge", [py, str(HERE / "api_challenge.py"), str(n_challenge), "--write"],
        None if write else "needs --write: this stage spends Console API credit"))
    # 2b. THE RETRIEVAL LOOP, which is what turns an adversarial critic into a swarm that can
    # answer its own objections rather than only raising them.
    #
    #   evaluate  -> every constraint it cannot settle records WHY, in one sentence
    #   questions -> those sentences become literature questions, as QUANTITIES not yes/nos
    #   harvest   -> one search per question; each paper is asked only the question that found it
    #   record    -> verified values become claims, labelled by how the PAPER came by the number
    #
    # Until 2026-11-05 every one of these was run by hand and the insufficient verdicts -- the
    # most actionable thing the evaluator produces -- were printed to stdout and discarded, so
    # each run paid to recompute a sentence nothing had kept. Run as a loop, an evaluator's
    # complaint becomes the next search, and the next cycle's evaluator sees what came back.
    #
    # BOUNDED HARD, because a harvest is hours long and this runs unattended: a handful of
    # questions per cycle, a dozen candidates each. The loop's value is that it runs EVERY cycle,
    # not that any one cycle is exhaustive.
    spend = None if write else "needs --write: these stages spend Console API credit"
    stages.append(run_stage(
        "evaluate", [py, str(HERE / "api_evaluate_constraints.py"), "12", "--write"], spend))
    stages.append(run_stage(
        "questions", [py, str(HERE / "extraction_questions.py"), "--from-gaps", "--generalise",
                      "--cap", "6", "--out", str(EXTRACT / "questions_cycle.txt")], spend))
    stages.append(run_stage(
        # --judge-relevance added 2026-11-06. The quote gate establishes that a value is
        # really in the paper and nothing establishes that it answers the question: one
        # complete harvest gave 300 quote-verified values of which 0 answered (claim 3186),
        # and the recorder would have written all 300 as claims asserting they were harvested
        # to answer a question they do not answer. claims_from_extraction now withholds a value
        # judged False, but only an EXPLICIT False -- so without this flag the loop keeps
        # recording unjudged values and the withholding never fires.
        "harvest", [py, str(HERE / "targeted_harvest.py"), "--questions",
                    str(EXTRACT / "questions_cycle.txt"), "--limit", "4", "--write",
                    "--judge-relevance"],
        spend or (None if (EXTRACT / "questions_cycle.txt").exists()
                  else "no question file: the questions stage did not produce one")))
    # Recording is free and must run even when the paid stages were skipped, because a previous
    # cycle's harvest may be sitting unrecorded -- which is exactly how this pipeline sat for a
    # day with 225 papers and a 37-byte output file.
    stages.append(run_stage("record", [py, str(HERE / "claims_from_extraction.py"), "--write"]))

    # 3. Synthesis.
    stages.append(run_stage("synthesis", [py, str(HERE / "design_chain.py")]))
    # 4. Conformance. EVERY check_*.py RUNS HERE, and that is the point of the loop below
    # rather than a hand-written list.
    #
    # Before this, cycle.py invoked `check_specs` and `check_vacuity` and nothing else, while
    # swarm/ held SEVEN check_*.py files. Five of them -- claim_citations, frontier_stale,
    # route_typing, grader_use, interval_collapse -- were run by nothing at all. A checker
    # that nobody invokes reports nothing and reads exactly like a checker that found nothing,
    # which is the same failure as a gate that is switched off.
    #
    # Discovering them from the directory means a new check_*.py is wired in by existing,
    # instead of by somebody remembering to add a line here.
    for chk in sorted(HERE.glob("check_*.py")):
        stages.append(run_stage(chk.stem.replace("check_", ""), [py, str(chk)]))
    # 5. Publish, ALWAYS dry-run. It asserts no network module is loaded and writes to disk.
    stages.append(run_stage("publish", [py, str(HERE / "publish_dryrun.py")]))
    # 6. Did anything actually move?
    stages.append(run_stage("progress", [py, str(HERE / "progress.py")]))

    counts = {}
    for s in stages:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    return {"project": project, "at": datetime.now(timezone.utc).isoformat(),
            "stages": stages, "counts": counts}


LOCK = HERE.parent / "results" / "cycles" / ".cycle.lock"


def take_lock():
    """One cycle at a time, enforced by the OS rather than by who remembers to check.

    The nested-run sentinel below stops a cycle INVOKING ITSELF. It does not stop two SIBLING
    cycles -- one launched by hand and one by the credit supervisor -- from running at once, and
    those collide concretely: the questions stage writes a fixed `questions_cycle.txt` that the
    harvest stage then reads, so the second cycle's questions silently become the first cycle's
    harvest. That is the same fixed-path collision that made two concurrent harvests overwrite
    each other's results earlier today, and it was invisible for the same reason: the file is
    always a valid, complete question list. Just not the one that stage produced.

    flock is advisory but it is held by the kernel for the life of the process, so a cycle that
    is killed releases it without leaving a stale lock behind -- which a lockfile-plus-pid scheme
    does not manage.
    """
    import fcntl
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    fh = open(LOCK, "w")
    try:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return None
    return fh                      # kept open: closing it would release the lock


def previous_record(project: str) -> dict | None:
    """The most recent cycle record for this project, or None on the first ever run."""
    fs = sorted(OUT.glob(f"{project}-*.json"), key=lambda f: f.stat().st_mtime)
    for f in reversed(fs):
        try:
            return json.loads(f.read_text())
        except Exception:                                      # noqa: BLE001
            continue
    return None


def report_delta(prior: dict | None, now: dict) -> None:
    """Say which stages CHANGED since the last cycle, not merely which are red.

    Two stages here are permanently red by design, so "2 RAN-FAILED" has been the steady state
    and carried no information. This prints the transitions instead. A stage that is red in both
    cycles with the SAME signature is `unchanged`; one whose findings moved is `CHANGED`, which
    is the line a reader should act on.
    """
    if not prior:
        print("\n  DELTA: no previous cycle for this project; nothing to compare.")
        return
    old = {s["stage"]: s for s in prior.get("stages", [])}
    new = {s["stage"]: s for s in now.get("stages", [])}
    lines = []
    for name, s in new.items():
        o = old.get(name)
        if o is None:
            lines.append((f"NEW STAGE   {name}", s["status"]))
            continue
        if o["status"] != s["status"]:
            lines.append((f"{o['status']} -> {s['status']}  {name}", "transition"))
        elif o.get("signature") != s.get("signature"):
            lines.append((f"CHANGED     {name} ({s['status']}, findings moved)", "signature"))
    for name in old:
        if name not in new:
            lines.append((f"GONE        {name}", "missing"))
    print(f"\n  DELTA against the previous cycle ({prior.get('at', '?')}):")
    if not lines:
        print("    nothing changed -- same stages, same statuses, same findings.")
        red = [n for n, s in new.items() if s["status"] != "RAN-OK"]
        if red:
            print(f"    still red, unchanged: {', '.join(sorted(red))}")
        return
    for text, _kind in lines:
        print(f"    {text}")
    print("    A red stage that is unchanged is NOT listed here; it is in the stage table.")


def selftest() -> int:
    """Controls for signature() and report_delta(), shipped with them.

    A GUARD NEEDS A CASE IT MUST FLAG AND A CASE IT MUST NOT. The must-not case is the one that
    matters here: if the signature moved every run, every stage would read CHANGED forever and
    the delta would be exactly as uninformative as the bare FAILED count it replaces.
    """
    same_findings_later_clock = (
        "checked 12 claims\n  claim 402 FLAGGED\ndone in 3.2s at 2026-11-05T21:53:05+00:00",
        "checked 12 claims\n  claim 402 FLAGGED\ndone in 9.9s at 2026-11-05T22:41:11+00:00")
    more_findings = (
        same_findings_later_clock[0],
        "checked 13 claims\n  claim 402 FLAGGED\n  claim 999 FLAGGED\ndone in 3.2s "
        "at 2026-11-05T21:53:05+00:00")
    def rec(st):
        return {"at": "2026-11-05T21:00:00+00:00", "stages": st}
    def S(n, st, sig):
        return {"stage": n, "status": st, "signature": sig}
    base = [S("specs", "RAN-FAILED", "aaa"), S("grader_use", "RAN-FAILED", "bbb"),
            S("gap", "RAN-OK", "ccc")]
    checks = [
        ("signature ignores clock and duration",
         signature(same_findings_later_clock[0]) == signature(same_findings_later_clock[1])),
        ("signature moves when a finding is added",
         signature(more_findings[0]) != signature(more_findings[1])),
    ]
    import io
    import contextlib
    def delta_text(new_stages):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            report_delta(rec(base), rec(new_stages))
        return buf.getvalue()
    checks.append(("identical cycles report no change",
                   "nothing changed" in delta_text(base)))
    moved = [S("specs", "RAN-FAILED", "aaa"), S("grader_use", "RAN-FAILED", "ZZZ"),
             S("gap", "RAN-OK", "ccc")]
    checks.append(("a persistent red whose findings move is CHANGED",
                   "CHANGED" in delta_text(moved)))
    newfail = [S("specs", "RAN-FAILED", "aaa"), S("grader_use", "RAN-FAILED", "bbb"),
               S("gap", "RAN-FAILED", "ddd")]
    t = delta_text(newfail)
    checks.append(("a NEW failure behind two persistent reds is surfaced",
                   "RAN-OK -> RAN-FAILED" in t and "gap" in t))
    bad = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"  {'ok  ' if ok else 'FAIL'}  {n}")
    print(f"\n  {len(checks) - len(bad)} of {len(checks)} controls pass")
    return 1 if bad else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    # THE NESTING GUARD: check first, set second. Setting without checking is not a guard.
    if os.environ.get(SENTINEL):
        print(f"REFUSING: {SENTINEL} is set, so a cycle is already running in this process tree. "
              f"A runner that can invoke itself is how this fleet forked 1,600 processes once.")
        return 2
    os.environ[SENTINEL] = "1"

    args = sys.argv[1:]
    _lock = take_lock()
    if _lock is None:
        print("  another cycle is already running (flock held); this one exits without running.")
        print("  That is not a failure: a cycle is a loop iteration, and two at once would have")
        print("  the second's questions file read by the first's harvest.")
        return 0
    def opt(flag, default):
        return args[args.index(flag) + 1] if flag in args else default
    project = opt("--project", os.environ.get("SWARM_PROJECT", "zebrafish-flight"))
    os.environ["SWARM_PROJECT"] = project
    cycles = max(1, min(MAX_CYCLES, int(opt("--cycles", "1"))))
    n_chal = int(opt("--challenge", "5"))
    write = "--write" in args

    OUT.mkdir(parents=True, exist_ok=True)
    # Snapshot the newest PRIOR record before writing any of our own, so the delta below
    # compares against the last cycle and not against this one.
    prior = previous_record(project)
    print("=" * 78)
    print(f"SWARM CYCLE -- project {project!r}, {cycles} cycle(s), "
          f"{'WRITING' if write else 'dry (no spend)'}")
    print("=" * 78)

    recs = []
    for i in range(cycles):
        print(f"\n  --- cycle {i + 1} of {cycles} ---")
        rec = one_cycle(project, n_chal, write)
        recs.append(rec)
        p = OUT / f"{project}-{rec['at'].replace(':', '').replace('-', '')[:15]}.json"
        p.write_text(json.dumps(rec, indent=1))

    if recs:
        report_delta(prior, recs[-1])

    print("\n" + "-" * 78)
    total = {}
    for r in recs:
        for k, v in r["counts"].items():
            total[k] = total.get(k, 0) + v
    print(f"  {total}")
    ok = total.get("RAN-OK", 0)
    ran = ok + total.get("RAN-FAILED", 0) + total.get("ERRORED", 0)
    skipped = total.get("SKIPPED", 0)
    print(f"  {ok} of {ran} stages that RAN passed; {skipped} SKIPPED and counted as neither.")
    if skipped:
        print("  A cycle with skipped stages is NOT a green cycle. The skipped ones are named")
        print("  in the record with their reason, so a later reader cannot mistake them for")
        print("  checks that found nothing.")
    print(f"  records under {OUT}")
    print("-" * 78)
    # Exit code: 0 only if everything that ran passed AND nothing was skipped.
    if total.get("RAN-FAILED") or total.get("ERRORED"):
        return 1
    return 0 if not skipped else 1


if __name__ == "__main__":
    raise SystemExit(main())
