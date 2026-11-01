"""J6: experiment design for M5: which looming protocol would discriminate the encoders (kappa / eta / theta) that J3 could not?

    python -m engineering.neuro.m5_design --out OUTDIR --j3 m5_mcell.json.gz [--trials 64] [--device cuda]

Takes the parameter sets that met J3's preregistered criteria C1-C3 (regenerated exactly from params(sets, seed), checked against
J3's sha256), and re-simulates them under candidate protocols:
  P_J3       onset 5 deg, l/v {10..240} ms (J3's protocol; reproduction control)
  P_onset2   onset 2 deg, same l/v (removes the 5 deg floor)
  P_wide     onset 2 deg, l/v {5, 10, 20, 40, 80, 160, 320, 500} ms
Per protocol and encoder: the response-angle-vs-l/v and latency-vs-l/v signatures of the consistent sets. Discriminability: a
nearest-centroid classifier on per-l/v mean response angles and log-latencies from n simulated fish (one parameter set per fish,
`trials` trials each). Accuracy vs n by Monte Carlo. Chance = 1/3. This sizes a real experiment; it is a simulation.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, math, os, sys, time
import numpy as np

from engineering.neuro import m5_mcell as M

PROTOCOLS = {"P_J3": (5.0, [0.010, 0.020, 0.040, 0.080, 0.120, 0.160, 0.240]),
             "P_onset2": (2.0, [0.010, 0.020, 0.040, 0.080, 0.120, 0.160, 0.240]),
             "P_wide": (2.0, [0.005, 0.010, 0.020, 0.040, 0.080, 0.160, 0.320, 0.500])}


def run_protocol(P, enc, theta0_deg, lvs, trials, dt, dev, seed):
    old = M.THETA0; M.THETA0 = math.radians(theta0_deg)
    try:
        out = {lv: M.run(P, enc, lv, trials, dt, dev, seed + j) for j, lv in enumerate(lvs)}
    finally:
        M.THETA0 = old
    ang = np.stack([np.degrees(np.nanmean(np.where(out[lv][0], out[lv][2], np.nan), 1)) for lv in lvs], 1)
    lat = np.stack([np.nanmean(np.where(out[lv][0], out[lv][1], np.nan), 1) + P["motor_s"] for lv in lvs], 1)
    p = np.stack([out[lv][0].mean(1) for lv in lvs], 1)
    return ang, lat, p


def classify(feats, n_fish, rng, reps=400):
    """feats[enc] = [sets, k] features of consistent sets. Draw n fish per encoder (sets with replacement), centroid from a disjoint
    training draw of 200 sets, classify each test fish by nearest standardized centroid. Returns accuracy."""
    encs = list(feats); allf = np.concatenate([f for f in feats.values()]); mu = np.nanmean(allf, 0); sd = np.nanstd(allf, 0) + 1e-9
    z = {e: np.nan_to_num((f - mu) / sd) for e, f in feats.items()}; acc = []
    for _ in range(reps):
        cent = {e: z[e][rng.integers(0, len(z[e]), 200)].mean(0) for e in encs}
        ok = 0; tot = 0
        for i, e in enumerate(encs):
            X = z[e][rng.integers(0, len(z[e]), n_fish)].mean(0)       # group mean over n fish of this (true) encoder
            pred = min(encs, key=lambda c: np.sum((X - cent[c]) ** 2)); ok += pred == e; tot += 1
        acc.append(ok / tot)
    return float(np.mean(acc))


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--j3", required=True)
    ap.add_argument("--trials", type=int, default=64); ap.add_argument("--dt", type=float, default=0.0005); ap.add_argument("--device", default=None)
    a = ap.parse_args(argv); t0 = time.time(); os.makedirs(a.out, exist_ok=True)
    import torch
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    J = json.load(gzip.open(a.j3, "rt")) if a.j3.endswith(".gz") else json.load(open(a.j3)); pr = J["params_regenerate"]
    P = M.params(pr["sets"], pr["seed"])
    sha = hashlib.sha256(np.stack([P[k] for k in M.RANGES]).astype("<f8").tobytes()).hexdigest()
    checks = [{"name": "control: J3 parameter sets regenerated exactly (sha256 of float64 array)", "pass": sha == pr["sha256_float64"], "detail": sha[:16]}]
    res = {"protocols": {k: {"theta0_deg": v[0], "lv_s": v[1]} for k, v in PROTOCOLS.items()}, "trials": a.trials, "device": dev, "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else None, "encoders": {}}
    feats = {pk: {} for pk in PROTOCOLS}
    for e in M.ENC:
        idx = np.array(J["encoders"][e]["per_set"]["C123"], dtype=int); Pe = {k: v[idx] for k, v in P.items()}
        res["encoders"][e] = {"n_consistent_sets": int(len(idx)), "protocols": {}}
        for pk, (th0, lvs) in PROTOCOLS.items():
            ang, lat, p = run_protocol(Pe, e, th0, lvs, a.trials, a.dt, dev, 7000 + 13 * len(pk))
            q = lambda X: [[float(np.nanpercentile(X[:, j], s)) if np.isfinite(X[:, j]).any() else None for s in (10, 50, 90)] for j in range(X.shape[1])]
            res["encoders"][e]["protocols"][pk] = {"angle_deg_q10_50_90": q(ang), "latency_s_q10_50_90": q(lat), "p_mean": [float(x) for x in np.nanmean(p, 0)],
                                                   "angle_slope_deg_per_log2_lv": float(np.nanmedian(np.polyfit(np.log2(lvs), np.nan_to_num(ang.T, nan=np.nanmean(ang)), 1)[0]))}
            feats[pk][e] = np.concatenate([ang, np.log(np.clip(lat, 1e-3, None))], 1)
            if pk == "P_J3":     # reproduction control: J3's mean response probability for these sets
                ps = J["encoders"][e]["per_set"]
                j3p = np.array(ps["p_mean_C123"], dtype=float) if "p_mean_C123" in ps else np.array(ps["p_mean"], dtype=float)[idx]
                res["encoders"][e]["p_mean_reproduction_abs_diff_median"] = float(np.nanmedian(np.abs(p.mean(1) - j3p)))
    checks.append({"name": "control: P_J3 reproduces J3's per-set mean response probability (median |diff| <= 0.06 with new noise draws)",
                   "pass": all(res["encoders"][e]["p_mean_reproduction_abs_diff_median"] <= 0.06 for e in M.ENC), "detail": {e: res["encoders"][e]["p_mean_reproduction_abs_diff_median"] for e in M.ENC}})
    rng = np.random.default_rng(20261101); res["discrimination_accuracy"] = {}
    for pk in PROTOCOLS:
        res["discrimination_accuracy"][pk] = {str(n): classify(feats[pk], n, rng) for n in (1, 2, 4, 8, 16, 32)}
    res["checks"] = checks; res["all_checks_pass"] = all(c["pass"] for c in checks); res["elapsed_s"] = time.time() - t0
    import scipy; res["env"] = {"python": sys.version.split()[0], "numpy": np.__version__, "torch": torch.__version__, "scipy": scipy.__version__}
    with gzip.open(os.path.join(a.out, "m5_design.json.gz"), "wt") as fh:
        json.dump(res, fh, default=lambda o: o.tolist() if hasattr(o, "tolist") else (o.item() if isinstance(o, np.generic) else str(o)))
    print(json.dumps({"checks": [(c["name"], c["pass"], c["detail"]) for c in checks], "accuracy": res["discrimination_accuracy"], "elapsed_s": res["elapsed_s"]}, default=str))
    return 0 if res["all_checks_pass"] else 3





def fair_main(argv=None):
    """J8: protocol-fair comparison. Fresh parameter sets (new seed); for EACH protocol the C1-C3 selection uses trials [0, T/2) and
    the classification features use the held-out trials [T/2, T), so no protocol is favoured by how the sets were chosen."""
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--sets", type=int, default=8192)
    ap.add_argument("--trials", type=int, default=32); ap.add_argument("--dt", type=float, default=0.0005); ap.add_argument("--seed", type=int, default=20261102)
    ap.add_argument("--device", default=None)
    a = ap.parse_args(argv); t0 = time.time(); os.makedirs(a.out, exist_ok=True)
    import torch
    from scipy.stats import spearmanr
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    P = M.params(a.sets, a.seed); h = a.trials // 2
    res = {"sets": a.sets, "trials": a.trials, "seed": a.seed, "protocols": {k: {"theta0_deg": v[0], "lv_s": v[1]} for k, v in PROTOCOLS.items()}, "device": dev,
           "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else None, "by_protocol": {}}
    rng = np.random.default_rng(a.seed)
    for pk, (th0, lvs) in PROTOCOLS.items():
        feats, sel = {}, {}
        for ei, e in enumerate(M.ENC):
            old = M.THETA0; M.THETA0 = math.radians(th0)
            try:
                out = {lv: M.run(P, e, lv, a.trials, a.dt, dev, a.seed + 100 * ei + j) for j, lv in enumerate(lvs)}
            finally:
                M.THETA0 = old
            def stats(sl):
                ang = np.stack([np.degrees(np.nanmean(np.where(out[lv][0][:, sl], out[lv][2][:, sl], np.nan), 1)) for lv in lvs], 1)
                lat = np.stack([np.nanmean(np.where(out[lv][0][:, sl], out[lv][1][:, sl], np.nan), 1) + P["motor_s"] for lv in lvs], 1)
                p = np.stack([out[lv][0][:, sl].mean(1) for lv in lvs], 1)
                return ang, lat, p
            with np.errstate(invalid="ignore", divide="ignore"):
                angA, latA, pA = stats(slice(0, h)); angB, latB, pB = stats(slice(h, a.trials))
            pm = pA.mean(1); rho = np.array([spearmanr(lvs, latA[i]).statistic if np.isfinite(latA[i]).all() else np.nan for i in range(len(pm))])
            ok = (pm >= 0.70) & (pm <= 0.91) & np.isfinite(angA[:, -1]) & np.isfinite(angA[:, 0]) & (np.abs(angA[:, -1] - angA[:, 0]) <= 10) & (np.nan_to_num(rho, nan=-1) >= 0.9)
            sel[e] = int(ok.sum()); feats[e] = np.concatenate([angB[ok], np.log(np.clip(latB[ok], 1e-3, None))], 1)
        usable = all(len(f) >= 20 for f in feats.values())
        res["by_protocol"][pk] = {"n_selected": sel, "accuracy": ({str(n): classify(feats, n, rng) for n in (1, 2, 4, 8, 16, 32)} if usable else None),
                                  "note": None if usable else "fewer than 20 selected sets for some encoder"}
    res["elapsed_s"] = time.time() - t0; res["checks"] = [{"name": "control: every protocol yields >= 20 selected sets per encoder", "pass": all(v["accuracy"] is not None for v in res["by_protocol"].values())}]
    res["all_checks_pass"] = res["checks"][0]["pass"]
    import scipy; res["env"] = {"python": sys.version.split()[0], "numpy": np.__version__, "torch": torch.__version__, "scipy": scipy.__version__}
    with gzip.open(os.path.join(a.out, "m5_design_fair.json.gz"), "wt") as fh:
        json.dump(res, fh, default=lambda o: o.tolist() if hasattr(o, "tolist") else (o.item() if isinstance(o, np.generic) else str(o)))
    print(json.dumps({k: v for k, v in res.items() if k in ("by_protocol", "elapsed_s", "checks")}, default=str))
    return 0 if res["all_checks_pass"] else 3


if __name__ == "__main__":
    sys.exit(fair_main(sys.argv[2:]) if len(sys.argv) > 1 and sys.argv[1] == "fair" else main())
