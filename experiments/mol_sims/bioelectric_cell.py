"""s5: single-cell pump-leak bioelectric model for Kcnk5b dose (claude-mol, 2026-11-01).

Question it can answer: can a K2P leak gain-of-function (Kcnk5b, the zebrafish `another longfin` locus) DEPOLARISE a
fin-bud/blastema cell at steady state, as Yi et al. 2024 (PLoS Biol 22:e3002565, PMID 38527087) report
("Kcnk5b enhanced depolarization in fin bud cells via Na+ channels" with decreased intracellular K+), when a
textbook fixed-gradient view says more K+ leak must hyperpolarise? The model keeps [Na]i, [K]i, [Cl]i dynamic
under a saturable Na/K-ATPase, adds a Kcnj13-like inward rectifier and a persistent Na conductance, and reports a
Cav3.1-like (cacna1g) T-type window current as the Ca2+ readout (Dev 2025, PMID 41321290, cacna1g mutants
regenerate long fins).

Every parameter below is an ASSUMPTION (generic vertebrate cell values), not a zebrafish measurement; the
sources only give signs/qualitative behaviour. SIMULATED, not observed. Deterministic: no seed.
Usage: python bioelectric_cell.py   -> results/mol-sims/claude-20261101/s5_bioelectric_kcnk5b_sweep.json + receipt
"""
import hashlib, json, math, sys, time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/mol-sims/claude-20261101"
F, R, T = 96485.0, 8.314, 301.15          # 28 C, zebrafish rearing temperature
RT_F = R * T / F
r_cm = 5e-4                                # cell radius 5 um (assumed)
A = 4 * math.pi * r_cm ** 2                # cm^2
VOL = 4 / 3 * math.pi * r_cm ** 3          # cm^3 (fixed volume: simplification)
CM = 1e-6                                  # F/cm^2
OUTSIDE = {"K": 4.0, "Na": 140.0, "Cl": 120.0, "Ca": 2.0}  # mM, generic vertebrate interstitium (assumed)

BASE = {
    "P_K2P": 2.0e-8,     # cm/s, Kcnk5b-like leak (scaled in the sweep)
    "P_Kother": 1.0e-8,  # other K leak
    "g_Kir": 2.0e-6,     # S/cm^2, Kcnj13-like inward rectifier
    "P_Na": 2.0e-9,      # Na background leak
    "g_NaP": 2.0e-6,     # S/cm^2, persistent Na (Nav window) -- the route Yi 2024 implicate
    "P_Cl": 4.0e-9,
    "Ip_max": 1.5e-7,    # A/cm^2, Na/K-ATPase maximal current (scaled in the sweep)
    "g_CaT": 1.0e-5,     # S/cm^2, Cav3.1-like (readout only; Ca concentration not tracked)
}


def ghk(P, z, V, ci, co):
    """GHK current density (A/cm^2), outward positive. Concentrations mM -> mol/cm^3."""
    ci, co = ci * 1e-6, co * 1e-6
    u = z * V / RT_F
    if abs(u) < 1e-6:
        return P * z * F * (ci - co)
    return P * z * z * F * V / RT_F * (ci - co * math.exp(-u)) / (1 - math.exp(-u))


def nernst(z, ci, co):
    return RT_F / z * math.log(co / ci)


def currents(V, Na, K, Cl, p):
    EK, ENa = nernst(1, K, OUTSIDE["K"]), nernst(1, Na, OUTSIDE["Na"])
    I_K2P = ghk(p["P_K2P"], 1, V, K, OUTSIDE["K"])
    I_Ko = ghk(p["P_Kother"], 1, V, K, OUTSIDE["K"])
    I_Kir = p["g_Kir"] * (V - EK) / (1 + math.exp((V - EK - 0.010) / 0.010))      # rectification 10 mV
    m_nap = 1 / (1 + math.exp(-(V + 0.050) / 0.006))                               # Nav persistent window, V1/2 -50 mV
    I_NaP = p["g_NaP"] * m_nap * (V - ENa)
    I_Na = ghk(p["P_Na"], 1, V, Na, OUTSIDE["Na"]) + I_NaP
    I_Cl = ghk(p["P_Cl"], -1, V, Cl, OUTSIDE["Cl"])
    fNa = Na ** 3 / (Na ** 3 + 10.0 ** 3)
    fK = OUTSIDE["K"] ** 2 / (OUTSIDE["K"] ** 2 + 1.5 ** 2)
    Ip = p["Ip_max"] * fNa * fK                                                       # net outward, 3Na out : 2K in
    m_t = 1 / (1 + math.exp(-(V + 0.050) / 0.0074)); h_t = 1 / (1 + math.exp((V + 0.078) / 0.005))  # Cav3.1-like
    I_CaT = p["g_CaT"] * m_t ** 2 * h_t * (V - 0.120)                                 # ECa ~ +120 mV fixed
    return {"I_K2P": I_K2P, "I_Ko": I_Ko, "I_Kir": I_Kir, "I_Na": I_Na, "I_NaP": I_NaP, "I_Cl": I_Cl, "Ip": Ip, "I_CaT": I_CaT,
            "EK": EK, "ENa": ENa}


def rhs(t, y, p):
    V, Na, K, Cl = y
    c = currents(V, Na, K, Cl, p)
    Itot = c["I_K2P"] + c["I_Ko"] + c["I_Kir"] + c["I_Na"] + c["I_Cl"] + c["Ip"] + c["I_CaT"]
    k = A / (F * VOL) * 1e6   # (A/cm^2) -> mM/s
    return [-Itot / CM,
            -(c["I_Na"] + 3 * c["Ip"]) * k,
            -(c["I_K2P"] + c["I_Ko"] + c["I_Kir"] - 2 * c["Ip"]) * k,
            c["I_Cl"] * k]


def steady(p, y0=(-0.045, 12.0, 140.0, 30.0), t_end=2e6):
    s = solve_ivp(rhs, (0, t_end), list(y0), args=(p,), method="LSODA", rtol=1e-9, atol=[1e-9, 1e-7, 1e-7, 1e-7])
    y = s.y[:, -1]
    d = rhs(0, y, p)
    c = currents(*y, p)
    # time for Vm to come within 1 mV of its final value
    far = np.where(np.abs(s.y[0] - y[0]) >= 1e-3)[0]
    tv = float(s.t[far[-1] + 1]) if len(far) and far[-1] + 1 < len(s.t) else (0.0 if not len(far) else None)
    return {"ok": bool(s.success), "Vm_mV": y[0] * 1e3, "Na_i": y[1], "K_i": y[2], "Cl_i": y[3],
            "EK_mV": c["EK"] * 1e3, "ENa_mV": c["ENa"] * 1e3, "I_CaT_pA": c["I_CaT"] * A * 1e12, "Ip_pA": c["Ip"] * A * 1e12,
            "max_abs_rate": float(max(abs(d[0]) * 1e3, *map(abs, d[1:]))), "t_settle_Vm_s": tv}


def step_response(p, y0, times=(600.0, 3600.0, 21600.0, 86400.0)):
    """Kcnk5b changed as a step at t=0 from the baseline state y0 (e.g. heat-shock induction); state at fixed times."""
    s = solve_ivp(rhs, (0, max(times)), list(y0), args=(p,), method="LSODA", rtol=1e-9, atol=[1e-9, 1e-7, 1e-7, 1e-7], t_eval=list(times))
    return [{"t_s": float(t), "Vm_mV": float(s.y[0][i] * 1e3), "Na_i": float(s.y[1][i]), "K_i": float(s.y[2][i]), "Cl_i": float(s.y[3][i])}
            for i, t in enumerate(s.t)]


def fixed_gradient_vm(p, Na=12.0, K=140.0, Cl=30.0):
    """Instantaneous Vm with concentrations clamped (the 'textbook' view): root of total current."""
    from scipy.optimize import brentq
    # channel currents only (no pump), I_NaP already inside I_Na
    f = lambda V: sum(currents(V, Na, K, Cl, p)[k] for k in ("I_K2P", "I_Ko", "I_Kir", "I_Na", "I_Cl", "I_CaT"))
    try:
        return brentq(f, -0.15, 0.08) * 1e3
    except ValueError:
        return None


def main():
    t0 = time.time()
    folds = [0.0, 0.25, 0.5, 1, 2, 4, 8, 16, 32]
    pumps = {"pump_x0.5": 0.5, "pump_x1": 1.0, "pump_x2": 2.0}
    sweep = {}
    for pn, pf in pumps.items():
        rows = []
        for f in folds:
            p = dict(BASE, P_K2P=BASE["P_K2P"] * f, Ip_max=BASE["Ip_max"] * pf)
            r = steady(p)
            r.update({"kcnk5b_fold": f, "Vm_fixed_gradient_mV": fixed_gradient_vm(p)})
            rows.append(r)
            print(pn, f, round(r["Vm_mV"], 2), round(r["K_i"], 1), round(r["Na_i"], 1), r["Vm_fixed_gradient_mV"], round(r["I_CaT_pA"], 4), flush=True)
        sweep[pn] = rows
    # Na-route control: same sweep with the persistent Na conductance removed (Yi 2024 report Na-channel dependence)
    nonap = []
    for f in folds:
        p = dict(BASE, P_K2P=BASE["P_K2P"] * f, g_NaP=0.0)
        r = steady(p); r["kcnk5b_fold"] = f; nonap.append(r)
        print("noNaP", f, round(r["Vm_mV"], 2), round(r["K_i"], 1), flush=True)
    # Hypothesis arm: Kcnk5b recruits Na channels (g_NaP scales as fold**c). c=0 is pure passive coupling.
    coupled = {}
    for cexp in [0.0, 0.5, 1.0, 1.5]:
        rows = []
        for f in folds:
            p = dict(BASE, P_K2P=BASE["P_K2P"] * f, g_NaP=BASE["g_NaP"] * (f ** cexp))  # 0.0**0 == 1 keeps the c=0 arm passive
            r = steady(p); r["kcnk5b_fold"] = f; rows.append(r)
            print("coupling", cexp, f, round(r["Vm_mV"], 2), round(r["K_i"], 1), round(r["I_CaT_pA"], 4), flush=True)
        coupled[f"c={cexp}"] = rows
    # hysteresis check: start each run hyperpolarised instead of depolarised
    hyst = []
    for f in folds:
        p = dict(BASE, P_K2P=BASE["P_K2P"] * f)
        r = steady(p, y0=(-0.085, 12.0, 140.0, 8.0)); r["kcnk5b_fold"] = f; hyst.append(r)
    # Developmental-timescale view: the full ion steady state takes days (t_settle_Vm_s), longer than fin-bud
    # growth, so report a step change of Kcnk5b from the 1x state at 10 min, 1 h, 6 h, 24 h.
    b = steady(dict(BASE)); y0 = (b["Vm_mV"] * 1e-3, b["Na_i"], b["K_i"], b["Cl_i"])
    steps = {}
    for cexp in [0.0, 1.0]:
        steps[f"c={cexp}"] = []
        for f in folds:
            p = dict(BASE, P_K2P=BASE["P_K2P"] * f, g_NaP=BASE["g_NaP"] * (f ** cexp))
            steps[f"c={cexp}"].append({"kcnk5b_fold": f, "trajectory": step_response(p, y0)})
            tr = steps[f"c={cexp}"][-1]["trajectory"]
            print("step", cexp, f, [round(q["Vm_mV"], 1) for q in tr], [round(q["K_i"], 1) for q in tr], flush=True)
    # Kcnj13 (Kir7.1) loss as a second channel perturbation
    kir = []
    for g in [0.0, 0.5, 1.0, 2.0]:
        p = dict(BASE, g_Kir=BASE["g_Kir"] * g)
        r = steady(p); r["kcnj13_fold"] = g; kir.append(r)
    out = {"model": "pump-leak single cell, GHK leaks + Kir + persistent Na + Na/K-ATPase; T-type window current readout",
           "parameters_base": BASE, "outside_mM": OUTSIDE, "temperature_K": T, "radius_cm": r_cm,
           "parameter_status": "all assumed generic vertebrate values; none fitted or measured in zebrafish",
           "kcnk5b_sweep_by_pump_capacity": sweep, "kcnk5b_sweep_no_persistent_Na": nonap, "kcnk5b_na_recruitment_hypothesis": coupled, "kcnk5b_sweep_hyperpolarised_start": hyst, "kcnk5b_step_from_1x_state": steps, "step_baseline_state": b, "kcnj13_sweep": kir,
           "sources_for_qualitative_targets": {"PMID:38527087": "Yi et al. 2024 PLoS Biol: Kcnk5b overexpression decreases intracellular K+, enhances depolarisation via Na+ channels, increases fin-bud size; shha induction needs IP3R Ca2+ release",
                                               "PMID:41321290": "Dev 2025: depolarisation of fin fibroblasts triggers VGCC Ca2+ spikes; cacna1g mutants regenerate long fins"}}
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "s5_bioelectric_kcnk5b_sweep.json"
    p.write_text(json.dumps(out, indent=1, sort_keys=True))
    rec = {"sim": "s5", "command": ".venv-mol/bin/python experiments/mol_sims/bioelectric_cell.py", "exit_code": 0,
           "scipy": scipy.__version__, "integrator": "LSODA rtol=1e-9", "seed": None, "seed_note": "deterministic ODE",
           "input_sha256": {"script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
           "output_sha256": {"result": hashlib.sha256(p.read_bytes()).hexdigest()}, "evidence_kind": "simulated",
           "scope": "SIMULATED, not observed. Assumed generic parameters; qualitative sign test only; no zebrafish calibration.",
           "wall_seconds": round(time.time() - t0, 1)}
    (OUT / "s5_receipt.json").write_text(json.dumps(rec, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
