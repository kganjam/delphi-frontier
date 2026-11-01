"""Collective scale, population/behavioural layer: do schooling flying fish escape a predator better per capita than solitary ones?

Agent-based, 2-D top-down, vectorised over B independent attack episodes per condition.
  school geometry : zonal model (repulsion / orientation / attraction; Couzin et al. 2002 form) run to a polarised school, then
                    translated rigidly at cruise speed until alarm. Radii are ASSUMPTIONS.
  detection       : a prey within r_det of the predator detects it at rate q_det (per s); "many eyes" emerges from N detectors.
  alarm (sync)    : a detection alerts every school-mate after tau_alarm per hop on the neighbour graph (r_alarm) of the school
                    geometry at the moment of attack (Trafalgar-effect form, Treherne & Foster 1981). OFF = each fish only acts on
                    its own detection.
  launch          : an alerted glider exits after tau_launch; airborne distance/time = the project glide (common.launch_and_glide)
                    for the phenotype x a per-launch lognormal factor (CV 0.2, ASSUMPTION); direction away from the predator +- 30 deg.
                    Re-launch allowed after t_refract. Non-gliders swim away at U_flee.
  predator        : approaches the school centroid at U_app; bursts at U_burst (FishBase T. albacares burst row range) within
                    r_burst of the nearest prey; burst lasts t_burst then the episode ends (sustained speed is below prey flee speed).
                    In-water strike at r_strike succeeds with P1 / (1 + kappa (n_near - 1)) (confusion; Landeau & Terborgh 1986 form).
                    When its target launches it keeps visual track with probability exp(-d/d_vis) / (1 + kappa_air (n_air_view - 1))
                    (visual term of common.escape_prob plus aerial confusion from other fish airborne at once) and then pursues the
                    target's current ground-projected position at its own speed (no foreknowledge of the landing point; whether it keeps up
                    is explicit kinematics); otherwise it retargets the nearest in-water prey within r_view.
  controls        : glide_sync, glide_indep, swim_sync (alarm cascade, no gliding), swim (neither) -- swim_sync added after argon review.
Output: P(capture per attack episode), per-capita capture probability per encounter (= P/N), and per-capita risk per unit time
for encounter rate scaling lambda(N) = lambda_1 N^alpha (alpha swept). SIMULATED; no school or predator was observed.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engineering.ecology_sims import common as C  # noqa: E402

ABM = {  # value, unit, provenance
    "r_rep": (0.15, "m", "ASSUMPTION zone of repulsion (~1 SL)"), "r_ori": (0.6, "m", "ASSUMPTION zone of orientation"), "r_att": (2.0, "m", "ASSUMPTION zone of attraction"),
    "v_cruise": (0.5, "m/s", "ASSUMPTION cruise speed (~3 SL/s)"), "r_det": (3.0, "m", "ASSUMPTION predator detection range (set equal to r_burst so detection races the strike; 6 m is a sensitivity case)"), "q_det": (2.0, "1/s", "ASSUMPTION detection rate within r_det"),
    "r_alarm": (0.8, "m", "ASSUMPTION alarm neighbour radius"), "tau_alarm": (0.1, "s", "ASSUMPTION delay per alarm hop"), "tau_launch": (0.3, "s", "ASSUMPTION alert-to-exit latency"),
    "t_refract": (1.0, "s", "ASSUMPTION time before a landed fish can re-launch"), "glide_cv": (0.2, "1", "ASSUMPTION per-launch lognormal CV of airborne distance/time"),
    "U_flee": (1.7, "m/s", "ASSUMPTION non-glider flee speed (~10 SL/s for a 17 cm fish)"), "U_app": (2.0, "m/s", "ASSUMPTION predator approach speed"),
    "r0": (12.0, "m", "ASSUMPTION predator start distance from school centroid"), "r_burst": (3.0, "m", "ASSUMPTION distance at which the predator bursts"),
    "r_strike": (0.3, "m", "ASSUMPTION strike reach"), "P1": (0.5, "1", "ASSUMPTION single-target strike success"), "strike_cooldown": (0.3, "s", "ASSUMPTION"),
    "kappa": (0.2, "1", "ASSUMPTION confusion strength in water (Landeau & Terborgh form)"), "r_conf": (1.0, "m", "ASSUMPTION confusion radius"),
    "kappa_air": (0.2, "1", "ASSUMPTION confusion from simultaneous airborne fish"), "r_view": (8.0, "m", "ASSUMPTION predator view radius for retargeting / aerial confusion"),
    "T_max": (12.0, "s", "episode cap"), "dt": (0.02, "s", "time step"),
}
A0 = {k: v[0] for k, v in ABM.items()}


def make_schools(rng, B, N, A, steps=250):
    """Zonal model in 2-D, B schools of N in parallel; returns positions (B,N,2) centred, heading rotated to +x."""
    pos = rng.normal(0, 0.25 * math.sqrt(N), (B, N, 2)); ang = rng.normal(0, 0.3, (B, N))
    vel = np.stack([np.cos(ang), np.sin(ang)], -1)
    if N == 1:
        return np.zeros((B, 1, 2))
    for _ in range(steps):
        dvec = pos[:, None, :, :] - pos[:, :, None, :]        # j - i
        dist = np.linalg.norm(dvec, axis=-1) + np.eye(N)[None] * 1e9
        rep = dist < A["r_rep"]; ori = (dist >= A["r_rep"]) & (dist < A["r_ori"]); att = (dist >= A["r_ori"]) & (dist < A["r_att"])
        u = dvec / dist[..., None]
        drep = -(u * rep[..., None]).sum(2)
        dsoc = (vel[:, None, :, :] * ori[..., None]).sum(2) + (u * att[..., None]).sum(2)
        has_rep = rep.any(2)[..., None]
        des = np.where(has_rep, drep, dsoc)
        lone = (np.linalg.norm(des, axis=-1) < 1e-9)[..., None]
        des = np.where(lone, vel, des)
        des = des / np.maximum(np.linalg.norm(des, axis=-1, keepdims=True), 1e-12)
        vel = 0.7 * vel + 0.3 * des + rng.normal(0, 0.05, vel.shape)
        vel /= np.linalg.norm(vel, axis=-1, keepdims=True)
        pos = pos + vel * A["v_cruise"] * 0.1
    head = vel.mean(1); th = np.arctan2(head[:, 1], head[:, 0])
    c, s = np.cos(-th), np.sin(-th)
    R = np.stack([np.stack([c, -s], -1), np.stack([s, c], -1)], -2)    # (B,2,2)
    pos = pos - pos.mean(1, keepdims=True)
    return np.einsum("bij,bnj->bni", R, pos)


def hop_matrix(pos, r):
    """All-pairs hop counts on the r-neighbour graph (min-plus closure), inf where disconnected."""
    B, N, _ = pos.shape
    d = np.linalg.norm(pos[:, :, None] - pos[:, None], axis=-1)
    H = np.where(d < r, 1.0, np.inf); H[:, np.arange(N), np.arange(N)] = 0
    for k in range(N):
        H = np.minimum(H, H[:, :, k:k + 1] + H[:, k:k + 1, :])
    return H


def run(rng, B, N, mode, glide_d, glide_t, A, P, record=False):
    """mode: 'glide_sync', 'glide_indep', 'swim'. Returns dict with capture flags and optional trajectory for episode 0."""
    dt = A["dt"]; steps = int(A["T_max"] / dt)
    pos = make_schools(rng, B, N, A)
    hops = hop_matrix(pos, A["r_alarm"]) if (mode.endswith("_sync") and N > 1) else None
    th0 = rng.uniform(0, 2 * np.pi, B)
    ppos = np.stack([A["r0"] * np.cos(th0), A["r0"] * np.sin(th0)], -1)
    status = np.zeros((B, N), int)            # 0 water, 1 air, 2 caught
    alert_t = np.full((B, N), np.inf); detected = np.zeros((B, N), bool)
    launch_t = np.full((B, N), np.inf); land_t = np.full((B, N), -np.inf); refr = np.full((B, N), -np.inf)
    lpos0 = np.zeros((B, N, 2)); lpos1 = np.zeros((B, N, 2)); lt0 = np.zeros((B, N)); lt1 = np.ones((B, N))
    pmode = np.zeros(B, int)                  # 0 approach, 1 burst, 2 done
    burst_left = np.full(B, P["t_burst"]); target = np.full(B, -1); tracking_air = np.zeros(B, bool)
    cool = np.zeros(B); captured = np.zeros(B, bool); n_launch = np.zeros(B); first_detect = np.full(B, np.inf)
    bi = np.arange(B)
    frames = [] if record else None
    vcr = np.array([A["v_cruise"], 0.0])
    for k in range(steps):
        t = k * dt
        live = pmode < 2
        if not live.any():
            break
        water = status == 0
        # detection
        dpp = np.linalg.norm(pos - ppos[:, None], axis=-1)
        newdet = water & ~detected & (dpp < A["r_det"]) & (rng.random((B, N)) < 1 - math.exp(-A["q_det"] * dt)) & live[:, None]
        if newdet.any():
            detected |= newdet
            alert_t = np.where(newdet, np.minimum(alert_t, t), alert_t)
            first_detect = np.where(newdet.any(1), np.minimum(first_detect, t), first_detect)
            if hops is not None:
                src = np.where(newdet, t, np.inf)                                        # (B,N)
                prop = (src[:, :, None] + A["tau_alarm"] * hops).min(1)                 # (B,N)
                alert_t = np.minimum(alert_t, prop)
        alerted = (alert_t <= t)
        # prey motion in water
        away = pos - ppos[:, None]; away /= np.maximum(np.linalg.norm(away, axis=-1, keepdims=True), 1e-9)
        if mode.startswith("swim"):
            v = np.where((alerted & water)[..., None], away * A["U_flee"], vcr)
        else:
            v = np.where((alerted & water)[..., None], away * A["U_flee"], vcr)
            can = water & alerted & (t >= alert_t + A["tau_launch"]) & (t >= refr) & live[:, None]
            if can.any():
                f = np.exp(rng.normal(-0.5 * A["glide_cv"] ** 2, A["glide_cv"], (B, N)))
                ang = np.arctan2(away[..., 1], away[..., 0]) + rng.normal(0, math.radians(30), (B, N))
                dvec = np.stack([np.cos(ang), np.sin(ang)], -1) * (glide_d * f)[..., None]
                lpos0 = np.where(can[..., None], pos, lpos0); lpos1 = np.where(can[..., None], pos + dvec, lpos1)
                lt0 = np.where(can, t, lt0); lt1 = np.where(can, t + glide_t * f, lt1)
                status = np.where(can, 1, status); n_launch += can.sum(1)
                # predator decision if its target just launched
                tl = can[bi, np.maximum(target, 0)] & (target >= 0) & (pmode == 1)
                if tl.any():
                    j = target[tl]; b = bi[tl]
                    d = glide_d * f[b, j]; ta = glide_t * f[b, j]
                    nair = ((status[b] == 1) & (np.linalg.norm(pos[b] - ppos[b][:, None], axis=-1) < A["r_view"])).sum(1)
                    # visual retention only; whether the predator keeps up is explicit kinematics below (no d_gap term here)
                    ptrack = np.exp(-d / P["d_vis"]) / (1 + A["kappa_air"] * np.maximum(nair - 1, 0))
                    keep = rng.random(len(b)) < ptrack
                    tracking_air[b] = keep
                    target[b[~keep]] = -1
            water = status == 0
        pos = np.where(water[..., None] & live[:, None, None], pos + v * dt, pos)
        air = status == 1
        if air.any():
            frac = np.clip((t - lt0) / np.maximum(lt1 - lt0, 1e-9), 0, 1)[..., None]
            pos = np.where(air[..., None], lpos0 + frac * (lpos1 - lpos0), pos)
            landed = air & (t >= lt1)
            status = np.where(landed, 0, status); refr = np.where(landed, t + A["t_refract"], refr)
        # predator
        water = status == 0
        dpp = np.linalg.norm(pos - ppos[:, None], axis=-1)
        dw = np.where(water, dpp, np.inf)
        nearest = dw.argmin(1); nd = dw.min(1)
        app = (pmode == 0)
        if app.any():
            cen = np.where(water[..., None], pos, 0).sum(1) / np.maximum(water.sum(1), 1)[:, None]
            dirc = cen - ppos; dirc /= np.maximum(np.linalg.norm(dirc, axis=-1, keepdims=True), 1e-9)
            ppos = np.where(app[:, None], ppos + dirc * A["U_app"] * dt, ppos)
            go = app & (nd < A["r_burst"])
            pmode = np.where(go, 1, pmode); target = np.where(go, nearest, target)
            pmode = np.where(app & ~np.isfinite(nd), 2, pmode)   # nobody in water and still approaching: give up
        bur = pmode == 1
        if bur.any():
            # retarget if no target or target caught
            notg = bur & (target < 0)
            ok_new = notg & (nd < A["r_view"])
            target = np.where(ok_new, nearest, target); tracking_air = np.where(ok_new, False, tracking_air)
            pmode = np.where(notg & ~ok_new, 2, pmode)
            bur = pmode == 1
            tj = np.maximum(target, 0)
            tpos = pos[bi, tj]          # pursue the target's current ground-projected position (airborne or not); no foreknowledge of landing
            dv = tpos - ppos; dist = np.linalg.norm(dv, axis=-1)
            spd = np.where(burst_left > 0, P["U_burst"], P["U_sus"])
            stepl = np.minimum(spd * dt, dist)
            ppos = np.where(bur[:, None], ppos + dv / np.maximum(dist, 1e-9)[:, None] * stepl[:, None], ppos)
            burst_left = np.where(bur, burst_left - dt, burst_left)
            # strike
            inw = status[bi, tj] == 0
            strike = bur & inw & (np.linalg.norm(pos[bi, tj] - ppos, axis=-1) < A["r_strike"]) & (t >= cool)
            if strike.any():
                nn = ((np.linalg.norm(pos - ppos[:, None], axis=-1) < A["r_conf"]) & water).sum(1)
                pc = A["P1"] / (1 + A["kappa"] * np.maximum(nn - 1, 0))
                hit = strike & (rng.random(B) < pc)
                status[bi[hit], tj[hit]] = 2
                captured |= hit; pmode = np.where(hit, 2, pmode)
                miss = strike & ~hit
                cool = np.where(miss, t + A["strike_cooldown"], cool)
                target = np.where(miss, -1, target)
            pmode = np.where((pmode == 1) & (burst_left <= 0), 2, pmode)
        if record:
            frames.append((t, pos[0].copy(), status[0].copy(), ppos[0].copy(), int(pmode[0]), alerted[0].copy()))
    return {"captured": captured, "n_launch": n_launch, "first_detect": first_detect, "frames": frames}


CONDS = ["glide_sync", "glide_indep", "swim_sync", "swim"]
NS = [1, 2, 4, 8, 16, 32, 64]


def batch(seed, B, glide_d, glide_t, A, P, ns=NS, conds=CONDS):
    out = {}
    for cond in conds:
        for N in ns:
            rng = np.random.default_rng([seed, N, CONDS.index(cond)])
            r = run(rng, B, N, cond, glide_d, glide_t, A, P)
            pc = float(r["captured"].mean())
            se = math.sqrt(max(pc * (1 - pc), 1e-12) / B)
            out[f"{cond}|{N}"] = {"P_capture_episode": pc, "se": se, "per_capita": pc / N, "per_capita_se": se / N, "mean_launches": float(r["n_launch"].mean())}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(C.OUT / "collective-school-escape"))
    ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--B", type=int, default=600)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--part", default="all", help="all | main | sens:<i>-<j> (slice of the sensitivity list)")
    a_ = ap.parse_args()
    started = C.utcnow(); t0 = time.time(); inputs = C.input_hashes(__file__)
    do_main = a_.part in ("all", "main"); sl = slice(None) if a_.part == "all" else (slice(*map(int, a_.part[5:].split("-"))) if a_.part.startswith("sens:") else slice(0, 0))
    sfx = "" if a_.part == "all" else "_" + a_.part.replace(":", "").replace("-", "_")
    out = Path(a_.out); out.mkdir(parents=True, exist_ok=True)
    P = dict(C.DEFAULT)
    tz = C.target_phenotype(P); g = C.launch_and_glide(tz["p"], tz["A"], tz["M"], tz["c"], P)
    gd, gt = float(g["d"]), float(g["t_air"])
    res = {"schema": "frontier.eco.collective/1", "abm_assumptions": ABM, "shared_assumptions": C.ASSUMPTIONS, "sources": C.SOURCES,
           "glide_input": {"phenotype": tz, "airborne_distance_m": gd, "airborne_time_s": gt, "from": "common.launch_and_glide (project glide model), Exocoetus-like target"}}
    ns = [1, 4, 16] if a_.quick else NS
    res["part"] = a_.part
    if do_main:
        res["main"] = batch(a_.seed, a_.B, gd, gt, A0, P, ns=ns)
        for k, v in res["main"].items():
            print(k, v, flush=True)
        # alpha (encounter-rate scaling) post-hoc
        res["risk_per_time_relative_to_solitary"] = {}
        for alpha in (0.0, 0.5, 1.0):
            for cond in CONDS:
                base = res["main"][f"{cond}|1"]["P_capture_episode"]
                res["risk_per_time_relative_to_solitary"][f"alpha={alpha}|{cond}"] = {str(N): (res["main"][f"{cond}|{N}"]["P_capture_episode"] * N ** alpha / N) / max(base, 1e-12) for N in ns}
    if not a_.quick:
        sens = []
        Bs = max(200, a_.B // 2)
        for name, aov, pov, glide_scale in [
            ("kappa=0", {"kappa": 0.0, "kappa_air": 0.0}, {}, 1.0), ("kappa=0.5", {"kappa": 0.5, "kappa_air": 0.5}, {}, 1.0),
            ("tau_alarm=0.3", {"tau_alarm": 0.3}, {}, 1.0), ("r_alarm=0.4", {"r_alarm": 0.4}, {}, 1.0), ("r_det=6", {"r_det": 6.0}, {}, 1.0),
            ("q_det=1", {"q_det": 1.0}, {}, 1.0), ("q_det=4", {"q_det": 4.0}, {}, 1.0), ("P1=0.8", {"P1": 0.8}, {}, 1.0), ("U_burst=20.46", {}, {"U_burst": 20.46}, 1.0),
            ("U_burst=5.21", {}, {"U_burst": 5.21}, 1.0), ("d_vis=80", {}, {"d_vis": 80.0}, 1.0), ("glide x0.5 (intermediate-like)", {}, {}, 0.5),
            ("tau_launch=0.6", {"tau_launch": 0.6}, {}, 1.0), ("U_flee=5", {"U_flee": 5.0}, {}, 1.0), ("U_flee=10 (=V_exit)", {"U_flee": 10.0}, {}, 1.0)][sl]:
            r = batch(a_.seed + 1, Bs, gd * glide_scale, gt * glide_scale, {**A0, **aov}, {**P, **pov}, ns=[1, 8, 32])
            sens.append({"setting": name, "abm_overrides": aov, "escape_overrides": pov, "glide_scale": glide_scale, "B": Bs, "results": r})
            print(name, {k: round(v["per_capita"], 4) for k, v in r.items()}, flush=True)
        res["sensitivity"] = sens
        if do_main:  # seed replicate of the main table for N in {1, 16}
            res["seed_replicate"] = batch(a_.seed + 99, a_.B, gd, gt, A0, P, ns=[1, 16])
    if do_main:  # record one episode per condition for the video
        rec = {}
        for cond in CONDS:
            for N in (1, 32):
                rng = np.random.default_rng([a_.seed, 7, N, CONDS.index(cond)])
                rec[f"{cond}|{N}"] = run(rng, 1, N, cond, gd, gt, A0, P, record=True)
        import pickle
        with open(out / "_frames.pkl", "wb") as fh:
            pickle.dump({k: {"frames": v["frames"], "captured": bool(v["captured"][0])} for k, v in rec.items()}, fh)
    res["elapsed_s"] = time.time() - t0
    C.dump(out / f"results{sfx}.json", res)
    C.dump(out / f"receipt{sfx}.json", C.receipt(__file__, a_.seed, started, {"elapsed_s": res["elapsed_s"], "B": a_.B, "part": a_.part, "rng": "numpy default_rng([seed, N, condition_index]); sensitivity uses seed+1, replicate seed+99"},
                                                outputs=[out / f"results{sfx}.json"], inputs=inputs))


def merge(out_dir, sfxs):
    out = Path(out_dir); res = None; shards = []
    for t in sfxs:
        r = json.loads((out / f"results_{t}.json").read_text()); rc = json.loads((out / f"receipt_{t}.json").read_text())
        shards.append({"part": rc.get("part"), "receipt": f"receipt_{t}.json", "receipt_sha256": C.sha256_file(out / f"receipt_{t}.json"), "exit_code": rc["exit_code"], "command": rc["command"], "elapsed_s": rc.get("elapsed_s")})
        if res is None:
            res = {k: v for k, v in r.items() if k not in ("sensitivity", "part", "elapsed_s")}; res["sensitivity"] = []
        for k in ("main", "risk_per_time_relative_to_solitary", "seed_replicate"):
            if k in r:
                res[k] = r[k]
        res["sensitivity"] += r.get("sensitivity", [])
    C.dump(out / "results.json", res)
    first = json.loads((out / f"receipt_{sfxs[0]}.json").read_text())
    C.dump(out / "receipt.json", {"schema": "frontier.eco.receipt/1", "kind": "merge of shard receipts", "script": first["script"], "seed": first["seed"], "exit_code": 0 if all(s["exit_code"] == 0 for s in shards) else 1,
                                  "command": "python3 -c 'from engineering.ecology_sims.collective import merge; merge(...)'", "started_utc": min(json.loads((out / f"receipt_{t}.json").read_text())["started_utc"] for t in sfxs),
                                  "finished_utc": C.utcnow(), "inputs_sha256": first["inputs_sha256"], "shards": shards, "outputs_sha256": {"results.json": C.sha256_file(out / "results.json")}})


if __name__ == "__main__":
    main()
