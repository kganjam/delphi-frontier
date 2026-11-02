#!/usr/bin/env python3
"""Assemble cargo-work.json from the four arms, and apply the corrections the
arms themselves exposed."""
import json, os, statistics
import numpy as np
ROOT = "/data/scratch/designspaces/xenobot"
MU_K, G = 0.8, 9.80665

W = json.load(open(f"{ROOT}/cargo-work.raw.json"))
B = json.load(open(f"{ROOT}/data/cargo-arm1b.json"))
M = json.load(open(f"{ROOT}/data/cargo-arm2b.json"))
S = json.load(open(f"{ROOT}/data/cargo-arm3.json"))
GAITS = ("uniform", "longitudinal", "lateral", "dorsoventral", "travelling", "checker")

R = {"schema": "design-space-study/0.1", "id": "cargo-work"}
R["headline"] = ("In this dry-friction model the body plan that moves itself best also pushes best: "
                 "the travelling wave wins on cargo displacement, on transport ratio and on energy "
                 "efficiency, contradicting our predeclared expectation. The real design gate is not "
                 "which gait ranks highest but whether the gait moves an external object at all, and "
                 "in 5 cycles only one of six even reaches its cargo.")
R["declared_metrics"] = W["declared_metrics"]
R["predeclared_expectation"] = {
    "statement": "the gait that moves the construct itself furthest will NOT be the gait that pushes an external object furthest",
    "outcome": "REFUTED",
    "evidence": "travelling is first on every metric in arm 1b: cargo displacement 103.6 mm vs 35.8 mm (longitudinal) and 21.7 mm (lateral); transport ratio 0.947 vs 0.508 and 0.260; efficiency 0.0326 vs 0.0114 and 0.0044. The ordering is identical to the self-locomotion ordering and the gap is WIDER in pushing than in self-locomotion.",
    "note": "We record this as a failed prediction rather than reframing it. One pilot run of the travelling pattern was executed as a plumbing check before the metrics were written down, and its cargo displacement was seen; every other number here was produced afterwards."}

R["model"] = {
    "engine": {"name": "Voxelyze", "commit": "4287e365e11416dd108f2f361e9ec4c5a011a16c",
               "licence_from_source_headers": "LGPL-3.0-or-later",
               "driver": "code/cargo_actuation.cpp, OUR code, extending the delphi-frontier soft_actuation driver with a second never-actuated material, an actuation-work accumulator and a seeded RNG for particle placement"},
    "regression_control": "with the cargo removed, this driver reproduces the pinned artifact's travelling run bit-for-bit at 0.0145773 m against the published 0.014577281 m",
    "parameters": [
        {"name": "voxel_m", "value": 0.01, "units": "m", "status": "sourced",
         "source": "voxcraft/voxcraft-sim demos/basic/base.vxa @ dd8668f9, Lattice_Dim, via the pinned artifact's protocol.json"},
        {"name": "E", "value": 1e5, "units": "Pa", "status": "sourced", "source": "same base.vxa, Elastic_Mod"},
        {"name": "rho", "value": 1e3, "units": "kg m^-3", "status": "sourced", "source": "same base.vxa, Density"},
        {"name": "poisson", "value": 0.35, "units": "-", "status": "sourced", "source": "same base.vxa, Poissons_Ratio"},
        {"name": "mu_static", "value": 1.0, "units": "-", "status": "sourced", "source": "same base.vxa, uStatic"},
        {"name": "mu_kinetic", "value": 0.8, "units": "-", "status": "sourced", "source": "same base.vxa, uDynamic"},
        {"name": "cte", "value": 0.01, "units": "degC^-1", "status": "assumed",
         "source": "declared engineering choice in the pinned protocol; no measured biological referent"},
        {"name": "temp_amplitude", "value": 10.0, "units": "degC", "status": "assumed",
         "source": "same; cte x amplitude gives 0.10 peak linear strain"},
        {"name": "freq", "value": 4.0, "units": "Hz", "status": "assumed", "source": "same"},
        {"name": "zeta_internal", "value": 1.0, "units": "-", "status": "assumed", "source": "same"},
        {"name": "zeta_global", "value": 0.1, "units": "-", "status": "assumed",
         "source": "same; a numerical absolute-frame term, NOT fluid drag"},
        {"name": "zeta_collision", "value": 0.8, "units": "-", "status": "assumed", "source": "same"},
        {"name": "g", "value": 9.80665, "units": "m s^-2", "status": "sourced",
         "source": "standard gravity, used only in the closed-form friction work"},
        {"name": "cargo_volume", "value": 8, "units": "voxels", "status": "assumed",
         "source": "our choice: the smallest block that is clearly an object rather than a particle"},
        {"name": "cargo_gap", "value": 1, "units": "lattice sites", "status": "assumed",
         "source": "our choice, and it is the MINIMUM: at zero gap Voxelyze would link the cargo to the construct and fuse them"},
        {"name": "contact_threshold", "value": 1e-6, "units": "m", "status": "assumed",
         "source": "our choice, declared before arm 1b was run"}]}

R["controls"] = dict(W["controls"])
R["controls"]["C5b_swarm_zero_amplitude_fixed_geometry"] = S["control_zero_amplitude"]
R["controls"]["C6_degenerate_swarm_geometry_refused"] = {
    "what": "the driver exits 4 if any construct is placed outside the particle field, because swarm size would then not be the only variable",
    "why_it_exists": "the FIRST version of the swarm arm auto-spread constructs over a square field and silently pushed the outermost ones outside it at N=6 and N=8, which returned bit-identical particle outcomes for those two sizes. That run is discarded and not reported.",
    "verified": "running 8 constructs against a field of half-width 5 sites prints the FATAL line and refuses"}
R["all_controls_met"] = all(v.get("met", True) for v in R["controls"].values())

# ---------------------------------------------------- arm 1 and arm 1b ----
R["arm1_reach_limited_5_cycles"] = {
    "finding": "at the artifact's own 5 cycles the arm measures REACH, not push. The cargo's nearest surface sits 7.5 mm from the construct's (one clear lattice site, minus two 6.25 mm collision envelopes) and only the travelling wave covers that distance in 5 cycles. Every other gait scores exactly zero because it never arrives.",
    "engineering_reading": "this is a real result and not only an artifact of our geometry: a construct that moves slowly never reaches its workpiece within its working life. It is reported separately from the push question rather than mixed into it.",
    "per_gait": {g: {"self_locomotion_m": W["arm1_directed_push"]["per_gait"][g]["self_locomotion"]["net_disp_m"],
                     "cargo_best_m": W["arm1_directed_push"]["per_gait"][g]["M1_best"]} for g in GAITS}}
R["arm1b_contact_gated_40_cycles"] = {
    "design": B["design" ] if "design" in B else B["declared_before_running"],
    "contact_threshold_m": B["declared_contact_threshold_m"],
    "gaits_that_made_contact": B["gaits_that_made_contact"],
    "gaits_that_never_reached_the_cargo_in_40_cycles": [g for g in GAITS if g not in B["gaits_that_made_contact"]],
    "per_gait": {g: {
        "self_locomotion_40cyc_m": B["per_gait"][g]["self_locomotion_40cyc"]["net_disp_m"],
        "best_direction": B["per_gait"][g]["best_direction"],
        "M1_cargo_net_disp_m": B["per_gait"][g]["M1_best_m"],
        "transport_ratio_after_contact": B["per_gait"][g]["transport_ratio_after_contact"],
        "efficiency_after_contact": B["per_gait"][g]["efficiency_after_contact"]} for g in GAITS},
    "ranking_self_locomotion": B["ranking_self_locomotion"],
    "ranking_cargo_transport": B["ranking_cargo_transport"],
    "ranking_transport_ratio_contacting_only": B["ranking_transport_ratio_contacting_only"],
    "ranking_efficiency_contacting_only": B["ranking_efficiency_contacting_only"],
    "rankings_agree": B["ranking_self_locomotion"][:3] == B["ranking_cargo_transport"][:3]}

# ------------------------- reach and push are different quantities --------
reach, push = {}, {}
for g in GAITS:
    row = B["per_gait"][g]
    bd = row["best_direction"]
    c = row["by_direction"][bd]["contact"] if bd else {"made_contact": False}
    reach[g] = {
        "self_speed_mm_per_cycle": row["self_locomotion_40cyc"]["net_disp_m"] * 1000 / 40.0,
        "made_contact_within_40_cycles": c.get("made_contact", False),
        "time_to_contact_s": c.get("contact_t_s"),
        "cycles_to_contact": (c["contact_t_s"] * 4.0) if c.get("made_contact") else None,
        "fraction_of_run_spent_reaching": c.get("contact_frac_of_run")}
    if c.get("made_contact"):
        push[g] = {
            "cargo_displacement_after_contact_m": c["cargo_disp_after_contact_m"],
            "construct_path_after_contact_m": c["construct_path_after_contact_m"],
            "transport_ratio_after_contact": c["transport_ratio_after_contact"],
            "W_actuation_after_contact_J": c["W_actuation_after_contact_J"],
            "W_cargo_friction_after_contact_J": c["W_cargo_friction_after_contact_J"],
            "efficiency_after_contact": c["efficiency_after_contact"]}
_pr = None
R["reach_and_push_are_different_quantities"] = {
    "why_they_are_reported_separately": "time-to-contact and work-after-contact are different engineering quantities, and a body plan can be good at one and bad at the other. Collapsing them into a single cargo-displacement number hides which one a design is losing on, and in the 5-cycle arm it hid the fact that five of six gaits were losing on REACH and had not been tested on push at all.",
    "reach_gate": "does the construct arrive at the workpiece within its working life? Measured here as time to first cargo motion above 1 um, with the cargo 7.5 mm of clear space away.",
    "push_gate": "given contact, how much of the construct's own motion and energy reaches the cargo? Measured over the post-contact window only.",
    "reach": reach,
    "push_contacting_gaits_only": push,
    "ranking_by_reach": sorted([g for g in GAITS if reach[g]["made_contact_within_40_cycles"]],
                               key=lambda g: reach[g]["time_to_contact_s"]),
    "ranking_by_push_transport_ratio": sorted(push, key=lambda g: -push[g]["transport_ratio_after_contact"]),
    "do_the_two_rankings_agree": (
        sorted([g for g in GAITS if reach[g]["made_contact_within_40_cycles"]],
               key=lambda g: reach[g]["time_to_contact_s"])
        == sorted(push, key=lambda g: -push[g]["transport_ratio_after_contact"])),
    "commercial_reading": (
        "The two orderings are NOT the same, which is the reason for reporting them apart. "
        "Travelling is first on both. But between the two reciprocal gaits the order swaps: "
        "lateral reaches the cargo FIRST (1.71 s against longitudinal's 1.79 s) and then pushes "
        "WORST, transferring 0.26 of its own path against longitudinal's 0.51. So arriving "
        "sooner and pushing better are separable properties here, and a cargo-displacement "
        "number alone would have hidden it."),
    "size_of_the_swap": {
        "reach_difference_lateral_vs_longitudinal_pct": 100 * abs(
            reach["longitudinal"]["time_to_contact_s"] - reach["lateral"]["time_to_contact_s"])
            / reach["longitudinal"]["time_to_contact_s"],
        "push_ratio_longitudinal_over_lateral": (
            push["longitudinal"]["transport_ratio_after_contact"]
            / push["lateral"]["transport_ratio_after_contact"]) if {"longitudinal","lateral"} <= set(push) else None,
        "honest_scale": "the reach difference between those two is about 4.8%, which is small and rests on a single contact-threshold crossing per gait with no seed spread (this model has no RNG). The push difference is about 2x and is the robust half of the comparison. Do not read the reach swap as a strong result."}}

# -------------------------------------------------------------- arm 2b ---
m2 = {}
for g, rows in M["per_gait"].items():
    out = {}
    for rs, v in rows.items():
        wact = v["M3_W_cargo_friction_J"] / v["M4_efficiency"] if v["M4_efficiency"] else None
        wnet = MU_K * v["cargo_mass_kg"] * G * v["M1_cargo_net_disp_m"]
        out[rs] = dict(v)
        out[rs]["W_actuation_J_derived"] = wact
        out[rs]["W_useful_directed_J"] = wnet
        out[rs]["efficiency_directed"] = (wnet / wact) if wact else None
    m2[g] = out
stall = {}
for g, rows in m2.items():
    ks = sorted(rows, key=float)
    d = [rows[k]["M1_cargo_net_disp_m"] for k in ks]
    drop = [(float(ks[i + 1]), d[i] / d[i + 1] if d[i + 1] else float("inf")) for i in range(len(d) - 1)]
    worst = max(drop, key=lambda t: t[1])
    stall[g] = {"stall_between_rho": worst[0], "displacement_drop_factor": worst[1],
                "cargo_mass_at_stall_kg": rows[str(worst[0])]["cargo_mass_kg"],
                "best_directed_efficiency": max(
                    (rows[k]["efficiency_directed"], float(k)) for k in ks if rows[k]["efficiency_directed"] is not None)}
R["arm2b_cargo_mass"] = {
    "design": M["design"],
    "per_gait": m2,
    "stall": stall,
    "metric_correction": {
        "problem": "our declared efficiency M4 uses the cargo's PATH LENGTH, so a stalled cargo that is merely jiggled back and forth still accumulates friction work. Past the stall threshold M4 therefore RISES while transport collapses: travelling at 256 g reports the highest M4 of the whole sweep (0.134) while moving the cargo 0.105 mm.",
        "fix": "we add efficiency_directed, which uses the cargo's NET displacement instead, a stricter lower bound on useful directed work. Both are reported; M4 is the declared metric and is not deleted.",
        "rule": "M4 is meaningful only BELOW the stall threshold."},
    "ranking_by_mass": M["ranking_by_mass"],
    "ranking_apparently_changes": not M["ranking_is_constant_across_mass"],
    "ranking_change_is_not_real": "the ordering of longitudinal and lateral swaps only at 128 g and 256 g, where BOTH are stalled and both move the cargo by less than 0.25 mm. That is a swap between two noise-floor values, not a reversal, and it must not be reported as the ranking depending on cargo mass."}

# --------------------------------------------------------------- arm 3 ---
ns = sorted(S["per_N"], key=int)
s1 = [S["per_N"][n]["S1_min_median_max"][1] for n in ns]
fit = np.polyfit(np.log([float(n) for n in ns]), np.log(s1), 1)
R["arm3_swarm"] = {
    "design": "N constructs evenly spread along y inside a FIXED rectangular particle field (x -16..+2, y -22..+22 lattice sites) holding 120 single-voxel passive particles; 40 actuation cycles; 5 seeds; every construct runs the travelling gait. The field is offset to -x because that is the direction all these gaits travel, so the swept and seeded regions coincide.",
    "n_particles": S["n_particles"], "seeds": S["seeds"], "field": S["field"],
    "per_N": S["per_N"],
    "S1_scaling_exponent_vs_N": float(fit[0]),
    "S1_scaling_reading": f"mean particle displacement scales as N^{fit[0]:.2f} over N = 1 to 8, i.e. very slightly superlinear. Eight constructs move {s1[-1]/s1[0]:.1f}x as much material as one.",
    "S4_energy_efficiency_flat": {
        "values": {n: S["per_N"][n]["S4_fric_per_actuation_median"] for n in ns},
        "reading": "friction work done on the field per unit actuation work is 0.0066-0.0102 across the whole range and does not improve with swarm size. A bigger swarm moves more material because it spends more energy, not because it spends it better."},
    "S2_aggregation": {
        "values_min_median_max_m": {n: S["per_N"][n]["S2_min_median_max"] for n in ns},
        "as_percent_of_field_radius": {
            n: {"rg_start_m": S["per_N"][n]["per_seed"][0]["rg_start_m"],
                "median_change_pct": 100 * S["per_N"][n]["S2_min_median_max"][1]
                                     / S["per_N"][n]["per_seed"][0]["rg_start_m"]} for n in ns},
        "effect_size_caution": (
            "State this as an effect size, not as a mechanism. The median change is 0.22% to 0.77% of the "
            "field's radius of gyration, and it is NOT monotone in N: N=8 sits below N=6 and barely above "
            "N=1. A sub-1% change that does not scale with swarm size is 'the field barely moves', not "
            "dispersal. For scale, the particles' centre of mass travels 1.9 to 19 mm over the run while a "
            "construct travels 116 mm. The defensible claim is NO AGGREGATION AT ANY N; the word 'disperses' "
            "invites a reader to think a mechanism was identified, and none was."),
        "verdict": "NO aggregation. The particle field's radius of gyration INCREASED in 28 of the 30 runs. Both exceptions are at the largest swarm size, N=8, where 2 of 5 seeds turn negative (-0.111 and -0.457 mm) and the median dispersion falls 2.6-fold from its N=6 value. That is a possible ONSET rather than scatter, and it is tested in the follow-up arm rather than left as a hedge.",
        "mechanism": "every construct runs the same gait and travels the same way, so their contributions add as a common drift rather than converging. Corralling needs either a concave body that traps material, as the published semitoroidal progenitor has, or constructs that move differently from one another.",
        "scope": "this is a statement about a uniform, sensorless, single-gait swarm in this model. It is not a statement about swarms."}}

R["limitations"] = [
    "This is the dry-friction regime - Coulomb friction on a rigid floor under gravity, plus a numerical absolute-frame damping term - matching the artifact it extends. Our own regime-check study finds that a real millimetre-scale construct sits at Reynolds number below 0.1, where four of the six gaits compared here produce exactly zero displacement and could not push anything at all. Every number in this study is inside a model the first study says is the wrong regime.",
    "The cargo gap is one lattice site because that is the minimum that avoids Voxelyze linking the two bodies into one. That sets a 7.5 mm clear distance the construct must cross before any pushing happens, which is why arm 1 is reach-limited and arm 1b exists.",
    "W_actuation is the axial term only: bending and torsion rest states are not actuated so they do no actuation work, but they do store and dissipate energy that is not counted. The actuation efficiency is therefore an UPPER bound on the fraction of total input energy delivered.",
    "W_cargo_friction is a closed form that ignores collision damping and any kinetic energy left in the cargo at the end, so it is a LOWER bound on work done on the cargo.",
    "Our declared efficiency metric M4 breaks down past the stall threshold, for the reason recorded above. We found this by running the sweep far enough to stall rather than stopping at a mass where the metric still behaved.",
    "The swarm's particles are single voxels on the floor with the same friction and density as the construct. Nothing is calibrated to cells, debris or microplastic.",
    "Voxelyze has no random number generator and this driver's only randomness is our own seeded particle placement, so the seed spread reported here is spread over ARENAS, not over mechanics. Repeat runs at a fixed seed are bitwise identical."]
R["what_this_cannot_establish"] = [
    "that any construct would push anything in water, which is the regime that matters",
    "that a real xenobot or anthrobot can transport a defined cargo; no published one has",
    "a force, a modulus or a transport rate for any organism",
    "that a swarm cannot aggregate - only that this uniform single-gait swarm does not"]
json.dump(R, open(f"{ROOT}/cargo-work.json", "w"), indent=2)
print("controls all met:", R["all_controls_met"])
print("rankings agree (top 3):", R["arm1b_contact_gated_40_cycles"]["rankings_agree"])
print("S1 ~ N^%.2f" % fit[0])
for g, v in stall.items():
    print(f"  stall {g:13s} at rho x{v['stall_between_rho']:<5g} m={v['cargo_mass_at_stall_kg']*1000:6.1f} g drop={v['displacement_drop_factor']:.1f}x  best directed eff {v['best_directed_efficiency'][0]:.4f} at rho x{v['best_directed_efficiency'][1]:g}")
print("wrote cargo-work.json")
