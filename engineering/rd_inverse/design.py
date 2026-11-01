"""Bounded inverse Schnakenberg design exercise (synthetic, model units). See protocol.json, frozen first.

Subcommands: preflight (hashes only) | control (tiny CPU controls + CPU/CUDA parity; CUDA required with --require-cuda) |
run (targets -> Sobol baseline and elite Gaussian search, 64 true evaluations each per target -> oracle/negatives ->
independent checks). Each phase writes and hashes its output before the next. Reuses the frozen solver unmodified.
Nothing here interprets a result biologically; optimizer worse or failed is a legitimate outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import time
from pathlib import Path

import numpy as np
import torch

from engineering.rd_diffusion import rd_ddpm as rd
from engineering.rd_numerics import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.json"
A, B_PAR, TAU, DT, N = 0.15, 0.9, 200.0, 0.02, 64
D_RANGE, L_RANGE = (10.0, 40.0), (30.0, 70.0)
BUDGET, ROUNDS, PER_ROUND, ELITES, SD_FLOOR = 64, 4, 16, 4, 0.03
GATE_A_PTP, GATE_B_RMS, NEAR_MARGIN, FAIL_ABS = 0.10, 0.02, 0.005, 1000.0


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=1, sort_keys=True, allow_nan=False) + "\n")


def protocol():
    return json.loads(PROTOCOL.read_text())


def preflight():
    """Refuse when a pinned source differs from the protocol. Hash and import check only."""
    proto, bad = protocol(), []
    for name, pin in proto["source_pins"].items():
        if sha(ROOT / pin["path"]) != pin["sha256"]:
            bad.append(name)
    if bad:
        raise SystemExit(f"preflight refused: source hash mismatch for {bad}")
    return {"preflight": "ok", "protocol_sha256": sha(PROTOCOL), "design_py_sha256": sha(Path(__file__)),
            "pins": {k: v["sha256"] for k, v in proto["source_pins"].items()}}


# ------------------------------------------------------------------ mapping and solver
def to_params(unit):
    unit = np.asarray(unit, float)
    return np.stack([D_RANGE[0] + (D_RANGE[1] - D_RANGE[0]) * unit[..., 0], L_RANGE[0] + (L_RANGE[1] - L_RANGE[0]) * unit[..., 1]], -1)


def solve_batch(dl, seeds, n=N, dt=DT, tau=TAU, device="cpu"):
    """dl: (B,2) [d, L]; seeds: (B,). Returns final (u,v) fields (B,2,n) float64. a and b are the frozen values."""
    dl = np.asarray(dl, float)
    us, vs = [], []
    u0, v0 = A + B_PAR, B_PAR / (A + B_PAR) ** 2
    for (_d, length), seed in zip(dl, seeds):
        du, dv = rd.ic_modal(int(seed), rd.S["K_modes"], length, n, rd.S["eps"] * abs(u0), rd.S["eps"] * abs(v0))
        us.append(u0 + du)
        vs.append(v0 + dv)

    def make(x):
        return torch.as_tensor(np.asarray(x), dtype=torch.float64, device=device)

    count = len(dl)
    u, v, _ = rd.advance(make(us), make(vs), make(np.full(count, A)), make(np.full(count, B_PAR)), make(dl[:, 0]), make(dl[:, 1]),
                         int(round(tau / dt)), dt=dt)
    return torch.stack([u, v], 1).cpu().numpy()


def rms(field, target):
    """Raw RMS over both channels and all cells; None when the candidate failed."""
    if not np.isfinite(field).all() or np.abs(field).max() > FAIL_ABS:
        return None
    return float(np.sqrt(np.mean((field - target) ** 2)))


# ------------------------------------------------------------------ methods (blind: they see points and scores only)
def sobol_points(seed, count):
    return torch.quasirandom.SobolEngine(2, scramble=True, seed=int(seed)).draw(count, dtype=torch.float64).numpy()


def baseline_points(index):
    return sobol_points(1000 + index, BUDGET)


def initial_points(index):
    return sobol_points(2000 + index, PER_ROUND)


def next_points(index, round_no, points, scores):
    """Elite Gaussian proposal from already evaluated unit-square points and scores (None = failed, ranks last)."""
    order = sorted(range(len(points)), key=lambda i: (math.inf if scores[i] is None else scores[i], i))[:ELITES]
    elite = np.asarray(points)[order]
    sd = np.maximum(elite.std(axis=0), SD_FLOOR)
    gen = torch.Generator().manual_seed(3000 + 10 * index + round_no)
    draw = torch.randn(PER_ROUND, 2, generator=gen, dtype=torch.float64).numpy() * sd + elite.mean(axis=0)
    return np.clip(draw, 0.0, 1.0)


class Ledger:
    """Counts every true solver evaluation per (target, method); refuses to exceed the budget."""

    def __init__(self):
        self.used = {}

    def charge(self, target, method, count):
        key = (target, method)
        self.used[key] = self.used.get(key, 0) + count
        if self.used[key] > BUDGET:
            raise RuntimeError(f"budget exceeded for {key}: {self.used[key]}")


def select(scores):
    ranked = sorted(range(len(scores)), key=lambda i: (math.inf if scores[i] is None else scores[i], i))
    return ranked[0]


# ------------------------------------------------------------------ phases
def control(device, require_cuda):
    if require_cuda and not torch.cuda.is_available():
        raise SystemExit("control refused: CUDA required and unavailable; no CPU fallback")
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    out = {"audit_controls": audit.controls(device)}
    dl = np.array([[20.0, 40.0], [30.0, 55.0], [12.0, 35.0], [38.0, 68.0]])
    seeds = np.array([910000, 910001, 910002, 910003])
    cpu = solve_batch(dl, seeds, tau=20.0, device="cpu")
    out["my_solver_cpu_cuda_max_abs"] = float(np.abs(cpu - solve_batch(dl, seeds, tau=20.0, device="cuda")).max()) if device == "cuda" else None
    out["tf32_disabled"] = not (torch.backends.cuda.matmul.allow_tf32 or torch.backends.cudnn.allow_tf32)
    out["passed"] = bool(out["audit_controls"]["passed"] and out["tf32_disabled"]
                         and (device != "cuda" or out["my_solver_cpu_cuda_max_abs"] < 1e-9))
    out["device"] = device
    return out


def environment(device):
    return {"python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "device": device,
            "cuda_available": torch.cuda.is_available(), "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "tf32_matmul": bool(torch.backends.cuda.matmul.allow_tf32), "tf32_cudnn": bool(torch.backends.cudnn.allow_tf32),
            "cpu_count": os.cpu_count(), "torch_threads": torch.get_num_threads(), "gpu_telemetry": rd.gpu_telemetry()}


def run(out_dir, device, require_cuda, cap_s=None):
    start = time.time()
    proto = protocol()
    cap = proto["bounds"]["hard_cap_s"] if cap_s is None else cap_s
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    receipt = {"schema": "frontier.rd-inverse.receipt/1", "protocol_sha256": sha(PROTOCOL), "design_py_sha256": sha(Path(__file__)),
               "phases": {}, "complete": False, "environment": environment(device)}

    def finish(name, files):
        receipt["phases"][name] = {"files": {f: sha(out / f) for f in files}, "elapsed_s": round(time.time() - start, 2)}
        dump(out / "receipt.json", receipt)
        if time.time() - start > cap:
            receipt["stopped_at_cap_after"] = name
            dump(out / "receipt.json", receipt)
            raise SystemExit(f"hard cap {cap}s reached after {name}; later phases absent")

    pre = preflight()
    ctl = control(device, require_cuda)
    dump(out / "control.json", {**ctl, "preflight": pre})
    finish("control", ["control.json"])
    if not ctl["passed"]:
        raise SystemExit("control failed; no outcomes generated")

    targets = proto["targets"]["list"]
    true_dl = np.array([[t["d_true"], t["L_true"]] for t in targets])
    seeds = np.array([t["ic_seed"] for t in targets])
    target_fields = solve_batch(true_dl, seeds, device=device)
    ptp = [float(f[0].max() - f[0].min()) for f in target_fields]
    gate_a = [p >= GATE_A_PTP for p in ptp]
    np.savez_compressed(out / "targets.npz", fields=target_fields, d_L_true=true_dl, ic_seed=seeds)
    dump(out / "targets.json", {"targets": targets, "u_peak_to_peak": ptp, "gate_A_met": gate_a, "gate_A_threshold": GATE_A_PTP})
    finish("targets", ["targets.npz", "targets.json"])

    ledger = Ledger()
    traces = {m: [[] for _ in targets] for m in ("baseline", "optimizer")}
    fields = {m: [[] for _ in targets] for m in ("baseline", "optimizer")}

    def evaluate(method, unit_by_target):
        flat_unit = np.concatenate(unit_by_target)
        idx = np.concatenate([[i] * len(u) for i, u in enumerate(unit_by_target)])
        for i, u in enumerate(unit_by_target):
            ledger.charge(i, method, len(u))
        result = solve_batch(to_params(flat_unit), seeds[idx], device=device)
        return flat_unit, idx, result

    def record(method, flat_unit, idx, result):
        for k in range(len(flat_unit)):
            i = int(idx[k])
            traces[method][i].append({"unit": flat_unit[k].tolist(), "params_dL": to_params(flat_unit[k]).tolist(), "score": rms(result[k], target_fields[i])})
            fields[method][i].append(result[k])

    base_units = [baseline_points(i) for i in range(len(targets))]
    record("baseline", *evaluate("baseline", base_units))
    units = [initial_points(i) for i in range(len(targets))]
    record("optimizer", *evaluate("optimizer", units))
    for r in range(2, ROUNDS + 1):
        nxt = []
        for i in range(len(targets)):
            pts = np.array([t["unit"] for t in traces["optimizer"][i]])
            nxt.append(next_points(i, r, pts, [t["score"] for t in traces["optimizer"][i]]))
        record("optimizer", *evaluate("optimizer", nxt))
    assert all(ledger.used[(i, m)] == BUDGET for i in range(len(targets)) for m in ("baseline", "optimizer"))
    dump(out / "traces.json", {"budget_per_target_per_method": BUDGET, "evaluation_counts": {f"{i}:{m}": n for (i, m), n in ledger.used.items()}, "traces": traces})
    np.savez_compressed(out / "evaluated_fields.npz", **{f"{m}_{i}": np.stack(fields[m][i]) for m in fields for i in range(len(targets))})
    finish("search", ["traces.json", "evaluated_fields.npz"])

    chosen = {m: [select([t["score"] for t in traces[m][i]]) for i in range(len(targets))] for m in traces}
    sel = {m: [traces[m][i][chosen[m][i]] for i in range(len(targets))] for m in traces}
    near = []
    for i in range(len(targets)):
        pooled = [(m, k, t) for m in traces for k, t in enumerate(traces[m][i]) if t["score"] is not None]
        best = min(t["score"] for _, _, t in pooled)
        members = [t["params_dL"] for _, _, t in pooled if t["score"] <= best + NEAR_MARGIN]
        arr = np.array(members)
        near.append({"target": targets[i]["id"], "best_pooled_score": best, "near_optimal_count": len(members),
                     "d_range": [float(arr[:, 0].min()), float(arr[:, 0].max())], "L_range": [float(arr[:, 1].min()), float(arr[:, 1].max())],
                     "true_in_d_range": bool(arr[:, 0].min() <= targets[i]["d_true"] <= arr[:, 0].max()),
                     "note": "range spread is nonidentifiability, not an error"})
    summary = {"selection": {m: [{"target": targets[i]["id"], "index": chosen[m][i], "params_dL": sel[m][i]["params_dL"], "score": sel[m][i]["score"],
                                   "gate_A_met": gate_a[i], "gate_B_success": bool(gate_a[i] and sel[m][i]["score"] is not None and sel[m][i]["score"] <= GATE_B_RMS)}
                                  for i in range(len(targets))] for m in sel},
               "near_optimal": near, "statuses": {"transport_completeness": "see receipt", "numerical_validity": "control.json passed", "biology": "unknown, not addressed"}}
    dump(out / "selection.json", summary)
    finish("selection", ["selection.json"])

    # separate validation controls: never part of either candidate set
    oracle = solve_batch(true_dl, seeds, device=device)
    over = np.minimum(true_dl * np.array([1.5, 1.0]), [D_RANGE[1], L_RANGE[1]])
    swapped = np.stack([true_dl[:, 0], np.where(true_dl[:, 1] < 50, L_RANGE[1], L_RANGE[0])], 1)
    wrong_ic = solve_batch(true_dl, seeds + 1, device=device)
    neg = {"positive_oracle_scores": [rms(oracle[i], target_fields[i]) for i in range(len(targets))],
           "negative_wrong_d_scores": [rms(f, target_fields[i]) for i, f in enumerate(solve_batch(over, seeds, device=device))],
           "negative_wrong_L_scores": [rms(f, target_fields[i]) for i, f in enumerate(solve_batch(swapped, seeds, device=device))],
           "wrong_ic_scores": [rms(wrong_ic[i], target_fields[i]) for i in range(len(targets))]}
    neg["oracle_ok"] = all(s is not None and s < 1e-12 for s in neg["positive_oracle_scores"])
    neg["negative_ok_on_patterned"] = all(max(a or 0, b or 0) > GATE_B_RMS for a, b, g in zip(neg["negative_wrong_d_scores"], neg["negative_wrong_L_scores"], gate_a) if g)
    neg["wrong_ic_ok"] = all(s is not None and s > 1e-6 for s in neg["wrong_ic_scores"])
    dump(out / "validation_controls.json", neg)
    finish("validation_controls", ["validation_controls.json"])

    cands = {"true": true_dl, "optimizer": np.array([s["params_dL"] for s in sel["optimizer"]]), "baseline": np.array([s["params_dL"] for s in sel["baseline"]])}
    independent = {"seed_generalisation": [], "resolution": []}
    for k in range(3):
        new_seeds = np.array([920000 + 10 * i + k for i in range(len(targets))])
        ref = solve_batch(true_dl, new_seeds, device=device)
        for name in ("optimizer", "baseline"):
            got = solve_batch(cands[name], new_seeds, device=device)
            independent["seed_generalisation"].append({"method": name, "seed_slot": k, "rms_vs_true_params": [rms(got[i], ref[i]) for i in range(len(targets))]})
    base_fields = {name: solve_batch(c, seeds, device=device) for name, c in cands.items()}
    for n, dt in proto["independent_checks"]["resolution"]["configs"]:
        if time.time() - start > cap:
            independent["resolution"].append({"config": [n, dt], "status": "not run: hard cap"})
            continue
        fine = {name: solve_batch(c, seeds, n=n, dt=dt, device=device) for name, c in cands.items()}
        def common(x):
            return np.stack([audit.common_grid(x[:, ch, :])[0] for ch in range(2)], 1)
        row = {"config": [n, dt], "finite": {k: bool(np.isfinite(v).all()) for k, v in fine.items()}}
        if all(row["finite"].values()):
            tgt = common(fine["true"])
            for name in ("optimizer", "baseline"):
                row[f"{name}_rms_vs_target_at_config"] = [rms(common(fine[name])[i], tgt[i]) for i in range(len(targets))]
                row[f"{name}_self_difference_vs_base"] = [rms(common(fine[name])[i], base_fields[name][i]) for i in range(len(targets))]
            row["true_self_difference_vs_base"] = [rms(common(fine["true"])[i], base_fields["true"][i]) for i in range(len(targets))]
        independent["resolution"].append(row)
    dump(out / "independent_checks.json", {**independent, "scope": "sparse: three seeds and three configs, one IC seed per target for resolution; no convergence claim"})
    finish("independent_checks", ["independent_checks.json"])
    receipt["complete"] = True
    receipt["total_elapsed_s"] = round(time.time() - start, 2)
    dump(out / "receipt.json", receipt)
    return receipt


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("preflight", "control", "run"))
    p.add_argument("--out", default="out")
    p.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    p.add_argument("--require-cuda", action="store_true")
    a = p.parse_args(argv)
    if a.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("--device cuda requested and CUDA is unavailable; refusing to fall back")
    if a.command == "preflight":
        print(json.dumps(preflight()))
    elif a.command == "control":
        print(json.dumps(control(a.device, a.require_cuda)))
    else:
        print(json.dumps(run(a.out, a.device, a.require_cuda)["complete"]))


if __name__ == "__main__":
    main()
