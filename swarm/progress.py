#!/usr/bin/env python3
"""One command that answers: is anything actually progressing, and will the credit be spent?

Written because "the monitor is alive" and "the monitor is working" look identical from outside, and
that confusion cost five hours and ~$900 of expiring credit on 2026-11-03. Every check here reports a
NUMBER and a FRESHNESS, never a status word: a thing that has not changed in an hour is not working,
whatever it says about itself.

Exit code is the alarm: 0 healthy, 1 degraded, 2 stalled. Run it from a loop.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

DEADLINE = 1793864700          # 2026-11-04 23:45 PST, when cloud-session credit expires
START_CREDIT = 998.48
PGBASE = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm", "-tAq"]
REPO = "/data/worktrees/delphi-frontier/swarm-arch"
STATE = "/data/swarm/progress-state.json"


def env():
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q1(sql, default="0"):
    try:
        r = subprocess.run(PGBASE + ["-c", sql], capture_output=True, text=True, env=env(), timeout=60)
        return (r.stdout.strip() or default)
    except Exception:
        return default


def sh(cmd, cwd=None, timeout=90):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def credit():
    out = sh("orchestra cloud credit", timeout=200)
    tot = 0.0
    for line in out.split("\n"):
        p = line.split()
        if len(p) >= 2 and "usable" in line:
            try:
                tot += float(p[1])
            except ValueError:
                pass
    return tot


def main() -> int:
    now = time.time()
    hours_left = max(0.0, (DEADLINE - now) / 3600)
    prev = {}
    if os.path.exists(STATE):
        try:
            prev = json.load(open(STATE))
        except Exception:
            prev = {}

    left = credit()
    spent = START_CREDIT - left
    running = int(q1("select count(*) from agent_session where status in ('running','working')"))
    claims = int(q1("select count(*) from claim"))
    chal = int(q1("select count(*) from challenge where outcome is not null and outcome<>'not-run'"))
    sup = int(q1("select count(*) from claim where superseded_by is not null"))
    answered = int(q1("select count(*) from subproblem where status='answered'"))

    laws = len([f for f in os.listdir(f"{REPO}/library/laws") if f.endswith(".yaml")]) \
        if os.path.isdir(f"{REPO}/library/laws") else 0
    commits_1h = int(sh("git log --oneline --since='1 hour ago' --all | wc -l", cwd=REPO) or 0)
    branches = int(sh("git branch -r 2>/dev/null | grep -c 'origin/claude/'", cwd=REPO) or 0)

    mon_age = (now - os.path.getmtime("/data/swarm/monitor.log")) / 60 \
        if os.path.exists("/data/swarm/monitor.log") else 1e9

    # Burn projection. The only question that matters before the deadline.
    # The credit endpoint updates in batches, so two samples minutes apart can read identical and
    # produce a spurious "$0/h, nothing is being spent" alarm while 30 sessions are billing. Require
    # a baseline long enough for the figure to have moved, and keep the LAST baseline that did move
    # rather than overwriting it every run -- otherwise a fast loop can never measure a burn at all.
    base_t, base_left = prev.get("base_t", now), prev.get("base_left", left)
    dt_h = (now - base_t) / 3600
    burn = ((base_left - left) / dt_h) if dt_h >= 0.25 else None   # need >= 15 min of baseline
    need = (left / hours_left) if hours_left > 0.1 else float("inf")
    projected = (left - burn * hours_left) if burn is not None else left

    print(f"=== progress {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')} ===")
    print(f"  credit      ${left:.2f} left of ${START_CREDIT:.2f}  (spent ${spent:.2f})  {hours_left:.1f}h to expiry")
    btxt = f"${burn:.0f}/h observed" if burn is not None else f"not yet measurable ({dt_h*60:.0f} min of baseline, need 15)"
    print(f"  burn        {btxt}   ${need:.0f}/h NEEDED to finish   -> projected leftover ${max(0,projected):.0f}")
    print(f"  sessions    {running} running        monitor.log {mon_age:.0f} min old")
    print(f"  knowledge   {claims} claims ({sup} superseded), {chal} challenges resolved, {answered} subproblems answered")
    print(f"  content     {laws} law entries, {branches} claude branches, {commits_1h} commits in the last hour")

    alarms = []
    if mon_age > 20:
        alarms.append(f"monitor.log is {mon_age:.0f} min stale -- the generator may be dead")
    if running < 10:
        alarms.append(f"only {running} sessions running; credit cannot be spent at this rate")
    if hours_left > 0.5 and burn is not None and burn < need * 0.6:
        alarms.append(f"burn ${burn:.0f}/h is below the ${need:.0f}/h needed; ~${max(0,projected):.0f} will expire unused")
    if prev and claims <= prev.get("claims", 0) and commits_1h == 0:
        alarms.append("no new claims and no commits in the last hour -- nothing is being learned")

    if alarms:
        print("\n  ALARMS:")
        for a in alarms:
            print(f"    ! {a}")
        print("\n  REMEDY: python3 /data/swarm/generate.py 40   (refills the queue; safe to run repeatedly)")
    else:
        print("\n  no alarms")

    st = {"t": now, "left": left, "claims": claims, "running": running, "laws": laws,
          "base_t": base_t, "base_left": base_left}
    if abs(base_left - left) > 0.01 and dt_h >= 0.25:      # baseline consumed; start a fresh one
        st["base_t"], st["base_left"] = now, left
    json.dump(st, open(STATE, "w"))
    return 2 if mon_age > 20 or running < 4 else (1 if alarms else 0)


if __name__ == "__main__":
    sys.exit(main())
