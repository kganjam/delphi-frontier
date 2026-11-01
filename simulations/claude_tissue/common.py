"""Shared helpers: hashing, receipts, status file. Simulated results only."""
import hashlib, json, os, subprocess, sys, time, pathlib, platform
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATUS = pathlib.Path("/data/artifacts/delphi-evolve-rethink/messages/claude-tissue-status.md")

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def env_info():
    return {"python": platform.python_version(), "numpy": np.__version__,
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS")}

def write_receipt(out_dir, name, command, seed, inputs, outputs, t0, exit_code=0, extra=None):
    out_dir = pathlib.Path(out_dir)
    rec = {
        "name": name, "command": command, "exit_code": exit_code, "seed": seed,
        "wall_s": round(time.time() - t0, 3),
        "code_sha256": {str(p): sha(ROOT / p) for p in [pathlib.Path(sys.argv[0]).resolve().relative_to(ROOT), pathlib.Path("simulations/claude_tissue/common.py")]},
        "input_sha256": {str(p): sha(ROOT / p) for p in inputs},
        "output_sha256": {str(p.relative_to(ROOT)): sha(p) for p in map(pathlib.Path, outputs)},
        "environment": env_info(),
        "resource_cap": "systemd-run --user --scope TasksMax=256 MemoryMax=4G MemorySwapMax=0 RuntimeMaxSec=600; OMP_NUM_THREADS=1",
        "evidence_kind": "simulated; not observed",
        "gpu": "none used (CPU numpy); no Nebius job started",
    }
    if extra: rec.update(extra)
    p = out_dir / f"receipt-{name}.json"
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return rec

def update_status(lines):
    """Atomic .tmp+mv status write. lines: markdown string body."""
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    br = subprocess.run(["git", "-C", str(ROOT), "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    now = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    tmp = STATUS.with_suffix(".tmp")
    tmp.write_text(f"# claude-tissue status\n\nUTC {now}\nbranch {br} commit {head}\n\n{lines}\n")
    os.replace(tmp, STATUS)
