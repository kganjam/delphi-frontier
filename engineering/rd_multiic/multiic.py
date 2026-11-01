"""Matched true-solver-budget one-IC vs multi-IC inverse fitting (synthetic, model units). See protocol.json, frozen first.

Subcommands: preflight (hashes; checks only that the sealed manifest path exists) | run. Reuses the original solver unmodified
(engineering.rd_inverse.design.solve_batch). The optimizer sees points and losses only. The fresh test-seed manifest is opened only by
SealedManifest.read(), which raises before the barrier receipt is durably written. Nothing here interprets a result biologically.
"""
from __future__ import annotations

import argparse
import dataclasses
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
from engineering.rd_inverse import design as base
from engineering.rd_numerics import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.json"
ARM_INDEX = {"A_single_IC_matched": 0, "B_multi_IC_matched": 1, "C_single_IC_candidate_matched": 2}
ELITES, SD_FLOOR = 4, 0.03
GATE_A_PTP, GATE_B_RMS, FAIL_ABS = 0.10, 0.02, 1000.0
MANIFEST_SCHEMA = "frontier.rd-multiic.test-seeds/1"
SEED_LO, SEED_HI = 2_000_000, 2_000_000_000


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def protocol():
    return json.loads(PROTOCOL.read_text())


@dataclasses.dataclass
class Plan:
    targets: tuple = (0, 1, 2, 3, 4)
    reps: int = 4
    rounds: int = 8
    arms: dict = dataclasses.field(default_factory=lambda: {"A_single_IC_matched": (1, 64), "B_multi_IC_matched": (4, 16), "C_single_IC_candidate_matched": (1, 16)})
    tau: float = 200.0
    test_count: int = 16
    soft_s: float = 1500.0
    hard_s: float = 1800.0
    sparse_configs: tuple = ((64, 0.005), (128, 0.005), (256, 0.005))

    @classmethod
    def from_protocol(cls):
        p = protocol()
        arms = {n: (a["K"], a["candidates_per_round"]) for n, a in p["arms"].items()}
        return cls(reps=p["replication"]["replicates"], rounds=next(iter(p["arms"].values()))["rounds"], arms=arms, test_count=p["fresh_test_seeds"]["count"],
                   soft_s=p["bounds"]["soft_deadline_s"], hard_s=p["bounds"]["scientific_tree_hard_cap_s"])

    def budget(self, arm):
        k, per = self.arms[arm]
        return k * per * self.rounds


# ------------------------------------------------------------------ seeds, targets, sources
def train_seed(r, i, k):
    return 930000 + 1000 * r + 100 * i + k


def sobol_seed(r, i):
    return 5000 + 100 * r + 10 * i


def proposal_seed(r, i, arm, round_no):
    return 6000 + 1000 * r + 100 * i + 10 * ARM_INDEX[arm] + round_no


def all_training_seeds(plan):
    return {train_seed(r, i, k) for r in range(plan.reps) for i in plan.targets for k in range(4)}


def targets():
    t = json.loads((ROOT / "engineering/rd_inverse/protocol.json").read_text())["targets"]["list"]
    return t[:5]


def preflight(manifest_path=None):
    """Hash check of every pinned source. The manifest is only tested for existence, never opened."""
    bad = [n for n, pin in protocol()["sources"]["pins"].items() if sha(ROOT / pin["path"]) != pin["sha256"]]
    if bad:
        raise SystemExit(f"preflight refused: source hash mismatch for {bad}")
    out = {"preflight": "ok", "protocol_sha256": sha(PROTOCOL), "multiic_py_sha256": sha(Path(__file__))}
    if manifest_path is not None:
        out["manifest_path_exists"] = os.path.exists(manifest_path)
    return out


# ------------------------------------------------------------------ sealed manifest
class EarlyReadError(RuntimeError):
    pass


class SealedManifest:
    """Source-order sealing: read() raises until seal() has durably written the barrier receipt."""

    def __init__(self, path, expected_sha256):
        self.path, self.expected, self._sealed = Path(path), expected_sha256, False

    def seal(self, barrier_path, selections_path, traces_path):
        receipt = {"schema": "frontier.rd-multiic.barrier/1", "selections_sha256": sha(selections_path), "training_traces_sha256": sha(traces_path),
                   "monotonic_ns": time.monotonic_ns(), "unix_time": time.time(), "note": "written and fsynced before the manifest is opened; order in code, not secrecy"}
        with open(barrier_path, "w") as fh:
            fh.write(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        self._sealed = True
        return receipt

    def read(self, plan, forbidden_seeds):
        if not self._sealed:
            raise EarlyReadError("test-seed manifest read before the barrier receipt was written")
        raw = self.path.read_bytes()
        got = hashlib.sha256(raw).hexdigest()
        if got != self.expected:
            raise ValueError(f"manifest sha256 {got} != expected {self.expected}")
        m = json.loads(raw)
        seeds = m.get("seeds", [])
        problems = []
        if m.get("schema") != MANIFEST_SCHEMA:
            problems.append("schema")
        if m.get("protocol_sha256") != sha(PROTOCOL):
            problems.append("protocol_sha256")
        if m.get("count") != plan.test_count or len(seeds) != plan.test_count or len(set(seeds)) != len(seeds):
            problems.append("count_or_duplicates")
        if any((not isinstance(s, int)) or not SEED_LO <= s < SEED_HI for s in seeds):
            problems.append("range")
        if set(seeds) & forbidden_seeds:
            problems.append("overlaps_training_seeds")
        if problems:
            raise ValueError(f"manifest invalid: {problems}")
        return [int(s) for s in seeds]


# ------------------------------------------------------------------ optimizer (blind: points and losses only)
def initial_points(r, i, count):
    return base.sobol_points(sobol_seed(r, i), count)


def propose(seed, points, losses, count):
    order = sorted(range(len(points)), key=lambda j: (math.inf if losses[j] is None else losses[j], j))[:ELITES]
    elite = np.asarray(points)[order]
    sd = np.maximum(elite.std(axis=0), SD_FLOOR)
    gen = torch.Generator().manual_seed(int(seed))
    draw = torch.randn(count, 2, generator=gen, dtype=torch.float64).numpy() * sd + elite.mean(axis=0)
    return np.clip(draw, 0.0, 1.0)


class Ledger:
    def __init__(self, budgets):
        self.budgets, self.used = budgets, {}

    def charge(self, key, count):
        self.used[key] = self.used.get(key, 0) + count
        if self.used[key] > self.budgets[key]:
            raise RuntimeError(f"budget exceeded for {key}: {self.used[key]} > {self.budgets[key]}")


def loss_of(scores):
    return None if any(s is None for s in scores) else float(np.mean(scores))


def common(x):
    return np.stack([audit.common_grid(x[:, ch, :])[0] for ch in range(2)], 1)


def conc(fields):
    return base.conc(fields)


def dump(path, value):
    base.dump(path, value)


def ptp_u(f):
    return float(f[0].max() - f[0].min()) if np.isfinite(f).all() and np.abs(f).max() <= FAIL_ABS else None


def environment(device):
    return {"python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "device": device,
            "cuda_available": torch.cuda.is_available(), "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "tf32_matmul_after_setting": bool(torch.backends.cuda.matmul.allow_tf32), "tf32_cudnn_after_setting": bool(torch.backends.cudnn.allow_tf32),
            "cpu_count": os.cpu_count(), "torch_threads": torch.get_num_threads(), "env_threads": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
            "gpu_telemetry": rd.gpu_telemetry()}


def control(device, require_cuda):
    if require_cuda and not torch.cuda.is_available():
        raise SystemExit("control refused: CUDA required and unavailable; no CPU fallback")
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    dl = np.array([[20.0, 40.0], [30.0, 55.0], [12.0, 35.0], [38.0, 68.0]])
    seeds = np.array([910000, 910001, 910002, 910003])
    cpu = base.solve_batch(dl, seeds, tau=20.0, device="cpu")
    alone = base.solve_batch(dl[2:3], seeds[2:3], tau=20.0, device=device)
    batched = base.solve_batch(dl, seeds, tau=20.0, device=device)
    out = {"audit_controls": audit.controls(device), "device": device,
           "batch_equivalence_max_abs": float(np.abs(alone[0] - batched[2]).max()),
           "cpu_cuda_max_abs": float(np.abs(cpu - batched).max()) if device == "cuda" else None}
    out["tf32_flags_after_setting"] = {"matmul": bool(torch.backends.cuda.matmul.allow_tf32), "cudnn": bool(torch.backends.cudnn.allow_tf32)}
    out["passed"] = bool(out["audit_controls"]["passed"] and out["batch_equivalence_max_abs"] < 1e-10
                         and not any(out["tf32_flags_after_setting"].values()) and (device != "cuda" or out["cpu_cuda_max_abs"] < 1e-9))
    return out


# ------------------------------------------------------------------ pure endpoint logic
def support_verdict(D, admissible, controls_ok, n_pairs_required=15, n_targets_required=4, min_admissible=8):
    """D: dict (target, rep) -> E_A - E_B (None when undefined); admissible: dict target -> count.
    Returns a named verdict. A failed control blocks; the rule thresholds are those frozen in the protocol."""
    if not controls_ok["all"]:
        return {"verdict": "blocked", "failed_controls": [k for k, v in controls_ok.items() if k != "all" and not v]}
    included = [t for t in sorted({k[0] for k in D}) if admissible.get(t, 0) >= min_admissible]
    excluded = [t for t in sorted({k[0] for k in D}) if t not in included]
    pairs = [(k, v) for k, v in D.items() if k[0] in included and v is not None]
    positive = sum(v > 0 for _, v in pairs)
    med_pos = 0
    for t in included:
        vals = [v for (tt, _), v in pairs if tt == t]
        med_pos += bool(vals) and float(np.median(vals)) > 0
    ok = positive >= n_pairs_required and med_pos >= n_targets_required
    return {"verdict": "supported_descriptively" if ok else "not_supported", "pairs_positive": positive, "pairs_total": len(pairs),
            "targets_with_positive_median": med_pos, "targets_included": included, "targets_excluded_insufficient_admissible_seeds": excluded,
            "thresholds": {"pairs": n_pairs_required, "targets": n_targets_required}}


# ------------------------------------------------------------------ run
def run(out_dir, device, require_cuda, manifest_path, manifest_sha256, plan=None):
    start = time.time()
    plan = plan or Plan.from_protocol()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    receipt = {"schema": "frontier.rd-multiic.receipt/1", "protocol_sha256": sha(PROTOCOL), "multiic_py_sha256": sha(Path(__file__)), "phases": {},
               "complete": False, "status": None, "plan": dataclasses.asdict(plan)}

    def finish(name, files):
        receipt["phases"][name] = {"files": {f: sha(out / f) for f in files}, "elapsed_s": round(time.time() - start, 2)}
        dump(out / "receipt.json", receipt)
        if time.time() - start > plan.hard_s:
            receipt["stopped_at_hard_cap_after"] = name
            dump(out / "receipt.json", receipt)
            raise SystemExit(f"hard cap {plan.hard_s}s reached after {name}")

    def soft_passed():
        return time.time() - start > plan.soft_s

    pre = preflight(str(manifest_path))
    ctl = control(device, require_cuda)
    receipt["environment_after_setting_flags"] = environment(device)
    dump(out / "control.json", {**ctl, "preflight": pre})
    finish("control", ["control.json"])
    if not ctl["passed"]:
        receipt["status"] = "control_failed: no outcomes generated"
        dump(out / "receipt.json", receipt)
        raise SystemExit(receipt["status"])

    tg = targets()
    true_dl = {i: np.array([tg[i]["d_true"], tg[i]["L_true"]]) for i in plan.targets}
    arms = plan.arms
    # reference fields: the true-parameter field under every training IC seed (reference data, not candidate evaluations)
    ref_keys = [(r, i, k) for r in range(plan.reps) for i in plan.targets for k in range(4)]
    ref = base.solve_batch(np.array([true_dl[i] for _, i, _ in ref_keys]), np.array([train_seed(*key) for key in ref_keys]), tau=plan.tau, device=device)
    ref_field = {key: ref[n] for n, key in enumerate(ref_keys)}
    train_ptp = {f"{r}:{i}:{k}": ptp_u(ref_field[(r, i, k)]) for (r, i, k) in ref_keys}
    train_admissible = {key: bool(v is not None and v >= GATE_A_PTP) for key, v in train_ptp.items()}
    np.savez_compressed(out / "reference_fields.npz", **{f"r{r}_t{i}_k{k}": ref_field[(r, i, k)] for (r, i, k) in ref_keys})
    dump(out / "reference.json", {"reference_trajectories": len(ref_keys), "training_seeds": {f"{r}:{i}:{k}": train_seed(r, i, k) for (r, i, k) in ref_keys},
                                  "u_peak_to_peak": train_ptp, "admissible": train_admissible, "gate_A_threshold": GATE_A_PTP,
                                  "concentration": conc(ref)})
    finish("reference", ["reference_fields.npz", "reference.json"])

    runs = [(r, i, a) for r in range(plan.reps) for i in plan.targets for a in arms]
    ledger = Ledger({run_key: plan.budget(run_key[2]) for run_key in runs})
    state = {k: {"points": [], "loss": [], "per_ic": [], "fields": []} for k in runs}
    complete_training = True
    for round_no in range(1, plan.rounds + 1):
        if soft_passed():
            complete_training = False
            receipt["status"] = f"training_incomplete: soft deadline before round {round_no}; matched comparison void"
            break
        proposals = {}
        for (r, i, a) in runs:
            k_ic, per = arms[a]
            if round_no == 1:
                proposals[(r, i, a)] = initial_points(r, i, per)
            else:
                s = state[(r, i, a)]
                proposals[(r, i, a)] = propose(proposal_seed(r, i, a, round_no), np.array(s["points"]), s["loss"], per)
        rows, owners = [], []
        for key, pts in proposals.items():
            r, i, a = key
            k_ic = arms[a][0]
            ledger.charge(key, len(pts) * k_ic)
            for c, u in enumerate(pts):
                for k in range(k_ic):
                    rows.append((base.to_params(u), train_seed(r, i, k)))
                    owners.append((key, c, k))
        res = base.solve_batch(np.array([p for p, _ in rows]), np.array([s for _, s in rows]), tau=plan.tau, device=device)
        per_cand = {}
        for n, (key, c, k) in enumerate(owners):
            r, i, _ = key
            sc = base.rms(res[n], ref_field[(r, i, k)])
            per_cand.setdefault((key, c), []).append((sc, res[n]))
        for key, pts in proposals.items():
            s = state[key]
            for c, u in enumerate(pts):
                scs, fl = zip(*per_cand[(key, c)])
                s["points"].append(np.asarray(u))
                s["per_ic"].append(list(scs))
                s["loss"].append(loss_of(scs))
                s["fields"].append(np.stack(fl))
        dump(out / "traces_partial.json", {"after_round": round_no, "evaluation_counts": {f"{r}:{i}:{a}": n for (r, i, a), n in ledger.used.items()}})

    rows_out = []
    for key in runs:
        r, i, a = key
        s = state[key]
        rows_out.append({"rep": r, "target": i, "arm": a, "K": arms[a][0], "candidates": [
            {"unit": s["points"][c].tolist(), "params_dL": base.to_params(s["points"][c]).tolist(), "per_ic_rms": s["per_ic"][c], "loss": s["loss"][c]} for c in range(len(s["points"]))]})
    dump(out / "training_traces.json", {"evaluation_counts": {f"{r}:{i}:{a}": n for (r, i, a), n in ledger.used.items()},
                                        "budgets": {f"{r}:{i}:{a}": b for (r, i, a), b in ledger.budgets.items()}, "runs": rows_out})
    np.savez_compressed(out / "training_fields.npz", **{f"r{r}_t{i}_{a[0]}": np.stack(state[(r, i, a)]["fields"]) for (r, i, a) in runs if state[(r, i, a)]["fields"]})
    sel = []
    for key in runs:
        r, i, a = key
        s = state[key]
        valid = [c for c, v in enumerate(s["loss"]) if v is not None]
        idx = min(valid, key=lambda c: (s["loss"][c], c)) if valid else None
        sel.append({"rep": r, "target": i, "arm": a, "index": idx, "status": None if idx is not None else "no_valid_candidate",
                    "params_dL": None if idx is None else base.to_params(s["points"][idx]).tolist(), "loss": None if idx is None else s["loss"][idx],
                    "trajectories_used": ledger.used.get(key, 0), "budget": ledger.budgets[key],
                    "training_pairs_admissible": [train_admissible[f"{r}:{i}:{k}"] for k in range(arms[a][0])]})
    dump(out / "selections.json", {"selection_rule": "lowest training loss, ties to earlier evaluation; training information only", "selections": sel,
                                   "matched_budget_complete": bool(complete_training and all(ledger.used.get(k) == ledger.budgets[k] for k in runs))})
    finish("training", ["training_traces.json", "training_fields.npz", "selections.json"])
    if not complete_training:
        dump(out / "receipt.json", receipt)
        return receipt

    guard = SealedManifest(manifest_path, manifest_sha256)
    barrier = guard.seal(out / "barrier.json", out / "selections.json", out / "training_traces.json")
    receipt["barrier"] = {"selections_sha256": barrier["selections_sha256"], "training_traces_sha256": barrier["training_traces_sha256"]}
    finish("barrier", ["barrier.json"])
    try:
        test_seeds = guard.read(plan, all_training_seeds(plan))
    except (ValueError, OSError) as exc:
        receipt["status"] = f"manifest_unusable: {exc}; training retained, no test endpoint"
        dump(out / "receipt.json", receipt)
        raise SystemExit(receipt["status"])
    if soft_passed():
        receipt["status"] = "soft deadline reached before test phase; not run"
        dump(out / "receipt.json", receipt)
        return receipt

    chosen = [s for s in sel if s["index"] is not None]
    nT, nS = len(plan.targets), len(test_seeds)
    pairs = [(i, s) for i in plan.targets for s in test_seeds]
    true_test = base.solve_batch(np.array([true_dl[i] for i, _ in pairs]), np.array([s for _, s in pairs]), tau=plan.tau, device=device)
    true_field = {pair: true_test[n] for n, pair in enumerate(pairs)}
    admissible = {pair: bool((ptp_u(true_field[pair]) or 0.0) >= GATE_A_PTP) for pair in pairs}
    cand_rows = [(c, s) for c in chosen for s in test_seeds]
    cand_out = base.solve_batch(np.array([c["params_dL"] for c, _ in cand_rows]), np.array([s for _, s in cand_rows]), tau=plan.tau, device=device)
    oracle = base.solve_batch(np.array([true_dl[i] for i, _ in pairs]), np.array([s for _, s in pairs]), tau=plan.tau, device=device)
    over = {i: np.array([min(1.5 * true_dl[i][0], base.D_RANGE[1]), true_dl[i][1]]) for i in plan.targets}
    swap = {i: np.array([true_dl[i][0], base.L_RANGE[1] if true_dl[i][1] < 50 else base.L_RANGE[0]]) for i in plan.targets}
    wd = base.solve_batch(np.array([over[i] for i, _ in pairs]), np.array([s for _, s in pairs]), tau=plan.tau, device=device)
    wl = base.solve_batch(np.array([swap[i] for i, _ in pairs]), np.array([s for _, s in pairs]), tau=plan.tau, device=device)
    np.savez_compressed(out / "test_fields.npz", true=true_test, oracle=oracle, wrong_d=wd, wrong_L=wl, candidates=cand_out,
                        test_seeds=np.array(test_seeds), pair_target=np.array([i for i, _ in pairs]), cand_index=np.array([[c["rep"], c["target"], ARM_INDEX[c["arm"]]] for c, _ in cand_rows]))
    rec = {}
    for n, (c, s) in enumerate(cand_rows):
        i = c["target"]
        rec[(c["rep"], i, c["arm"], s)] = base.rms(cand_out[n], true_field[(i, s)])
    # controls
    per_t = {}
    for i in plan.targets:
        adm = [s for s in test_seeds if admissible[(i, s)]]
        idx = {pair: n for n, pair in enumerate(pairs)}
        wdv = [base.rms(wd[idx[(i, s)]], true_field[(i, s)]) for s in adm]
        wlv = [base.rms(wl[idx[(i, s)]], true_field[(i, s)]) for s in adm]
        wic = [base.rms(true_field[(i, s)], true_field[(i, test_seeds[(test_seeds.index(s) + 1) % nS])]) for s in adm]
        orc = [base.rms(oracle[idx[(i, s)]], true_field[(i, s)]) for s in test_seeds]
        med = lambda v: float(np.median([x for x in v if x is not None])) if any(x is not None for x in v) else None
        per_t[i] = {"admissible_test_seeds": len(adm), "oracle_max": max(x if x is not None else math.inf for x in orc),
                    "wrong_d_median": med(wdv), "wrong_L_median": med(wlv), "wrong_IC_median": med(wic)}
        per_t[i]["oracle_ok"] = per_t[i]["oracle_max"] < 1e-12
        per_t[i]["wrong_parameter_informative"] = bool(max(per_t[i]["wrong_d_median"] or 0, per_t[i]["wrong_L_median"] or 0) > GATE_B_RMS)
        per_t[i]["wrong_IC_informative"] = bool((per_t[i]["wrong_IC_median"] or 0) > GATE_B_RMS)
    inc = [i for i in plan.targets if per_t[i]["admissible_test_seeds"] >= 8]
    controls_ok = {"positive_oracle": all(per_t[i]["oracle_ok"] for i in plan.targets), "wrong_parameter": all(per_t[i]["wrong_parameter_informative"] for i in inc),
                   "wrong_IC": all(per_t[i]["wrong_IC_informative"] for i in inc), "cpu_cuda_and_batch_parity": bool(ctl["passed"])}
    controls_ok["all"] = all(controls_ok.values()) and bool(inc)
    dump(out / "controls.json", {"per_target": {str(i): v for i, v in per_t.items()}, "controls_ok": controls_ok,
                                 "wrong_parameter_predicate": "max(wrong_d, wrong_L) median > 0.02: at least one perturbation, not both",
                                 "concentration_test": {"true": conc(true_test), "candidates": conc(cand_out), "wrong_d": conc(wd), "wrong_L": conc(wl)}})
    finish("test_and_controls", ["test_fields.npz", "controls.json"])

    E, F, perr = {}, {}, {}
    for c in chosen:
        i, a, r = c["target"], c["arm"], c["rep"]
        vals = [rec[(r, i, a, s)] for s in test_seeds if admissible[(i, s)]]
        ok = [v for v in vals if v is not None]
        E[(r, i, a)] = float(np.mean(ok)) if ok and len(ok) == len(vals) else None
        F[(r, i, a)] = float(np.mean([v is not None and v <= GATE_B_RMS for v in vals])) if vals else None
        perr[(r, i, a)] = [abs(c["params_dL"][0] - true_dl[i][0]) / 30.0, abs(c["params_dL"][1] - true_dl[i][1]) / 40.0]
    A, B, C = list(arms)[:3]
    D = {(i, r): (None if E.get((r, i, A)) is None or E.get((r, i, B)) is None else E[(r, i, A)] - E[(r, i, B)]) for i in plan.targets for r in range(plan.reps)}
    verdict = support_verdict(D, {i: per_t[i]["admissible_test_seeds"] for i in plan.targets}, controls_ok)
    dump(out / "endpoints.json", {
        "primary_E": {f"{r}:{i}:{a}": v for (r, i, a), v in E.items()}, "fraction_test_seeds_le_0.02": {f"{r}:{i}:{a}": v for (r, i, a), v in F.items()},
        "per_test_seed_rms": {f"{r}:{i}:{a}:{s}": v for (r, i, a, s), v in rec.items()},
        "paired_D_A_minus_B": {f"{i}:{r}": v for (i, r), v in D.items()}, "parameter_error_range_normalised_d_L": {f"{r}:{i}:{a}": v for (r, i, a), v in perr.items()},
        "verdict": verdict, "arm_C_note": "secondary, a quarter of the trajectory budget, not budget matched",
        "scope": "descriptive; 20 paired cases; one synthetic model; parameter error against known synthetic truth is not identifiability; no biology"})
    finish("endpoints", ["endpoints.json"])

    # sparse N/dt controls: replicate 0, arms A and B, first admissible test seed per target (runs last, skipped past the soft deadline)
    sparse = {"scope": "arms A and B selected candidates (replicate 0) and the true parameters, first admissible test seed per target; consistency only, no convergence claim", "configs": []}
    raw = {}
    rows = []
    for i in plan.targets:
        s0 = next((s for s in test_seeds if admissible[(i, s)]), None)
        if s0 is None:
            continue
        rows.append(("true", i, s0, true_dl[i]))
        for c in chosen:
            if c["rep"] == 0 and c["target"] == i and c["arm"] in (A, B):
                rows.append((c["arm"], i, s0, np.array(c["params_dL"])))
    for n_, dt_ in plan.sparse_configs:
        if soft_passed():
            sparse["configs"].append({"config": [n_, dt_], "status": "not run: soft deadline"})
            continue
        fine = base.solve_batch(np.array([r_[3] for r_ in rows]), np.array([r_[2] for r_ in rows]), n=n_, dt=dt_, tau=plan.tau, device=device)
        raw[f"N{n_}_dt{dt_}"] = fine
        row = {"config": [n_, dt_], "finite": bool(np.isfinite(fine).all()), "rows": []}
        if row["finite"]:
            truths = {r_[1]: common(fine[n:n + 1])[0] for n, r_ in enumerate(rows) if r_[0] == "true"}
            for n, (arm, i, s0, _) in enumerate(rows):
                if arm == "true":
                    continue
                row["rows"].append({"arm": arm, "target": i, "test_seed": s0, "rms_vs_true_at_config": base.rms(common(fine[n:n + 1])[0], truths[i])})
        sparse["configs"].append(row)
    np.savez_compressed(out / "sparse_fields.npz", **raw, order=np.array([f"{a}:{i}:{s}" for a, i, s, _ in rows]))
    dump(out / "sparse_controls.json", sparse)
    finish("sparse_controls", ["sparse_controls.json", "sparse_fields.npz"])
    receipt["complete"] = True
    receipt["status"] = "complete"
    receipt["runtime_scope"] = "GPU runtime of this design unknown before this run; the hard cap and per-phase durable outputs are the bound"
    receipt["total_elapsed_s"] = round(time.time() - start, 2)
    dump(out / "receipt.json", receipt)
    return receipt


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("preflight", "run"))
    p.add_argument("--out", default="out")
    p.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    p.add_argument("--require-cuda", action="store_true")
    p.add_argument("--manifest", default=None)
    p.add_argument("--manifest-sha256", default=None)
    a = p.parse_args(argv)
    if a.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("--device cuda requested and CUDA is unavailable; refusing to fall back")
    if a.command == "preflight":
        print(json.dumps(preflight(a.manifest)))
    else:
        if not a.manifest or not a.manifest_sha256:
            raise SystemExit("run needs --manifest and --manifest-sha256 (infra's sealed test-seed manifest)")
        print(json.dumps(run(a.out, a.device, a.require_cuda, a.manifest, a.manifest_sha256)["complete"]))


if __name__ == "__main__":
    main()
