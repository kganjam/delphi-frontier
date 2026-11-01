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


def read_arm(d: Path, log_step: float) -> dict | None:
    """Read one trajectory and decide, per horizon, whether it is OBSERVED at all.

    A horizon is observed only if the trajectory actually covers it. Taking the last available
    sample as the value at a later horizon is what produced a demonstrated FALSE PASS: fed the
    original 1000-only logs, every arm reported horizons 2000/4000/8000 as observed and the
    analysis returned rc0 SUPPORTED. reached_full_horizon was computed and never used.

    One early-closure exception, deliberately separate and labelled: once the gap reaches 0 at
    t_c, "closed by h" is already true for every h >= t_c and no later sample can change it. So
    CLOSED is determinable without coverage to h; ARRESTED at h is not, and requires coverage.
    """
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
    t_end = ts[-1]
    first_zero = next((t for t in ts if gap[t] <= 0), None)
    finite = bad == 0

    per_h = {}
    for h in HORIZONS:
        expected = int(h / log_step) + 1
        got = sum(1 for t in ts if t <= h)
        covered = t_end >= h
        cardinality_ok = got >= expected
        closed_early = first_zero is not None and first_zero <= h
        if closed_early:
            # The OUTCOME is settled -- once the gap reaches 0 at t_c <= h, "closed by h" is true
            # and no later sample can change it -- but the trajectory was still only observed as
            # far as it ran. These are reported as two different things on purpose: `observed`
            # is coverage and nothing else, so no unobserved horizon can be read as unchanged.
            per_h[str(h)] = dict(
                observed=covered and cardinality_ok and finite,
                outcome_settled_by_early_closure=True,
                basis="closure at or before this horizon settles the outcome; coverage is "
                      "reported separately and is not implied by it",
                closed=True, closure_time=first_zero, coverage_to_h=covered,
                samples_to_h=got, samples_expected=expected, finite=finite)
            continue
        if not (covered and cardinality_ok and finite):
            per_h[str(h)] = dict(
                observed=False, closed=None,
                why=("trajectory ends at %g, short of this horizon" % t_end if not covered else
                     "only %d samples at or below this horizon, %d expected" % (got, expected)
                     if not cardinality_ok else "non-finite or unparseable values present"),
                t_end=t_end, coverage_to_h=covered, samples_to_h=got,
                samples_expected=expected, finite=finite)
            continue
        within = [t for t in ts if t <= h]
        i = max(0, int(len(within) * 0.8) - 1)
        per_h[str(h)] = dict(
            observed=True, basis="full coverage to this horizon", closed=False, closure_time=None,
            gap_at_h=gap[within[-1]], delta_last_20pct=gap[within[i]] - gap[within[-1]],
            still_shrinking=(gap[within[i]] - gap[within[-1]]) > 1,
            coverage_to_h=True, samples_to_h=got, samples_expected=expected, finite=finite)

    return dict(t_end=t_end, gap0=gap[ts[0]], nonfinite=bad, finite=finite, per_horizon=per_h,
                reached_full_horizon=t_end >= max(HORIZONS),
                horizons_observed=[h for h in HORIZONS if per_h[str(h)]["observed"]],
                horizons_not_observed=[h for h in HORIZONS if not per_h[str(h)]["observed"]])


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

    log_step = float(proto["sample_times"]["log_step"])
    arms, missing = {}, []
    for spec in proto["arms"]:
        r = read_arm(root / spec["id"], log_step)
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

    # The protocol's falsifier is per ARM: any selected hi-side arrested arm closing later.
    # Bracket-tuple motion is a weaker proxy -- a group that is UNRESOLVED at baseline AND at
    # the final horizon can hide a hi-side arm that closed. This implements the declared
    # falsifier directly; bracket resolution stays reported separately and is never dropped.
    falsifier = {}
    for name, A in arms.items():
        if not A["spec"]["role"].startswith("bracket hi-side"):
            continue
        base = A["per_horizon"][str(HORIZONS[0])]
        later = [h for h in HORIZONS[1:] if A["per_horizon"][str(h)]["observed"]]
        closed_at = next((h for h in later if A["per_horizon"][str(h)]["closed"]), None)
        falsifier[name] = dict(
            baseline_observed=base["observed"],
            baseline_closed=base.get("closed"),
            later_horizons_observed=later,
            closed_at_later_horizon=closed_at,
            falsifies=(closed_at is not None and base.get("closed") is False),
            uninformative=(not base["observed"] or not later or base.get("closed") is not False),
            uninformative_why=("baseline horizon not observed" if not base["observed"] else
                               "no later horizon observed" if not later else
                               "already closed at the baseline horizon, so it cannot close later"
                               if base.get("closed") is not False else None))
    falsified = [n for n, v in falsifier.items() if v["falsifies"]]
    hi_side_total = len(falsifier)
    hi_side_informative = sum(1 for v in falsifier.values() if not v["uninformative"])

    # temporal coverage, reported before any verdict
    not_observed = {n: A["horizons_not_observed"] for n, A in arms.items() if A["horizons_not_observed"]}
    full_coverage = sum(1 for A in arms.values() if A["reached_full_horizon"])

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

    # A verdict over an empty set is not a verdict, and a verdict over data that was never
    # observed is worse. The ladder below refuses before it concludes.
    evaluable = sum(1 for v in moved.values() if v["baseline_1000"].get("state") == "BRACKETED")
    any_moved = any(v["moved"] for v in moved.values())
    repro_ok = (repro is not None and repro["verdict"] == "REPRODUCED")
    bad_ctrl = [n for n, v in ctrl.items() if not v["passed"]]
    final_h = HORIZONS[-1]
    arms_missing_final = [n for n, A in arms.items()
                          if not A["per_horizon"][str(final_h)].get("coverage_to_h")]

    if repro is None:
        outcome = "UNINTERPRETABLE: the reproduction control was not run"
    elif not repro_ok:
        outcome = (f"UNINTERPRETABLE: reproduction verdict {repro['verdict']}. "
                   f"{len(uninterpretable)} arm(s) do not reproduce their original prefix.")
    elif missing:
        outcome = f"UNINTERPRETABLE: {len(missing)} declared arm(s) produced no readable trajectory"
    elif arms_missing_final:
        outcome = (f"UNINTERPRETABLE: {len(arms_missing_final)} of {len(arms)} arm(s) never reached "
                   f"horizon {final_h}. Horizons that were not observed cannot be reported as "
                   f"unchanged; the last available sample is NOT the value at a later horizon.")
    elif bad_ctrl:
        outcome = (f"UNINTERPRETABLE: required control(s) failed ({', '.join(sorted(bad_ctrl))}). "
                   f"A failed control removes the basis for reading the arms, whatever the brackets did.")
    elif falsified:
        outcome = (f"NOT SUPPORTED: {len(falsified)} selected hi-side arrested arm(s) closed at a "
                   f"later horizon -- {', '.join(sorted(falsified))}")
    elif hi_side_informative == 0:
        outcome = ("UNRESOLVED: no hi-side arm was informative (none had both an observed baseline "
                   "and an observed later horizon), so the declared falsifier was never exercised")
    elif any_moved:
        outcome = "NOT SUPPORTED: at least one bracket moved with horizon"
    elif evaluable == 0:
        outcome = ("UNRESOLVED: no cell produced a bracket at the baseline horizon, so there is "
                   "nothing whose motion could be observed across horizons")
    else:
        outcome = (f"SUPPORTED at these horizons: none of the {hi_side_informative} informative "
                   f"hi-side arms closed later and none of the {evaluable} evaluable brackets moved")

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
        coverage=dict(final_horizon=final_h, arms=len(arms),
                      arms_with_full_coverage=full_coverage,
                      arms_missing_the_final_horizon=sorted(arms_missing_final),
                      horizons_not_observed_per_arm=not_observed,
                      rule="a horizon is observed only when the trajectory covers it, except that "
                           "closure at or before a horizon settles that horizon without coverage"),
        falsifier=dict(declared="any selected hi-side arrested arm closing at a later horizon",
                       hi_side_arms=hi_side_total, informative=hi_side_informative,
                       falsified_by=sorted(falsified), per_arm=falsifier),
        controls_failed=sorted(bad_ctrl),
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
    raise SystemExit(0 if outcome.startswith(("SUPPORTED", "NOT SUPPORTED")) else 2)


if __name__ == "__main__":
    main()
