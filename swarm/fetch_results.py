#!/usr/bin/env python3
"""Pull a finished Nebius run's output files onto disk, and verify them.

Written because three ESMFold2 runs SUCCEEDED on 2026-11-03 and their structures were still not in
the repository a day later. A completed operation and a fetched result look identical from the
operation log -- `ops` printed SUCCEEDED for all three -- and only `find results -name '*.cif'`
showed that nothing had been written. That is this project's recurring shape: the mechanism ran and
nobody counted its output.

Two things make this harder than a GET:
  * every download URL is presigned and expires in 60 SECONDS, so resolve-and-fetch must happen in
    one process; a human round trip between the two always fails.
  * the run result does not carry file artifact ids. It carries an OUTPUT MANIFEST artifact, which
    must itself be downloaded and parsed to learn them.

Every file is checked against the sha256 the manifest declares. A download that silently truncates
and a download that worked are the same bytes-on-disk to anything that does not hash them.
"""
from __future__ import annotations

import hashlib
import json
import os
import ssl
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "library", "tools"))
import nbx  # noqa: E402

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def _get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, method="GET"), context=CTX, timeout=300) as r:
        return r.read()


def fetch_artifact(artifact_id: str, expect_sha: str | None = None) -> bytes:
    """Resolve a presigned handle and spend it immediately. Returns the bytes, verified."""
    h = nbx.call("download_scientific_artifact", {"artifact_id": artifact_id})
    if "handle" not in h:
        raise RuntimeError(f"no handle for {artifact_id}: {json.dumps(h)[:300]}")
    raw = _get(h["handle"]["url"])
    got = hashlib.sha256(raw).hexdigest()
    declared = expect_sha or h.get("artifact", {}).get("sha256")
    if declared and got != declared:
        raise RuntimeError(f"sha256 mismatch for {artifact_id}: got {got[:16]} want {declared[:16]}")
    return raw


EXT = {"chemical/x-mmcif": ".cif", "application/json": ".json",
       "text/plain": ".txt", "application/x-tar": ".tar"}


def status_of(res: dict) -> str:
    """Read the status out of whichever shape this operation uses.

    FOUR shapes are live on this endpoint, and the fourth cost three finished runs a day of
    invisibility. The scientific-batch tools put it at the top level as `status` or
    `terminal_status`; the async/native tools (proteinmpnn, msa-search, openfold3) nest it under
    `operation.status` and otherwise report completion only through `result_available` and
    `progress.steps[].state`. A reader that knows three of the four prints "?" for the fourth --
    and an operation that reads "?" looks exactly like one that failed, so nobody fetches it.
    """
    for v in (res.get("terminal_status"), res.get("status"),
              (res.get("operation") or {}).get("status"), res.get("state")):
        if v:
            return str(v).lower()
    if res.get("result_available") is True:
        return "succeeded"
    return ""


def _write(path: str, raw: bytes) -> None:
    """Write, refusing to destroy a different file that is already there.

    Two jobs sharing an `outdir` used to overwrite each other in silence: the direct-artifact
    branch names every file `result.<ext>`, and the manifest branch reuses the manifest's own
    entry names, which repeat across two runs of the same tool. The loss is invisible -- the
    second job reports success and the first job's result is simply gone, which reads afterwards
    as a job that was never submitted. Measured 2026-11-05 on two ProteinMPNN runs into
    results/nebius/slc12a7a; the first was renamed by hand with two minutes to spare.
    Re-fetching the SAME bytes is fine and stays idempotent.
    """
    if os.path.exists(path) and open(path, "rb").read() != raw:
        raise RuntimeError(
            f"{path} already exists with different contents -- refusing to overwrite. "
            f"Pass a distinct `stem` (or outdir) per job; two jobs are writing the same name.")
    with open(path, "wb") as f:
        f.write(raw)


def fetch_run(op_id: str, outdir: str, stem: str | None = None) -> list[tuple[str, str, int]]:
    """Fetch every output file of a finished run. Returns (name, path, bytes) per file.

    `stem` prefixes every filename, so several jobs can share one `outdir` without colliding.
    """
    res = nbx.call("get_operation_result", {"operation_id": op_id})
    status = status_of(res)
    if status not in ("succeeded", "success", "completed"):
        raise RuntimeError(f"{op_id} is {status or 'unknown'}, not succeeded -- nothing to fetch")

    os.makedirs(outdir, exist_ok=True)

    # Shape B: a single direct result artifact, no manifest (the async/native tools).
    direct = (res.get("result") or {}).get("artifact") or {}
    if direct.get("artifact_id") and not (res.get("output_manifest") or {}).get("artifact_id"):
        raw = fetch_artifact(direct["artifact_id"], direct.get("sha256"))
        base = stem or "result"
        path = os.path.join(outdir, f"{base}{EXT.get(direct.get('media_type'), '.bin')}")
        _write(path, raw)
        return [(base, path, len(raw))]

    om = res.get("output_manifest") or {}
    if not om.get("artifact_id"):
        raise RuntimeError(f"{op_id} succeeded but carries neither an output manifest nor a "
                           f"direct result artifact; top-level keys were {sorted(res.keys())}")
    manifest = json.loads(fetch_artifact(om["artifact_id"], om.get("sha256")))

    written = []
    for entry in manifest.get("artifacts", []) or manifest.get("entries", []):
        art = entry.get("artifact") or {}
        aid = art.get("artifact_id")
        if not aid:
            continue
        raw = fetch_artifact(aid, art.get("sha256"))
        name = entry.get("name", aid)
        ext = EXT.get(art.get("media_type"), ".bin")
        path = os.path.join(outdir, f"{stem}_{name}{ext}" if stem else f"{name}{ext}")
        _write(path, raw)
        written.append((name, path, len(raw)))
    # A run that reports success and yields no files is the empty-set failure, not a success.
    if not written:
        raise RuntimeError(f"{op_id}: manifest parsed but produced NO files -- "
                           f"keys were {sorted(manifest.keys())}")
    return written


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: fetch_results.py <operation_id> <outdir>", file=sys.stderr)
        return 2
    op, outdir = sys.argv[1], sys.argv[2]
    try:
        for name, path, n in fetch_run(op, outdir):
            print(f"  {name:28} -> {path}  ({n:,} bytes, sha256 verified)")
    except Exception as e:
        print(f"  {op}: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
