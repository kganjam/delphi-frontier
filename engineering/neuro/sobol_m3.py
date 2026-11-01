"""J4: global (Sobol/Saltelli) sensitivity of glide ROLL stabilisation (M3 lateral loop): which design, neural, muscle and
environment parameters decide whether the r3-daane glider stays upright?

    python -m engineering.neuro.sobol_m3 --out OUTDIR [--N 2048] [--trials 128] [--procs 16] [--device cuda]

14 inputs (uniform, or log-uniform where marked): dihedral 0-16 deg; caudal vertical-surface fraction k_v 0.05-0.40; mass 25-50 g;
trim CL 0.4-0.9; vision bank delay 0-200 ms; canal rate delay 0-80 ms; attitude gain x0.1-3 (log); rate gain x0.1-3 (log);
fin actuator lag 5-50 ms (log); fin authority 5-25 deg; gust sd 0.5-2 m/s; attitude noise 0.5-4 deg; rate noise 2-10 deg/s;
Dryden gust length 0.5-3 m. Gains multiply the M3 nominal PD gains (w 10 rad/s, zeta 0.7) of each airframe.
Outputs: P(|bank| > 45 deg within 5 s) from `trials` saturation Monte Carlo trajectories per point (GPU, float64), and the exact
linear delayed spectral radius (CPU pool; stable if < 1). Plant, sensors and controller: engineering.neuro.glide_stab, vision + canal set.
Controls: Ishigami analytic indices (reused from sobol_m1); the batched integrator reproduces glide_stab.closed_loop matrix power
for one point; Monte-Carlo noise share of the failure variance is reported (binomial variance / total variance).
SIMULATED; ranks the model's own priors.
"""
from __future__ import annotations
import argparse, gzip, json, math, os, sys, time
from multiprocessing import Pool
import numpy as np

from engineering.neuro import glide_stab as G
from engineering.neuro.sobol_core import saltelli, indices, ishigami_control

DEG = math.pi / 180
IN = {"dihedral_deg": (0, 16, "lin"), "k_v": (0.05, 0.40, "lin"), "mass_kg": (0.025, 0.05, "lin"), "CL_trim": (0.4, 0.9, "lin"),
      "tau_vision_s": (0.0, 0.2, "lin"), "tau_canal_s": (0.0, 0.08, "lin"), "gain_att": (0.1, 3.0, "log"), "gain_rate": (0.1, 3.0, "log"),
      "tau_act_s": (0.005, 0.05, "log"), "sat_deg": (5, 25, "lin"), "gust_sd_ms": (0.5, 2.0, "lin"), "noise_att_deg": (0.5, 4.0, "lin"),
      "noise_rate_dps": (2, 10, "lin"), "gust_L_m": (0.5, 3.0, "lin")}
NAMES = list(IN)


def to_vals(U):
    v = {}
    for j, (k, (lo, hi, kind)) in enumerate(IN.items()):
        v[k] = lo + (hi - lo) * U[:, j] if kind == "lin" else np.exp(np.log(lo) + (np.log(hi) - np.log(lo)) * U[:, j])
    return v


def plant(args):
    g, dh, kv, m, cl = args
    d = G.derivs(g, m=m, dihedral_deg=dh, k_v=kv, CL=cl); A, B, Bg, o = G.lat_ss(d); Ad, Bd, Bgd = G.disc(A, B, Bg)
    return Ad, Bd, Bgd, G.gains(B[1], G.W_ROLL), d["V"]


def lin_radius(args):
    Ad, Bd, K, ga, gr, tv, tc, ta = args
    o = np.r_[0, 0, 0, 1, 0.0], np.r_[0, 1, 0, 0, 0.0]
    return G.radius(Ad, Bd, list(o), np.array([ga * K[0], gr * K[1]]), [tv, tc], tau_act=ta)


def mc(P, v, trials, T, seed, device, chunk=1_200_000):
    import torch
    dt = G.DT; steps = int(round(T / dt)); n = len(P); fails = np.zeros(n)
    per = max(1, chunk // trials); gen = torch.Generator(device=device); gen.manual_seed(seed)
    L = int(round(max(v["tau_vision_s"].max(), v["tau_canal_s"].max()) / dt)) + 1
    for s0 in range(0, n, per):
        idx = np.arange(s0, min(n, s0 + per)); nb = len(idx) * trials
        rep = lambda a: torch.tensor(np.repeat(np.asarray(a)[idx], trials, axis=0), dtype=torch.float64, device=device)
        Ad = rep(np.stack([p[0] for p in P])); Bd = rep(np.stack([p[1] for p in P])); Bgd = rep(np.stack([p[2] for p in P]))
        K0 = rep(np.array([p[3][0] for p in P]) * v["gain_att"]); K1 = rep(np.array([p[3][1] for p in P]) * v["gain_rate"])
        Vv = rep(np.array([p[4] for p in P])); ndv = rep(np.round(v["tau_vision_s"] / dt)).long(); ndc = rep(np.round(v["tau_canal_s"] / dt)).long()
        aa = torch.exp(-dt / rep(v["tau_act_s"])); sat = rep(v["sat_deg"] * DEG); gs = rep(v["gust_sd_ms"]); Lg = rep(v["gust_L_m"])
        na = rep(v["noise_att_deg"] * DEG); nr = rep(v["noise_rate_dps"] * DEG)
        ag = torch.exp(-Vv * dt / Lg); sg = gs * torch.sqrt(1 - ag * ag)
        x = torch.zeros(nb, 4, dtype=torch.float64, device=device); act = torch.zeros(nb, dtype=torch.float64, device=device)
        wg = torch.randn(nb, generator=gen, device=device, dtype=torch.float64) * gs
        buf = torch.zeros(L, nb, 2, dtype=torch.float64, device=device); ar = torch.arange(nb, device=device); failed = torch.zeros(nb, dtype=torch.bool, device=device)
        for k in range(steps):
            y = torch.stack([x[:, 3] + na * torch.randn(nb, generator=gen, device=device, dtype=torch.float64),
                             x[:, 1] + nr * torch.randn(nb, generator=gen, device=device, dtype=torch.float64)], 1)
            p = k % L; buf[p] = y
            u = torch.clamp(-(K0 * buf[(p - ndv) % L, ar, 0] + K1 * buf[(p - ndc) % L, ar, 1]), -sat, sat)
            xn = torch.einsum("bij,bj->bi", Ad, x) + Bd * act[:, None] + Bgd * wg[:, None]
            act = aa * act + (1 - aa) * u; x = xn
            wg = ag * wg + torch.randn(nb, generator=gen, device=device, dtype=torch.float64) * sg
            failed |= x[:, 3].abs() > 45 * DEG; x[failed] = 0
        fails[idx] = failed.view(len(idx), trials).double().mean(1).cpu().numpy()
    return fails


def integrator_control(g, device):
    """One point, no noise/gust/saturation reach: batched loop above (same update order) vs glide_stab.closed_loop matrix power."""
    import torch
    Ad, Bd, Bgd, K, V = plant((g, 7.0, 0.15, 0.025, 0.6)); tv, tc, ta = 0.03, 0.01, 0.02
    rows = [np.r_[0, 0, 0, 1, 0.0], np.r_[0, 1, 0, 0, 0.0]]
    M = G.closed_loop(Ad, Bd, rows, K, [tv, tc], tau_act=ta); z = np.zeros(M.shape[0]); z[1] = 0.01
    for _ in range(300):
        z = M @ z
    dt = G.DT; L = int(round(max(tv, tc) / dt)) + 1; nv, nc = int(round(tv / dt)), int(round(tc / dt)); aa = math.exp(-dt / ta)
    x = np.zeros(4); x[1] = 0.01; act = 0.0; buf = np.zeros((L, 2))
    for k in range(300):
        p = k % L; buf[p] = [x[3], x[1]]
        u = -(K[0] * buf[(p - nv) % L, 0] + K[1] * buf[(p - nc) % L, 1])
        xn = Ad @ x + Bd * act; act = aa * act + (1 - aa) * u; x = xn
    err = float(np.max(np.abs(np.r_[x, act] - z[:5])))
    return {"name": "control: batched-loop update order reproduces glide_stab.closed_loop matrix power (300 steps)", "pass": err < 1e-12, "detail": err}


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--N", type=int, default=2048)
    ap.add_argument("--trials", type=int, default=128); ap.add_argument("--T", type=float, default=5.0); ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--procs", type=int, default=os.cpu_count() or 1); ap.add_argument("--device", default=None); ap.add_argument("--geometry")
    a = ap.parse_args(argv); t0 = time.time(); os.makedirs(a.out, exist_ok=True)
    import torch
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    g = json.load(open(a.geometry))["geometry"] if a.geometry else G.geometry()
    checks = [ishigami_control(a.seed), integrator_control(g, dev)]
    d = len(NAMES); A, B, AB = saltelli(a.N, d, a.seed)
    M = np.concatenate([A, B] + [AB[j] for j in range(d)]); v = to_vals(M)
    tp = time.time()
    with Pool(a.procs) as p:
        P = p.map(plant, [(g, v["dihedral_deg"][i], v["k_v"][i], v["mass_kg"][i], v["CL_trim"][i]) for i in range(len(M))], chunksize=256)
        R = np.array(p.map(lin_radius, [(P[i][0], P[i][1], P[i][3], v["gain_att"][i], v["gain_rate"][i], v["tau_vision_s"][i], v["tau_canal_s"][i], v["tau_act_s"][i]) for i in range(len(M))], chunksize=64))
    t_lin = time.time() - tp; tm = time.time()
    F = mc(P, v, a.trials, a.T, a.seed, dev); t_mc = time.time() - tm
    res = {"inputs": IN, "N": a.N, "d": d, "points": len(M), "trials": a.trials, "T_s": a.T, "device": dev, "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else None,
           "elapsed": {"linear_s": t_lin, "mc_s": t_mc}, "outputs": {}}
    rng = np.random.default_rng(a.seed)
    for name, y in (("fail_prob", F), ("linear_unstable", (R >= 1).astype(float)), ("log_radius", np.log(R))):
        fA, fB = y[:a.N], y[a.N:2 * a.N]; fAB = y[2 * a.N:].reshape(d, a.N).T
        r = indices(fA, fB, fAB, rng)
        o = {"mean": float(np.mean(np.r_[fA, fB])), "variance": float(r["var"]), "S1": dict(zip(NAMES, r["S1"].tolist())), "ST": dict(zip(NAMES, r["ST"].tolist())),
             "S1_ci95": dict(zip(NAMES, r["S1_ci95"].tolist())), "ST_ci95": dict(zip(NAMES, r["ST_ci95"].tolist()))}
        if name == "fail_prob":
            o["mc_noise_share_of_variance"] = float(np.mean(y * (1 - y) / a.trials) / max(r["var"], 1e-12))
        res["outputs"][name] = o
    agree = float(np.mean((R[:2 * a.N] < 1) == (F[:2 * a.N] < 0.5)))
    res["linear_vs_mc_agreement"] = {"fraction_where_linear_stable_iff_fail_prob_below_0.5": agree}
    res["checks"] = checks; res["all_checks_pass"] = all(c["pass"] for c in checks); res["elapsed_s"] = time.time() - t0
    import scipy; res["env"] = {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__, "torch": torch.__version__, "cpu_count": os.cpu_count()}
    res["points_head"] = {"fail_prob": [float(f"{x:.4g}") for x in F[:2 * a.N]], "radius": [float(f"{x:.6g}") for x in R[:2 * a.N]]}
    with gzip.open(os.path.join(a.out, "sobol_m3.json.gz"), "wt") as fh:
        json.dump(res, fh, default=lambda o: o.tolist() if hasattr(o, "tolist") else (o.item() if isinstance(o, np.generic) else str(o)))
    print(json.dumps({"checks": [(c["name"], c["pass"]) for c in checks], "elapsed": res["elapsed"], "fail_mean": res["outputs"]["fail_prob"]["mean"]}, default=str))
    return 0 if res["all_checks_pass"] else 3


if __name__ == "__main__":
    sys.exit(main())
