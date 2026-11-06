#!/usr/bin/env python3
"""Submit one sequence to Nebius BioEmu2, recording the operation id before anything can lose it.

WHY THIS FILE EXISTS. BioEmu2 is the only model left on this endpoint that could give the
project a FUNCTIONAL or thermodynamic readout rather than another structure. Claim 507
enumerated all 26 catalogue models and found none that computes monomer stability; claim 1449
narrowed what remains to this one, because K2P gating is a conformational equilibrium and
`sample-equilibrium` is one of its four operations. It was unreachable until now for a purely
mechanical reason: the submit takes an `input_manifest` whose entry name and semantic type are
NOT PUBLISHED. Only 5 of the 26 models carry an `input_artifact_contract` (alphafold3,
cosmos3-lerobot-augmentation, holoscan-endoscopy, isaac-healthcare, monai-spleen-ct) and
bioemu2 is not among them.

THE SHAPE, recovered 2026-11-05 and the reason this is a file and not a shell line:

    name           "workload"
    semantic_type  "bioemu2-workload-tar/v1"
    artifact       a TAR, media type application/x-tar, holding the input files

THE VALIDATOR DISCRIMINATES, WHICH IS WHAT MADE IT FINDABLE, and it is worth recording because
the isaac-healthcare case behaved the opposite way -- there one error message came back for
seven different candidate shapes and for an empty manifest, so it could not tell a wrong key
from no content. Here the two failure modes are distinguishable:

    wrong NAME            "BioEmu2 input manifest must contain exactly one verified workload entry"
    right name, wrong TYPE "BioEmu2 workload semantic type is invalid"

So the name was settled first, by watching the message change, and only then the type. A JSON
inner artifact (the shape esmfold2 uses) gives the first message, which is how the tar
requirement was found. Every rejection carries `admission: "not-submitted"`, and validation
runs before admission, so none of these probes occupies the single serial slot.

CONVENTION, for the next unpublished model: holoscan-endoscopy, the one model whose contract
spells out a workload, uses logical_artifact_id "workload" with semantic_type
"holoscan-recorded-video-tar/v1". `<model>-<content>-tar/v1` with the name `workload` is
therefore the first thing to try, and it is what worked here on the first candidate.

    python3 submit_bioemu2.py <label> <sequence> [operation] [num_samples]

ALWAYS SETS AN IDEMPOTENCY KEY, and sets a DETERMINISTIC one. A submit whose key cannot be
reproduced is unrecoverable: a 503 or a lost response leaves an operation that holds the slot,
cannot be cancelled (`cancel_operation` refuses with "recover the original admission with the
same idempotency key first") and cannot be completed. The key here is derived from the label
and a sha256 of the inputs. It must NOT come from `hash()`, which Python salts per process --
measured here the same day, on a probe whose id then had to be recovered from the operations
listing.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import tarfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "library", "tools"))
import nbx  # noqa: E402

MODEL = "bioemu2"
OPS_LOG = "/data/swarm/nebius-ops.jsonl"
VALID = re.compile(r"^[ACDEFGHIKLMNPQRSTVWY]+$")
OPERATIONS = ("sample-equilibrium", "predict-structure", "propagate", "simulate-trajectory")


def record(op_id: str, note: str) -> None:
    with open(OPS_LOG, "a") as f:
        f.write(json.dumps({"op": op_id, "tool": "submit_bioemu2", "note": note,
                            "t": time.time()}) + "\n")


def workload_tar(sequence: str) -> bytes:
    """The inner artifact. A tar, not JSON -- a JSON inner artifact is rejected (see module docstring)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as t:
        for name, data in (("sequence.fasta", f">input\n{sequence}\n".encode()),
                           ("input.json", json.dumps({"sequence": sequence}).encode())):
            ti = tarfile.TarInfo(name)
            ti.size = len(data)
            t.addfile(ti, io.BytesIO(data))
    return buf.getvalue()


def submit(label: str, sequence: str, operation: str = "sample-equilibrium",
           num_samples: int = 8, seed: int = 42) -> tuple[str | None, dict]:
    sequence = sequence.strip().upper()
    if not VALID.match(sequence):
        raise SystemExit("sequence has characters outside the 20 standard amino acids: "
                         f"{sorted(set(sequence) - set('ACDEFGHIKLMNPQRSTVWY'))}")
    if operation not in OPERATIONS:
        raise SystemExit(f"operation must be one of {OPERATIONS}")

    tar = workload_tar(sequence)
    inner = nbx.upload(tar, "application/x-tar", MODEL)
    if "artifact_id" not in inner:
        raise SystemExit(f"workload upload failed: {json.dumps(inner)[:300]}")

    mf_body = json.dumps({
        "schema": "fs2-serve.nebius.ai/scientific-artifact-manifest/v1",
        "artifacts": [{"name": "workload",
                       "semantic_type": "bioemu2-workload-tar/v1",
                       "artifact": inner}]}).encode()
    mf = nbx.upload(mf_body, "application/vnd.fs2.scientific-manifest+json", MODEL)
    if "artifact_id" not in mf:
        raise SystemExit(f"manifest upload failed: {json.dumps(mf)[:300]}")

    # Deterministic, so a lost response can be replayed. NOT hash().
    digest = hashlib.sha256(f"{label}|{sequence}|{operation}|{num_samples}|{seed}"
                            .encode()).hexdigest()[:16]
    idem = f"ms-bioemu2-{digest}"

    req = {"schema": "fs2-serve.nebius.ai/scientific-run-request/v1",
           "operation": operation,
           "service_class": "customer-batch",
           "input_manifest": mf,
           "parameters": {"num_samples": num_samples,
                          "batch_size": min(num_samples, 8), "seed": seed},
           "idempotency_key": idem}
    out = nbx.call("submit_bioemu2", req)
    op = (out.get("operation_id") or out.get("id")
          or (out.get("operation") or {}).get("id"))
    if not op:
        m = re.search(r"(op-[0-9a-f]{16})", json.dumps(out))
        op = m.group(1) if m else None
    record(op or "UNKNOWN", f"{label} ({operation}, key {idem}, n={num_samples}, seed {seed})"
           + ("" if op else f" -- NO OPERATION ID: {json.dumps(out)[:300]}"))
    print(f"idempotency key {idem}  (deterministic: re-running this exact command replays it)")
    return op, out


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    label, seq = sys.argv[1], sys.argv[2]
    operation = sys.argv[3] if len(sys.argv) > 3 else "sample-equilibrium"
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    op, out = submit(label, seq, operation, n)
    print(f"operation: {op}")
    print(json.dumps(out, indent=1)[:600])
    return 0 if op else 1


if __name__ == "__main__":
    raise SystemExit(main())
