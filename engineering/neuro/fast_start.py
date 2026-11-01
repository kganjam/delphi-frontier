"""M1: escape trigger -> Mauthner-initiated C-start -> CPG burst to the surface -> taxi -> release into the EXISTING glide model.

    OMP_NUM_THREADS=1 python -m engineering.neuro.fast_start [--seed 20261101] [--n 20000]

Monte Carlo over sourced/assumed priors (each tagged in PRIORS). 3D point-body kinematics (x, y horizontal, z up):
  decision   a predator looms from below at speed u_p; the trigger fires when its angular size crosses theta_thr (Preuss 2006:
             the M-cell is a threshold detector on a scaled angular size); response probability p_resp in [0.70, 0.91] (Preuss 2006).
  latency    Mauthner path delay after threshold (Domenici & Blake 1997 / Burgess & Granato 2007, recalled: ~5-20 ms).
  C-start    stage 1 is a YAW turn to an escape trajectory ET measured horizontally from the threat azimuth; ET mixture over
             90-180 deg with 50-90% away responses (Domenici 2011, abstract); turn-rate cap omega_max (recalled, order 10^3 deg/s);
             a small pitch component of the escape gamma_cs is an ASSUMPTION; a stage-2 speed jump.
  burst      speed from M2 (EBT thrust with muscle low-pass, capped by muscle power, minus submerged drag); after stage 1 the fish
             pitches toward an emergence angle gamma* in [20, 45] deg (bracketing Park & Choi 2010's 30-35 deg emergence ATTACK
             angle; path angle is not attack angle) at a pitch-rate cap. Steering to the surface is a separate, assumed decision.
  taxi       starts from the emergence speed (optimistic: no speed lost at re-contact) or from its horizontal component
             (pessimistic); M2 immersed-lobe thrust (power-capped, feathering limit sampled) minus air drag on the organism glide
             polar, spray drag and a residual wetted-hull fraction; take-off at 1.1 x stall speed within the taxi time budget.
  glide      engineering.simulation.glide.integrate with the organism baseline polar from engineering/simulation/video/manifest.json
             (m 0.05 kg, S 0.0057 m^2, AR 7.86, CL_max 1.2, CD0 0.06, e 0.8). Release at h0 = 0.1 m, gamma0 = 0 (continuity with a
             surface take-off; 0.1 m is an assumed body-height). h0 = 1.0 m (the glide model's own convention) is reported only to
             compare with the glide-fixed-launch card.
All SIMULATED. The predator is a kinematic pure-pursuit point, not an animal model.
"""
from __future__ import annotations
import argparse, json, math, sys, time
import numpy as np

from engineering.neuro import common as C
from engineering.neuro import caudal_cpg as M2
from engineering.simulation import glide

RID = "m1-fast-start"
L = C.L_BODY
DEG = math.pi / 180
H0_CONT = 0.1
PRIORS = {
    "p_resp": ([0.70, 0.91], "preuss2006 abstract_verified"),
    "theta_thr_deg": ([15, 40], "assumption; Preuss 2006 verifies the angular-size threshold principle, not these values"),
    "u_pred_ms": ([2, 6], "assumption: pursuit speed of a pelagic predator"),
    "D_pred_m": ([0.10, 0.30], "assumption: predator frontal size"),
    "r0_m": ([1.5, 4.0], "assumption: predator distance at looming onset"),
    "e_pred_deg": ([-150, -30], "assumption: threat elevation, from below"),
    "lat_M_ms": ([5, 20], "domenici_blake1997 / burgess_granato2007 recalled_not_reread (wide)"),
    "t_stage1_ms": ([15, 35], "domenici_blake1997 recalled_not_reread (scaled for ~17 cm)"),
    "omega_max_deg_s": ([1500, 5000], "domenici_blake1997 recalled_not_reread (wide)"),
    "p_away": ([0.5, 0.9], "domenici2011 abstract_verified"),
    "gamma_cs_deg": ([-10, 30], "assumption: vertical component of the C-start escape path"),
    "dU_cstart_BL_s": ([5, 15], "assumption informed by fast-start reviews (recalled); stage-2 speed jump"),
    "d0_m": ([0.3, 2.0], "assumption: starting depth of an epipelagic fish"),
    "u0_ms": ([0.3, 1.0], "assumption: cruise speed before stimulus"),
    "gamma_star_deg": ([20, 45], "assumption bracketing park_choi2010 30-35 deg emergence attack angle"),
    "q_max_deg_s": ([200, 800], "assumption: burst pitch-rate cap"),
    "f_burst_Hz": ([20, 60], "assumption; upper end from edgerton_breder1941 taxi range (recalled)"),
    "f_m_Hz": ([20, 70], "wardle1975 recalled (form assumed); same range as M2 sweep"),
    "H_over_L": ([0.08, 0.15], "assumption, M2 range"),
    "lam_over_L": ([0.8, 1.2], "assumption, M2 range"),
    "k_swim": ([1.0, 3.0], "assumption, M2 range"),
    "P_musc_W_per_kg": ([50, 250], "assumption: burst white-muscle mechanical power per kg muscle, order of magnitude recalled; thrust <= eta P / U"),
    "f_taxi_Hz": ([30, 70], "edgerton_breder1941 recalled_not_reread (50-70 Hz) widened"),
    "alpha_feather_deg": ([6, 15], "assumption: passive feathering limit of the taxi lobe (drives taxi thrust; reviewer flag)"),
    "wet_frac": ([0.0, 0.10], "assumption: residual wetted-hull drag fraction during taxi (reviewer flag)"),
    "T_taxi_max_s": ([0.3, 1.5], "assumption: taxi time budget"),
}
MUSCLE_FRAC, ETA_PROP = M2.MUSCLE_FRAC, 0.75      # assumptions: axial muscle fraction of body mass; propulsive efficiency in the cap


def sample(rng, n, override=None):
    s = {k: rng.uniform(*v[0], n) for k, v in PRIORS.items()}
    for k, v in (override or {}).items():
        s[k] = np.full(n, float(v))
    return s


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def lobe_vec(U, f, H, a_max, nph=96):
    """Vectorised M2.lobe_thrust with a per-sample feathering limit (same equations)."""
    P = M2.NOM; S = P["lobe_area_over_L2"] * L ** 2; AR = P["lobe_AR"]; cla = 2 * math.pi * AR / (AR + 2)
    ph = np.linspace(0, 2 * math.pi, nph, endpoint=False)[None, :]
    v = np.abs(2 * math.pi * f[:, None] * H[:, None] * np.cos(ph)); Uc = U[:, None]
    W = np.sqrt(Uc ** 2 + v ** 2); beta = np.arctan2(v, Uc); ae = np.minimum(beta, a_max[:, None])
    CL = cla * ae; CD = 2 * M2.cf(np.maximum(W, 1e-3) * math.sqrt(S / AR) / C.NU_W) + CL ** 2 / (math.pi * 0.8 * AR)
    return np.mean(0.5 * C.RHO_W * W ** 2 * S * (CL * np.sin(beta) - CD * np.cos(beta)), axis=1)


def simulate(s, dt=1e-3, T=4.0):
    n = len(s["p_resp"]); rng = np.random.default_rng(int(s.get("_seed", 0)))
    # ---- decision: time for the looming angle to reach threshold (predator closing on a nearly still fish)
    r_thr = s["D_pred_m"] / (2 * np.tan(s["theta_thr_deg"] * DEG / 2))
    t_thr = np.maximum(s["r0_m"] - r_thr, 0) / s["u_pred_ms"]
    responds = rng.uniform(size=n) < s["p_resp"]
    t_go = t_thr + s["lat_M_ms"] * 1e-3
    # ---- geometry: fish at (0,0,-d0) heading +x; predator at elevation e_p, azimuth a_p
    a_p = rng.uniform(-math.pi, math.pi, n); e_p = s["e_pred_deg"] * DEG
    p0 = np.stack([s["r0_m"] * np.cos(e_p) * np.cos(a_p), s["r0_m"] * np.cos(e_p) * np.sin(a_p), -s["d0_m"] + s["r0_m"] * np.sin(e_p)], 1)
    fish = np.stack([np.zeros(n), np.zeros(n), -s["d0_m"]], 1)
    t1 = t_go + s["t_stage1_ms"] * 1e-3
    adv = np.minimum(s["u_pred_ms"] * t1, s["r0_m"])[:, None]           # predator closes straight until the fish moves
    pred = fish + (p0 - fish) * (1 - adv / s["r0_m"][:, None])
    # ---- C-start: yaw to escape trajectory ET from the threat azimuth
    away = rng.uniform(size=n) < s["p_away"]
    et = np.where(away, np.where(rng.uniform(size=n) < 0.6, rng.uniform(130, 180, n), rng.uniform(90, 130, n)), rng.uniform(0, 90, n)) * DEG
    side = np.where(rng.uniform(size=n) < 0.5, 1.0, -1.0)
    psi_t = wrap(a_p + side * et)
    cap = s["omega_max_deg_s"] * DEG * s["t_stage1_ms"] * 1e-3
    psi = np.sign(psi_t) * np.minimum(np.abs(psi_t), cap)               # partial turn if the cap binds; finished at 1/4 rate below
    yaw_rate_after = 0.25 * s["omega_max_deg_s"] * DEG
    gam = s["gamma_cs_deg"] * DEG
    U = s["u0_ms"] + s["dU_cstart_BL_s"] * L
    caught = ~responds | (np.linalg.norm(pred - fish, axis=1) < 0.5 * s["D_pred_m"])
    Hf = M2.muscle_amp(s["f_burst_Hz"], s["H_over_L"] * L, s["f_m_Hz"]); lam = s["lam_over_L"] * L; span = M2.NOM["span_over_L"] * L
    meff = C.ORG["m_kg"] * (1 + M2.NOM["m_add_frac"])
    Pcap = ETA_PROP * s["P_musc_W_per_kg"] * MUSCLE_FRAC * C.ORG["m_kg"]
    gs = s["gamma_star_deg"] * DEG; qm = s["q_max_deg_s"] * DEG
    active = ~caught; emerged = np.zeros(n, bool)
    Ue = np.full(n, np.nan); ge = np.full(n, np.nan); te = np.full(n, np.nan); dmin = np.full(n, np.inf)
    for k in range(int(T / dt)):
        if not active.any():
            break
        Tq = np.minimum(M2.ebt_thrust(U, s["f_burst_Hz"], Hf, lam, span), Pcap / np.maximum(U, 0.1))
        U = np.where(active, np.maximum(U + dt * (Tq - M2.drag_sub(U, s["k_swim"])) / meff, 0.0), U)
        gam = np.where(active, gam + np.clip(gs - gam, -qm * dt, qm * dt), gam)
        dpsi = np.clip(wrap(psi_t - psi), -yaw_rate_after * dt, yaw_rate_after * dt); psi = np.where(active, psi + dpsi, psi)
        vel = np.stack([U * np.cos(gam) * np.cos(psi), U * np.cos(gam) * np.sin(psi), U * np.sin(gam)], 1)
        fish = np.where(active[:, None], fish + dt * vel, fish)
        d = fish - pred; r = np.linalg.norm(d, axis=1) + 1e-12
        pred = np.where(active[:, None], pred + dt * s["u_pred_ms"][:, None] * d / r[:, None], pred)
        dmin = np.where(active, np.minimum(dmin, r), dmin)
        hit = active & (r < 0.5 * s["D_pred_m"]); caught |= hit
        out = active & ~hit & (fish[:, 2] >= 0)
        Ue = np.where(out, U, Ue); ge = np.where(out, gam, ge); te = np.where(out, t1 + (k + 1) * dt, te)
        emerged |= out; active &= ~(hit | out)
    res = {"responds": responds, "caught": caught, "emerged": emerged, "t_go_s": t_go, "U_emerge_ms": Ue, "gamma_emerge_deg": np.degrees(ge),
           "t_emerge_s": te, "et_deg": np.degrees(et), "away": away}
    Vs = float(glide.stall_speed(C.ORG["m_kg"], C.ORG["S_m2"], C.RHO_A_GLIDE, C.ORG["CL_max"])); res["V_stall_ms"] = Vs
    for tag, V0 in (("opt", Ue), ("pes", Ue * np.cos(np.nan_to_num(ge)))):
        V, tt, ok = taxi(np.where(emerged, V0, np.nan), s, emerged, Pcap, Vs)
        res[f"V_taxi_end_ms_{tag}"] = V; res[f"taxi_time_s_{tag}"] = tt; res[f"took_off_{tag}"] = ok
    return res


def taxi(V, s, mask, Pcap, Vs, dt=2e-3):
    V = V.copy(); tt = np.zeros(len(V)); ok = np.zeros(len(V), bool); tax = mask.copy()
    Ht = M2.muscle_amp(s["f_taxi_Hz"], s["H_over_L"] * L, s["f_m_Hz"]); am = s["alpha_feather_deg"] * DEG
    for _ in range(int(1.6 / dt)):
        if not tax.any():
            break
        i = np.where(tax)[0]; Vi = np.maximum(V[i], 0.1)
        Tl = np.minimum(lobe_vec(Vi, s["f_taxi_Hz"][i], Ht[i], am[i]), Pcap[i] / Vi)
        Dw = 0.24 * 0.5 * C.RHO_W * Vi ** 2 * (0.01 * L) ** 2 + s["wet_frac"][i] * M2.drag_sub(Vi, 1.0)
        V[i] = np.maximum(Vi + dt * (Tl - M2.air_drag_taxi(Vi) - Dw) / C.ORG["m_kg"], 0.0)
        tt[i] += dt
        up = tax & (V >= 1.1 * Vs); ok |= up
        tax &= ~up & (tt < s["T_taxi_max_s"])
    return V, tt, ok


def glide_ranges(V0, gam0_deg=None, h0=H0_CONT):
    """engineering.simulation.glide.integrate on the organism polar; gam0 binned to 1 deg because integrate takes one release angle."""
    V0 = np.asarray(V0, float); o = C.ORG
    if V0.size == 0:
        return np.array([]), np.array([])
    cl = glide.cl_command(o["CL_max"], o["CD0"], o["e"], o["AR"])
    g = np.zeros_like(V0) if gam0_deg is None else np.round(np.asarray(gam0_deg, float))
    rng, why = np.zeros_like(V0), np.zeros(V0.size, int)
    for gv in np.unique(g):
        i = g == gv
        r = glide.integrate(o["m_kg"], o["S_m2"], o["AR"], C.RHO_A_GLIDE, cl, o["CD0"], o["e"], h0, V0[i], gam0=float(gv) * DEG, dt=0.002)
        rng[i], why[i] = r["range_m"], r["end_reason"]
    return rng, why


def q(a, ps=(5, 25, 50, 75, 95)):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return ({f"q{p}": float(np.percentile(a, p)) for p in ps} | {"n": int(a.size)}) if a.size else {"n": 0}


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=20261101); ap.add_argument("--n", type=int, default=20000)
    a = ap.parse_args(argv); t0 = time.time(); out = C.OUT / RID; out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(a.seed); checks = []
    # controls ----------------------------------------------------------------------------------------------
    s = sample(np.random.default_rng(1), 200, {"p_resp": 0.0}); s["_seed"] = 1
    checks.append({"name": "control: p_resp = 0 gives zero emergences", "pass": int(simulate(s)["emerged"].sum()) == 0})
    s = sample(np.random.default_rng(2), 200, {"p_resp": 1.0, "u_pred_ms": 1e-6}); s["_seed"] = 2; r1 = simulate(s)
    checks.append({"name": "control: stationary predator -> every responder emerges", "pass": bool(r1["emerged"].all()), "detail": int(r1["emerged"].sum())})
    rs = sample(np.random.default_rng(3), 400); rs["_seed"] = 3
    ra, rb = simulate(rs, dt=1e-3), simulate(rs, dt=5e-4); both = ra["emerged"] & rb["emerged"]
    dU = float(np.nanmax(np.abs(ra["U_emerge_ms"][both] - rb["U_emerge_ms"][both]) / rb["U_emerge_ms"][both]))
    checks.append({"name": "control: dt halving changes emergence speed < 2% (max over samples emerging in both)", "pass": dU < 0.02, "detail": dU})
    rg, _ = glide_ranges([12.0], h0=1.0)
    checks.append({"name": "control: glide feed reproduces the glide-fixed-launch nominal range 25.14 m at V0 12 m/s, h0 1 m", "pass": abs(rg[0] - 25.14228700829958) < 0.05, "detail": float(rg[0])})
    lv = lobe_vec(np.array([5.0, 10.0]), np.array([50.0, 50.0]), np.array([0.017, 0.017]), np.radians([12.0, 12.0]))
    lm = M2.lobe_thrust(np.array([5.0, 10.0]), 50.0, 0.017)
    checks.append({"name": "control: vectorised lobe thrust equals M2.lobe_thrust within 0.1%", "pass": bool(np.all(np.abs(lv / lm - 1) < 1e-3)), "detail": [lv.tolist(), lm.tolist()]})
    # main Monte Carlo ----------------------------------------------------------------------------------------------
    s = sample(rng, a.n); s["_seed"] = a.seed
    r = simulate(s); em = r["emerged"]
    direct, why_d = glide_ranges(np.nan_to_num(r["U_emerge_ms"][em]), r["gamma_emerge_deg"][em], h0=0.05)
    summ = {"n": a.n, "P_respond": float(r["responds"].mean()), "P_caught": float(r["caught"].mean()), "P_emerge": float(em.mean()),
            "V_stall_ms": r["V_stall_ms"], "t_go_s": q(r["t_go_s"][r["responds"]]), "U_emerge_ms": q(r["U_emerge_ms"]), "gamma_emerge_deg": q(r["gamma_emerge_deg"]),
            "t_emerge_s": q(r["t_emerge_s"]),
            "power_to_hold_10ms_submerged_W_per_kg_muscle": {f"k_swim={k}": float(M2.drag_sub(10.0, k) * 10.0 / ETA_PROP / (MUSCLE_FRAC * C.ORG["m_kg"])) for k in (1.0, 2.0, 3.0)},
            "direct_launch_from_emergence": {"glide_range_m": q(direct), "fraction_stalled_or_splashed_within_1m": float(np.mean(direct < 1.0)) if direct.size else None},
            "glide_feed_note": f"after-taxi release at h0={H0_CONT} m, gamma0=0 (continuity); h0=1 m only for comparison with glide-fixed-launch"}
    for tag in ("opt", "pes"):
        to = r[f"took_off_{tag}"]
        g_c, _ = glide_ranges(r[f"V_taxi_end_ms_{tag}"][to], h0=H0_CONT); g_1, _ = glide_ranges(r[f"V_taxi_end_ms_{tag}"][to], h0=1.0)
        summ[f"taxi_{tag}"] = {"start": "V = U_emerge" if tag == "opt" else "V = U_emerge cos(gamma_emerge)", "P_takeoff": float(to.mean()),
                               "P_takeoff_given_emerge": float(to.sum() / max(em.sum(), 1)), "V_end_ms_all_emerged": q(r[f"V_taxi_end_ms_{tag}"][em]),
                               "taxi_time_s_takeoff": q(r[f"taxi_time_s_{tag}"][to]), "glide_range_m_h0_0.1": q(g_c), "glide_range_m_h0_1.0_comparison": q(g_1)}
    # perturbation sweeps (neural latency, muscle corner, emergence-angle command) ------------------------------------
    sweep = {"lat_M_ms": [], "f_m_Hz": [], "gamma_star_deg": [], "P_musc_W_per_kg": []}
    for key, vals in (("lat_M_ms", (5, 10, 20, 40, 80, 160, 320)), ("f_m_Hz", (20, 35, 50, 70)), ("gamma_star_deg", (15, 25, 35, 45, 60)), ("P_musc_W_per_kg", (50, 100, 150, 250, 500, 1000))):
        for v in vals:
            ss = sample(np.random.default_rng(a.seed + 7), 4000, {key: v}); ss["_seed"] = a.seed + 7; rr = simulate(ss)
            sweep[key].append({"value": v, "P_caught": float(rr["caught"].mean()), "P_emerge": float(rr["emerged"].mean()),
                               "P_takeoff_pes": float(rr["took_off_pes"].mean()), "P_takeoff_opt": float(rr["took_off_opt"].mean()),
                               "U_emerge": q(rr["U_emerge_ms"]), "gamma_emerge": q(rr["gamma_emerge_deg"])})
    from scipy.stats import spearmanr
    keys = [k for k in PRIORS if np.ptp(s[k][em]) > 0]
    sens = {k: float(spearmanr(s[k][em], r["U_emerge_ms"][em]).statistic) for k in keys}
    sens_to = {k: float(spearmanr(s[k][em], r["took_off_pes"][em].astype(float)).statistic) for k in keys}
    sens_caught = {k: float(spearmanr(s[k][r["responds"]], r["caught"][r["responds"]].astype(float)).statistic) for k in PRIORS if np.ptp(s[k]) > 0}
    res = {"summary": summ, "sweep": sweep, "spearman_U_emerge": sens, "spearman_takeoff_pes_given_emerge": sens_to, "spearman_caught_given_respond": sens_caught,
           "samples_head": {k: np.asarray(v)[:2000].tolist() for k, v in r.items() if isinstance(v, np.ndarray)}}
    C.dump(out / "results.json", res)
    plot(out, r, direct, sweep, summ)
    ok = all(c["pass"] for c in checks)
    man = {"schema": "frontier.neuro.manifest/1", "id": RID, "project": "flying-fish", "project_scale": "neural", "also_scales": ["organism"],
           "evidence_kind": "simulated, not observed",
           "title": "Mauthner-triggered C-start escape to surface emergence, taxi and glide release (Monte Carlo over sourced priors)",
           "feeds": "engineering/simulation/glide.py integrate() with the glide-fixed-launch organism polar: a launch-speed distribution in place of the assumed fixed V0 = 12 m/s",
           "command": " ".join(["python", "-m", "engineering.neuro.fast_start"] + (argv if argv is not None else sys.argv[1:])), "seed": a.seed,
           "git_head_at_run": C.git_head(), "ran": C.now(), "elapsed_s": time.time() - t0, "env": C.env(),
           "code_sha256": C.code_hashes(["fast_start", "caudal_cpg"]) | {"engineering/simulation/glide.py": C.sha(C.ROOT / "engineering/simulation/glide.py")},
           "inputs": C.inputs([C.ROOT / "engineering/simulation/video/manifest.json", C.ROOT / "engineering/simulation/glide.py", C.ROOT / "engineering/behavior/model.py"]),
           "priors": {k: {"uniform": v[0], "basis": v[1]} for k, v in PRIORS.items()}, "checks": checks, "all_checks_pass": ok, "summary": summ,
           "outputs": {f.name: C.sha(f) for f in sorted(out.glob("*")) if f.suffix in (".json", ".png") and f.name != "manifest.json"}}
    C.dump(out / "manifest.json", man)
    print(json.dumps({"checks": [(c["name"], c["pass"], c.get("detail")) for c in checks], "summary": summ}, indent=1, default=C._default))
    return 0 if ok else 3


def plot(out, r, direct, sweep, summ):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.5)); em = r["emerged"]
    ax[0, 0].hist(r["t_go_s"][r["responds"]] * 1e3, 60, color="C0"); ax[0, 0].axvspan(142, 716, color="g", alpha=.15, label="Preuss 2006: mean looming latencies (goldfish)")
    ax[0, 0].set_xlabel("looming onset -> Mauthner command (ms)"); ax[0, 0].legend(fontsize=8); ax[0, 0].set_title("decision timing")
    ax[0, 1].hist(r["U_emerge_ms"][em], 60, color="C1"); ax[0, 1].axvline(10, color="r", ls=":", label="10 m/s taxi start (Fish 1990)")
    ax[0, 1].axvline(r["V_stall_ms"], color="k", ls="--", label=f"glide stall {r['V_stall_ms']:.1f} m/s"); ax[0, 1].legend(fontsize=8)
    ax[0, 1].set_xlabel("emergence speed (m/s)"); ax[0, 1].set_title(f"emergence speed, P(emerge) = {em.mean():.2f}")
    ax[0, 2].hist(r["gamma_emerge_deg"][em], 60, color="C2"); ax[0, 2].axvspan(30, 35, color="g", alpha=.2, label="Park & Choi: 30-35 deg ATTACK angle at emergence")
    ax[0, 2].set_xlabel("emergence path angle (deg)"); ax[0, 2].legend(fontsize=8); ax[0, 2].set_title("emergence path angle")
    for tag, c in (("pes", "C3"), ("opt", "C4")):
        ax[1, 0].hist(r[f"V_taxi_end_ms_{tag}"][em], 60, alpha=.6, color=c, label=f"taxi start {summ['taxi_' + tag]['start']}")
    ax[1, 0].axvline(1.1 * r["V_stall_ms"], color="k", ls="--", label="take-off threshold 1.1 V_stall")
    ax[1, 0].set_xlabel("speed at end of taxi (m/s)"); ax[1, 0].legend(fontsize=7)
    ax[1, 0].set_title(f"taxi: P(take-off|emerge) pes {summ['taxi_pes']['P_takeoff_given_emerge']:.2f}, opt {summ['taxi_opt']['P_takeoff_given_emerge']:.2f}")
    sw = sweep["lat_M_ms"]; ax[1, 1].plot([w["value"] for w in sw], [w["P_caught"] for w in sw], "o-", label="P(caught)")
    ax[1, 1].plot([w["value"] for w in sw], [w["P_takeoff_pes"] for w in sw], "s-", label="P(take-off), pessimistic taxi"); ax[1, 1].set_xscale("log")
    ax[1, 1].set_xlabel("Mauthner path latency after threshold (ms)"); ax[1, 1].legend(fontsize=8); ax[1, 1].set_title("perturbation: neural latency")
    sw = sweep["P_musc_W_per_kg"]; x = [w["value"] for w in sw]
    ax[1, 2].plot(x, [w["U_emerge"].get("q50", np.nan) for w in sw], "o-", label="median emergence speed (m/s)")
    ax[1, 2].plot(x, [10 * w["P_takeoff_pes"] for w in sw], "s-", label="10 x P(take-off), pessimistic")
    ax[1, 2].axhline(10, color="r", ls=":"); ax[1, 2].set_xscale("log"); ax[1, 2].set_xlabel("muscle power (W/kg muscle), fixed")
    ax[1, 2].legend(fontsize=8); ax[1, 2].set_title("perturbation: muscle power")
    fig.suptitle("M1 fast-start escape -> launch (SIMULATED Monte Carlo, not observed; organism 0.05 kg, L 0.171 m assumed)", fontsize=11)
    fig.tight_layout(); fig.savefig(out / "figure.png", dpi=105); plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
