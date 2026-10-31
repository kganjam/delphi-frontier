"""Evaluate 2-D cylinder runs against cyl2d_contract.json and cyl2d_band.json (both frozen before any run).

    python engineering/cfd3d/cyl2d_eval.py OUT.json R1=r1.json R2=r2.json R3_domain=r3.json M1_mutant=m1.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
CONTRACT = json.loads((HERE / "cyl2d_contract.json").read_text())
BAND = json.loads((HERE / "cyl2d_band.json").read_text())


def window(t: list[float], cl: list[float], t0: float) -> dict:
    """Lift up-crossings after t0 (linear interpolation); whole periods only."""
    ups = [t[i] + (t[i + 1] - t[i]) * (-cl[i]) / (cl[i + 1] - cl[i])
           for i in range(len(t) - 1) if t[i] >= t0 and cl[i] < 0 <= cl[i + 1]]
    if len(ups) < 2:
        return {"periods": 0, "ups": ups}
    per = [b - a for a, b in zip(ups, ups[1:])]
    m = sum(per) / len(per)
    cv = math.sqrt(sum((p - m) ** 2 for p in per) / len(per)) / m
    return {"periods": len(per), "t_start": ups[0], "t_stop": ups[-1], "period_mean": m, "period_cv": cv}


def time_mean(t, y, a, b) -> float:
    """Trapezoid time mean of y over [a, b] (whole periods; samples are not uniform in t)."""
    s = w = 0.0
    for i in range(len(t) - 1):
        lo, hi = max(t[i], a), min(t[i + 1], b)
        if hi > lo:
            s += 0.5 * (y[i] + y[i + 1]) * (hi - lo)
            w += hi - lo
    return s / w if w else float("nan")


def evaluate(run: dict) -> dict:
    t, cl = run["t"], run["Cl"]
    pc = CONTRACT["frequency"]["periodic_state_required"]
    w = window(t, cl, CONTRACT["time"]["transient_discarded_before"])
    out = {"window": w}
    if w["periods"] == 0:
        out["periodic"] = False
        return out
    out["periodic"] = w["periods"] >= 20 and w["period_cv"] <= 0.02     # contract: >= 20 periods, CV <= 0.02
    out["periodic_rule"] = pc
    a, b = w["t_start"], w["t_stop"]
    out["Cd"] = time_mean(t, run["Cd"], a, b)
    out["Cd_p"] = time_mean(t, run["Cd_p"], a, b)
    out["Cl_rms"] = math.sqrt(time_mean(t, [c * c for c in cl], a, b))
    out["St"] = 1.0 / w["period_mean"]                                  # t is t U / D, so f D / U = 1 / period
    sf = run.get("surface") or {}
    cp = sf.get("Cp_wall_mean") or []
    if cp:
        n = len(cp)
        d_theta = 2 * math.pi / n
        # Cd_p_surface = -sum(Cp n_x R dtheta) / D with R = D / 2 (contract, corrected ddc7095)
        out["Cd_p_surface"] = -sum(c * math.cos(2 * math.pi * k / n) for k, c in enumerate(cp)) * d_theta / 2
        out["surface_closure"] = out["Cd_p_surface"] / out["Cd_p"] - 1 if out["Cd_p"] else None
        out["surface_note"] = "time mean from t >= 100 (every 10th step), not exactly the whole-period window"
    return out


def in_band(e: dict, ref: dict) -> dict:
    hw = BAND["half_width_derivation"]
    r = {k: {"value": e.get(k), "ref": ref[k], "rel": (e[k] / ref[k] - 1) if e.get(k) is not None else None,
             "half_width": hw[k]["half_width"]} for k in ("Cd", "Cd_p", "St")}
    for v in r.values():
        v["pass"] = v["rel"] is not None and abs(v["rel"]) <= v["half_width"]
    r["all"] = bool(e.get("periodic")) and all(v["pass"] for k, v in r.items() if k != "all")
    return r


def main(out: Path, runs: dict[str, Path]) -> dict:
    refs = BAND["references"]
    res = {"schema": "cfd3d-cyl2d-eval-0.1", "band": "cyl2d_band.json", "contract": "cyl2d_contract.json", "runs": {}}
    for rid, path in runs.items():
        e = evaluate(json.loads(path.read_text()))
        ref = refs["H120"] if rid == "R3_domain" else refs["H60"]
        e["band"] = in_band(e, ref)
        res["runs"][rid] = e
    R = res["runs"]
    v = {}
    if "R2" in R:
        v["R2_fidelity"] = R["R2"]["band"]["all"]
    if "R1" in R and "R2" in R and R["R1"].get("Cd") and R["R2"].get("Cd"):
        v["grid_pair_rel"] = {k: abs(R["R2"][k] - R["R1"][k]) / abs(R["R2"][k]) for k in ("Cd", "Cd_p", "St")}
        v["grid_pair"] = v["grid_pair_rel"]["Cd"] <= 0.03
    if "M1_mutant" in R:
        v["mutant"] = not R["M1_mutant"]["band"]["all"]
    v["periodic_R1_R2_R3"] = all(R.get(k, {}).get("periodic") for k in ("R1", "R2", "R3_domain"))
    if "R2" in R and R["R2"].get("surface_closure") is not None:
        v["surface_internal"] = abs(R["R2"]["surface_closure"]) <= 0.10
    need = ("R2_fidelity", "grid_pair", "mutant", "periodic_R1_R2_R3")
    v["control_passes"] = all(v.get(k) is True for k in need)
    v["missing"] = [k for k in need if k not in v]
    res["verdict"] = v
    out.write_text(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    runs = dict(a.split("=", 1) for a in sys.argv[2:])
    r = main(Path(sys.argv[1]), {k: Path(p) for k, p in runs.items()})
    print(json.dumps(r["verdict"], indent=1))
