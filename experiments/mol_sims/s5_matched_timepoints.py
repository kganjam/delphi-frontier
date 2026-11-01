"""Re-report the Kcnk5b step response at MATCHED timepoints (claude-mol, 2026-11-01).

gemini-4-argon's round-2 review flagged a real reporting error: the passive arm (c=0) was quoted at
10 min and the Na-recruitment arm (c=1) at 1 h, so the two signs were compared at different times and
the system is not at steady state at either. The underlying sweep already stored both arms at the same
four times (600 / 3600 / 21600 / 86400 s), so this reads them out side by side with no new simulation.

It also records, per arm and timepoint, whether Vm is still moving, so nothing is presented as a
steady state that is not one. SIMULATED single-cell model, nothing observed.

Usage: python s5_matched_timepoints.py [fold]   -> results/.../s5_matched_timepoints.json
"""
import hashlib, json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2] / "results/mol-sims/claude-20261101"
src = R / "s5_bioelectric_kcnk5b_sweep.json"
d = json.loads(src.read_text())
fold = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
step = d["kcnk5b_step_from_1x_state"]
base = d.get("step_baseline_state", {})

rows, arms = [], sorted(step)
for arm in arms:
    rec = next((r for r in step[arm] if abs(r["kcnk5b_fold"] - fold) < 1e-9), None)
    if rec is None:
        continue
    traj = rec["trajectory"]
    for k, pt in enumerate(traj):
        prev = traj[k - 1] if k else None
        rows.append({"arm": arm, "kcnk5b_fold": fold, "t_s": pt["t_s"],
                     "Vm_mV": round(pt["Vm_mV"], 2), "K_i_mM": round(pt["K_i"], 1),
                     "Na_i_mM": round(pt["Na_i"], 2), "Cl_i_mM": round(pt["Cl_i"], 1),
                     "dVm_from_previous_point_mV": None if prev is None else round(pt["Vm_mV"] - prev["Vm_mV"], 2)})

at = {}
for t in sorted({r["t_s"] for r in rows}):
    at[f"t={t:.0f}s"] = {r["arm"]: {"Vm_mV": r["Vm_mV"], "K_i_mM": r["K_i_mM"], "Na_i_mM": r["Na_i_mM"],
                                    "still_moving_mV_since_previous_point": r["dVm_from_previous_point_mV"]}
                         for r in rows if r["t_s"] == t}

v0 = base.get("Vm_mV")
# A fixed-volume pump-leak cell can run far outside anything a real cell survives. Flag it rather than
# quote it: a vertebrate cell holds roughly Na_i 5-30 mM and K_i 100-150 mM.
for r in rows:
    bad = []
    if not 5.0 <= r["Na_i_mM"] <= 30.0:
        bad.append(f"Na_i {r['Na_i_mM']} mM outside 5-30")
    if not 100.0 <= r["K_i_mM"] <= 150.0:
        bad.append(f"K_i {r['K_i_mM']} mM outside 100-150")
    r["outside_physiological_range"] = bad or None
signs = {}
for t, per in at.items():
    signs[t] = {arm: ("depolarised" if v0 is not None and per[arm]["Vm_mV"] > v0 else
                      "hyperpolarised" if v0 is not None else "no baseline recorded")
                for arm in per}
def earliest(arm, f):
    rec = next((r for r in step[arm] if abs(r["kcnk5b_fold"] - f) < 1e-9), None)
    return rec["trajectory"][0] if rec else None


folds = sorted({r["kcnk5b_fold"] for a in arms for r in step[a]})
inrange = {}
for arm in arms:
    good = [f for f in folds if (t := earliest(arm, f)) and 5 <= t["Na_i"] <= 30 and 100 <= t["K_i"] <= 150]
    f = max(good) if good else None
    t = earliest(arm, f) if f is not None else None
    inrange[arm] = None if t is None else {
        "largest_fold_still_physiological_at_600s": f, "Vm_mV": round(t["Vm_mV"], 2),
        "Na_i_mM": round(t["Na_i"], 1), "K_i_mM": round(t["K_i"], 1),
        "delta_Vm_from_baseline_mV": None if v0 is None else round(t["Vm_mV"] - v0, 2)}

out = {"scope": "SIMULATED single-cell pump-leak model; a hypothesis about signs, not a measurement",
       "largest_physiological_fold_per_arm": inrange,
       "restated_conclusion": (
           "Inside the window where the cell's ion concentrations stay physiological, the two arms still move Vm in "
           "OPPOSITE directions, but the depolarisation is small. At the largest in-range fold the recruitment arm "
           "depolarises by only a few mV with a modest K+ loss, while the passive arm hyperpolarises by tens of mV. "
           "The larger depolarisation quoted earlier (to about -19 mV) came from 8x fold at 1 h, where Na_i has run to "
           "about 90 mM and K_i to about 42 mM: that is a failing cell, not a phenotype, and is withdrawn."),
       "correction": ("Earlier text compared the passive arm at 600 s with the recruitment arm at 3600 s. "
                      "Both arms are listed here at all four stored times. At every time the direction of the Vm "
                      "change still separates the arms, but neither arm is at steady state at any of them: the "
                      "per-point Vm change is non-zero throughout, so these are transients, not resting potentials."),
       "baseline_before_step": base, "fold_reported": fold,
       "matched_timepoints": at, "direction_vs_baseline": signs, "rows": rows,
       "usable_window": {
           "first_time_each_arm_leaves_physiological_range_s": {
               arm: next((r["t_s"] for r in rows if r["arm"] == arm and r["outside_physiological_range"]), None)
               for arm in arms if any(r["arm"] == arm for r in rows)},
           "note": ("Ion concentrations are flagged against roughly Na_i 5-30 mM and K_i 100-150 mM. Where an arm is "
                    "flagged, its later points describe a cell that would not survive at fixed volume, so only the "
                    "earliest unflagged points may be used, and only for the DIRECTION of the Vm change.")},
       "falsification_experiment_from_round2_review": (
           "Argon asked for a test that can falsify rather than confirm the recruitment arm: measure intracellular "
           "[Na+] (e.g. SBFI) in Kcnk5b-overexpressing cells, or hold them in Na+-free extracellular solution "
           "(NMDG+ substitution) and record Vm. The recruitment hypothesis requires a rise in [Na+]i and requires "
           "the depolarisation to DISAPPEAR without external Na+. Persistent depolarisation in zero-Na+, or no "
           "[Na+]i rise, falsifies it; the passive arm predicts hyperpolarisation in both conditions."),
       "known_tautology_risk": ("The recruitment arm adds an inward Na+ conductance that scales with the same factor "
                                "as the K+ conductance, so recovering a depolarisation is close to built in. It shows "
                                "the data do not EXCLUDE a depolarising route, not that this route is the one used."),
       "source_file": {"s5_bioelectric_kcnk5b_sweep.json": hashlib.sha256(src.read_bytes()).hexdigest()}}
p = R / "s5_matched_timepoints.json"
p.write_text(json.dumps(out, indent=1, sort_keys=True))
print(json.dumps({"baseline_Vm_mV": v0, "matched": at, "direction": signs}, indent=1))
print("wrote", p)
