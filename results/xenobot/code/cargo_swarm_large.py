#!/usr/bin/env python3
"""Follow-up arm, declared after seeing the N=8 result and labelled as post-hoc.

The main swarm arm found the particle field DISPERSING at every N from 1 to 6 in
all 5 seeds, then at N=8 the median dispersion fell 2.6-fold and 2 of 5 seeds
turned negative. That is either the onset of aggregation at larger swarm size or
seed scatter at the edge of the sweep. N > 9 does not fit the original field at
the minimum construct stride, so this arm widens the field in y and scales the
particle count to hold DENSITY fixed, then pushes N to 16.

PREDECLARED for this arm: if it is an onset, the median rg change should keep
falling with N and cross zero. If it is scatter, the median should stay positive
and the spread should simply be wide at every large N.
"""
import json, os, subprocess, statistics, time
BIN = "/data/scratch/designspaces/xenobot/build/cargo_actuation"
OUTD = "/data/scratch/designspaces/xenobot/data/cargo"
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]
# original field: x -16..2 (19), y -22..22 (45) -> 855 sites, 120 particles
# widened:        x -16..2 (19), y -42..42 (85) -> 1615 sites, density-matched:
FIELD = dict(fieldXlo=-16, fieldXhi=2, fieldYlo=-42, fieldYhi=42)
NPARTS = round(120 * (19 * 85) / (19 * 45))
NS, SEEDS = (4, 8, 12, 16), (1, 2, 3, 4, 5)


def run(tag, **kw):
    out = os.path.join(OUTD, tag)
    if not os.path.exists(out + ".json"):
        cmd = CAP + [BIN] + [f"--{k}={v}" for k, v in sorted(kw.items())] + [f"--out={out}"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        if p.returncode != 0:
            raise RuntimeError(f"{tag} rc={p.returncode} {p.stderr[-400:]}")
    return json.load(open(out + ".json"))


R = {"schema": "design-space-study/0.1", "id": "cargo-work-arm3b-onset",
     "status": "POST-HOC. Declared after seeing the N=8 result in the main arm, and reported as a diagnosis rather than as confirmatory evidence.",
     "field": FIELD, "n_particles": NPARTS,
     "density_matched_to_main_arm": "120 particles over 19x45 sites, scaled to the same density over 19x85",
     "predeclared_for_this_arm": "an onset predicts the median rg change keeps falling with N and crosses zero; seed scatter predicts the median stays positive with a wide spread",
     "per_N": {}}
t0 = time.time()
for n in NS:
    per = []
    for sd in SEEDS:
        d = run(f"L-n{n}-s{sd}", mode="swarm", nBots=n, nParts=NPARTS, measure=10,
                seed=sd, pattern="travelling", **FIELD)
        per.append({"seed": sd, "n_particles": d["cargo"]["n_voxels"],
                    "S1_particle_net_disp_m": d["cargo"]["net_disp_m"],
                    "S2_rg_change_m": d["cargo"]["rg_change_m"],
                    "rg_start_m": d["cargo"]["rg_start_m"], "rg_end_m": d["cargo"]["rg_end_m"],
                    "W_actuation_J": d["energetics"]["W_actuation_J"],
                    "W_particles_friction_J": d["energetics"]["W_cargo_friction_J"],
                    "diverged": d["numerics"]["diverged"]})
    v2 = [p["S2_rg_change_m"] for p in per]
    v1 = [p["S1_particle_net_disp_m"] for p in per]
    R["per_N"][str(n)] = {"per_seed": per,
                          "S1_min_median_max": [min(v1), statistics.median(v1), max(v1)],
                          "S2_min_median_max": [min(v2), statistics.median(v2), max(v2)],
                          "n_seeds_aggregating": sum(1 for x in v2 if x < 0),
                          "any_diverged": any(p["diverged"] for p in per)}
    v = R["per_N"][str(n)]
    print(f"  N={n:2d}  S1med={v['S1_min_median_max'][1]*1000:7.3f} mm  "
          f"S2med={v['S2_min_median_max'][1]*1000:+7.3f} mm  "
          f"aggregating seeds {v['n_seeds_aggregating']}/5", flush=True)
meds = [R["per_N"][str(n)]["S2_min_median_max"][1] for n in NS]
R["median_rg_change_falls_with_N"] = all(meds[i + 1] < meds[i] for i in range(len(meds) - 1))
R["median_crosses_zero"] = any(m < 0 for m in meds)
R["verdict"] = ("ONSET" if R["median_crosses_zero"] else
                ("FALLING but median still positive at N=16" if R["median_rg_change_falls_with_N"]
                 else "NOT a monotone onset; consistent with seed scatter"))
R["wall_s"] = round(time.time() - t0, 1)
json.dump(R, open("/data/scratch/designspaces/xenobot/data/cargo-arm3b.json", "w"), indent=2)
print("verdict:", R["verdict"], "| wrote cargo-arm3b.json", R["wall_s"], "s")
