#!/usr/bin/env python3
"""ProteinMPNN across monomer / dimer / truncated-dimer, keeping the single Nebius slot busy.

THE QUESTION. The project's existing kcnk5b ProteinMPNN run was on a MONOMER, so every
constraint it reports is cis. Claim 1043 established that the functional channel is a dimer
and produced one (OpenFold3 + the pdb70 alignment) that reproduces canonical K2P architecture:
the extracellular cap and both stretches flanking the two selectivity filters form the
interface. Interface residues should be MORE constrained in the dimer than in the monomer,
because the monomer run never saw the partner chain. Nobody has measured that.

THE CONTROLS ARE THE OTHER TWO RUNS. Comparing a dimer against the OLD monomer run would
confound oligomeric state with the structure-prediction method, so the monomer is re-predicted
and re-run through the same pipeline. The truncated dimer then asks whether removing the
C-terminus changes interface constraint -- claim 1045 found it does not change the pore's
geometry, which is a different question from whether it changes what sequence the fold admits.

THE SLOT IS THE SCARCE RESOURCE, not money: ONE operation at a time across all 69 tools, so
the only throughput lever is never leaving it idle. This submits, polls, fetches and moves on.

    python3 mpnn_series.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nebius  # noqa: E402

D = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "results" / "fish-proteins" / "structures"
RUNS = (
    ("kcnk5b-homodimer-msa", ["A", "B"], "full-length homodimer"),
    ("kcnk5b-monomer-msa", ["A"], "full-length monomer, the method control"),
    ("kcnk5b-trunc240-dimer-msa", ["A", "B"], "truncated 1-240 homodimer"),
)


def already(label: str) -> str | None:
    """The op id of a previous submit of this label, so a re-run does not duplicate."""
    log = pathlib.Path("/data/swarm/nebius-ops.jsonl")
    if not log.exists():
        return None
    for line in log.read_text().splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        note = d.get("note", "")
        op = d.get("op", "")
        # Match the series tag OR a hand-submitted run of the same structure. The full-length
        # dimer was submitted by hand before this script existed, under a different
        # idempotency key, and without this the series would duplicate it against a slot that
        # admits ONE operation -- which is exactly what happened: a 503 with
        # admission "unknown", on a job already running.
        if op.startswith("op-") and (note.startswith(f"mpnn-series:{label}")
                                     or (label in note and "roteinMPNN" in note)):
            return op
    return None


def wait(op: str, limit_s: int = 1800) -> str:
    t0 = time.time()
    while time.time() - t0 < limit_s:
        d = nebius.call("get_operation", {"operation_id": op})
        st = (d.get("operation") or {}).get("status") or "?"
        if st in ("SUCCEEDED", "FAILED", "CANCELLED") or d.get("result_available"):
            return st
        time.sleep(20)
    return "TIMEOUT-LOCALLY"


def main() -> int:
    for label, chains, why in RUNS:
        pdb = D / label / "model.pdb"
        if not pdb.exists():
            print(f"  {label}: no model.pdb, skipping")
            continue
        out = D / label / "mpnn"
        op = already(label)
        if op is None:
            data = pdb.read_bytes()
            print(f"\n=== {label} ({why}) ===\n  uploading {len(data)} bytes", flush=True)
            ref = nebius.upload(data, "chemical/x-pdb", "proteinmpnn", f"ms-{label}-pdb-v1")
            # A 503 here means "admission unknown": the submit may or may not have landed, and
            # the endpoint's own next_action is to retry with the ORIGINAL idempotency key,
            # which makes the retry idempotent rather than a second job. One failed structure
            # must not abandon the rest of the series, so this continues instead of raising.
            op = None
            for attempt in range(6):
                try:
                    op, _ = nebius.submit("infer_proteinmpnn_native", {
                        "input_pdb": ref, "input_pdb_chains": chains,
                        "num_seq_per_target": 8, "sampling_temp": 0.1, "random_seed": 42,
                        "idempotency_key": f"ms-{label}-mpnn-v1"},
                        f"mpnn-series:{label} -- {why}; interface constraint in the dimer context")
                    break
                except RuntimeError as e:
                    # READ THE ERROR BODY. A 503 from this endpoint is several different
                    # failures wearing one status code, and `admission` says which:
                    #   not-submitted  -> validation; nothing was created; retrying is pointless
                    #   accepted + phase=observation + operation_id -> THE JOB IS FINE and the
                    #       OBSERVATION path failed. Resubmitting is wrong; take the op id.
                    #   not-confirmed  -> the serverless layer is degraded generally
                    # Measured 2026-11-05: six submits read as failures had all been ACCEPTED,
                    # and a plain retry minutes later succeeded, so this loop reported "giving
                    # up" on work that existed.
                    try:
                        err = json.loads(str(e))
                    except json.JSONDecodeError:
                        err = {}
                    if err.get("operation_id"):
                        op = err["operation_id"]
                        print(f"  attempt {attempt+1}: {err.get('code')} but the operation "
                              f"EXISTS ({op}, admission={err.get('admission')!r}, "
                              f"phase={err.get('phase')!r}) -- taking it, not resubmitting",
                              flush=True)
                        nebius.record(op, "infer_proteinmpnn_native",
                                      f"mpnn-series:{label} -- recovered from a "
                                      f"{err.get('code')} carrying its operation_id")
                        break
                    print(f"  submit attempt {attempt+1} failed "
                          f"(admission={err.get('admission')!r}): {str(e)[:110]}", flush=True)
                    time.sleep(90)
            if op is None:
                print(f"  GIVING UP on {label} after 6 attempts; continuing with the rest",
                      flush=True)
                continue
            print(f"  submitted {op}", flush=True)
        else:
            print(f"\n=== {label} ===\n  already submitted as {op}", flush=True)
        st = wait(op)
        print(f"  {op} -> {st}", flush=True)
        if st == "SUCCEEDED":
            out.mkdir(parents=True, exist_ok=True)
            os.system(f"python3 {os.path.dirname(os.path.abspath(__file__))}/fetch_results.py "
                      f"{op} {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
