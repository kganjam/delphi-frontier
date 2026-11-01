"""Predation / escape ecology: when does leaving the water pay?

Uses common.launch_and_glide (project glide model) for three phenotypes anchored on Daane 2021 S1A / FishBase:
ancestor halfbeak-like, flying-halfbeak-like intermediate (Oxyporhamphus p), Exocoetus-like target. Predators are parameterised
from FishBase rows (Thunnus albacares burst 8.4-31 SL/s; sustained 0.46-0.65 m/s; Coryphaena hippurus sustained 0.56 m/s).

Outputs: escape probability per attack vs predator burst speed / endurance / aerial hazard; a (prey SL, predator SL) map of the
escape gain over not leaving the water; launch energy (kinetic lower bound) as a fraction of an ASSUMED routine metabolic budget.
SIMULATED; no predator-prey encounter was observed. Encounter rate is a swept assumption, not an estimate.
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engineering.ecology_sims import common as C  # noqa: E402
from engineering.simulation import glide  # noqa: E402
from engineering.simulation.controlled import POLARS, RHO  # noqa: E402

RMR_W_PER_KG = (0.3, "W/kg", "ASSUMED routine metabolic rate for a ~30 g tropical pelagic fish; not sourced; swept 0.1-1.0", [0.1, 1.0])
MUSCLE_EFF = (0.2, "1", "ASSUMED muscle efficiency converting metabolic to mechanical work; swept 0.1-0.3", [0.1, 0.3])
BURST_L_PER_S = [8.4, 18.8, 31.0]   # FishBase T. albacares burst rows (SL/s)


def phenotypes(P):
    a, t = C.ancestor_phenotype(P), C.target_phenotype(P)
    s = 0.5
    mid = {"p": C.ANCHORS["flying_halfbeak"]["p"], "A": a["A"] * (t["A"] / a["A"]) ** s, "M": float(C.mass_from_sl(C.ANCHORS["flying_halfbeak"]["SL_cm"], C.LW["halfbeak"])),
           "c": a["c"] + (t["c"] - a["c"]) * s}
    return {"ancestor (halfbeak-like)": a, "intermediate (flying-halfbeak p)": mid, "target (Exocoetus-like)": t}


def series(z, P, dt=0.004, stride=5):
    mo = C.morphology(z["p"], z["A"], z["M"], z["c"], P)
    r0 = C.launch_and_glide(z["p"], z["A"], z["M"], z["c"], P, dt=dt)
    pol = POLARS[P["polar"]]
    AR = float(np.clip(mo["AR"], 1, 30))
    CL = float(r0["CL_cmd"])
    r = glide.integrate(z["M"], float(mo["S"]), AR, RHO, CL, pol["CD0"], pol["e"], P["h0"], float(r0["V0"]), gam0=math.radians(P["gam0_deg"]), dt=dt, record_stride=stride, stall_floor=0.3)
    ts = np.array([s[0] for s in r["series"]]); xs = np.array([s[1][0, 0] for s in r["series"]]); hs = np.array([s[1][1, 0] for s in r["series"]])
    act = np.array([s[2][0] for s in r["series"]])
    return {"t": ts[act], "x": xs[act], "h": hs[act], "d": float(r0["d"]), "t_air": float(r0["t_air"]), "V0": float(r0["V0"]), "E": float(r0["E_launch"]), "S": float(mo["S"]), "AR": AR, "SL": float(mo["SL"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(C.OUT / "eco-escape-ecology"))
    ap.add_argument("--seed", type=int, default=20261101)
    ap.add_argument("--dt", type=float, default=0.004)
    a_ = ap.parse_args()
    np.random.seed(a_.seed)
    started = C.utcnow(); t0 = time.time(); inputs = C.input_hashes(__file__)
    out = Path(a_.out); out.mkdir(parents=True, exist_ok=True)
    P = dict(C.DEFAULT)
    ph = phenotypes(P)
    res = {"schema": "frontier.eco.escape/1", "assumptions": {**C.ASSUMPTIONS, "RMR_W_per_kg": RMR_W_PER_KG, "muscle_efficiency": MUSCLE_EFF}, "sources": C.SOURCES, "phenotypes": {}}
    for k, z in ph.items():
        s = series(z, P, a_.dt)
        s2 = C.launch_and_glide(z["p"], z["A"], z["M"], z["c"], P, dt=a_.dt / 2)
        rmr_day = RMR_W_PER_KG[0] * z["M"] * 86400.0
        sb = C.launch_and_glide(z["p"], z["A"], z["M"], z["c"], P, dt=a_.dt, lift=False)   # zero-lift (ballistic) control, argon review
        res["phenotypes"][k] = {"z": z, "airborne_distance_m": s["d"], "airborne_time_s": s["t_air"], "V0_m_s": s["V0"], "S_m2": s["S"], "AR": s["AR"], "SL_m": s["SL"],
                                "dt_half_distance_m": float(s2["d"]), "ballistic_control_distance_m": float(sb["d"]), "ballistic_control_time_s": float(sb["t_air"]),
                                "ballistic_control_escape_both": float(C.escape_prob(sb["d"], sb["t_air"], P)),
                                "fin_wetted_over_body_wetted": float(C.fin_wetted_ratio(C.launch_and_glide(z["p"], z["A"], z["M"], z["c"], P, dt=a_.dt), P)), "launch_kinetic_J": s["E"], "launch_metabolic_J_lower_bound": s["E"] / MUSCLE_EFF[0],
                                "launch_cost_frac_of_assumed_daily_RMR": s["E"] / MUSCLE_EFF[0] / rmr_day,
                                **{f"escape_{h}": float(C.escape_prob(s["d"], s["t_air"], P, h_vis=h != "chase", h_chase=h != "vis")) for h in ("vis", "chase", "both")}}
        print(k, {kk: (round(v, 4) if isinstance(v, float) else v) for kk, v in res["phenotypes"][k].items() if kk != "z"}, flush=True)
    # 1. escape vs predator burst speed and endurance, per phenotype and hypothesis
    U = np.linspace(2, 25, 47); TB = np.array([1.0, 2.0, 4.0, 6.0])
    curves = {}
    for k in ph:
        d, ta = res["phenotypes"][k]["airborne_distance_m"], res["phenotypes"][k]["airborne_time_s"]
        for h in ("vis", "chase", "both"):
            for tb in TB:
                curves[f"{k}|{h}|t_burst={tb}"] = [float(C.escape_prob(d, ta, {**P, "U_burst": u, "t_burst": tb}, h_vis=h != "chase", h_chase=h != "vis")) for u in U]
    res["escape_vs_U_burst"] = {"U_burst_m_s": U.tolist(), "curves": curves}
    # break-even predator speed per phenotype: smallest U at which the H_chase escape gain over e_swim falls below 0.01
    be = {}
    for k in ph:
        c = np.array(curves[f"{k}|chase|t_burst=2.0"]) - P["e_swim"]
        i = np.where(c < 0.01)[0]
        be[k] = float(U[i[0]]) if len(i) else None
    res["H_chase_predator_speed_where_gain_below_0.01_m_s"] = be
    # 2. (prey SL, predator SL) map: prey = target shape scaled in mass via a_LW; predator burst = k * SL_pred
    preySL = np.linspace(0.10, 0.50, 21); predSL = np.linspace(0.3, 1.5, 25)
    t = ph["target (Exocoetus-like)"]
    Mp = C.mass_from_sl(preySL * 100, P["a_LW"])
    r = C.launch_and_glide(t["p"], t["A"], Mp, t["c"], P, dt=a_.dt)
    maps = {}
    for kb in BURST_L_PER_S:
        for h in ("vis", "chase", "both"):
            gain = np.array([[float(C.escape_prob(r["d"][i], r["t_air"][i], {**P, "U_burst": kb * ps}, h_vis=h != "chase", h_chase=h != "vis")) - P["e_swim"] for ps in predSL] for i in range(len(preySL))])
            maps[f"k={kb}|{h}"] = gain.tolist()
    res["size_map"] = {"prey_SL_m": preySL.tolist(), "pred_SL_m": predSL.tolist(), "prey_airborne_m": r["d"].tolist(), "prey_airborne_s": r["t_air"].tolist(),
                       "note": "fixed Exocoetus-like proportions (p, A, c) at every prey size; FishBase exocoetid max lengths 10.3-50 cm; predator burst = k x SL with k from FishBase T. albacares burst rows", "gain": maps}
    # 3. aerial hazard x predator speed: where does leaving the water pay (gain > 0) for the target?
    B = np.linspace(0, 0.4, 41)
    d, ta = res["phenotypes"]["target (Exocoetus-like)"]["airborne_distance_m"], res["phenotypes"]["target (Exocoetus-like)"]["airborne_time_s"]
    pay = np.array([[float(C.escape_prob(d, ta, {**P, "U_burst": u, "beta_air": b})) - P["e_swim"] for u in U] for b in B])
    res["aerial_map"] = {"beta_air_per_s": B.tolist(), "U_burst_m_s": U.tolist(), "gain_both": pay.tolist()}
    # 4. daily energy at attack rate lambda (attacks/day), target phenotype
    lam = [0.1, 1, 3, 10]
    tp = res["phenotypes"]["target (Exocoetus-like)"]
    res["energy"] = {"attacks_per_day": lam, "launch_metabolic_frac_of_daily_RMR": [l * tp["launch_cost_frac_of_assumed_daily_RMR"] for l in lam],
                     "note": "kinetic energy at take-off / muscle efficiency: a LOWER bound (taxi drag work and swimming before exit excluded); RMR is an assumption"}
    # sensitivity: one-at-a-time on physics + escape settings for the target and ancestor escape gain
    sens = []
    for name, ov in [("default", {}), ("V_exit=4", {"V_exit": 4.0}), ("dV_taxi=4", {"dV_taxi": 4.0}), ("gam0=5", {"gam0_deg": 5.0}), ("gam0=30", {"gam0_deg": 30.0}),
                     ("polar=P2_high_drag", {"polar": "P2_high_drag"}), ("a_LW=exocoetid", {"a_LW": C.LW["exocoetid"]}), ("U_burst=5.21", {"U_burst": 5.21}),
                     ("U_burst=20.46", {"U_burst": 20.46}), ("t_burst=6", {"t_burst": 6.0}), ("e_swim=0.1", {"e_swim": 0.1}), ("e_swim=0.6", {"e_swim": 0.6}),
                     ("d_vis=5", {"d_vis": 5.0}), ("d_vis=80", {"d_vis": 80.0}), ("beta_air=0.2", {"beta_air": 0.2}), ("n_trim=1.5", {"n_trim": 1.5})]:
        Q = {**P, **ov}; row = {"setting": name}
        for k, z in ph.items():
            rr = C.launch_and_glide(z["p"], z["A"], z["M"], z["c"], Q, dt=a_.dt)
            for h in ("vis", "chase", "both"):
                row[f"{k}|{h}|gain"] = float(C.escape_prob(rr["d"], rr["t_air"], Q, h_vis=h != "chase", h_chase=h != "vis")) - Q["e_swim"]
            row[f"{k}|airborne_m"] = float(rr["d"])
        sens.append(row)
    res["sensitivity"] = sens
    res["elapsed_s"] = time.time() - t0
    C.dump(out / "results.json", res)
    import pickle
    with open(out / "_series.pkl", "wb") as fh:
        pickle.dump({k: series(z, P, a_.dt, stride=4) for k, z in ph.items()}, fh)
    C.dump(out / "receipt.json", C.receipt(__file__, a_.seed, started, {"elapsed_s": res["elapsed_s"], "dt": a_.dt}, outputs=[out / "results.json"], inputs=inputs))


if __name__ == "__main__":
    main()
