"""R5b: staggered collective release (follow-up to R5): can a time-staggered release let lanes sit closer without
mid-air contact, and what do followers lose by flying through the leaders' wakes?

    python -m engineering.organ_sims.r5b_stagger [n_seeds] [workers]

Same 6-DOF PyBullet model, pelvic key, assumed dispersion scenarios and wake model as R5 (r5_school_launch.py);
only the release timing changes.  Grid: spacing 0.25/0.30/0.40 m x stagger 0/50/100/200 ms x pattern
sequential/alternate x dispersion low/high, wake on; plus wake-off twins at 100 ms to isolate the wake-following
effect.  8 fish per launch.  Simulated, not observed; the dispersion is assumed (no launch has been measured).
"""
import json, math, sys, time
import numpy as np
from engineering.organ_sims import common as C
from engineering.organ_sims import r5_school_launch as R5

RID = "r5b-staggered-release"
N = 8
SPACINGS = (0.25, 0.30, 0.40)
STAGGERS = (0.0, 0.05, 0.10, 0.20)
PATTERNS = ("sequential", "alternate")
DEC = 4.0
import os
if os.environ.get("R5B_SMOKE"):                 # pipeline smoke test only: never used for a reported result
    SPACINGS, STAGGERS = (0.30,), (0.0, 0.10)


def _run(args):
    spacing, stagger, pattern, disp, wake, seed = args
    o, col, _ = R5.simulate(R5.build_model(decalage=DEC), N, spacing, disp, seed, wake_on=wake, stagger_s=stagger, pattern=pattern)
    return o, col


def main():
    nseed = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    seeds = [1000 + s for s in range(nseed)]
    jobs = []
    for disp in ("low", "high"):
        for spacing in SPACINGS:
            for stagger in STAGGERS:
                for pattern in (PATTERNS if stagger > 0 else ("sequential",)):
                    for seed in seeds:
                        jobs.append((spacing, stagger, pattern, disp, True, seed))
            for pattern in PATTERNS:
                for seed in seeds:
                    jobs.append((spacing, 0.10, pattern, disp, False, seed))
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_run, jobs, chunksize=2))
    rows = []
    for (spacing, stagger, pattern, disp, wake, seed), (o, col) in zip(jobs, res):
        order = list(range(N)) if pattern == "sequential" else list(range(0, N, 2)) + list(range(1, N, 2))
        rows.append({"spacing_m": spacing, "stagger_s": stagger, "pattern": pattern, "disp": disp, "wake": wake, "seed": seed,
                     "n_collision_pairs": len(col), "pairs": col, "n_fish_collided": sum(x["collided"] for x in o),
                     "ranges_m": [x["range_m"] for x in o], "release_slot": [order.index(i) for i in range(N)],
                     "lane_dev_m": [None if x["y_land_m"] is None else x["y_land_m"] - x["y0_m"] for x in o],
                     "max_roll_deg": max(x["max_roll_deg"] for x in o), "n_timeout": sum(x["end"] == "timeout" for x in o)})
    checks = []
    # control: stagger 0 reproduces R5's simultaneous wake-on rows exactly for the shared seeds and spacings
    r5 = json.loads((C.ROOT / "artifacts/organ-sims/r5-school-launch/manifest.json").read_text())["results"]["rows"]
    matched, mism = 0, []
    for r in rows:
        if r["stagger_s"] == 0 and r["wake"]:
            ref = [x for x in r5 if x["wake"] and x["disp"] == r["disp"] and x["spacing_m"] == r["spacing_m"] and x["seed"] == r["seed"]]
            if ref:
                matched += 1
                rm = float(np.mean([v for v in r["ranges_m"] if v is not None]))
                if ref[0]["n_collision_pairs"] != r["n_collision_pairs"] or abs(ref[0]["range_mean_m"] - rm) > 1e-9:
                    mism.append((r["disp"], r["spacing_m"], r["seed"]))
    checks.append({"name": "control: stagger 0 reproduces R5 simultaneous rows exactly (collision pairs, mean range 1e-9)", "pass": matched > 0 and not mism,
                   "detail": {"matched": matched, "mismatched": mism}})
    checks.append({"name": "every launch finished (no timeouts, all ranges finite)", "pass": all(r["n_timeout"] == 0 and all(v is not None and math.isfinite(v) for v in r["ranges_m"]) for r in rows), "detail": len(rows)})
    summ = {}
    for disp in ("low", "high"):
        for spacing in SPACINGS:
            for stagger in STAGGERS:
                for pattern in (PATTERNS if stagger > 0 else ("sequential",)):
                    rs = [r for r in rows if r["disp"] == disp and r["spacing_m"] == spacing and r["stagger_s"] == stagger and r["pattern"] == pattern and r["wake"]]
                    first = [r["ranges_m"][r["release_slot"].index(0)] for r in rs]
                    later = [v for r in rs for v, sl in zip(r["ranges_m"], r["release_slot"]) if sl > 0]
                    summ[f"{disp}/{spacing:g}/{int(stagger * 1000)}ms/{pattern}"] = {
                        "launches": len(rs), "frac_launches_with_collision": float(np.mean([r["n_collision_pairs"] > 0 for r in rs])),
                        "mean_fish_collided": float(np.mean([r["n_fish_collided"] for r in rs])),
                        "range_mean_m": float(np.mean([v for r in rs for v in r["ranges_m"]])),
                        "range_first_released_mean_m": float(np.mean(first)), "range_later_released_mean_m": float(np.mean(later))}
    # wake-following effect at 100 ms: paired wake-on minus wake-off per fish (same seeds -> same release draws)
    wf = {}
    for disp in ("low", "high"):
        for spacing in SPACINGS:
            for pattern in PATTERNS:
                on = {r["seed"]: r for r in rows if r["wake"] and r["disp"] == disp and r["spacing_m"] == spacing and r["stagger_s"] == 0.10 and r["pattern"] == pattern}
                off = {r["seed"]: r for r in rows if not r["wake"] and r["disp"] == disp and r["spacing_m"] == spacing and r["stagger_s"] == 0.10 and r["pattern"] == pattern}
                d = [a - b for s in on for a, b in zip(on[s]["ranges_m"], off[s]["ranges_m"])]
                wf[f"{disp}/{spacing:g}/{pattern}"] = {"mean_range_change_m": float(np.mean(d)), "p10_m": float(np.percentile(d, 10)), "p90_m": float(np.percentile(d, 90)),
                                                       "collision_frac_on": float(np.mean([r["n_collision_pairs"] > 0 for r in on.values()])),
                                                       "collision_frac_off": float(np.mean([r["n_collision_pairs"] > 0 for r in off.values()]))}
    figs = fig(summ)
    C.manifest(RID, "Staggered collective release of printed gliders (PyBullet 6-DOF, wake coupling, contacts)",
               ["artifacts/glider/r4-daane-printfix/flight_model.json", "artifacts/glider/r4-daane-printfix/manifest.json",
                "artifacts/organ-sims/r3-underwater-drag/manifest.json", "artifacts/organ-sims/r5-school-launch/manifest.json"],
               {"summary": summ, "wake_following_100ms": wf, "rows": rows, "seeds": seeds, "n_launches": len(rows), "pelvic_key_decalage_deg": DEC,
                "dispersion_scenarios": R5.DISP, "wall_s": time.time() - t0, "workers": workers},
               checks, {"see": "docs/organ-sims.md"}, seed=seeds, figures=figs)
    print(json.dumps({"summary": summ, "wake": wf}, indent=1))
    C.enforce(checks)


def fig(summ):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
    for a, disp in zip(ax, ("low", "high")):
        for i, spacing in enumerate(SPACINGS):
            for pattern, ls in (("sequential", "-"), ("alternate", "--")):
                y = [summ[f"{disp}/{spacing:g}/{int(s * 1000)}ms/{pattern if s > 0 else 'sequential'}"]["frac_launches_with_collision"] for s in STAGGERS]
                a.plot([s * 1000 for s in STAGGERS], y, "o" + ls, color=f"C{i}", label=f"{spacing:g} m, {pattern}")
        a.set_xlabel("release offset between consecutive fish, ms"); a.set_title(f"dispersion {disp} (simulated, assumed)")
    ax[0].set_ylabel("fraction of 8-fish launches with a mid-air contact"); ax[0].legend(fontsize=7)
    fig.tight_layout(); fp = C.OUT / RID / "stagger.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/stagger.png"]


if __name__ == "__main__":
    main()
