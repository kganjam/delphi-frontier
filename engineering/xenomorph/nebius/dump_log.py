#!/usr/bin/env python3
"""dump_log.py <aijob-id> <since-UTC> <until-UTC> <out.txt>: full job stdout via `nebius logging query --forward`,
paginated by nanosecond timestamp with (timestamp, message) de-duplication. `nebius ai job logs` caps at 1000 lines
with 1-second timestamps, which cannot page through multi-MB base64 returns."""
import json
import os
import subprocess
import sys

job, since, until, out = sys.argv[1:5]
N = os.path.expanduser("~/.nebius/bin/nebius")
LIMIT = int(os.environ.get("LIMIT", "5000"))
seen = set()
lines = []
cur = since
while True:
    r = subprocess.run([N, "--profile", "hackathon", "logging", "query", f'{{vmapp_id="{job}",container="job"}}',
                        "--bucket", "default", "--since", cur, "--until", until, "--forward", "--limit", str(LIMIT),
                        "--format", "json", "--timeout", "5m"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        sys.exit(f"query failed: {r.stderr[:500]}")
    page = [json.loads(x) for x in r.stdout.splitlines() if x.strip().startswith("{")]
    new = 0
    for e in page:
        key = (e["timestamp"], e["message"])
        if key in seen:
            continue
        seen.add(key)
        lines.append(e)
        new += 1
    print(f"page since {cur}: {len(page)} entries, {new} new, total {len(lines)}", file=sys.stderr)
    if len(page) < LIMIT or new == 0:
        if len(page) >= LIMIT and new == 0:
            sys.exit("stuck: a full page shares one timestamp window; raise LIMIT")
        break
    cur = page[-1]["timestamp"]
def ns(ts: str) -> tuple:
    """RFC3339 with trimmed trailing zeros ('...35.5182758Z'): string order is NOT time order, so parse."""
    head, _, frac = ts.rstrip("Z").partition(".")
    return (head, int((frac + "000000000")[:9]))


lines.sort(key=lambda e: ns(e["timestamp"]))
with open(out, "w") as f:
    for e in lines:
        f.write(e["message"] if e["message"].endswith("\n") else e["message"] + "\n")
with open(out + ".jsonl", "w") as f:  # timestamps kept: entries sharing one timestamp may come back in any order
    for e in lines:
        f.write(json.dumps({"t": e["timestamp"], "m": e["message"]}) + "\n")
print(len(lines), "lines ->", out)
