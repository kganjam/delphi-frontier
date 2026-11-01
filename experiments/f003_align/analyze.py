"""F003 alignment analysis: implements PREREG.md + AMENDMENT_1.md definitions exactly. Evidence kind: simulated + computed.
  PYTHONPATH=frontier_compute/vendor:. python3 experiments/f003_align/analyze.py BASE_DIR SPEC_DIR GRID2_DIR ROWS.jsonl P8_DT2.jsonl OUT.json"""
from __future__ import annotations

import collections
import glob
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

from scopedesk.oracles.nonlinear_sweep import ensemble as E
from scopedesk.oracles.nonlinear_sweep import run as R
from experiments.f003_align import linear_indep as LI

TOL_AMP_SOLVERS = R.TOL_AMP_SOLVERS


def nca_category(A, B):
    """The frozen sweep's cell-outcome rule (run.run_cell), applied to given A and B metric dicts."""
    if A.get("diverged") or B.get("diverged"):
        return "unresolved", "diverged"
    if A["pattern"] != B["pattern"]:
        return "unresolved", "solver_disagree_flag"
    if A["pattern"] and (A["mode"] != B["mode"] or abs(A["amp"] - B["amp"]) > TOL_AMP_SOLVERS * max(A["amp"], B["amp"])):
        return "unresolved", "solver_disagree_mode_or_amp"
    if not (A["settled"] and B["settled"]):
        return "unresolved", "not_settled"
    return ("pattern" if A["pattern"] else "no_pattern"), None


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rates(cells, outcome, linear):
    """R1, R2, R3, unresolved mass under a given outcome map {id: (category, mode)}."""
    st = [c for c in cells if linear[c] == "out_of_scope"]
    un = [c for c in cells if linear[c] == "applies"]
    r1 = sum(1 for c in st if outcome[c][0] == "pattern")
    r2 = sum(1 for c in un if outcome[c][0] == "no_pattern")
    return {"R1": [r1, len(st)], "R2": [r2, len(un)], "R3": None, "unresolved": [sum(1 for c in cells if outcome[c][0] == "unresolved"), len(cells)]}


def main():
    base_dir, spec_dir, grid_dir, rows_p, p8_p, out_p = sys.argv[1:7]
    rows = {r["id"]: r for r in map(json.loads, open(rows_p))}
    base = {}
    for f in sorted(glob.glob(f"{base_dir}/*.jsonl")):
        for l in open(f):
            r = json.loads(l)
            base[r["id"]] = r
    grid = {}
    for f in sorted(glob.glob(f"{grid_dir}/*.jsonl")):
        for l in open(f):
            r = json.loads(l)
            grid[r["id"]] = r
    p8 = {}
    for l in open(p8_p):
        r = json.loads(l)
        if r["arm"] == "dt2":
            p8[r["id"]] = r
    cells = {c["id"]: c for c in E.build(10)}
    ids = sorted(cells)
    missing = [i for i in ids if i not in base]
    out = {"inputs": {"rows_sha256": sha(rows_p), "p8_dt2_sha256": sha(p8_p), "n_base": len(base), "n_grid2": len(grid), "missing_base": missing[:50],
                      "n_missing_base": len(missing), "analyze_sha256": sha(__file__), "align_sha256": sha(Path(__file__).parent / "align.py"),
                      "linear_indep_sha256": sha(Path(__file__).parent / "linear_indep.py")}}

    # ---------------- R0 reproduction gate
    r0_fail = []
    for i in ids:
        b, fa = base.get(i), rows[i]["A"]
        if b is None:
            r0_fail.append((i, "missing")); continue
        if fa.get("diverged"):
            if not b["diverged_by_T"]:
                r0_fail.append((i, "frozen diverged, rerun not"))
            continue
        a = b.get("A_T")
        if a is None:
            r0_fail.append((i, "rerun diverged or no T state")); continue
        if a["pattern"] != fa["pattern"] or a["mode"] != fa["mode"] and a["pattern"] or a["settled"] != fa["settled"]:
            r0_fail.append((i, "flag/mode/settled")); continue
        if a["pattern"] and abs(a["amp"] - fa["amp"]) > 1e-6 * fa["amp"]:
            r0_fail.append((i, f"amp rel {abs(a['amp'] - fa['amp']) / fa['amp']:.2e}"))
    out["R0"] = {"n_fail": len(r0_fail), "fail": r0_fail[:100], "passes": len(r0_fail) <= 0.01 * len(ids)}
    r0_bad = {i for i, _ in r0_fail}

    # ---------------- step sensitivity (P8-1 recomputed per cell, B fixed at frozen rows)
    step = {}
    cat_changes = mode_flips = 0
    for i in ids:
        r = rows[i]
        A2 = p8.get(i)
        if A2 is None:
            step[i] = "no_dt2"; continue
        c2, _ = nca_category(A2, r["B"])
        changed = c2 != r["category"]
        mflip = bool(r["A"].get("pattern") and A2.get("pattern") and A2["mode"] != r["A"]["mode"])
        cat_changes += changed
        mode_flips += mflip
        step[i] = "step_sensitive" if (changed or mflip) else "step_ok_dt0.01"
    out["step"] = {"recomputed_category_changes": cat_changes, "recomputed_patterned_mode_flips": mode_flips,
                   "matches_P8_published_26_28": (cat_changes, mode_flips) == (26, 28), "n_step_sensitive": sum(v == "step_sensitive" for v in step.values())}

    # ---------------- horizon, stationarity
    horizon, stat = {}, {}
    for i in ids:
        b = base.get(i)
        if b is None or "A_T" not in b or "A_2T" not in b:
            if b is None:
                horizon[i] = "missing"
            elif b.get("diverged_by_T"):
                horizon[i] = "diverged_by_T"
            elif b.get("diverged_at_step"):
                horizon[i] = "diverged_after_T"
            else:
                horizon[i] = "no_2T"
            stat[i] = None
            continue
        a, z = b["A_T"], b["A_2T"]
        same = a["pattern"] == z["pattern"] and (not a["pattern"] or (a["mode"] == z["mode"] and abs(a["amp"] - z["amp"]) <= 0.05 * max(a["amp"], 1e-300)))
        horizon[i] = "horizon_stable" if same else "horizon_changed"
        ust = LI.steady(cells[i]["model"], cells[i]["params"])[0]
        stat[i] = "stationary" if b.get("dudt_inf_T") is not None and b["dudt_inf_T"] / max(abs(ust), 1.0) <= 1e-4 else "transient"
    out["horizon"] = dict(collections.Counter(horizon.values()))
    out["stationarity"] = dict(collections.Counter(str(v) for v in stat.values()))

    # ---------------- grid (subset)
    gridc = {}
    for i in ids:
        if i % 10:
            continue
        g, b = grid.get(i), base.get(i)
        if g is None or "A_T" not in g or b is None or "A_T" not in b:
            gridc[i] = "grid_missing_or_diverged"; continue
        a, z = b["A_T"], g["A_T"]
        same = a["pattern"] == z["pattern"] and (not a["pattern"] or (a["mode"] == z["mode"] and abs(a["amp"] - z["amp"]) <= 0.10 * a["amp"]))
        gridc[i] = "grid_ok" if same else "grid_sensitive"
    out["grid_subset"] = dict(collections.Counter(gridc.values()))

    # ---------------- linear (independent) and the observable decomposition
    lin = {}
    per = {}
    specs = {}
    for f in glob.glob(f"{spec_dir}/*.npz"):
        specs[f] = np.load(f)
    spec_of = {}
    for f, z in specs.items():
        for k in z.files:
            if k.startswith("std_"):
                spec_of[int(k[4:])] = f
    for i in ids:
        c, r = cells[i], rows[i]
        L, NA, NB, K = R.grid_for(c)
        s = LI.linear_summary(c["model"], c["params"], c["Dv"], L, NA, NB)
        lin[i] = s
        if r["linear"] != "applies" or r["category"] != "pattern" or i in r0_bad or i not in spec_of:
            continue
        z = specs[spec_of[i]]
        a = z[f"std_{i}"].astype(float)
        sp = z[f"spec_{i}"].astype(float)
        aT = base[i]["A_T"]["amp"]
        ust = LI.steady(c["model"], c["params"])[0]
        nstar = s["fastest_mode"]
        rec = {"model": c["model"], "rho": c["rho"], "x": c["x"], "eps": c["eps"], "nstar": nstar, "mT": base[i]["A_T"]["mode"],
               "LIN_OK": bool(a[0] <= 0.1 * aT), "LIN_ABS": bool(a[0] <= 0.02 * abs(ust))}
        above = np.where(a >= 0.5 * aT)[0]
        tg = int(above[0]) if len(above) else None
        rec["t_g"] = tg
        te = None
        if tg is not None:
            small = np.where(a[: tg + 1] <= 0.1 * aT)[0]
            small = small[small < tg]
            te = int(small[-1]) if len(small) else None
        rec["t_e"] = te
        if tg is not None and te is not None:
            pred = LI.l3_prediction(c["model"], c["params"], c["Dv"], L, z[f"w0u_{i}"], z[f"w0v_{i}"], float(te))
            L3 = int(np.argmax(pred[1:]) + 1)
            m_te = int(np.argmax(sp[te][1:]) + 1)
            m_tg = int(np.argmax(sp[tg][1:]) + 1)
            mT = rec["mT"]
            sT = sp[-1]
            num = np.linalg.norm(sp[te][1:] - pred[1:])
            rec.update({"L3_te": L3, "m_te": m_te, "m_tg": m_tg, "spec_relL2_te": float(num / max(np.linalg.norm(pred[1:]), 1e-300)),
                        "t_e_is_zero": te == 0, "aliasing_limited": (tg - te) <= 1})
            links = [nstar == L3, L3 == m_te, m_te == m_tg, m_tg == mT]
            rec["links_equal"] = links
            tol = [not (pred[L3] > 1.05 * pred[nstar]), not (sp[te][m_te] > 1.05 * sp[te][L3]), not (sp[tg][m_tg] > 1.05 * sp[tg][m_te]),
                   not (sT[int(np.argmax(sT[1:]) + 1)] > 1.05 * sT[m_tg])]
            rec["links_equal_tol5"] = [bool(x or y) for x, y in zip(links, tol)]
            rec["dn"] = [L3 - nstar, m_te - L3, m_tg - m_te, mT - m_tg]
            J = LI.jacobian(c["model"], c["params"])
            q = (L3 * math.pi / L) ** 2
            M = J - q * np.diag([1.0, float(__import__("fractions").Fraction(c["Dv"]))])
            rec["L3_mode_complex"] = bool((np.trace(M) ** 2 / 4 - np.linalg.det(M)) < 0)
        per[i] = rec

    def attribute(rec, key):
        if rec["mT"] == rec["nstar"]:
            first = "match"
        else:
            names = ["L_fastest_not_dominant", "L_linear_departure", "N_growth_selection", "N_post_saturation"]
            first = next((n for n, ok in zip(names, rec[key]) if not ok), "chain_equal_but_final_differs")
        return first

    def table(pop, key):
        att = collections.Counter(attribute(per[i], key) for i in pop)
        cont = collections.Counter("".join("=" if x else "x" for x in per[i][key]) for i in pop)
        returned = sum(1 for i in pop if per[i]["mT"] == per[i]["nstar"] and not all(per[i][key]))
        by = {}
        for f in ("model", "rho", "eps", "x"):
            by[f] = {str(k): dict(collections.Counter(attribute(per[i], key) for i in pop if per[i][f] == k)) for k in sorted({per[j][f] for j in pop})}
        return {"n": len(pop), "attribution": dict(att), "contingency_links(n*->L3,L3->m_te,m_te->m_tg,m_tg->mT)": dict(cont), "returned_to_nstar_after_break": returned, "by": by}

    allpat = [i for i in per]
    usable = [i for i in per if "links_equal" in per[i]]
    lin_ok = [i for i in usable if per[i]["LIN_OK"] and not per[i]["t_e_is_zero"]]
    lin_abs = [i for i in usable if per[i]["LIN_ABS"] and not per[i]["t_e_is_zero"]]
    out["decomposition"] = {
        "population": "linear applies, frozen category pattern, R0 pass",
        "n_population": len(allpat),
        "n_LIN_OK": sum(per[i]["LIN_OK"] for i in allpat), "n_LIN_ABS": sum(per[i]["LIN_ABS"] for i in allpat),
        "LIN_OK_by_eps": {str(e): [sum(per[i]["LIN_OK"] for i in allpat if per[i]["eps"] == e), sum(1 for i in allpat if per[i]["eps"] == e)] for e in E.EPS},
        "n_t_e_missing": sum(1 for i in allpat if per[i]["t_e"] is None), "n_t_e_zero": sum(1 for i in usable if per[i]["t_e_is_zero"]),
        "n_aliasing_limited": sum(1 for i in usable if per[i]["aliasing_limited"]),
        "frozen_R3_mismatch_in_population": sum(1 for i in allpat if per[i]["mT"] != per[i]["nstar"]),
        "frozen_R3_mismatch_by_regime": {"LIN_OK_resolved": sum(1 for i in lin_ok if per[i]["mT"] != per[i]["nstar"]),
                                          "finite_amplitude_start_or_unresolved_regime": sum(1 for i in allpat if per[i]["mT"] != per[i]["nstar"] and i not in lin_ok)},
        "LIN_OK": {"strict": table(lin_ok, "links_equal"), "tol5": table(lin_ok, "links_equal_tol5")},
        "LIN_ABS": {"strict": table(lin_abs, "links_equal"), "tol5": table(lin_abs, "links_equal_tol5")},
        "linear_validity_at_t_e_LIN_OK": {"m_te_equals_L3": sum(per[i]["links_equal"][1] for i in lin_ok), "n": len(lin_ok),
                                          "spec_relL2_le_0.2": sum(per[i]["spec_relL2_te"] <= 0.2 for i in lin_ok),
                                          "spec_relL2_median": float(np.median([per[i]["spec_relL2_te"] for i in lin_ok])) if lin_ok else None},
        "L3_mode_complex_LIN_OK": sum(per[i]["L3_mode_complex"] for i in lin_ok),
        "abs_dn_at_first_break_LIN_OK": dict(collections.Counter(next((abs(d) for d, ok in zip(per[i]["dn"], per[i]["links_equal"]) if not ok), 0) for i in lin_ok if per[i]["mT"] != per[i]["nstar"]))}

    # ---------------- aligned outcomes
    linear = {i: rows[i]["linear"] for i in ids}

    def aligned(i, use_grid, use_stat):
        r = rows[i]
        if r["category"] == "unresolved":
            return ("unresolved", "frozen:" + str(r["why"]))
        if i in r0_bad:
            return ("unresolved", "R0_fail")
        if horizon[i] != "horizon_stable":
            return ("unresolved", horizon[i])
        if step[i] == "step_sensitive":
            return ("unresolved", "step_sensitive")
        if use_grid and gridc.get(i) != "grid_ok":
            return ("unresolved", gridc.get(i))
        if use_stat and r["category"] == "pattern" and stat[i] != "stationary":
            return ("unresolved", "transient_at_T")
        return (r["category"], None)

    def summary(pop, use_grid, use_stat):
        oc = {i: aligned(i, use_grid, use_stat) for i in pop}
        st = [i for i in pop if linear[i] == "out_of_scope"]
        un = [i for i in pop if linear[i] == "applies"]
        r3 = [i for i in un if oc[i][0] == "pattern" and rows[i]["A"]["mode"] != rows[i]["linear_fastest_mode"]]
        res = {"n": len(pop), "R1": [sum(oc[i][0] == "pattern" for i in st), len(st)], "R2": [sum(oc[i][0] == "no_pattern" for i in un), len(un)],
               "R3": [len(r3), len(un)], "unresolved": [sum(oc[i][0] == "unresolved" for i in pop), len(pop)],
               "unresolved_reasons": dict(collections.Counter(oc[i][1] for i in pop if oc[i][0] == "unresolved"))}
        # frozen (unaligned) for the same population
        res["frozen"] = {"R1": [sum(rows[i]["category"] == "pattern" for i in st), len(st)], "R2": [sum(rows[i]["category"] == "no_pattern" for i in un), len(un)],
                         "R3": [sum(1 for i in un if rows[i]["category"] == "pattern" and rows[i]["A"]["mode"] != rows[i]["linear_fastest_mode"]), len(un)],
                         "unresolved": [sum(rows[i]["category"] == "unresolved" for i in pop), len(pop)]}
        # R3 split by attribution (LIN_OK strict) among aligned-resolved R3 cells
        res["R3_aligned_by_regime_attribution"] = dict(collections.Counter(
            (attribute(per[i], "links_equal") if i in lin_ok else "not_LIN_OK_or_regime_unresolved") for i in r3 if i in per))
        res["horizon_changed_by_model_rho"] = dict(collections.Counter(f"{cells[i]['model']}|{cells[i]['rho']}" for i in pop if horizon[i] == "horizon_changed"))
        return res

    sub = [i for i in ids if i % 10 == 0]
    out["aligned"] = {"full_no_grid": summary(ids, False, False), "full_no_grid_plus_stationarity": summary(ids, False, True),
                      "subset_mod10_with_grid": summary(sub, True, False)}
    out["per_cell"] = {str(i): {**per.get(i, {}), "horizon": horizon[i], "stationarity": stat[i], "step": step[i], "grid": gridc.get(i),
                                "aligned_full": aligned(i, False, False)[0]} for i in ids}
    json.dump(out, open(out_p, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps({k: v for k, v in out.items() if k != "per_cell"}, indent=1, default=str))


if __name__ == "__main__":
    main()
