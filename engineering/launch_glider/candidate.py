"""Placeholder flight candidate built from the v3a meshes at print thicknesses, until claude-05's flight_model.json.

Mass properties come from the actual v3a component meshes, with the print alterations declared here:
  body       hollow shell of thickness t_body over body.stl (sheet integral on the closed outer surface);
  fins       membranes of thickness t_fin over each fin's panels.json mid-surface quads (sheets), plus a
             leading-edge spar (w x h line mass along leading_edge_m) on the paired fins;
  head       bulkhead + hook boss as point masses at declared positions (the requirement R3 hardware);
  ballast    a point mass at x_ballast solved so the CG lands on x_cg_target (refused if it would be negative).
Ground contact points are the convex hull of every component vertex projected on the x-z plane (pitch plane).
None of this is claude-05's design; it exists so the dynamics run on real geometry before that design lands.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from . import mass_props as mp
from . import print_requirements as pr

V3A = Path("artifacts/fish3d/fish3d-v3a-fan")
FINS = ("pectoral_L", "pectoral_R", "pelvic_L", "pelvic_R", "caudal", "dorsal", "anal")


def _quads_to_tris(quads) -> np.ndarray:
    q = np.asarray(quads, float)
    return np.concatenate([q[:, [0, 1, 2]], q[:, [0, 2, 3]]])


def _polyline_mass(pts, lin_density) -> dict:
    P = np.asarray(pts, float)
    seg = np.linalg.norm(P[1:] - P[:-1], axis=1)
    mid = 0.5 * (P[1:] + P[:-1])
    parts = [{"mass_kg": lin_density * L, "cg_m": m.tolist(),
              "inertia_cg_kg_m2": np.zeros((3, 3)).tolist()} for L, m in zip(seg, mid)]
    return mp.combine(parts)


def hull_xz(points: np.ndarray) -> np.ndarray:
    """Convex hull (monotone chain) of (x, z) points, counter-clockwise, no repeats."""
    P = sorted(set(map(tuple, np.round(points, 9))))
    if len(P) < 3:
        return np.array(P)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


DEFAULTS = {
    "t_body_m": {"value": 0.8e-3, "status": "claude-05 plan default (0.8 mm body), not frozen"},
    "t_fin_m": {"value": 0.5e-3, "status": "requirement R1/R2 membrane"},
    "spar_pect_m": {"value": [1.6e-3, 2.0e-3], "status": "requirement R1 (w, h)"},
    "spar_pelv_m": {"value": [1.2e-3, 1.2e-3], "status": "requirement R2 (w, h)"},
    "head_hardware": {"value": [{"id": "bulkhead", "mass_kg": 0.4e-3, "x_m": 0.030, "z_m": 0.0},
                                {"id": "hook_boss", "mass_kg": 0.3e-3, "x_m": 0.025, "z_m": -0.008}],
                      "status": "assumed point masses for requirement R3 hardware"},
    "x_ballast_m": {"value": 0.015, "status": "assumed nose ballast bay position"},
}


def build(x_cg_target: float, mat: dict, root: Path = Path("."), opts: dict | None = None) -> dict:
    o = {k: v["value"] for k, v in DEFAULTS.items()} | (opts or {})
    rho = mat["solid_density_kg_m3"]
    v3a = root / V3A
    panels = json.loads((v3a / "panels.json").read_text())
    parts, verts = {}, []
    body = mp.read_stl(v3a / "components/body.stl")
    parts["body_shell"] = mp.sheet(body, rho, o["t_body_m"])
    verts.append(body.reshape(-1, 3))
    for f in FINS:
        tri = _quads_to_tris(panels["fins"][f]["quads_m"])
        parts[f"{f}_membrane"] = mp.sheet(tri, rho, o["t_fin_m"])
        verts.append(mp.read_stl(v3a / f"components/{f}.stl").reshape(-1, 3))
    for f, key in (("pectoral_L", "spar_pect_m"), ("pectoral_R", "spar_pect_m"),
                   ("pelvic_L", "spar_pelv_m"), ("pelvic_R", "spar_pelv_m")):
        w, h = o[key]
        parts[f"{f}_spar"] = _polyline_mass(panels["fins"][f]["leading_edge_m"], rho * w * h)
    for hw in o["head_hardware"]:
        parts[hw["id"]] = mp.point(hw["mass_kg"], [hw["x_m"], 0.0, hw["z_m"]])
    dry = mp.combine(list(parts.values()))
    xb = o["x_ballast_m"]
    mb = dry["mass_kg"] * (dry["cg_m"][0] - x_cg_target) / (x_cg_target - xb)
    status = "ok"
    if mb < 0:
        status = "NO_BALLAST_NEEDED_CG_AHEAD_OF_TARGET"
        mb = 0.0
    parts["ballast"] = mp.point(mb, [xb, 0.0, 0.0])
    tot = mp.combine(list(parts.values()))
    hull = hull_xz(np.concatenate(verts)[:, [0, 2]])
    S_paired = 2 * (panels["fins"]["pectoral_L"]["area_flat_m2"] + panels["fins"]["pelvic_L"]["area_flat_m2"])
    pect = pr.planform(panels["fins"]["pectoral_L"])
    span = 2 * float(np.max(np.asarray(panels["fins"]["pectoral_L"]["outline_m"])[:, 1]))
    return {"evidence_kind": "derived_estimate",
            "source": "v3a candidate meshes at declared print thicknesses (not claude-05's design)",
            "candidate_sha256": panels["candidate_sha256"], "options": o, "material_id": mat["id"],
            "parts": {k: {kk: v[kk] for kk in ("mass_kg", "cg_m", "inertia_cg_kg_m2")} for k, v in parts.items()},
            "dry": dry, "ballast_kg": mb, "ballast_status": status, "assembled": tot,
            "contacts_xz_m": hull.tolist(), "S_paired_m2": S_paired, "span_m": span,
            "mac_m": pr.mac(pect)["mac_m"], "AR_total": span * span / S_paired}


def to_params(cand: dict, aero: dict, n: int = 1):
    """Dynamics parameters from a candidate and an aero dict (values or (N,) arrays)."""
    from . import dynamics as dy
    a = cand["assembled"]
    x_cg, z_cg = a["cg_m"][0], a["cg_m"][2]
    inertia = np.asarray(a["inertia_cg_kg_m2"])
    hull = np.asarray(cand["contacts_xz_m"])
    xi = (x_cg - hull[:, 0])[None, :]
    zeta = (hull[:, 1] - z_cg)[None, :]
    kw = dict(m=a["mass_kg"], Iyy=inertia[1, 1], x_cg=x_cg, z_cg=z_cg, S=cand["S_paired_m2"], c=cand["mac_m"],
              AR=cand["AR_total"], contacts_xi=xi, contacts_zeta=zeta)
    kw.update(aero)
    return dy.Params(**kw).broadcast(n)


AERO_NOMINAL = {  # scenario coefficients: value, bracket, source; none measured for this glider
    "CLa": (4.8, (4.4, 5.2), "Helmbold on the paired-fin reference with declared downwash (print_requirements NP bracket)"),
    "x_np": (0.0601, (0.0583, 0.0619), "fins-only hand NP bracket, print_requirements.neutral_point"),
    "e": (0.75, (0.6, 0.9), "declared span efficiency"),
    "CD0": (0.07, (0.04, 0.12), "declared; laminar Cf build-up ~0.045 at Re 1e4; Park & Choi stuffed fish CD_min 0.055 "
                                "on body-inclusive area (~0.08 on paired area) is a comparison only"),
    "CL_max": (0.7, (0.6, 0.9), "declared; Park & Choi stuffed fish CL_max 0.78 at 35 deg on body-inclusive area"),
    "d_alpha": (math.radians(2.0), (math.radians(1.0), math.radians(4.0)), "declared stall-onset width"),
    "k_post": (0.9, (0.8, 1.0), "declared flat-plate post-stall factor"),
    "Cm_q": (-4.5, (-8.0, -2.0), "pelvic tail-volume estimate -2 a_t V_H (l_t/c)(1-eps); declared"),
    "k_munk": (0.9, (0.8, 0.95), "slender-body k2-k1 for fineness ~6, recalled; declared"),
    "x_cp_post": (0.0658, (0.060, 0.072), "paired-fin area centroid; declared post-stall centre of pressure"),
}


def aero_nominal(cand: dict, body_volume_m3: float) -> dict:
    a = {k: v[0] for k, v in AERO_NOMINAL.items()}
    a["vol"] = body_volume_m3
    return a


def ballistic_cd(aero: dict) -> float:
    """No-lift control: the same profile drag CD0 on the same S, zero lift, zero induced drag, no moments."""
    return aero["CD0"]


def stall_speed(cand: dict, CL_max: float, rho: float = 1.225) -> float:
    return math.sqrt(2 * cand["assembled"]["mass_kg"] * 9.80665 / (rho * cand["S_paired_m2"] * CL_max))
