"""F003 alignment runner: solver A of the frozen nonlinear sweep, batched over cells sharing (model, N), integrated to 2T with a time-resolved
spectrum up to T. Same scheme as scopedesk.oracles.pde._run (Strang: half diffusion, RK4 reaction, half diffusion; exact cosine-mode
diffusion with orthonormal DCT-II; dt 0.02; float64; divergence check after 0-based step k with k % 200 == 0), same initial cosine series
(solvers.ic_modal), same metrics (solvers.metrics). Evidence kind: simulated. See PREREG.md.

  PYTHONPATH=frontier_compute/vendor:. python3 experiments/f003_align/align.py run OUTDIR SPECDIR [--arm base|grid2] [--workers 3]
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from fractions import Fraction as F
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.fft import dct, idct

from scopedesk.oracles import kinetics, linear
from scopedesk.oracles.nonlinear_sweep import ensemble as E
from scopedesk.oracles.nonlinear_sweep import run as R
from scopedesk.oracles.nonlinear_sweep import solvers as S

DT = 0.02
REC_EVERY = 50          # record spectrum and std every 1 tau (50 steps)


def horizon(c):
    lin = linear.check(E.linear_structured(c))
    fast = (lin.get("witness") or {}).get("fastest_growing_mode")
    sig = (fast or {}).get("max_eigenvalue_float", 0.0) or 0.0
    return min(1500.0, max(800.0, 40.0 / sig)) if sig > 0 else 800.0


def run_group(args):
    key, cells, arm, outdir, specdir = args
    model, N, chunk = key
    out_f = Path(outdir) / f"{arm}_{model}_{N}_{chunk}.jsonl"
    if out_f.exists():
        return str(out_f), 0.0
    t0 = time.time()
    B = len(cells)
    pp = [kinetics.params(model, c["params"]) for c in cells]
    st = [tuple(float(z) for z in kinetics.steady(model, p)) for p in pp]
    Ls = np.array([R.grid_for(c)[0] for c in cells])
    Ks = [R.grid_for(c)[3] for c in cells]
    Ts = [c["_T"] for c in cells]
    n_T = [int(round(T / DT)) for T in Ts]
    mult = 1 if arm == "grid2" else 2
    n_end = [mult * n for n in n_T]
    U, V = np.zeros((B, N)), np.zeros((B, N))
    for i, c in enumerate(cells):
        pu, pv = S.ic_modal(c["seed"], Ks[i], Ls[i], N, c["eps"] * abs(st[i][0]), c["eps"] * abs(st[i][1]))
        U[i], V[i] = st[i][0] + pu, st[i][1] + pv
    q = (np.arange(N)[None, :] * math.pi / Ls[:, None]) ** 2
    Dv = np.array([float(F(c["Dv"])) for c in cells])[:, None]
    mu, mv = np.exp(-q * DT / 2), np.exp(-Dv * q * DT / 2)
    keys = ("a", "b") if model == "schnakenberg" else ("A", "B")
    pa = np.array([float(p[keys[0]]) for p in pp])[:, None]
    pb = np.array([float(p[keys[1]]) for p in pp])[:, None]

    def react(u, v):
        w = u * u * v
        if model == "schnakenberg":
            return pa - u + w, pb - w
        return pa - (pb + 1) * u + w, pb * u - w

    def diff(x, m):
        return idct(dct(x, type=2, norm="ortho", axis=1) * m, type=2, norm="ortho", axis=1)

    # initial DCT coefficients of the perturbation (for the exact linear prediction)
    w0u = dct(U - np.array([s[0] for s in st])[:, None], type=2, norm="ortho", axis=1)
    w0v = dct(V - np.array([s[1] for s in st])[:, None], type=2, norm="ortho", axis=1)
    rec = {i: {"std": [float(U[i].std())], "spec": [np.abs(dct(U[i] - U[i].mean(), type=2, norm="ortho")).astype(np.float32)]} for i in range(B)}
    snaps = {i: {} for i in range(B)}
    diverged = np.zeros(B, bool)
    alive = np.arange(B)
    nT_arr = np.array(n_T)
    event_steps = set()
    for nT, ne in zip(n_T, n_end):
        event_steps |= {int(round(0.9 * nT)), nT, nT + 1, int(round(1.8 * nT)), 2 * nT, ne}
    k = 0
    kmax = max(n_end)
    while k < kmax and len(alive):
        ua, va = U[alive], V[alive]
        mua, mva = mu[alive], mv[alive]
        paa, pba = pa[alive], pb[alive]

        def rx(u, v):
            w = u * u * v
            if model == "schnakenberg":
                return paa - u + w, pba - w
            return paa - (pba + 1) * u + w, pba * u - w
        ua, va = diff(ua, mua), diff(va, mva)
        k1u, k1v = rx(ua, va)
        k2u, k2v = rx(ua + .5 * DT * k1u, va + .5 * DT * k1v)
        k3u, k3v = rx(ua + .5 * DT * k2u, va + .5 * DT * k2v)
        k4u, k4v = rx(ua + DT * k3u, va + DT * k3v)
        ua = ua + DT / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        va = va + DT / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        ua, va = diff(ua, mua), diff(va, mva)
        U[alive], V[alive] = ua, va
        step = k + 1
        if k % 200 == 0:
            m = np.maximum(np.abs(ua).max(1), np.abs(va).max(1))
            bad = ~np.isfinite(m) | (m > 1e3)
            for j in np.where(bad)[0]:
                i = alive[j]
                if step <= n_T[i]:
                    diverged[i] = True
                snaps[i]["diverged_at_step"] = step
        if step % REC_EVERY == 0:
            for j in np.where(nT_arr[alive] >= step)[0]:
                i = alive[j]
                rec[i]["std"].append(float(ua[j].std()))
                rec[i]["spec"].append(np.abs(dct(ua[j] - ua[j].mean(), type=2, norm="ortho")).astype(np.float32))
        if step in event_steps:
            for j, i in enumerate(alive):
                nT = n_T[i]
                if step == int(round(0.9 * nT)):
                    snaps[i]["u09"] = ua[j].copy()
                if step == nT:
                    snaps[i]["uT"] = ua[j].copy()
                    snaps[i]["vT"] = va[j].copy()
                if step == nT + 1:
                    snaps[i]["dudt_inf"] = float(np.abs(ua[j] - snaps[i]["uT"]).max() / DT)
                if step == int(round(1.8 * nT)):
                    snaps[i]["u18"] = ua[j].copy()
                if step == 2 * nT:
                    snaps[i]["u2T"] = ua[j].copy()
        if step in event_steps or k % 200 == 0:
            keep = np.array([("diverged_at_step" not in snaps[i]) and step < n_end[i] for i in alive], bool)
            alive = alive[keep]
        k += 1
    lines = []
    specs = {}
    for i, c in enumerate(cells):
        ust = st[i][0]
        r = {"id": c["id"], "arm": arm, "N": N, "T": Ts[i], "diverged_by_T": bool(diverged[i]),
             "diverged_at_step": snaps[i].get("diverged_at_step"), "n_steps_T": n_T[i]}
        if "uT" in snaps[i] and "u09" in snaps[i] and not diverged[i]:
            r["A_T"] = S.metrics(snaps[i]["uT"], snaps[i]["u09"], ust)
            r["dudt_inf_T"] = snaps[i].get("dudt_inf")
        if arm == "base" and "u2T" in snaps[i] and "u18" in snaps[i]:
            r["A_2T"] = S.metrics(snaps[i]["u2T"], snaps[i]["u18"], ust)
        lines.append(r)
        if arm == "base":
            specs[f"spec_{c['id']}"] = np.array(rec[i]["spec"])
            specs[f"std_{c['id']}"] = np.array(rec[i]["std"])
            specs[f"w0u_{c['id']}"] = w0u[i]
            specs[f"w0v_{c['id']}"] = w0v[i]
    if arm == "base":
        sp = Path(specdir) / f"{model}_{N}_{chunk}.npz"
        np.savez_compressed(sp, **specs)
        sh = hashlib.sha256(sp.read_bytes()).hexdigest()
        for r in lines:
            r["spec_file"], r["spec_sha256"] = sp.name, sh
    secs = time.time() - t0
    for r in lines:
        r["group_seconds"] = round(secs, 1)
    out_f.write_text("".join(json.dumps(r) + "\n" for r in lines))
    return str(out_f), secs


def main():
    cmd, outdir, specdir = sys.argv[1:4]
    arm = sys.argv[sys.argv.index("--arm") + 1] if "--arm" in sys.argv else "base"
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 3
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    Path(outdir).mkdir(parents=True, exist_ok=True)
    Path(specdir).mkdir(parents=True, exist_ok=True)
    cells = E.build(10)
    if arm == "grid2":
        cells = [c for c in cells if c["id"] % 10 == 0]
    groups = {}
    for c in cells:
        c["_T"] = horizon(c)
        NA = R.grid_for(c)[1]
        N = NA * (2 if arm == "grid2" else 1)
        groups.setdefault((c["model"], N), []).append(c)
    if only:
        m, n = only.split(":")
        groups = {k: v for k, v in groups.items() if k == (m, int(n))}
    CH = 48
    groups = {(m, n, j // CH): v[j:j + CH] for (m, n), v in groups.items() for j in range(0, len(v), CH)}
    # largest work first
    order = sorted(groups.items(), key=lambda kv: -sum(c["_T"] for c in kv[1]) * kv[0][1])
    jobs = [(k, v, arm, outdir, specdir) for k, v in order]
    t0 = time.time()
    with Pool(workers) as pool:
        for f, s in pool.imap_unordered(run_group, jobs):
            print(f"{time.time() - t0:8.1f}s done {f} ({s:.1f}s)", flush=True)
    print("ALL DONE", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
