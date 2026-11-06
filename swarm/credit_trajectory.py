#!/usr/bin/env python3
"""Project each tenant's credit forward and say which way it fails.

A credit pool fails in TWO opposite directions and a single balance shows neither:
it can run dry while work is still queued, or it can sit idle and EXPIRE UNUSED. Both
have happened here. api_gmail went 178.48 -> 40.96 in 11.9 hours (about 11-17 USD/hour)
while heavy stages ran, and then went flat -- two samples 90 seconds apart were identical,
which at that rate would have shown 0.40 USD. So "is the burn too fast or too slow" has no
answer from one reading, and the goal asks for both: use the credits before they expire,
and do not stall.

The check-ins already record the credit table every ~20 minutes. This reads that history,
fits a recent rate per tenant, and classifies the trajectory. Nothing is sampled live, so it
costs nothing and cannot itself move the number it measures.

    python3 swarm/credit_trajectory.py            # all tenants
    python3 swarm/credit_trajectory.py --hours 3  # fit over a shorter window
"""
from __future__ import annotations

import datetime
import glob
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CHECKINS = HERE.parent / "results" / "checkins"
#: TENANT EMAIL ON KEY LEFT OF EXPIRES SPENDABLE -- LEFT is field 5, and reading field 6 gives
#: the pool SIZE, which is constant and reads as "nothing is spending". Measured 2026-11-05.
ROW = re.compile(r"^(api_\w+)\s+\S+\s+(\w+)\s+(\w+)\s+([\d.]+)\s+([\d.]+)\s+(\S+)\s+(.*)$", re.M)


def history() -> dict[str, list[tuple[datetime.datetime, float, str, str]]]:
    out: dict[str, list] = {}
    for f in sorted(glob.glob(str(CHECKINS / "goal-*.txt"))):
        stamp = os.path.basename(f)[5:20]
        try:
            when = datetime.datetime.strptime(stamp, "%Y%m%dT%H%M%S")
        except ValueError:
            continue
        for m in ROW.finditer(open(f, errors="ignore").read()):
            tenant, _on, _key, left, _of, expires, spendable = m.groups()
            out.setdefault(tenant, []).append(
                (when, float(left), expires, spendable.strip()))
    for v in out.values():
        v.sort(key=lambda r: r[0])
    return out


def main() -> int:
    args = sys.argv[1:]
    win_h = float(args[args.index("--hours") + 1]) if "--hours" in args else 2.0
    h = history()
    if not h:
        print("  no check-in history parsed -- NOT reporting a projection.")
        return 1
    now = max(r[0] for v in h.values() for r in v)
    print(f"\n  {len(h)} tenant(s) across {sum(len(v) for v in h.values())} check-in rows; "
          f"latest {now:%Y-%m-%d %H:%M} UTC\n")
    # A RATE FITTED OVER A WINDOW THAT ALREADY CLOSED IS NOT THE CURRENT RATE. Measured
    # 2026-11-05: this printed "RUNS DRY in 2.8 h" from a window ending at the last check-in,
    # while two live samples 90 s apart were identical -- the burn had stopped after that
    # window. The age is printed and a stale history disqualifies the projection, because a
    # monitor that confidently extrapolates dead data is worse than one that says it cannot.
    age_h = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - now).total_seconds() / 3600
    stale = age_h > 0.75
    print(f"  last check-in is {age_h:.1f} h old"
          + ("  -- STALE: rates below describe that window, not now" if stale else ""))
    print(f"  {'tenant':<14}{'left':>9}{'rate/h':>9}  {'expiry':>7}  verdict")
    worst = 0
    for tenant, rows in sorted(h.items()):
        when, left, expires, spendable = rows[-1]
        # ONE WINDOW HIDES A TREND. Measured 2026-11-05: the 2 h fit said 14.86/h while the
        # most recent 20 minutes ran at about 1/h -- the burn was decelerating, and a single
        # rate reported either "runs dry in 2.8 h" or "idle" depending only on the window
        # chosen. Three windows are printed so the direction is visible.
        def fit(h_):
            rec = [r for r in rows if (when - r[0]).total_seconds() <= h_ * 3600]
            if len(rec) < 2:
                return None
            dt = (rec[-1][0] - rec[0][0]).total_seconds() / 3600
            return (rec[0][1] - rec[-1][1]) / dt if dt > 0 else None
        trend = [(h_, fit(h_)) for h_ in (1.0, win_h, 6.0)]
        rate = next((r for _h, r in trend if r is not None), 0.0) or 0.0
        try:
            exp = datetime.datetime.strptime(expires[:19], "%Y-%m-%dT%H:%M:%S")
            days = max(0.0, (exp - when).total_seconds() / 86400)
        except ValueError:
            days = float("nan")
        if not spendable.startswith("yes"):
            verdict = f"not spendable ({spendable[:34]})"
        elif rate <= 0:
            verdict = (f"IDLE -- ${left:.2f} expires UNUSED in {days:.1f} d "
                       f"unless work resumes")
            worst = max(worst, 1)
        else:
            dry_h = left / rate
            if dry_h < days * 24:
                verdict = f"RUNS DRY in {dry_h:.1f} h, {days:.1f} d before expiry"
                worst = max(worst, 2)
            else:
                verdict = f"on track: {dry_h:.0f} h of burn, {days:.1f} d to expiry"
        if stale and spendable.startswith("yes"):
            verdict = f"UNKNOWN -- history {age_h:.1f} h stale; last window ran {rate:.2f}/h"
            worst = max(worst, 1)
        tr = "  ".join(f"{h_:g}h:{('%.2f' % r) if r is not None else '--':>6}"
                       for h_, r in trend)
        print(f"  {tenant:<14}{left:>9.2f}{rate:>9.2f}  {days:>6.1f}d  {verdict}")
        if spendable.startswith("yes"):
            print(f"  {'':<14}{'rates':>9}  {tr}")
    print(f"\n  rate is fitted over the last {win_h:g} h of check-ins. A tenant at its "
          f"provider's\n  reserve floor is marked not spendable: that residue cannot be used "
          f"by anyone,\n  so it is not a shortfall anyone can close.")
    print("  IDLE and RUNS DRY are opposite failures and a single balance shows neither.")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
