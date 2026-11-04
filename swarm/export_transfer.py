#!/usr/bin/env python3
"""ask-transfer/v1: export a quantity so its value cannot be separated from its envelope (ASK D5).

SPEC-ASK section 4 item 3 asks for "a serialisation in which a value cannot be separated from its
units, conditions and scope", and D5's INVALID clause is "exporting a value without the conditions
under which it holds -- the dimension most easily lost at an API boundary, and the one that causes
the most downstream damage, because the receiving project cannot see what it is missing."

TWO DESIGN CHOICES FOLLOW, and the second is the one that does the work.

  1. The record offers NO bare scalar at top level. A value lives only inside a `quantity` object
     that also holds `units` and `conditions`. A consumer may still dig the number out; what they
     cannot do is read this format casually and end up with a naked number.
  2. `validate()` REFUSES a record missing any envelope field. A format without a validator is a
     convention, and a convention is what D5 says gets lost at the boundary. The refusal is the
     feature; the schema is just where it is written down.

WHAT THE CENSUS IS FOR. The spec's D5 row cites `spec_parameter.conditions` and `.units` as
"mandatory". That table holds ZERO ROWS, so the constraint is vacuously satisfied and tells you
nothing -- this repository's own empty-set failure, inside its own conformance table. The census
counts, per source table, how many live quantities could actually be exported without severing
their conditions. That number, not the schema, is the D5 answer.

    python3 export_transfer.py --census          # what could be exported, per table
    python3 export_transfer.py --emit            # write ask-transfer/v1 records to stdout
    python3 export_transfer.py --control         # must-flag / must-miss cases
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
SCHEMA = "ask-transfer/v1"

# Every one of these must be present and non-empty, or the record is refused. `conditions` is the
# field D5 exists to protect; `units` is the one whose absence is hardest to notice downstream.
# Checked INSIDE `quantity`. `source` is deliberately NOT here: it lives in `evidence`, and the
# first version of this tuple listed it anyway, so every complete record was refused for a field
# that was present in another object. The must-miss control caught it on the first run -- which is
# the whole reason a validator ships with a case it must ACCEPT, not only cases it must reject.
REQUIRED = ("units", "conditions")
REQUIRED_EVIDENCE = ("source",)


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def lit(s) -> str:
    return "'" + str(s).replace("'", "''") + "'"


def validate(rec: dict) -> list[str]:
    """Return the reasons this record may NOT be exported. Empty list means it may."""
    bad = []
    if rec.get("schema") != SCHEMA:
        bad.append(f"schema is {rec.get('schema')!r}, not {SCHEMA!r}")
    qy = rec.get("quantity")
    if not isinstance(qy, dict):
        return bad + ["no `quantity` object: a bare value is exactly what D5 forbids"]
    v = qy.get("value")
    if not isinstance(v, dict) or all(v.get(k) is None for k in ("point", "lo", "hi")):
        bad.append("`quantity.value` carries no point and no interval")
    for f in REQUIRED:
        if not str(qy.get(f) or "").strip():
            bad.append(f"`quantity.{f}` is missing or empty"
                       + (" -- this is the field D5 exists to protect" if f == "conditions" else ""))
    ev = rec.get("evidence") or {}
    for f in REQUIRED_EVIDENCE:
        if not str(ev.get(f) or "").strip():
            bad.append(f"`evidence.{f}` is missing or empty")
    return bad


def build(row: dict) -> dict:
    """One ask-transfer/v1 record. The value is reachable ONLY inside `quantity`."""
    return {
        "schema": SCHEMA,
        "id": f"ms:parameter/{row['symbol']}",
        "project": PROJECT,
        "quantity": {
            "symbol": row["symbol"],
            "name": row.get("name") or None,
            "value": {"point": row.get("point"), "lo": row.get("lo"), "hi": row.get("hi"),
                      "interval_kind": row.get("interval_kind") or None},
            "units": row.get("units"),
            "conditions": row.get("conditions"),
        },
        "evidence": {"read_level": row.get("read_level") or None,
                     "derivation": row.get("derivation") or None,
                     "how": row.get("how") or None,
                     "source": row.get("source")},
        "provenance": {"created_at": row.get("created_at"), "table": "parameter"},
        # D6: a consumer must be able to see what is contested, not only what is asserted.
        "contestation": {"superseded": False, "open_challenges": []},
        "transfer_note": ("Every field in `quantity` travels together. A value taken without "
                          "`units` and `conditions` is not this quantity."),
    }


def rows() -> list[dict]:
    cols = ("symbol", "name", "point", "lo", "hi", "interval_kind", "units", "conditions",
            "derivation", "how", "source", "read_level", "created_at")
    sel = ", ".join(f"coalesce({c}::text,'')" for c in cols)
    out = []
    for r in q(f"select {sel} from parameter where project_id={lit(PROJECT)} "
               f"and superseded_by is null order by id"):
        d = dict(zip(cols, r))
        for n in ("point", "lo", "hi"):
            d[n] = float(d[n]) if d[n] not in ("", None) else None
        out.append(d)
    return out


def census() -> int:
    print(f"  D5 census for project {PROJECT!r}: live quantities that could be exported\n")
    print(f"  {'table':22} {'quantities':>10} {'with units':>11} {'with conditions':>16} {'exportable':>11}")
    tot_ok = 0
    for table, valexpr, cond in (
            ("parameter", "point is not null or lo is not null", "conditions"),
            # spec_parameter has NO project_id column, so it is counted project-wide. It holds 0
            # rows, which is why the spec's D5 row citing its "mandatory" constraints is vacuous.
            ("spec_parameter", "value_nominal is not null or value_min is not null", "conditions"),
            ("claim", "value_num is not null", None),
            ("constraint_entailed", "quantity is not null or lo is not null", None)):
        has_proj = int(q("select count(*) from information_schema.columns where "
                         f"table_name={lit(table)} and column_name='project_id'")[0][0])
        where = f"where project_id={lit(PROJECT)}" if has_proj else "where true"
        if table in ("claim", "parameter"):
            where += " and superseded_by is null"
        try:
            n = int(q(f"select count(*) from {table} {where} and ({valexpr})")[0][0])
            u = int(q(f"select count(*) from {table} {where} and ({valexpr}) "
                      f"and btrim(coalesce(units,''))<>''")[0][0])
            c = (int(q(f"select count(*) from {table} {where} and ({valexpr}) "
                       f"and btrim(coalesce({cond},''))<>''")[0][0]) if cond else 0)
        except Exception as e:
            print(f"  {table:22} query failed: {type(e).__name__}")
            continue
        note = "" if cond else "   <- NO conditions column at all"
        print(f"  {table:22} {n:10} {u:11} {c:16} {c:11}{note}")
        tot_ok += c
    print(f"\n  TOTAL exportable without severing conditions: {tot_ok}")
    print("  A quantity in a table with no `conditions` column cannot be exported under D5 at all:")
    print("  its conditions exist only in prose, and prose does not travel with the number.")
    return 0


def control() -> int:
    ok = True
    rs = rows()
    if not rs:
        print("  CONTROL CANNOT RUN: no parameter rows")
        return 2
    good = build(rs[0])
    bad = validate(good)
    print(f"  must-miss  a complete record ({good['id']}): "
          + ("accepted  ok" if not bad else f"REFUSED {bad}  *** false positive ***"))
    ok &= not bad
    stripped = json.loads(json.dumps(good))
    stripped["quantity"]["conditions"] = ""
    r2 = validate(stripped)
    print(f"  must-flag  the same record with conditions stripped: "
          + (f"REFUSED ({r2[0][:60]}...)  ok" if r2 else "ACCEPTED  *** the validator is broken ***"))
    ok &= bool(r2)
    r3 = validate({"schema": SCHEMA, "quantity": {"units": "m", "conditions": "x", "source": "y",
                                                  "value": {"point": None, "lo": None, "hi": None}}})
    print(f"  must-flag  a record with an empty value: "
          + ("REFUSED  ok" if r3 else "ACCEPTED  *** broken ***"))
    ok &= bool(r3)
    return 0 if ok else 1


def main() -> int:
    if "--control" in sys.argv:
        return control()
    if "--census" in sys.argv:
        return census()
    if "--emit" in sys.argv:
        n = bad = 0
        for r in rows():
            rec = build(r)
            why = validate(rec)
            if why:
                bad += 1
                print(f"# REFUSED {rec['id']}: {'; '.join(why)}", file=sys.stderr)
                continue
            n += 1
            print(json.dumps(rec, sort_keys=True))
        print(f"# {n} exported, {bad} refused", file=sys.stderr)
        return 1 if bad else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
