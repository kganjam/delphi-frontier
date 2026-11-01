"""Shared receipt / manifest / check helpers for the organ- and organism-scale simulation runs (claude-organ).

Every run: seed, input hashes, command, a bounds check that raises (so the process exits non-zero), and a
manifest whose scope is 'simulated, not observed'.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/organ-sims"
SCOPE = "simulated, not observed"


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def head() -> str:
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()


def manifest(run_id: str, title: str, inputs: list[str], results: dict, checks: list[dict], design: dict, seed=None,
             figures: list[str] = (), extra: dict | None = None) -> dict:
    m = {"schema": "frontier.organ-sim.manifest/1", "id": run_id, "title": title, "evidence_kind": SCOPE,
         "scope": SCOPE, "command": " ".join(sys.argv), "seed": seed, "git_head_at_run": head(),
         "python": platform.python_version(), "ran_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "inputs": {p: {"sha256": sha(ROOT / p), "bytes": (ROOT / p).stat().st_size} for p in inputs},
         "code_sha256": {str(q.relative_to(ROOT)): sha(q) for q in sorted((ROOT / "engineering/organ_sims").glob("*.py"))},
         "git_dirty_paths_at_run": subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "engineering", "artifacts/organ-sims"],
                                                  capture_output=True, text=True).stdout.splitlines()[:50],
         "results": results, "checks": checks, "design_implications": design, "figures": list(figures)}
    if extra:
        m.update(extra)
    d = OUT / run_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps(m, indent=1, default=float) + "\n")
    return m


def enforce(checks: list[dict]):
    """Exit non-zero if any bound check fails (the manifest is already written, failed checks stay recorded)."""
    bad = [c for c in checks if not c["pass"]]
    for c in bad:
        print("CHECK FAILED:", c["name"], c.get("detail", ""), file=sys.stderr)
    if bad:
        raise SystemExit(3)
