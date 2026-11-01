"""M5 (job J3): a spiking Mauthner-cell decision model for looming stimuli: which visual encoding plus feedforward inhibition
reproduces the measured signatures of looming escapes, and what threshold angle / latency does it predict for M1?

    python -m engineering.neuro.m5_mcell --out OUTDIR [--sets 16384] [--trials 32] [--device cuda]

Stimulus: an object of half-size l approaching at speed v; angular size theta(t) = 2 atan(l / (v (t_c - t))), shown from
theta0 = 5 deg until collision; approach parameter l/v in {10, 20, 40, 80, 120, 160, 240} ms.
Encoders (drive d(t) fed to the M-cell, delayed by a visual delay delta):
  kappa  d = theta(t-delta) exp(-beta theta(t-delta))                 (Preuss et al. 2006 J Neurosci, abstract form)
  eta    d = theta_dot(t-delta) exp(-beta theta(t-delta))             (LGMD eta function: Hatsopoulos 1995; Gabbiani 2002)
  theta  d = theta(t-delta)                                            (pure angular-size drive)
M-cell: leaky integrate-and-fire with feedforward inhibition, exact exponential update at dt:
  tau_m dV/dt = -V + g_E d(t) - g_I I(t) + sigma sqrt(tau_m) xi(t),   tau_I dI/dt = d(t) - I,   spike when V >= 1.
Escape = first spike before collision (dt 0.5 ms: at 2 ms the response angle was not dt-converged near collision); latency = spike time from looming onset + motor delay (5-10 ms).
Preregistered consistency criteria (fixed in code before any cloud run; sources abstract-verified, see sources.json):
  C1 mean response probability over l/v in [0.70, 0.91]                         (Preuss 2006)
  C2 response angle invariant to approach rate: |theta_resp(240 ms) - theta_resp(10 ms)| <= 10 deg (Bhattacharyya 2017; Temizer 2015)
  C3 latency increases with l/v (Spearman rho >= 0.9 over the 7 l/v values)      (Bhattacharyya 2017: slower approach, longer latency)
  C4 (loose; stimulus set differs from Preuss's) mean latency from onset in [142, 716] ms
Controls: analytic threshold angle for the noise-free, inhibition-free theta encoder with fast membrane; dt halving on a subset;
CPU-vs-device agreement on a noise-free subset. SIMULATED; a reduced neuron, not the goldfish/zebrafish circuit.
"""
from __future__ import annotations
import argparse, gzip, json, math, os, sys, time
import numpy as np

LV = [0.010, 0.020, 0.040, 0.080, 0.120, 0.160, 0.240]
THETA0 = math.radians(5.0)
ENC = ["kappa", "eta", "theta"]
RANGES = {"delta_s": (0.02, 0.08, "lin"), "beta_per_rad": (0.5, 8.0, "lin"), "gE": (0.1, 100.0, "log"), "gI_over_gE": (0.0, 1.5, "lin"),
          "tauI_s": (0.005, 0.1, "log"), "taum_s": (0.002, 0.02, "log"), "sigma": (0.0, 1.0, "lin"), "motor_s": (0.005, 0.010, "lin")}
BASIS = {"delta_s": "assumption: retina-to-tectum-to-M-cell visual delay", "beta_per_rad": "assumption: exponential angle factor (Preuss/Gabbiani forms)",
         "gE": "assumption: excitatory gain (threshold = 1)", "gI_over_gE": "assumption: feedforward inhibition ratio", "tauI_s": "assumption",
         "taum_s": "assumption: M-cell membrane time constant", "sigma": "assumption: membrane noise (units of threshold)", "motor_s": "domenici_blake1997 recalled (M-cell to muscle)"}
SCALE_ETA = 0.05   # s: eta drive (rad/s) times this to give it the same order as theta (rad); absorbed in gE, stated for transparency


def params(n, seed):
    from scipy.stats import qmc
    U = qmc.Sobol(d=len(RANGES), scramble=True, seed=seed).random(n)
    P = {}
    for j, (k, (lo, hi, kind)) in enumerate(RANGES.items()):
        P[k] = lo + (hi - lo) * U[:, j] if kind == "lin" else np.exp(np.log(lo) + (np.log(hi) - np.log(lo)) * U[:, j])
    return P


def run(P, enc, lv, trials, dt, device, seed, noise=True):
    """All parameter sets x trials for one encoder and one l/v. Returns (spiked, t_spike_from_onset, theta_at_spike) [sets, trials]."""
    import torch
    t_c = lv / math.tan(THETA0 / 2)                     # collision time measured from onset (theta(0) = theta0)
    steps = int(math.ceil(t_c / dt)); S = len(P["gE"])
    tt = lambda k: torch.tensor(np.repeat(P[k], trials), dtype=torch.float32, device=device)
    dl, be, gE, gI, tI, tm, sg = tt("delta_s"), tt("beta_per_rad"), tt("gE"), tt("gI_over_gE") * tt("gE"), tt("tauI_s"), tt("taum_s"), tt("sigma")
    nb = S * trials; V = torch.zeros(nb, device=device); I = torch.zeros(nb, device=device)
    spk = torch.zeros(nb, dtype=torch.bool, device=device); tsp = torch.full((nb,), float("nan"), device=device); thsp = torch.full((nb,), float("nan"), device=device)
    am, ai = torch.exp(-dt / tm), torch.exp(-dt / tI)
    gen = torch.Generator(device=device); gen.manual_seed(seed)
    nsd = sg * torch.sqrt((1 - am * am) / 2.0)          # exact OU increment for unit-variance-per-sqrt(tau) noise
    for k in range(steps):
        t = k * dt; td = torch.clamp(t - dl, min=0.0)
        rem = torch.clamp(t_c - td, min=1e-6)
        th = 2 * torch.atan(lv / rem)
        if enc == "kappa":
            d = th * torch.exp(-be * th)
        elif enc == "eta":
            thd = 2 * lv / (rem * rem + lv * lv)            # d theta / dt
            d = SCALE_ETA * thd * torch.exp(-be * th)
        else:
            d = th
        d = torch.where(t - dl < 0, torch.zeros_like(d), d)
        I = ai * I + (1 - ai) * d
        V = am * V + (1 - am) * (gE * d - gI * I)
        if noise:
            V = V + nsd * torch.randn(nb, generator=gen, device=device)
        new = (V >= 1.0) & ~spk
        if new.any():
            th_now = 2 * math.atan(lv / max(t_c - t, 1e-6))
            tsp = torch.where(new, torch.full_like(tsp, t), tsp); thsp = torch.where(new, torch.full_like(thsp, th_now), thsp); spk |= new
    return (spk.view(S, trials).cpu().numpy(), tsp.view(S, trials).cpu().numpy(), thsp.view(S, trials).cpu().numpy())


def summarise(P, res, trials):
    """res[lv] = (spk, tsp, thsp). Per parameter set: p per l/v, mean latency (incl. motor delay), mean response angle."""
    S = len(P["gE"]); p = np.zeros((S, len(LV))); lat = np.full((S, len(LV)), np.nan); ang = np.full((S, len(LV)), np.nan)
    for j, lv in enumerate(LV):
        spk, tsp, thsp = res[lv]
        p[:, j] = spk.mean(1)
        with np.errstate(invalid="ignore"):
            lat[:, j] = np.nanmean(np.where(spk, tsp, np.nan), 1) + P["motor_s"]
            ang[:, j] = np.degrees(np.nanmean(np.where(spk, thsp, np.nan), 1))
    pm = p.mean(1)
    from scipy.stats import spearmanr
    rho = np.array([spearmanr(LV, lat[i]).statistic if np.isfinite(lat[i]).sum() == len(LV) else np.nan for i in range(S)])
    C1 = (pm >= 0.70) & (pm <= 0.91)
    C2 = np.isfinite(ang[:, -1]) & np.isfinite(ang[:, 0]) & (np.abs(ang[:, -1] - ang[:, 0]) <= 10.0)
    C3 = np.nan_to_num(rho, nan=-1) >= 0.9
    C4 = (np.nanmean(lat, 1) >= 0.142) & (np.nanmean(lat, 1) <= 0.716)
    return {"p": p, "lat": lat, "ang": ang, "rho": rho, "C1": C1, "C2": C2, "C3": C3, "C4": C4, "C123": C1 & C2 & C3, "C1234": C1 & C2 & C3 & C4}


def q(a):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return {f"q{p}": float(np.percentile(a, p)) for p in (5, 25, 50, 75, 95)} | {"n": int(a.size)} if a.size else {"n": 0}


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--sets", type=int, default=16384)
    ap.add_argument("--trials", type=int, default=32); ap.add_argument("--dt", type=float, default=0.0005); ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--device", default=None)
    a = ap.parse_args(argv); t0 = time.time(); os.makedirs(a.out, exist_ok=True)
    import torch
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    checks = []
    # control 1: analytic threshold angle (theta encoder, no noise/inhibition, fast membrane, no delay): spike when gE theta = 1
    Pc = {k: np.full(4, v) for k, v in {"delta_s": 0.0, "beta_per_rad": 1.0, "gI_over_gE": 0.0, "tauI_s": 0.01, "taum_s": 1e-4, "sigma": 0.0, "motor_s": 0.0}.items()}
    Pc["gE"] = np.array([2.0, 3.0, 4.0, 6.0]); Pc["delta_s"] = np.full(4, 0.0)
    spk, tsp, thsp = run(Pc, "theta", 0.08, 1, 1e-4, dev, 0, noise=False)
    want = np.degrees(1 / Pc["gE"]); got = np.degrees(thsp[:, 0])
    checks.append({"name": "control: noise-free theta encoder spikes at theta = 1/gE (fast membrane, no inhibition), within 0.2 deg",
                   "pass": bool(np.all(np.abs(got - want) < 0.2)), "detail": {"want_deg": want.tolist(), "got_deg": got.tolist()}})
    # control 2: dt halving on 512 sets (noise-free) for each encoder
    Ps = params(512, a.seed + 99); dd = {}
    for enc in ENC:
        r1 = run(Ps, enc, 0.08, 1, a.dt, dev, 1, noise=False); r2 = run(Ps, enc, 0.08, 1, a.dt / 2, dev, 1, noise=False)
        both = r1[0][:, 0] & r2[0][:, 0]; agree = float(np.mean(r1[0][:, 0] == r2[0][:, 0]))
        da = np.abs(np.degrees(r1[2][both, 0] - r2[2][both, 0])) if both.any() else np.zeros(1)
        dd[enc] = {"spike_agreement": agree, "p99_angle_diff_deg": float(np.percentile(da, 99)), "max_angle_diff_deg": float(da.max())}
    checks.append({"name": "control: dt halving (noise-free, l/v 80 ms): spike/no-spike agreement >= 0.99 and 99th-percentile angle difference <= 1 deg, every encoder",
                   "pass": all(v["spike_agreement"] >= 0.99 and v["p99_angle_diff_deg"] <= 1.0 for v in dd.values()), "detail": dd})
    # control 3: device vs CPU on 256 noise-free sets
    if dev != "cpu":
        Pk = params(256, a.seed + 7); rc = run(Pk, "kappa", 0.04, 1, a.dt, "cpu", 2, noise=False); rg = run(Pk, "kappa", 0.04, 1, a.dt, dev, 2, noise=False)
        agree = float(np.mean(rc[0] == rg[0])); both = rc[0][:, 0] & rg[0][:, 0]
        dang = float(np.nanmax(np.abs(np.degrees(rc[2][both, 0] - rg[2][both, 0])))) if both.any() else 0.0
        checks.append({"name": "control: device and CPU agree on 256 noise-free kappa sets (spike agreement >= 0.99, angle within 0.5 deg)", "pass": agree >= 0.99 and dang <= 0.5, "detail": [agree, dang]})
    # main sweep
    out = {"lv_s": LV, "theta0_deg": math.degrees(THETA0), "ranges": {k: list(v[:2]) + [v[2]] for k, v in RANGES.items()}, "basis": BASIS, "sets": a.sets, "trials": a.trials,
           "dt": a.dt, "device": dev, "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else None, "encoders": {}}
    P = params(a.sets, a.seed); ts = time.time()
    for ei, enc in enumerate(ENC):
        res = {lv: run(P, enc, lv, a.trials, a.dt, dev, a.seed + 1000 * ei + j) for j, lv in enumerate(LV)}
        sm = summarise(P, res, a.trials)
        ok = sm["C123"]; ok4 = sm["C1234"]
        e = {"fraction": {c: float(sm[c].mean()) for c in ("C1", "C2", "C3", "C4", "C123", "C1234")},
             "n_consistent_C123": int(ok.sum()), "n_consistent_C1234": int(ok4.sum()),
             "consistent_response_angle_deg": q(sm["ang"][ok].ravel()), "consistent_latency_s_by_lv": {str(lv): q(sm["lat"][ok, j]) for j, lv in enumerate(LV)},
             "consistent_params": {k: q(P[k][ok]) for k in RANGES}, "all_params_marginal_pass_rate": {}}
        for k in RANGES:   # where in each parameter's range do consistent sets lie (10 bins)
            edges = np.quantile(P[k], np.linspace(0, 1, 11)); idx = np.clip(np.searchsorted(edges, P[k], side="right") - 1, 0, 9)
            e["all_params_marginal_pass_rate"][k] = {"bin_edges": edges.tolist(), "C123_rate": [float(ok[idx == b].mean()) if (idx == b).any() else None for b in range(10)]}
        e["per_set"] = {"p_mean": sm["p"].mean(1).astype(np.float32).tolist(), "ang_lv10": sm["ang"][:, 0].astype(np.float32).tolist(), "ang_lv240": sm["ang"][:, -1].astype(np.float32).tolist(),
                        "rho": sm["rho"].astype(np.float32).tolist(), "lat_mean": np.nanmean(sm["lat"], 1).astype(np.float32).tolist()}
        out["encoders"][enc] = e
    out["params"] = {k: v.astype(np.float32).tolist() for k, v in P.items()}
    out["sweep_elapsed_s"] = time.time() - ts; out["checks"] = checks; out["all_checks_pass"] = all(c["pass"] for c in checks); out["elapsed_s"] = time.time() - t0
    import scipy; out["env"] = {"python": sys.version.split()[0], "numpy": np.__version__, "torch": torch.__version__, "scipy": scipy.__version__}
    with gzip.open(os.path.join(a.out, "m5_mcell.json.gz"), "wt") as fh:
        json.dump(out, fh, default=lambda o: o.tolist() if hasattr(o, "tolist") else (o.item() if isinstance(o, np.generic) else str(o)))
    print(json.dumps({"checks": [(c["name"], c["pass"]) for c in checks], "fractions": {k: v["fraction"] for k, v in out["encoders"].items()}, "sweep_elapsed_s": out["sweep_elapsed_s"]}, default=str))
    return 0 if out["all_checks_pass"] else 3


if __name__ == "__main__":
    sys.exit(main())
