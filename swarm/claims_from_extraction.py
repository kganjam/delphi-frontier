#!/usr/bin/env python3
"""Put verified extracted values into the claim graph, with the paper's provenance preserved.

WHY THIS EXISTS. `extract_values.py --write` wrote a JSON file and stopped. 225 retrieved full
texts, a working quote check and a correct refusal to fabricate all dead-ended in
`results/extracted-values.json`, which nothing read. A retrieval pipeline whose output no part
of the system consumes is indistinguishable from one that was never run -- and for a while it
was literally indistinguishable, because the file contained `{"verified": [], "discarded": []}`.

THE EVIDENCE LABEL IS THE WHOLE JOB, and it is NOT `measured`.
This project did not measure any of these numbers; a published paper did, or modelled it, or
quoted it from somewhere else. The extractor records which, in `provenance`, and that maps onto
this project's closed evidence vocabulary:

    measured-here  -> literature   the authors measured it and we READ that
    quoted         -> literature   the paper attributes it to an earlier study; attribution kept
    modelled-here  -> simulated    an output of that paper's model, not an observation
    assumed-here   -> assumed      a constant their model takes as input
    unclear        -> unknown      the excerpt did not say, and guessing is worse than not

Nothing here is written as `measured`. That matters because the project's own goal scoreboard
counts `measured` claims carrying a biological scale, and relabelling literature as measurement
would move that number without a single new observation existing. The row is supposed to be hard.

WHAT A `read_level: abstract` ROW IS AND IS NOT. Most of these come from abstracts, because the
measurements this project needs are in journals outside PMC's open-access subset. An abstract
gives the headline number with no methods, no table and no conditions. Each row carries the
label, and a value read in an abstract must never be written up in the voice of having read the
paper (docs/research/README.md). It is a lead with a number attached, and it is a great deal
better than the nothing that was there before.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbq  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
EXTRACT = pathlib.Path(__file__).resolve().parent.parent / "results" / "extract"

EVIDENCE = {
    "measured-here": "literature",
    "quoted": "literature",
    "modelled-here": "simulated",
    "assumed-here": "assumed",
    "unclear": "unknown",
    "": "unknown",
}


def numeric(value) -> float | None:
    """First number in the value string, or None. A range like '0.0001 to 1.5109' keeps its low
    end in value_num and its full text in the statement -- a range is not a scalar, and picking
    the midpoint would invent a number the paper never stated."""
    import re
    if isinstance(value, (int, float)):
        return float(value)
    m = re.search(r"-?\d[\d,]*\.?\d*(?:\s*[x×]\s*10\s*\(?-?\d+\)?)?", str(value or ""))
    if not m:
        return None
    raw = m.group(0).replace(",", "")
    exp = re.search(r"[x×]\s*10\s*\(?(-?\d+)\)?", raw)
    try:
        base = float(re.split(r"[x×]", raw)[0].strip())
        return base * (10 ** int(exp.group(1))) if exp else base
    except Exception:                                             # noqa: BLE001
        return None


def load(paths: list[pathlib.Path]) -> list[dict]:
    out = []
    for p in paths:
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:                                         # noqa: BLE001
            continue
        for v in d.get("verified", []):
            if v.get("verified_quote"):
                v["_file"] = p.name
                out.append(v)
    return out


def source_string(it: dict) -> str:
    bits = [str(it.get("paper", "")).strip()]
    for key in ("journal", "year", "doi"):
        if it.get(key):
            bits.append(str(it[key]))
    if it.get("provenance") == "quoted" and it.get("attributed_to"):
        bits.append(f"value attributed by that paper to {it['attributed_to']}")
    bits.append(f'quote verified against the source: "{str(it.get("quote", ""))[:220]}"')
    return "; ".join(b for b in bits if b)


def statement(it: dict) -> str:
    prov = str(it.get("provenance", "unclear"))
    how = {"measured-here": "MEASURED BY THAT PAPER",
           "modelled-here": "AN OUTPUT OF THAT PAPER'S MODEL, NOT AN OBSERVATION",
           "assumed-here": "A CONSTANT THAT PAPER'S MODEL ASSUMES",
           "quoted": "QUOTED BY THAT PAPER FROM AN EARLIER STUDY",
           "unclear": "PROVENANCE NOT DETERMINABLE FROM THE TEXT READ"}.get(prov, prov)
    sp = str(it.get("species") or "unstated")
    cond = str(it.get("conditions") or "unstated")
    lvl = str(it.get("read_level") or "full-text")
    return (f"[LITERATURE VALUE, {how}] {it.get('value')} {it.get('units') or ''}".strip()
            + f"\nspecies: {sp}\nconditions: {cond}\n"
            + f"read level: {lvl} -- "
            + ("an abstract states a number without its methods, table or conditions; this is a "
               "lead with a number attached and is not a reading of the paper"
               if lvl == "abstract" else "full text read")
            + f"\nasked: question {it.get('asked')} of the open-constraint question set")


def main() -> int:
    write = "--write" in sys.argv
    files = [EXTRACT / "abstracts.json", EXTRACT / "targeted.json",
             EXTRACT.parent / "extracted-values.json"]
    items = load(files)
    print("=" * 78)
    print("EXTRACTED VALUES -> CLAIMS")
    print("=" * 78)
    print(f"  {len(items)} verified value(s) in {len([f for f in files if f.exists()])} file(s)")

    # Dedupe against what is already recorded. The source string carries the paper id and the
    # quote, so re-running the harvester cannot double-record the same sentence.
    existing = {r[0] for r in dbq.q(
        f"select source from claim where project_id = {dbq.lit(PROJECT)} "
        "and source like '%quote verified against the source%'")}
    rows, skipped, nonum = [], 0, 0
    for it in items:
        src = source_string(it)
        if src in existing:
            skipped += 1
            continue
        existing.add(src)
        if numeric(it.get("value")) is None:
            nonum += 1
        rows.append((it, src))

    by_ev: dict[str, int] = {}
    for it, _ in rows:
        ev = EVIDENCE.get(str(it.get("provenance", "")), "unknown")
        by_ev[ev] = by_ev.get(ev, 0) + 1
    print(f"  {len(rows)} new, {skipped} already recorded, {nonum} with no parseable number")
    print(f"  evidence mapping: {by_ev}")
    print("  NOTE: none of these is `measured`. This project measured none of them; the "
          "goal scoreboard's measured-with-a-scale row does NOT move, by design.")

    # TWO-SIDED CONTROL on the mapping itself, before anything is written.
    probe = {"provenance": "modelled-here", "value": "565 × 10(-6)", "units": "N m^2"}
    must_not_be_measured = EVIDENCE[probe["provenance"]] == "simulated"
    must_parse = abs((numeric(probe["value"]) or 0) - 565e-6) < 1e-9
    must_reject = numeric("no number here at all") is None
    ok = must_not_be_measured and must_parse and must_reject
    print(f"  [{'ok' if ok else 'FAIL'}] controls: a modelled value maps to `simulated` "
          f"({must_not_be_measured}); 565 x 10(-6) parses to 5.65e-4 ({must_parse}); "
          f"prose yields no number ({must_reject})")
    if not ok:
        print("\n  ABORTING: the mapping is what this module is for.")
        return 2

    for it, src in rows[:12]:
        print(f"    {str(it.get('paper'))[:13]:<13} {str(it.get('value'))[:22]:<22} "
              f"{str(it.get('units'))[:12]:<12} {EVIDENCE.get(str(it.get('provenance')), '?'):<11} "
              f"{str(it.get('read_level') or 'full-text')}")

    if not write:
        print("\n  (dry run; pass --write to record)")
        return 0

    n = 0
    for it, src in rows:
        cid = dbq.write_claim(PROJECT, None, statement(it),
                              EVIDENCE.get(str(it.get("provenance", "")), "unknown"),
                              numeric(it.get("value")), str(it.get("units") or "")[:400],
                              src, str(it.get("read_level") or "full-text"))
        n += 1 if cid else 0
    print(f"\n  recorded {n} claim(s)")
    print("  scale_id is left NULL: the generalised question no longer names the constraint's "
          "scale, and assigning one by guessing the unit would be the invention this pipeline "
          "exists to avoid. Reported rather than filled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
