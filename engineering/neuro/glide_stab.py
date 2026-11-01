"""M3: glide pitch/roll stabilisation with pelvic (pitch: symmetric incidence) and pectoral (roll: differential incidence) fins
as control surfaces, under per-channel sensing delays, sensor noise, fin-actuator lag/saturation and gusts.

    OMP_NUM_THREADS=1 python -m engineering.neuro.glide_stab [--seed 20261101]

Plant geometry: ff-organ's r3-daane printed glider (artifacts/glider/r3-daane/{flight_model,manifest}.json): pectoral pair
2 x 2909 mm^2, MAC 30.9 mm, quarter chord x 56.2 mm, dihedral 7 deg; pelvic pair 2 x 481 mm^2 at x 90.4 mm; dry inertia from
flight_model. Trim CG = NP - 8% MAC (ff-organ r2 rule). Masses: 25 g (ff-organ baseline print) and 50 g (organism baseline), the
50 g case ASSUMING the same geometry, CG and radii of gyration (inertia scaled by mass).
Aerodynamics: linear small-perturbation derivatives (textbook flight mechanics, recalled; no fish polar): Helmbold lift slopes,
downwash, Munk body moment, tail volume; lateral [beta, p, r, phi] with strip-theory roll terms, dihedral C_l_beta, and the caudal
fin as the only vertical surface (area fraction k_v of the pectoral area and arm l_v are ASSUMPTIONS, swept).
Aeroelastic tie-in: ff-organ's dCL = -0.54% at compliance 0.2 (artifacts/aeroelastic/RESULTS.md) as a lift-slope factor; effective
dihedral swept because bending adds dihedral.
Sensing (all outputs derived from the plant state, no fudge factors):
  canals   p, q, r with delay tau_c;
  otolith  gravito-inertial direction: pitch theta_oto = theta + u_dot/g; bank phi_oto = -f_y/g = -Y/(m g) (aero side force), which
           is NOT bank angle in flight: it is set by sideslip;
  vision   theta, phi (horizon / dorsal light) with delay tau_v.
Stability: exact spectral radius of the discrete-time closed loop with one delay chain per sensed channel. Failures: nonlinear
fin-saturation Monte Carlo under Dryden-like gusts and white sensor noise. All SIMULATED, none observed.
"""
from __future__ import annotations
import argparse, json, math, sys, time
import numpy as np
from scipy.linalg import expm

from engineering.neuro import common as C

RID = "m3-glide-stabilizer"
FM = C.ROOT / "artifacts/glider/r3-daane/flight_model.json"
MAN = C.ROOT / "artifacts/glider/r3-daane/manifest.json"
DT = 0.002
DEG = math.pi / 180
TAU_ACT, SAT = 0.02, 15 * DEG          # fin actuator lag (assumption) and incidence authority (assumption)
W_PITCH, W_ROLL, ZETA = 15.0, 10.0, 0.7
T_MC = 5.0                              # s: failure window (flying-fish glides last seconds; assumption)
helm = lambda ar: 2 * math.pi * ar / (2 + math.sqrt(4 + ar * ar))


def geometry():
    H = json.loads(FM.read_text()); M = json.loads(MAN.read_text()); hn = M["hand_neutral_point"]
    pec, pel = hn["pectoral"], hn["pelvic"]; ls = {s["id"]: s for s in H["lifting_surfaces"]}
    pl = ls.get("pelvic") or next(v for k, v in ls.items() if k.startswith("pelvic"))
    y0 = ls["pectoral"]["frame_L"]["origin_mm"][1] * 1e-3; eu = ls["pectoral"]["frame_L"]["e_u"][1]
    yt = pl["frame_L"]["origin_mm"][1] * 1e-3; eut = pl["frame_L"]["e_u"][1]
    Sw = 2 * pec["area_mm2"] * 1e-6; bw = 2 * (y0 + pec["span_in_plane_mm"] * 1e-3 * eu)
    St = 2 * pel["area_mm2"] * 1e-6; bt = 2 * (yt + pel["span_in_plane_mm"] * 1e-3 * eut)
    I = np.array(H["assembled_dry"]["inertia_cg_kg_m2"])
    return {"Sw": Sw, "bw": bw, "ARw": bw ** 2 / Sw, "cw": pec["mac_mm"] * 1e-3, "x_w": pec["quarter_chord_x_mm"] * 1e-3,
            "St": St, "bt": bt, "ARt": bt ** 2 / St, "x_t": pel["quarter_chord_x_mm"] * 1e-3, "dihedral_deg": float(ls["pectoral"]["dihedral_deg"]),
            "vol": hn["body_volume_mm3"] * 1e-9, "np_bracket_m": [v * 1e-3 for v in hn["np_x_mm_bracket"]],
            "Ixx_dry": float(I[0, 0]), "Iyy_dry": float(I[1, 1]), "Izz_dry": float(I[2, 2]), "m_dry": H["assembled_dry"]["mass_kg"],
            "cg_dry": H["assembled_dry"]["cg_m"][0], "X_BALLAST": 0.015}


def derivs(g, sm=0.08, m=0.025, CL=0.6, CD0=0.06, e=0.8, eta=0.9, munk=0.875, cla_factor=1.0 - 0.0054, dihedral_deg=None, k_v=0.15, l_v=0.06, AR_v=1.5):
    a_w = helm(g["ARw"]) * cla_factor; a_t = helm(g["ARt"]) * cla_factor; a_v = helm(AR_v)
    de = 2 * a_w / (math.pi * g["ARw"]); St_r = g["St"] / g["Sw"]
    CLa = a_w + eta * St_r * a_t * (1 - de)
    dCm_body = munk * 2 * g["vol"] / (g["Sw"] * g["cw"])
    x_np = (a_w * g["x_w"] + eta * St_r * a_t * (1 - de) * g["x_t"]) / CLa - dCm_body * g["cw"] / CLa
    x_cg = x_np - sm * g["cw"]; lt = g["x_t"] - x_cg; VH = St_r * lt / g["cw"]
    CD = CD0 + CL ** 2 / (math.pi * e * g["ARw"]); CDa = 2 * CL * CLa / (math.pi * e * g["ARw"])
    V = math.sqrt(2 * m * C.G / (C.RHO_A * g["Sw"] * CL)); gam = -math.atan(CD / CL)
    m_b = max(g["m_dry"] * (g["cg_dry"] - x_cg) / (x_cg - g["X_BALLAST"]), 0.0); m_print = g["m_dry"] + m_b
    Iyy = (g["Iyy_dry"] + m_b * (x_cg - g["X_BALLAST"]) ** 2) * m / m_print
    Izz = (g["Izz_dry"] + m_b * (x_cg - g["X_BALLAST"]) ** 2) * m / m_print
    Ixx = g["Ixx_dry"] * m / m_print
    Gam = (g["dihedral_deg"] if dihedral_deg is None else dihedral_deg) * DEG
    Sv = k_v * g["Sw"]; Vv = Sv * l_v / (g["Sw"] * g["bw"])
    return dict(V=V, gam=gam, CL=CL, CD=CD, CLa=CLa, CDa=CDa, Cma=-CLa * (x_np - x_cg) / g["cw"], Cmq=-2.2 * eta * VH * a_t * lt / g["cw"],
                Cmad=-2 * eta * VH * a_t * lt / g["cw"] * de, CLde=eta * St_r * a_t, Cmde=-eta * VH * a_t, x_np=x_np, x_cg=x_cg, m=m, m_ballast_print=m_b,
                Iyy=Iyy, Ixx=Ixx, Izz=Izz, S=g["Sw"], c=g["cw"], b=g["bw"], sm=sm, dihedral=Gam,
                CYb=-Sv / g["Sw"] * a_v, Clb=-a_w * Gam / 6, Clp=-a_w / 8, Clr=CL / 4, Clda=0.21 * a_w,
                Cnb=Vv * a_v - munk * 2 * g["vol"] / (g["Sw"] * g["bw"]), Cnr=-2 * Vv * a_v * l_v / g["bw"], Cnp=-CL / 8, k_v=k_v, l_v=l_v)


def long_ss(d):
    """x = [u, alpha, q, theta]; input pelvic incidence delta_e; gust w_g (m/s) enters as alpha_g = w_g / V."""
    V, m, S, c, I = d["V"], d["m"], d["S"], d["c"], d["Iyy"]; qd = 0.5 * C.RHO_A * V * V
    Xu = -2 * qd * S * d["CD"] / (m * V); Xa = qd * S * (d["CL"] - d["CDa"]) / m
    Zu = -2 * qd * S * d["CL"] / (m * V * V); Za = -qd * S * (d["CLa"] + d["CD"]) / (m * V); Zd = -qd * S * d["CLde"] / (m * V)
    Ma = qd * S * c * d["Cma"] / I; Mq = qd * S * c * c * d["Cmq"] / (2 * V * I); Mad = qd * S * c * c * d["Cmad"] / (2 * V * I); Md = qd * S * c * d["Cmde"] / I
    sg, cg = math.sin(d["gam"]), math.cos(d["gam"])
    A = np.array([[Xu, Xa, 0, -C.G * cg], [Zu, Za, 1, -C.G * sg / V], [Mad * Zu, Ma + Mad * Za, Mq + Mad, -Mad * C.G * sg / V], [0, 0, 1, 0]])
    B = np.array([0, Zd, Md + Mad * Zd, 0.0]); Bg = np.array([Xa, Za, Ma + Mad * Za, 0.0]) / V
    # sensed channels as rows over [x, actuator]: vision theta, otolith theta + u_dot/g, canal q
    out = {"theta_vis": np.r_[0, 0, 0, 1, 0], "theta_oto": np.r_[A[0] / C.G + np.array([0, 0, 0, 1]), B[0] / C.G], "q_canal": np.r_[0, 0, 1, 0, 0]}
    return A, B, Bg, out


def lat_ss(d):
    """x = [beta, p, r, phi] (stability axes, Ixz neglected); input differential pectoral incidence delta_a; side gust v_g (m/s)."""
    V, m, S, b = d["V"], d["m"], d["S"], d["b"]; qd = 0.5 * C.RHO_A * V * V
    Yb = qd * S * d["CYb"]; Lb, Lp, Lr, Ld = (qd * S * b * d["Clb"], qd * S * b * b * d["Clp"] / (2 * V), qd * S * b * b * d["Clr"] / (2 * V), qd * S * b * d["Clda"])
    Nb, Np, Nr = qd * S * b * d["Cnb"], qd * S * b * b * d["Cnp"] / (2 * V), qd * S * b * b * d["Cnr"] / (2 * V)
    A = np.array([[Yb / (m * V), 0, -1, C.G * math.cos(d["gam"]) / V],
                  [Lb / d["Ixx"], Lp / d["Ixx"], Lr / d["Ixx"], 0],
                  [Nb / d["Izz"], Np / d["Izz"], Nr / d["Izz"], 0],
                  [0, 1, 0, 0]])
    B = np.array([0, Ld / d["Ixx"], 0, 0.0]); Bg = A[:, 0] / V                      # side gust acts like sideslip v_g / V
    out = {"phi_vis": np.r_[0, 0, 0, 1, 0], "phi_oto": np.r_[-Yb / (m * C.G), 0, 0, 0, 0], "p_canal": np.r_[0, 1, 0, 0, 0]}
    return A, B, Bg, out


def disc(A, B, Bg, dt=DT):
    n = A.shape[0]; Mx = np.zeros((n + 2, n + 2)); Mx[:n, :n] = A; Mx[:n, n] = B; Mx[:n, n + 1] = Bg
    E = expm(Mx * dt); return E[:n, :n], E[:n, n], E[:n, n + 1]


def closed_loop(Ad, Bd, rows, K, delays, dt=DT, tau_act=TAU_ACT):
    """Augmented discrete closed loop z = [x, act, delay chains...]; each sensed channel j (row over [x, act]) has its own delay.
    u_cmd = -sum_j K_j y_j(t - tau_j); act' = a act + (1-a) u_cmd. Returns the transition matrix."""
    n = Ad.shape[0]; a = math.exp(-dt / tau_act); nds = [int(round(t / dt)) for t in delays]
    N = n + 1 + sum(nds); M = np.zeros((N, N))
    M[:n, :n] = Ad; M[:n, n] = Bd; M[n, n] = a
    off = n + 1
    for row, k, nd in zip(rows, K, nds):
        if nd == 0:
            M[n, :n + 1] += -(1 - a) * k * row
        else:
            M[off, :n + 1] = row
            for i in range(1, nd):
                M[off + i, off + i - 1] = 1.0
            M[n, off + nd - 1] += -(1 - a) * k
            off += nd
    return M


def radius(*args, **kw):
    return float(np.max(np.abs(np.linalg.eigvals(closed_loop(*args, **kw)))))


def gains(b_rate, w, zeta=ZETA):
    """PD on [attitude, rate] so that attitude'' ~ -w^2 att - 2 zeta w rate given rate_dot ~ b_rate u (airframe terms ignored)."""
    return np.array([w * w, 2 * zeta * w]) / b_rate


def mc(Ad, Bd, Bgd, rows, K, delays, noise, gust_sd, V, Lg, T, rng, att_idx, fail_rad, n_mc=300, tau_act=TAU_ACT):
    n = Ad.shape[0]; a = math.exp(-DT / tau_act); ag = math.exp(-V * DT / Lg); sg = gust_sd * math.sqrt(1 - ag * ag)
    nds = [int(round(t / DT)) for t in delays]; R = np.array(rows)
    x = np.zeros((n_mc, n)); act = np.zeros(n_mc); wg = rng.normal(0, gust_sd, n_mc)
    bufs = [np.zeros((nd + 1, n_mc)) for nd in nds]; failed = np.zeros(n_mc, bool); sq = np.zeros(n_mc); steps = int(T / DT)
    for _ in range(steps):
        y = np.c_[x, act] @ R.T + rng.normal(0, 1, (n_mc, len(rows))) * noise
        ucmd = np.zeros(n_mc)
        for j, nd in enumerate(nds):
            bufs[j] = np.roll(bufs[j], 1, axis=0); bufs[j][0] = y[:, j]; ucmd -= K[j] * bufs[j][nd]
        act = a * act + (1 - a) * np.clip(ucmd, -SAT, SAT)
        x = x @ Ad.T + np.outer(act, Bd) + np.outer(wg, Bgd)
        wg = ag * wg + rng.normal(0, sg, n_mc)
        failed |= np.abs(x[:, att_idx]) > fail_rad; sq += np.where(failed, 0, x[:, att_idx] ** 2); x[failed] = 0
    return float(failed.mean()), float(np.sqrt(sq[~failed].mean() / steps)) if (~failed).any() else float("nan")


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=20261101); a = ap.parse_args(argv)
    t0 = time.time(); rng = np.random.default_rng(a.seed); out = C.OUT / RID; out.mkdir(parents=True, exist_ok=True)
    g = geometry(); checks = []; d25 = derivs(g, m=0.025); d50 = derivs(g, m=0.050)
    # controls -------------------------------------------------------------------------------------------------------
    checks.append({"name": "control: computed neutral point within 3 mm of the repo hand-NP bracket 55.6-58.3 mm (same method family: consistency, not validation)",
                   "pass": g["np_bracket_m"][0] - 0.003 <= d25["x_np"] <= g["np_bracket_m"][1] + 0.003, "detail": d25["x_np"] * 1e3})
    checks.append({"name": "control: trim ballast at SM 8% within 10% of ff-organ r2 baseline ballast 4.69 g", "pass": abs(d25["m_ballast_print"] / 0.0046885 - 1) < 0.10, "detail": d25["m_ballast_print"] * 1e3})
    A, B, Bg, Lo = long_ss(d25)
    checks.append({"name": "control: open-loop longitudinal modes stable at SM 8%", "pass": bool(np.all(np.linalg.eigvals(A).real < 0)), "detail": np.linalg.eigvals(A).tolist()})
    checks.append({"name": "control: SM -10% gives an unstable open-loop pitch mode", "pass": bool(np.any(np.linalg.eigvals(long_ss(derivs(g, sm=-0.10))[0]).real > 0))})
    Ad, Bd, Bgd = disc(A, B, Bg)
    rows = [Lo["theta_vis"], Lo["q_canal"]]; K = gains(B[2], W_PITCH)
    r0 = radius(Ad, Bd, rows, 0 * K, [0.0, 0.0]); r_ol = max(np.max(np.abs(np.linalg.eigvals(Ad))), math.exp(-DT / TAU_ACT))
    checks.append({"name": "control: zero-gain closed loop radius equals open-loop radius", "pass": abs(r0 - r_ol) < 1e-9})
    # delay chain exactness: impulse response of the augmented matrix equals a brute-force simulation with explicit buffers
    Mx = closed_loop(Ad, Bd, rows, K, [0.03, 0.01]); z = np.zeros(Mx.shape[0]); z[1] = 0.01; zz = z.copy()
    for _ in range(400):
        zz = Mx @ zz
    xb = np.zeros(4); xb[1] = 0.01; act = 0.0; hist = [np.r_[xb, act]]; aa = math.exp(-DT / TAU_ACT)
    for k in range(400):
        y0 = rows[0] @ (hist[k - 15] if k - 15 >= 0 else np.zeros(5)); y1 = rows[1] @ (hist[k - 5] if k - 5 >= 0 else np.zeros(5))
        xb = Ad @ xb + Bd * act; act = aa * act + (1 - aa) * (-(K[0] * y0 + K[1] * y1)); hist.append(np.r_[xb, act])
    checks.append({"name": "control: augmented delay matrix reproduces an explicit-buffer simulation (400 steps, delays 30/10 ms)",
                   "pass": bool(np.allclose(zz[:5], hist[-1], atol=1e-12, rtol=1e-9)), "detail": float(np.max(np.abs(zz[:5] - hist[-1])))})
    Alat, Blat, _, _ = lat_ss(d25)
    lam_lat = np.linalg.eigvals(Alat)
    res = {"geometry": g, "trim": {"25g": d25, "50g": d50}, "lat_openloop_eig_25g": lam_lat.tolist()}
    # ---------------------------------------------------------------------------------------- pitch envelopes
    tc = np.arange(0, 0.1001, 0.005); tv = np.arange(0, 0.2001, 0.01); gs = np.geomspace(0.1, 10, 21)
    pitch = {}
    for mk, d in (("25g", d25), ("50g", d50)):
        A, B, Bg, Lo = long_ss(d); Ad, Bd, _ = disc(A, B, Bg); K = gains(B[2], W_PITCH)
        pv = [Lo["theta_vis"], Lo["q_canal"]]; po = [Lo["theta_oto"], Lo["q_canal"]]
        pitch[mk] = {"V_ms": d["V"], "K": K, "openloop_eig": np.linalg.eigvals(A).tolist(),
                     "vision_tc_x_tv": np.array([[radius(Ad, Bd, pv, K, [v, c]) for v in tv] for c in tc]),
                     "otolith_tc_x_gain": np.array([[radius(Ad, Bd, po, k * K, [c, c]) for k in gs] for c in tc]),
                     "vision_tv_x_gain_tc0.01": np.array([[radius(Ad, Bd, pv, k * K, [v, 0.01]) for k in gs] for v in tv])}
    res["pitch"] = pitch
    smd = []
    for s_ in np.linspace(-0.10, 0.30, 21):
        d = derivs(g, sm=s_); A, B, Bg, Lo = long_ss(d); Ad, Bd, _ = disc(A, B, Bg); K = gains(B[2], W_PITCH)
        crit = {}
        for kscale in (0.1, 0.3, 1.0):
            st = [radius(Ad, Bd, [Lo["theta_vis"], Lo["q_canal"]], kscale * K, [v, 0.01]) < 1 for v in tv]
            crit[str(kscale)] = -1.0 if not st[0] else (float(tv[int(np.argmin(st)) - 1]) if not all(st) else float(tv[-1]))
        smd.append({"sm": float(s_), "passive_stable": bool(np.all(np.linalg.eigvals(A).real < 0)), "max_stable_vision_delay_s_by_gain_scale": crit})
    res["pitch_sm_vs_delay"] = smd
    # ---------------------------------------------------------------------------------------- roll envelopes
    roll = {}
    for mk, mm in (("25g", 0.025), ("50g", 0.05)):
        for Gd in (0, 4, 7, 10, 14):
            for kv in (0.05, 0.15, 0.30):
                d = derivs(g, m=mm, dihedral_deg=Gd, k_v=kv); A, B, Bg, Lo = lat_ss(d); Ad, Bd, _ = disc(A, B, Bg); K = gains(B[1], W_ROLL)
                rv = [Lo["phi_vis"], Lo["p_canal"]]; ro = [Lo["phi_oto"], Lo["p_canal"]]
                ent = {"V_ms": d["V"], "K": K, "openloop_eig": np.linalg.eigvals(A).tolist(),
                       "openloop_max_real": float(np.max(np.linalg.eigvals(A).real)),
                       "vision_crit_tv_s_tc0.01": None, "otolith_radius_tc0.01": radius(Ad, Bd, ro, K, [0.01, 0.01]),
                       "vision_radius_tv0.06_tc0.01": radius(Ad, Bd, rv, K, [0.06, 0.01]), "phi_oto_gain_per_rad_beta": float(Lo["phi_oto"][0])}
                st = [radius(Ad, Bd, rv, K, [v, 0.01]) < 1 for v in tv]
                ent["vision_crit_tv_s_tc0.01"] = None if all(st) else (-1.0 if not st[0] else float(tv[int(np.argmin(st))]))
                if Gd == 7 and kv == 0.15:
                    ent["vision_tc_x_tv"] = np.array([[radius(Ad, Bd, rv, K, [v, c]) for v in tv] for c in tc])
                    ent["otolith_tc_x_gain"] = np.array([[radius(Ad, Bd, ro, k * K, [c, c]) for k in gs] for c in tc])
                roll[f"{mk}_G{Gd}_kv{kv}"] = ent
    res["roll"] = roll
    # ---------------------------------------------------------------------------------------- Monte Carlo failures
    mcr = []
    A, B, Bg, Lo = long_ss(d25); Ad, Bd, Bgd = disc(A, B, Bg); Kp = gains(B[2], W_PITCH)
    Al, Bl, Bgl, Ll = lat_ss(d25); Adl, Bdl, Bgdl = disc(Al, Bl, Bgl); Kr = gains(Bl[1], W_ROLL)
    for gust in (0.25, 0.5, 1.0, 2.0):
        for tvv in (0.03, 0.06, 0.1, 0.15):
            row = {"gust_sd_ms": gust, "tau_vision_s": tvv, "tau_canal_s": 0.01}
            row["pitch_vision"] = mc(Ad, Bd, Bgd, [Lo["theta_vis"], Lo["q_canal"]], Kp, [tvv, 0.01], np.array([1 * DEG, 5 * DEG]), gust, d25["V"], 1.0, T_MC, rng, 3, 30 * DEG)
            row["pitch_passive"] = mc(Ad, Bd, Bgd, [Lo["theta_vis"], Lo["q_canal"]], 0 * Kp, [tvv, 0.01], np.array([1 * DEG, 5 * DEG]), gust, d25["V"], 1.0, T_MC, rng, 3, 30 * DEG)
            row["roll_vision"] = mc(Adl, Bdl, Bgdl, [Ll["phi_vis"], Ll["p_canal"]], Kr, [tvv, 0.01], np.array([2 * DEG, 5 * DEG]), gust, d25["V"], 1.0, T_MC, rng, 3, 45 * DEG)
            row["roll_otolith"] = mc(Adl, Bdl, Bgdl, [Ll["phi_oto"], Ll["p_canal"]], Kr, [0.01, 0.01], np.array([2 * DEG, 5 * DEG]), gust, d25["V"], 1.0, T_MC, rng, 3, 45 * DEG)
            row["roll_rate_only"] = mc(Adl, Bdl, Bgdl, [Ll["phi_vis"], Ll["p_canal"]], np.array([0.0, Kr[1]]), [tvv, 0.01], np.array([2 * DEG, 5 * DEG]), gust, d25["V"], 1.0, T_MC, rng, 3, 45 * DEG)
            row["roll_passive"] = mc(Adl, Bdl, Bgdl, [Ll["phi_vis"], Ll["p_canal"]], 0 * Kr, [tvv, 0.01], np.array([2 * DEG, 5 * DEG]), gust, d25["V"], 1.0, T_MC, rng, 3, 45 * DEG)
            mcr.append(row)
    res["monte_carlo"] = mcr
    # ---------------------------------------------------------------------------------------- summary
    def crit_rows(Z, axis_vals):
        return None if (Z < 1).all() else float(axis_vals[int(np.argmax(Z >= 1))])
    k1 = int(np.argmin(np.abs(gs - 1)))
    summ = {"trim_25g": {k: d25[k] for k in ("V", "gam", "x_np", "x_cg", "sm", "m_ballast_print", "Iyy", "Ixx", "Izz")},
            "trim_50g": {k: d50[k] for k in ("V", "gam", "Iyy", "Ixx", "Izz")},
            "pitch_openloop_eig_25g": pitch["25g"]["openloop_eig"], "lat_openloop_eig_25g_G7_kv0.15": roll["25g_G7_kv0.15"]["openloop_eig"],
            "pitch_crit_vision_delay_s_tc0.01_nominal_gain": {mk: crit_rows(np.asarray(pitch[mk]["vision_tv_x_gain_tc0.01"])[:, k1], tv) for mk in pitch},
            "pitch_crit_common_delay_s_otolith_nominal_gain": {mk: crit_rows(np.asarray(pitch[mk]["otolith_tc_x_gain"])[:, k1], tc) for mk in pitch},
            "roll_crit_vision_delay_s_tc0.01": {k: v["vision_crit_tv_s_tc0.01"] for k, v in roll.items()},
            "roll_otolith_stable_tc0.01": {k: v["otolith_radius_tc0.01"] < 1 for k, v in roll.items()},
            "roll_openloop_unstable": {k: v["openloop_max_real"] > 0 for k, v in roll.items()},
            "passive_pitch_stable_sm_range": [min(r["sm"] for r in smd if r["passive_stable"]), max(r["sm"] for r in smd if r["passive_stable"])],
            "notes": "crit = smallest swept delay with closed-loop spectral radius >= 1 (None = stable over the whole sweep; -1 = unstable at zero delay)."}
    C.dump(out / "results.json", res)
    plot(out, res, tc, tv, gs)
    ok = all(c["pass"] for c in checks)
    man = {"schema": "frontier.neuro.manifest/1", "id": RID, "project": "flying-fish", "project_scale": "neural", "also_scales": ["organ", "organism"],
           "evidence_kind": "simulated, not observed",
           "title": "Glide pitch/roll stabiliser: pelvic/pectoral control surfaces, per-channel sensing delay and noise, stability envelope and failure map",
           "command": " ".join(["python", "-m", "engineering.neuro.glide_stab"] + (argv if argv is not None else sys.argv[1:])), "seed": a.seed,
           "git_head_at_run": C.git_head(), "ran": C.now(), "elapsed_s": time.time() - t0, "env": C.env(), "code_sha256": C.code_hashes(["glide_stab"]),
           "inputs": C.inputs([FM, MAN, C.ROOT / "artifacts/aeroelastic/RESULTS.md"]),
           "ties": {"ff-organ wing placement": "trim CG = NP - 8% MAC as in claude-organ r2-glide-sweep; r3-daane geometry; static margin swept -10..30% MAC",
                    "ff-organ aeroelastic": "lift-slope factor 1-0.0054 from artifacts/aeroelastic/RESULTS.md (24x6 mesh, compliance 0.2, alpha 4 deg); effective dihedral swept 0-14 deg"},
           "assumptions": {"actuator_lag_s": TAU_ACT, "fin_authority_deg": 15, "design_bandwidth_rad_s": {"pitch": W_PITCH, "roll": W_ROLL}, "trim_CL": 0.6, "CD0": 0.06, "e": 0.8,
                           "vertical_surface": "caudal fin only, k_v 0.05-0.30 of pectoral area, arm 0.06 m, AR 1.5", "gust": "first-order Dryden-like, L_g 1 m",
                           "noise": "white: attitude 1-2 deg, rate 5 deg/s per sample", "50g_case": "same geometry, CG and radii of gyration as the 25 g print"},
           "checks": checks, "all_checks_pass": ok, "summary": summ,
           "outputs": {f.name: C.sha(f) for f in sorted(out.glob("*")) if f.suffix in (".json", ".png", ".mp4") and f.name != "manifest.json"}}
    C.dump(out / "manifest.json", man)
    print(json.dumps({"checks": [(c["name"], c["pass"], c.get("detail")) for c in checks], "summary": summ}, indent=1, default=C._default))
    return 0 if ok else 3


def plot(out, res, tc, tv, gs):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(16, 9.5))
    lv = np.linspace(-0.01, 0.01, 21)
    def env(a_, Z, x, y, xl, yl, title, logx=False):
        Z = np.asarray(Z); a_.contourf(x, y, np.log10(Z), levels=lv, cmap="RdBu_r", extend="both"); a_.contour(x, y, Z, levels=[1.0], colors="k")
        if logx:
            a_.set_xscale("log")
        a_.set_xlabel(xl); a_.set_ylabel(yl); a_.set_title(title, fontsize=9)
    P = res["pitch"]["25g"]
    env(ax[0, 0], P["vision_tc_x_tv"], tv * 1e3, tc * 1e3, "vision attitude delay (ms)", "canal rate delay (ms)", f"pitch 25 g, V {P['V_ms']:.1f} m/s: vision+canal (blue stable, black = boundary)")
    env(ax[0, 1], P["vision_tv_x_gain_tc0.01"], gs, tv * 1e3, "feedback gain / nominal", "vision delay (ms), canal 10 ms", "pitch 25 g: gain x vision delay", logx=True)
    smd = res["pitch_sm_vs_delay"]
    for ks, mk in (("0.1", "o-"), ("0.3", "s-"), ("1.0", "^-")):
        yv = [r["max_stable_vision_delay_s_by_gain_scale"][ks] for r in smd]
        ax[0, 2].plot([r["sm"] * 100 for r in smd], [v * 1e3 if v >= 0 else -20 for v in yv], mk, label=f"gain x{ks}")
    ax[0, 2].axvline(8, color="g", ls=":", label="ff-organ trim SM 8% MAC"); ax[0, 2].set_xlabel("static margin (% MAC)"); ax[0, 2].set_ylabel("max stable vision delay (ms); -20 = unstable at 0; 200 = whole sweep")
    ax[0, 2].legend(fontsize=8); ax[0, 2].set_title("pitch: static margin vs tolerable delay", fontsize=9)
    R = res["roll"]["25g_G7_kv0.15"]
    env(ax[1, 0], R["vision_tc_x_tv"], tv * 1e3, tc * 1e3, "vision bank delay (ms)", "canal rate delay (ms)", f"roll 25 g (dihedral 7, k_v 0.15): vision+canal")
    env(ax[1, 1], R["otolith_tc_x_gain"], gs, tc * 1e3, "feedback gain / nominal", "vestibular delay (ms)", "roll 25 g: OTOLITH 'bank' (= side force) + canal", logx=True)
    mcr = res["monte_carlo"]
    for key, mk in (("roll_vision", "o-"), ("roll_otolith", "s--"), ("roll_rate_only", "d-."), ("roll_passive", "x:")):
        for gust, col in ((0.5, "C0"), (2.0, "C3")):
            rows = [r for r in mcr if r["gust_sd_ms"] == gust]
            ax[1, 2].plot([r["tau_vision_s"] * 1e3 for r in rows], [r[key][0] for r in rows], mk, color=col, label=f"{key} gust {gust}")
    ax[1, 2].set_xlabel("vision delay (ms)"); ax[1, 2].set_ylabel(f"P(|bank| > 45 deg within {T_MC:.0f} s)"); ax[1, 2].legend(fontsize=6, ncol=2); ax[1, 2].set_title("roll failures (fin +-15 deg saturation)", fontsize=9)
    fig.suptitle("M3 glide stabiliser on the r3-daane geometry (SIMULATED: exact linear-delay stability + saturation Monte Carlo; not observed)", fontsize=11)
    fig.tight_layout(); fig.savefig(out / "figure.png", dpi=100); plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
