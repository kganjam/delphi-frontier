#!/usr/bin/env python3
"""Reconcile every headline number quoted in prose (routes.json, index-fragment.json,
NOTES.md) against the data file it comes from. Run after any edit. Exit 1 on a
mismatch, because a number in prose that the data does not support is a defect.
"""
import json, math, re, sys
ROOT = "/data/scratch/designspaces/xenobot"
rc = json.load(open(f"{ROOT}/regime-check.json"))
cv = json.load(open(f"{ROOT}/convergence.json"))
cw = json.load(open(f"{ROOT}/cargo-work.json"))
rt = json.load(open(f"{ROOT}/routes.json"))
ok = True


def chk(label, got, want, tol=0.03):
    global ok
    good = abs(got - want) / max(abs(want), 1e-30) <= tol
    ok &= good
    print(("  OK   " if good else "  FAIL ") + f"{label}: prose {want}, data {got}")


print("== regime-check")
A = rc["reynolds_map"]["anchors"]
chk("anthrobot Re min 1.5e-4", A[0]["Re"], 1.5e-4, 0.05)
chk("anthrobot Re max 2.5e-2", A[1]["Re"], 2.5e-2, 0.05)
chk("1 mm xenobot Re 0.0996", A[2]["Re"], 0.0996, 0.01)
chk("artifact Re 643", rc["simulated_object_regime"]["Re_translational"], 643, 0.01)
chk("orders apart 3.8", rc["regime_separation_orders_of_magnitude"], 3.8, 0.02)
chk("artifact speed 12.9 mm/s", rc["simulated_object_regime"]["U_m_s"] * 1000, 12.9, 0.01)
chk("stokes travelling 0.0342", rc["stokes_ranking"]["per_gait_body_lengths_per_cycle"]["travelling"], 0.0342, 0.01)
chk("dry travelling 0.364", rc["dry_friction_ranking"]["per_gait_body_lengths_5_cycles"]["travelling"], 0.364)
chk("dry longitudinal 0.153", rc["dry_friction_ranking"]["per_gait_body_lengths_5_cycles"]["longitudinal"], 0.153)
chk("longitudinal area 1.9e-16", rc["reciprocity"]["per_gait"]["longitudinal"]["enclosed_area_per_voxel"], 1.9e-16, 0.06)
chk("spearman 0.94", rc["ranking_comparison"]["spearman_rho_all_six"], 0.94, 0.01)
assert len(rc["reciprocity"]["reciprocal_gaits"]) == 5
assert rc["reciprocity"]["non_reciprocal_gaits"] == ["travelling"]
assert all(v["rejected"] for v in rc["stokes_must_fail_controls"].values())
print("  OK   5 reciprocal / 1 not; all 4 must-fail arms rejected")

print("== convergence")
sA = cv["refinement_series"]["series"]["A_travelling"]
sB = cv["refinement_series"]["series"]["B_longitudinal"]
chk("A spread 41%", sA["total_spread_rel_to_coarsest"], 0.41, 0.03)
chk("B spread 54%", sB["total_spread_rel_to_coarsest"], 0.54, 0.03)
assert not sA["monotone"] and not sB["monotone"]
r = cv["ranking_stability"]["travelling_over_longitudinal_by_level"]
chk("margin 19.4 -> 10.4 (coarse)", r[0], 19.4, 0.01)
chk("margin 19.4 -> 10.4 (fine)", r[-1], 10.4, 0.01)
d1 = cv["parity_vs_resonance"]["D1_alternation_must_appear_in_travelling_too"]
chk("longitudinal alternation 20.3", d1["longitudinal_median_odd_over_even_neighbours"], 20.3, 0.01)
chk("travelling alternation 1.008", d1["travelling_median_odd_over_even_neighbours"], 1.008, 0.01)
fo = cv["parity_vs_resonance"]["D2_optimum_frequency_must_scale_as_1_over_L"]
chk("f_opt nx=4 is 12 Hz", fo["longitudinal_f_opt_nx4_Hz"], 12.0, 1e-9)
chk("f_opt nx=8 is 12 Hz", fo["longitudinal_f_opt_nx8_Hz"], 12.0, 1e-9)
ts = cv["timestep_separation_arm"]["per_series"]
chk("travelling spatial/temporal 17", ts["travelling"]["spatial_over_temporal"], 17, 0.05)
chk("longitudinal spatial/temporal 3.5", ts["longitudinal"]["spatial_over_temporal"], 3.5, 0.05)
chk("travelling max dt change 1.3%", ts["travelling"]["max_temporal_change_pct_at_fixed_grid"], 1.3, 0.05)
chk("longitudinal max dt change 15.5%", ts["longitudinal"]["max_temporal_change_pct_at_fixed_grid"], 15.5, 0.02)
cond = cv["conditioning_arm"]["measurement"]
chk("longitudinal amplification 1.2e6", cond["longitudinal"]["amplification"], 1.2e6, 0.02)
chk("travelling amplification 1.1e4", cond["travelling"]["amplification"], 1.15e4, 0.03)
chk("finest grid 2880 voxels", sA["levels"][-1]["voxels"], 2880, 0)
# parity range quoted in routes
lo = cv["parity_vs_resonance"]["parity_sweep"]["longitudinal"]
pairs = [lo[str(n)] / lo[str(m)] for n in range(3, 17) if n % 2
         for m in (n - 1, n + 1) if 3 <= m <= 16]
chk("parity adjacent min 7.6", min(pairs), 7.6, 0.02)
chk("parity adjacent max 66", max(pairs), 66.4, 0.02)
chk("parity adjacent median 23", sorted(pairs)[len(pairs) // 2], 23.1, 0.02)
chk("parity n pairs 13", len(pairs), 13, 0)

print("== cargo-work")
b = cw["arm1b_contact_gated_40_cycles"]["per_gait"]
chk("travelling cargo 103.6 mm", b["travelling"]["M1_cargo_net_disp_m"] * 1000, 103.6, 0.01)
chk("longitudinal cargo 35.8 mm", b["longitudinal"]["M1_cargo_net_disp_m"] * 1000, 35.8, 0.01)
chk("lateral cargo 21.7 mm", b["lateral"]["M1_cargo_net_disp_m"] * 1000, 21.7, 0.01)
chk("transport ratio 0.95", b["travelling"]["transport_ratio_after_contact"], 0.95)
chk("ratio 51%", b["longitudinal"]["transport_ratio_after_contact"] * 100, 51)
chk("ratio 26%", b["lateral"]["transport_ratio_after_contact"] * 100, 26)
chk("efficiency 3.3%", b["travelling"]["efficiency_after_contact"] * 100, 3.3)
chk("7.5x eff vs lateral", b["travelling"]["efficiency_after_contact"] / b["lateral"]["efficiency_after_contact"], 7.5, 0.03)
m = cw["arm2b_cargo_mass"]["per_gait"]["travelling"]
chk("eff 0.8% at 2 g", m["0.25"]["M4_efficiency"] * 100, 0.82, 0.03)
chk("eff 8.2% at 32 g", m["4.0"]["M4_efficiency"] * 100, 8.22, 0.02)
chk("disp 107 mm at 2 g", m["0.25"]["M1_cargo_net_disp_m"] * 1000, 106.8, 0.01)
chk("disp 78 mm at 32 g", m["4.0"]["M1_cargo_net_disp_m"] * 1000, 78.1, 0.01)
chk("disp 4.6 mm at 64 g", m["8.0"]["M1_cargo_net_disp_m"] * 1000, 4.58, 0.02)
chk("stall drop 17x", cw["arm2b_cargo_mass"]["stall"]["travelling"]["displacement_drop_factor"], 17.0, 0.02)
chk("spurious eff 13.4% at 256 g", m["32.0"]["M4_efficiency"] * 100, 13.37, 0.02)
chk("directed eff 0.08% at 256 g", m["32.0"]["efficiency_directed"] * 100, 0.08, 0.06)
for g, v in cw["arm2b_cargo_mass"]["stall"].items():
    assert abs(v["cargo_mass_at_stall_kg"] - 0.064) < 1e-9, g
print("  OK   all three gaits stall at 64 g")
sw = cw["arm3_swarm"]
chk("S1 exponent 1.15", sw["S1_scaling_exponent_vs_N"], 1.15, 0.02)
nd = sum(1 for n in sw["per_N"] for s in sw["per_N"][n]["per_seed"] if s["S2_rg_change_m"] > 0)
nt = sum(len(sw["per_N"][n]["per_seed"]) for n in sw["per_N"])
chk("dispersed in 28 of 30", nd, 28, 0); chk("of 30 runs", nt, 30, 0)
s4 = [sw["per_N"][n]["S4_fric_per_actuation_median"] for n in sw["per_N"]]
assert 0.006 <= min(s4) and max(s4) <= 0.011, s4
print(f"  OK   S4 flat in 0.007-0.010 (actual {min(s4):.4f}-{max(s4):.4f})")
assert cw["all_controls_met"] and cv["not_diverged_gate"]["gate_met"]
print("  OK   all controls met; no run diverged")

print("== routes.json structure")
req = ["id", "scale", "title", "intervention", "predicted_phenotype", "mechanism",
       "evidence_strength", "reversibility", "lethality_risk", "difficulty", "evidence"]
assert not [(r["id"], k) for r in rt["routes"] for k in req if k not in r]
scales = {s["key"] for s in rt["scales"]}
assert not {r["scale"] for r in rt["routes"]} - scales
assert not [r["id"] for r in rt["routes"]
            if not any(re.search(oc["match"], r["predicted_phenotype"], re.I)
                       for oc in rt["outcome_classes"])]
assert rt["recommendation"]["single_best_route"] in {r["id"] for r in rt["routes"]}
assert not [r["id"] for r in rt["routes"] if "study" in r
            and r["study"] not in {"regime-check", "convergence", "cargo-work"}]
print(f"  OK   {len(rt['routes'])} routes, {len(rt['scales'])} scales, all keys present, "
      f"no route invisible to the filter, recommendation resolves")

print("\nALL NUMBERS RECONCILE" if ok else "\nSOME NUMBERS DO NOT RECONCILE")
sys.exit(0 if ok else 1)
