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

DEADLINE = 1793864700          # kept: the CLOUD pool's expiry, now past. See cloud_pool_done().
START_CREDIT = 998.48          # kept: that pool's size, for the historical line only.
EXCLUDED_TENANTS = ("api_allen",)   # owner's standing instruction; never spend, never count
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


def console_credit():
    """Per-tenant Console API credit, the pool that is actually live and expiring.

    Returns (rows, total_spendable, soonest). Reads `orchestra api-credits list` rather than
    hard-coding a number, because a hard-coded total is how this monitor came to be watching a
    pool that no longer exists. api_allen is excluded by the owner's standing instruction.
    """
    import re as _re
    out = sh("orchestra api-credits list", timeout=200) or ""
    rows = []
    for ln in out.splitlines():
        m = _re.match(r"\s*(api_\S+)\s+\S+\s+(yes|no)\s+(yes|no)\s+([\d.]+)\s+(\d+)\s+(\S+)", ln)
        if not m:
            continue
        tenant, on, _key, left, _of, exp = m.groups()
        if tenant in EXCLUDED_TENANTS:
            continue
        rows.append({"tenant": tenant, "on": on == "yes", "left": float(left), "expires": exp})
    spendable = [r for r in rows if r["on"]]
    total = sum(r["left"] for r in spendable)
    soonest = min(spendable, key=lambda r: r["expires"]) if spendable else None
    return rows, total, soonest


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
    print(f"  cloud       ${left:.2f} left of ${START_CREDIT:.2f} -- this pool is FINISHED and "
          f"its deadline is past; kept as history, not as an alarm")
    try:
        crows, ctotal, csoon = console_credit()
    except Exception as e:                                   # noqa: BLE001
        crows, ctotal, csoon = [], 0.0, None
        print(f"  console     COULD NOT READ ({type(e).__name__}) -- not reported as zero")
    if crows:
        print(f"  console     ${ctotal:.2f} spendable across {len([r for r in crows if r['on']])} "
              f"tenant(s), api_allen excluded by standing instruction")
        for r in sorted(crows, key=lambda x: x["expires"]):
            flag = "" if r["on"] else "  (OFF, not spendable)"
            print(f"                ${r['left']:>7.2f}  {r['tenant']:<14} expires {r['expires'][:10]}{flag}")
        if csoon:
            print(f"  nearest     ${csoon['left']:.2f} on {csoon['tenant']} expires "
                  f"{csoon['expires'][:10]} -- that is the amount actually at risk first, "
                  f"NOT the total")
    btxt = f"${burn:.0f}/h observed" if burn is not None else f"not yet measurable ({dt_h*60:.0f} min of baseline, need 15)"
    print(f"  burn        {btxt}   ${need:.0f}/h NEEDED to finish   -> projected leftover ${max(0,projected):.0f}")
    print(f"  sessions    {running} running        monitor.log {mon_age:.0f} min old")
    print(f"  knowledge   {claims} claims ({sup} superseded), {chal} challenges resolved, {answered} subproblems answered")
    print(f"  content     {laws} law entries, {branches} claude branches, {commits_1h} commits in the last hour")

    alarms = []
    cloud_done = left <= 0.01 or hours_left <= 0
    if not cloud_done:
        if mon_age > 20:
            alarms.append(f"monitor.log is {mon_age:.0f} min stale -- the generator may be dead")
        if running < 10:
            alarms.append(f"only {running} sessions running; credit cannot be spent at this rate")
        if hours_left > 0.5 and burn is not None and burn < need * 0.6:
            alarms.append(f"burn ${burn:.0f}/h is below the ${need:.0f}/h needed; "
                          f"~${max(0,projected):.0f} will expire unused")
    # Live pool: alarm on the amount at risk SOONEST, not the total. Quoting the total as
    # "expiring" overstates it -- the four tenants expire on three different dates.
    if csoon:
        import datetime as _dt
        try:
            exp = _dt.datetime.fromisoformat(csoon["expires"].replace("Z", "+00:00"))
            days = (exp - _dt.datetime.now(_dt.timezone.utc)).total_seconds() / 86400
        except Exception:                                    # noqa: BLE001
            days = None
        if days is not None and days < 3 and csoon["left"] > 50:
            alarms.append(f"${csoon['left']:.2f} on {csoon['tenant']} expires in {days:.1f} days "
                          f"and is largely unspent (total spendable ${ctotal:.2f} across "
                          f"{len([r for r in crows if r['on']])} tenants expiring on "
                          f"{len({r['expires'][:10] for r in crows if r['on']})} different dates)")
    if prev and claims <= prev.get("claims", 0) and commits_1h == 0:
        alarms.append("no new claims and no commits in the last hour -- nothing is being learned")

    if alarms:
        print("\n  ALARMS:")
        for a in alarms:
            print(f"    ! {a}")
        if cloud_done:
            print("\n  NOTE: the cloud pool is finished, so its generator/session alarms are "
                  "suppressed rather than fired for ever.")
        else:
            print("\n  REMEDY: python3 /data/swarm/generate.py 40   (refills the cloud queue; "
                  "safe to run repeatedly)")
    else:
        print("\n  no alarms")

    st = {"t": now, "left": left, "claims": claims, "running": running, "laws": laws,
          "base_t": base_t, "base_left": base_left}
    if abs(base_left - left) > 0.01 and dt_h >= 0.25:      # baseline consumed; start a fresh one
        st["base_t"], st["base_left"] = now, left
    json.dump(st, open(STATE, "w"))
    # Exit code must track the LIVE pool. Keying it to the finished cloud pool returned 2
    # (stalled) permanently, which is the same false-positive failure as the alarms above.
    if not cloud_done and (mon_age > 20 or running < 4):
        return 2
    return 1 if alarms else 0


if __name__ == "__main__":
    sys.exit(main())
