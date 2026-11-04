#!/usr/bin/env python3
"""Import ask-transfer/v1 records into a project, refusing any that arrive without their envelope.

WHY THIS EXISTS. swarm/export_transfer.py emits the serialisation SPEC-ASK section 4 item 3 asks
for, and until now NOTHING CONSUMED IT. A grep for `ask-transfer` returned two files: the spec
that specifies the format and the script that writes it. An export surface with no consumer is a
mechanism walking an empty set -- the format was correct, validated, and had never been read by
anything, so D5 transferability had never been exercised at an actual boundary.

D5 says the test is whether another project can import an entity "without severing its provenance,
scope conditions, dependencies, or restrictions". That is a property of the RECEIVING side as much
as the sending one: a reader that silently accepts a value whose `conditions` are missing severs
them just as surely as a writer that never sent them. So this importer REFUSES such a record, and
the refusal is the feature.

    python3 import_transfer.py <file.jsonl> <project_id> [--write]
    python3 import_transfer.py --round-trip        # export, re-import, compare
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export_transfer as xt  # noqa: E402


def import_records(recs: list[dict], project: str, write: bool) -> tuple[int, int]:
    ok = refused = 0
    for r in recs:
        why = xt.validate(r)
        if why:
            refused += 1
            print(f"  REFUSED {r.get('id', '(no id)')}: {'; '.join(why)}")
            continue
        q = r["quantity"]
        ok += 1
        print(f"  accept  {r['id']:<28} {q['symbol']:<8} units={q['units']!r} "
              f"conditions={q['conditions'][:46]!r}")
        if write:
            v = q["value"]
            # The envelope travels into the row. `conditions` is NOT optional on the way in:
            # validate() has already refused anything lacking it, so this cannot write a bare value.
            xt.q(f"""insert into parameter (project_id, symbol, name, point, lo, hi, interval_kind,
                                            units, conditions, derivation, how, source, read_level)
                     values ({xt.lit(project)}, {xt.lit(q['symbol'])}, {xt.lit(q.get('name'))},
                             {v.get('point') if v.get('point') is not None else 'null'},
                             {v.get('lo') if v.get('lo') is not None else 'null'},
                             {v.get('hi') if v.get('hi') is not None else 'null'},
                             {xt.lit(v.get('interval_kind'))}, {xt.lit(q['units'])},
                             {xt.lit(q['conditions'] + '  [imported from ' + r['id'] + ']')},
                             {xt.lit((r.get('evidence') or {}).get('derivation'))},
                             {xt.lit((r.get('evidence') or {}).get('how'))},
                             {xt.lit((r.get('evidence') or {}).get('source'))},
                             {xt.lit((r.get('evidence') or {}).get('read_level'))})""")
    return ok, refused


def round_trip() -> int:
    """Export, re-import, and compare -- plus a must-refuse case with the envelope stripped."""
    rows = xt.rows()
    recs = [xt.build(r) for r in rows]
    print(f"  exported {len(recs)} record(s) from `parameter`\n")
    ok, refused = import_records(recs, xt.PROJECT, write=False)
    print(f"\n  round trip: {ok} accepted, {refused} refused")

    # Field-by-field comparison: the envelope must survive the trip intact.
    bad = []
    for src, rec in zip(rows, recs):
        for a, b in (("units", rec["quantity"]["units"]), ("conditions", rec["quantity"]["conditions"]),
                     ("symbol", rec["quantity"]["symbol"])):
            if str(src[a] or "") != str(b or ""):
                bad.append(f"{src['symbol']}.{a}")
    print(f"  envelope fields identical after the trip: {'YES' if not bad else 'NO -- ' + ', '.join(bad)}")

    # MUST-REFUSE: strip the conditions and confirm the receiver rejects it.
    stripped = json.loads(json.dumps(recs[0]))
    stripped["quantity"]["conditions"] = ""
    print("\n  MUST-REFUSE control, same record with `conditions` removed:")
    o2, r2 = import_records([stripped], xt.PROJECT, write=False)
    good = (r2 == 1 and o2 == 0)
    print(f"  -> {'REFUSED as required' if good else '*** ACCEPTED -- the boundary does not hold ***'}")
    return 0 if (not bad and good and refused == 0) else 1


def main() -> int:
    if "--round-trip" in sys.argv:
        return round_trip()
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    ok, refused = import_records(recs, sys.argv[2], "--write" in sys.argv)
    print(f"\n  {ok} imported, {refused} refused")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
