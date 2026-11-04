#!/usr/bin/env python3
"""Nebius Scientific AI: upload artifacts, submit a run, poll it, read the result.

Written as a library rather than a one-off because the upload/manifest/submit/poll dance is four
round trips with a checksum and an idempotency key, and getting it wrong is how the slot got
self-blocked once already -- operations were submitted whose IDs were never captured, and there is
NO list-operations tool, so they could not be found or cancelled afterwards.

So: EVERY submit writes its operation id to OPS_LOG before it returns. A submit whose id is not
recorded is a slot that cannot be reclaimed.
"""
from __future__ import annotations

import hashlib
import json
import os
import ssl
import sys
import time
import urllib.request

URL = "https://89.169.99.188/mcp"
OPS_LOG = "/data/swarm/nebius-ops.jsonl"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def key():
    for line in open(os.path.expanduser("~/.config/morphoswarm/nebius.env")):
        if line.startswith("NEBIUS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no NEBIUS_API_KEY")


K = key()


def call(tool, args, timeout=180):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {K}", "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        raw = r.read().decode()
    d = json.loads(raw[raw.find("{"):])
    if "error" in d and "result" not in d:
        raise RuntimeError(json.dumps(d["error"])[:400])
    txt = d["result"]["content"][0]["text"]
    try:
        out = json.loads(txt)
    except json.JSONDecodeError:
        return {"_text": txt}
    if isinstance(out, dict) and "error" in out:
        raise RuntimeError(json.dumps(out["error"])[:400])
    return out


def upload(data: bytes, media_type: str, model_id: str, idem: str):
    """Reserve, PUT, finalize. Returns the artifact_ref a manifest or submit can carry."""
    sha = hashlib.sha256(data).hexdigest()
    res = call("begin_scientific_artifact_upload", {
        "model_id": model_id, "sha256": sha, "size_bytes": len(data),
        "media_type": media_type, "compression": "none", "idempotency_key": idem})
    up_id = res.get("upload_id") or res.get("id")
    # TWO transports come back. `upload_url` is the API endpoint and NEEDS the bearer -- sending
    # the bytes there without it is a 401, which reads exactly like a bad key rather than a missing
    # header. `direct_upload_url` is presigned S3 and takes NO headers at all (its signature covers
    # `host` only, so adding Content-Type invalidates it) but expires in 60 s. Prefer the API
    # endpoint: it does not race the clock.
    put = res.get("upload_url") or res.get("content_path")
    if put.startswith("/"):
        put = URL.rsplit("/mcp", 1)[0] + put
    req = urllib.request.Request(put, data=data, method="PUT", headers={
        "Authorization": f"Bearer {K}", "Content-Type": media_type})
    with urllib.request.urlopen(req, timeout=300, context=CTX) as r:
        r.read()
    fin = call("finalize_scientific_artifact_upload", {"upload_id": up_id})
    art = fin.get("artifact") or fin
    return {"artifact_id": art.get("artifact_id") or art.get("id"), "sha256": sha,
            "size_bytes": len(data), "media_type": media_type, "compression": "none"}


def manifest(entries, model_id, idem):
    """entries: [(name, semantic_type, bytes, media_type)] -> the manifest's own artifact_ref."""
    items = []
    for name, sem, data, mt in entries:
        ref = upload(data, mt, model_id, f"{idem}-{name}")
        items.append({"name": name, "semantic_type": sem, "artifact": ref})
    # The wrapper key is `artifacts`, NOT `entries`, and each entry NESTS its ref under `artifact`
    # rather than spreading it. Both were established the hard way in a previous session and are
    # recorded in the nebius-scientific-ai-workbench memory; the server's error for a wrong shape
    # is the same string as for an empty manifest, so it cannot be found by guessing.
    body = json.dumps({"schema": "fs2-serve.nebius.ai/scientific-artifact-manifest/v1",
                       "artifacts": items}).encode()
    return upload(body, "application/vnd.fs2.scientific-manifest+json", model_id, f"{idem}-mf")


def record(op_id, tool, note):
    with open(OPS_LOG, "a") as f:
        f.write(json.dumps({"op": op_id, "tool": tool, "note": note, "t": time.time()}) + "\n")


def submit(tool, args, note=""):
    # An ADMISSION_PENDING / 503 reply arrives as an ERROR and still carries an operation_id. That
    # id is the only handle on the work: there is no list-pending view, and cancel is refused until
    # admission is recovered. Recording only on success is how four operations were lost
    # permanently. Record from the error path too, then re-raise.
    try:
        out = call(tool, args)
    except RuntimeError as e:
        try:
            op = json.loads(str(e)).get("operation_id")
        except json.JSONDecodeError:
            op = None
        if op:
            record(op, tool, f"{note} -- ADMISSION_PENDING at submit; replay the SAME key")
        raise
    op = out.get("operation_id") or out.get("id") or out.get("operation", {}).get("id")
    if op:
        record(op, tool, note)      # BEFORE returning: an unrecorded id is an unreclaimable slot
    else:
        record("UNKNOWN", tool, f"{note} -- NO OPERATION ID IN RESPONSE: {json.dumps(out)[:300]}")
    return op, out


def wait(op, timeout=1800, every=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = call("get_operation", {"operation_id": op})
        # THREE RESPONSE SHAPES, all seen on this endpoint in one session:
        #   batch tools (submit_esmfold2)      -> top-level "status"
        #   some native tools (msa_search)     -> top-level "result_available"
        #   other native tools (proteinmpnn)   -> status NESTED under "operation"
        # Reading only the top level returns None for the third, so a poll loop prints a blank
        # status forever and is blind to SUCCEEDED. Read all three.
        s = (st.get("status") or st.get("state")
             or (st.get("operation") or {}).get("status") or "").lower()
        # `result_available` is how this API signals completion; there is no top-level `status` on
        # a finished native op. Polling only for "succeeded" waits out the full timeout on a job
        # that finished minutes ago -- the request succeeds every time, so nothing looks wrong.
        if st.get("result_available") or st.get("done") or s in (
                "succeeded", "failed", "cancelled", "completed", "error"):
            return st
        time.sleep(every)
    return {"status": "TIMEOUT-LOCALLY", "note": "still running server side", "operation_id": op}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ops"
    if cmd == "ops":
        for line in open(OPS_LOG) if os.path.exists(OPS_LOG) else []:
            d = json.loads(line)
            try:
                st = call("get_operation", {"operation_id": d["op"]})
                print(f"{d['op']:40} {st.get('status', st.get('state','?')):12} {d['note'][:50]}")
            except Exception as e:
                print(f"{d['op']:40} ERR {str(e)[:60]}")
    elif cmd == "poll":
        print(json.dumps(call("get_operation", {"operation_id": sys.argv[2]}), indent=1)[:2000])
    elif cmd == "result":
        print(json.dumps(call("get_operation_result", {"operation_id": sys.argv[2]}), indent=1)[:6000])
