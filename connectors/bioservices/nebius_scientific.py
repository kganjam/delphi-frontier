"""Nebius Scientific AI — hosted scientific model execution over MCP.

Wraps the upload → submit → poll → fetch flow the server documents. Used here to
run a **hosted** ESM-2 scoring job as an independent implementation check on
scoring this harness also performed locally.

Credentials: read by the configured client in Delphi Evolve's
``gpuops/scientific_services``, from a mode-600 env file, into a header only.
**No credential is accepted as an argument here, printed, or written to any
artifact**, and the bearer token never appears in a URL.

Operational facts measured against the live service, recorded because none of
them is in the published schema:

- The reservation returns two upload routes. ``upload_url`` (the MCP host)
  returns **401** without a bearer header; ``direct_upload_url`` is a presigned
  object-store URL and works with no auth. This client prefers the presigned
  route so the token is never attached to a bulk transfer.
- A paused App answers submit with ``MODEL_MAINTENANCE``, ``admission:
  not-submitted``, and asks for **one** retry after 30 s **with the same
  idempotency key**. That is the server's own instruction and is obeyed exactly
  once; it is not a licence to loop.
- The server's standing instruction is: never retry inference with a *new* key
  after a timeout. Key reuse is how a lost response is recovered.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.request
from dataclasses import dataclass, field

GPUOPS = "/data/worktrees/delphi-evolve/gpuops"
MANIFEST_MEDIA_TYPE = "application/vnd.fs2.scientific-manifest+json"
TERMINAL = {"SUCCEEDED", "FAILED", "CANCELLED", "ERROR", "EXPIRED"}


class NebiusError(RuntimeError):
    pass


class ModelMaintenance(NebiusError):
    """The App is paused. Not a failure of the request, and not retryable in a loop."""


@dataclass
class JobRecord:
    """Everything needed to re-read a submission later, and nothing secret."""

    model_id: str
    operation: str
    idempotency_key: str
    artifact_id: str | None = None
    artifact_sha256: str | None = None
    operation_id: str | None = None
    submitted_utc: str | None = None
    states: list[str] = field(default_factory=list)
    final_state: str | None = None
    error: dict | None = None
    result: dict | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


def _client():
    if GPUOPS not in sys.path:
        sys.path.insert(0, GPUOPS)
    from scientific_services.nebius_mcp import NebiusMCP

    c = NebiusMCP()
    c.initialize()
    return c, NebiusMCP


def _payload(NebiusMCP, res) -> dict:
    return NebiusMCP.tool_payload(res)


def _raise_if_error(payload: dict) -> dict:
    err = payload.get("error") if isinstance(payload, dict) else None
    if err:
        if err.get("code") == "MODEL_MAINTENANCE":
            raise ModelMaintenance(json.dumps(err))
        raise NebiusError(json.dumps(err)[:800])
    return payload


def upload_manifest(model_id: str, manifest: dict, idempotency_key: str) -> dict:
    """Upload a manifest and return its artifact reference."""
    c, NebiusMCP = _client()
    body = json.dumps(manifest).encode()
    sha = hashlib.sha256(body).hexdigest()
    begin = _raise_if_error(_payload(NebiusMCP, c.call_tool(
        "begin_scientific_artifact_upload",
        {"model_id": model_id, "sha256": sha, "size_bytes": len(body),
         "media_type": MANIFEST_MEDIA_TYPE, "idempotency_key": idempotency_key})))
    upload_id = begin["upload_id"]

    url = begin.get("direct_upload_url")
    headers = {"Content-Type": MANIFEST_MEDIA_TYPE}
    if not url:  # fall back to the authenticated host route
        url = begin["upload_url"]
        headers["Authorization"] = "Bearer " + c._key
    req = urllib.request.Request(url, data=body, method="PUT", headers=headers)
    with urllib.request.urlopen(req, timeout=300) as resp:
        if resp.status not in (200, 201, 204):
            raise NebiusError(f"upload PUT returned {resp.status}")

    fin = _raise_if_error(_payload(NebiusMCP, c.call_tool(
        "finalize_scientific_artifact_upload", {"upload_id": upload_id})))
    art = fin.get("artifact", fin)
    if art["sha256"] != sha:
        raise NebiusError("finalized artifact checksum does not match what was uploaded")
    return {"artifact_id": art["artifact_id"], "sha256": art["sha256"],
            "size_bytes": art["size_bytes"], "media_type": art["media_type"]}


def submit(model_id: str, tool_name: str, operation: str, artifact_ref: dict,
           parameters: dict, idempotency_key: str,
           maintenance_retry: bool = True) -> dict:
    """Submit once. On MODEL_MAINTENANCE, wait as instructed and retry ONCE."""
    c, NebiusMCP = _client()
    args = {"schema": "fs2-serve.nebius.ai/scientific-run-request/v1",
            "operation": operation, "service_class": "customer-batch",
            "input_manifest": artifact_ref, "parameters": parameters,
            "idempotency_key": idempotency_key}
    try:
        return _raise_if_error(_payload(NebiusMCP, c.call_tool(tool_name, args)))
    except ModelMaintenance as exc:
        if not maintenance_retry:
            raise
        detail = json.loads(str(exc))
        wait = int(detail.get("retry_after_seconds", 30))
        time.sleep(wait + 2)
        # Same key on purpose: the server documents key reuse as the recovery path.
        return _raise_if_error(_payload(NebiusMCP, c.call_tool(tool_name, args)))


def poll(operation_id: str, timeout_s: float = 1500, interval_s: float = 15) -> dict:
    """Poll until terminal or the budget runs out. Never resubmits."""
    c, NebiusMCP = _client()
    deadline = time.time() + timeout_s
    seen: list[str] = []
    last: dict = {}
    while time.time() < deadline:
        last = _payload(NebiusMCP, c.call_tool("get_operation", {"operation_id": operation_id}))
        state = str(last.get("status") or last.get("state") or "UNKNOWN").upper()
        if not seen or seen[-1] != state:
            seen.append(state)
        if state in TERMINAL:
            return {"states": seen, "final": state, "detail": last}
        time.sleep(interval_s)
    return {"states": seen, "final": "TIMEOUT_WHILE_POLLING", "detail": last}


def result(operation_id: str) -> dict:
    c, NebiusMCP = _client()
    return _payload(NebiusMCP, c.call_tool("get_operation_result", {"operation_id": operation_id}))


def build_manifest(files: dict[str, str]) -> dict:
    """Manifest carrying each input file by name.

    The manifest schema is **not published** by the server; this shape was
    inferred from the request schema, which names ``fasta_file`` and
    ``variants_file`` as paths *within* the manifest. It is recorded as inferred
    so a later mismatch is read as a wrong guess here rather than as a service
    fault.
    """
    return {"schema": "fs2-serve.nebius.ai/scientific-manifest/v1", "files": dict(files)}
