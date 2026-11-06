#!/usr/bin/env python3
"""SPEC-015's capability state, computed per scale from the evidence the project actually holds.

WHY THIS EXISTS. `swarm/check_spec_coverage.py` reports which specs are named by some checker.
SPEC-015 is one of the five that **nothing names**, and its first substantive requirement is this:

    "Each scale must display its actual capability state: sourced possibility, available tool,
     executed forward model, executed inverse design, numerical checks or empirical validation.
     Listing a tool or producing a candidate is not completion of every subsequent state."

That last sentence is the whole point, and nothing was enforcing it. A scale can accumulate two
hundred literature claims and read, in any summary that counts claims, as well covered -- while
nothing has ever been executed there. Counting claims cannot tell those apart; counting
EVIDENCE KINDS can, because this project already maintains a closed evidence vocabulary and
`classify_scale.py` deliberately leaves `scale_id` NULL rather than inheriting one.

WHAT IT DOES NOT DO. It does not judge whether an executed model was any good, and it maps
`measured` to "executed measurement" rather than to SPEC-015's "empirical validation" -- in this
corpus `measured` means we ran something and read a number off it, including off a file or an
API response. Wet-lab validation of a fish does not exist here and this must not imply it does.
The distinction matters enough to be in the output legend rather than only in this docstring.

    python3 swarm/check_capability_state.py             # report
    python3 swarm/check_capability_state.py --control   # must-flag / must-miss cases
"""
from __future__ import annotations

import sys
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import dbq  # noqa: E402

#: Evidence kind -> the SPEC-015 capability state it can support, weakest first. The ORDER is the
#: claim: an executed model outranks an analysis, which outranks a citation. `refused` and
#: `unknown` support nothing -- they are the record of a gap, which is why they score 0 rather
#: than being dropped (SPEC-015: "Count solver/model-domain failures rather than dropping them").
STATE = {
    "unknown": (0, "gap recorded"),
    "refused": (0, "gap recorded"),
    "assumed": (1, "assumption"),
    "literature": (2, "sourced possibility"),
    "derived": (3, "analysis / numerical check"),
    "simulated": (4, "executed forward model"),
    "measured": (4, "executed measurement"),
}
#: Below this, the scale has nothing executed: SPEC-015's "listing is not completion".
EXECUTED = 4


def tally(project: str) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = defaultdict(dict)
    for scale, ev, n in dbq.q(
            "select coalesce(scale_id,'(unscaled)'), coalesce(evidence,'(none)'), count(*) "
            f"from claim where project_id = {dbq.lit(project)} and superseded_by is null "
            "group by 1, 2"):
        out[scale][ev] = int(n)
    return out


def report(counts: dict[str, dict[str, int]]) -> list[str]:
    """Print the per-scale state table. Returns the scales with nothing executed."""
    print("\n  SPEC-015 capability state per scale, from evidence kinds\n")
    print(f"  {'scale':12} {'state reached':28} {'executed':>9} {'analysed':>9} "
          f"{'sourced':>8} {'gaps':>6} {'total':>6} {'exec%':>7}")
    thin, frac = [], {}
    for scale in sorted(counts):
        c = counts[scale]
        executed = sum(n for e, n in c.items() if STATE.get(e, (0, ""))[0] >= EXECUTED)
        analysed = sum(n for e, n in c.items() if STATE.get(e, (0, ""))[0] == 3)
        sourced = sum(n for e, n in c.items() if STATE.get(e, (0, ""))[0] in (1, 2))
        gaps = sum(n for e, n in c.items() if STATE.get(e, (0, ""))[0] == 0)
        best = max((STATE.get(e, (0, "unrecognised"))[0] for e in c), default=0)
        label = next((lbl for lvl, lbl in sorted(STATE.values()) if lvl == best), "nothing")
        total = sum(c.values())
        frac[scale] = executed / total if total else 0.0
        print(f"  {scale:12} {label:28} {executed:>9} {analysed:>9} {sourced:>8} "
              f"{gaps:>6} {total:>6} {100 * frac[scale]:>6.1f}%")
        if executed == 0:
            thin.append(scale)
    report.last_fraction = frac
    return thin


def legend() -> None:
    print("\n  `executed` counts `simulated` and `measured`. In THIS corpus `measured` means a")
    print("  number was read off something we ran -- a model, a file, an API -- NOT a wet-lab")
    print("  measurement of an animal. No scale here has reached SPEC-015's \"empirical")
    print("  validation\", and this table must not be read as saying one has.")
    print("  `gaps` counts `refused` and `unknown`. They are kept, not dropped, because SPEC-015")
    print("  requires solver and model-domain failures to be counted.")
    print("  A scale with claims but nothing executed is SPEC-015's \"listing a tool is not")
    print("  completion\" -- a necessary condition only; execution is not quality.")


def control() -> int:
    """A case the report MUST flag and a case it MUST NOT. Neither touches the database."""
    must_flag = {"paper-only": {"literature": 40, "assumed": 2, "unknown": 5}}
    must_miss = {"worked-on": {"literature": 10, "simulated": 3}}
    bad = 0
    f1 = report(must_flag)
    if f1 != ["paper-only"]:
        print(f"  CONTROL FAILED: must-flag case returned {f1}"); bad += 1
    f2 = report(must_miss)
    if f2:
        print(f"  CONTROL FAILED: must-miss case was flagged {f2}"); bad += 1
    # a scale whose ONLY evidence is a gap must still be flagged, not skipped as empty
    f3 = report({"all-gaps": {"unknown": 3}})
    if f3 != ["all-gaps"]:
        print(f"  CONTROL FAILED: gap-only case returned {f3}"); bad += 1
    print(f"\n  controls: {'all passed' if not bad else str(bad) + ' FAILED'}")
    return 1 if bad else 0


def main() -> int:
    if "--control" in sys.argv:
        return control()
    counts = tally(dbq.PROJECT)
    if not counts:
        print(f"  no claims for project {dbq.PROJECT}")
        return 0
    thin = report(counts)
    legend()
    if thin:
        print(f"\n  {len(thin)} scale(s) with NOTHING executed: {', '.join(thin)}")
        print("  Each is a frontier entry: the scale is sourced but never exercised.")
    else:
        print("\n  NOTHING-EXECUTED test: passed -- every scale has at least one executed")
        print("  model or measurement. That is a weak test and it is reported as such: ONE")
        print("  executed claim satisfies it, so it cannot separate a scale that has been")
        print("  worked from one that has been touched. The ranking below is the real signal.")

    frac = getattr(report, "last_fraction", {})
    med = sorted(frac.values())[len(frac) // 2] if frac else 0.0
    print(f"\n  Executed fraction, weakest first. The project's own median is {100 * med:.1f}%,")
    print("  which is the comparison used here -- a threshold taken from this corpus rather")
    print("  than chosen, because a chosen one is what gets argued with and then switched off.")
    for scale in sorted(frac, key=lambda k: frac[k]):
        mark = "  <- below median" if frac[scale] < med else ""
        print(f"    {scale:12} {100 * frac[scale]:>5.1f}%{mark}")
    print("\n  This is a RANKING, not a verdict: a low fraction is where SPEC-015's")
    print("  \"listing is not completion\" is most likely to apply, and is a place to look.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
