#!/usr/bin/env python3
"""Which OPEN cross-scale entailments could be closed with evidence this project already holds?

The cross-scale chain spans 8 of 8 scales but only 130 of 381 entailments are `satisfied`, and
151 sit `open`. 122 of those carry numeric bounds, so they are mechanically checkable the moment
a claim with a comparable quantity exists. Nobody had asked which ones.

THIS PROPOSES, IT DOES NOT SATISFY. Matching an entailment's quantity to a claim's value is a
judgement about whether two things are the SAME quantity, and units agreeing is weak evidence
for that -- m/s is m/s whether it is a launch speed or a wind speed. So this prints candidate
pairs for a person to accept or reject, and writes nothing. Auto-satisfying on a unit match
would manufacture a satisfied chain, which is the failure this whole project is organised
against.

THE OUTPUT IS A WORK LIST, and its value is in the HITS it finds, not in a count of how many
entailments remain open.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env, flat  # noqa: E402


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.strip().split("\n") if ln]


def norm(u: str) -> str:
    """Units as written vary; compare on a squashed form. Deliberately crude -- see the docstring."""
    u = (u or "").lower().strip()
    u = re.sub(r"\(.*?\)", "", u)          # drop parentheticals like "(upper bound = ...)"
    u = re.sub(r"[^a-z0-9/^%.-]+", " ", u).strip()
    return " ".join(u.split()[:3])          # the leading tokens carry the dimension


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    # Hoisted out of the f-string: a backslash escape inside one is a SyntaxError on
    # Python 3.11, which ruff targets. It only ran here because this interpreter is 3.13.
    src_stmt = flat("coalesce(c.statement, '')", 1600)
    ents = q(f"""select e.id::text, e.source_scale, e.target_scale, coalesce(e.quantity,''),
                        coalesce(e.lo::text,''), coalesce(e.hi::text,''), coalesce(e.units,''),
                        {flat('e.statement', 110)}, coalesce(e.source_claim::text,''),
                        {src_stmt}
                 from constraint_entailed e
                 left join claim c on c.id = e.source_claim
                 where e.project_id = '{proj}' and e.status = 'open'
                   and (e.lo is not null or e.hi is not null) and coalesce(e.units,'') <> ''
                 order by e.id""")
    claims = q(f"""select id::text, coalesce(value_num::text,''), {flat('units', 160)},
                          coalesce(scale_id,'')
                   from claim where project_id = '{proj}' and superseded_by is null
                     and value_num is not null and coalesce(units,'') <> ''""")
    by_unit: dict[str, list] = {}
    for c in claims:
        if len(c) >= 4:
            by_unit.setdefault(norm(c[2]), []).append(c)

    hits = checked = 0
    circular = 0
    for e in ents:
        if len(e) < 8:
            continue
        eid, ss, ts, quant, lo, hi, units, stmt = e[:8]
        src_id = e[8] if len(e) > 8 else ""
        src_text = e[9] if len(e) > 9 else ""
        checked += 1
        cands = by_unit.get(norm(units), [])
        inside = []
        for cid, val, cu, cscale in cands:
            try:
                v = float(val)
            except ValueError:
                continue
            if lo and v < float(lo):
                continue
            if hi and v > float(hi):
                continue
            # CIRCULARITY GUARD. An entailment's bounds are usually DERIVED from its source
            # claim, so a candidate that IS that claim -- or whose value is quoted inside its
            # text -- confirms the constraint with the number that generated it. Measured
            # 2026-11-05: entailment 88 (bounds 1.31-1.45 m/s) matched claim 75 at 1.38 m/s,
            # and its source claim 191 reads "At the measured maximum burst of 1.38 m/s ...".
            # That pair looked like the cleanest hit in the whole run.
            if cid == src_id:
                circular += 1
                continue
            vs = f"{v:g}"
            if vs and vs in (src_text or ""):
                circular += 1
                continue
            inside.append((cid, v, cu, cscale))
        if inside:
            hits += 1
            print(f"\n  entailment {eid} [{ss}->{ts}]  {quant[:60]}")
            print(f"      bounds [{lo or '-'}, {hi or '-'}] {units[:46]}")
            print(f"      {stmt[:96]}")
            for cid, v, cu, cscale in inside[:4]:
                print(f"      CANDIDATE claim {cid:>5} = {v:<12g} {cu[:40]:<40} scale={cscale}")
    print(f"\n  {checked} open entailments with bounds AND units; {hits} have at least one")
    print("  live claim whose value falls inside them, matched on units alone.")
    print(f"  {circular} candidate pair(s) REJECTED as circular -- the value already appears in")
    print("  the entailment's own source claim, so the bound was derived from it.")
    print("  A UNIT MATCH IS NOT A QUANTITY MATCH. m/s is m/s whether it is a launch speed or a")
    print("  wind speed, so every pair above needs a person to accept or reject it. Nothing is")
    print("  written. Auto-satisfying on this would manufacture a satisfied chain.")
    print()
    print("  AND A BOUND DOES NOT CARRY ITS CONDITIONS, which is the subtler failure. Worked")
    print("  example, entailment 180: it requires pectoral muscle to deliver net CYCLIC power")
    print("  >= 50 W/kg, and claim 309 measures 142.7 W/kg -- non-circular, right units, three")
    print("  times the bound. It is still NOT a satisfaction: the measurement is Scorpaena")
    print("  notata MYOTOMAL fibres at 20 C under FAST-START strain, not pectoral muscle cycling")
    print("  at flapping frequency. Power and frequency trade off in muscle -- superfast muscle")
    print("  is weak BECAUSE it is fast (claims 979, 998, 1090) -- so a power figure without its")
    print("  frequency is not comparable to a cyclic-power requirement. Read the conditions on")
    print("  both sides, not just the number and the unit.")
    print()
    print("  FIVE candidates were worked by hand and ALL FIVE failed (claim 1094), in five")
    print("  distinct ways no numeric filter catches:")
    print("    circular -- the bound was derived from the candidate            (e88, now guarded)")
    print("    conditions the bound does not carry -- regime mismatch          (e180)")
    print("    WRONG SIDE: the candidate is the REQUIREMENT, not the capability (e123)")
    print("    the candidate's OWN TEXT forbids the use                        (e54)")
    print("    same units, unrelated physics                                   (e281)")
    print("  e54 is the one to remember: claim 238 exists specifically to say its 2.5 g is a")
    print("  DIFFERENT quantity and must not be conflated -- and this tool proposed exactly that")
    print("  conflation. A corpus that records its own refusals will have them offered back by")
    print("  any naive matcher, and a numeric matcher cannot read 'do not use X for Y'.")
    print("  The tool is still worth running: 151 open -> 12 worth reading, in minutes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
