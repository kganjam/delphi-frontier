#!/usr/bin/env python3
"""Find summary ranges that are NARROWER than the range their source document states.

THE PATTERN, measured four times in one day. A research document states an interval and its
caveats; the summary carries a point, or a narrower interval, and drops them. Nothing downstream
can recover a caveat that was never carried, so the summary is where this error does its damage.

  * frog spring-loading work: source 32-81 J/kg, summary quoted 53-81 -- the MEAN as a floor
  * hydromechanical efficiency: source 0.34-0.39, summary quoted the point 0.37
  * one-sided muscle fraction: source calls it an assumption, summary quoted it as an input
  * taxi ceiling: source states 1.9-2.9 m/s as the uncertainty span, summary carries 2.2-2.9

THIS IS A SWEEP, NOT A GATE, and every hit of one full run has been adjudicated to say how good
it is. On the corrected document: 7 raw hits, 5 unique after duplicates, of which

  1  REAL      the taxi ceiling, 2.2-2.9 vs a stated uncertainty span of 1.9-2.9 m/s
  1  a QUOTE   "53-81 J/kg" inside this project's own note explaining that correction;
               a string matcher cannot tell claiming from quoting (documented 4x here)
  3  WRONG     different quantities that happen to share a unit:
                 7.5-20% muscle fraction      vs Park & Choi's 7-20% BODY SHARE
                 15-20 m/s exocoetid taxi     vs 10-20 m/s max FLIGHT speed
                 0.45-1.38 m/s measured burst vs 0.36-1.39 m/s MINIMUM SUPPORTABLE speed

So the hit rate is 1 in 5, and the dominant failure is unit-collision between unrelated
quantities. That is useful for a sweep somebody reads and useless as a gate, which is the same
conclusion this project reached for its zero-cell sweep at 1 in 9. Read every hit.

IT EARNS ITS KEEP ON THE MUST-FLAG TEST. Against the pre-correction document it flags
"53-81 J/kg vs 32-81 J/kg", which is the real error, found independently of knowing it was there.

    python3 check_interval_collapse.py [summary.md]
"""
from __future__ import annotations

import re
import os
import sys

sys.path.insert(0, "/data/swarm")
from harvest import BASE, git   # noqa: E402

RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*(J/kg|m/s|Hz|GPa|%)")
SUMMARY = "/data/worktrees/delphi-frontier/swarm-arch/docs/FINDINGS.md"


# THE READER MUST FOLLOW THE WRITER. generate.py and swarm.py write a project's research under
# docs/research/<project>, and this checker scanned a literal "research/fish" -- so for any other
# project it would read nothing and report a clean pass over an empty set, which is this repo's
# vacuous-success shape. Derived identically to generate.py rather than restated as a constant.
RESEARCH_DIR = "docs/research/" + ("fish" if os.environ.get("SWARM_PROJECT", "zebrafish-flight")
                                   == "zebrafish-flight"
                                   else os.environ.get("SWARM_PROJECT", "").split("-")[0])


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
                  if y.endswith(".md") and RESEARCH_DIR in y]:
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
