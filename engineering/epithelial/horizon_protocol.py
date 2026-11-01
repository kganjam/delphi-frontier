"""Frozen protocol for the observation-horizon follow-up study. SEPARATE from dff5e58.

This study tests ONE new scoped hypothesis: whether the closure thresholds measured at
StopTime 1000 depend on the observation horizon. It cannot and does not reinterpret the
previous FAIL. The 36-run and 240-run records, their criteria and their verdicts are
immutable and are not read by anything here except as the source of the arm selection.

Selection is derived from the returned data, not chosen for a verdict: the minimum feasible
spread is  max_i(lo_i/J_i) / min_i(hi_i/J_i), so only two J columns set it at each gap —
the lowest J (which sets the numerator) and the highest J (which sets the denominator). A
longer horizon can only turn ARRESTED into CLOSED, which moves a bracket UP. Therefore:

  * if the hi-side arm at the highest J closes later, min(hi/J) rises and the spread SHRINKS;
  * if the hi-side arm at the lowest J closes later, max(lo/J) rises and the spread GROWS.

Both directions are in the selected set, so the design can move the result either way. The
middle J columns cannot set the spread and are excluded; that is the justification for not
re-running all 240 arms.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BRACKET_KEY = re.compile(r"k(?P<k>\d+)-s(?P<s>\d+)-J(?P<J>[\d.]+)")
LAMBDA_GRID = (0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8)
HORIZONS = (1000, 2000, 4000, 8000)
STOP_TIME = 8000
LOG_STEP = 10          # must equal the original run's, or the reproduction control is void
DEEP_ARRESTED_LAMBDA = 12.8

NATIVE_RETURN = ("/data/artifacts/delphi-evolve-rethink/gcp/epithelial-j-scaling-v1/"
                 "frontier-cpu-20261031-02/final-ae15a56498cc4a0e80ad1b00a7e7fc0c")


def next_lambda(lam: float) -> float | None:
    for a, b in zip(LAMBDA_GRID, LAMBDA_GRID[1:]):
        if a == lam:
            return b
    return None


def select(audit: dict) -> tuple[list[dict], dict]:
    rows = []
    for key, v in audit["brackets"].items():
        m = BRACKET_KEY.match(key)
        rows.append(dict(k=int(m["k"]), s=int(m["s"]), J=float(m["J"]), **v))

    picked, why = {}, []
    for k in sorted({r["k"] for r in rows}):
        sel = [r for r in rows if r["k"] == k]
        Js = sorted({r["J"] for r in sel})
        j_lo, j_hi = Js[0], Js[-1]
        for J, role in ((j_lo, "sets max(lo/J): if its hi-side arm closes later the spread GROWS"),
                        (j_hi, "sets min(hi/J): if its hi-side arm closes later the spread SHRINKS")):
            cells = [r for r in sel if r["J"] == J]
            why.append(dict(gap=k, J=J, role=role,
                            brackets={f"s{c['s']}": [c["lo"], c["hi"]] for c in sorted(cells, key=lambda c: c["s"])}))
            for c in cells:
                nxt = next_lambda(c["hi"])
                picked[(k, J, c["hi"], c["s"])] = "bracket hi-side: the arrested arm a longer horizon could flip"
                if nxt is not None:
                    picked[(k, J, nxt, c["s"])] = ("one grid step above the hi-side, so a flipped bracket "
                                                   "still has an upper edge instead of becoming unresolved")
            c0 = min(cells, key=lambda c: c["s"])
            picked[(k, J, c0["lo"], c0["s"])] = ("POSITIVE CONTROL: already CLOSED by 1000. Must close again, "
                                                 "at the same sweep count, or the extension is not an extension")
        picked[(k, j_hi, DEEP_ARRESTED_LAMBDA, 1)] = ("NEGATIVE CONTROL: deep in the arrested regime. If this "
                                                      "closes, arrest is horizon-fragile everywhere and no "
                                                      "bracket in the study is interpretable")
    arms = [dict(id=f"S-k{k}-J{J:g}-lamV{lam:g}-s{s}", gap_k=k, J=J, lambda_v=lam, seed=s, role=role)
            for (k, J, lam, s), role in sorted(picked.items())]
    return arms, dict(per_gap_columns=why,
                      excluded="the middle J columns cannot set the minimum feasible spread, so "
                               "re-running them could not change the statistic under test")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", required=True)
    ap.add_argument("--emit", required=True)
    a = ap.parse_args()
    audit = json.loads(Path(a.audit).read_text())
    arms, rationale = select(audit)

    doc = {
        "schema": "frontier.epithelial-horizon-protocol.v1",
        "status": "FROZEN before any new outcome existed",
        "relationship_to_previous": {
            "preserves": "dff5e58 and every record, criterion and verdict in it, unchanged",
            "cannot_do": "this study CANNOT reinterpret the previous FAIL as a pass. The fixed-horizon "
                         "result stands on its own criteria. A horizon effect found here would be a new, "
                         "separately scoped finding about observation horizon, not a revision of that one.",
            "release": "belongs to a later release than the one carrying the 36-run and 240-run records",
        },
        "hypothesis": {
            "H": "The closure thresholds measured at StopTime 1000 are unchanged when the observation "
                 "horizon is extended 8x, for the parameter columns that set the minimum feasible spread.",
            "tests_what": "observation-horizon dependence of the bracket positions, and only that",
            "falsified_if": "any selected hi-side arrested arm closes at a horizon beyond 1000, which moves "
                            "its bracket up a grid step",
            "not_a_test_of": ["whether lambda* is proportional to J (that is the frozen FAIL, untouched)",
                              "gap-size scaling (untested at this resolution; see card section 6)",
                              "anything biological. Model-time units are not calibrated tissue time."],
        },
        "selection": {"rationale": rationale, "arms": len(arms), "arm_ids": [x["id"] for x in arms]},
        "arms": arms,
        "horizon_schedule": {
            "stop_time": STOP_TIME,
            "observed_at": list(HORIZONS),
            "one_trajectory_many_horizons": True,
            "justification": "measured locally before freezing: a run at StopTime 2000 reproduces the "
                             "StopTime 1000 run's logger BYTE-IDENTICALLY for t<=1000, so extending the "
                             "stop time does not perturb the trajectory and one longer run legitimately "
                             "carries several horizon observations. If the packet's reproduction control "
                             "fails, this justification is void and no horizon reading may be taken.",
        },
        "sample_times": {"log_step": LOG_STEP,
                         "must_equal_original": True,
                         "why": "a different logging cadence would change the sampled rows and make the "
                                "t<=1000 reproduction control impossible to evaluate byte-wise"},
        "closure_definition": {
            "operational": "gap_nodes(t) = 40000 - sum(cell.volume) over living cells at a logged time. "
                           "An arm is CLOSED AT HORIZON h if gap_nodes reaches 0 at some logged t <= h.",
            "per_arm": "every arm is classified on its own trajectory; no averaging across seeds",
            "per_seed": "seeds are reported separately and never pooled into a mean before classification. "
                        "A seed mean masked a shrinking arm once already (k=4, J=560, lambda_V=12.8: "
                        "-3, -16, +22 with mean +1.0); that is why this is written into the protocol.",
            "arrested_at_h": "not closed by horizon h. This is an observation, not permanent arrest, and "
                             "not a bound on closure beyond h.",
        },
        "bracketing_rules": {
            "bracket_at_h": "per (gap, J, seed): lo = largest lambda_V CLOSED by h, hi = smallest "
                            "lambda_V ARRESTED at h, requiring lo < hi",
            "unresolved": "if no bracket exists inside the selected lambda_V set at horizon h, that cell is "
                          "UNRESOLVED at h. UNRESOLVED is never a pass and is never dropped to let the "
                          "remaining cells look consistent.",
            "censoring": "an arm still shrinking at the final horizon is reported as censored at that "
                         "horizon. Censoring is descriptive; a finite window bounds nothing about later closure.",
            "nonmonotone": "if bracket positions do not move monotonically with h, that is reported as "
                           "observed and is not smoothed",
            "thresholds_as_intervals": "every threshold is reported as its bracketing interval. The "
                                       "geometric mean is a summary of that interval and is never reported "
                                       "alone as a measured threshold.",
        },
        "reproduction_control": {
            "requirement": "for every selected arm, the extended run's logger rows at t <= 1000 must be "
                           "BYTE-IDENTICAL to the corresponding rows of that arm's native logger from the "
                           "previous CPU run",
            "columns": ["time", "cell.id", "cell.center.x", "cell.center.y", "cell.volume", "cell.surface"],
            "roundoff_policy": "byte-identical text, no tolerance. Justified because the solver is "
                               "deterministic for a fixed seed and the same pinned binary: measured before "
                               "freezing, a local rerun of S-k4-J560-lamV1.6-s1 reproduced the VM's native "
                               "logger byte for byte on different hardware. A numeric tolerance would hide "
                               "exactly the nondeterminism this control exists to detect.",
            "binary_and_environment": "the binary is pinned by sha256 and fetched by the packet, so it is "
                                      "identical. The host is NOT asserted identical; the control is what "
                                      "establishes that the difference did not matter.",
            "on_failure": "if any arm's prefix does not reproduce, that arm's horizon readings are "
                          "UNINTERPRETABLE and must be reported as such, not analysed. If more than one "
                          "arm fails, the trajectory-reuse justification above is void for the whole "
                          "packet and no horizon conclusion may be drawn from it.",
        },
        "cardinality": {"arms": len(arms), "horizons_per_arm": len(HORIZONS),
                        "observations": len(arms) * len(HORIZONS),
                        "gaps": 2, "j_columns_per_gap": 2, "seeds": 3},
        "limits": {
            "measured_basis": "6.85 s and 285 927 bytes per 1000 model-time units, peak RSS 10.8 MB, "
                              "measured locally on one arm at StopTime 1000 and 2000 (linear in both)",
            "projected_per_arm": {"wall_s": 55, "logger_bytes": 2287416},
            "projected_total": {"cpu_s": 55 * len(arms), "output_mb": round(2287416 * len(arms) / 1e6, 1)},
            "caps_requested": {"vcpu": "4-8", "memory": "<=12 GiB", "threads_per_arm": 1,
                               "whole_tree_s": 1800, "outputs_mb": 100},
            "headroom_note": "the projection sits well inside every cap; if the timing gate in the packet "
                             "measures a materially slower rate the run should stop rather than expand",
        },
        "returns": ["per-arm logger.csv", "per-arm model.xml", "per-arm stdout/exit",
                    "binary receipt (url, bytes, sha256, environment)",
                    "completeness audit over the exact declared ids",
                    "every skipped or failed arm, by id, preserved",
                    "NO lattice frames and therefore NO movie: centre/volume logs cannot be turned into "
                    "cell shapes or a wound boundary, and none will be invented"],
        "native_source": {"return_dir": NATIVE_RETURN,
                          "manifest_sha256": "39f32c4d97c86aecab6e1dd02b3147cca8d029652ba2380adf99a10d06e116f7"},
    }
    Path(a.emit).parent.mkdir(parents=True, exist_ok=True)
    Path(a.emit).write_text(json.dumps(doc, indent=1))
    print(f"arms={len(arms)} horizons={len(HORIZONS)} observations={len(arms) * len(HORIZONS)} -> {a.emit}")
    for x in arms:
        print(f"  {x['id']:26s} {x['role'][:72]}")


if __name__ == "__main__":
    main()
