#!/usr/bin/env python3
"""cargo-work: does the construct do useful mechanical work on an EXTERNAL object,
and is the body plan that moves itself best also the one that pushes best?

METRICS DECLARED BEFORE THE SWEEP WAS RUN (one pilot run of the travelling
pattern was executed first, as a plumbing check, and its cargo displacement was
seen before these were written down; every other number below was produced
after):
  M1 PRIMARY  cargo net COM displacement, metres
  M2          cargo net displacement per actuation cycle
  M3          useful work against floor friction, closed form mu_k * m * g * path
  M4          efficiency = M3 / W_actuation
  M5          transport ratio = cargo net displacement / construct path length
PRIMARY QUESTION: is argmax_gait(M1) the same gait as argmax_gait(self-locomotion)?
PREDECLARED EXPECTATION, to be tested and not assumed: they are NOT the same.

SWARM ARM, declared in advance:
  S1 PRIMARY  mean particle net displacement vs swarm size N
  S2          change in particle radius of gyration (NEGATIVE = aggregation)
  S3          spread across 5 random seeds, reported as min/median/max
Every stochastic element is OUR seeded RNG in cargo_actuation.cpp; Voxelyze has
no RNG and contributes no variance.
"""
import json, os, subprocess, sys, time, statistics
BIN = "/data/scratch/designspaces/xenobot/build/cargo_actuation"
OUTD = "/data/scratch/designspaces/xenobot/data/cargo"
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]
GAITS = ("uniform", "longitudinal", "lateral", "dorsoventral", "travelling", "checker")
DIRS = {"-x": -1, "+x": 1, "-y": -2, "+y": 2}


def run(tag, **kw):
    out = os.path.join(OUTD, tag)
    if os.path.exists(out + ".json"):
        return json.load(open(out + ".json"))
    cmd = CAP + [BIN] + [f"--{k}={v}" for k, v in sorted(kw.items())] + [f"--out={out}"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
    if p.returncode != 0:
        raise RuntimeError(f"{tag} rc={p.returncode} {p.stdout[-300:]} {p.stderr[-300:]}")
    return json.load(open(out + ".json"))


def main():
    t0 = time.time()
    R = {"schema": "design-space-study/0.1", "id": "cargo-work"}
    R["declared_metrics"] = {
        "M1_primary": "cargo net COM displacement, m",
        "M2": "cargo net displacement per actuation cycle, m",
        "M3": "useful work against floor friction, mu_k*m*g*path (closed form, LOWER BOUND)",
        "M4": "efficiency = M3 / W_actuation",
        "M5": "transport ratio = cargo net displacement / construct path length",
        "S1_primary_swarm": "mean particle net displacement vs swarm size N",
        "S2": "change in particle radius of gyration (negative = aggregation)",
        "S3": "spread over 5 seeds (min/median/max)"}

    # ------------------------------------------------------------ controls --
    ctrl = {}
    d = run("X-C1-regression", mode="cargo", cargoDir=0, pattern="travelling")
    ctrl["C1_no_cargo_reproduces_pinned_artifact"] = {
        "net_disp_m": d["construct"]["net_disp_m"],
        "published_artifact_m": 0.014577281,
        "rel_diff": abs(d["construct"]["net_disp_m"] - 0.014577281) / 0.014577281,
        "gate": "<= 1e-6", "met": abs(d["construct"]["net_disp_m"] - 0.014577281) / 0.014577281 <= 1e-6}
    d = run("X-C2-far", mode="cargo", cargoDir=-1, cargoGap=8, pattern="travelling")
    ctrl["C2_cargo_out_of_reach_must_not_move"] = {
        "cargo_net_disp_m": d["cargo"]["net_disp_m"],
        "construct_net_disp_m": d["construct"]["net_disp_m"],
        "gate": "cargo <= 1e-9 m while the construct still moves", 
        "met": d["cargo"]["net_disp_m"] <= 1e-9 and d["construct"]["net_disp_m"] > 1e-3}
    for tag, kw in (("X-C3-amp0", {"amp": 0}), ("X-C4-cte0", {"cte": 0})):
        d = run(tag, mode="cargo", cargoDir=-1, cargoGap=1, pattern="travelling", **kw)
        ctrl[tag] = {"W_actuation_J": d["energetics"]["W_actuation_J"],
                     "cargo_net_disp_m": d["cargo"]["net_disp_m"],
                     "construct_net_disp_m": d["construct"]["net_disp_m"],
                     "gate": "W_actuation exactly 0 and cargo <= 1e-9 m",
                     "met": d["energetics"]["W_actuation_J"] == 0.0 and d["cargo"]["net_disp_m"] <= 1e-9}
    d = run("X-C5-swarm-amp0", mode="swarm", nBots=4, nParts=40, fieldR=0.10,
            measure=10, seed=1, pattern="travelling", amp=0)
    ctrl["C5_swarm_zero_amplitude_particles_must_not_move"] = {
        "particle_net_disp_m": d["cargo"]["net_disp_m"], "gate": "<= 1e-6 m",
        "met": d["cargo"]["net_disp_m"] <= 1e-6}
    R["controls"] = ctrl
    R["all_controls_met"] = all(v.get("met") for v in ctrl.values())
    print("controls met:", R["all_controls_met"], flush=True)

    # ------------------------------------------------- arm 1: directed push --
    arm1 = {}
    for g in GAITS:
        free = run(f"A1-free-{g}", mode="cargo", cargoDir=0, pattern=g)
        row = {"self_locomotion": {
            "net_disp_m": free["construct"]["net_disp_m"],
            "body_lengths": free["construct"]["body_lengths"],
            "net_dx_m": free["construct"]["net_dx_m"],
            "net_dy_m": free["construct"]["net_dy_m"],
            "path_len_m": free["construct"]["path_len_m"],
            "W_actuation_J": free["energetics"]["W_actuation_J"]}, "by_direction": {}}
        for dn, dv in DIRS.items():
            d = run(f"A1-{g}-{dn.replace('+','p').replace('-','m')}",
                    mode="cargo", cargoDir=dv, cargoGap=1, pattern=g)
            e = d["energetics"]
            row["by_direction"][dn] = {
                "M1_cargo_net_disp_m": d["cargo"]["net_disp_m"],
                "M2_cargo_disp_per_cycle_m": e["cargo_disp_per_cycle_m"],
                "M3_W_cargo_friction_J": e["W_cargo_friction_J"],
                "M4_efficiency": e["efficiency_cargo_friction_over_actuation"],
                "M5_transport_ratio": e["transport_ratio_cargo_disp_over_bot_path"],
                "W_actuation_J": e["W_actuation_J"],
                "construct_net_disp_m": d["construct"]["net_disp_m"],
                "diverged": d["numerics"]["diverged"]}
        best = max(row["by_direction"], key=lambda k: row["by_direction"][k]["M1_cargo_net_disp_m"])
        row["best_direction"] = best
        row["M1_best"] = row["by_direction"][best]["M1_cargo_net_disp_m"]
        row["M4_best_direction"] = row["by_direction"][best]["M4_efficiency"]
        arm1[g] = row
        print(f"  arm1 {g:14s} self={row['self_locomotion']['net_disp_m']:.6f} m "
              f"cargo_best={row['M1_best']:.6f} m ({best})", flush=True)
    R["arm1_directed_push"] = {
        "design": "cargo block of 2x2x2 passive voxels placed one clear lattice site away, in each of four directions; the best direction is reported per gait because different gaits travel along different axes",
        "per_gait": arm1,
        "ranking_self_locomotion": sorted(GAITS, key=lambda g: -arm1[g]["self_locomotion"]["net_disp_m"]),
        "ranking_cargo_transport": sorted(GAITS, key=lambda g: -arm1[g]["M1_best"]),
        "ranking_efficiency": sorted(GAITS, key=lambda g: -arm1[g]["M4_best_direction"])}

    # ------------------------------------------------- arm 2: cargo mass ----
    arm2 = {}
    for g in ("travelling", "longitudinal", "lateral"):
        arm2[g] = {}
        for rs in (0.25, 0.5, 1.0, 2.0, 4.0):
            d = run(f"A2-{g}-rho{rs}", mode="cargo", cargoDir=-1, cargoGap=1,
                    pattern=g, cargoRhoScale=rs)
            arm2[g][str(rs)] = {
                "cargo_mass_kg": d["cargo"]["mass_kg"],
                "M1_cargo_net_disp_m": d["cargo"]["net_disp_m"],
                "M3_W_cargo_friction_J": d["energetics"]["W_cargo_friction_J"],
                "M4_efficiency": d["energetics"]["efficiency_cargo_friction_over_actuation"]}
        print(f"  arm2 {g} done", flush=True)
    R["arm2_cargo_mass"] = {
        "design": "cargo density scaled 0.25x to 4x at fixed volume, cargo placed at -x (the travel direction of travelling and longitudinal). NOTE lateral travels along y, so its -x row is an off-axis push and is reported as such.",
        "per_gait": arm2}

    # ------------------------------------------------------ arm 3: swarm ----
    arm3 = {}
    for n in (1, 2, 3, 4, 6, 8):
        per_seed = []
        for sd in (1, 2, 3, 4, 5):
            d = run(f"A3-n{n}-s{sd}", mode="swarm", nBots=n, nParts=40, fieldR=0.10,
                    measure=10, seed=sd, pattern="travelling")
            per_seed.append({
                "seed": sd, "n_particles": d["cargo"]["n_voxels"],
                "S1_particle_net_disp_m": d["cargo"]["net_disp_m"],
                "particle_path_len_m": d["cargo"]["path_len_m"],
                "S2_rg_change_m": d["cargo"]["rg_change_m"],
                "rg_start_m": d["cargo"]["rg_start_m"], "rg_end_m": d["cargo"]["rg_end_m"],
                "W_actuation_J": d["energetics"]["W_actuation_J"],
                "W_particles_friction_J": d["energetics"]["W_cargo_friction_J"],
                "construct_net_disp_m": d["construct"]["net_disp_m"],
                "diverged": d["numerics"]["diverged"]})
        v1 = [p["S1_particle_net_disp_m"] for p in per_seed]
        v2 = [p["S2_rg_change_m"] for p in per_seed]
        vw = [p["W_particles_friction_J"] for p in per_seed]
        va = [p["W_actuation_J"] for p in per_seed]
        arm3[str(n)] = {
            "per_seed": per_seed,
            "S1_min_median_max": [min(v1), statistics.median(v1), max(v1)],
            "S2_min_median_max": [min(v2), statistics.median(v2), max(v2)],
            "W_particles_friction_min_median_max": [min(vw), statistics.median(vw), max(vw)],
            "W_actuation_median": statistics.median(va),
            "S3_aggregation_observed_in_any_seed": any(x < 0 for x in v2),
            "friction_work_per_unit_actuation_median": statistics.median(
                [p["W_particles_friction_J"] / p["W_actuation_J"] for p in per_seed])}
        print(f"  arm3 N={n} S1med={statistics.median(v1):.6f} S2med={statistics.median(v2):+.6f} "
              f"aggregated={arm3[str(n)]['S3_aggregation_observed_in_any_seed']}", flush=True)
    R["arm3_swarm"] = {
        "design": "N constructs evenly spread along y inside a 0.10 m particle field of 40 single-voxel passive particles, 40 actuation cycles (10 s), 5 seeds. Every construct runs the SAME gait (travelling), which is the condition the published self-replication work operates under; no construct has any sensing or any differentiated role.",
        "per_N": arm3}

    R["wall_s"] = round(time.time() - t0, 1)
    return R


if __name__ == "__main__":
    r = main()
    with open("/data/scratch/designspaces/xenobot/cargo-work.raw.json", "w") as f:
        json.dump(r, f, indent=2)
    print("wrote cargo-work.raw.json", r["wall_s"], "s")
