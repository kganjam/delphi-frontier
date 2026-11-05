#!/usr/bin/env python3
"""SPEC-ASK section 4 item 3: a transfer record in which a value CANNOT be separated from its
units, conditions and scope.

THE GAP THIS CLOSES, measured rather than assumed (2026-11-05):
  * D5 is the weakest dimension that is not honestly absent. Section 3 says "No export format
    that carries them. A consumer reading the DB directly can drop `conditions` without
    noticing."
  * `spec_parameter` holds **0 rows**. Its mandatory `conditions`/`units` columns are therefore
    VACUOUSLY satisfied -- the spec's own note says so, and section 1 rule 4 of AGENTS.md treats a
    vacuous pass as a release blocker. A constraint no row is subject to is not a constraint.
  * Meanwhile 442 live claims carry a numeric value and all 442 carry units -- in a FREE-TEXT
    column, beside a value, with nothing binding them together. Copy the number out and the units
    stay behind. That is precisely the D5 failure.

WHAT MAKES THIS A TRANSFER RECORD RATHER THAN A DUMP. The value is not addressable on its own.
There is no key whose value is the bare number: `quantity` is an object, and a consumer that
wants the number must take the object that carries its units, its evidence class, its read level,
its scope and its provenance. Dropping a field is not an oversight a reader can make silently --
validate() REFUSES the record, and the digest changes.

WHAT IT DOES NOT DO, stated because D5 is partial and must stay visibly partial: it does not make
ids resolvable (D1), it is not a federation protocol (D6), and it does not carry a dependency
closure sufficient to recompute the value. It carries enough that a consumer cannot MISREAD the
number, which is the specific thing D5 asks for.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__)))))
from dbq import PG, env, flat  # noqa: E402

SCHEMA = "morphoswarm/ask-transfer-record/v1"
#: Every one of these must be present and non-empty inside `quantity`. The value is deliberately
#: NOT reachable except through this object.
REQUIRED_IN_QUANTITY = ("value", "units", "evidence", "scope", "provenance")
#: `read_level` is required ONLY for evidence classes that rest on reading a source. MEASURED,
#: DERIVED and SIMULATED values have no paper to have read, and requiring it of them was this
#: module's first rule -- it refused 31 legitimate records (26 derived, 5 simulated) before the
#: distribution was checked. The two vocabularies are separate on purpose: `evidence` says how
#: the value was obtained, `read_level` how deeply its SOURCE was read.
READ_LEVEL_REQUIRED_FOR = ("literature", "refused")


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\x01") for ln in r.stdout.strip().split("\n") if ln]


def build(row: list[str]) -> dict:
    cid, project, scale, value, units, evidence, read_level, source, created = (row + [""] * 9)[:9]
    return {
        "schema": SCHEMA,
        "claim_id": cid,
        # The number lives HERE and nowhere else in the record.
        "quantity": {
            "value": float(value) if value else None,
            "units": units,
            "evidence": evidence,
            "read_level": read_level or None,
            "scope": {"project": project, "scale": scale or None},
            "provenance": {"source": source, "recorded_at": created},
        },
    }


def validate(rec: dict) -> list[str]:
    """Return the reasons this record may not be transferred. Empty list means it may."""
    bad = []
    if rec.get("schema") != SCHEMA:
        bad.append(f"schema is {rec.get('schema')!r}, not {SCHEMA!r}")
    qy = rec.get("quantity")
    if not isinstance(qy, dict):
        return bad + ["no `quantity` object: a bare value is not transferable"]
    for f in REQUIRED_IN_QUANTITY:
        v = qy.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, dict) and not v):
            bad.append(f"quantity.{f} is missing or empty")
    if qy.get("evidence") in READ_LEVEL_REQUIRED_FOR and not str(qy.get("read_level") or "").strip():
        bad.append(f"evidence is {qy.get('evidence')!r} but read_level is absent: a value taken "
                   f"from a source must say how deeply that source was read")
    # A value with no units is the exact D5 failure and is called out as such.
    if qy.get("value") is not None and not str(qy.get("units") or "").strip():
        bad.append("quantity.value present with no units -- this is the D5 failure")
    # A number must not be reachable outside the quantity object.
    for k, v in rec.items():
        if k != "quantity" and isinstance(v, (int, float)) and not isinstance(v, bool):
            bad.append(f"bare number at top level key {k!r}: value must only be inside quantity")
    return bad


def digest(rec: dict) -> str:
    return hashlib.sha256(json.dumps(rec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    proj = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
    rows = q(f"select id::text, project_id, coalesce(scale_id,''), coalesce(value_num::text,''), "
             f"{flat('units', 400)}, coalesce(evidence,''), coalesce(read_level,''), "
             f"{flat('source', 300)}, created_at::text "
             f"from claim where project_id = '{proj}' and superseded_by is null "
             f"and value_num is not null order by id")
    recs = [build(r) for r in rows]
    bad = [(r["claim_id"], validate(r)) for r in recs]
    refused = [(c, b) for c, b in bad if b]
    print(f"  {len(recs)} transferable quantities in {proj}")
    print(f"  {len(recs)-len(refused)} validate; {len(refused)} REFUSED\n")
    for cid, reasons in refused[:12]:
        print(f"    claim {cid}: {'; '.join(reasons)}")
    out = pathlib.Path(os.environ.get("MS_TRANSFER_OUT", "")) if os.environ.get("MS_TRANSFER_OUT") else None
    if out:
        payload = [r for r in recs if not validate(r)]
        out.write_text(json.dumps({"schema": SCHEMA, "project": proj,
                                   "records": payload,
                                   "digest": digest({"r": payload})}, indent=1))
        print(f"\n  wrote {len(payload)} records to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
