#!/usr/bin/env python3
"""Submit one sequence to Nebius ESMFold2, recording the operation id before anything can lose it.

Written because the previous ESMFold2 submissions were built ad hoc and nothing in the repository
could rebuild one: the input shape had to be recovered by downloading a successful run's own input
manifest. The shape is not guessable -- the wrapper key is `artifacts`, each entry NESTS its ref
under `artifact`, and the server returns the identical error for a wrong key and for an empty
manifest, so a wrong shape cannot be distinguished from no content.

    python3 submit_esmfold2.py <label> <sequence> [seed]

The seed is explicit and defaults to 0 because a mutant compared against a wild type run at a
different seed is not a controlled comparison.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "library", "tools"))
import nbx  # noqa: E402

MODEL = "esmfold2"
OPS_LOG = "/data/swarm/nebius-ops.jsonl"
VALID = re.compile(r"^[ACDEFGHIKLMNPQRSTVWYX]+$")


def record(op_id: str, note: str) -> None:
    import time
    with open(OPS_LOG, "a") as f:
        f.write(json.dumps({"op": op_id, "tool": "submit_esmfold2", "note": note, "t": time.time()}) + "\n")


def submit(label: str, sequence: str, seed: int = 0) -> tuple[str | None, dict]:
    sequence = sequence.strip().upper()
    if not VALID.match(sequence):
        raise SystemExit(f"sequence has characters outside the model's alphabet: "
                         f"{sorted(set(sequence) - set('ACDEFGHIKLMNPQRSTVWYX'))}")
    if not 1 <= len(sequence) <= 4096:
        raise SystemExit(f"sequence length {len(sequence)} outside 1..4096")

    idem = f"ms-{label}"
    inner = nbx.upload(json.dumps({"sequence": sequence}).encode(), "application/json", MODEL)
    if "artifact_id" not in inner:
        raise SystemExit(f"inner upload failed: {json.dumps(inner)[:300]}")
    mf_body = json.dumps({
        "schema": "fs2-serve.nebius.ai/scientific-artifact-manifest/v1",
        "artifacts": [{"name": "esmfold2-input",
                       "semantic_type": "esmfold2-input-json/v1",
                       "artifact": inner}]}).encode()
    mf = nbx.upload(mf_body, "application/vnd.fs2.scientific-manifest+json", MODEL)
    if "artifact_id" not in mf:
        raise SystemExit(f"manifest upload failed: {json.dumps(mf)[:300]}")

    req = {"schema": "fs2-serve.nebius.ai/scientific-run-request/v1",
           "operation": "predict-structure",
           "service_class": "customer-batch",
           "input_manifest": mf,
           "parameters": {"sequence": sequence, "mode": "single-sequence", "seed": seed},
           "idempotency_key": idem}
    out = nbx.call("submit_esmfold2", req)
    op = (out.get("operation_id") or out.get("id")
          or (out.get("operation") or {}).get("id"))
    # Record BEFORE returning, and record from a failure too: an unrecorded id is an
    # unreclaimable slot, and there is no tool that lists pending operations.
    if op:
        record(op, f"{label} (key {idem}, seed {seed})")
    else:
        blob = json.dumps(out)
        m = re.search(r"(op-[0-9a-f]{16})", blob)
        if m:
            record(m.group(1), f"{label} (key {idem}) -- id recovered from an error reply")
            op = m.group(1)
        else:
            record("UNKNOWN", f"{label} (key {idem}) -- NO OPERATION ID: {blob[:300]}")
    return op, out


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    label, seq = sys.argv[1], sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    op, out = submit(label, seq, seed)
    print(f"  {label}: operation {op}")
    if not op:
        print(f"  response: {json.dumps(out)[:400]}")
    return 0 if op else 1


if __name__ == "__main__":
    sys.exit(main())
