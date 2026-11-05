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

ONE WRITER. Every run REWRITES the state file, so running this by hand while the heartbeat loop
is running resets the clock the loop depends on and can keep it permanently under the 120 s
floor. Use MS_CREDIT_STATE to point an ad-hoc run at a different file, or just let the loop own
this one.
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
#: Top up whenever fewer than this many arms are alive, WHATEVER the measured rate says.
#: The arms==0 special case was not enough: with ONE arm left, the observed rate still reflects
#: the three or four that were running during the sample window, so the supervisor reports "on
#: track" while the fleet is collapsing. Measured 2026-11-05 -- arms fell 4 -> 1 while
#: api_outlook2 went $151 -> $144, and the next cycle would have taken no action. Zero was an
#: arbitrary floor; the real rule is that a DECLINING arm count predicts the future and a
#: trailing average does not.
MIN_ARMS = 3
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
    """Count arms by their ACTUAL process, not by a substring any command line may contain.

    `pgrep -fc api_challenge.py` minus one was wrong, and it was wrong in the direction that
    silences the supervisor. Measured 2026-11-05: a watcher I started to observe this very
    function had `pgrep -fc api_challenge.py` in its own command line, so pgrep matched it and
    the supervisor counted a monitoring process as a running arm. AGENTS.md section 6b documents
    exactly this -- "a pgrep -f 'foo' inside a command whose own text contains foo matches
    itself" -- and subtracting a fixed 1 only ever accounts for the pgrep, never for the other
    processes that mention the pattern.

    Reading /proc and requiring the EXECUTABLE to be python and the script to appear as its own
    argument cannot match a shell whose text merely quotes the name.
    """
    n = 0
    for pid in pathlib.Path("/proc").iterdir():
        if not pid.name.isdigit():
            continue
        try:
            argv = (pid / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        argv = [a.decode("utf-8", "replace") for a in argv if a]
        if not argv or "python" not in os.path.basename(argv[0]):
            continue
        if any(a.endswith("api_challenge.py") for a in argv[1:]):
            n += 1
    return n


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

    observed, why = None, "no prior sample"
    if prior.get("at") and binding in prior.get("bal", {}):
        dtsec = (now - dt.datetime.fromisoformat(prior["at"])).total_seconds()
        if dtsec > 120:
            spent = prior["bal"][binding] - amount
            observed = spent / (dtsec / 3600)
            print(f"  observed ${observed:.2f}/h over the last {dtsec/60:.0f} min")
        else:
            # NOT the same as having no sample, and saying so matters: a supervisor that has
            # been running for hours but prints "first sample" reads as broken state. This
            # branch means the previous sample is simply too close in time to divide by.
            why = f"prior sample only {dtsec:.0f}s old; too recent to derive a rate"

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"at": now.isoformat(),
                                 "bal": {t: v[0] for t, v in bal.items()}}))

    if observed is None:
        print(f"  NO RATE YET ({why}). Recorded; launching nothing this run.")
        return 0

    arms = running_arms()
    print(f"  {arms} arm(s) running, cap {MAX_ARMS}")
    # THE OBSERVED RATE IS A LAGGING INDICATOR AND THE ARM COUNT IS THE LEADING ONE.
    # Measured 2026-11-05, cycle 2: it printed "observed $8.42/h ... 0 arm(s) running ... on
    # track; no action". Both statements were true and the conclusion was wrong -- that $8.42/h
    # was earned by arms that had since exited, so the forward rate was about to be zero. A
    # supervisor that waits for the average to fall always acts one interval too late, and on a
    # 15-minute cycle near an expiry that is real money. With nothing running, past burn
    # predicts nothing.
    if arms < MIN_ARMS and amount > 0:
        want = min(MAX_ARMS - arms, MIN_ARMS - arms)
        why = ("NOTHING RUNNING" if arms == 0 else
               f"ONLY {arms} ARM(S) LEFT, below the floor of {MIN_ARMS}")
        print(f"  {why} -- launching {want} arm(s) on {binding} regardless of the "
              f"observed rate, which was earned by arms that have since exited")
        for _ in range(want):
            subprocess.Popen(ARM + ["--tenant", binding],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        return 0
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
