#!/bin/bash
# fetch_return.sh <aijob-id> <outdir>: pull job logs, decode the base64 return archive, verify its sha256.
set -eu
J=$1; D=$2; mkdir -p $D
~/.nebius/bin/nebius --profile hackathon ai job logs $J --since 12h --tail 1000 > $D/job.log 2>&1 || true
python3 - "$D" <<'PY'
import sys, re, base64, hashlib, os
d = sys.argv[1]; L = open(os.path.join(d, "job.log"), errors="replace").read().splitlines()
strip = lambda l: re.sub(r"^\[[^\]]*\] ", "", l)
L = [strip(l) for l in L]
try:
    i = L.index("VOXGPU_B64_BEGIN"); j = L.index("VOXGPU_B64_END")
except ValueError:
    print("NO_RETURN_MARKERS"); sys.exit(2)
blob = base64.b64decode("".join(L[i+1:j]))
want = [l for l in L if "RETURN bytes=" in l]
sha = hashlib.sha256(blob).hexdigest()
open(os.path.join(d, "ret.tgz"), "wb").write(blob)
print("decoded", len(blob), "sha256", sha, "| job said:", [w.split("RETURN ")[1] for w in want])
PY
mkdir -p $D/ret && tar xzf $D/ret.tgz -C $D/ret && ls $D/ret
