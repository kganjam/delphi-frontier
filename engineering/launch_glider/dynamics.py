"""Longitudinal 3-DOF rigid-body launch (slingshot stroke) and flight of the printed glider, batched over draws.

Frames.  World: X forward horizontal, Z up.  The body's forward axis f = (cos th, sin th) and up axis
n = (-sin th, cos th); th is the pitch of the nose above the horizon, q = dth/dt (nose-up positive).  Body points are
given as (xi, zeta): xi ahead of the CG, zeta above it.  A geometry point at (x aft-of-snout, z up) maps to
xi = x_cg - x, zeta = z - z_cg.

State y = [X, Z, th, VX, VZ, q] per draw (arrays of shape (N,)).

Aerodynamics (scenario model; every coefficient is a declared parameter, none is measured for this glider):
  alpha = th - gamma, gamma = atan2(VZ, VX), still air.
  attached:  CL = CLa (alpha - a0) + CL_q qhat,   CD = CD0 + CL^2 / (pi e AR),   qhat = q c / (2 V)
  separated: flat plate CL = k sin 2alpha,  CD = CD0 + 2 k sin^2 alpha, blended by a C1 smoothstep in
             |alpha - a0| over [a_s - d_alpha, a_s + d_alpha], a_s = CL_max/CLa (zero separation below it).  VLM cannot predict stall; the stall
             angle and post-stall shape are brackets.
  pitch moment about the CG:
     M = qd S c Cm0 (1 - s) - qd S CN (x_cp - x_cg) + qd 2 Vol k_munk sin a cos a + qd S c Cm_q qhat
     CN = CL cos a + CD sin a (normal force), x_cp = (1 - s) x_np + s x_cp_post (geometry x, aft of snout).
  The Munk term is the slender-body potential couple (destabilising); x_np is the FINS-ONLY neutral point.
Slingshot stroke: band force F(xi) along a fixed launch direction u = (cos phi, sin phi), applied at the hook,
  xi = hook displacement along u.  Profiles over xi/s, each with mean 1 over displacement (so the work is Fbar s and
  a_mean = Fbar/m is SPEC-010's V0^2/2s when nothing else does work), and peak/mean {1, pi/2, 2}:
  constant 1; quarter-cosine (pi/2) cos(pi xi / 2s); linear (ideal elastic band) 2 (1 - xi/s).  All are
  pre-tensioned (F(0) > 0): the model starts at rest, so a profile with F(0) = 0 never starts.  Fbar is iterated per draw so the CG speed at release
  (xi = s) equals V0.  The band releases completely at xi = s (SPEC-010 rule 1).  Aero and gravity act throughout.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, fields

import numpy as np

G = 9.80665
PROFILES = {"constant": 0, "quarter_cosine": 1, "linear": 2}
PEAK_OVER_MEAN = {"constant": 1.0, "quarter_cosine": math.pi / 2, "linear": 2.0}


def _arr(v, n):
    return np.broadcast_to(np.asarray(v, float), (n,)).astype(float)


@dataclass
class Params:
    """Per-draw parameters (scalars broadcast to N).  Lengths m, angles rad, mass kg."""
    m: object
    Iyy: object
    x_cg: object
    z_cg: object
    S: object
    c: object
    AR: object
    e: object = 0.8
    CLa: object = 4.8
    a0: object = 0.0
    CL_max: object = 0.7
    d_alpha: object = math.radians(2.0)
    k_post: object = 1.0
    CD0: object = 0.06
    x_np: object = 0.058
    x_cp_post: object = 0.07
    Cm0: object = 0.0
    Cm_q: object = -4.0
    CL_q: object = 0.0
    vol: object = 0.0
    k_munk: object = 0.9
    rho: object = 1.225
    lift: object = 1.0          # 0 switches lift and all moments off (ballistic control)
    drag: object = 1.0          # 0 switches drag off (energy control)
    cd_ballistic: object = 0.0  # drag coefficient on S used when lift = 0
    contacts_xi: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))   # (N, P) or (1, P)
    contacts_zeta: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))

    def broadcast(self, n: int) -> "Params":
        kw = {}
        for f in fields(self):
            v = getattr(self, f.name)
            kw[f.name] = (np.broadcast_to(np.atleast_2d(np.asarray(v, float)), (n, np.atleast_2d(v).shape[1])).copy()
                          if f.name.startswith("contacts") else _arr(v, n))
        return Params(**kw)


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def aero(p: Params, alpha, V, q):
    """CL, CD, CN, Cm-moment [N m] / qd, separation weight s.  Vectorised."""
    qhat = np.where(V > 1e-9, q * p.c / (2 * np.maximum(V, 1e-9)), 0.0)
    a_rel = alpha - p.a0
    a_stall = p.CL_max / p.CLa
    u = np.clip((np.abs(a_rel) - (a_stall - p.d_alpha)) / (2 * p.d_alpha), 0.0, 1.0)
    s = u * u * (3 - 2 * u)                  # C1 smoothstep: 0 below a_stall - d_alpha, 1 above a_stall + d_alpha
    cl_att = p.CLa * a_rel + p.CL_q * qhat
    cd_att = p.CD0 + cl_att**2 / (math.pi * p.e * p.AR)
    cl_sep = p.k_post * np.sin(2 * alpha)
    cd_sep = p.CD0 + 2 * p.k_post * np.sin(alpha) ** 2
    CL = (1 - s) * cl_att + s * cl_sep
    CD = (1 - s) * cd_att + s * cd_sep
    CN = CL * np.cos(alpha) + CD * np.sin(alpha)
    x_cp = (1 - s) * p.x_np + s * p.x_cp_post
    M_over_qd = (p.S * p.c * p.Cm0 * (1 - s) - p.S * CN * (x_cp - p.x_cg)
                 + 2 * p.vol * p.k_munk * np.sin(alpha) * np.cos(alpha) + p.S * p.c * p.Cm_q * qhat)
    return CL, CD, CN, M_over_qd, s


def _force_shape(kind: np.ndarray, frac: np.ndarray) -> np.ndarray:
    f = np.clip(frac, 0.0, 1.0)
    return np.select([kind == 0, kind == 1, kind == 2],
                     [np.ones_like(f), (math.pi / 2) * np.cos(0.5 * math.pi * f), 2.0 * (1.0 - f)])


def rhs(p: Params, y: np.ndarray, band: dict | None = None):
    X, Z, th, VX, VZ, q = y
    V = np.hypot(VX, VZ)
    gam = np.arctan2(VZ, VX)
    alpha = _wrap(th - gam)
    qd = 0.5 * p.rho * V * V
    CL, CD, CN, Mq, s = aero(p, alpha, V, q)
    CL = CL * p.lift
    CD = np.where(p.lift > 0, CD, p.cd_ballistic) * p.drag
    Mq = Mq * p.lift
    cg_, sg_ = np.cos(gam), np.sin(gam)
    FX = qd * p.S * (-CL * sg_ - CD * cg_)
    FZ = qd * p.S * (CL * cg_ - CD * sg_) - p.m * G
    M = qd * Mq
    if band is not None:
        f = np.stack([np.cos(th), np.sin(th)])
        n = np.stack([-np.sin(th), np.cos(th)])
        r = band["xi_h"] * f + band["zeta_h"] * n                       # hook relative to CG, world
        hook = np.stack([X, Z]) + r
        xi = (hook[0] - band["hook0"][0]) * band["u"][0] + (hook[1] - band["hook0"][1]) * band["u"][1]
        on = (xi < band["s"]) & band["active"]
        F = np.where(on, band["Fbar"] * _force_shape(band["kind"], xi / band["s"]), 0.0)
        FX = FX + F * band["u"][0]
        FZ = FZ + F * band["u"][1]
        M = M + r[0] * F * band["u"][1] - r[1] * F * band["u"][0]
        extra = {"F": F, "xi": xi, "on": on}
    else:
        extra = {}
    dy = np.stack([VX, VZ, q, FX / p.m, FZ / p.m, M / p.Iyy])
    return dy, {"alpha": alpha, "V": V, "s": s, "CL": CL, "CD": CD, **extra}


def _rk4(p, y, dt, band=None):
    k1, aux = rhs(p, y, band)
    k2, _ = rhs(p, y + 0.5 * dt * k1, band)
    k3, _ = rhs(p, y + 0.5 * dt * k2, band)
    k4, _ = rhs(p, y + dt * k3, band)
    return y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), aux


@dataclass
class Launch:
    V0: object            # target CG speed at release [m/s]
    stroke: object        # effective acceleration stroke s [m]
    phi: object           # launch (band) elevation [rad]
    delta: object = 0.0   # initial body pitch relative to the band line [rad]
    profile: object = 0   # PROFILES code
    xi_h: object = 0.025  # hook ahead of CG [m]
    zeta_h: object = 0.0  # hook above CG [m] (negative = below)


def stroke(p: Params, L: Launch, n: int, dt: float = 1e-4, iters: int = 4, t_max: float = 1.0) -> dict:
    """Integrate the band stroke from rest to release.  Returns release states and launch loads per draw."""
    V0, s, phi = _arr(L.V0, n), _arr(L.stroke, n), _arr(L.phi, n)
    delta, kind = _arr(L.delta, n), _arr(L.profile, n).astype(int)
    xi_h, zeta_h = _arr(L.xi_h, n), _arr(L.zeta_h, n)
    u = np.stack([np.cos(phi), np.sin(phi)])
    th0 = phi + delta
    hook0 = xi_h * np.stack([np.cos(th0), np.sin(th0)]) + zeta_h * np.stack([-np.sin(th0), np.cos(th0)])
    Fbar = p.m * V0**2 / (2 * s)
    for it in range(iters + 1):
        y = np.stack([np.zeros(n), np.zeros(n), th0, np.zeros(n), np.zeros(n), np.zeros(n)])
        band = {"u": u, "s": s, "Fbar": Fbar, "kind": kind, "xi_h": xi_h, "zeta_h": zeta_h, "hook0": hook0,
                "active": np.ones(n, bool)}
        rel = np.full((6, n), np.nan)
        t_rel = np.full(n, np.nan)
        Fpk = np.zeros(n)
        Mpk = np.zeros(n)
        H = np.zeros(n)        # angular impulse of the band about the CG
        t = 0.0
        while np.any(band["active"]) and t < t_max:
            y_new, aux = _rk4(p, y, dt, band)
            F = aux["F"]
            f = np.stack([np.cos(y[2]), np.sin(y[2])])
            nn = np.stack([-np.sin(y[2]), np.cos(y[2])])
            r = xi_h * f + zeta_h * nn
            Mb = r[0] * F * u[1] - r[1] * F * u[0]
            Fpk = np.maximum(Fpk, np.where(band["active"], F, 0.0))
            Mpk = np.where(np.abs(Mb) > np.abs(Mpk), Mb, Mpk)
            H = H + np.where(band["active"], Mb * dt, 0.0)
            _, aux_new = rhs(p, y_new, band)
            done = band["active"] & ~aux_new["on"]
            rel[:, done] = y_new[:, done]
            t_rel[done] = t + dt
            band["active"] = band["active"] & ~done
            y = np.where(band["active"], y_new, y)
            t += dt
        Vrel = np.hypot(rel[3], rel[4])
        if it == iters:
            break
        Fbar = Fbar * (V0 / Vrel) ** 2
    gam = np.arctan2(rel[4], rel[3])
    return {"release_state": rel, "t_release_s": t_rel, "V_release_m_s": Vrel, "gamma_release_rad": gam,
            "alpha_release_rad": _wrap(rel[2] - gam), "q_release_rad_s": rel[5], "theta_release_rad": rel[2],
            "Fbar_N": Fbar, "F_peak_N": Fpk, "a_mean_m_s2": Fbar / p.m, "a_peak_m_s2": Fpk / p.m,
            "band_moment_peak_N_m": Mpk, "band_angular_impulse_N_m_s": H,
            "a_mean_formula_m_s2": V0**2 / (2 * s), "unreleased": int(np.sum(np.isnan(t_rel)))}


def fly(p: Params, y0: np.ndarray, dt: float = 1e-3, t_max: float = 6.0, record_every: int = 0) -> dict:
    """Integrate free flight from y0 until any contact point reaches Z = 0 (or t_max)."""
    n = y0.shape[1]
    y = y0.copy()
    live = np.ones(n, bool)
    out = {k: np.full(n, np.nan) for k in ("range_m", "t_s", "V_impact", "gamma_impact", "theta_impact", "q_impact")}
    out["contact_id"] = np.full(n, -1)
    a_max = np.full(n, -np.inf)
    a_min = np.full(n, np.inf)
    s_max = np.zeros(n)
    V_min = np.full(n, np.inf)
    q_absmax = np.zeros(n)
    X0 = y0[0].copy()
    zc_prev = _contact_z(p, y)
    if np.any(zc_prev.min(axis=1) <= 0):
        raise ValueError("a contact point starts at or below the ground")
    hist = []
    t = 0.0
    k = 0
    while np.any(live) and t < t_max:
        y_new, aux = _rk4(p, y, dt)
        zc = _contact_z(p, y_new)
        zmin = zc.min(axis=1)
        hit = live & (zmin <= 0)
        if np.any(hit):
            zp = zc_prev.min(axis=1)
            frac = np.clip(zp / np.maximum(zp - zmin, 1e-15), 0, 1)
            yi = y + frac * (y_new - y)
            out["range_m"][hit] = (yi[0] - X0)[hit]
            out["t_s"][hit] = t + frac[hit] * dt
            out["V_impact"][hit] = np.hypot(yi[3], yi[4])[hit]
            out["gamma_impact"][hit] = np.arctan2(yi[4], yi[3])[hit]
            out["theta_impact"][hit] = yi[2][hit]
            out["q_impact"][hit] = yi[5][hit]
            out["contact_id"][hit] = np.argmin(zc, axis=1)[hit]
        a_max = np.where(live, np.maximum(a_max, aux["alpha"]), a_max)
        a_min = np.where(live, np.minimum(a_min, aux["alpha"]), a_min)
        s_max = np.where(live, np.maximum(s_max, aux["s"]), s_max)
        V_min = np.where(live, np.minimum(V_min, aux["V"]), V_min)
        q_absmax = np.where(live, np.maximum(q_absmax, np.abs(y[5])), q_absmax)
        live = live & ~hit
        y = np.where(live, y_new, y)
        zc_prev = np.where(live[:, None], zc, zc_prev)
        k += 1
        t += dt
        if record_every and k % record_every == 0:
            hist.append(np.concatenate([[t], y[:, 0]]))
    out.update({"alpha_max_rad": a_max, "alpha_min_rad": a_min, "separation_max": s_max, "V_min": V_min,
                "q_absmax": q_absmax, "airborne_at_t_max": int(np.sum(live)),
                "tumbled": (a_max > math.pi / 2) | (a_min < -math.pi / 2)})
    if record_every:
        out["history_first_draw"] = np.array(hist)
    return out


def _contact_z(p: Params, y):
    Z, th = y[1], y[2]
    return Z[:, None] + p.contacts_xi * np.sin(th)[:, None] + p.contacts_zeta * np.cos(th)[:, None]


def _f(v) -> float:
    return float(np.asarray(v, float).ravel()[0])


def alpha_for_cl(p: Params, CL_target: float) -> float:
    """Smallest alpha >= a0 with CL(alpha) = CL_target on the blended curve (bisection; refuses if unreachable)."""
    lo = _f(p.a0)
    grid = lo + np.radians(np.linspace(0, 40, 4001))
    q1 = p.broadcast(grid.size)
    CL = aero(q1, grid, np.full_like(grid, 10.0), np.zeros_like(grid))[0]
    k = np.nonzero(CL >= CL_target)[0]
    if not len(k):
        raise ValueError(f"CL {CL_target} unreachable (max {CL.max():.3f}); trim impossible")
    a, b = grid[max(k[0] - 1, 0)], grid[k[0]]
    p1 = p.broadcast(1)
    for _ in range(60):
        mid = 0.5 * (a + b)
        if _f(aero(p1, np.atleast_1d(mid), np.atleast_1d(10.0), np.zeros(1))[0]) < CL_target:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b)


def trim(p: Params, CL_trim: float) -> dict:
    """Steady glide at CL_trim (N = 1 parameters; Cm0 must already trim there, see cm0_for_trim).

    alpha_t solves CL(alpha) = CL_trim; gamma from tan(gamma) = -CD/CL; V from lift = W cos(gamma)."""
    a_t = alpha_for_cl(p, CL_trim)
    CL, CD, CN, _, s = aero(p, np.atleast_1d(a_t), np.atleast_1d(10.0), np.zeros(1))
    gam = -math.atan2(_f(CD), _f(CL))
    V = math.sqrt(2 * _f(p.m) * G * math.cos(gam) / (_f(p.rho) * _f(p.S) * _f(CL)))
    return {"alpha_rad": a_t, "gamma_rad": gam, "V_m_s": V, "CL": _f(CL), "CD": _f(CD), "separation": _f(s)}


def trim_state(p: Params, CL_trim: float, X: float = 0.0, Z: float = 1.0) -> np.ndarray:
    t = trim(p, CL_trim)
    g = t["gamma_rad"]
    return np.array([[X], [Z], [g + t["alpha_rad"]], [t["V_m_s"] * math.cos(g)], [t["V_m_s"] * math.sin(g)], [0.0]])


def cm0_for_trim(p: Params, CL_trim: float) -> float:
    """Cm0 (about the fins' NP, attached part) that makes the CG moment vanish at CL_trim, q = 0.

    Decalage is what sets Cm0 on the real model; cfd04's VLM maps one to the other."""
    a_t = alpha_for_cl(p, CL_trim)
    q0 = Params(**{**p.__dict__, "Cm0": np.zeros(1), "Cm_q": np.zeros(1)}).broadcast(1)
    _, _, _, M0, s = aero(q0, np.atleast_1d(a_t), np.atleast_1d(10.0), np.zeros(1))
    if _f(s) >= 1.0:
        raise ValueError("trim alpha is fully separated")
    return -_f(M0) / (_f(p.S) * _f(p.c) * (1 - _f(s)))


def jacobian_modes(p: Params, y_trim: np.ndarray, eps: float = 1e-6) -> dict:
    """Eigenvalues of the numerical Jacobian of the flight RHS at a trim state (N = 1)."""
    J = np.zeros((6, 6))
    for j in range(6):
        d = np.zeros((6, 1))
        h = eps * max(1.0, abs(y_trim[j, 0]))
        d[j, 0] = h
        fp, _ = rhs(p, y_trim + d)
        fm, _ = rhs(p, y_trim - d)
        J[:, j] = (fp - fm)[:, 0] / (2 * h)
    lam = np.linalg.eigvals(J)
    lam = lam[np.argsort(-np.abs(lam))]
    osc = [complex(v) for v in lam if v.imag > 1e-9]
    return {"J": J, "eigenvalues": [[float(v.real), float(v.imag)] for v in lam], "oscillatory": osc,
            "short_period": osc[0] if osc else None, "phugoid": osc[-1] if len(osc) > 1 else None,
            "max_real": float(np.max(lam.real))}
