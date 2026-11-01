"""J2: M3 design-space atlas: nonlinear-saturation failure Monte Carlo on GPU (torch, float64) plus the exact linear-delay stability
atlas on the CPU pool, over every r3-daane airframe variant x sensing delay x sensor set x gust level.

    python -m engineering.neuro.m3_atlas --out OUTDIR [--geometry geometry.json] [--reference m3_mc_reference.json] [--n-mc 2048]

Plant, controller, sensors, gusts, noise and failure rule are exactly those of engineering.neuro.glide_stab (imported):
lateral airframes = mass {25, 50 g} x dihedral {0,2,4,7,10,12,14,16 deg} x caudal vertical-surface fraction {0.05..0.40};
longitudinal airframes = mass x static margin {-5..30 % MAC}. Sensor sets: lateral vision+canal, otolith+canal, canal rate only,
passive; longitudinal vision+canal, otolith+canal, passive. Delays: canal {0..80 ms}, vision {0..200 ms}. Gust sd {0.5, 1, 2} m/s.
Controls: (1) the GPU delay-buffer integrator reproduces the CPU closed-loop matrix power (no noise/gust); (2) GPU Monte Carlo
failure fractions agree with the committed CPU M3 run's 300-sample rows (two-proportion |z| < 3.5 for every comparable row);
(3) zero-gain linear radius equals the open-loop radius. SIMULATED; linear quasi-steady aerodynamics as in M3.
"""
from __future__ import annotations
import argparse, gzip, itertools, json, math, os, sys, time
from multiprocessing import Pool
import numpy as np

from engineering.neuro import glide_stab as G

DIH = [0, 2, 4, 7, 10, 12, 14, 16]; KV = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]; MASS = [0.025, 0.05]
SM = [-0.05, 0.0, 0.025, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30]
TC = [0.0, 0.01, 0.02, 0.03, 0.045, 0.06, 0.08]; TV = [0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.20]; GUST = [0.5, 1.0, 2.0]
LIN_TC = [round(0.01 * i, 3) for i in range(11)]; LIN_TV = [round(0.02 * i, 3) for i in range(11)]; LIN_GAIN = [0.3, 1.0, 3.0]
DEG = math.pi / 180


def airframes(g):
    lat, lon = [], []
    for m, dh, kv in itertools.product(MASS, DIH, KV):
        d = G.derivs(g, m=m, dihedral_deg=dh, k_v=kv); A, B, Bg, o = G.lat_ss(d); Ad, Bd, Bgd = G.disc(A, B, Bg)
        lat.append({"key": {"m": m, "dihedral": dh, "k_v": kv}, "Ad": Ad, "Bd": Bd, "Bgd": Bgd, "V": d["V"], "K": G.gains(B[1], G.W_ROLL),
                    "rows": {"vis": o["phi_vis"], "oto": o["phi_oto"], "rate": o["p_canal"]}, "att": 3, "fail": 45 * DEG, "noise": [2 * DEG, 5 * DEG],
                    "gust_scale": 1.0, "ol_max_real": float(np.max(np.linalg.eigvals(A).real))})
    for m, sm in itertools.product(MASS, SM):
        d = G.derivs(g, m=m, sm=sm); A, B, Bg, o = G.long_ss(d); Ad, Bd, Bgd = G.disc(A, B, Bg)
        lon.append({"key": {"m": m, "sm": sm}, "Ad": Ad, "Bd": Bd, "Bgd": Bgd, "V": d["V"], "K": G.gains(B[2], G.W_PITCH),
                    "rows": {"vis": o["theta_vis"], "oto": o["theta_oto"], "rate": o["q_canal"]}, "att": 3, "fail": 30 * DEG, "noise": [1 * DEG, 5 * DEG],
                    "gust_scale": 1.0, "ol_max_real": float(np.max(np.linalg.eigvals(A).real))})
    return lat, lon


def sensor_cases(lateral):
    """(name, attitude row key, gains multiplier [att, rate], delays (att, rate)) for each delay combination."""
    cases = [("vision", "vis", (1, 1), (tv, tc)) for tc in TC for tv in TV]
    cases += [("otolith", "oto", (1, 1), (tc, tc)) for tc in TC]
    if lateral:
        cases += [("rate_only", "vis", (0, 1), (0.0, tc)) for tc in TC]
    cases += [("passive", "vis", (0, 0), (0.0, 0.0))]
    return cases


def mc_gpu(frames, cases, n_mc, T, seed, device, chunk=1_500_000):
    import torch
    dt = G.DT; steps = int(round(T / dt)); a_act = math.exp(-dt / G.TAU_ACT)
    jobs = [(fi, ci, gi) for fi in range(len(frames)) for ci in range(len(cases)) for gi in range(len(GUST))]
    Ad = torch.tensor(np.stack([f["Ad"] for f in frames]), dtype=torch.float64, device=device)
    Bd = torch.tensor(np.stack([f["Bd"] for f in frames]), dtype=torch.float64, device=device)
    Bgd = torch.tensor(np.stack([f["Bgd"] for f in frames]), dtype=torch.float64, device=device)
    fail = np.zeros(len(jobs)); rms = np.full(len(jobs), np.nan)
    per = max(1, chunk // n_mc); gen = torch.Generator(device=device); gen.manual_seed(seed)
    Lmax = int(round(max(TV + TC) / dt)) + 1
    for s0 in range(0, len(jobs), per):
        J = jobs[s0:s0 + per]; nb = len(J) * n_mc
        fid = torch.tensor(np.repeat([j[0] for j in J], n_mc), device=device)
        rows, K, nd, noise, V, gs, att, flim = [], [], [], [], [], [], [], []
        for fi, ci, gi in J:
            f = frames[fi]; nm, rk, gm, dl = cases[ci]
            rows.append(np.stack([f["rows"][rk], f["rows"]["rate"]])); K.append(np.array(gm) * f["K"]); nd.append([int(round(x / dt)) for x in dl])
            noise.append(f["noise"]); V.append(f["V"]); gs.append(GUST[gi] * f["gust_scale"]); att.append(f["att"]); flim.append(f["fail"])
        rep = lambda a, dt_=torch.float64: torch.tensor(np.repeat(np.asarray(a), n_mc, axis=0), dtype=dt_, device=device)
        R = rep(rows); Kt = rep(K); ND = rep(nd, torch.long); NZ = rep(noise); Vt = rep(V); GS = rep(gs); ATT = rep(att, torch.long); FL = rep(flim)
        ag = torch.exp(-Vt * dt / 1.0); sg = GS * torch.sqrt(1 - ag * ag)
        n = Ad.shape[-1]; x = torch.zeros(nb, n, dtype=torch.float64, device=device); act = torch.zeros(nb, dtype=torch.float64, device=device)
        wg = torch.randn(nb, generator=gen, device=device, dtype=torch.float64) * GS
        buf = torch.zeros(Lmax, nb, 2, dtype=torch.float64, device=device); ar = torch.arange(nb, device=device)
        failed = torch.zeros(nb, dtype=torch.bool, device=device); sq = torch.zeros(nb, dtype=torch.float64, device=device)
        AdB, BdB, BgB = Ad[fid], Bd[fid], Bgd[fid]
        for k in range(steps):
            z = torch.cat([x, act[:, None]], 1)
            y = torch.einsum("bcj,bj->bc", R, z) + torch.randn(nb, 2, generator=gen, device=device, dtype=torch.float64) * NZ
            p = k % Lmax; buf[p] = y
            y0 = buf[(p - ND[:, 0]) % Lmax, ar, 0]; y1 = buf[(p - ND[:, 1]) % Lmax, ar, 1]
            ucmd = torch.clamp(-(Kt[:, 0] * y0 + Kt[:, 1] * y1), -G.SAT, G.SAT)
            act = a_act * act + (1 - a_act) * ucmd
            x = torch.einsum("bij,bj->bi", AdB, x) + BdB * act[:, None] + BgB * wg[:, None]
            wg = ag * wg + torch.randn(nb, generator=gen, device=device, dtype=torch.float64) * sg
            a_ = x[ar, ATT]; failed |= a_.abs() > FL; sq += torch.where(failed, torch.zeros_like(a_), a_ * a_); x[failed] = 0
        fz = failed.view(len(J), n_mc).double(); fail[s0:s0 + len(J)] = fz.mean(1).cpu().numpy()
        ok = (~failed).view(len(J), n_mc); sqv = (sq.view(len(J), n_mc) * ok).sum(1) / ok.sum(1).clamp(min=1) / steps
        rms[s0:s0 + len(J)] = torch.sqrt(sqv).cpu().numpy()
    return jobs, fail, rms


def gpu_vs_cpu_control(frame, device):
    """Deterministic: no noise, no gust, small initial state; GPU buffer integration vs CPU closed-loop matrix power."""
    import torch
    dl = (0.03, 0.01); rows = [frame["rows"]["vis"], frame["rows"]["rate"]]
    M = G.closed_loop(frame["Ad"], frame["Bd"], rows, frame["K"], list(dl)); z = np.zeros(M.shape[0]); z[1] = 0.01
    for _ in range(400):
        z = M @ z
    dt = G.DT; L = int(round(max(dl) / dt)) + 1; nd = [int(round(t / dt)) for t in dl]; a_act = math.exp(-dt / G.TAU_ACT)
    Ad = torch.tensor(frame["Ad"], dtype=torch.float64, device=device); Bd = torch.tensor(frame["Bd"], dtype=torch.float64, device=device)
    R = torch.tensor(np.stack(rows), dtype=torch.float64, device=device); K = torch.tensor(frame["K"], dtype=torch.float64, device=device)
    x = torch.zeros(4, dtype=torch.float64, device=device); x[1] = 0.01; act = torch.zeros((), dtype=torch.float64, device=device)
    buf = torch.zeros(L, 2, dtype=torch.float64, device=device)
    for k in range(400):
        y = R @ torch.cat([x, act[None]]); p = k % L; buf[p] = y
        u = -(K[0] * buf[(p - nd[0]) % L, 0] + K[1] * buf[(p - nd[1]) % L, 1])
        x_new = Ad @ x + Bd * act; act = a_act * act + (1 - a_act) * u; x = x_new
    err = float(np.max(np.abs(np.r_[x.cpu().numpy(), act.cpu().numpy()] - z[:5])))
    return {"name": "control: GPU delay-buffer integration equals CPU closed-loop matrix power (400 steps, 30/10 ms)", "pass": bool(err < 1e-12), "detail": err}


def lin_task(args):
    kind, fi, frame, sens, gm, tc, tv = args
    rows = [frame["rows"][sens], frame["rows"]["rate"]]; dl = [tv if sens == "vis" else tc, tc]
    return (kind, fi, sens, gm, tc, tv, G.radius(frame["Ad"], frame["Bd"], rows, gm * frame["K"], dl))


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--geometry"); ap.add_argument("--reference")
    ap.add_argument("--n-mc", type=int, default=2048); ap.add_argument("--T", type=float, default=G.T_MC); ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--procs", type=int, default=os.cpu_count() or 1); ap.add_argument("--device", default=None); ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(argv); t0 = time.time(); os.makedirs(a.out, exist_ok=True)
    import torch
    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    g = json.load(open(a.geometry))["geometry"] if a.geometry else G.geometry()
    global DIH, KV, SM, TC, TV, LIN_TC, LIN_TV
    if a.quick:
        DIH, KV, SM, TC, TV = [7], [0.15], [0.08], [0.01], [0.06]; LIN_TC, LIN_TV = [0.01], [0.06]
    lat, lon = airframes(g); checks = []
    base = next(i for i, f in enumerate(lat) if f["key"] == {"m": 0.025, "dihedral": 7, "k_v": 0.15})
    checks.append(gpu_vs_cpu_control(lat[base], device))
    zr = G.radius(lat[base]["Ad"], lat[base]["Bd"], [lat[base]["rows"]["vis"], lat[base]["rows"]["rate"]], 0 * lat[base]["K"], [0.0, 0.0])
    olr = max(np.max(np.abs(np.linalg.eigvals(lat[base]["Ad"]))), math.exp(-G.DT / G.TAU_ACT))
    checks.append({"name": "control: zero-gain linear radius equals open-loop radius", "pass": bool(abs(zr - olr) < 1e-9)})
    out = {"grids": {"dihedral": DIH, "k_v": KV, "mass": MASS, "sm": SM, "tc": TC, "tv": TV, "gust": GUST, "lin_tc": LIN_TC, "lin_tv": LIN_TV, "lin_gain": LIN_GAIN},
           "n_mc": a.n_mc, "T_s": a.T, "device": device, "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
           "airframes": {"lateral": [dict(f["key"], V=f["V"], ol_max_real=f["ol_max_real"]) for f in lat], "longitudinal": [dict(f["key"], V=f["V"], ol_max_real=f["ol_max_real"]) for f in lon]}}
    # Monte Carlo (GPU)
    tm = time.time(); mc = {}
    for kind, frames in (("lateral", lat), ("longitudinal", lon)):
        cases = sensor_cases(kind == "lateral")
        jobs, fail, rms = mc_gpu(frames, cases, a.n_mc, a.T, a.seed + (0 if kind == "lateral" else 1), device)
        mc[kind] = [{"airframe": fi, "sensor": cases[ci][0], "delay_att_s": cases[ci][3][0], "delay_rate_s": cases[ci][3][1], "gust_sd_ms": GUST[gi],
                     "fail_frac": float(fail[j]), "rms_att_rad": None if not np.isfinite(rms[j]) else float(rms[j])} for j, (fi, ci, gi) in enumerate(jobs)]
    out["mc"] = mc; out["mc_elapsed_s"] = time.time() - tm; out["mc_trajectories"] = sum(len(v) for v in mc.values()) * a.n_mc
    # agreement with the committed CPU Monte Carlo (300 samples per row)
    if a.reference:
        ref = json.load(open(a.reference)); zs = []
        def find(kind, fi, sensor, da, dr, gust):
            return next((r for r in mc[kind] if r["airframe"] == fi and r["sensor"] == sensor and abs(r["delay_att_s"] - da) < 1e-9 and abs(r["delay_rate_s"] - dr) < 1e-9 and r["gust_sd_ms"] == gust), None)
        lb = next(i for i, f in enumerate(lon) if f["key"] == {"m": 0.025, "sm": 0.08})
        for row in ref["rows"]:
            tv, gu = row["tau_vision_s"], row["gust_sd_ms"]
            for key, kind, fi, sensor, da, dr in (("roll_vision", "lateral", base, "vision", tv, 0.01), ("roll_otolith", "lateral", base, "otolith", 0.01, 0.01),
                                                  ("roll_rate_only", "lateral", base, "rate_only", 0.0, 0.01), ("roll_passive", "lateral", base, "passive", 0.0, 0.0),
                                                  ("pitch_vision", "longitudinal", lb, "vision", tv, 0.01), ("pitch_passive", "longitudinal", lb, "passive", 0.0, 0.0)):
                r = find(kind, fi, sensor, da, dr, gu)
                if r is None:
                    continue
                p1, n1, p2, n2 = row[key][0], 300, r["fail_frac"], a.n_mc; pp = (p1 * n1 + p2 * n2) / (n1 + n2)
                se = math.sqrt(max(pp * (1 - pp), 1e-12) * (1 / n1 + 1 / n2)); zs.append({"row": key, "tau_vision": tv, "gust": gu, "cpu": p1, "gpu": p2, "z": (p2 - p1) / se if se > 0 else 0.0})
        checks.append({"name": "control: GPU Monte Carlo agrees with the committed CPU M3 rows (two-proportion |z| < 3.5 on every comparable row)",
                       "pass": bool(zs) and all(abs(z["z"]) < 3.5 for z in zs), "detail": {"rows_compared": len(zs), "max_abs_z": max((abs(z["z"]) for z in zs), default=None), "rows": zs}})
    # exact linear atlas (CPU pool)
    tl = time.time()
    tasks = [("lateral", fi, f, s, gm, tc, tv) for fi, f in enumerate(lat) for s in ("vis", "oto") for gm in LIN_GAIN for tc in LIN_TC for tv in (LIN_TV if s == "vis" else [0.0])]
    tasks += [("longitudinal", fi, f, s, gm, tc, tv) for fi, f in enumerate(lon) for s in ("vis", "oto") for gm in LIN_GAIN for tc in LIN_TC for tv in (LIN_TV if s == "vis" else [0.0])]
    with Pool(a.procs) as p:
        lin = p.map(lin_task, tasks, chunksize=64)
    out["linear"] = [{"kind": k, "airframe": fi, "sensor": s, "gain": gm, "tc": tc, "tv": tv, "radius": r} for k, fi, s, gm, tc, tv, r in lin]
    out["linear_elapsed_s"] = time.time() - tl
    out["checks"] = checks; out["all_checks_pass"] = all(c["pass"] for c in checks); out["elapsed_s"] = time.time() - t0
    out["env"] = {"python": sys.version.split()[0], "numpy": np.__version__, "torch": torch.__version__, "cpu_count": os.cpu_count()}
    import scipy; out["env"]["scipy"] = scipy.__version__
    with gzip.open(os.path.join(a.out, "m3_atlas.json.gz"), "wt") as fh:
        json.dump(out, fh, default=lambda o: o.tolist() if hasattr(o, "tolist") else (o.item() if isinstance(o, np.generic) else str(o)))
    print(json.dumps(default=str, obj={"checks": [(c["name"], c["pass"], c.get("detail") if not isinstance(c.get("detail"), dict) else {k: v for k, v in c["detail"].items() if k != "rows"}) for c in checks],
                      "mc_trajectories": out["mc_trajectories"], "mc_elapsed_s": out["mc_elapsed_s"], "linear_elapsed_s": out["linear_elapsed_s"]}))
    return 0 if out["all_checks_pass"] else 3


if __name__ == "__main__":
    sys.exit(main())
