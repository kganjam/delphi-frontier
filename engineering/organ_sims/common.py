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

# Project scale(s) each run belongs to (studio-page vocabulary) and what it does NOT establish, so the studio panel can
# link a run without overclaiming.  index.json in artifacts/organ-sims repeats this per run with the manifest hash.
SCALES = {
    "r1-v3b-convergence": (["organ"], "No fin load, flight or biological claim: an inviscid thin-surface lattice-convergence diagnosis of three designed fin geometries; no body, viscosity or separation."),
    "r2-glide-sweep": (["organism", "organ"], "No achieved range: point-mass glide with fixed CL and assumed polars; ranges are +-20% at best and nothing was printed or thrown; hand-launch feasibility is not shown."),
    "r3-underwater-drag": (["organism"], "No measured or CFD-resolved drag at the target Reynolds number; no swimming, wave drag or surface taxiing; rigid deep-water build-up only."),
    "r4-aeroelastic-stiffness": (["organ", "tissue"], "No flying-fish fin stiffness: the sourced EI is bluegill rays (Alben 2007); torsion-rigid, linear beam; does not establish fin twist, membrane mechanics or in-flight deformation."),
    "r5b-staggered-release": (["collective", "organism"], "No observed schooling or launch: rigid printed gliders released with assumed timing offsets and dispersion; no sensing, control or behaviour (ff-eco); straight horseshoe wakes, no wake roll-up or decay."),
    "r6-trim-map": (["organism"], "No flight test: 6-DOF quasi-steady glider with assumed polars, CLmax and dispersion; trims are computed, not hand-trimmed; keys above dec+4 do not exist as prints; no aeroelasticity (R4) or launch-stroke loads."),
    "r4b-torsion": (["organ", "tissue"], "No measured fin torsional stiffness: GJ is swept as a ratio of EI (biology unsourced) and estimated for the print with an ASSUMED Poisson ratio; uniform rod about an assumed elastic axis; no membrane, ray network or unsteady loads."),
    "r1b-v3b-fix": (["organ"], "No measured fin pose or lift: inviscid thin-surface VLM on rebuilt designed geometry; camber sign and sweep are assumed deployment knobs (Park & Choi 2010 unread); no body, viscosity or separation."),
    "r5c-integrated-launch": (["collective", "organism"], "No observed launch or schooling: rigid printed gliders of computed (not hand-trimmed) designs released under an assumed timing rule and dispersion; straight horseshoe wakes; no control or behaviour (ff-eco)."),
    "r7-aeroelastic-flight": (["organism", "organ"], "No measured fin flexibility or flight: a quasi-static lift multiplier from R4b (v3a fin geometry, assumed elastic axis and Poisson ratio) applied in the 6-DOF model; no fin dynamics or flutter."),
    "r5-school-launch": (["collective", "organism"], "No observed schooling or collective behaviour: rigid printed gliders released together under an ASSUMED dispersion; no sensing, control, decision or population dynamics (ff-eco owns those); wake model is a straight horseshoe per fish."),
}


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def head() -> str:
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()


def manifest(run_id: str, title: str, inputs: list[str], results: dict, checks: list[dict], design: dict, seed=None,
             figures: list[str] = (), extra: dict | None = None) -> dict:
    sc = SCALES.get(run_id, ([], None))
    m = {"schema": "frontier.organ-sim.manifest/1", "id": run_id, "title": title, "evidence_kind": SCOPE,
         "scales": sc[0], "does_not_establish": sc[1],
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
