"""J1: global (Sobol/Saltelli) sensitivity of the M1 escape-to-launch model: which unknowns drive capture, emergence speed and take-off?

    python -m engineering.neuro.sobol_m1 --out OUTDIR [--N 4096] [--seed 20261101] [--procs 16]

Inputs: the 26 M1 priors (uniform, PRIORS in fast_start.py) plus 6 auxiliary uniforms that replace M1's internal random draws
(response, away/towards, ET mixture, ET value, turn side, threat azimuth) so the model is a deterministic function of 32 inputs.
Design: scrambled Sobol sequence (scipy.stats.qmc, seeded), Saltelli A/B/AB_i matrices, N (d+2) model runs per scenario.
Estimators: first order S1 (Saltelli 2010 form), total ST (Jansen 1999 form); 95% bootstrap intervals (300 resamples).
Scenarios:
  predator   all inputs vary; output = caught (0/1).
  kinematic  predator disabled (_no_predator switch, p_resp = 1, generous 8 s horizon): outputs = emergence speed, emergence angle,
             time to surface, taxi end speed (pessimistic start), take-off (0/1). Inputs that cannot act here (predator,
             looming, p_resp) must come out ~0: an inert-input control.
Controls: Ishigami function with analytic indices; exact reproduction of the committed M1 run's first 2000 samples (seed 20261101).
SIMULATED: sensitivity of a model to its declared priors; it ranks what to measure, it does not measure anything.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, sys, time
from multiprocessing import Pool
import numpy as np
from scipy.stats import qmc

from engineering.neuro import fast_start as F

AUX = ["_u_resp", "_u_away", "_u_mix", "_u_et", "_u_side", "_u_ap"]
NAMES = list(F.PRIORS) + AUX
INERT_KINEMATIC = ["p_resp", "theta_thr_deg", "u_pred_ms", "D_pred_m", "r0_m", "e_pred_deg", "_u_resp", "_u_ap"]


def to_inputs(U):
    s = {}
    for j, k in enumerate(NAMES):
        if k in F.PRIORS:
            lo, hi = F.PRIORS[k][0]; s[k] = lo + (hi - lo) * U[:, j]
        else:
            s[k] = U[:, j].copy()
    return s


def run_chunk(args):
    U, scen = args
    s = to_inputs(U); s["_seed"] = 0
    if scen == "kinematic":
        s["p_resp"] = np.full(len(U), 1.0); s["_no_predator"] = True
        r = F.simulate(s, T=8.0)
        return {"U_emerge": r["U_emerge_ms"], "gamma_emerge": r["gamma_emerge_deg"], "t_emerge_after_command": r["t_emerge_s"] - r["t_go_s"],
                "V_taxi_end": r["V_taxi_end_ms_pes"], "takeoff": r["took_off_pes"].astype(float), "emerged": r["emerged"].astype(float)}
    r = F.simulate(s)
    return {"caught": r["caught"].astype(float)}


def evaluate(M, scen, procs, chunk=2048):
    parts = [(M[i:i + chunk], scen) for i in range(0, len(M), chunk)]
    with Pool(procs) as p:
        outs = p.map(run_chunk, parts)
    return {k: np.concatenate([o[k] for o in outs]) for k in outs[0]}


def indices(fA, fB, fAB, rng, nboot=300):
    N, d = fAB.shape
    def est(idx):
        a, b, ab = fA[idx], fB[idx], fAB[idx]
        V = np.var(np.r_[a, b])
        S1 = np.mean(b[:, None] * (ab - a[:, None]), axis=0) / V
        ST = 0.5 * np.mean((a[:, None] - ab) ** 2, axis=0) / V
        return S1, ST, V
    S1, ST, V = est(np.arange(N))
    bs = [est(rng.integers(0, N, N)) for _ in range(nboot)]
    S1b = np.array([b[0] for b in bs]); STb = np.array([b[1] for b in bs])
    return {"S1": S1, "ST": ST, "S1_ci95": np.percentile(S1b, [2.5, 97.5], axis=0).T, "ST_ci95": np.percentile(STb, [2.5, 97.5], axis=0).T, "var": V}


def saltelli(N, d, seed):
    X = qmc.Sobol(d=2 * d, scramble=True, seed=seed).random(N)
    A, B = X[:, :d], X[:, d:]
    AB = np.repeat(A[None], d, axis=0)
    for j in range(d):
        AB[j, :, j] = B[:, j]
    return A, B, AB


def ishigami_control(seed):
    a, b = 7.0, 0.1
    f = lambda X: np.sin(X[:, 0]) + a * np.sin(X[:, 1]) ** 2 + b * X[:, 2] ** 4 * np.sin(X[:, 0])
    A, B, AB = saltelli(8192, 3, seed); sc = lambda Z: -math.pi + 2 * math.pi * Z
    fA, fB = f(sc(A)), f(sc(B)); fAB = np.stack([f(sc(AB[j])) for j in range(3)], 1)
    r = indices(fA, fB, fAB, np.random.default_rng(seed), nboot=50)
    V = a * a / 8 + b * math.pi ** 4 / 5 + b * b * math.pi ** 8 / 18 + 0.5
    V1 = 0.5 * (1 + b * math.pi ** 4 / 5) ** 2; V2 = a * a / 8; V13 = b * b * math.pi ** 8 * (1 / 18 - 1 / 50)
    exact_S1 = [V1 / V, V2 / V, 0.0]; exact_ST = [(V1 + V13) / V, V2 / V, V13 / V]
    ok = bool(np.all(np.abs(r["S1"] - exact_S1) < 0.03) and np.all(np.abs(r["ST"] - exact_ST) < 0.03))
    return {"name": "control: Ishigami S1/ST within 0.03 of analytic (N 8192)", "pass": ok, "detail": {"S1": r["S1"].tolist(), "exact_S1": exact_S1, "ST": r["ST"].tolist(), "exact_ST": exact_ST}}


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--N", type=int, default=4096)
    ap.add_argument("--seed", type=int, default=20261101); ap.add_argument("--procs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--reference", default=None, help="committed M1 results.json for the reproduction control")
    a = ap.parse_args(argv); t0 = time.time(); os.makedirs(a.out, exist_ok=True)
    checks = [ishigami_control(a.seed)]
    if a.reference:
        ref = json.load(open(a.reference))["samples_head"]
        s = F.sample(np.random.default_rng(20261101), 20000); s["_seed"] = 20261101; x = F.simulate(s)
        nref = len(ref["caught"]); keys = ("U_emerge_ms", "V_taxi_end_ms_pes", "caught", "gamma_emerge_deg")
        same = all(np.array_equal(np.nan_to_num(np.asarray(x[k][:nref], float), nan=-1), np.nan_to_num(np.asarray(ref[k], float), nan=-1)) for k in keys)
        close = all(np.allclose(np.nan_to_num(np.asarray(x[k][:nref], float), nan=-1), np.nan_to_num(np.asarray(ref[k], float), nan=-1), rtol=1e-9, atol=1e-12) for k in keys)
        checks.append({"name": f"control: committed M1 run (seed 20261101) reproduced on this machine, first {nref} samples (bitwise / within 1e-9)", "pass": close, "detail": {"bitwise": same, "within_1e-9": close}})
    d = len(NAMES); rng = np.random.default_rng(a.seed)
    A, B, AB = saltelli(a.N, d, a.seed)
    M = np.concatenate([A, B] + [AB[j] for j in range(d)])
    res = {"inputs": NAMES, "N": a.N, "d": d, "runs_per_scenario": len(M), "scenarios": {}}
    for scen in ("predator", "kinematic"):
        ts = time.time(); Y = evaluate(M, scen, a.procs)
        out = {"elapsed_s": time.time() - ts, "outputs": {}}
        for k, y in Y.items():
            if k == "emerged":
                out["emerged_fraction"] = float(y.mean()); continue
            y = np.where(np.isfinite(y), y, np.nan)
            fin = np.isfinite(y).all() or k in ("caught", "takeoff")
            if not np.isfinite(y).all():          # non-emerged rows (kinematic): impute as 0 speed / NaN-free by construction check
                nbad = int((~np.isfinite(y)).sum()); y = np.nan_to_num(y, nan=0.0)
            else:
                nbad = 0
            fA, fB = y[:a.N], y[a.N:2 * a.N]; fAB = y[2 * a.N:].reshape(d, a.N).T
            r = indices(fA, fB, fAB, rng)
            out["outputs"][k] = {"mean": float(np.mean(np.r_[fA, fB])), "nonfinite_rows_set_to_0": nbad,
                                 "S1": dict(zip(NAMES, r["S1"].tolist())), "ST": dict(zip(NAMES, r["ST"].tolist())),
                                 "S1_ci95": dict(zip(NAMES, r["S1_ci95"].tolist())), "ST_ci95": dict(zip(NAMES, r["ST_ci95"].tolist())), "variance": float(r["var"])}
        res["scenarios"][scen] = out
    kin = res["scenarios"]["kinematic"]["outputs"]
    inert_max = max(abs(kin[o]["ST"][k]) for o in kin for k in INERT_KINEMATIC)
    checks.append({"name": "control: inert inputs in the kinematic scenario (predator, looming, response) have |ST| < 0.01", "pass": inert_max < 0.01, "detail": inert_max})
    res["checks"] = checks; res["all_checks_pass"] = all(c["pass"] for c in checks)
    res["elapsed_s"] = time.time() - t0
    res["env"] = {"python": sys.version.split()[0], "numpy": np.__version__, "cpu_count": os.cpu_count(), "procs": a.procs}
    import scipy; res["env"]["scipy"] = scipy.__version__
    with open(os.path.join(a.out, "sobol_m1.json"), "w") as fh:
        json.dump(res, fh, default=lambda o: o.tolist() if hasattr(o, "tolist") else (o.item() if isinstance(o, np.generic) else str(o)))
    print(json.dumps({"checks": [(c["name"], c["pass"]) for c in checks], "elapsed_s": res["elapsed_s"]}))
    return 0 if res["all_checks_pass"] else 3


if __name__ == "__main__":
    sys.exit(main())
