set -o pipefail
mkdir -p /work/repo && cd /work/repo && python3 -c "import base64,io,tarfile; tarfile.open(fileobj=io.BytesIO(base64.b64decode(open('/work/bundle.b64').read())),mode='r:xz').extractall('/work/repo',filter='data')" || { echo "NEURO-DONE none 0 97"; exit 97; }
echo "NEURO-BUNDLE $(base64 -d /work/bundle.b64 | sha256sum | cut -c1-64)"
echo "NEURO-START $(date -u +%FT%TZ) $(nproc) cpus"
pip install --no-cache-dir -q scipy > /work/pip.log 2>&1 || { echo NEURO-PIP-FAIL; tail -5 /work/pip.log; }
mkdir -p /work/out
( python -V; nvidia-smi --query-gpu=name,memory.total --format=csv; OMP_NUM_THREADS=1 python -m engineering.neuro.sobol_m3 --out /work/out --N 2048 --trials 128 --procs 16 --geometry /work/repo/geometry.json --seed 20261101 ) > /work/out/stdout.log 2> /work/out/stderr.log; rc=$?
echo "NEURO-RC $rc $(date -u +%FT%TZ)"; tail -c 2000 /work/out/stdout.log; tail -c 2000 /work/out/stderr.log
python3 - "$rc" <<'PY'
import base64, hashlib, io, sys, tarfile
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as t:
    t.add("/work/out", arcname="out")
b = buf.getvalue(); e = base64.b64encode(b).decode(); W = 16000   # provider splits lines at 16384 chars and keeps the last 100 lines
ch = [e[i:i + W] for i in range(0, len(e), W)]
if len(ch) > 95:
    print(f"NEURO-TOO-BIG {len(b)} bytes needs {len(ch)} chunks > 95; output not transportable via logs", flush=True); print(f"NEURO-DONE {hashlib.sha256(b).hexdigest()} {len(b)} 98", flush=True); sys.exit(0)
for i, c in enumerate(ch):
    print(f"NEURO-CHUNK {i} {len(ch)} {hashlib.sha256(c.encode()).hexdigest()[:16]} {c}", flush=True)
print(f"NEURO-DONE {hashlib.sha256(b).hexdigest()} {len(b)} {sys.argv[1]}", flush=True)
PY
