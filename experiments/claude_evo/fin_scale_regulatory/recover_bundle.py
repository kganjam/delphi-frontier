"""Recover the EVOFS_B64 bundle from a Nebius job log into a directory.

Collects every line containing the marker, in log order, regardless of
BEGIN/END — a lost BEGIN must not silently drop the payload. `set -x` trace
and sha256sum output interleave in the same stream, hence the substring find.
"""
import base64, gzip, io, sys, tarfile, os
log, outdir = sys.argv[1], sys.argv[2]
M = "EVOFS_B64 "
blob = []
for line in open(log, errors="replace"):
    i = line.find(M)
    if i >= 0:
        blob.append(line[i + len(M):].strip())
if not blob:
    sys.exit("no EVOFS_B64 lines found")
raw = gzip.decompress(base64.b64decode("".join(blob)))
os.makedirs(outdir, exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
    names = tf.getnames()
    tf.extractall(outdir, filter="data")
print(f"recovered {len(blob)} chunks, {len(raw)} bytes tar -> {outdir}")
for n in sorted(names):
    print("  ", n)
