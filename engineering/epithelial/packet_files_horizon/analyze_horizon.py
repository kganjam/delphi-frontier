"""Read closure at each declared horizon from one trajectory per arm. Criterion frozen here.

This file's own sha256 goes into every report, so a report can be checked against the
criterion that produced it. There is no flag that changes a rule.

What it does NOT do: it never compares against the previous FAIL, never recomputes lambda*/J
and never issues a pass or fail on the J-scaling question. That result is frozen elsewhere and
this study cannot revise it. The only question here is whether a bracket moves with horizon.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import re
from pathlib import Path

ARM = re.compile(r"^S-k(?P<k>\d+)-J(?P<J>[\d.]+)-lamV(?P<lam>[\d.]+)-s(?P<seed>\d+)$")
TOTAL_NODES = 40000
HORIZONS = (1000, 2000, 4000, 8000)


def criterion_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def read_arm(d: Path) -> dict | None:
    log = d / "logger.csv"
    if not log.exists():
        return None
    by = collections.defaultdict(float)
    bad = 0
    for r in csv.DictReader(log.open(), delimiter="\t"):
        try:
            t, v = float(r["time"]), float(r["cell.volume"])
            if not (math.isfinite(t) and math.isfinite(v)):
                bad += 1
                continue
            by[t] += v
        except (KeyError, TypeError, ValueError):
            bad += 1
    if not by:
        return None
    ts = sorted(by)
    gap = {t: TOTAL_NODES - by[t] for t in ts}
    first_zero = next((t for t in ts if gap[t] <= 0), None)
    per_h = {}
    for h in HORIZONS:
        within = [t for t in ts if t <= h]
        if not within:
            per_h[str(h)] = dict(observed=False)
            continue
        closed = first_zero is not None and first_zero <= h
        i = max(0, int(len(within) * 0.8) - 1)
        per_h[str(h)] = dict(observed=True, closed=closed,
                             closure_time=(first_zero if closed else None),
                             gap_at_h=gap[within[-1]],
                             delta_last_20pct=gap[within[i]] - gap[within[-1]],
                             still_shrinking=(gap[within[i]] - gap[within[-1]]) > 1)
    return dict(t_end=ts[-1], gap0=gap[ts[0]], nonfinite=bad, per_horizon=per_h,
                reached_full_horizon=ts[-1] >= max(HORIZONS))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--reproduction", default=None)
    a = ap.parse_args()
    proto = json.loads(Path(a.protocol).read_text())
    root = Path(a.out)
    repro = json.loads(Path(a.reproduction).read_text()) if a.reproduction and Path(a.reproduction).exists() else None
    uninterpretable = set(repro["diverged_arms"] + repro["missing_arms"]) if repro else set()

    arms, missing = {}, []
    for spec in proto["arms"]:
        r = read_arm(root / spec["id"])
        (arms.__setitem__(spec["id"], dict(spec=spec, **r)) if r else missing.append(spec["id"]))

    # brackets per (gap, J, seed) at each horizon, over the lambda_V values present here
    cells = collections.defaultdict(lambda: collections.defaultdict(dict))
    for name, A in arms.items():
        if name in uninterpretable:
            continue
        m = ARM.match(name)
        key = f"k{m['k']}-J{float(m['J']):g}-s{m['seed']}"
        for h in HORIZONS:
            ph = A["per_horizon"][str(h)]
            if ph.get("observed"):
                cells[key][h][float(m["lam"])] = ph["closed"]

    brackets, moved = {}, {}
    for key, per_h in cells.items():
        brackets[key] = {}
        for h in HORIZONS:
            lam = per_h.get(h, {})
            cl = [v for v, c in lam.items() if c]
            ar = [v for v, c in lam.items() if not c]
            if cl and ar and max(cl) < min(ar):
                brackets[key][str(h)] = dict(state="BRACKETED", lo=max(cl), hi=min(ar))
            else:
                brackets[key][str(h)] = dict(
                    state="UNRESOLVED",
                    why=("all selected lambda_V closed" if not ar else
                         "none of the selected lambda_V closed" if not cl else
                         "closed and arrested interleave"),
                    note="UNRESOLVED is not a pass and is not dropped")
        seq = [brackets[key][str(h)] for h in HORIZONS]
        b0, bN = seq[0], seq[-1]
        moved[key] = dict(
            baseline_1000=b0, final=bN,
            moved=(b0.get("lo"), b0.get("hi")) != (bN.get("lo"), bN.get("hi")),
            monotone=all(
                (seq[i].get("lo") or 0) <= (seq[i + 1].get("lo") or 0) for i in range(len(seq) - 1)),
        )

    ctrl = {}
    for name, A in arms.items():
        role = A["spec"]["role"]
        if role.startswith("POSITIVE"):
            ph = A["per_horizon"]["1000"]
            ctrl[name] = dict(kind="positive", passed=bool(ph.get("closed")),
                              requirement="must still close by horizon 1000",
                              closure_time=ph.get("closure_time"))
        elif role.startswith("NEGATIVE"):
            ph = A["per_horizon"][str(max(HORIZONS))]
            ctrl[name] = dict(kind="negative", passed=not ph.get("closed"),
                              requirement="must NOT close by the final horizon",
                              gap_at_final=ph.get("gap_at_h"))

    censored = {n: A["per_horizon"][str(max(HORIZONS))]["delta_last_20pct"]
                for n, A in arms.items()
                if A["per_horizon"][str(max(HORIZONS))].get("still_shrinking")}

    # A verdict over an empty set is not a verdict. If the reproduction control did not pass,
    # or nothing was evaluable, there is NOTHING to support the hypothesis with -- and an
    # earlier version of this file answered "SUPPORTED: no selected bracket moved" in exactly
    # that situation, because no bracket had moved for want of any bracket at all. Caught by
    # the end-to-end fixture before dispatch.
    # A cell counts as evaluable only if it HAS a bracket at the baseline horizon. A cell that
    # is UNRESOLVED at every horizon has no bracket to move, so counting it would make "nothing
    # moved" vacuous a second time, one level below the reproduction guard. Caught by the H3
    # control, which supplies arms that never close.
    evaluable = sum(1 for v in moved.values() if v["baseline_1000"].get("state") == "BRACKETED")
    any_moved = any(v["moved"] for v in moved.values())
    repro_ok = (repro is not None and repro["verdict"] == "REPRODUCED")
    if repro is None:
        outcome = "UNINTERPRETABLE: the reproduction control was not run"
    elif not repro_ok:
        outcome = (f"UNINTERPRETABLE: reproduction verdict {repro['verdict']}. "
                   f"{len(uninterpretable)} arm(s) do not reproduce their original prefix, so no "
                   f"horizon reading may be taken from them.")
    elif evaluable == 0:
        outcome = ("UNRESOLVED: no cell produced a bracket at the baseline horizon, so there is "
                   "nothing whose motion could be observed across horizons")
    elif any_moved:
        outcome = "NOT SUPPORTED: at least one bracket moved with horizon"
    else:
        outcome = f"SUPPORTED at these horizons: none of the {evaluable} evaluable brackets moved"
    report = dict(
        schema="frontier.epithelial-horizon-result.v1",
        criterion=dict(source_file=Path(__file__).name, criterion_sha256=criterion_sha256(),
                       horizons=list(HORIZONS),
                       hypothesis=proto["hypothesis"]["H"],
                       falsified_if=proto["hypothesis"]["falsified_if"]),
        scope="observation-horizon dependence only. This report does NOT revisit the frozen "
              "fixed-horizon FAIL and cannot turn it into a pass.",
        arms_declared=len(proto["arms"]), arms_read=len(arms), arms_missing=missing,
        uninterpretable_by_reproduction=sorted(uninterpretable),
        reproduction_verdict=(repro["verdict"] if repro else "NOT CHECKED"),
        hypothesis_outcome=outcome,
        evaluable_cells=evaluable,
        outcome_is_vacuous_guarded=True,
        brackets_by_horizon=brackets, bracket_motion=moved,
        controls=ctrl,
        censored_at_final_horizon=dict(
            arms=censored,
            note="still shrinking at the final horizon. Descriptive: a finite window bounds "
                 "nothing about closure beyond it."),
        per_arm=arms)
    Path(a.report).write_text(json.dumps(report, indent=1, default=float))
    print(f"{report['hypothesis_outcome']}  (reproduction: {report['reproduction_verdict']})")
    for n, v in ctrl.items():
        print(f"  control {v['kind']:8s} {n:26s} {'PASS' if v['passed'] else 'FAIL'}")
    bad_ctrl = [n for n, v in ctrl.items() if not v["passed"]]
    raise SystemExit(2 if (missing or uninterpretable or bad_ctrl or not evaluable) else 0)


if __name__ == "__main__":
    main()
