#!/usr/bin/env python3
"""Measure how two reviewer models disagree, from the challenge table rather than from a sample.

WHY IT IS A SCRIPT AND NOT A QUERY RUN BY HAND. The first estimate of this asymmetry came from a
convenience sample: sonnet had 18 verdicts, all `weakened`, and that produced claim 497's reading
that the asymmetry "is the MODEL". Those 18 were every claim OPUS HAD REFUSED -- a `category: bio`
subset, which is to say the protein claims. Sampling the thing that selected the sample is how a
0-of-18 comes to look like a property of a model.

The panel runs every claim through both, so the subset is no longer chosen by the refusal. This
reads the resulting rows and reports: survival rate per model over claims that model JUDGED, the
refusal rate, and the disagreement rate over claims BOTH judged -- which is the only number that
compares like with like.
"""
from __future__ import annotations

import os
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def main() -> int:
    rows = q("""select claim_id,
                       split_part(replace(challenger,'api-panel:',''),'@',1) as model,
                       outcome
                from challenge where challenger like 'api-panel:%'""")
    by: dict[tuple[str, str], str] = {}
    for cid, mdl, out in rows:
        by[(cid, mdl)] = out
    models = sorted({m for _, m in by})
    if len(models) < 2:
        print(f"  only {len(models)} model(s) in panel rows; nothing to compare.")
        return 1
    print(f"  {len(rows)} panel verdicts across {len({c for c, _ in by})} claims\n")
    print(f"  {'model':22} {'judged':>7} {'survived':>9} {'rate':>7}")
    for m in models:
        v = [o for (c, mm), o in by.items() if mm == m]
        s = sum(1 for o in v if o == "survived")
        print(f"  {m:22} {len(v):>7} {s:>9} {100*s/len(v) if v else 0:>6.1f}%")
    both = [c for c in {c for c, _ in by} if all((c, m) in by for m in models)]
    dis = [c for c in both if len({by[(c, m)] for m in models}) > 1]
    print(f"\n  claims BOTH models judged : {len(both)}")
    print(f"  they disagree on          : {len(dis)}  ({100*len(dis)/len(both) if both else 0:.1f}%)")
    print("\n  Only the last figure compares like with like. A survival RATE per model is still")
    print("  computed over a different claim set for each, because one model refuses some.")
    if dis:
        print(f"\n  disagreed claims: {', '.join(sorted(dis, key=int)[:12])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
