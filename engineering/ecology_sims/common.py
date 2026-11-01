"""Shared phenotype -> launch -> glide -> escape model for the ecological and collective scales (claude-eco, 2026-11-01).

EVIDENCE KIND: SIMULATED under declared assumptions. A model of reachability or of escape is not evidence that any lineage
evolved this way, nor a measurement of any fish. Every input below is tagged with its source and read level.

Phenotype z = (p, A, M, c):
  p = pectoral fin length / standard length        (Daane et al. 2021 Data S1A measures exactly this ratio)
  A = individual pectoral fin aspect ratio = L_fin^2 / area_one_fin
  M = body mass, kg
  c = hypocaudal (lower caudal lobe) share of caudal area (0.5 = symmetric tail; Fish 1990 pooled flying fish 0.631)

Chain (all SI):
  SL      = (1000 M / a_LW)^(1/3) / 100            FishBase length-weight form W[g] = a SL[cm]^3 (b fixed at 3)
  L_fin   = p SL;  w = 0.1 SL (assumption);  S = 2 L_fin^2/A + w L_fin/A;  b = 2 L_fin + w;  AR = b^2 / S
  phi     = min(1, 0.5 rho V_exit^2 S CL_max / (M g))    fraction of weight carried aerodynamically at water exit
  V0      = V_exit + dV_taxi * s(c) * phi,  s(c) = clip((c-0.5)/(0.631-0.5), 0, 1)
            (taxi surrogate: tail sculling adds speed only while fins carry the body; Fish 1990 p.397 citing Shoulejkin:
             taxi raises speed from ~10 to 16-20 m/s -- secondary, read via the project's Fish 1990 re-read)
  glide   = engineering/simulation/glide.integrate (the project's own point-mass glide, polar P1_nominal) from h0 at angle gam0,
            fixed CL = min(CL_opt, CL_level(V0)) where CL_level gives lift = weight at exit speed (control rule added here: with
            CL_opt held at 10-18 m/s, low-wing-loading phenotypes otherwise loop backwards or stall in this point-mass model)
  escape  = (1 - P_air) * [1 - (1 - e_swim) * P_reacquire]
            P_reacquire = exp(-d / d_vis) * exp(-max(0, d - chase) / d_gap)   (H_vis term and H_chase term; either can be off)
            chase = U_burst * min(t_air, t_burst) + U_sus * max(0, t_air - t_burst)
            P_air = 1 - exp(-beta_air * t_air)                                  (aerial predators, e.g. seabirds; assumption)
  fitness = escape * exp(-kappa_fin * 2 S_fins / (k_wet SL^2))                     (aquatic cost of fins; kappa_fin = 0 is escape-only)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.simulation import glide  # noqa: E402  (the project's own glide model, reused unchanged)
from engineering.simulation.controlled import POLARS, RHO  # noqa: E402

G = 9.80665
HERE = Path(__file__).resolve().parent
OUT = ROOT / "site" / "artifacts" / "simulations"

# ---------------------------------------------------------------- sources (read levels stated, nothing silently defaulted)
SOURCES = {
    "daane2021": {"cite": "Daane JM et al. (2021) Modulation of bioelectric cues in the evolution of flying fishes. Curr Biol 31:5052-5061. doi:10.1016/j.cub.2021.08.054",
                  "read_level": "full Data S1A sheet parsed (project file data/fish-controls/daane2021_s1a_observations.csv)", "used_for": "pectoral length / SL per group: halfbeak 0.137 (Hyporhamphus unifasciatus median), flying halfbeak 0.337 (Oxyporhamphus), Exocoetus volitans 0.674"},
    "fish1990": {"cite": "Fish FE (1990) Wing design and scaling of flying fish with regard to flight performance. J Zool 221:391-403",
                 "read_level": "full text, tables read from page images (project file data/fish-controls/fish1990_tables.json)", "used_for": "Exocoetus wing-area fit 0.046 M^0.741 m^2, pectoral share 91.8%, pooled hypocaudal share 63.1%; taxi speed 10 -> 16-20 m/s is Fish citing Shoulejkin (secondary)"},
    "davenport1992": {"cite": "Davenport J (1992) J Mar Biol Assoc UK 72:25-39", "read_level": "abstract, as returned by a fetch tool (project source record)", "used_for": "hard limit p <= 0.79: pectoral length cannot exceed 78-79% SL without impairing swimming"},
    "lovejoy2004": {"cite": "Lovejoy NR, Iranpour M, Collette BB (2004) Integr Comp Biol 44:366-377", "read_level": "abstract (project source record)", "used_for": "phylogenetic frame: flyingfishes nested within a paraphyletic grade of halfbeaks; justifies a halfbeak-like ancestor"},
    "fishbase": {"cite": "FishBase species summary, length-weight and swimming-speed pages, fetched 2026-11-01 (engineering/ecology_sims/fishbase_parsed.json)", "read_level": "parsed directly from fetched HTML; primary references behind each FishBase row NOT re-read",
                 "used_for": "LW coefficients (Hyporhamphus unifasciatus a=0.00632 SL b=3; Exocoetus volitans a=0.01354 SL b=3), predator sizes (Coryphaena hippurus common 100 cm TL; Thunnus albacares common 150 cm FL), predator speeds (T. albacares burst 5.21-20.46 m/s at 62-66 cm SL, sustained 0.46-0.65 m/s; C. hippurus sustained 0.56 m/s at 67 cm SL; FishBase ref 308), Hyporhamphus caudal 'emarginate or slightly forked'"},
    "oxenford1999": {"cite": "Oxenford HA, Hunte W (1999) Feeding habits of the dolphinfish (Coryphaena hippurus) in the eastern Caribbean. Sci Mar 63:303-315. doi:10.3989/scimar.1999.63n3-4317", "read_level": "abstract (Crossref)", "used_for": "dolphinfish eat flyingfish and halfbeaks: names the predator class, no rate is taken from it"},
    "houle1992": {"cite": "Houle D (1992) Comparing evolvability and variability of quantitative traits. Genetics 130:195-204. doi:10.1093/genetics/130.1.195", "read_level": "abstract (Crossref)", "used_for": "mean-standardised additive variance (CV_A) as the evolvability scale for the G matrix; the CV_A value used is an assumption, not taken from the paper"},
    "lande1979": {"cite": "Lande R (1979) Quantitative genetic analysis of multivariate evolution, applied to brain:body size allometry. Evolution 33:402. doi:10.2307/2407630", "read_level": "bibliographic record only (Crossref); the equation dz = G grad ln W is standard and not re-read here", "used_for": "model form of the adaptive walk"},
    "weinreich2005": {"cite": "Weinreich DM, Watson RA, Chao L (2005) Sign epistasis and genetic constraint on evolutionary trajectories. Evolution 59:1165. doi:10.1554/04-272", "read_level": "bibliographic record only (Crossref)", "used_for": "notion of accessible (monotone) mutational paths on a landscape; method form only"},
    "landeau1986": {"cite": "Landeau L, Terborgh J (1986) Oddity and the 'confusion effect' in predation. Anim Behav 34:1372-1380. doi:10.1016/s0003-3472(86)80208-1", "read_level": "bibliographic record only (Crossref)", "used_for": "model form of a confusion effect; strength parameter is an assumption swept"},
    "treherne1981": {"cite": "Treherne JE, Foster WA (1981) Group transmission of predator avoidance behaviour in a marine insect: the Trafalgar effect. Anim Behav 29:911-917. doi:10.1016/s0003-3472(81)80028-0", "read_level": "bibliographic record only (Crossref)", "used_for": "model form of alarm transmission through a group; speed/delay values are assumptions swept"},
    "couzin2002": {"cite": "Couzin ID, Krause J, James R, Ruxton GD, Franks NR (2002) Collective memory and spatial sorting in animal groups. J Theor Biol 218:1-11. doi:10.1006/jtbi.2002.3065", "read_level": "bibliographic record only (Crossref)", "used_for": "zonal repulsion/orientation/attraction school model form; zone radii are assumptions"},
    "hamilton1971": {"cite": "Hamilton WD (1971) Geometry for the selfish herd. J Theor Biol 31:295-311. doi:10.1016/0022-5193(71)90189-5", "read_level": "bibliographic record only (Crossref)", "used_for": "dilution / selfish-herd framing; no number taken"},
    "project_glide": {"cite": "engineering/simulation/glide.py (glide-pointmass/1) with polar P1_nominal CL_max 1.2, CD0 0.06, e 0.8 (project DESIGN ASSUMPTIONS) and rho 1.225", "read_level": "project code, reused unchanged", "used_for": "airborne phase of every phenotype"},
}

# ---------------------------------------------------------------- anchors (sourced) and assumptions (declared)
ANCHORS = {
    "ancestor": {"label": "halfbeak-like ancestor (Hyporhamphus unifasciatus anchors)", "p": 0.137, "A": 2.0, "M": None, "c": 0.50, "SL_cm": 14.0,
                 "provenance": {"p": "daane2021 S1A median, n=12", "SL_cm": "daane2021 S1A median SL, n=12", "M": "FishBase LW a=0.00632 b=3 (SL) at SL 14.0 cm",
                                "A": "ASSUMPTION (rounded paddle-like fin; no measurement found) - swept 1.2-3.0",
                                "c": "ASSUMPTION from FishBase text 'caudal fin emarginate or slightly forked' -> near-symmetric 0.50 - swept 0.45-0.56"}},
    "flying_halfbeak": {"label": "flying halfbeak marker (Oxyporhamphus micropterus)", "p": 0.337, "SL_cm": 12.55, "provenance": {"p": "daane2021 S1A median, n=10"}},
    "target": {"label": "Exocoetus-like exocoetid target (two-winged)", "p": 0.674, "A": None, "M": None, "c": 0.631, "SL_cm": 13.5,
               "provenance": {"p": "daane2021 S1A Exocoetus volitans median, n=19", "SL_cm": "daane2021 S1A median SL, n=19",
                              "M": "FishBase LW a=0.01354 b=3 (SL) at SL 13.5 cm", "c": "fish1990 pooled hypocaudal share 63.1%",
                              "A": "DERIVED: Fish 1990 Exocoetus wing area 0.046 M^0.741 x pectoral share 0.918, with L_fin = p SL(M; model a_LW); Fish 1990 reports individual AR 8.9-19.9 for Exocoetus under its own definition, which may differ"}},
}
LW = {"halfbeak": 0.00632, "exocoetid": 0.01354}   # FishBase a (g, cm SL, b=3)

ASSUMPTIONS = {  # value, unit, why, sweep range
    "a_LW": (LW["halfbeak"], "g cm^-3", "FishBase Hyporhamphus LW used for the whole walk (body shape is not an evolving trait here)", [LW["halfbeak"], LW["exocoetid"]]),
    "w_body_frac": (0.10, "1", "body width / SL for span; assumption", [0.06, 0.14]),
    "V_exit": (10.0, "m/s", "water-exit speed, same for all phenotypes; Fish 1990 citing Shoulejkin gives ~10 m/s before taxiing (secondary)", [4.0, 10.0]),
    "dV_taxi": (8.0, "m/s", "max taxi speed gain at full asymmetry and full aerodynamic support; 10 -> 18 m/s midpoint of Fish 1990/Shoulejkin 16-20", [4.0, 10.0]),
    "h0": (0.05, "m", "height at water exit; assumption", [0.02, 0.3]),
    "gam0_deg": (15.0, "deg", "exit angle above horizontal; assumption", [5.0, 30.0]),
    "polar": ("P1_nominal", "-", "project polar (design assumption)", ["P1_nominal", "P2_high_drag"]),
    "e_swim": (0.30, "1", "escape probability of a prey that does not leave the water, per attack; assumption", [0.1, 0.6]),
    "U_burst": (10.0, "m/s", "predator burst speed; inside FishBase Thunnus albacares burst rows 5.21-20.46 m/s", [5.21, 20.46]),
    "t_burst": (2.0, "s", "predator burst endurance; assumption", [1.0, 6.0]),
    "U_sus": (0.56, "m/s", "predator sustained speed; FishBase Coryphaena hippurus sustained row", [0.46, 0.65]),
    "d_gap": (3.0, "m", "H_chase: distance scale over which a lead beyond the predator's chase breaks pursuit; assumption", [1.0, 10.0]),
    "d_vis": (20.0, "m", "H_vis: distance scale over which an airborne excursion breaks visual tracking (inf = off); assumption", [5.0, 80.0]),
    "beta_air": (0.0, "1/s", "aerial predator hazard while airborne; assumption", [0.0, 0.2]),
    "p_max": (0.79, "1", "Davenport 1992 limit on pectoral length / SL", [0.79]),
    "n_trim": (1.0, "1", "CL rule: commanded lift at exit <= n_trim x weight (1.0 = level at exit); 1.5 lets fast fish climb (argon review)", [1.0, 1.5]),
    "kappa_fin": (0.0, "1", "aquatic cost of fins: survival/fecundity factor exp(-kappa_fin * fin wetted area / body wetted area); 0 = escape-only fitness; added after argon review", [0.0, 0.1, 0.3, 1.0]),
    "k_wet": (0.4, "1", "body wetted area = k_wet SL^2 (ASSUMPTION for a slender fusiform fish)", [0.4]),
}
DEFAULT = {k: v[0] for k, v in ASSUMPTIONS.items()}


def sl_from_mass(M, a_LW):
    return (1000.0 * np.asarray(M, float) / a_LW) ** (1.0 / 3.0) / 100.0


def mass_from_sl(SL_cm, a_LW):
    return a_LW * SL_cm ** 3 / 1000.0


def target_phenotype(P=None):
    P = {**DEFAULT, **(P or {})}
    M = mass_from_sl(ANCHORS["target"]["SL_cm"], LW["exocoetid"])
    SL = float(sl_from_mass(M, P["a_LW"]))
    S_pec = 0.046 * M ** 0.741 * 0.918
    L = ANCHORS["target"]["p"] * SL
    A = (2 * L ** 2 + P["w_body_frac"] * SL * L) / S_pec     # so that the model's total S equals Fish 1990 pectoral area
    return {"p": ANCHORS["target"]["p"], "A": float(A), "M": float(M), "c": ANCHORS["target"]["c"]}


def ancestor_phenotype(P=None):
    return {"p": ANCHORS["ancestor"]["p"], "A": ANCHORS["ancestor"]["A"], "M": float(mass_from_sl(ANCHORS["ancestor"]["SL_cm"], LW["halfbeak"])), "c": ANCHORS["ancestor"]["c"]}


def morphology(p, A, M, c, P):
    p, A, M, c = np.broadcast_arrays(*[np.asarray(x, float) for x in (p, A, M, c)])
    SL = sl_from_mass(M, P["a_LW"])
    L = p * SL
    w = P["w_body_frac"] * SL
    S = 2 * L ** 2 / A + w * L / A          # two fins + the body strip between them at the fin's mean chord L/A
    b = 2 * L + w
    AR = b ** 2 / S
    return {"SL": SL, "L_fin": L, "S": S, "b": b, "AR": AR, "WL": M * G / S}


def integrate_scheduled(m, S, AR, rho, CL_cap, CD0, e, h0, V0, gam0, n_trim, dt=0.004, t_max=120.0, v_floor=0.3):
    """Same point-mass equations as engineering/simulation/glide.py (copied RK4, vectorised), but the lift coefficient is SCHEDULED
    with speed each step: CL = min(CL_cap, n_trim * 2 m g / (rho V^2 S)) -- level-flight lift at the current speed, capped at CL_opt.
    A sensitivity variant of the project's fixed-CL rule (argon review: a fixed trimmed CL wastes energy). -> range_m, time_s, end_reason."""
    m, S, AR, CL_cap, V0 = [np.atleast_1d(np.asarray(a, float)).ravel().copy() for a in np.broadcast_arrays(m, S, AR, CL_cap, V0)]
    n = m.size
    k_i = 1.0 / (np.pi * e * AR)

    def rhs(st):
        x, h, V, gm = st
        Vs = np.maximum(V, 1e-6)
        CL = np.minimum(CL_cap, n_trim * 2 * m * G / (rho * Vs ** 2 * S))
        q = 0.5 * rho * Vs ** 2 * S
        return np.stack([V * np.cos(gm), V * np.sin(gm), -q * (CD0 + k_i * CL ** 2) / m - G * np.sin(gm), q * CL / (m * Vs) - G * np.cos(gm) / Vs])
    st = np.stack([np.zeros(n), np.full(n, float(h0)), V0, np.full(n, float(gam0))])
    active = np.ones(n, bool); rng = np.zeros(n); tend = np.zeros(n); reason = np.full(n, 1)
    for k in range(int(t_max / dt)):
        if not active.any():
            break
        prev = st.copy()
        k1 = rhs(st); k2 = rhs(st + 0.5 * dt * k1); k3 = rhs(st + 0.5 * dt * k2); k4 = rhs(st + dt * k3)
        new = np.where(active, st + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), st)
        bad = ~np.isfinite(new).all(axis=0) & active
        hit = (new[1] <= 0) & active & ~bad
        slow = (new[2] <= v_floor) & active & ~bad & ~hit
        frac = np.where(hit, prev[1] / np.maximum(prev[1] - new[1], 1e-300), 0.0)
        rng = np.where(hit, prev[0] + frac * (new[0] - prev[0]), rng); tend = np.where(hit, (k + frac) * dt, tend); reason = np.where(hit, 0, reason)
        for mask, code in ((slow, 2), (bad, 3)):
            rng = np.where(mask, np.nan_to_num(prev[0]), rng); tend = np.where(mask, k * dt, tend); reason = np.where(mask, code, reason)
        active &= ~(hit | slow | bad)
        st = np.where(active, new, st)
    rng = np.where(active, st[0], rng); tend = np.where(active, k * dt, tend)
    return {"range_m": rng, "time_s": tend, "end_reason": reason}


def launch_and_glide(p, A, M, c, P, dt=0.004, lift=True):
    """-> dict of arrays: d (airborne horizontal distance, m), t_air (s), V0, phi, E_launch (J, kinetic lower bound), morphology."""
    mo = morphology(p, A, M, c, P)
    pol = POLARS[P["polar"]]
    M_ = np.broadcast_to(np.asarray(M, float), mo["S"].shape)
    c_ = np.broadcast_to(np.asarray(c, float), mo["S"].shape)
    phi = np.minimum(1.0, 0.5 * RHO * P["V_exit"] ** 2 * mo["S"] * pol["CL_max"] / (M_ * G))
    s = np.clip((c_ - 0.5) / (0.631 - 0.5), 0.0, 1.0)
    V0 = P["V_exit"] + P["dV_taxi"] * s * phi
    AR = np.clip(mo["AR"], 1.0, 30.0)
    CL_opt = glide.cl_command(pol["CL_max"], pol["CD0"], pol["e"], AR)
    CL_level = P.get("n_trim", 1.0) * 2 * M_ * G / (RHO * V0 ** 2 * mo["S"])   # lift = n_trim x weight at exit speed
    CL = np.minimum(CL_opt, CL_level)                          # control rule: never command more lift than weight at exit (no loops)
    if P.get("cl_schedule") and lift:
        r = integrate_scheduled(M_.ravel(), mo["S"].ravel(), AR.ravel(), RHO, CL_opt.ravel(), pol["CD0"], pol["e"], P["h0"], V0.ravel(), math.radians(P["gam0_deg"]),
                                P.get("n_trim", 1.0), dt=dt)
    else:
        r = glide.integrate(M_.ravel(), mo["S"].ravel(), AR.ravel(), RHO, CL.ravel(), pol["CD0"], pol["e"], P["h0"], V0.ravel(),
                            gam0=math.radians(P["gam0_deg"]), dt=dt, stall_floor=0.3, lift=lift)   # absolute floor: a leap is not ended by the level-stall rule
    shp = mo["S"].shape
    return {"d": r["range_m"].reshape(shp), "t_air": r["time_s"].reshape(shp), "end_reason": r["end_reason"].reshape(shp), "V0": V0, "phi": phi,
            "E_launch": 0.5 * M_ * V0 ** 2, "CL_cmd": CL, "trim_limited": CL_level < CL_opt, **mo}


def fin_wetted_ratio(r, P):
    w = P["w_body_frac"] * r["SL"]
    S_fins = r["S"] * (2 * r["L_fin"]) / (2 * r["L_fin"] + w)       # S = (2 L^2 + w L)/A -> fins share = 2L/(2L+w)
    return 2 * S_fins / (P.get("k_wet", 0.4) * r["SL"] ** 2)


def fitness(r, P, h_vis=True, h_chase=True):
    """Model fitness per attack generation: escape probability x aquatic fin-cost factor."""
    return escape_prob(r["d"], r["t_air"], P, h_vis=h_vis, h_chase=h_chase) * np.exp(-P.get("kappa_fin", 0.0) * fin_wetted_ratio(r, P))


def escape_prob(d, t_air, P, h_vis=True, h_chase=True):
    d, t = np.maximum(np.asarray(d, float), 0.0), np.asarray(t_air, float)
    chase = P["U_burst"] * np.minimum(t, P["t_burst"]) + P["U_sus"] * np.maximum(0.0, t - P["t_burst"])
    reacq = np.ones_like(d)
    if h_vis and np.isfinite(P["d_vis"]):
        reacq = reacq * np.exp(-d / P["d_vis"])
    if h_chase:
        reacq = reacq * np.exp(-np.maximum(0.0, d - chase) / P["d_gap"])
    p_air = 1 - np.exp(-P["beta_air"] * t)
    return (1 - p_air) * (1 - (1 - P["e_swim"]) * reacq)


# ---------------------------------------------------------------- receipts
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_head():
    try:
        return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def input_hashes(script=None):
    files = [HERE / "common.py", HERE / "fishbase_parsed.json", ROOT / "engineering/simulation/glide.py", ROOT / "engineering/simulation/controlled.py",
             ROOT / "data/fish-controls/daane2021_s1a_observations.csv", ROOT / "data/fish-controls/fish1990_tables.json"]
    out = {str(f.relative_to(ROOT)): sha256_file(f) for f in files}
    if script:
        out["__script__"] = sha256_file(script)
    return out


def receipt(script, seed, started, extra=None, outputs=(), inputs=None):
    """inputs: dict from input_hashes() taken at process START (so later edits cannot mislabel a finished run)."""
    return {"schema": "frontier.eco.receipt/1", "script": str(Path(script).resolve().relative_to(ROOT)), "script_sha256": (inputs or {}).get("__script__") or sha256_file(script),
            "command": "python3 " + " ".join([str(Path(script).resolve().relative_to(ROOT))] + sys.argv[1:]), "exit_code": 0, "seed": seed,
            "started_utc": started, "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "git_head_at_run": git_head(),
            "python": platform.python_version(), "numpy": np.__version__, "host": platform.node(), "inputs_sha256": inputs if inputs is not None else input_hashes(), "inputs_hashed_at": "start" if inputs is not None else "end",
            "outputs_sha256": {os.path.relpath(o, ROOT): sha256_file(o) for o in outputs}, **(extra or {})}


def utcnow():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def dump(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tmp = str(path) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    os.replace(tmp, path)
