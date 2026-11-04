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


def fetch_run(op_id: str, outdir: str) -> list[tuple[str, str, int]]:
    """Fetch every output file of a finished run. Returns (name, path, bytes) per file."""
    res = nbx.call("get_operation_result", {"operation_id": op_id})
    status = (res.get("terminal_status") or res.get("status") or "").lower()
    if status != "succeeded":
        raise RuntimeError(f"{op_id} is {status or 'unknown'}, not succeeded -- nothing to fetch")

    om = res.get("output_manifest") or {}
    if not om.get("artifact_id"):
        raise RuntimeError(f"{op_id} succeeded but carries no output manifest")
    manifest = json.loads(fetch_artifact(om["artifact_id"], om.get("sha256")))

    os.makedirs(outdir, exist_ok=True)
    written = []
    for entry in manifest.get("artifacts", []) or manifest.get("entries", []):
        art = entry.get("artifact") or {}
        aid = art.get("artifact_id")
        if not aid:
            continue
        raw = fetch_artifact(aid, art.get("sha256"))
        name = entry.get("name", aid)
        ext = {"chemical/x-mmcif": ".cif", "application/json": ".json"}.get(art.get("media_type"), ".bin")
        path = os.path.join(outdir, f"{name}{ext}")
        with open(path, "wb") as f:
            f.write(raw)
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
