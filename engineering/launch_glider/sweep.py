"""Feasibility map: slingshot stroke + flight against NP scenario, wall thickness, trim CL, release speed and pitch.

    python -m engineering.launch_glider.sweep artifacts/launch-glider/feasibility-map.json

Every draw uses the placeholder candidate (v3a meshes at print thicknesses, candidate.py) with its CG put at
SM_TARGET * MAC ahead of the scenario NP by ballast, and the NOMINAL scenario coefficients (candidate.AERO_NOMINAL).
The no-lift control starts from the same release state with the same profile drag CD0, zero lift and no moments.
It is a scenario map on assumed coefficients: not calibrated, not a probability, not flight-tested.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

from . import candidate as cd
from . import dynamics as dy
from . import print_requirements as pr

SM_TARGET = 0.15
GRID = {
    "x_np_m": {"values": [0.060, 0.066, 0.072],
               "status": "hand fins-only NP 60 mm (print_requirements), and two aft scenarios: Park & Choi's stable "
                         "stuffed fish had x_CG/SL 0.39-0.44 (62-70 mm on this SL); VLM (cfd04) replaces all three"},
    "t_body_m": {"values": [0.5e-3, 0.8e-3], "status": "shell wall scenarios"},
    "CL_trim": {"values": [0.3, 0.45, 0.6], "status": "decalage design choice (sets Cm0)"},
    "V0_m_s": {"values": [4.0, 6.0, 8.0, 10.0, 12.0],
               "status": "4/6/8 are SPEC-010 rule 3; 10 and 12 are added beyond SPEC-010 to locate where gliding starts"},
    "phi_deg": {"values": [0.0, 15.0, 30.0], "status": "declared launch pitch (band elevation), reviewer item 1"},
    "hook_zeta_m": {"values": [-0.0015, 0.0, 0.0015], "status": "catch height relative to the CG (R3 correction)"},
    "hook_xi_m": {"values": [0.025, 0.040], "status": "hook distance ahead of the CG (R3 correction)"},
}
FIXED = {"h_release_m": 1.35, "stroke_m": 0.2, "profile": "linear", "delta_deg": 0.0}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build_draws(root: Path, card: Path, grid: dict | None = None) -> tuple[list[dict], dict]:
    GRID_ = grid or GRID
    mat = pr.load_material(card)
    cands = {}
    rows = []
    for x_np, tb in itertools.product(GRID_["x_np_m"]["values"], GRID_["t_body_m"]["values"]):
        probe = cd.build(0.06, mat, root=root, opts={"t_body_m": tb})
        x_cg = x_np - SM_TARGET * probe["mac_m"]
        c = cd.build(x_cg, mat, root=root, opts={"t_body_m": tb})
        if c["ballast_status"] != "ok":   # dry CG already ahead: no ballast, actual SM is larger than target
            x_cg = c["assembled"]["cg_m"][0]
        cands[(x_np, tb)] = c
        for cl, V0, phi, hz, hx in itertools.product(GRID_["CL_trim"]["values"], GRID_["V0_m_s"]["values"],
                                                     GRID_["phi_deg"]["values"], GRID_["hook_zeta_m"]["values"],
                                                     GRID_["hook_xi_m"]["values"]):
            rows.append({"x_np_m": x_np, "t_body_m": tb, "CL_trim": cl, "V0_m_s": V0, "phi_deg": phi,
                         "hook_zeta_m": hz, "hook_xi_m": hx,
                         "x_cg_m": c["assembled"]["cg_m"][0], "mass_kg": c["assembled"]["mass_kg"],
                         "ballast_kg": c["ballast_kg"], "Iyy_kg_m2": c["assembled"]["inertia_cg_kg_m2"][1][1]})
    return rows, {"cands": cands, "mat": mat}


def run(root: Path, card: Path, dt_stroke=1e-4, dt_fly=1e-3, grid: dict | None = None) -> dict:
    rows, ctx = build_draws(root, card, grid)
    vol = json.loads((root / cd.V3A / "components.json").read_text())["components"]["body"]["check"]["volume_mm3"] * 1e-9
    sim = simulate(rows, [ctx["cands"][(r["x_np_m"], r["t_body_m"])] for r in rows], vol, dt_stroke, dt_fly)
    return {"schema": "frontier.glider.feasibility-map/1", "evidence_kind": "simulated_scenario",
            "grid": grid or GRID, "fixed": FIXED, "sm_target": SM_TARGET, "aero_nominal": cd.AERO_NOMINAL,
            "material": {k: ctx["mat"][k] for k in ("id", "card_path", "card_sha256")},
            "dt": {"stroke_s": dt_stroke, "flight_s": dt_fly}, **sim,
            "limits": ["placeholder geometry (v3a meshes at declared thicknesses), not claude-05's design",
                       "nominal scenario coefficients; NP is a scenario axis, not a VLM result",
                       "pitch plane only: no roll, yaw, sideslip or spiral modes",
                       "launcher speed, force profile and alignment are chosen scenarios, not measurements",
                       "no ground effect, no wall/ceiling, still air"]}


def simulate(rows: list[dict], cands: list[dict], vol: float, dt_stroke=1e-4, dt_fly=1e-3) -> dict:
    """Trim, modes, stroke, flight and the no-lift control for each draw; draw i flies candidate cands[i].

    A row needs x_np_m, CL_trim, V0_m_s, phi_deg, hook_xi_m, hook_zeta_m (catch relative to that draw's CG) and
    mass_kg / x_cg_m. Rows whose trim fails are returned in failed_designs with the reason, not dropped."""
    plist, flown = [], []
    for r, c in zip(rows, cands):
        a = cd.aero_nominal(c, vol) | {"x_np": r["x_np_m"]}
        p1 = cd.to_params(c, a, 1)
        try:
            p1.Cm0 = np.array([dy.cm0_for_trim(p1, r["CL_trim"])])
        except ValueError as e:   # retained as a failed design, not dropped
            r["status"] = str(e).split(":")[0]
            r["detail"] = str(e)
            continue
        r["status"] = "ok"
        t = dy.trim(p1, r["CL_trim"])
        r.update({"Cm0": float(p1.Cm0[0]), "V_trim_m_s": t["V_m_s"], "gamma_trim_deg": math.degrees(t["gamma_rad"]),
                  "alpha_trim_deg": math.degrees(t["alpha_rad"]),
                  "wing_loading_N_m2": r["mass_kg"] * dy.G / c["S_paired_m2"],
                  "Re_mac_at_V0": r["V0_m_s"] * c["mac_m"] / 1.5e-5,
                  "static_margin": (r["x_np_m"] - r["x_cg_m"]) / c["mac_m"],
                  "modes": _modes_json(dy.jacobian_modes(p1, dy.trim_state(p1, r["CL_trim"])))})
        plist.append(p1)
        flown.append(c)
    failed = [r for r in rows if r["status"] != "ok"]
    rows = [r for r in rows if r["status"] == "ok"]
    n = len(rows)
    if n == 0:
        return {"rows": [], "failed_designs": failed, "unreleased": 0, "airborne_at_t_max": 0}
    P = _stack(plist)
    L = dy.Launch(V0=[r["V0_m_s"] for r in rows], stroke=FIXED["stroke_m"],
                  phi=np.radians([r["phi_deg"] for r in rows]), delta=math.radians(FIXED["delta_deg"]),
                  profile=dy.PROFILES[FIXED["profile"]], xi_h=[r["hook_xi_m"] for r in rows],
                  zeta_h=[r["hook_zeta_m"] for r in rows])
    st = dy.stroke(P, L, n, dt=dt_stroke)
    y0 = st["release_state"].copy()
    y0[0] = 0.0
    y0[1] = FIXED["h_release_m"]
    fl = dy.fly(P, y0, dt=dt_fly)
    Pb = _stack(plist)
    Pb.lift = np.zeros(n)
    Pb.cd_ballistic = P.CD0.copy()
    bl = dy.fly(Pb, y0, dt=dt_fly)
    for i, r in enumerate(rows):
        hull = np.asarray(flown[i]["contacts_xz_m"])
        r.update({"release": {"V_m_s": float(st["V_release_m_s"][i]), "gamma_deg": math.degrees(st["gamma_release_rad"][i]),
                              "alpha_deg": math.degrees(st["alpha_release_rad"][i]),
                              "q_rad_s": float(st["q_release_rad_s"][i]), "a_mean_m_s2": float(st["a_mean_m_s2"][i]),
                              "a_peak_m_s2": float(st["a_peak_m_s2"][i]), "F_peak_N": float(st["F_peak_N"][i]),
                              "band_moment_peak_N_m": float(st["band_moment_peak_N_m"][i]),
                              "band_angular_impulse_N_m_s": float(st["band_angular_impulse_N_m_s"][i])},
                  "flight": {"range_m": float(fl["range_m"][i]), "t_s": float(fl["t_s"][i]),
                             "alpha_max_deg": math.degrees(fl["alpha_max_rad"][i]),
                             "alpha_min_deg": math.degrees(fl["alpha_min_rad"][i]),
                             "separation_max": float(fl["separation_max"][i]), "V_min_m_s": float(fl["V_min"][i]),
                             "tumbled": bool(fl["tumbled"][i]), "V_impact_m_s": float(fl["V_impact"][i]),
                             "KE_impact_J": 0.5 * r["mass_kg"] * float(fl["V_impact"][i]) ** 2,
                             "theta_impact_deg": math.degrees(fl["theta_impact"][i]),
                             "first_contact_xz_m": hull[int(fl["contact_id"][i])].tolist()},
                  "no_lift_control": {"range_m": float(bl["range_m"][i]), "t_s": float(bl["t_s"][i])},
                  "glide_gain_m": float(fl["range_m"][i] - bl["range_m"][i]),
                  "in_target_5_8_m": bool(5.0 <= fl["range_m"][i] <= 8.0)})
    return {"rows": rows, "failed_designs": failed, "unreleased": st["unreleased"],
            "airborne_at_t_max": fl["airborne_at_t_max"]}


def _modes_json(md: dict) -> dict:
    def c(z):
        return None if z is None else {"re": z.real, "im": z.imag, "period_s": 2 * math.pi / z.imag,
                                       "damping_ratio": -z.real / abs(z)}
    return {"eigenvalues": md["eigenvalues"], "short_period": c(md["short_period"]), "phugoid": c(md["phugoid"]),
            "max_real": md["max_real"]}


def _stack(plist):
    from dataclasses import fields
    kw = {}
    width = max(p.contacts_xi.shape[1] for p in plist)
    for f in fields(dy.Params):
        vs = [getattr(p, f.name) for p in plist]
        if f.name.startswith("contacts"):   # hulls differ in point count: pad by repeating the last point
            vs = [np.pad(v, ((0, 0), (0, width - v.shape[1])), mode="edge") for v in vs]
            kw[f.name] = np.concatenate(vs, axis=0)
        else:
            kw[f.name] = np.concatenate(vs)
    return dy.Params(**kw)


def main(argv):
    out = Path(argv[1])
    root = Path(".")
    card = root / "data/materials/formlabs-studio-2026-10-31.json"
    r = run(root, card)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=1, sort_keys=True, default=float) + "\n")
    print(out, _sha(out))


if __name__ == "__main__":
    main(sys.argv)
