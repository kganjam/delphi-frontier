#!/usr/bin/env python3
"""Lift the execution environment out of committed result files and into run.environment (ASK D3).

SPEC-ASK section 4 item 1 asks for `run.environment`. The spec also said only 1 of 19 committed GPU
run families had environment capture at all. THAT WAS STALE: searching by CONTENT rather than by
filename finds substantive records -- torch build, python version, GPU model, CUDA version, driver
-- in 10 of 19. The capture was never the gap. The gap was that it sat in files linked to nothing,
which is what this script closes.

Nothing is inferred. A run gets an `environment` only if a file IT WROTE carries one, and the row
records which file, so the value can be re-read. A run with no such file keeps NULL and is reported
BY NAME -- NULL must mean "no record found", never "none looked for", or the column becomes another
mechanism walking an empty set.

    python3 backfill_run_environment.py            # report only
    python3 backfill_run_environment.py --write    # write run.environment
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
# RESOLVED FROM THIS FILE, not from the caller's cwd. As a relative path it silently reported
# "0 run(s) with an environment record, 14 without" when run from anywhere but the worktree root
# -- a wrong answer shaped exactly like a finding, and in the script whose own docstring says NULL
# must mean "no record found" and never "none looked for". Found by running it from /tmp.
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "compute")
# Normalised field -> the key spellings seen across the families. Kept explicit so a reviewer can
# disagree with a row, rather than inferred by fuzzy matching.
FIELDS = {
    "python": ("python", "python_version"),
    "torch": ("torch", "torch_version"),
    "gpu": ("gpu", "gpu_name", "device_name"),
    "cuda": ("cuda", "cuda_version"),
    "driver": ("driver", "driver_version"),
}


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def flatten(o, out: dict) -> None:
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                flatten(v, out)
            else:
                lk = k.lower()
                for norm, spellings in FIELDS.items():
                    if lk in spellings and norm not in out and v not in (None, ""):
                        out[norm] = str(v)[:200]
    elif isinstance(o, list):
        for v in o:
            flatten(v, out)


def find_env(run_tag: str) -> tuple[dict, str] | tuple[None, None]:
    """Search the family that owns this run_tag. Matched on the manifest, not on a guessed path."""
    for mf in glob.glob(os.path.join(ROOT, "**", f"manifest-{run_tag}.json"), recursive=True):
        fam = os.path.dirname(mf)
        best, best_path = {}, None
        for p in sorted(glob.glob(os.path.join(fam, "**", "*.json"), recursive=True)):
            if os.path.basename(p).startswith("manifest-"):
                continue
            try:
                d = json.load(open(p, encoding="utf-8", errors="replace"))
            except Exception:
                continue
            got: dict = {}
            flatten(d, got)
            if len(got) > len(best):
                best, best_path = got, os.path.relpath(p)
        if best:
            return best, best_path
    return None, None


def main() -> int:
    write = "--write" in sys.argv
    if not os.path.isdir(ROOT):
        print(f"  REFUSING: {ROOT} does not exist, so every run would report NO ENVIRONMENT "
              f"RECORD FOUND. That is a missing tree, not a measurement.", file=sys.stderr)
        return 2
    rows = q("select id, tool, coalesce(substring(notes from 'manifest-([a-z0-9]+)\\.json'),'') "
             "from run order by id")
    found = missed = 0
    for rid, tool, tag in rows:
        if not tag:
            continue
        e, path = find_env(tag)
        if not e:
            missed += 1
            print(f"  run {rid:>3} {tool:28} {tag:16} NO ENVIRONMENT RECORD FOUND")
            continue
        found += 1
        e["_source"] = path
        print(f"  run {rid:>3} {tool:28} {tag:16} {', '.join(f'{k}={v}' for k, v in e.items() if k != '_source')[:88]}")
        if write:
            lit = "'" + json.dumps(e).replace("'", "''") + "'"
            q(f"update run set environment = {lit}::jsonb where id = {int(rid)}")
    print(f"\n  {found} run(s) with an environment record, {missed} without "
          f"(those keep NULL and are named above, not silently skipped)")
    if not write:
        print("  report only; pass --write to store")
    return 0


if __name__ == "__main__":
    sys.exit(main())
