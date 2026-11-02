#!/usr/bin/env python3
"""arm 1b: separate REACH from PUSH.

The 5-cycle directed-push arm is reach-limited, not push-limited: with the cargo
one clear lattice site away the nearest surfaces are 7.5 mm apart, and in 5
cycles only the travelling gait covers that. Every other gait scores zero cargo
displacement because it never arrives. That is a real engineering fact and it is
reported, but it does not answer "which body plan pushes best".

This arm runs 40 cycles so every gait that moves at all makes contact, and then
gates the metrics on contact: the first measurement sample at which the cargo
COM has moved more than 1 um starts the window, and transport is measured from
there. Gaits that never make contact in 40 cycles are reported as such.
"""
import csv, json, os, subprocess, sys, time
BIN = "/data/scratch/designspaces/xenobot/build/cargo_actuation"
OUTD = "/data/scratch/designspaces/xenobot/data/cargo"
CAP = ["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=6G",
       "-p", "MemorySwapMax=0", "-p", "TasksMax=256", "nice", "-n", "19"]
GAITS = ("uniform", "longitudinal", "lateral", "dorsoventral", "travelling", "checker")
DIRS = {"-x": -1, "+x": 1, "-y": -2, "+y": 2}
CONTACT_M = 1e-6          # declared before running


def run(tag, **kw):
    out = os.path.join(OUTD, tag)
    if not os.path.exists(out + ".json"):
        cmd = CAP + [BIN] + [f"--{k}={v}" for k, v in sorted(kw.items())] + [f"--out={out}"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
        if p.returncode != 0:
            raise RuntimeError(f"{tag} rc={p.returncode} {p.stdout[-300:]} {p.stderr[-300:]}")
    return json.load(open(out + ".json")), out + "-com.csv"


def contact_metrics(csv_path):
    rows = [r for r in csv.DictReader(open(csv_path)) if r["phase"] == "measure"]
    if not rows:
        return None
    x0, y0 = float(rows[0]["part_x"]), float(rows[0]["part_y"])
    ic = None
    for i, r in enumerate(rows):
        d = ((float(r["part_x"]) - x0) ** 2 + (float(r["part_y"]) - y0) ** 2) ** 0.5
        if d > CONTACT_M:
            ic = i
            break
    if ic is None:
        return {"made_contact": False}
    seg = rows[ic:]
    bp = 0.0
    for a, b in zip(seg[:-1], seg[1:]):
        bp += ((float(b["bot_x"]) - float(a["bot_x"])) ** 2 +
               (float(b["bot_y"]) - float(a["bot_y"])) ** 2) ** 0.5
    cd = ((float(seg[-1]["part_x"]) - float(seg[0]["part_x"])) ** 2 +
          (float(seg[-1]["part_y"]) - float(seg[0]["part_y"])) ** 2) ** 0.5
    W0, W1 = float(seg[0]["W_act_J"]), float(seg[-1]["W_act_J"])
    Wf0, Wf1 = float(seg[0]["W_fric_J"]), float(seg[-1]["W_fric_J"])
    return {"made_contact": True, "contact_t_s": float(seg[0]["t_s"]),
            "contact_frac_of_run": ic / len(rows),
            "cargo_disp_after_contact_m": cd,
            "construct_path_after_contact_m": bp,
            "transport_ratio_after_contact": cd / bp if bp > 0 else 0.0,
            "W_actuation_after_contact_J": W1 - W0,
            "W_cargo_friction_after_contact_J": Wf1 - Wf0,
            "efficiency_after_contact": (Wf1 - Wf0) / (W1 - W0) if (W1 - W0) > 0 else 0.0}


def main():
    t0 = time.time()
    R = {"schema": "design-space-study/0.1", "id": "cargo-work-arm1b",
         "declared_contact_threshold_m": CONTACT_M,
         "declared_before_running": "contact window starts at the first measurement sample where the cargo COM has moved more than 1 um; transport ratio and efficiency are computed over that window only",
         "cycles": 40, "per_gait": {}}
    for g in GAITS:
        free, _ = run(f"B1-free-{g}", mode="cargo", cargoDir=0, pattern=g, measure=10)
        row = {"self_locomotion_40cyc": {
            "net_disp_m": free["construct"]["net_disp_m"],
            "body_lengths": free["construct"]["body_lengths"],
            "path_len_m": free["construct"]["path_len_m"],
            "W_actuation_J": free["energetics"]["W_actuation_J"]}, "by_direction": {}}
        for dn, dv in DIRS.items():
            d, cpath = run(f"B1-{g}-{dn.replace('+','p').replace('-','m')}",
                           mode="cargo", cargoDir=dv, cargoGap=1, pattern=g, measure=10)
            e = d["energetics"]
            m = contact_metrics(cpath)
            row["by_direction"][dn] = {
                "M1_cargo_net_disp_m": d["cargo"]["net_disp_m"],
                "M3_W_cargo_friction_J": e["W_cargo_friction_J"],
                "M4_efficiency_whole_run": e["efficiency_cargo_friction_over_actuation"],
                "W_actuation_J": e["W_actuation_J"],
                "construct_net_disp_m": d["construct"]["net_disp_m"],
                "diverged": d["numerics"]["diverged"], "contact": m}
        cand = {k: v for k, v in row["by_direction"].items() if v["contact"]["made_contact"]}
        if cand:
            best = max(cand, key=lambda k: cand[k]["M1_cargo_net_disp_m"])
            row["best_direction"] = best
            row["M1_best_m"] = cand[best]["M1_cargo_net_disp_m"]
            row["transport_ratio_after_contact"] = cand[best]["contact"]["transport_ratio_after_contact"]
            row["efficiency_after_contact"] = cand[best]["contact"]["efficiency_after_contact"]
            row["made_contact"] = True
        else:
            row.update({"best_direction": None, "M1_best_m": 0.0, "made_contact": False,
                        "transport_ratio_after_contact": None, "efficiency_after_contact": None})
        R["per_gait"][g] = row
        print(f"  {g:14s} self40={row['self_locomotion_40cyc']['net_disp_m']:.6f} m "
              f"contact={row['made_contact']} cargo={row['M1_best_m']:.6f} m "
              f"ratio={row['transport_ratio_after_contact']}", flush=True)
    moved = [g for g in GAITS if R["per_gait"][g]["made_contact"]]
    R["gaits_that_made_contact"] = moved
    R["ranking_self_locomotion"] = sorted(GAITS, key=lambda g: -R["per_gait"][g]["self_locomotion_40cyc"]["net_disp_m"])
    R["ranking_cargo_transport"] = sorted(GAITS, key=lambda g: -R["per_gait"][g]["M1_best_m"])
    R["ranking_transport_ratio_contacting_only"] = sorted(
        moved, key=lambda g: -R["per_gait"][g]["transport_ratio_after_contact"])
    R["ranking_efficiency_contacting_only"] = sorted(
        moved, key=lambda g: -R["per_gait"][g]["efficiency_after_contact"])
    R["wall_s"] = round(time.time() - t0, 1)
    with open("/data/scratch/designspaces/xenobot/data/cargo-arm1b.json", "w") as f:
        json.dump(R, f, indent=2)
    print("wrote cargo-arm1b.json", R["wall_s"], "s")


if __name__ == "__main__":
    main()
