set -o pipefail
mkdir -p /work/repo && cd /work/repo && python3 -c "import base64,io,tarfile; tarfile.open(fileobj=io.BytesIO(base64.b64decode(open('/work/bundle.b64').read())),mode='r:xz').extractall('/work/repo',filter='data')" || { echo "NEURO-DONE none 0 97"; exit 97; }
echo "NEURO-BUNDLE $(base64 -d /work/bundle.b64 | sha256sum | cut -c1-64)"
echo "NEURO-START $(date -u +%FT%TZ) $(nproc) cpus"
pip install --no-cache-dir -q scipy > /work/pip.log 2>&1 || { echo NEURO-PIP-FAIL; tail -5 /work/pip.log; }
mkdir -p /work/out
( python -V; nvidia-smi --query-gpu=name,memory.total --format=csv; OMP_NUM_THREADS=1 python -m engineering.neuro.m3_atlas --out /work/out --geometry /work/repo/geometry.json --reference /work/repo/reference.json --n-mc 4096 --procs 16 --seed 20261102 --grid '{"DIH":[0,1,2,3,4,5,6,7],"KV":[0.1,0.125,0.15,0.175,0.2,0.25],"MASS":[0.025,0.03,0.035],"SM":[0.04,0.08,0.12],"TC":[0.01,0.02,0.03],"TV":[0.03,0.06,0.09],"GUST":[1.0,2.0,3.0],"LIN_TC":[0.01,0.02,0.03,0.05],"LIN_TV":[0.03,0.06,0.09,0.12]}' ) > /work/out/stdout.log 2> /work/out/stderr.log; rc=$?
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
