#!/usr/bin/env python3
"""fetch_parts.py <aijob-id> <outdir>: pull the job log, decode every XM_PART, verify its sha256, untar.
Adapted from the voxgpu harness's fetch_parts.py (same log-transport pattern)."""
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile

j, d = sys.argv[1], sys.argv[2]
os.makedirs(d, exist_ok=True)
log = subprocess.run([os.path.expanduser("~/.nebius/bin/nebius"), "--profile", "hackathon", "ai", "job", "logs", j],
                     capture_output=True, text=True).stdout
open(os.path.join(d, "job.log.txt"), "w").write(log)
L = [re.sub(r"^\[[^\]]*\] ", "", ln) for ln in log.splitlines()]
got = []
i = 0
while i < len(L):
    m = re.match(r"XM_PART_BEGIN (\S+) sha256=(\w+) bytes=(\d+)", L[i])
    if m:
        name, want, nbytes = m.group(1), m.group(2), int(m.group(3))
        k = i + 1
        buf = []
        while k < len(L) and not L[k].startswith("XM_PART_END"):
            buf.append(L[k].strip())
            k += 1
        try:
            blob = base64.b64decode("".join(buf))
        except Exception as e:  # noqa: BLE001
            blob = b""
        ok = hashlib.sha256(blob).hexdigest() == want and len(blob) == nbytes
        if ok:
            tarfile.open(fileobj=io.BytesIO(blob)).extractall(os.path.join(d, "parts"), filter="data")
        got.append({"part": name, "bytes": len(blob), "declared_bytes": nbytes, "sha256": want, "sha_ok": ok})
        i = k
    i += 1
status = [ln for ln in L if ln.startswith(("XM_RUN_DONE", "XM_SWEEP_DONE", "XM_ALL_DONE", "XM_START", "XM_BINARY", "XM_INPUT", "XM_BUNDLE", "XM_PY"))]
json.dump({"job": j, "parts": got, "status_lines": status}, open(os.path.join(d, "fetch_receipt.json"), "w"), indent=1)
for g in got:
    print("PART", g["part"], g["bytes"], "ok" if g["sha_ok"] else "SHA_FAIL")
print("\n".join(status))
