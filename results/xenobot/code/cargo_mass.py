#!/usr/bin/env python3
"""arm 2b: cargo mass sweep, contact-guaranteed (40 cycles).

The 5-cycle version of this arm was reach-limited: longitudinal and lateral
never arrived at the cargo, so every one of their rows read 0 and the sweep
measured nothing about them. 40 cycles gives every gait that moves at all time
to make contact. Declared in advance: the metric is cargo net displacement and
the efficiency M4 = W_friction/W_actuation; the question is whether the RANKING
of gaits changes with cargo mass, and where transport stalls.
"""
import json, os, subprocess, sys, time
BIN = "/data/scratch/designspaces/xenobot/build/cargo_actuation"
OUTD = "/data/scratch/designspaces/xenobot/data/cargo"
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]
DIR = {"travelling": -1, "longitudinal": -1, "lateral": -2}
RHOS = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0)


def run(tag, **kw):
    out = os.path.join(OUTD, tag)
    if not os.path.exists(out + ".json"):
        cmd = CAP + [BIN] + [f"--{k}={v}" for k, v in sorted(kw.items())] + [f"--out={out}"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        if p.returncode != 0:
            raise RuntimeError(f"{tag} rc={p.returncode} {p.stderr[-300:]}")
    return json.load(open(out + ".json"))


R = {"schema": "design-space-study/0.1", "id": "cargo-work-arm2b", "cycles": 40,
     "design": "cargo density scaled 0.25x to 32x at fixed volume (8 voxels), placed one clear lattice site away in each gait's OWN direction of travel, 40 cycles so contact is guaranteed",
     "per_gait": {}}
t0 = time.time()
for g, dv in DIR.items():
    R["per_gait"][g] = {}
    for rs in RHOS:
        d = run(f"M-{g}-rho{rs}", mode="cargo", cargoDir=dv, cargoGap=1, pattern=g,
                cargoRhoScale=rs, measure=10)
        e = d["energetics"]
        R["per_gait"][g][str(rs)] = {
            "cargo_mass_kg": d["cargo"]["mass_kg"],
            "M1_cargo_net_disp_m": d["cargo"]["net_disp_m"],
            "M3_W_cargo_friction_J": e["W_cargo_friction_J"],
            "M4_efficiency": e["efficiency_cargo_friction_over_actuation"],
            "W_actuation_J": e["W_actuation_J"],
            "construct_net_disp_m": d["construct"]["net_disp_m"],
            "diverged": d["numerics"]["diverged"]}
        v = R["per_gait"][g][str(rs)]
        print(f"  {g:13s} rho x{rs:<5g} m={v['cargo_mass_kg']*1000:6.2f} g "
              f"cargo={v['M1_cargo_net_disp_m']:.6f} eff={v['M4_efficiency']:.5f}", flush=True)
R["ranking_by_mass"] = {
    str(rs): sorted(DIR, key=lambda g: -R["per_gait"][g][str(rs)]["M1_cargo_net_disp_m"])
    for rs in RHOS}
R["ranking_is_constant_across_mass"] = len({tuple(v) for v in R["ranking_by_mass"].values()}) == 1
R["wall_s"] = round(time.time() - t0, 1)
with open("/data/scratch/designspaces/xenobot/data/cargo-arm2b.json", "w") as f:
    json.dump(R, f, indent=2)
print("ranking constant across mass:", R["ranking_is_constant_across_mass"])
print("wrote cargo-arm2b.json", R["wall_s"], "s")
