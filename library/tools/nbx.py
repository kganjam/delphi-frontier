#!/usr/bin/env python3
"""Nebius Scientific AI workbench client: upload artifacts, submit runs, poll operations.

Written because the submit path is four round trips (reserve -> PUT -> finalize -> submit) with a
60-second presigned URL in the middle, and doing that by hand once per job is how a step gets skipped.
The key is read from the environment and never printed; every response is returned whole so the caller
can read the server's own error text rather than a paraphrase of it.
"""
import hashlib, json, os, ssl, sys, time, urllib.request

MCP = "https://89.169.99.188/mcp"
KEY = os.environ.get("NEBIUS_API_KEY", "")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE          # the cert does not validate for a bare IP; documented in memory


def _post(url, data, headers, method="POST"):
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, context=CTX, timeout=300) as r:
        return r.status, r.read()


def call(tool, args):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args}}).encode()
    st, raw = _post(MCP, body, {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
                                "Accept": "application/json, text/event-stream"})
    d = json.loads(raw)
    if "error" in d:                      # transport-level error
        return {"_transport_error": d["error"]}
    txt = d["result"]["content"][0]["text"]
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return {"_text": txt}


def upload(path_or_bytes, media_type, model_id):
    """Reserve, transfer, finalize. Returns the artifact reference a manifest or a run request needs."""
    raw = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    sha, size = hashlib.sha256(raw).hexdigest(), len(raw)
    res = call("begin_scientific_artifact_upload",
               {"model_id": model_id, "sha256": sha, "size_bytes": size, "media_type": media_type})
    if "upload_url" not in res:
        return {"_failed_at": "begin", "response": res}
    st, _ = _post(res["upload_url"], raw,
                  {"Authorization": f"Bearer {KEY}", "Content-Type": media_type}, method="PUT")
    if st != 200:
        return {"_failed_at": "transfer", "http": st}
    fin = call("finalize_scientific_artifact_upload", {"upload_id": res["upload_id"]})
    if fin.get("state") != "finalized":
        return {"_failed_at": "finalize", "response": fin}
    return fin["artifact"]


TERMINAL = {"SUCCEEDED", "SUCCESS", "COMPLETED", "FAILED", "CANCELLED", "CANCELED", "EXPIRED", "ERROR"}


def op_status(resp):
    """The operation's status, preferring the field with the explicit vocabulary.

    Both `status` and `state` exist at the top level and they do NOT agree: a wedged operation reads
    status='ADMISSION_PENDING' but state='admission-unknown'. Some responses also nest a copy under
    `operation`. Prefer `status`, fall back to the nested copy, then to `state`.
    """
    if not isinstance(resp, dict):
        return ""
    inner = resp.get("operation") if isinstance(resp.get("operation"), dict) else {}
    return str(resp.get("status") or inner.get("status") or resp.get("state") or "").upper()


def is_terminal(resp):
    """True only for a status we KNOW means finished.

    This pins the positive fact instead of listing the bad ones. The previous version asked whether
    the status contained none of RUN/PEND/QUEUE/PROGRESS, and 'admission-unknown' contains none of
    them -- so a permanently wedged operation was reported as finished. A blocklist cannot see a
    state nobody thought of; an allowlist fails safe by continuing to poll.
    """
    return op_status(resp).replace("-", "_") in TERMINAL


def poll(op_id, every=20, limit=90):
    """Poll until the status is one we know to be terminal. Returns the last response seen."""
    last = None
    for _ in range(limit):
        last = call("get_operation", {"operation_id": op_id})
        st = op_status(last)
        print(f"  [{time.strftime('%H:%M:%S')}] {st or json.dumps(last)[:120]}", flush=True)
        if is_terminal(last):
            return last
        time.sleep(every)
    return last


if __name__ == "__main__":
    if sys.argv[1] == "call":
        print(json.dumps(call(sys.argv[2], json.loads(sys.argv[3])), indent=1)[:4000])
    elif sys.argv[1] == "upload":
        print(json.dumps(upload(sys.argv[2], sys.argv[3], sys.argv[4]), indent=1))
    elif sys.argv[1] == "poll":
        print(json.dumps(poll(sys.argv[2]), indent=1)[:3000])
