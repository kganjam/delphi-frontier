"""Timing gate: the probe must have WORKED, not merely finished quickly.

A probe that fails -- a missing shared library, a refused model, a killed process -- finishes
in milliseconds and would sail through a projection computed from elapsed time alone. So the
gate requires all of: exit 0, a logger with the expected header, at least one data row, every
value finite, and a projection that fits the declared budget and the whole-tree bound.

A failed probe writes its receipt, including the solver's own stdout tail, and stops the run
before any scientific arm starts.
"""
from __future__ import annotations

import argparse
import json
import math
import os

REQUIRED = ["time", "cell.id", "cell.center.x", "cell.center.y", "cell.volume", "cell.surface"]
PROBE_STOP_TIME = 500.0
DECLARED_PER_ARM_S = 55.0
ARM_STOP_TIME = 8000.0


def main() -> None:
    ap = argparse.ArgumentParser()
    for f in ("start", "end", "arms", "factor", "job-timeout", "workers", "probe-exit",
              "logger", "stdout", "report"):
        ap.add_argument(f"--{f}", required=True)
    a = ap.parse_args()
    elapsed = float(a.end) - float(a.start)
    prc = int(a.probe_exit)
    n_arms = len(json.loads(open(a.arms).read()))
    problems: list[str] = []

    if prc != 0:
        problems.append(f"probe exited {prc}")

    rows = finite_rows = 0
    try:
        with open(a.logger) as fh:
            header = [h.strip('"') for h in next(fh).rstrip("\n").split("\t")]
            if header != REQUIRED:
                problems.append(f"probe logger header {header}, expected {REQUIRED}")
            for ln in fh:
                if not ln.strip():
                    continue
                rows += 1
                try:
                    finite_rows += all(math.isfinite(float(x)) for x in ln.split("\t"))
                except ValueError:
                    pass
    except FileNotFoundError:
        problems.append("probe produced no logger.csv")
    except StopIteration:
        problems.append("probe logger.csv is empty")

    if rows and finite_rows != rows:
        problems.append(f"{rows - finite_rows} non-finite or unparseable probe rows")
    if rows == 0 and not any("logger" in p for p in problems):
        problems.append("probe logger.csv has no data rows")

    per_arm = (elapsed / PROBE_STOP_TIME) * ARM_STOP_TIME
    total_cpu = per_arm * n_arms
    wall = total_cpu / max(int(a.workers), 1)
    if per_arm > DECLARED_PER_ARM_S * float(a.factor):
        problems.append(f"projected {per_arm:.0f}s/arm exceeds declared "
                        f"{DECLARED_PER_ARM_S}s x {a.factor}")
    if wall > float(a.job_timeout):
        problems.append(f"projected wall {wall:.0f}s exceeds whole-tree bound {a.job_timeout}s")

    ok = not problems
    tail = open(a.stdout).read()[-2000:] if os.path.exists(a.stdout) else ""
    json.dump({"probe_stop_time": PROBE_STOP_TIME, "probe_wall_s": round(elapsed, 2),
               "probe_exit": prc, "probe_logger_rows": rows, "probe_rows_finite": finite_rows,
               "projected_per_arm_s": round(per_arm, 1),
               "declared_per_arm_s": DECLARED_PER_ARM_S,
               "projected_total_cpu_s": round(total_cpu, 1),
               "projected_wall_s_at_workers": round(wall, 1), "workers": int(a.workers),
               "job_timeout_s": float(a.job_timeout), "passed": ok, "problems": problems,
               "stdout_tail": tail,
               "rule": "the probe must exit 0 AND produce a non-empty, correctly-headed, finite "
                       "logger, AND the projection must fit. A failing probe is fast, so elapsed "
                       "time alone cannot be the gate."},
              open(a.report, "w"), indent=1)
    print(f"timing gate: probe rc={prc} {elapsed:.1f}s rows={rows} -> {per_arm:.0f}s/arm, "
          f"{wall:.0f}s wall at {a.workers} workers; "
          f"{'PASS' if ok else 'REFUSE: ' + '; '.join(problems)}")
    raise SystemExit(0 if ok else 4)


if __name__ == "__main__":
    main()
