#!/usr/bin/env python3
"""arm 3c: does the swarm negative survive giving the particles ADHESION?

Why this exists. Kriegman et al. 2021's feedstock was dissociated Xenopus stem
cells, and their own simulation modelled them as "adhesive voxel singletons"
that "bonded" on collision. Our particles have no cohesion at all, so stirring
cannot pile them however good the gait is: without this arm the swarm result
measures the absence of adhesion rather than a property of swarms.

DECLARED BEFORE RUNNING:
  cohesion is a pairwise attraction between PASSIVE PARTICLES ONLY, of constant
  magnitude, expressed as a multiple of one particle's own sliding friction
  force mu_k*m*g, acting between 0.9 and 1.8 lattice spacings. Constructs carry
  no external force.
  H1 (knob on the cargo): aggregation appears above a cohesion threshold and
     never below it. Then the design knob for aggregation is the CARGO, not the
     robot, and the swarm negative inverts into a useful positive.
  H2 (no knob): no cohesion value produces aggregation. The negative is then
     much stronger, because the obvious alternative is ruled out.
  CONTROL, and it decides the whole arm: at every cohesion level, repeat with
     amp=0 so the constructs do not actuate. If the field aggregates THERE,
     cohesion alone did it and no aggregation at that level can be credited to
     the swarm. This is the positive control that has to sit beside the negative.
"""
import json, os, subprocess, statistics, time
BIN = "/data/scratch/designspaces/xenobot/build/cargo_actuation"
OUTD = "/data/scratch/designspaces/xenobot/data/cargo"
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]
FIELD = dict(fieldXlo=-16, fieldXhi=2, fieldYlo=-22, fieldYhi=22)
COHS, NS, SEEDS, NPARTS = (0.0, 0.1, 0.3, 1.0, 3.0, 10.0), (1, 4, 8), (1, 2, 3), 120


def run(tag, **kw):
    out = os.path.join(OUTD, tag)
    if not os.path.exists(out + ".json"):
        cmd = CAP + [BIN] + [f"--{k}={v}" for k, v in sorted(kw.items())] + [f"--out={out}"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        if p.returncode != 0:
            raise RuntimeError(f"{tag} rc={p.returncode} {p.stderr[-400:]}")
    return json.load(open(out + ".json"))


R = {"schema": "design-space-study/0.1", "id": "cargo-work-arm3c-cohesion",
     "why": __doc__.strip().split("Why this exists. ")[1].split("\n\nDECLARED")[0],
     "declared_hypotheses": {
         "H1_knob_on_the_cargo": "aggregation appears above a cohesion threshold and never below it",
         "H2_no_knob": "no cohesion value produces aggregation",
         "control": "at every cohesion level, amp=0 with constructs present. Aggregation there means cohesion alone did it and cannot be credited to the swarm."},
     "cohesion_units": "multiples of one particle's sliding friction force mu_k * m * g",
     "field": FIELD, "n_particles": NPARTS, "seeds": list(SEEDS), "cycles": 40,
     "per_cohesion": {}}
t0 = time.time()
for coh in COHS:
    entry = {"by_N": {}}
    for n in NS:
        per = []
        for sd in SEEDS:
            d = run(f"H-c{coh}-n{n}-s{sd}", mode="swarm", nBots=n, nParts=NPARTS,
                    measure=10, seed=sd, pattern="travelling", cohesion=coh, **FIELD)
            per.append({"seed": sd, "rg_start_m": d["cargo"]["rg_start_m"],
                        "rg_change_m": d["cargo"]["rg_change_m"],
                        "rg_change_pct_of_start": 100 * d["cargo"]["rg_change_m"] / d["cargo"]["rg_start_m"],
                        "particle_net_disp_m": d["cargo"]["net_disp_m"],
                        "diverged": d["numerics"]["diverged"]})
        v = [p["rg_change_pct_of_start"] for p in per]
        entry["by_N"][str(n)] = {"per_seed": per,
                                 "rg_change_pct_min_median_max": [min(v), statistics.median(v), max(v)],
                                 "aggregating_seeds": sum(1 for x in v if x < 0),
                                 "any_diverged": any(p["diverged"] for p in per)}
    # the control: constructs present but not actuating
    cper = []
    for sd in SEEDS:
        d = run(f"H-c{coh}-CTRL-s{sd}", mode="swarm", nBots=4, nParts=NPARTS, measure=10,
                seed=sd, pattern="travelling", cohesion=coh, amp=0, **FIELD)
        cper.append({"seed": sd, "rg_change_pct_of_start":
                     100 * d["cargo"]["rg_change_m"] / d["cargo"]["rg_start_m"],
                     "particle_net_disp_m": d["cargo"]["net_disp_m"]})
    cv = [p["rg_change_pct_of_start"] for p in cper]
    entry["control_amp0"] = {"per_seed": cper,
                             "rg_change_pct_min_median_max": [min(cv), statistics.median(cv), max(cv)],
                             "aggregating_seeds": sum(1 for x in cv if x < 0)}
    R["per_cohesion"][str(coh)] = entry
    ln = " | ".join(f"N={n}:{entry['by_N'][str(n)]['rg_change_pct_min_median_max'][1]:+.3f}%"
                    f"({entry['by_N'][str(n)]['aggregating_seeds']}/3)" for n in NS)
    print(f"  coh={coh:<5g} {ln} || amp0 ctrl {statistics.median(cv):+.3f}% "
          f"({entry['control_amp0']['aggregating_seeds']}/3)", flush=True)
# verdict
agg_actuated = {c: sum(R["per_cohesion"][c]["by_N"][str(n)]["aggregating_seeds"] for n in NS) for c in R["per_cohesion"]}
agg_control = {c: R["per_cohesion"][c]["control_amp0"]["aggregating_seeds"] for c in R["per_cohesion"]}
R["aggregating_runs_actuated_by_cohesion"] = agg_actuated
R["aggregating_runs_control_by_cohesion"] = agg_control
R["wall_s"] = round(time.time() - t0, 1)
json.dump(R, open("/data/scratch/designspaces/xenobot/data/cargo-arm3c.json", "w"), indent=2)
print("actuated aggregating runs by cohesion:", agg_actuated)
print("control  aggregating runs by cohesion:", agg_control)
print("wrote cargo-arm3c.json", R["wall_s"], "s")
