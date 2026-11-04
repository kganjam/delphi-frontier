#!/usr/bin/env python3
"""Keep Nebius's single submission slot occupied, one job at a time, and fetch each result.

This endpoint allows ONE operation in flight across all 69 tools: a second submit returns
429 ADMISSION_LIMIT_REACHED regardless of which model it names. So the resource cannot be
maximised by fanning out -- it is a serial queue, and the only throughput lever is never leaving
the slot idle. Fanning out here produces 429s, not parallelism.

It also cannot be driven by hand, for a reason measured on this project: 8 of 8 completed
operations had never been fetched, because a finished operation and a fetched result look
identical from the operation log. Submit, poll and fetch therefore belong in one loop.

    python3 nebius_queue.py jobs.jsonl            # run every job in the file
    python3 nebius_queue.py jobs.jsonl --dry-run  # validate the file, submit nothing

Each line is one job:
    {"label": "...", "outdir": "...", "tool": "submit_esmfold2", "sequence": "...", "seed": 0}
    {"label": "...", "outdir": "...", "tool": "infer_proteinmpnn_native", "args": {...}}

Bounded by a deadline and an iteration cap, never by a condition another process must produce:
a loop waiting on a signal whose producer has died waits forever.
"""
from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "library", "tools"))
import nbx  # noqa: E402

sys.path.insert(0, HERE)
import fetch_results as fr  # noqa: E402
import submit_esmfold2 as se  # noqa: E402

POLL_EVERY = 30
MAX_WAIT = 3600          # per job
BACKOFF = 60             # the server's own retry_after on a 429


def submit_job(job: dict) -> str | None:
    tool = job["tool"]
    if tool == "submit_esmfold2":
        op, _ = se.submit(job["label"], job["sequence"], int(job.get("seed", 0)))
        return op
    args = dict(job["args"])
    args.setdefault("idempotency_key", f"ms-{job['label']}")
    out = nbx.call(tool, args)
    op = (out.get("operation_id") or out.get("id") or (out.get("operation") or {}).get("id"))
    if op:
        se.record(op, f"{job['label']} ({tool})")
    else:
        # Record even without an id: an unrecorded operation holds the slot and there is no
        # tool on this endpoint that lists pending operations.
        se.record("UNKNOWN", f"{job['label']} ({tool}) -- NO ID: {json.dumps(out)[:200]}")
    return op


def run_job(job: dict) -> bool:
    label = job["label"]
    print(f"\n=== {label} ({job['tool']}) ===", flush=True)
    op = None
    for attempt in range(10):
        try:
            op = submit_job(job)
            break
        except Exception as e:
            if "ADMISSION_LIMIT" in str(e) or "429" in str(e):
                print(f"  slot busy, waiting {BACKOFF}s (attempt {attempt + 1})", flush=True)
                time.sleep(BACKOFF)
                continue
            print(f"  submit failed: {type(e).__name__}: {str(e)[:300]}", flush=True)
            return False
    if not op:
        print("  no operation id; giving up on this job", flush=True)
        return False
    print(f"  operation {op}", flush=True)

    t0 = time.time()
    while time.time() - t0 < MAX_WAIT:
        try:
            st = fr.status_of(nbx.call("get_operation", {"operation_id": op})) or "?"
        except Exception as e:
            st = f"poll-error {type(e).__name__}"
        if st in ("succeeded", "success", "completed"):
            try:
                for n, p, b in fr.fetch_run(op, job["outdir"]):
                    print(f"  FETCHED {n} -> {p} ({b:,} bytes, sha256 verified)", flush=True)
                return True
            except Exception as e:
                print(f"  fetch failed: {type(e).__name__}: {str(e)[:300]}", flush=True)
                return False
        if st in ("failed", "cancelled", "canceled", "error", "expired"):
            print(f"  terminal: {st}", flush=True)
            return False
        print(f"  t+{int(time.time() - t0):4}s {st}", flush=True)
        time.sleep(POLL_EVERY)
    print(f"  gave up after {MAX_WAIT}s; operation {op} is still recorded and can be fetched later",
          flush=True)
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    jobs = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
    for j in jobs:
        for k in ("label", "outdir", "tool"):
            if k not in j:
                print(f"job missing '{k}': {json.dumps(j)[:200]}", file=sys.stderr)
                return 2
    print(f"{len(jobs)} job(s) queued")
    if "--dry-run" in sys.argv:
        for j in jobs:
            print(f"  would run {j['label']} ({j['tool']}) -> {j['outdir']}")
        return 0
    ok = sum(run_job(j) for j in jobs)
    print(f"\n{ok}/{len(jobs)} job(s) completed and fetched")
    return 0 if ok == len(jobs) else 1


if __name__ == "__main__":
    sys.exit(main())
