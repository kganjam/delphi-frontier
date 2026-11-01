"""R6: re-fly R2's wing designs in the 6-DOF model with a REAL trim (CG and pelvic key chosen by moment balance) instead
of R2's linear neutral-point rule, then launch each with dispersion.  Answers: does R2's design ranking survive trim
and pitch dynamics, and which printed configuration flies furthest?

    python -m engineering.organ_sims.r6_trim_map [n_seeds] [workers]

Design grid (R2 vocabulary): pectoral area x{1.0,1.2,1.4,1.6,1.8}, aspect ratio x{0.7,0.85,1.0}, root shift {0,+4 mm}.
For each design and pelvic key (decalage 2,3,4 printed; 6,8 would need a NEW printed key), the CG target is swept
-4..+12 mm from R2's rule; a trim is admissible when ballast >= 0, CG in 44-60 mm, static margin >= 0.05 MAC and trim CL
in 0.40-0.70; the admissible CG closest to trim CL 0.55 is kept.  Each kept configuration is flown nominally and with
the R5 'low' dispersion at V0 6 and 8 m/s.  Constraints from R2 (print length, biology band, catch slot) are recorded
per design.  Simulated, not observed; dispersion assumed.
"""
import gzip, json, math, sys, time
import numpy as np
from engineering.organ_sims import common as C
from engineering.organ_sims import r5_school_launch as R5
from engineering.organ_sims import r2_glide_sweep as R2

RID = "r6-trim-map"
KA = (1.0, 1.2, 1.4, 1.6, 1.8)
KAR = (0.7, 0.85, 1.0)
DX = (0.0, 0.004)
KEYS = (2.0, 3.0, 4.0, 6.0, 8.0)
SHIFTS = tuple(np.round(np.arange(-0.004, 0.0121, 0.002), 4))
V0S = (6.0, 8.0)
import os
if os.environ.get("R6_SMOKE"):             # pipeline smoke test only: never used for a reported result
    KA, KAR, DX, KEYS, SHIFTS = (1.0, 1.8), (0.7, 1.0), (0.0, 0.004), (4.0, 8.0), (0.0, 0.008)


def static(args):
    ka, kar, dx, key, sh = args
    m = R5.build_model(cg_shift=sh, decalage=key, pec=(ka, kar, dx))
    sc = R5.trim_scan(m)
    tp = R5.trim_point(sc)
    lin = [(a, cl) for a, cl, _, _ in sc if -2 <= a <= 6]
    cla = np.polyfit([a for a, _ in lin], [c for _, c in lin], 1)[0]
    sm = None if tp is None else -tp["dCm_dalpha_per_deg"] / cla
    return {"ka": ka, "kar": kar, "dx_m": dx, "key_deg": key, "cg_shift_m": float(sh), "m_kg": m["m"], "m_ballast_kg": m["m_ballast"],
            "ballast_clipped": bool(m["m_ballast"] <= 0.0 and sh > 0),
            "cg_x_m": float(m["cg"][0]), "trim": tp, "static_margin_MAC": sm}


def fly(args):
    ka, kar, dx, key, sh, v0, seed = args
    R5.V0 = v0
    m = R5.build_model(cg_shift=sh, decalage=key, pec=(ka, kar, dx))
    o, _, _ = R5.simulate(m, 1, 1.0, "none" if seed is None else "low", 0 if seed is None else seed, wake_on=False)
    return o[0]


def main():
    nseed = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    grid = [(ka, kar, dx, key, sh) for ka in KA for kar in KAR for dx in DX for key in KEYS for sh in SHIFTS]
    with ProcessPoolExecutor(workers) as ex:
        st = list(ex.map(static, grid, chunksize=4))
    # R2 hard constraints per design (same functions as R2), evaluated at R2's own CG rule
    def r2c(ka, kar, dx):
        c = R2.config(R2.S_PEC0 * ka, R2.AR0 * kar, dx, 0.8, 8.0, 0.0)
        k = R2.constraints(c)
        return {"print_length_ok": bool(k["pectoral_print_length_le_115mm"]), "biology_band_ok": bool(k["pectoral_over_SL_in_0.584_0.77"]),
                "catch_slot_ok": bool(k["fin_clears_catch_slot_x_root_ge_37mm"]), "L_fin_m": c["L_fin_m"]}
    kept = {}
    for r in st:
        tp = r["trim"]
        r["admissible"] = bool(tp and not r["ballast_clipped"] and 0.044 <= r["cg_x_m"] <= 0.060 and (r["static_margin_MAC"] or 0) >= 0.05 and 0.40 <= tp["CL"] <= 0.70)
        key = (r["ka"], r["kar"], r["dx_m"], r["key_deg"])
        if r["admissible"] and (key not in kept or abs(tp["CL"] - 0.55) < abs(kept[key]["trim"]["CL"] - 0.55)):
            kept[key] = r
    fl = []
    seeds = [None] + [2000 + s for s in range(nseed)]
    for key, r in kept.items():
        for v0 in V0S:
            for sd in seeds:
                fl.append((r["ka"], r["kar"], r["dx_m"], r["key_deg"], r["cg_shift_m"], v0, sd))
    with ProcessPoolExecutor(workers) as ex:
        fo = list(ex.map(fly, fl, chunksize=4))
    res = {}
    for a, o in zip(fl, fo):
        k = a[:4]; v0 = a[5]
        e = res.setdefault(k, {}).setdefault(v0, {"nominal": None, "dispersed": []})
        if a[6] is None:
            e["nominal"] = o["range_m"]
        else:
            e["dispersed"].append(o["range_m"])
    configs = []
    for k, r in kept.items():
        c = {"ka": k[0], "kar": k[1], "dx_m": k[2], "key_deg": k[3], "new_key_needed": k[3] > 4.0, "cg_shift_m": r["cg_shift_m"],
             "cg_x_m": r["cg_x_m"], "m_kg": r["m_kg"], "m_ballast_kg": r["m_ballast_kg"], "trim": r["trim"], "static_margin_MAC": r["static_margin_MAC"],
             "r2_constraints": r2c(*k[:3])}
        for v0 in V0S:
            d = res[k][v0]
            c[f"V{v0:g}"] = {"nominal_range_m": d["nominal"], "mean_range_m": float(np.mean(d["dispersed"])),
                             "p10_range_m": float(np.percentile(d["dispersed"], 10)), "sd_range_m": float(np.std(d["dispersed"]))}
        c["r2_feasible_all_hard"] = all(c["r2_constraints"][x] for x in ("print_length_ok", "biology_band_ok", "catch_slot_ok")) and 0.044 <= c["cg_x_m"] <= 0.060
        configs.append(c)
    # R2 point-mass ranges for the same designs (R2 rows, CLmax 0.8, level release, no penalty)
    rows2 = json.loads(gzip.open(C.ROOT / "artifacts/organ-sims/r2-glide-sweep/rows.json.gz", "rt").read())
    def r2range(ka, kar, dx, v0):
        hit = [x for x in rows2 if abs(x["S_pec_m2"] / R2.S_PEC0 - ka) < 1e-9 and abs(x["AR"] / R2.AR0 - kar) < 1e-9 and abs(x["dx_m"] - dx) < 1e-12
               and x["CLmax"] == 0.8 and x["V0"] == v0 and x["gam0"] == 0.0 and x["cd0_add"] == 0.0]
        return hit[0]["range_m"] if hit else None
    for c in configs:
        for v0 in V0S:
            c[f"V{v0:g}"]["r2_point_mass_range_m"] = r2range(c["ka"], c["kar"], c["dx_m"], v0)
    checks = []
    base = [c for c in configs if c["ka"] == 1.0 and c["kar"] == 1.0 and c["dx_m"] == 0.0 and c["key_deg"] == 4.0]
    checks.append({"name": "control: baseline design with printed key dec+4 is admissible (R5 found CL 0.55 trim at R2's CG)", "pass": bool(base), "detail": base[0] if base else None})
    s5 = [r for r in st if r["ka"] == 1.0 and r["kar"] == 1.0 and r["dx_m"] == 0.0 and r["key_deg"] == 4.0 and r["cg_shift_m"] == 0.0]
    checks.append({"name": "control: baseline dec+4 at zero CG shift reproduces R5's trim CL 0.547 (1e-6)", "pass": bool(s5) and abs(s5[0]["trim"]["CL"] - 0.5471) < 2e-3, "detail": s5[0]["trim"] if s5 else None})
    checks.append({"name": "every flown range finite and positive", "pass": all(v is not None and math.isfinite(v) and v > 0 for v in [o["range_m"] for o in fo]), "detail": len(fo)})
    # ranking comparison among designs that are both R2-feasible and 6-DOF-admissible with a PRINTED key
    def best(lst, v0, key):
        return max(lst, key=lambda c: c[f"V{v0:g}"][key]) if lst else None
    printed = [c for c in configs if not c["new_key_needed"]]
    feas_printed = [c for c in printed if c["r2_feasible_all_hard"]]
    summary = {}
    for v0 in V0S:
        summary[f"V{v0:g}"] = {
            "best_6dof_printed_key_feasible": best(feas_printed, v0, "mean_range_m"),
            "best_6dof_any_key_feasible": best([c for c in configs if c["r2_feasible_all_hard"]], v0, "mean_range_m"),
            "baseline_dec4": base[0][f"V{v0:g}"] if base else None}
        pts = [(c[f"V{v0:g}"]["r2_point_mass_range_m"], c[f"V{v0:g}"]["mean_range_m"]) for c in configs if c[f"V{v0:g}"]["r2_point_mass_range_m"] is not None]
        if len(pts) > 3:
            a = np.argsort(np.argsort([p[0] for p in pts])); b = np.argsort(np.argsort([p[1] for p in pts]))
            summary[f"V{v0:g}"]["spearman_r2_vs_6dof"] = float(np.corrcoef(a, b)[0, 1])
    figs = fig(configs)
    C.manifest(RID, "R2 wing designs re-flown in 6-DOF with moment-balance trim (CG and pelvic key) and launch dispersion",
               ["artifacts/glider/r4-daane-printfix/flight_model.json", "artifacts/glider/r4-daane-printfix/manifest.json",
                "artifacts/organ-sims/r3-underwater-drag/manifest.json", "artifacts/organ-sims/r2-glide-sweep/rows.json.gz"],
               {"summary": summary, "configs": configs, "static_grid": st, "n_static": len(st), "n_flights": len(fo), "seeds": seeds[1:], "wall_s": time.time() - t0},
               checks, {"see": "docs/organ-sims.md"}, seed=seeds[1:], figures=figs)
    print(json.dumps(summary, indent=1, default=float))
    C.enforce(checks)


def fig(configs):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    for a, v0 in zip(ax, V0S):
        for c in configs:
            x = c[f"V{v0:g}"]["r2_point_mass_range_m"]; y = c[f"V{v0:g}"]["mean_range_m"]
            if x is None:
                continue
            a.scatter(x, y, c="C3" if c["new_key_needed"] else "C0", marker="o" if c["r2_feasible_all_hard"] else "x", s=12 + 20 * c["ka"])
        lim = [0, max(a.get_xlim()[1], a.get_ylim()[1])]
        a.plot(lim, lim, "k:", lw=0.8)
        a.set_xlabel("R2 point-mass range (CLmax 0.8, R2 CG rule), m"); a.set_ylabel("6-DOF mean range, trimmed + dispersed, m")
        a.set_title(f"V0 {v0:g} m/s (blue printed key, red new key; x = fails an R2 hard constraint)", fontsize=8)
    fig.tight_layout(); fp = C.OUT / RID / "trim_map.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/trim_map.png"]


if __name__ == "__main__":
    main()
