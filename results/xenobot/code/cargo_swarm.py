#!/usr/bin/env python3
"""arm 3 (rerun): swarm aggregation vs swarm size, on a FIXED rectangular field.

The first version of this arm auto-spread the constructs over a square field and
silently pushed the outermost constructs OUTSIDE it at N=6 and N=8, so those two
sizes returned bit-identical particle outcomes. The driver now refuses that
geometry outright (exit 4) and the field is a fixed rectangle covering the swept
region, so swarm size N is the only thing that varies.

DECLARED BEFORE THIS RERUN:
  S1 PRIMARY  mean particle net COM displacement vs N
  S2          change in particle radius of gyration; NEGATIVE means aggregation
  S3          min / median / max over 5 seeds
  S4          work done against floor friction on the particle field, per unit
              actuation work, vs N -- does a bigger swarm pay off per unit energy?
"""
import json, os, subprocess, statistics, sys, time
BIN = "/data/scratch/designspaces/xenobot/build/cargo_actuation"
OUTD = "/data/scratch/designspaces/xenobot/data/cargo"
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]
FIELD = dict(fieldXlo=-16, fieldXhi=2, fieldYlo=-22, fieldYhi=22)
NPARTS, SEEDS, NS = 120, (1, 2, 3, 4, 5), (1, 2, 3, 4, 6, 8)


def run(tag, **kw):
    out = os.path.join(OUTD, tag)
    if not os.path.exists(out + ".json"):
        cmd = CAP + [BIN] + [f"--{k}={v}" for k, v in sorted(kw.items())] + [f"--out={out}"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        if p.returncode != 0:
            raise RuntimeError(f"{tag} rc={p.returncode} {p.stdout[-300:]} {p.stderr[-400:]}")
    return json.load(open(out + ".json"))


def main():
    t0 = time.time()
    R = {"schema": "design-space-study/0.1", "id": "cargo-work-arm3-rerun",
         "field": FIELD, "n_particles": NPARTS, "cycles": 40, "seeds": list(SEEDS),
         "declared_metrics": {
             "S1_primary": "mean particle net COM displacement, m",
             "S2": "change in particle radius of gyration, m; NEGATIVE = aggregation",
             "S3": "min/median/max over 5 seeds",
             "S4": "work against floor friction on the field per unit actuation work"},
         "per_N": {}}
    ctrl = run("S-C0-amp0", mode="swarm", nBots=4, nParts=NPARTS, measure=10,
               seed=1, pattern="travelling", amp=0, **FIELD)
    R["control_zero_amplitude"] = {
        "particle_net_disp_m": ctrl["cargo"]["net_disp_m"],
        "rg_change_m": ctrl["cargo"]["rg_change_m"],
        "gate": "particles must not move with the actuation off",
        "met": ctrl["cargo"]["net_disp_m"] <= 1e-6}
    print("control amp=0 met:", R["control_zero_amplitude"]["met"], flush=True)
    for n in NS:
        per = []
        for sd in SEEDS:
            d = run(f"S-n{n}-s{sd}", mode="swarm", nBots=n, nParts=NPARTS, measure=10,
                    seed=sd, pattern="travelling", **FIELD)
            per.append({"seed": sd, "n_particles": d["cargo"]["n_voxels"],
                        "S1_particle_net_disp_m": d["cargo"]["net_disp_m"],
                        "particle_path_len_m": d["cargo"]["path_len_m"],
                        "S2_rg_change_m": d["cargo"]["rg_change_m"],
                        "rg_start_m": d["cargo"]["rg_start_m"],
                        "rg_end_m": d["cargo"]["rg_end_m"],
                        "W_actuation_J": d["energetics"]["W_actuation_J"],
                        "W_particles_friction_J": d["energetics"]["W_cargo_friction_J"],
                        "construct_net_disp_m": d["construct"]["net_disp_m"],
                        "diverged": d["numerics"]["diverged"]})
        f = lambda k: [p[k] for p in per]
        R["per_N"][str(n)] = {
            "per_seed": per,
            "S1_min_median_max": [min(f("S1_particle_net_disp_m")),
                                  statistics.median(f("S1_particle_net_disp_m")),
                                  max(f("S1_particle_net_disp_m"))],
            "S2_min_median_max": [min(f("S2_rg_change_m")), statistics.median(f("S2_rg_change_m")),
                                  max(f("S2_rg_change_m"))],
            "path_min_median_max": [min(f("particle_path_len_m")),
                                    statistics.median(f("particle_path_len_m")),
                                    max(f("particle_path_len_m"))],
            "W_fric_median": statistics.median(f("W_particles_friction_J")),
            "W_act_median": statistics.median(f("W_actuation_J")),
            "S4_fric_per_actuation_median": statistics.median(
                [p["W_particles_friction_J"] / p["W_actuation_J"] for p in per]),
            "any_seed_aggregated": any(x < 0 for x in f("S2_rg_change_m")),
            "all_seeds_dispersed": all(x > 0 for x in f("S2_rg_change_m")),
            "any_diverged": any(p["diverged"] for p in per)}
        v = R["per_N"][str(n)]
        print(f"  N={n}  S1med={v['S1_min_median_max'][1]:.6f}  S2med={v['S2_min_median_max'][1]:+.6f}  "
              f"S4={v['S4_fric_per_actuation_median']:.5f}  aggregated={v['any_seed_aggregated']}", flush=True)
    R["aggregation_observed_anywhere"] = any(R["per_N"][str(n)]["any_seed_aggregated"] for n in NS)
    R["wall_s"] = round(time.time() - t0, 1)
    with open("/data/scratch/designspaces/xenobot/data/cargo-arm3.json", "w") as fh:
        json.dump(R, fh, indent=2)
    print("wrote cargo-arm3.json", R["wall_s"], "s")


if __name__ == "__main__":
    main()
