#!/usr/bin/env python3
"""Fold the cohesion arm into cargo-work.json and let it decide how the swarm
result is stated. Three branches, declared in advance in the arm itself."""
import json, statistics
ROOT = "/data/scratch/designspaces/xenobot"
A = json.load(open(f"{ROOT}/data/cargo-arm3c.json"))
C = json.load(open(f"{ROOT}/cargo-work.json"))
cohs = sorted(A["per_cohesion"], key=float)

rows = []
for c in cohs:
    e = A["per_cohesion"][c]
    act = sum(e["by_N"][n]["aggregating_seeds"] for n in e["by_N"])
    tot = sum(len(e["by_N"][n]["per_seed"]) for n in e["by_N"])
    ctl = e["control_amp0"]["aggregating_seeds"]
    meds = {n: e["by_N"][n]["rg_change_pct_min_median_max"][1] for n in e["by_N"]}
    rows.append({"cohesion_x_friction": float(c), "aggregating_runs_actuated": act,
                 "actuated_runs": tot, "aggregating_runs_control_amp0": ctl,
                 "control_runs": len(e["control_amp0"]["per_seed"]),
                 "median_rg_change_pct_by_N": meds,
                 "control_median_rg_change_pct": e["control_amp0"]["rg_change_pct_min_median_max"][1]})

any_act = any(r["aggregating_runs_actuated"] for r in rows)
any_ctl = any(r["aggregating_runs_control_amp0"] for r in rows)
first_act = next((r["cohesion_x_friction"] for r in rows if r["aggregating_runs_actuated"]), None)
first_ctl = next((r["cohesion_x_friction"] for r in rows if r["aggregating_runs_control_amp0"]), None)
# a credited onset needs aggregation WITH actuation at a cohesion where the control shows none
credited = [r["cohesion_x_friction"] for r in rows
            if r["aggregating_runs_actuated"] and not r["aggregating_runs_control_amp0"]]

if credited and len(credited) >= 1 and all(
        r["aggregating_runs_actuated"] == 0 for r in rows
        if r["cohesion_x_friction"] < min(credited)):
    branch = "H1_knob_on_the_cargo"
    verdict = (f"H1 SUPPORTED. Aggregation appears only at cohesion >= {min(credited)}x the particle's own "
               f"sliding friction, and never below it, and at that level the amp=0 control shows none - so it "
               f"is the swarm doing the piling and not cohesion alone. The design knob for aggregation is on "
               f"the CARGO, not on the robot: a swarm that cannot corral a frictionless field can corral an "
               f"adhesive one. This inverts the main arm's negative into a positive and it matches the "
               f"published system, whose feedstock was dissociated cells that adhere.")
elif not any_act:
    branch = "H2_no_knob"
    verdict = ("H2 SUPPORTED. No cohesion value tested, up to 10x the particle's own sliding friction, "
               "produces aggregation under actuation. The main arm's negative is therefore much stronger "
               "than it was: it is not an artifact of frictionless cargo, because giving the cargo adhesion "
               "does not rescue it. A uniform, sensorless, single-gait swarm does not corral even an "
               "adhesive field.")
elif any_ctl:
    branch = "CONFOUNDED_by_cohesion_alone"
    verdict = (f"CONFOUNDED above cohesion {first_ctl}x: the amp=0 control aggregates there too, so at and "
               f"above that level cohesion alone pulls the field together and no aggregation can be credited "
               f"to the swarm. Only cohesion levels where the control shows nothing can support a claim about "
               f"swarms, and those are: "
               f"{[r['cohesion_x_friction'] for r in rows if not r['aggregating_runs_control_amp0']]}.")
else:
    branch = "MIXED"
    verdict = ("Aggregation appears under actuation but not monotonically in cohesion, so neither declared "
               "hypothesis is cleanly supported. Reported as observed, per cohesion level, without a trend claim.")

C["arm3c_cohesion"] = {
    "status": "Added in response to review, and it is the arm that decides whether the swarm negative means anything.",
    "why": A["why"], "declared_hypotheses": A["declared_hypotheses"],
    "cohesion_units": A["cohesion_units"],
    "force_law": ("constant-magnitude pairwise attraction between PASSIVE PARTICLES ONLY, acting between 0.9 "
                  "and 1.8 lattice spacings, magnitude = cohesion x mu_k x m_particle x g. Constructs carry no "
                  "external force. Collision handles repulsion below 0.9 lattice spacings."),
    "regression_control": ("cohesion=0 reproduces the no-cohesion swarm run bit-for-bit: rg_change 0.000950188 m "
                           "and net 0.009208152 m, identical to the stored N=4 seed 1 run."),
    "sweep": rows, "per_cohesion": A["per_cohesion"],
    "branch": branch, "verdict": verdict,
    "control_reading": ("The amp=0 control is what makes any of this interpretable. At cohesion 0 it gives "
                        "exactly 0.000% change - with the actuation off, nothing moves at all - so every "
                        "effect at higher cohesion can be compared against a field that cohesion alone acts on."),
    "limitations": [
        "Three seeds per cell, not five, to keep 60 runs affordable.",
        "One force law, constant-magnitude within a shell. Real cell-cell adhesion is neither constant nor pairwise-additive, and Kriegman et al. 2021 modelled it as irreversible BONDING on collision rather than as an attractive force. A bonding model could behave differently and was not tested.",
        "Cohesion acts between particles only. Particles do not adhere to the constructs, which is how the published system's piles form on the dish rather than on the organism.",
        "Swarm sizes 1, 4 and 8 only, in the narrower field."]}
C["arm3_swarm"]["S2_aggregation"]["cohesion_tested"] = verdict
C["limitations"].append(
    "The swarm negative was tested against the obvious alternative - that our particles simply have no "
    "adhesion, so no gait could pile them - by sweeping a cohesion parameter over two decades with an "
    "actuation-off control at every level. See arm3c_cohesion for what that found.")
json.dump(C, open(f"{ROOT}/cargo-work.json", "w"), indent=2)
print("branch:", branch)
print(verdict)
print()
for r in rows:
    print(f"  coh={r['cohesion_x_friction']:<5g} actuated {r['aggregating_runs_actuated']}/{r['actuated_runs']}"
          f"  control {r['aggregating_runs_control_amp0']}/{r['control_runs']}"
          f"  medians {({k: round(v,3) for k,v in r['median_rg_change_pct_by_N'].items()})}"
          f"  ctrl_med {r['control_median_rg_change_pct']:+.3f}%")
