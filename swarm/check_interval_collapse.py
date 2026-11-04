#!/usr/bin/env python3
"""Find summary ranges that are NARROWER than the range their source document states.

THE PATTERN, measured four times in one day. A research document states an interval and its
caveats; the summary carries a point, or a narrower interval, and drops them. Nothing downstream
can recover a caveat that was never carried, so the summary is where this error does its damage.

  * frog spring-loading work: source 32-81 J/kg, summary quoted 53-81 -- the MEAN as a floor
  * hydromechanical efficiency: source 0.34-0.39, summary quoted the point 0.37
  * one-sided muscle fraction: source calls it an assumption, summary quoted it as an input
  * taxi ceiling: source states 1.9-2.9 m/s as the uncertainty span, summary carries 2.2-2.9

THIS IS A SWEEP, NOT A GATE, and the measurement says why. On the corrected document it returns 7
hits of which 2 are the correction notes QUOTING the old value -- a forbidden-string check cannot
tell claiming from quoting, which this project has now documented four times -- and at least one
more is a different quantity that happens to share a unit (Park & Choi's 7-20% body share against
a 7.5-20% muscle fraction). Read every hit; expect roughly half to be nothing.

IT EARNS ITS KEEP ON THE MUST-FLAG TEST. Against the pre-correction document it flags
"53-81 J/kg vs 32-81 J/kg", which is the real error, found independently of knowing it was there.

    python3 check_interval_collapse.py [summary.md]
"""
from __future__ import annotations

import re
import sys

sys.path.insert(0, "/data/swarm")
from harvest import BASE, git   # noqa: E402

RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*(J/kg|m/s|Hz|GPa|%)")
SUMMARY = "/data/worktrees/delphi-frontier/swarm-arch/docs/FINDINGS.md"


def ranges(text):
    out = []
    for m in RANGE.finditer(text):
        lo, hi, u = float(m.group(1)), float(m.group(2)), m.group(3)
        if lo < hi:
            out.append((lo, hi, u, m.group(0)))
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else SUMMARY
    srcs = {}
    for b in [x.strip() for x in git("branch", "-r", "--sort=-committerdate").split("\n")
              if "origin/claude/" in x][:200]:
        for f in [y for y in git("diff", "--name-only", f"{BASE}...{b}").split("\n")
                  if y.endswith(".md") and "research/fish" in y]:
            try:
                srcs[f] = git("show", f"{b}:{f}")
            except Exception:
                pass
    src_ranges = [r + (f,) for f, t in srcs.items() for r in ranges(t)]

    hits = []
    for lo, hi, u, txt in ranges(open(path).read()):
        for slo, shi, su, stxt, f in src_ranges:
            # Same unit and the SAME upper end, but the summary's low end is higher: the interval
            # was narrowed from below, which is how a mean becomes a floor.
            if su == u and abs(shi - hi) / max(hi, 1e-9) < 0.02 and slo < lo * 0.98:
                hits.append((txt, stxt, f))
                break

    print(f"  {len(srcs)} source documents, {len(src_ranges)} ranges in them")
    print(f"  {len(hits)} summary range(s) narrower than a same-unit source range:\n")
    for t, s, f in hits:
        print(f"    summary '{t}'  vs source '{s}'   [{f.split('/')[-1]}]")
    print("\n  READ EVERY HIT. Roughly half are nothing: a correction note quoting the old value,")
    print("  or a different quantity sharing a unit. This is a sweep to read, not a gate to pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
