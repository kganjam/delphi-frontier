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

import json
import os
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
    mark = {"RAN-OK": "ok", "RAN-FAILED": "FAILED", "ERRORED": "ERROR"}[rec["status"]]
    print(f"  {name:<12} {rec['status']:<10} exit={rec['exit']} {rec['seconds']}s  {mark}")
    return rec


def one_cycle(project: str, n_challenge: int, write: bool) -> dict:
    py = sys.executable
    stages = []
    # 1. Is the project reading the right literature at all?
    stages.append(run_stage("gap", [py, str(HERE / "corpus_gap.py")]))
    # 2. Adversarial review. The only stage that SPENDS, so it is the only one gated on --write.
    stages.append(run_stage(
        "challenge", [py, str(HERE / "api_challenge.py"), str(n_challenge), "--write"],
        None if write else "needs --write: this stage spends Console API credit"))
    # 3. Synthesis.
    stages.append(run_stage("synthesis", [py, str(HERE / "design_chain.py")]))
    # 4. Conformance.
    stages.append(run_stage("specs", [py, str(HERE / "check_specs.py")]))
    stages.append(run_stage("vacuity", [py, str(HERE / "check_vacuity.py")]))
    # 5. Publish, ALWAYS dry-run. It asserts no network module is loaded and writes to disk.
    stages.append(run_stage("publish", [py, str(HERE / "publish_dryrun.py")]))
    # 6. Did anything actually move?
    stages.append(run_stage("progress", [py, str(HERE / "progress.py")]))

    counts = {}
    for s in stages:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    return {"project": project, "at": datetime.now(timezone.utc).isoformat(),
            "stages": stages, "counts": counts}


def main() -> int:
    # THE NESTING GUARD: check first, set second. Setting without checking is not a guard.
    if os.environ.get(SENTINEL):
        print(f"REFUSING: {SENTINEL} is set, so a cycle is already running in this process tree. "
              f"A runner that can invoke itself is how this fleet forked 1,600 processes once.")
        return 2
    os.environ[SENTINEL] = "1"

    args = sys.argv[1:]
    def opt(flag, default):
        return args[args.index(flag) + 1] if flag in args else default
    project = opt("--project", os.environ.get("SWARM_PROJECT", "zebrafish-flight"))
    os.environ["SWARM_PROJECT"] = project
    cycles = max(1, min(MAX_CYCLES, int(opt("--cycles", "1"))))
    n_chal = int(opt("--challenge", "5"))
    write = "--write" in args

    OUT.mkdir(parents=True, exist_ok=True)
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
