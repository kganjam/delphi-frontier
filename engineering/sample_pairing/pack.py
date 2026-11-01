"""Build the portable READY packet: a deterministic tar.gz of the audit code + frozen protocol, a per-member sha256/size
manifest, the exact source commit, entry argv and the offline preflight command. Refuses uncommitted or drifted members."""
import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMBERS = ["engineering/__init__.py", "engineering/sample_pairing/__init__.py", "engineering/sample_pairing/audit.py",
           "engineering/sample_pairing/controls.py", "engineering/sample_pairing/protocol.json"]
OUT = os.path.join(ROOT, "artifacts", "sample-pairing")


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a]).decode().strip()


def build(out=OUT):
    commit = git("rev-parse", "HEAD")
    members = []
    for m in MEMBERS:
        disk = open(os.path.join(ROOT, m), "rb").read()
        try:
            committed = subprocess.check_output(["git", "-C", ROOT, "show", f"{commit}:{m}"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise SystemExit(f"{m} is not in HEAD {commit[:10]}: commit it first") from None
        if disk != committed:
            raise SystemExit(f"{m} differs from HEAD {commit[:10]}: commit it first")
        members.append((m, disk))
    os.makedirs(out, exist_ok=True)
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz, tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for name, data in members:
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime, ti.mode, ti.uid, ti.gid, ti.uname, ti.gname = len(data), 0, 0o644, 0, 0, "", ""
            tf.addfile(ti, io.BytesIO(data))
    arc = buf.getvalue()
    open(os.path.join(out, "packet.tar.gz"), "wb").write(arc)
    packet = {"schema": "frontier.sample-pairing.packet/1", "source_commit": commit,
              "archive": {"path": "artifacts/sample-pairing/packet.tar.gz", "sha256": hashlib.sha256(arc).hexdigest(), "bytes": len(arc)},
              "members": [{"path": n, "sha256": hashlib.sha256(d).hexdigest(), "bytes": len(d)} for n, d in members],
              "python": ">=3.10", "dependencies": "none (standard library only)",
              "extract": "into a NEW empty directory; run every command with that directory as cwd",
              "preflight_argv": ["python3", "-m", "engineering.sample_pairing.audit", "--preflight"],
              "entry_argv": ["python3", "-m", "engineering.sample_pairing.audit", "--run", "--out", "$COPS_OUT"],
              "contract": {"COPS_OUT": "exact fresh output directory (must not exist)", "workers": 1, "numeric_threads": 1, "memory_bytes": 4294967296,
                           "tasks_max": 128, "hard_runtime_s": 600, "max_output_bytes": 20971520, "network": "metadata only: www.ncbi.nlm.nih.gov, finite URL rule in protocol.json",
                           "retries": "none; no budget expansion in the runner"},
              "outputs": ["results.json", "receipt.json", "raw/*.soft.txt"], "results_schema": "frontier.sample-pairing.results/1",
              "protocol_sha256": hashlib.sha256(dict(members)["engineering/sample_pairing/protocol.json"]).hexdigest()}
    json.dump(packet, open(os.path.join(out, "packet.json"), "w"), indent=1, sort_keys=True)
    return packet


if __name__ == "__main__":
    print(json.dumps(build(), indent=1))
    sys.exit(0)
