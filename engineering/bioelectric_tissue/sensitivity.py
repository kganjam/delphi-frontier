"""Run a paired, dimensionless K-permeability sensitivity experiment with BETSE.

This is a numerical control study of a generic membrane Dm_K multiplier. It
does not parameterize Kir2.1, Kcnj13, a fish fin, or a measured tissue.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import tempfile
import threading
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from engineering.bioelectric_tissue import analysis

HERE = Path(__file__).resolve().parent
OUT_DEFAULT = HERE.parents[1] / "artifacts" / "bioelectric-tissue" / "k-sensitivity-v1"
MULTIPLIERS = (2.0, 5.0, 10.0)
MAX_WORKERS = 2
_PROGRESS_LOCK = threading.Lock()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def protocol() -> dict:
    return json.loads((HERE / "sensitivity_protocol.json").read_text(encoding="utf-8"))


def environment_packages(betse_python: str) -> dict:
    code = ("import importlib.metadata as m, json; names="
            "['betse','beartype','dill','matplotlib','numpy','pillow','ruamel.yaml','scipy']; "
            "print(json.dumps({n:m.version(n) for n in names}))")
    result = subprocess.run([betse_python, "-c", code], capture_output=True, text=True,
                            timeout=30, check=True)
    return json.loads(result.stdout)


def progress_checkpoint(scenario: str, status: str, command: list[str], started_utc: str,
                        exit_code: int | None = None, source_work: Path | None = None,
                        log_path: Path | None = None) -> dict:
    out_text = os.environ.get("COPS_OUT")
    if not out_text:
        return {"status": status, "files": {}}
    out = Path(out_text)
    out.mkdir(parents=True, exist_ok=True)
    partial = out / "partial"
    partial.mkdir(exist_ok=True)
    source_files = {}
    if source_work is not None:
        for label, source in (("trajectory", source_work / f"{scenario}.npz"),
                              ("config", source_work / "cfg" / "run.yaml")):
            if source.is_file():
                suffix = ".npz" if label == "trajectory" else ".yaml"
                target = partial / f"{scenario}{suffix}"
                shutil.copy2(source, target)
                source_files[label] = {"path": f"partial/{target.name}", "sha256": sha256(target),
                                       "bytes": target.stat().st_size}
    if log_path is not None and log_path.is_file():
        source_files["log"] = {"path": str(log_path.relative_to(out)), "sha256": sha256(log_path),
                               "bytes": log_path.stat().st_size}
    with _PROGRESS_LOCK:
        progress_path = out / "progress.json"
        current = json.loads(progress_path.read_text()) if progress_path.exists() else {"schema": "frontier.betse-k-sensitivity.progress/1", "runs": {}}
        current["runs"][scenario] = {"status": status, "started_utc": started_utc,
                                      "exit_code": exit_code, "command": command,
                                      "files": source_files}
        payload = (json.dumps(current, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
        with tempfile.NamedTemporaryFile(dir=out, prefix=".progress.", delete=False) as stream:
            temp = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temp.replace(progress_path)
    return current["runs"][scenario]


def run_stage(py: str, scenario: str, work: Path, *, template: Path | None,
              multiplier: float = 1.0, k_change: bool = False,
              gap_block: bool = False, half_step: bool = False) -> dict:
    cmd = [py, str(HERE / "betse_stage.py"), scenario, str(work)]
    if template is not None:
        cmd.extend(["--template-dir", str(template)])
    if k_change:
        cmd.extend(["--k-change", "--k-multiplier", str(multiplier)])
    if gap_block:
        cmd.append("--gap-block")
    if half_step:
        cmd.append("--half-step")
    env = {"PATH": "/usr/bin:/bin", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
           "MKL_NUM_THREADS": "1", "MPLBACKEND": "Agg", "HOME": str(work)}
    work.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    started_clock = time.monotonic()
    log_root = Path(os.environ.get("COPS_OUT", str(work.parent))) / "run-logs"
    log_root.mkdir(parents=True, exist_ok=True)
    log_path = log_root / f"{scenario}.log"
    progress_checkpoint(scenario, "running", cmd, started, source_work=work)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=env)
    except subprocess.TimeoutExpired as error:
        log = f"timeout after 600 seconds\n{error.stdout or ''}\n{error.stderr or ''}"[-12000:]
        log_path.write_text(log, encoding="utf-8")
        progress_checkpoint(scenario, "timeout", cmd, started, source_work=work, log_path=log_path)
        raise RuntimeError(f"BETSE stage {scenario} timed out; see {log_path.name}") from error
    finished = datetime.now(timezone.utc).isoformat()
    log = (result.stdout + result.stderr)[-12000:]
    log_path.write_text(log, encoding="utf-8")
    if result.returncode != 0:
        progress_checkpoint(scenario, "failed", cmd, started, result.returncode, source_work=work, log_path=log_path)
        raise RuntimeError(f"BETSE stage {scenario} exited {result.returncode}; see {log_path.name}")
    progress = progress_checkpoint(scenario, "completed", cmd, started, result.returncode,
                                   source_work=work, log_path=log_path)
    return {"scenario": scenario, "command": cmd, "started_utc": started,
            "finished_utc": finished, "elapsed_s": time.monotonic() - started_clock,
            "exit_code": result.returncode, "log": str(log_path.relative_to(Path(os.environ.get("COPS_OUT", str(work.parent))))),
            "log_sha256": sha256(log_path), "checkpoint_files": progress["files"]}


def paired_effect(d: dict, base: dict) -> dict:
    eff = analysis.effect(d, base)
    target = eff["targeted_peak_dVm_mV"]
    other = eff["other_peak_dVm_mV"]
    eff["absolute_spread_ratio_other_over_targeted"] = (
        float(abs(other) / abs(target)) if target is not None and abs(target) > 0 else None
    )
    return eff


def timestep_difference(coarse: dict, fine: dict) -> dict:
    t = np.asarray(coarse["time_s"], dtype=float)
    tf = np.asarray(fine["time_s"], dtype=float)
    v_coarse = np.asarray(coarse["vm_cell_V"], dtype=float)
    v_fine = np.asarray(fine["vm_cell_V"], dtype=float)
    c_coarse = np.asarray(coarse["cc_mol_m3"], dtype=float)
    c_fine = np.asarray(fine["cc_mol_m3"], dtype=float)
    v_interp = np.stack([np.interp(t, tf, v_fine[:, j]) for j in range(v_fine.shape[1])], axis=1)
    c_interp = np.stack([np.interp(t, tf, c_fine[:, i, j]) for i in range(c_fine.shape[1])
                         for j in range(c_fine.shape[2])], axis=1).reshape(c_coarse.shape)
    return {
        "coarse_dt_s": float(coarse["dt_s"]), "fine_dt_s": float(fine["dt_s"]),
        "sample_times_interpolated_to_coarse_grid": True,
        "max_abs_delta_Vm_mV": float(np.max(np.abs(v_coarse - v_interp)) * 1e3),
        "max_abs_delta_concentration_mmol_L": float(np.max(np.abs(c_coarse - c_interp))),
        "note": "solver convergence comparison for this one simulated condition only; not an empirical error bound",
    }


def make_manifest(out: Path, work: Path, run_records: list[dict], source_commit: str,
                  betse_python: str) -> dict:
    protocol_obj = protocol()
    protocol_bytes = (HERE / "sensitivity_protocol.json").read_bytes()
    protocol_sha = hashlib.sha256(protocol_bytes).hexdigest()
    (out / "protocol.json").write_bytes(protocol_bytes)

    names = ["baseline", *[f"k{int(m)}_{c}" for m in MULTIPLIERS for c in ("open", "blocked")], "k10_open_half_dt"]
    data = {name: analysis.load(work / name / f"{name}.npz") for name in names}
    base = data["baseline"]
    files = {}
    effects = {}
    for name in names:
        config_src = work / name / "cfg" / "run.yaml"
        config_dst = out / "configs" / f"{name}.yaml"
        trajectory_src = work / name / f"{name}.npz"
        trajectory_dst = out / "trajectories" / f"{name}.npz"
        config_dst.parent.mkdir(parents=True, exist_ok=True)
        trajectory_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(config_src, config_dst)
        shutil.copy2(trajectory_src, trajectory_dst)
        files[name] = {
            "config": f"configs/{config_dst.name}", "config_sha256": sha256(config_dst),
            "trajectory": f"trajectories/{trajectory_dst.name}", "trajectory_sha256": sha256(trajectory_dst),
            "trajectory_bytes": trajectory_dst.stat().st_size,
        }
        if name != "baseline":
            effects[name] = paired_effect(data[name], base)
    coarse = data["k10_open"]
    fine = data["k10_open_half_dt"]
    comparison = timestep_difference(coarse, fine)
    numeric_ok = all(np.isfinite(v).all() for item in data.values()
                     for v in (item["vm_cell_V"], item["cc_mol_m3"], item["gj_open_fraction_mem"]))
    same_geometry = all(np.array_equal(item["cell_centres_m"], base["cell_centres_m"])
                        for item in data.values())
    checks = {
        "all_saved_states_finite": {"ok": bool(numeric_ok), "criterion": "all saved Vm, concentration and junction-state arrays finite"},
        "paired_world_geometry_identical": {"ok": bool(same_geometry), "criterion": "all scenarios have byte-numerically identical cell coordinates"},
        "positive_concentrations": {"ok": bool(all((item["cc_mol_m3"] > 0).all() for item in data.values())), "minimum_mmol_L": float(min(item["cc_mol_m3"].min() for item in data.values())), "criterion": "all saved concentrations positive"},
        "same_target_cells": {"ok": bool(all(np.array_equal(item["spot_cells"], base["spot_cells"]) for item in data.values())), "criterion": "all runs retain the baseline Spot target-cell indices"},
    }
    summary = {
        "schema": "frontier.betse-k-sensitivity.results/1",
        "label": "SIMULATED; BETSE 1.5.0; generic 2-D patch; parameter sensitivity only; not a measured tissue or fin model",
        "protocol_sha256": protocol_sha,
        "source_commit": source_commit,
        "source_files": {name: sha256(HERE / name) for name in ("betse_stage.py", "sensitivity.py", "render_sensitivity.py", "run-betse-sensitivity.sh", "sensitivity_protocol.json", "analysis.py", "requirements-betse.txt") if (HERE / name).is_file()},
        "protocol_path": "protocol.json",
        "betse_version": subprocess.run([str(Path(betse_python).parent / "betse"), "--version"], capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[-1],
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(),
                        "packages": environment_packages(betse_python),
                        "ffmpeg": subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True,
                                                  timeout=30, check=True).stdout.splitlines()[0],
                        "source_archive_sha256": os.environ.get("FRONTIER_SOURCE_ARCHIVE_SHA256", "not supplied by local runner")},
        "conditions": protocol_obj["conditions"],
        "n_cells": int(base["n_cells"]),
        "n_membranes": int(base["n_mems"]),
        "samples": int(len(base["time_s"])),
        "sampled_time_s": [float(base["time_s"][0]), float(base["time_s"][-1])],
        "files": files,
        "effects_vs_same_world_baseline": effects,
        "time_step_sensitivity_k10_open": comparison,
        "checks": checks,
        "run_records": run_records,
        "limits": protocol_obj["limits"],
        "all_checks_ok": all(item["ok"] for item in checks.values()),
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--betse-python", required=True, help="Python executable from the isolated BETSE 1.5.0 environment")
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--source-commit", default=os.environ.get("FRONTIER_SOURCE_COMMIT", "unknown"))
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    if args.preflight:
        version = subprocess.run([str(Path(args.betse_python).parent / "betse"), "--version"],
                                 capture_output=True, text=True, timeout=30, check=True).stdout.strip()
        if "BETSE 1.5.0" not in version:
            raise SystemExit("preflight requires BETSE 1.5.0")
        pyver = subprocess.run([args.betse_python, "-c", "import sys; print(sys.version.split()[0])"],
                               capture_output=True, text=True, timeout=30, check=True).stdout.strip()
        if not pyver.startswith("3.12."):
            raise SystemExit("preflight requires Python 3.12")
        packages = environment_packages(args.betse_python)
        pinned = {}
        for row in (HERE / "requirements-betse.txt").read_text(encoding="utf-8").splitlines():
            row = row.strip()
            if row and not row.startswith("#") and "==" in row:
                package, expected = row.split("==", 1)
                pinned[package.lower()] = expected
        normalized = {key.lower(): value for key, value in packages.items()}
        mismatch = {key: {"expected": value, "actual": normalized.get(key)}
                    for key, value in pinned.items() if normalized.get(key) != value}
        if mismatch:
            raise SystemExit("preflight pinned dependency versions do not match")
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            raise SystemExit("preflight requires ffmpeg to render saved states")
        ffmpeg_version = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True,
                                        timeout=30, check=True).stdout.splitlines()[0]
        print(json.dumps({"preflight": "ok", "betse": version, "python": pyver, "packages": packages,
                          "ffmpeg": ffmpeg_version, "conditions": len(protocol()["conditions"])}))
        return
    work = args.work.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    runs = []
    baseline = work / "baseline"
    runs.append(run_stage(args.betse_python, "baseline", baseline, template=None))
    conditions = [
        {"id": f"k{int(mult)}_{coupling}", "multiplier": mult, "blocked": coupling == "blocked", "half": False}
        for mult in MULTIPLIERS for coupling in ("open", "blocked")
    ] + [{"id": "k10_open_half_dt", "multiplier": 10.0, "blocked": False, "half": True}]
    def launch(condition: dict) -> dict:
        return run_stage(args.betse_python, condition["id"], work / condition["id"], template=baseline,
                         multiplier=condition["multiplier"], k_change=True,
                         gap_block=condition["blocked"], half_step=condition["half"])
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        runs.extend(pool.map(launch, conditions))
    result = make_manifest(out, work, runs, args.source_commit, args.betse_python)
    from engineering.bioelectric_tissue.render_sensitivity import render
    result["animation"] = render(out, result)
    (out / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"all_checks_ok": result["all_checks_ok"], "conditions": len(result["conditions"]),
                      "summary": str(out / "summary.json"), "video": str(out / "sensitivity.mp4")}))


if __name__ == "__main__":
    main()
