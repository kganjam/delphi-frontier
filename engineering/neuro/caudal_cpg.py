"""M2: caudal-fin CPG -> tail kinematics -> thrust -> swimming speed, EXTENDING engineering.behavior (not duplicating it).

    OMP_NUM_THREADS=1 python -m engineering.neuro.caudal_cpg [--seed 20261101]

What is reused unchanged: engineering.behavior.model.cpg (Ijspeert-form phase/amplitude chain, 8 segments) and its RK4.
What is added here (all SIMULATED, none observed):
  1. per-segment intrinsic-frequency detuning (descending-drive gradient) and the phase-locking STABILITY analysis of
     the reused chain (numerical locking + Jacobian eigenvalue, against the closed form for a unidirectional chain);
  2. a muscle low-pass  H(f) = H0 / sqrt(1 + (f/f_m)^2)  (assumed form; f_m swept 20-70 Hz, cf. Wardle 1975 twitch limit);
  3. submerged thrust by Lighthill elongated-body theory (EBT)  T = (m_a w^2 H^2 / 4)(1 - (U/c)^2),  m_a = pi/4 rho s^2,
     c = f*lambda, lambda set by the CPG head-to-tail phase lag;
  4. surface-taxi thrust of the immersed hypocaudal lobe as a quasi-steady feathering foil (assumed passive feathering);
  5. speed dynamics (m + m_add) dU/dt = T - D and its equilibrium stability d(T-D)/dU < 0;
  6. a re-run of behavior-cpg's own servo across its declared 15-45 Hz to show where its designed actuator saturates.
Locking condition (kept after review): in the reused unidirectional chain every follower locks to the LEADER's realised
frequency, so c sin(psi_i - lag) = w_0 - w_i = -i*dw; the binding link is the last one, |(N-1) dw| <= c. A reviewer (gemini-4-argon)
proposed |dw| <= c per link; that would hold only if each segment ran at its own intrinsic frequency, which a locked chain does not.
The numerical integration decides: see the locking check in the manifest.
Organism: 0.05 kg baseline shared with the glide manifest; L = 0.171 m from an assumed condition factor.
"""
from __future__ import annotations
import argparse, json, math, sys, time
import numpy as np
from scipy.optimize import brentq

from engineering.behavior import model as bm
from engineering.neuro import common as C

RID = "m2-caudal-cpg"
MUSCLE_FRAC = 0.5      # assumption: axial muscle fraction of body mass (same as fast_start)
L = C.L_BODY
NOM = {"H_over_L": 0.10, "span_over_L": 0.25, "f_m_Hz": 35.0, "k_swim": 2.0, "S_wet_over_L2": 0.40, "k_form": 0.2,
       "m_add_frac": 0.10, "lobe_area_over_L2": 0.010, "lobe_AR": 3.0, "alpha_feather_deg": 12.0}
BASIS = {"H_over_L": "assumption; ~0.1 L half-amplitude in fast steady swimming (recalled general fish kinematics), swept 0.05-0.15",
         "span_over_L": "assumption; caudal fin depth, swept 0.2-0.3", "f_m_Hz": "assumption form; corner swept 20-70 Hz (wardle1975, edgerton_breder1941)",
         "k_swim": "assumption; swimming drag augmentation over rigid-body drag, swept 1-3", "S_wet_over_L2": "assumption; fusiform wetted area",
         "k_form": "assumption", "m_add_frac": "assumption; longitudinal added mass", "lobe_area_over_L2": "assumption; immersed hypocaudal lobe during taxi, swept x0.5-2",
         "lobe_AR": "assumption", "alpha_feather_deg": "assumption; passive feathering holds effective attack angle at or below this"}


# ---------------------------------------------------------------- neural: reuse behavior CPG, add detuning
def cpg_steady(f_Hz, coupling_s, lag_rad, detune_Hz_per_seg=0.0, dt=1e-4, T=0.6, seed=0):
    """Integrate ONLY the CPG states of engineering.behavior.model (phase, amplitude, amplitude rate) with an added per-segment
    detuning. Returns locked flag, mean final inter-segment phase differences, leader frequency."""
    p = dict(bm.DEFAULTS, frequency_Hz=f_Hz, coupling_s=coupling_s, phase_lag_rad=lag_rad)   # validate() bypassed on purpose: f up to 80 Hz
    det = 2 * math.pi * detune_Hz_per_seg * np.arange(bm.N)
    rng = np.random.default_rng(seed)
    st = np.zeros((5, bm.N)); st[0] = -np.arange(bm.N) * lag_rad + 0.3 * rng.standard_normal(bm.N)

    def d(y):
        vel, acc, *_ = bm.cpg(y, p)
        out = np.zeros_like(y); out[0] = vel + det; out[1] = y[2]; out[2] = acc
        return out
    n = int(round(T / dt)); keep = []
    for k in range(n):
        st = bm.rk4(st, dt, d)
        if k * dt >= T - 0.15:
            keep.append(st[0].copy())
    ph = np.array(keep); dpsi = ph[:, :-1] - ph[:, 1:]
    spread = float(np.max(np.std(dpsi, axis=0)))
    return {"locked": spread < 0.05, "psi_rad": dpsi[-1].tolist(), "psi_spread_rad": spread,
            "leader_Hz": float((ph[-1, 0] - ph[0, 0]) / (2 * math.pi * (len(ph) - 1) * dt)), "amp": st[1].tolist()}


def lock_analytic(coupling_s, detune_Hz_per_seg, lag_rad):
    """Unidirectional chain (as in behavior.model: segment i driven only by i-1, unit amplitude at steady state):
    lock iff |dw_i - dw_0| <= c for all i; stable branch eigenvalue -sqrt(c^2 - dw^2); psi_i = lag + arcsin(dw/c)."""
    dw = 2 * math.pi * detune_Hz_per_seg * np.arange(1, bm.N)        # follower minus leader
    ok = np.all(np.abs(dw) <= coupling_s)
    lam = -np.sqrt(np.clip(coupling_s ** 2 - dw ** 2, 0, None))
    psi = lag_rad + np.arcsin(np.clip(-dw / coupling_s, -1, 1))       # c sin(psi-lag) = dw_0 - dw_i
    return {"locked": bool(ok), "slowest_eig_s": float(lam.max()) if ok else 0.0, "psi_rad": psi.tolist()}


def jacobian_eigs(coupling_s, psi, lag_rad):
    """Numerical Jacobian of the phase-difference flow of the reused chain at a locked state (unit amplitude)."""
    p = dict(bm.DEFAULTS, coupling_s=coupling_s, phase_lag_rad=lag_rad)
    th0 = -np.concatenate([[0.0], np.cumsum(psi)])

    def flow(th):
        st = np.zeros((5, bm.N)); st[0] = th; st[1] = 1.0
        v = bm.cpg(st, p)[0]
        return v[:-1] - v[1:]
    Jm = np.zeros((bm.N - 1, bm.N - 1)); eps = 1e-6
    for j in range(bm.N - 1):
        dth = np.zeros(bm.N); dth[j + 1:] -= eps          # perturb psi_j: shift all segments caudal of j
        Jm[:, j] = (flow(th0 + dth) - flow(th0 - dth)) / (2 * eps)
    return np.linalg.eigvals(Jm)


def wavelength(psi):
    return 2 * math.pi * L / float(np.sum(psi))          # one body length spans N-1 intervals


# ---------------------------------------------------------------- muscle + hydrodynamics
def muscle_amp(f, H0, f_m):
    return H0 / np.sqrt(1 + (np.asarray(f) / f_m) ** 2)


def ebt_thrust(U, f, H, lam, s, rho=C.RHO_W):
    m_a = math.pi / 4 * rho * s ** 2
    w = 2 * math.pi * np.asarray(f)
    c = np.asarray(f) * lam
    return m_a * w ** 2 * H ** 2 / 4 * (1 - (np.asarray(U) / c) ** 2)


def ebt_thrust_numeric(U, f, H, lam, s, rho=C.RHO_W, n=4096):
    """Phase-average of the Lighthill trailing-edge expression (control for the closed form)."""
    m_a = math.pi / 4 * rho * s ** 2; w = 2 * math.pi * f; k = 2 * math.pi / lam
    ph = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ht = w * H * np.sin(ph); hx = -k * H * np.sin(ph)
    return 0.5 * m_a * (np.mean(ht ** 2) - U ** 2 * np.mean(hx ** 2))


def cf(Re):
    return 0.074 * np.asarray(Re) ** -0.2


def drag_sub(U, k_swim, P=NOM, rho=C.RHO_W):
    U = np.asarray(U, float)
    Sw = P["S_wet_over_L2"] * L ** 2
    return 0.5 * rho * U ** 2 * Sw * cf(np.maximum(U, 1e-3) * L / C.NU_W) * (1 + P["k_form"]) * k_swim


def lobe_thrust(U, f, H, P=NOM, rho=C.RHO_W, n=256):
    """Immersed hypocaudal lobe during taxi: quasi-steady foil with passive feathering (effective attack angle limited to
    alpha_feather). Phase-averaged forward force minus lobe profile/induced drag. Assumed model, no source calibration."""
    S = P["lobe_area_over_L2"] * L ** 2; AR = P["lobe_AR"]; a_max = math.radians(P["alpha_feather_deg"])
    cla = 2 * math.pi * AR / (AR + 2)
    U = np.atleast_1d(np.asarray(U, float))[:, None]
    ph = np.linspace(0, 2 * math.pi, n, endpoint=False)[None, :]
    v = np.abs(2 * math.pi * f * H * np.cos(ph))
    W = np.sqrt(U ** 2 + v ** 2); beta = np.arctan2(v, U)
    ae = np.minimum(beta, a_max)
    CL = cla * ae; CD = 2 * cf(np.maximum(W, 1e-3) * math.sqrt(S / AR) / C.NU_W) + CL ** 2 / (math.pi * 0.8 * AR)
    q = 0.5 * rho * W ** 2 * S
    return np.mean(q * (CL * np.sin(beta) - CD * np.cos(beta)), axis=1)


def air_drag_taxi(V):
    """Air drag of the airborne body on the organism glide polar, CL limited to what supports the weight (or CL_max)."""
    q = 0.5 * C.RHO_A_GLIDE * np.asarray(V) ** 2 * C.ORG["S_m2"]
    CLn = np.minimum(C.ORG["m_kg"] * C.G / q, C.ORG["CL_max"])
    return q * (C.ORG["CD0"] + CLn ** 2 / (math.pi * C.ORG["e"] * C.ORG["AR"]))


def taxi_water_drag(V, wet_frac, t_over_L=0.01):
    """Water drag the taxiing fish still pays besides the lobe's own foil drag:
    spray drag of a surface-piercing strut, D = 0.24 * 1/2 rho V^2 t^2 (Hoerner, Fluid-Dynamic Drag, recalled_not_reread), lobe
    thickness t = 0.01 L (assumption), plus a residual wetted-hull fraction wet_frac of the submerged rigid-body drag (k_swim = 1).
    wet_frac is unknown (belly/anal-fin contact, planing); it is swept, not sourced."""
    V = np.asarray(V, float)
    return 0.24 * 0.5 * C.RHO_W * V ** 2 * (t_over_L * L) ** 2 + wet_frac * drag_sub(V, 1.0)


def terminal_speed(f, H, lam, s, k_swim):
    g = lambda U: ebt_thrust(U, f, H, lam, s) - drag_sub(U, k_swim)
    hi = f * lam * (1 - 1e-9)
    if g(1e-3) <= 0:
        return 0.0
    return float(brentq(g, 1e-3, hi))


def bainbridge(f):
    """Empirical U = L/4 (3f - 4) (Bainbridge 1958, recalled; dace/trout/goldfish 0-20 Hz). Comparison only."""
    return L / 4 * (3 * np.asarray(f) - 4)


# ---------------------------------------------------------------- run
def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=20261101); a = ap.parse_args(argv)
    t0 = time.time(); rng = np.random.default_rng(a.seed)
    out = C.OUT / RID; out.mkdir(parents=True, exist_ok=True)
    checks = []
    lag0 = bm.DEFAULTS["phase_lag_rad"]; c0 = bm.DEFAULTS["coupling_s"]
    lam0 = wavelength(np.full(bm.N - 1, lag0))

    # controls -------------------------------------------------------------------------------------------------
    s0 = NOM["span_over_L"] * L; H0 = NOM["H_over_L"] * L
    for U in (0.0, 1.0, 3.0):
        num, cl = ebt_thrust_numeric(U, 20.0, H0, lam0, s0), float(ebt_thrust(U, 20.0, H0, lam0, s0))
        checks.append({"name": f"EBT closed form equals phase-averaged Lighthill expression at U={U}", "pass": abs(num - cl) <= 1e-9 * max(1, abs(cl)), "detail": [num, cl]})
    checks.append({"name": "EBT thrust is zero when U equals wave speed c", "pass": abs(float(ebt_thrust(20 * lam0, 20, H0, lam0, s0))) < 1e-12})
    checks.append({"name": "zero amplitude gives zero EBT thrust and zero lobe thrust minus drag <= 0", "pass": float(ebt_thrust(2, 20, 0, lam0, s0)) == 0 and float(lobe_thrust(5, 50, 0)[0]) <= 0})
    st_a = cpg_steady(30.0, c0, lag0, 0.0, dt=1e-4); st_b = cpg_steady(30.0, c0, lag0, 0.0, dt=5e-5)
    checks.append({"name": "reused CPG: dt halving changes final phase lags < 1e-3 rad", "pass": float(np.max(np.abs(np.array(st_a["psi_rad"]) - st_b["psi_rad"]))) < 1e-3,
                   "detail": float(np.max(np.abs(np.array(st_a["psi_rad"]) - st_b["psi_rad"])))})
    checks.append({"name": "reused CPG locks at the behavior-cpg defaults with lag 2pi/7", "pass": st_a["locked"] and float(np.max(np.abs(np.array(st_a["psi_rad"]) - lag0))) < 1e-3})

    # stability analysis: coupling x detuning --------------------------------------------------------------
    couplings = np.array([10, 20, 40, 60, 80, 120.0]); detunes = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6.0])
    lock_rows = []
    for c in couplings:
        for g in detunes:
            num = cpg_steady(30.0, c, lag0, g, dt=1e-4, T=1.0, seed=int(rng.integers(1 << 30)))
            an = lock_analytic(c, g, lag0)
            row = {"coupling_s": c, "detune_Hz_per_seg": g, "numeric_locked": num["locked"], "analytic_locked": an["locked"],
                   "psi_spread_rad": num["psi_spread_rad"], "analytic_slowest_eig_s": an["slowest_eig_s"]}
            if num["locked"]:
                psi = np.array(num["psi_rad"]) % (2 * math.pi)
                row["lambda_over_L"] = wavelength(psi) / L
                row["numeric_jac_max_real_eig_s"] = float(np.max(np.real(jacobian_eigs(c, psi, lag0))))
                row["psi_err_vs_analytic_rad"] = float(np.max(np.abs(psi - np.array(an["psi_rad"]) % (2 * math.pi))))
            lock_rows.append(row)
    agree = [r["numeric_locked"] == r["analytic_locked"] for r in lock_rows]
    border = [r for r in lock_rows if abs(2 * math.pi * r["detune_Hz_per_seg"] * (bm.N - 1) / r["coupling_s"] - 1) < 0.15]
    checks.append({"name": "numerical locking matches the analytic condition |(N-1) dw| <= c in every case, including the 5 within 15% of the boundary",
                   "pass": all(agree),
                   "detail": {"agree": int(sum(agree)), "of": len(agree), "near_boundary": len(border)}})
    lk = [r for r in lock_rows if r["numeric_locked"] and r["analytic_locked"]]
    checks.append({"name": "numerical Jacobian slowest eigenvalue matches -sqrt(c^2-dw^2) within 2% where locked",
                   "pass": all(abs(r["numeric_jac_max_real_eig_s"] - r["analytic_slowest_eig_s"]) <= 0.02 * abs(r["analytic_slowest_eig_s"]) + 1e-6 for r in lk if r["analytic_slowest_eig_s"] < -1),
                   "detail": [[r["coupling_s"], r["detune_Hz_per_seg"], r["numeric_jac_max_real_eig_s"], r["analytic_slowest_eig_s"]] for r in lk[:6]]})

    # perturbation sweep: frequency x amplitude x muscle corner x wavelength x drag factor -----------------------
    fs = np.linspace(4, 80, 39); HL = np.array([0.05, 0.075, 0.10, 0.125, 0.15]); fms = np.array([20, 35, 50, 70.0])
    lams = np.array([0.8, 1.0, 1.2]) * L; ks = np.array([1.0, 2.0, 3.0])
    U = np.zeros((len(fs), len(HL), len(fms), len(lams), len(ks)))
    for i, f in enumerate(fs):
        for j, h in enumerate(HL):
            for k, fm in enumerate(fms):
                Hf = float(muscle_amp(f, h * L, fm))
                for l, lam in enumerate(lams):
                    for m_, kk in enumerate(ks):
                        U[i, j, k, l, m_] = terminal_speed(f, Hf, lam, s0, kk)
    # equilibrium stability: d(T-D)/dU at every equilibrium (finite difference)
    worst = -np.inf
    for i in range(0, len(fs), 4):
        for k in range(len(fms)):
            Hf = float(muscle_amp(fs[i], H0, fms[k])); u = U[i, 2, k, 1, 1]
            if u > 0.05:
                dg = (ebt_thrust(u * 1.001, fs[i], Hf, lam0, s0) - drag_sub(u * 1.001, 2) - ebt_thrust(u * 0.999, fs[i], Hf, lam0, s0) + drag_sub(u * 0.999, 2)) / (0.002 * u)
                worst = max(worst, float(dg))
    checks.append({"name": "every swept speed equilibrium is stable: d(T-D)/dU < 0", "pass": worst < 0, "detail": worst})
    nom = U[:, 2, 1, 1, 1]
    st = 2 * fs * muscle_amp(fs, H0, NOM["f_m_Hz"]) / np.maximum(nom, 1e-9)
    bb = bainbridge(fs)
    # mechanical power the muscle must deliver at each nominal equilibrium: P = T U / eta_Froude, eta = (1 + U/c)/2 (EBT)
    eta_f = (1 + nom / (fs * lam0)) / 2
    P_req = drag_sub(nom, NOM["k_swim"]) * nom / eta_f / (MUSCLE_FRAC * C.ORG["m_kg"])
    lowf = fs <= 20
    ratio = (nom[lowf] / np.maximum(bb[lowf], 1e-9))
    checks.append({"name": "comparison (not a fit): nominal EBT speed within factor 2 of Bainbridge empirical U=L/4(3f-4) for 8-20 Hz",
                   "pass": bool(np.all((ratio[fs[lowf] >= 8] > 0.5) & (ratio[fs[lowf] >= 8] < 2))), "detail": dict(zip(map(float, fs[lowf]), map(float, ratio)))})

    # taxi: lobe thrust (power-capped) vs air drag + surface-piercing spray drag + residual wetted-hull drag
    Vt = np.linspace(2, 25, 47); taxi = {}
    for f in (30, 50, 70):
        for fm in (35, 70):
            Hf = float(muscle_amp(f, H0, fm)); T = lobe_thrust(Vt, f, Hf)
            Dair = air_drag_taxi(Vt)
            vmax = float(Vt[np.where(T - Dair > 0)[0].max()]) if (T - Dair > 0).any() else None
            grid = {}
            for P in (50, 150, 250):
                Tc = np.minimum(T, 0.75 * P * MUSCLE_FRAC * C.ORG["m_kg"] / Vt)
                for kw in (0.0, 0.02, 0.05, 0.10):
                    net = Tc - Dair - taxi_water_drag(Vt, kw)
                    grid[f"P{P}_wet{kw}"] = float(Vt[np.where(net > 0)[0].max()]) if (net > 0).any() else None
            taxi[f"f{f}_fm{int(fm)}"] = {"V": Vt.tolist(), "T_lobe_N": T.tolist(), "D_air_N": Dair.tolist(), "D_water_wet0.02_N": taxi_water_drag(Vt, 0.02).tolist(),
                                         "V_max_taxi_ms": vmax, "V_max_taxi_capped_by_power_and_wet_fraction_ms": grid}

    # behavior-cpg's own servo across its declared band ------------------------------------------------------
    servo = []
    for f in (15, 25, 35, 45):
        r = bm.simulate({"frequency_Hz": float(f)})["metrics"]
        servo.append({"frequency_Hz": f, **{k: r[k] for k in ("tracking_relative_rms_after_0_5s", "sampled_torque_saturation_fraction", "peak_abs_angle_rad", "leader_frequency_Hz")}})

    res = {"lambda0_over_L": lam0 / L, "terminal_speed_ms": {"axes": {"f_Hz": fs, "H_over_L": HL, "f_m_Hz": fms, "lambda_over_L": lams / L, "k_swim": ks}, "U": U},
           "nominal_curve": {"f_Hz": fs, "U_ms": nom, "U_BL_s": nom / L, "St": st, "bainbridge_ms": bb, "P_req_W_per_kg_muscle": P_req,
                             "U_at_power_cap_ms": {str(P): float(np.interp(P, P_req, nom)) if P_req.max() > P else float(nom.max()) for P in (50, 150, 250)}},
           "lock": lock_rows, "taxi": taxi, "behavior_servo": servo}
    C.dump(out / "results.json", res)
    plot(out, res)
    manifest = {"schema": "frontier.neuro.manifest/1", "id": RID, "project": "flying-fish", "project_scale": "neural",
                "also_scales": ["organ", "organism"], "evidence_kind": "simulated, not observed",
                "title": "Caudal-fin CPG to thrust: phase-locking stability and frequency/amplitude/muscle sweep (extends behavior-cpg)",
                "extends": "behavior-cpg (engineering/behavior/model.py cpg() and rk4() imported unchanged)",
                "command": " ".join(["python", "-m", "engineering.neuro.caudal_cpg"] + (argv or sys.argv[1:])), "seed": a.seed,
                "git_head_at_run": C.git_head(), "ran": C.now(), "elapsed_s": time.time() - t0, "env": C.env(),
                "code_sha256": C.code_hashes(["caudal_cpg"]) | {C.rel(bm.__file__): C.sha(bm.__file__)},
                "inputs": C.inputs([C.ROOT / "engineering/behavior/model.py", C.ROOT / "engineering/simulation/video/manifest.json"]),
                "parameters": {k: {"value": v, "basis": BASIS[k]} for k, v in NOM.items()} | {"L_m": {"value": L, "basis": "assumption: m=0.05 kg baseline with condition factor 1.0"}},
                "checks": checks, "all_checks_pass": all(c["pass"] for c in checks),
                "headline": headline(res, L),
                "outputs": {f.name: C.sha(f) for f in sorted(out.glob("*")) if f.suffix in (".json", ".png") and f.name != "manifest.json"}}
    C.dump(out / "manifest.json", manifest)
    print(json.dumps({"checks": [(c["name"], c["pass"]) for c in checks], "headline": manifest["headline"]}, indent=1, default=C._default))
    return 0 if manifest["all_checks_pass"] else 3


def headline(res, L):
    nc = res["nominal_curve"]; U = np.array(nc["U_ms"]); f = np.array(nc["f_Hz"])
    Ut = np.array(res["terminal_speed_ms"]["U"])
    return {"nominal_peak_U_ms": float(U.max()), "nominal_peak_at_f_Hz": float(f[U.argmax()]),
            "sweep_max_U_ms": float(Ut.max()), "sweep_max_U_BL_s": float(Ut.max() / L),
            "taxi_V_max_ms_no_power_cap": {k: v["V_max_taxi_ms"] for k, v in res["taxi"].items()},
            "taxi_V_max_ms_capped_by_power_and_wet_fraction": {k: v["V_max_taxi_capped_by_power_and_wet_fraction_ms"] for k, v in res["taxi"].items()},
            "submerged_U_at_power_cap_W_per_kg": nc["U_at_power_cap_ms"],
            "reading": "Submerged EBT speed is capped below the body-wave speed f*lambda; the binding limit is muscle power, not frequency: "
                       "see submerged_U_at_power_cap against the ~10 m/s taxi start in Fish 1990."}


def plot(out, res):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 2, figsize=(12, 8.5))
    nc = res["nominal_curve"]; ax0 = ax[0, 0]
    A = res["terminal_speed_ms"]["axes"]; U = np.asarray(res["terminal_speed_ms"]["U"])
    for k, fm in enumerate(A["f_m_Hz"]):
        ax0.plot(A["f_Hz"], U[:, 2, k, 1, 1], label=f"muscle corner {fm:.0f} Hz")
    ax0.fill_between(A["f_Hz"], U[:, 0, 0, 0, 2], U[:, 4, 3, 2, 0], color="0.85", label="full sweep envelope")
    ax0.plot(nc["f_Hz"], np.clip(nc["bainbridge_ms"], 0, None), "k--", lw=1, label="Bainbridge 1958 empirical (recalled)")
    ax0.axhline(10, color="r", ls=":", lw=1); ax0.text(5, 10.2, "~10 m/s taxi start (Fish 1990 p.397)", color="r", fontsize=8)
    ax0.set_xlabel("CPG tail-beat frequency (Hz)"); ax0.set_ylabel("terminal submerged speed (m/s)"); ax0.legend(fontsize=7); ax0.set_title("EBT thrust = drag equilibria (simulated)")
    ax1 = ax[0, 1]; ax1.plot(nc["f_Hz"], nc["St"], label="St"); ax1.axhspan(0.2, 0.4, color="g", alpha=0.15, label="0.2<St<0.4 (Taylor 2003)")
    ax1.set_ylim(0, 0.8); ax1.set_xlabel("frequency (Hz)"); ax1.set_ylabel("St = 2fH/U at equilibrium"); ax1.legend(fontsize=8, loc="upper left")
    a2 = ax1.twinx(); a2.semilogy(nc["f_Hz"], nc["P_req_W_per_kg_muscle"], "r-", label="power required"); a2.axhspan(50, 250, color="r", alpha=0.08)
    a2.set_ylabel("required muscle power (W/kg muscle); band = assumed 50-250", color="r"); ax1.set_title("Strouhal number and power, nominal")
    ax2 = ax[1, 0]; rows = res["lock"]; cs = sorted({r["coupling_s"] for r in rows}); ds = sorted({r["detune_Hz_per_seg"] for r in rows})
    Z = np.full((len(cs), len(ds)), np.nan)
    for r in rows:
        Z[cs.index(r["coupling_s"]), ds.index(r["detune_Hz_per_seg"])] = r.get("lambda_over_L", np.nan)
    im = ax2.imshow(Z, origin="lower", aspect="auto", cmap="viridis", extent=[-0.5, len(ds) - 0.5, -0.5, len(cs) - 0.5])
    ax2.set_xticks(range(len(ds)), ds); ax2.set_yticks(range(len(cs)), cs); plt.colorbar(im, ax=ax2, label="body wavelength / L (blank = not phase-locked)")
    bnd = [c / (2 * math.pi * (8 - 1)) for c in cs]
    ax2.plot(np.interp(bnd, ds, range(len(ds))), range(len(cs)), "r-", label="analytic lock boundary |dw|=c")
    ax2.set_xlabel("intrinsic-frequency detuning (Hz per segment)"); ax2.set_ylabel("coupling c (1/s)"); ax2.legend(fontsize=8); ax2.set_title("Reused behavior-cpg chain: phase-locking stability")
    ax3 = ax[1, 1]
    for key, v in res["taxi"].items():
        ax3.plot(v["V"], np.array(v["T_lobe_N"]) * 1e3, label=f"lobe thrust {key}")
    v = next(iter(res["taxi"].values())); ax3.plot(v["V"], np.array(v["D_air_N"]) * 1e3, "k-", lw=2, label="air drag, 0.05 kg glide polar")
    ax3.plot(v["V"], (np.array(v["D_air_N"]) + np.array(v["D_water_wet0.02_N"])) * 1e3, "k--", lw=2, label="+ spray + 2% wetted hull")
    for P in (50, 150, 250):
        ax3.plot(v["V"], 0.75 * P * MUSCLE_FRAC * C.ORG["m_kg"] / np.array(v["V"]) * 1e3, ":", color="0.4", lw=1)
    ax3.text(18, 0.75 * 150 * MUSCLE_FRAC * C.ORG["m_kg"] / 18 * 1e3, "power caps 50/150/250 W/kg", fontsize=7, color="0.3"); ax3.set_yscale("log")
    ax3.set_xlabel("taxi speed (m/s)"); ax3.set_ylabel("force (mN)"); ax3.legend(fontsize=7); ax3.set_title("Surface taxi: immersed-lobe thrust vs air drag")
    fig.suptitle("M2 caudal CPG -> thrust (SIMULATED, not observed; organism 0.05 kg, L=0.171 m assumed)", fontsize=11)
    fig.tight_layout(); fig.savefig(out / "figure.png", dpi=110); plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
