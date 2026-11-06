#!/usr/bin/env python3
"""Nebius Scientific AI workbench client: upload artifacts, submit runs, poll operations.

Written because the submit path is four round trips (reserve -> PUT -> finalize -> submit) with a
60-second presigned URL in the middle, and doing that by hand once per job is how a step gets skipped.
The key is read from the environment and never printed; every response is returned whole so the caller
can read the server's own error text rather than a paraphrase of it.
"""
import hashlib, json, os, ssl, sys, time, urllib.request

MCP = "https://89.169.99.188/mcp"
KEYFILE = os.path.expanduser("~/.config/morphoswarm/nebius.env")


def _key() -> str:
    """The environment first, then the key file `swarm/nebius.py` has always used.

    THESE TWO MODULES AUTHENTICATED DIFFERENTLY AND IT FAILED SILENTLY (measured 2026-11-05).
    `nebius.py` reads the key from KEYFILE; this module read it only from the environment. A
    background run that polled with one and fetched with the other therefore saw a job reach
    SUCCEEDED and then got `HTTP Error 401: Unauthorized` fetching it ONE SECOND LATER, which
    reads as an expired token or a server fault rather than as an empty `Authorization: Bearer `
    header. Three queued submits died the same way. Falling back to the file makes the two
    agree; an empty key now raises here instead of producing a 401 four round trips later.
    """
    k = os.environ.get("NEBIUS_API_KEY", "").strip()
    if k:
        return k
    try:
        for line in open(KEYFILE):
            if line.startswith("NEBIUS_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    raise RuntimeError(f"no NEBIUS_API_KEY in the environment and none in {KEYFILE}")


KEY = ""        # resolved lazily by _key(); kept so existing `nbx.KEY` readers still import
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
    st, raw = _post(MCP, body, {"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
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
                  {"Authorization": f"Bearer {_key()}", "Content-Type": media_type}, method="PUT")
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


def op_id(resp):
    """The operation id from a submit response, wherever this server chose to put it.

    THREE SPELLINGS, ALL MEASURED IN ONE SESSION (2026-11-05), and a caller that knows only one
    reads a successful submit as a failure:

        msa_search_native      result.operation.id            -> op-cae0d4dc9544f2c0
        boltz2_predict_native  result.operation.id            -> op-a31030f2eb4a938d
        submit_esmfold2        result.operation.operation_id  -> op-cdf4e821a1c34145
                               (and the same id again at result.operation_id and result.id)

    Each of those submits SUCCEEDED. Each was reported by the caller as "NO OP" because its
    extractor looked in one place. That is the expensive shape: the job is queued and burning the
    single in-flight slot while the caller believes nothing was submitted and retries with a new
    idempotency key, stranding the first.
    """
    if not isinstance(resp, dict):
        return None
    r = resp.get("result", resp)
    inner = r.get("operation") if isinstance(r.get("operation"), dict) else {}
    for src in (inner, r, resp):
        for k in ("operation_id", "id"):
            v = src.get(k) if isinstance(src, dict) else None
            if isinstance(v, str) and v.startswith("op-"):
                return v
    return None


def has_payload(obj, key):
    """True only when `obj[key]` is a LIST OF DICTS, i.e. a real result payload.

    WHY NOT `key in json.dumps(obj)`. That substring test is what a caller reaches for, and it
    matched the PROGRESS object for a finished boltz2 run, because progress reports a step whose
    `step_id` is literally "structures". The caller then wrote the progress blob out as a
    structure and raised KeyError on it. A pattern that matches its own description is this
    repository's §6b, arriving through a JSON blob instead of a grep.
    """
    v = obj.get(key) if isinstance(obj, dict) else None
    return isinstance(v, list) and bool(v) and isinstance(v[0], dict)


def fetch_result(operation, verify=True):
    """Download a finished operation's result artifact and return (parsed_json, raw_bytes).

    THE RESULT IS NOT INLINE. `get_operation_result` returns an `operation-artifact-result/v1`
    envelope holding only an artifact ref; the bytes come from a SECOND call,
    `download_scientific_artifact`, whose presigned URL is at `handle.url` -- not `download_url`,
    which is the name every caller guesses first and which is absent.

    That URL is S3-presigned, **expires in 60 seconds**, and its signature covers `host` only, so
    it takes NO headers -- adding an Authorization or Content-Type header invalidates it. Both
    calls therefore have to happen in one process, close together; a human round trip between
    them always fails.

    `verify` checks the downloaded bytes against the sha256 the server declared. Leave it on: it
    is the only evidence that what arrived is what the run produced, and it costs one hash.
    """
    rr = call("get_operation_result", {"operation_id": operation})
    rr = rr.get("result", rr)
    ref = rr.get("artifact")
    if not ref:
        raise RuntimeError(f"no artifact in operation result: {json.dumps(rr)[:300]}")
    d = call("download_scientific_artifact", {"artifact_id": ref["artifact_id"]})
    d = d.get("result", d)
    url = (d.get("handle") or {}).get("url")
    if not url:
        raise RuntimeError(f"no handle.url in download response: {json.dumps(d)[:300]}")
    raw = urllib.request.urlopen(urllib.request.Request(url), context=CTX, timeout=300).read()
    if verify:
        got = hashlib.sha256(raw).hexdigest()
        if got != ref["sha256"]:
            raise RuntimeError(f"sha256 mismatch: declared {ref['sha256']}, got {got}")
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError:
        return None, raw


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
