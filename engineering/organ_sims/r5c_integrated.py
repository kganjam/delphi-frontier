"""R5c: integrated collective launch of the R6-recommended designs with the R5b release rule.

    python -m engineering.organ_sims.r5c_integrated [n_seeds] [workers]

Designs (taken from the committed R6 manifest, not retyped): baseline r4 at dec+4; R6's best feasible with an existing
printed key; R6's best feasible with any key (a new print).  Release: 100 ms alternating stagger at 0.25 and 0.30 m
lanes (R5b's rule) and simultaneous at 0.60 m (R5's rule), dispersion low/high, wake on, 8 fish.
Question: does the R6 design gain survive a collective launch (wakes, contacts), and does the release rule still hold
for the larger, differently trimmed fins?  Simulated, not observed; dispersion assumed.
"""
import json, math, sys, time
import numpy as np
from engineering.organ_sims import common as C
from engineering.organ_sims import r5_school_launch as R5

RID = "r5c-integrated-launch"
N = 8
RELEASES = ((0.25, 0.10, "alternate"), (0.30, 0.10, "alternate"), (0.60, 0.0, "sequential"))
import os
if os.environ.get("R5C_SMOKE"):
    RELEASES = ((0.25, 0.10, "alternate"), (0.60, 0.0, "sequential"))


def designs():
    r6 = json.loads((C.ROOT / "artifacts/organ-sims/r6-trim-map/manifest.json").read_text())["results"]["summary"]["V8"]
    out = {"baseline_dec4": {"pec": (1.0, 1.0, 0.0), "key": 4.0, "cg_shift": 0.0}}
    for name, k in (("r6_best_printed_key", "best_6dof_printed_key_feasible"), ("r6_best_new_key", "best_6dof_any_key_feasible")):
        c = r6[k]
        out[name] = {"pec": (c["ka"], c["kar"], c["dx_m"]), "key": c["key_deg"], "cg_shift": c["cg_shift_m"], "r6_V8": c["V8"]}
    return out


def _run(args):
    dname, d, spacing, stagger, pattern, disp, seed = args
    m = R5.build_model(cg_shift=d["cg_shift"], decalage=d["key"], pec=tuple(d["pec"]))
    o, col, _ = R5.simulate(m, N, spacing, disp, seed, wake_on=True, stagger_s=stagger, pattern=pattern)
    return o, col


def main():
    nseed = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    D = designs()
    seeds = [3000 + s for s in range(nseed)]
    jobs = [(dn, d, sp, st, pa, disp, sd) for dn, d in D.items() for (sp, st, pa) in RELEASES for disp in ("low", "high") for sd in seeds]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_run, jobs, chunksize=2))
    rows = []
    for (dn, d, sp, st, pa, disp, sd), (o, col) in zip(jobs, res):
        rows.append({"design": dn, "spacing_m": sp, "stagger_s": st, "pattern": pa, "disp": disp, "seed": sd, "n_collision_pairs": len(col),
                     "n_fish_collided": sum(x["collided"] for x in o), "ranges_m": [x["range_m"] for x in o],
                     "max_roll_deg": max(x["max_roll_deg"] for x in o), "n_timeout": sum(x["end"] == "timeout" for x in o)})
    summ = {}
    for dn in D:
        for (sp, st, pa) in RELEASES:
            for disp in ("low", "high"):
                rs = [r for r in rows if r["design"] == dn and r["spacing_m"] == sp and r["disp"] == disp]
                allr = [v for r in rs for v in r["ranges_m"]]
                summ[f"{dn}/{sp:g}m/{int(st * 1000)}ms/{disp}"] = {"launches": len(rs), "frac_launches_with_collision": float(np.mean([r["n_collision_pairs"] > 0 for r in rs])),
                                                                  "range_mean_m": float(np.mean(allr)), "range_p10_m": float(np.percentile(allr, 10)), "range_sd_m": float(np.std(allr))}
    checks = []
    checks.append({"name": "every launch finished (no timeouts, finite ranges)", "pass": all(r["n_timeout"] == 0 and all(v is not None and math.isfinite(v) for v in r["ranges_m"]) for r in rows), "detail": len(rows)})
    # cross-check: school-launch mean range of each design within 15% of its R6 single-fish dispersed mean (V0 8, low)
    xc = {}
    for dn, d in D.items():
        if "r6_V8" in d:
            k = f"{dn}/0.6m/0ms/low"
            xc[dn] = [summ[k]["range_mean_m"], d["r6_V8"]["mean_range_m"]]
    checks.append({"name": "cross-check: wide simultaneous school mean range within 15% of R6 single-fish dispersed mean (low)", "pass": all(abs(a / b - 1) <= 0.15 for a, b in xc.values()), "detail": xc})
    figs = fig(summ, D)
    C.manifest(RID, "Integrated collective launch: R6-recommended designs with the R5b staggered release (PyBullet 6-DOF)",
               ["artifacts/organ-sims/r6-trim-map/manifest.json", "artifacts/organ-sims/r5b-staggered-release/manifest.json",
                "artifacts/glider/r4-daane-printfix/flight_model.json", "artifacts/glider/r4-daane-printfix/manifest.json"],
               {"designs": D, "summary": summ, "rows": rows, "seeds": seeds, "n_launches": len(rows), "wall_s": time.time() - t0, "workers": workers},
               checks, {"see": "docs/organ-sims.md"}, seed=seeds, figures=figs)
    print(json.dumps(summ, indent=1))
    C.enforce(checks)


def fig(summ, D):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
    labels = [f"{sp:g} m, {int(st * 1000)} ms" for sp, st, _ in RELEASES]
    for i, dn in enumerate(D):
        for a, disp in zip(ax, ("low", "high")):
            y = [summ[f"{dn}/{sp:g}m/{int(st * 1000)}ms/{disp}"]["range_mean_m"] for sp, st, _ in RELEASES]
            p = [summ[f"{dn}/{sp:g}m/{int(st * 1000)}ms/{disp}"]["range_p10_m"] for sp, st, _ in RELEASES]
            x = np.arange(len(RELEASES)) + 0.25 * (i - 1)
            a.bar(x, y, 0.25, color=f"C{i}", label=dn); a.plot(x, p, "k_", ms=12)
            a.set_xticks(np.arange(len(RELEASES))); a.set_xticklabels(labels); a.set_title(f"dispersion {disp} (bars mean, ticks P10; simulated)")
    ax[0].set_ylabel("range, m"); ax[0].legend(fontsize=7)
    fig.tight_layout(); fp = C.OUT / RID / "integrated.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/integrated.png"]


if __name__ == "__main__":
    main()
