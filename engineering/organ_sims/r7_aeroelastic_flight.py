"""R7: fly R6's designs in the 6-DOF model with a quasi-static aeroelastic correction to pectoral lift taken from R4b
(bending + torsion of the printed fin), and compare with rigid fins.

    python -m engineering.organ_sims.r7_aeroelastic_flight [n_seeds] [workers]

Correction: R4b's printed-fin case (EI 7.35e-3 N m^2, elastic axis 0.05 chord = spar on the leading ray, 24x6 mesh)
gives dCL/CL at U = 8, 12, 16, 20 m/s for GJ/EI 0.3 and 1.0; the printed estimate GJ/EI (R4b manifest) is interpolated in
log(GJ/EI).  Below 8 m/s the change scales with U^2 (small-deflection linear aeroelasticity), above 20 m/s it is held.
The multiplier acts on each pectoral surface's CL at its local airspeed, every time step (quasi-static: no fin dynamics).
Caveats: R4b used v3a fin geometry; the R6 scaled fins reuse the same factor (their EI and GJ would change with size).
Designs: baseline dec+4 and R6's two recommendations; V0 6/8/10 m/s; nominal + 'low' dispersion seeds; rigid vs elastic.
Simulated, not observed.
"""
import json, math, sys, time
import numpy as np
from engineering.organ_sims import common as C
from engineering.organ_sims import r5_school_launch as R5
from engineering.organ_sims import r5c_integrated as R5C

RID = "r7-aeroelastic-flight"
V0S = (6.0, 8.0, 10.0)
import os
if os.environ.get("R7_SMOKE"):
    V0S = (8.0,)


def factor_table():
    m = json.loads((C.ROOT / "artifacts/organ-sims/r4b-torsion/manifest.json").read_text())["results"]
    gj = m["printed_fin_torsion_estimate"]["GJ_over_EI"]
    rows = [r for r in m["rows"] if abs(r["EI_pectoral_Nm2"] - 7.35e-3) < 1e-9 and r["f_ea"] == 0.05 and r["mesh"] == [24, 6] and r["valid"]]
    out = {}
    for U in (8.0, 12.0, 16.0, 20.0):
        lo = [r for r in rows if r["U_m_s"] == U and r["GJ_over_EI"] == 0.3]
        hi = [r for r in rows if r["U_m_s"] == U and r["GJ_over_EI"] == 1.0]
        if not lo or not hi:
            raise SystemExit(f"R4b lacks a valid printed-fin row at {U} m/s")
        w = (math.log(gj) - math.log(0.3)) / (math.log(1.0) - math.log(0.3))
        out[U] = (1 - w) * lo[0]["dCL_rel"] + w * hi[0]["dCL_rel"]
    return gj, out


def make_factor(tab):
    Us = np.array(sorted(tab)); d = np.array([tab[u] for u in Us])
    def f(V):
        if V <= Us[0]:
            return 1.0 + d[0] * (V / Us[0]) ** 2
        return 1.0 + float(np.interp(V, Us, d))
    return f


def _fly(args):
    dname, d, v0, seed, elastic, tab = args
    R5.V0 = v0
    R5.PEC_CL_FACTOR = make_factor(tab) if elastic else None
    m = R5.build_model(cg_shift=d["cg_shift"], decalage=d["key"], pec=tuple(d["pec"]))
    o, _, _ = R5.simulate(m, 1, 1.0, "none" if seed is None else "low", 0 if seed is None else seed, wake_on=False)
    tp = R5.trim_point(R5.trim_scan(m, V=v0))
    return o[0]["range_m"], o[0]["max_pitch_dev_deg"], tp


def main():
    nseed = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    gj, tab = factor_table()
    D = R5C.designs()
    seeds = [None] + [4000 + s for s in range(nseed)]
    jobs = [(dn, d, v0, sd, el, tab) for dn, d in D.items() for v0 in V0S for el in (False, True) for sd in seeds]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_fly, jobs, chunksize=4))
    summ = {}
    for (dn, d, v0, sd, el, _), (rg, pd, tp) in zip(jobs, res):
        e = summ.setdefault(f"{dn}/V{v0:g}/{'elastic' if el else 'rigid'}", {"dispersed": [], "nominal": None, "trim_nominal": None})
        if sd is None:
            e["nominal"] = rg; e["trim_nominal"] = tp; e["pitch_dev_nominal_deg"] = pd
        else:
            e["dispersed"].append(rg)
    for e in summ.values():
        x = e.pop("dispersed"); e["mean_range_m"] = float(np.mean(x)); e["p10_range_m"] = float(np.percentile(x, 10)); e["n"] = len(x)
    comp = {}
    for dn in D:
        for v0 in V0S:
            r, el = summ[f"{dn}/V{v0:g}/rigid"], summ[f"{dn}/V{v0:g}/elastic"]
            comp[f"{dn}/V{v0:g}"] = {"mean_range_change": el["mean_range_m"] / r["mean_range_m"] - 1, "p10_change": el["p10_range_m"] / r["p10_range_m"] - 1,
                                     "trim_CL_rigid": r["trim_nominal"] and r["trim_nominal"]["CL"], "trim_CL_elastic": el["trim_nominal"] and el["trim_nominal"]["CL"],
                                     "trim_alpha_rigid": r["trim_nominal"] and r["trim_nominal"]["alpha_deg"], "trim_alpha_elastic": el["trim_nominal"] and el["trim_nominal"]["alpha_deg"]}
    checks = []
    r6 = json.loads((C.ROOT / "artifacts/organ-sims/r6-trim-map/manifest.json").read_text())["results"]["summary"]["V8"]
    b = summ.get("baseline_dec4/V8/rigid")
    checks.append({"name": "control: rigid baseline dec+4 nominal range at 8 m/s equals R5/R6 (6.38316 m, 1e-6)", "pass": b is not None and abs(b["nominal"] - 6.38315643437261) < 1e-6, "detail": b and b["nominal"]})
    f = make_factor(tab)
    checks.append({"name": "control: correction factor is 1 at zero speed and matches R4b at 8/20 m/s", "pass": abs(f(0.0) - 1) < 1e-12 and abs(f(8.0) - 1 - tab[8.0]) < 1e-12 and abs(f(20.0) - 1 - tab[20.0]) < 1e-12,
                   "detail": {"table": tab, "GJ_over_EI_printed": gj}})
    checks.append({"name": "every range finite and positive", "pass": all(math.isfinite(r[0]) and r[0] > 0 for r in res), "detail": len(res)})
    C.manifest(RID, "6-DOF flights of R6 designs with an R4b quasi-static aeroelastic correction to pectoral lift",
               ["artifacts/organ-sims/r4b-torsion/manifest.json", "artifacts/organ-sims/r6-trim-map/manifest.json", "artifacts/glider/r4-daane-printfix/flight_model.json"],
               {"factor_table_dCL_rel_by_U": tab, "GJ_over_EI_printed": gj, "summary": summ, "comparison": comp, "designs": D, "seeds": seeds[1:], "wall_s": time.time() - t0},
               checks, {"see": "docs/organ-sims.md"}, seed=seeds[1:], figures=[])
    print(json.dumps(comp, indent=1))
    C.enforce(checks)


if __name__ == "__main__":
    main()
