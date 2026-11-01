#!/usr/bin/env python3
"""fetch_parts.py <aijob-id> <outdir>: pull job logs, decode every streamed VOXGPU_PART, verify sha256, untar."""
import sys, os, re, subprocess, base64, hashlib, tarfile, io
j, d = sys.argv[1], sys.argv[2]; os.makedirs(d, exist_ok=True)
log = subprocess.run([os.path.expanduser("~/.nebius/bin/nebius"), "--profile", "hackathon", "ai", "job", "logs", j, "--since", "12h", "--tail", "1000"],
                     capture_output=True, text=True).stdout
lp = os.path.join(d, "job.log")
if not os.path.exists(lp) or len(log) >= os.path.getsize(lp):
    open(lp, "w").write(log)   # never replace a longer earlier copy (provider truncates logs after cancel)
else:
    open(lp + ".short", "w").write(log)
L = [re.sub(r"^\[[^\]]*\] ", "", l) for l in log.splitlines()]
i = 0; got = []
while i < len(L):
    m = re.match(r"VOXGPU_PART_BEGIN (\S+) sha256=(\w+)", L[i])
    if m:
        name, want = m.groups(); k = i + 1; buf = []
        while k < len(L) and not L[k].startswith("VOXGPU_PART_END"):
            buf.append(L[k]); k += 1
        blob = base64.b64decode("".join(buf)); ok = hashlib.sha256(blob).hexdigest() == want
        if ok:
            tarfile.open(fileobj=io.BytesIO(blob)).extractall(os.path.join(d, "parts"))
        got.append((name, len(blob), ok)); i = k
    i += 1
for g in got: print("PART", *g)
print("\n".join(l for l in L if l.startswith("BATCH")))
