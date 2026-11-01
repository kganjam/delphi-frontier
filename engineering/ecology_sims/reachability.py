"""Reachability of an exocoetid-like glider from a halfbeak-like ancestor on a model escape-fitness landscape.

Three readings of one landscape W(p, A, M, c) = escape probability per attack (common.escape_prob of the glide from common.launch_and_glide):
  1. accessibility: on a 4-D grid with single-trait one-cell steps, the maximin path (the path whose worst step is least bad)
     from the ancestor cell to the target cell. worst step > 0: a strictly improving path exists; ~0: only through neutral
     steps (drift needed); < 0: every path crosses a valley at least that deep.
  2. Lande walk: dz/dt = G grad ln W, G = diag((CV_A z)^2) for A and M (mean-standardised) and (CV_A * range)^2 for p, c;
     run from the ancestor; where it ends and where it is slowest (the bottleneck).
  3. the straight line ancestor -> target, evaluated directly (not on the grid): largest drop.
A model of reachability is not evidence that the transition happened, nor of how.
"""
from __future__ import annotations

import argparse
import heapq
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engineering.ecology_sims import common as C  # noqa: E402

TRAITS = ["p", "A", "M", "c"]


def grids(P):
    a, t = C.ancestor_phenotype(P), C.target_phenotype(P)
    g = {"p": np.linspace(0.10, P["p_max"], 24), "A": np.geomspace(1.0, 14.0, 18), "M": np.geomspace(0.010, 0.060, 10), "c": np.linspace(0.45, 0.70, 11)}
    for k in TRAITS:  # make the anchors exact grid nodes
        g[k] = np.unique(np.r_[g[k], a[k], t[k]])
    return g, a, t


def landscape(P, dt):
    g, a, t = grids(P)
    mesh = np.meshgrid(*[g[k] for k in TRAITS], indexing="ij")
    r = C.launch_and_glide(*mesh, P, dt=dt)
    return g, a, t, r


def idx(g, z):
    return tuple(int(np.argmin(np.abs(g[k] - z[k]))) for k in TRAITS)


def maximin_path(W, start, goal, tol):
    """Widest-path Dijkstra: maximise the minimum step gain dW over single-axis +-1 moves. Returns (bottleneck, path)."""
    shape = W.shape
    best = np.full(shape, -np.inf)
    prev = {}
    best[start] = np.inf
    h = [(-np.inf, start)]
    while h:
        nb, u = heapq.heappop(h)
        b = -nb
        if b < best[u]:
            continue
        if u == goal:
            break
        for ax in range(4):
            for s in (-1, 1):
                v = list(u); v[ax] += s; v = tuple(v)
                if not (0 <= v[ax] < shape[ax]):
                    continue
                gain = W[v] - W[u]
                gain = 0.0 if abs(gain) <= tol else gain
                nbv = min(b, gain)
                if nbv > best[v]:
                    best[v] = nbv; prev[v] = u
                    heapq.heappush(h, (-nbv, v))
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return float(best[goal]), path[::-1]


def lande_walk(g, lnW, a, t, cv, gens, P, r_pc=0.0):
    from scipy.interpolate import RegularGridInterpolator
    # coordinates: x = (p, ln A, ln M, c)
    axes = [g["p"], np.log(g["A"]), np.log(g["M"]), g["c"]]
    f = RegularGridInterpolator(axes, lnW, bounds_error=False, fill_value=None)
    lo = np.array([ax[0] for ax in axes]); hi = np.array([ax[-1] for ax in axes])
    scale = np.array([cv * (g["p"][-1] - g["p"][0]), cv, cv, cv * (g["c"][-1] - g["c"][0])])  # sqrt(G) per axis
    x = np.array([a["p"], math.log(a["A"]), math.log(a["M"]), a["c"]])
    xt = np.array([t["p"], math.log(t["A"]), math.log(t["M"]), t["c"]])
    eps = np.array([0.004, 0.01, 0.01, 0.004])
    traj = [x.copy()]; gradn = []
    E = np.eye(4) * eps
    Rm = np.eye(4); Rm[0, 3] = Rm[3, 0] = r_pc          # optional genetic correlation between p and c (pleiotropy case)
    Gm = np.diag(scale) @ Rm @ np.diag(scale)
    for k in range(gens):
        v = f(np.vstack([x + E, x - E]))
        gr = (v[:4] - v[4:]) / (2 * eps)
        dx = Gm @ gr
        x = np.clip(x + dx, lo, hi)
        traj.append(x.copy()); gradn.append(float(np.linalg.norm(dx / scale)))
    traj = np.array(traj)
    norm = (traj - xt) / (hi - lo)
    dist = np.linalg.norm(norm, axis=1)
    return traj, np.array(gradn), dist


def analyse(g, a, t, r, P, hyp, cv, gens, r_pc=0.0):
    W = C.fitness(r, P, h_vis=hyp in ("vis", "both"), h_chase=hyp in ("chase", "both"))
    valid = (r["end_reason"] == 0) & (r["d"] > 0)   # only completed forward water-to-water flights count
    bad = int((~valid).sum())
    W = np.where(valid, W, P["e_swim"] * np.exp(-P.get("kappa_fin", 0.0) * C.fin_wetted_ratio(r, P)))
    s, gl = idx(g, a), idx(g, t)
    bott, path = maximin_path(W, s, gl, tol=1e-9)
    steps = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    gains = [W[v] - W[u] for u, v in steps]
    kmin = int(np.argmin(gains)) if gains else 0
    u, v = steps[kmin] if steps else (s, s)
    ax = [i for i in range(4) if u[i] != v[i]]
    bstep = {"trait": TRAITS[ax[0]] if ax else None, "from": {k: float(g[k][u[i]]) for i, k in enumerate(TRAITS)}, "to": {k: float(g[k][v[i]]) for i, k in enumerate(TRAITS)},
             "dW": float(gains[kmin]) if gains else None}
    n_neutral = int(sum(abs(x) <= 1e-9 for x in gains)); n_down = int(sum(x < -1e-9 for x in gains))
    lnW = np.log(np.maximum(W, 1e-12))
    traj, gradn, dist = lande_walk(g, lnW, a, t, cv, gens, P, r_pc)
    slow = int(np.argmin(gradn[: max(1, int(np.argmax(dist < dist[0] * 0.05)) or len(gradn))])) if len(gradn) else 0
    end = {"p": float(traj[-1][0]), "A": float(math.exp(traj[-1][1])), "M": float(math.exp(traj[-1][2])), "c": float(traj[-1][3])}
    reach = np.where(dist < 0.05)[0]
    return W, path, traj, gradn, dist, {
        "hypothesis": hyp, "W_ancestor": float(W[s]), "W_target": float(W[gl]), "W_grid_max": float(W.max()),
        "grid_cells": int(W.size), "cells_not_completed_flight": bad,
        "maximin_worst_step_dW": bott,
        "weakest_step_selection_coefficient": (bott / max(float(W[s]), 1e-12)) if bott > 0 else None,
        "Ne_needed_for_selection_to_dominate_drift_at_weakest_step": (1.0 / (2 * bott / max(float(W[s]), 1e-12))) if bott > 1e-12 else None, "strictly_improving_path_exists": bott > 1e-9, "path_only_via_neutral_steps": abs(bott) <= 1e-9,
        "valley_depth_if_any": (-bott if bott < -1e-9 else 0.0), "path_len": len(path) - 1, "path_neutral_steps": n_neutral, "path_downhill_steps": n_down,
        "path_bottleneck_step": bstep,
        "lande": {"generations": gens, "cv_A": cv, "end": end, "end_dist_to_target_norm": float(dist[-1]), "first_gen_within_0.05_of_target": int(reach[0]) if len(reach) else None,
                  "slowest_gen": slow, "slowest_state": {"p": float(traj[slow][0]), "A": float(math.exp(traj[slow][1])), "M": float(math.exp(traj[slow][2])), "c": float(traj[slow][3])},
                  "slowest_step_norm": float(gradn[slow]) if len(gradn) else None, "median_step_norm": float(np.median(gradn)) if len(gradn) else None},
    }


def straight_line(a, t, P, hyp, n=201, dt=0.004):
    s = np.linspace(0, 1, n)
    z = {k: (a[k] * (t[k] / a[k]) ** s if k in ("A", "M") else a[k] + (t[k] - a[k]) * s) for k in TRAITS}
    r = C.launch_and_glide(z["p"], z["A"], z["M"], z["c"], P, dt=dt)
    W = C.fitness(r, P, h_vis=hyp in ("vis", "both"), h_chase=hyp in ("chase", "both"))
    dW = np.diff(W)
    return s, W, r, {"max_drop": float(-dW.min()) if dW.min() < 0 else 0.0, "monotone_nondecreasing": bool((dW >= -1e-12).all()),
                     "frac_steps_flat": float(np.mean(np.abs(dW) < 1e-6))}


SETTINGS = [  # physics settings that need fresh glide integrations (name, overrides)
    ("default", {}), ("V_exit=4", {"V_exit": 4.0}), ("dV_taxi=4", {"dV_taxi": 4.0}), ("dV_taxi=10", {"dV_taxi": 10.0}),
    ("gam0=5", {"gam0_deg": 5.0}), ("gam0=30", {"gam0_deg": 30.0}), ("h0=0.3", {"h0": 0.3}), ("polar=P2_high_drag", {"polar": "P2_high_drag"}),
    ("a_LW=exocoetid", {"a_LW": C.LW["exocoetid"]}), ("w_body=0.06", {"w_body_frac": 0.06}), ("w_body=0.14", {"w_body_frac": 0.14}),
    ("n_trim=1.5", {"n_trim": 1.5}), ("CL_schedule", {"cl_schedule": True}),
]
ESC = [  # escape-model settings on the default physics (cheap)
    ("U_burst=5.21", {"U_burst": 5.21}), ("U_burst=20.46", {"U_burst": 20.46}), ("t_burst=6", {"t_burst": 6.0}), ("e_swim=0.1", {"e_swim": 0.1}),
    ("e_swim=0.6", {"e_swim": 0.6}), ("d_vis=5", {"d_vis": 5.0}), ("d_vis=80", {"d_vis": 80.0}), ("d_gap=10", {"d_gap": 10.0}), ("beta_air=0.05", {"beta_air": 0.05}),
    ("beta_air=0.2", {"beta_air": 0.2}), ("kappa_fin=0.1", {"kappa_fin": 0.1}), ("kappa_fin=0.3", {"kappa_fin": 0.3}), ("kappa_fin=1.0", {"kappa_fin": 1.0}),
]
LANDE_VARIANTS = [("cv=0.02", 0.02, 0.0), ("cv=0.10", 0.10, 0.0), ("r_pc=0.5 (p-c pleiotropy)", 0.05, 0.5), ("r_pc=-0.5", 0.05, -0.5)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(C.OUT / "eco-reachability"))
    ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--dt", type=float, default=0.004)
    ap.add_argument("--gens", type=int, default=4000)
    ap.add_argument("--cv", type=float, default=0.05)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--settings", default=None, help="comma-separated SETTINGS names to run (default: all)")
    ap.add_argument("--extras", action="store_true", help="with 'default': escape-setting sweep, Lande variants, zero-lift control, dt check, saved landscape")
    ap.add_argument("--tag", default=None, help="shard tag: writes results_<tag>.json / receipt_<tag>.json")
    a_ = ap.parse_args()
    np.random.seed(a_.seed)   # the model is deterministic; the seed is recorded for the receipt
    started = C.utcnow(); t0 = time.time(); inputs = C.input_hashes(__file__)
    out = Path(a_.out); out.mkdir(parents=True, exist_ok=True)
    sfx = f"_{a_.tag}" if a_.tag else ""
    res = {"schema": "frontier.eco.reachability/1", "shard": a_.tag, "assumptions": C.ASSUMPTIONS, "anchors": C.ANCHORS, "sources": C.SOURCES, "runs": []}
    keep = {}
    settings = SETTINGS[:1] if a_.quick else SETTINGS
    if a_.settings:
        want = a_.settings.split(","); settings = [x for x in SETTINGS if x[0] in want]
        assert len(settings) == len(want), f"unknown setting in {want}"
    extras = (not a_.quick) and (a_.extras or not a_.settings)
    for name, ov in settings:
        P = {**C.DEFAULT, **ov}
        g, a, t, r = landscape(P, a_.dt)
        hyps = ("vis", "chase", "both")
        for hyp in hyps:
            W, path, traj, gradn, dist, summ = analyse(g, a, t, r, P, hyp, a_.cv, a_.gens)
            s, Wl, rl, sl = straight_line(a, t, P, hyp, dt=a_.dt)
            row = {"setting": name, "overrides": ov, **summ, "straight_line": sl, "ancestor": a, "target": t}
            res["runs"].append(row); print(name, hyp, {k: row[k] for k in ("W_ancestor", "W_target", "maximin_worst_step_dW", "strictly_improving_path_exists")},
                                            "lande_end", {k: round(v, 3) for k, v in summ["lande"]["end"].items()}, flush=True)
            if name == "default":
                keep[hyp] = (g, a, t, r, W, path, traj, gradn, dist, s, Wl, rl)
        if name == "default" and extras:
            for en, eov in ESC:
                P2 = {**P, **eov}
                for hyp in hyps:
                    W, path, traj, gradn, dist, summ = analyse(g, a, t, r, P2, hyp, a_.cv, a_.gens)
                    s, Wl, rl, sl = straight_line(a, t, P2, hyp, dt=a_.dt)
                    res["runs"].append({"setting": en, "overrides": eov, **summ, "straight_line": sl, "ancestor": a, "target": t})
                    print(en, hyp, summ["maximin_worst_step_dW"], summ["strictly_improving_path_exists"], flush=True)
        if name == "default" and extras:
            for ln, cv, rpc in LANDE_VARIANTS:
                for hyp in hyps:
                    W, path, traj, gradn, dist, summ = analyse(g, a, t, r, P, hyp, cv, a_.gens, rpc)
                    res["runs"].append({"setting": "lande:" + ln, "overrides": {"cv_A": cv, "r_pc": rpc}, **summ, "ancestor": a, "target": t})
                    print(ln, hyp, {k: round(v, 3) for k, v in summ["lande"]["end"].items()}, flush=True)
            # zero-lift (ballistic) control on the default landscape: how much of W comes from lift at all
            rb = C.launch_and_glide(*np.meshgrid(*[g[k] for k in TRAITS], indexing="ij"), P, dt=a_.dt, lift=False)
            ia, it = idx(g, a), idx(g, t)
            res["ballistic_control"] = {"ancestor_d_lift": float(r["d"][ia]), "ancestor_d_no_lift": float(rb["d"][ia]), "target_d_lift": float(r["d"][it]), "target_d_no_lift": float(rb["d"][it]),
                                        "note": "same V0 (taxi gain still computed from phi); lift switched off in the airborne phase"}
            print("ballistic", res["ballistic_control"], flush=True)
        if name == "default" and extras:  # numerical check: dt halving on the landscape
            r2 = C.launch_and_glide(*np.meshgrid(*[g[k] for k in TRAITS], indexing="ij"), P, dt=a_.dt / 2)
            ok = (r["end_reason"] == 0) & (r2["end_reason"] == 0)
            rel = np.abs(r2["d"][ok] - r["d"][ok]) / np.maximum(r2["d"][ok], 1e-9)
            res["dt_check"] = {"dt": a_.dt, "dt_half": a_.dt / 2, "cells": int(ok.sum()), "max_rel_range_change": float(rel.max()), "p99_rel_range_change": float(np.quantile(rel, 0.99))}
            print("dt check", res["dt_check"], flush=True)
            np.savez_compressed(out / "landscape_default.npz", **{k: g[k] for k in TRAITS}, d=r["d"], t_air=r["t_air"], end_reason=r["end_reason"], V0=r["V0"], phi=r["phi"],
                                **{f"W_{h}": keep[h][4] for h in keep}, **{f"lande_{h}": keep[h][6] for h in keep})
    res["elapsed_s"] = time.time() - t0
    import pickle
    outs = [out / f"results{sfx}.json"]
    if keep:
        with open(out / "_keep.pkl", "wb") as fh:
            pickle.dump(keep, fh)
    if (out / "landscape_default.npz").exists() and extras:
        outs.append(out / "landscape_default.npz")
    C.dump(out / f"results{sfx}.json", res)
    C.dump(out / f"receipt{sfx}.json", C.receipt(__file__, a_.seed, started, {"elapsed_s": res["elapsed_s"], "dt": a_.dt, "gens": a_.gens, "cv_A": a_.cv, "shard": a_.tag,
                                                                            "settings": [x[0] for x in settings], "extras": extras}, outputs=outs, inputs=inputs))


if __name__ == "__main__":
    main()


def merge(out_dir, tags):
    """Merge shard results into results.json and a receipt.json that lists every shard receipt by hash."""
    out = Path(out_dir); res = None; shards = []
    for t in tags:
        r = json.loads((out / f"results_{t}.json").read_text()); rc = json.loads((out / f"receipt_{t}.json").read_text())
        shards.append({"tag": t, "receipt": f"receipt_{t}.json", "receipt_sha256": C.sha256_file(out / f"receipt_{t}.json"), "exit_code": rc["exit_code"], "command": rc["command"],
                       "settings": rc.get("settings"), "elapsed_s": rc.get("elapsed_s")})
        if res is None:
            res = {k: v for k, v in r.items() if k not in ("runs", "shard", "elapsed_s")}; res["runs"] = []
        res["runs"] += r["runs"]
        for k in ("dt_check", "ballistic_control"):
            if k in r:
                res[k] = r[k]
    C.dump(out / "results.json", res)
    first = json.loads((out / f"receipt_{tags[0]}.json").read_text())
    C.dump(out / "receipt.json", {"schema": "frontier.eco.receipt/1", "kind": "merge of shard receipts", "script": first["script"], "seed": first["seed"], "exit_code": 0 if all(s["exit_code"] == 0 for s in shards) else 1,
                                  "command": "python3 -c 'from engineering.ecology_sims.reachability import merge; merge(...)'", "started_utc": min(json.loads((out / f"receipt_{t}.json").read_text())["started_utc"] for t in tags),
                                  "finished_utc": C.utcnow(), "inputs_sha256": first["inputs_sha256"], "shards": shards,
                                  "outputs_sha256": {"results.json": C.sha256_file(out / "results.json")}})
