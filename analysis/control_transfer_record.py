#!/usr/bin/env python3
"""Controls for the ASK transfer record. A validator that never refuses is not a validator.

Over the live corpus every record validates, which is the correct outcome and also exactly how
a broken validator looks (AGENTS.md section 6b: a gate that is off looks like a gate that
passed). So each arm MUTATES ONE FIELD of a REAL record -- never a hand-written fixture, which
can be wrong in a way that makes the check pass for the wrong reason.
"""
from __future__ import annotations

import copy
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "swarm"))
import transfer_record as TR  # noqa: E402


def main() -> int:
    rows = TR.q(f"select id::text, project_id, coalesce(scale_id,''), coalesce(value_num::text,''), "
                f"{TR.flat('units', 400)}, coalesce(evidence,''), coalesce(read_level,''), "
                f"{TR.flat('source', 300)}, created_at::text "
                f"from claim where project_id = 'zebrafish-flight' and superseded_by is null "
                f"and value_num is not null and coalesce(units,'') <> '' "
                f"and evidence = 'literature' order by id limit 1")
    if not rows:
        print("  no literature record with units to mutate; cannot run controls")
        return 1
    real = TR.build(rows[0])
    arms = []

    arms.append(("must-NOT-flag  unmutated real record", TR.validate(real), False))

    a = copy.deepcopy(real)
    a["quantity"]["units"] = ""
    arms.append(("must-flag      units stripped (the D5 failure)", TR.validate(a), True))

    b = copy.deepcopy(real)
    b["quantity"].pop("scope")
    arms.append(("must-flag      scope removed", TR.validate(b), True))

    c = copy.deepcopy(real)
    c["quantity"].pop("provenance")
    arms.append(("must-flag      provenance removed", TR.validate(c), True))

    d = copy.deepcopy(real)
    d["quantity"]["read_level"] = ""
    arms.append(("must-flag      literature record with no read_level", TR.validate(d), True))

    e = copy.deepcopy(real)
    e["value_num"] = e["quantity"]["value"]
    arms.append(("must-flag      value hoisted to top level, bypassing units", TR.validate(e), True))

    f = copy.deepcopy(real)
    f["quantity"]["evidence"] = "measured"
    f["quantity"]["read_level"] = ""
    arms.append(("must-NOT-flag  MEASURED record with no read_level (no source to read)",
                 TR.validate(f), False))

    g = copy.deepcopy(real)
    g["schema"] = "something/else/v1"
    arms.append(("must-flag      wrong schema", TR.validate(g), True))

    ok = True
    for label, reasons, should_flag in arms:
        flagged = bool(reasons)
        good = flagged == should_flag
        ok &= good
        print(f"  {'PASS' if good else '*** FAIL ***'}  {label}")
        if reasons:
            print(f"           -> {reasons[0]}")
    print(f"\n  all arms behave: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
