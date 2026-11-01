"""Submit and collect claude-neuro Nebius AI jobs (CPU or GPU). Only jobs named claude-neuro-* and recorded in jobs.jsonl are touched.

    python -m engineering.neuro.nebius_job submit <spec.json>     # spec: name, platform, preset, timeout, files, command, image
    python -m engineering.neuro.nebius_job status
    python -m engineering.neuro.nebius_job collect <name> <dest_dir>

Transport: the container prints its output tar.gz as base64 lines "NEURO-CHUNK <i> <n> <sha256(chunk)> <data>" and a final
"NEURO-DONE <sha256(tar)> <bytes> <rc>". The collector rebuilds the archive from the job logs, checks every chunk hash and the
archive hash, and refuses an incomplete or corrupt stream. The token is read from ~/.nebius/token at each call, never printed.
"""
from __future__ import annotations
import base64, hashlib, io, json, os, subprocess, sys, tarfile, time
from pathlib import Path

from engineering.neuro import common as C

NEB = os.path.expanduser("~/.nebius/bin/nebius")
LEDGER = C.OUT / "jobs" / "jobs.jsonl"
SUBNET = "vpcsubnet-e00tc2metkvjckkqqp"
PREFIX = "claude-neuro-"
RUNNER = r'''set -o pipefail
mkdir -p /work/repo && cd /work/repo && python3 -c "import base64,io,tarfile; tarfile.open(fileobj=io.BytesIO(base64.b64decode(open('/work/bundle.b64').read())),mode='r:xz').extractall('/work/repo',filter='data')" || { echo "NEURO-DONE none 0 97"; exit 97; }
echo "NEURO-BUNDLE $(base64 -d /work/bundle.b64 | sha256sum | cut -c1-64)"
echo "NEURO-START $(date -u +%FT%TZ) $(nproc) cpus"
pip install --no-cache-dir -q __PIP__ > /work/pip.log 2>&1 || { echo NEURO-PIP-FAIL; tail -5 /work/pip.log; }
mkdir -p /work/out
( __COMMAND__ ) > /work/out/stdout.log 2> /work/out/stderr.log; rc=$?
echo "NEURO-RC $rc $(date -u +%FT%TZ)"; tail -c 2000 /work/out/stdout.log; tail -c 2000 /work/out/stderr.log
python3 - "$rc" <<'PY'
import base64, hashlib, io, sys, tarfile
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as t:
    t.add("/work/out", arcname="out")
b = buf.getvalue(); e = base64.b64encode(b).decode(); W = 3000
ch = [e[i:i + W] for i in range(0, len(e), W)]
for i, c in enumerate(ch):
    print(f"NEURO-CHUNK {i} {len(ch)} {hashlib.sha256(c.encode()).hexdigest()[:16]} {c}", flush=True)
print(f"NEURO-DONE {hashlib.sha256(b).hexdigest()} {len(b)} {sys.argv[1]}", flush=True)
PY
'''


def neb(*args, capture=True):
    env = dict(os.environ, NEBIUS_IAM_TOKEN=Path(os.path.expanduser("~/.nebius/token")).read_text().strip())
    return subprocess.run([NEB, "--profile", "hackathon", *args], capture_output=capture, text=True, env=env, cwd="/tmp")


def ledger():
    return [json.loads(l) for l in LEDGER.read_text().splitlines()] if LEDGER.exists() else []


def submit(spec_path):
    spec = json.loads(Path(spec_path).read_text()); name = spec["name"]
    assert name.startswith(PREFIX), "job names must start with " + PREFIX
    active = [j for j in status(quiet=True) if j["state"] not in ("COMPLETED", "FAILED", "CANCELLED", "ERROR")]
    if len(active) >= 2:
        raise SystemExit(f"refusing: {len(active)} claude-neuro jobs already active (cap 2)")
    stage = C.OUT / "jobs" / name / "stage"; stage.mkdir(parents=True, exist_ok=True)
    runner = stage / "run.sh"; runner.write_text(RUNNER.replace("__COMMAND__", spec["command"]).replace("__PIP__", spec.get("pip", "numpy==2.4.4 scipy==1.17.1")))
    pins, buf = {}, io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:xz", format=tarfile.PAX_FORMAT, preset=9) as t:      # deterministic: sorted, fixed mtime/owner
        for rel, src in sorted(spec["files"].items()):
            p = C.ROOT / src; data = p.read_bytes(); ti = tarfile.TarInfo(rel); ti.size = len(data); ti.mtime = 0; ti.mode = 0o644
            t.addfile(ti, io.BytesIO(data)); pins[rel] = {"source": src, "sha256": C.sha(p), "bytes": len(data)}
    bundle = stage / "bundle.b64"; raw = buf.getvalue(); bundle.write_text(base64.b64encode(raw).decode())
    assert bundle.stat().st_size + runner.stat().st_size <= 44 * 1024, "bundle + runner exceed the ~44 KiB budget (provider limit 65536 bytes after encoding)"
    inj = [f"{runner}:/work/run.sh", f"{bundle}:/work/bundle.b64"]
    args = ["ai", "job", "create", "--name", name, "--image", spec["image"], "--container-command", "bash", "--args", "/work/run.sh",
            "--platform", spec["platform"], "--preset", spec["preset"], "--timeout", spec["timeout"], "--disk-size", spec.get("disk", "50Gi"),
            "--subnet-id", SUBNET, "--async", "--format", "json"]
    for i in inj:
        args += ["--inject-file", i]
    r = neb(*args)
    rec = {"name": name, "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "spec": {k: v for k, v in spec.items() if k != "files"},
           "injected": pins, "runner_sha256": C.sha(runner), "bundle_tar_xz_sha256": hashlib.sha256(raw).hexdigest(), "bundle_b64_bytes": bundle.stat().st_size, "cli_rc": r.returncode, "git_head": C.git_head()}
    try:
        rec["job_id"] = json.loads(r.stdout).get("metadata", {}).get("id") or json.loads(r.stdout).get("resource_id")
    except Exception:
        rec["job_id"] = None; rec["cli_stderr_tail"] = r.stderr[-800:]
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({k: rec[k] for k in ("name", "job_id", "cli_rc")} | ({"stderr": r.stderr[-600:]} if r.returncode else {})))
    return r.returncode


def status(quiet=False):
    r = neb("ai", "job", "list", "--format", "json")
    mine = {j["name"]: j for j in ledger() if j.get("job_id")}
    out = []
    for it in json.loads(r.stdout).get("items", []):
        n = it["metadata"]["name"]
        if n in mine and it["metadata"]["id"] == mine[n].get("job_id", it["metadata"]["id"]):
            out.append({"name": n, "id": it["metadata"]["id"], "state": it["status"].get("state"), "updated": it["metadata"].get("updated_at")})
    if not quiet:
        print(json.dumps(out, indent=1))
    return out


def collect(name, dest):
    rec = [j for j in ledger() if j["name"] == name and j.get("job_id")][-1]       # latest submission that created a job
    r = neb("ai", "job", "logs", rec["job_id"])
    lines = r.stdout.splitlines()
    chunks, done, rc_line = {}, None, None
    for l in lines:
        l = l.split("NEURO-", 1)
        if len(l) < 2:
            continue
        f = ("NEURO-" + l[1]).split(" ")
        if f[0] == "NEURO-CHUNK":
            i, n, h, data = int(f[1]), int(f[2]), f[3], f[4]
            if hashlib.sha256(data.encode()).hexdigest()[:16] != h:
                raise SystemExit(f"chunk {i} hash mismatch")
            chunks[i] = (n, data)
        elif f[0] == "NEURO-DONE":
            done = (f[1], int(f[2]), int(f[3]))
        elif f[0] == "NEURO-RC":
            rc_line = " ".join(f)
    if not done:
        raise SystemExit("no NEURO-DONE line: incomplete stream (job still running, failed, or logs truncated)")
    n = next(iter(chunks.values()))[0]
    missing = [i for i in range(n) if i not in chunks]
    if missing:
        raise SystemExit(f"missing chunks {missing[:10]} of {n}")
    b = base64.b64decode("".join(chunks[i][1] for i in range(n)))
    if hashlib.sha256(b).hexdigest() != done[0] or len(b) != done[1]:
        raise SystemExit("archive hash/size mismatch")
    dest = Path(dest); dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(b), mode="r:gz") as t:
        for m in t.getmembers():
            if m.name.startswith("/") or ".." in m.name or not (m.isfile() or m.isdir()):
                raise SystemExit("unsafe archive member " + m.name)
        t.extractall(dest, filter="data")
    files = {str(p.relative_to(dest)): {"sha256": C.sha(p), "bytes": p.stat().st_size} for p in sorted(dest.rglob("*")) if p.is_file()}
    receipt = {"name": name, "job_id": rec["job_id"], "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "archive_sha256": done[0],
               "archive_bytes": done[1], "container_rc": done[2], "rc_line": rc_line, "chunks": n, "files": files, "submission": rec}
    (dest / "collection_receipt.json").write_text(json.dumps(receipt, indent=1))
    print(json.dumps({"name": name, "container_rc": done[2], "files": len(files), "archive_sha256": done[0][:16]}))
    return 0 if done[2] == 0 else done[2]


if __name__ == "__main__":
    cmd = sys.argv[1]
    sys.exit(submit(sys.argv[2]) if cmd == "submit" else (status() and 0) if cmd == "status" else collect(sys.argv[2], sys.argv[3]))
