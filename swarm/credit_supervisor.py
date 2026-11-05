#!/usr/bin/env python3
"""Keep expiring Console API credit being spent, by topping up panel arms when burn falls short.

WHY. Twice in two iterations every panel arm finished and nothing noticed. Burn fell from
$18.08/h to ~$7/h while the binding tenant needed $4.47/h, and the shortfall was only caught
because a human-driven check happened to run. Credit that expires unspent is gone; an arm that
exits is silent. This closes that loop.

WHAT IT WILL NOT DO, and these are hard rules rather than defaults:
  * It NEVER spends api_allen or any Allen-Institute-billed tenant. EXCLUDED below is checked
    against every tenant name before that tenant can be chosen, and the owner's instruction is
    "not using my credit card nor allen_api or ent_allen".
  * It NEVER launches anything that bills a credit card. It only runs api_challenge.py, which
    spends Console API grant credit through `orchestra api-credits call`.
  * It caps concurrency at MAX_ARMS. The point is to keep credit draining, not to fork-bomb a
    shared 8-core host that other sessions are using.

HOW THE RATE IS MEASURED. Balances are sampled into a state file. A rate needs two samples, so
the FIRST run never launches anything -- it records a sample and says so. That is deliberate:
launching on one sample means launching on no measurement at all.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import subprocess
import sys

#: Never spend these, whatever the arithmetic says. Owner instruction, not a tunable.
EXCLUDED = ("api_allen", "ent_allen", "allen_api", "max_allen")
MAX_ARMS = 6
ARM = ["python3", "-u", "swarm/api_challenge.py", "60", "--repanel", "--write"]
STATE = pathlib.Path(os.environ.get("MS_CREDIT_STATE",
                                    "/tmp/claude-1000/ms-credit-supervisor.json"))


def balances() -> dict[str, tuple[float, str]]:
    r = subprocess.run(["orchestra", "api-credits", "list"],
                       capture_output=True, text=True, timeout=240)
    out = {}
    for ln in r.stdout.splitlines():
        p = ln.split()
        if len(p) > 6 and p[0].startswith("api_") and p[2] == "yes":
            try:
                out[p[0]] = (float(p[4]), p[6])
            except (ValueError, IndexError):
                pass
    return out


def running_arms() -> int:
    # Match on the script path, never on a pattern this command's own line contains.
    r = subprocess.run(["pgrep", "-fc", "api_challenge.py"], capture_output=True, text=True)
    try:
        return max(0, int(r.stdout.strip()) - 1)   # minus the pgrep itself
    except ValueError:
        return 0


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    bal = balances()
    for name in list(bal):
        if name in EXCLUDED:
            print(f"  {name}: EXCLUDED by owner instruction, not considered")
            del bal[name]
    if not bal:
        print("  no spendable tenant after exclusions")
        return 0

    prior = {}
    if STATE.exists():
        try:
            prior = json.loads(STATE.read_text())
        except json.JSONDecodeError:
            prior = {}

    # The binding tenant is the one needing the highest $/h to finish before it expires.
    need = {}
    for t, (amount, expiry) in bal.items():
        try:
            exp = dt.datetime.fromisoformat(expiry.replace("Z", "+00:00"))
        except ValueError:
            continue
        hours = (exp - now).total_seconds() / 3600
        if hours > 0:
            need[t] = (amount / hours, amount, hours)
    if not need:
        print("  no tenant with a future expiry")
        return 0
    binding = max(need, key=lambda t: need[t][0])
    rate_needed, amount, hours = need[binding]
    print(f"  binding tenant {binding}: ${amount:.2f}, {hours:.1f} h -> needs ${rate_needed:.2f}/h")

    observed = None
    if prior.get("at") and binding in prior.get("bal", {}):
        dtsec = (now - dt.datetime.fromisoformat(prior["at"])).total_seconds()
        if dtsec > 120:
            spent = prior["bal"][binding] - amount
            observed = spent / (dtsec / 3600)
            print(f"  observed ${observed:.2f}/h over the last {dtsec/60:.0f} min")

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"at": now.isoformat(),
                                 "bal": {t: v[0] for t, v in bal.items()}}))

    if observed is None:
        print("  FIRST SAMPLE: a rate needs two. Recorded; launching nothing this run.")
        return 0

    arms = running_arms()
    print(f"  {arms} arm(s) running, cap {MAX_ARMS}")
    if observed >= rate_needed:
        print("  on track; no action")
        return 0
    if arms >= MAX_ARMS:
        print(f"  BEHIND by ${rate_needed-observed:.2f}/h but at the arm cap; not launching")
        return 0
    want = min(MAX_ARMS - arms, 3)
    print(f"  BEHIND by ${rate_needed-observed:.2f}/h -> launching {want} arm(s) on {binding}")
    for _ in range(want):
        subprocess.Popen(ARM + ["--tenant", binding],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
