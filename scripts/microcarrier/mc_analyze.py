#!/usr/bin/env python3
"""Evaluate the frozen microcarrier endpoints. Implements the protocol's verdict rules
literally. E2/E3 numbers are NOT computed unless E1 is PASS (protocol gate).
usage: mc_analyze.py RUNDIR [RUNDIR...] --out verdicts.json"""
import argparse, glob, itertools, json, math, os, sys

L = 1.0e-3   # body length (m)

def load(dirs):
    R = {}
    for d in dirs:
        for rp in glob.glob(os.path.join(d, "*.receipt.json")):
            rec = json.load(open(rp)); rid = rec["run"]["id"]
            out = rp.replace(".receipt.json", ".json")
            res = json.load(open(out)) if os.path.exists(out) else None
            R[rid] = {"receipt": rec, "out": res, "dir": d}
    return R

def ok(e):
    o = e["out"]
    return (e["receipt"]["exit_code"] == 0 and o is not None and not o["numerics"]["diverged"]
            and o["result"].get("max_floor_penetration_voxel_frac", 0) <= 0.1)

def d_post(e):
    r = e["out"]["result"]; return (r["post_transient_dx_m"], r["post_transient_dy_m"])

def norm(v): return math.hypot(v[0], v[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])

def e1(R):
    ids = ["E1-passive-m1-dt0.5", "E1-passive-m1-dt0.25", "E1-passive-m2-dt0.5", "E1-passive-m3-dt0.5"]
    rows, verdict = [], "PASS"
    for i in ids:
        if i not in R: rows.append({"id": i, "status": "MISSING"}); verdict = "INCOMPLETE" if verdict == "PASS" else verdict; continue
        e = R[i]; o = e["out"]
        if not ok(e): rows.append({"id": i, "status": "RUN_FAILED", "exit": e["receipt"]["exit_code"]}); verdict = "FAIL"; continue
        r = o["result"]; p2p = o["settle"]["last_0p05s_peak_to_peak_m"]
        full = r["net_disp_m"] / L; post = norm(d_post(e)) / L; settle = max(p2p) / L
        good = full <= 1e-6 and post <= 1e-6 and settle <= 1e-6
        rows.append({"id": i, "net_disp_L": full, "post_transient_disp_L": post, "settle_p2p_L": settle,
                     "tolerance_L": 1e-6, "pass": good, "host": e["receipt"]["host"], "wall_s": e["receipt"]["wall_s"]})
        if not good: verdict = "FAIL"
    sup = []
    for i in ["E1s-uniform-m1-dt0.5", "E1s-uniform-m2-dt0.5"]:
        if i in R and ok(R[i]):
            sup.append({"id": i, "post_transient_disp_L": norm(d_post(R[i])) / L, "net_disp_L": R[i]["out"]["result"]["net_disp_m"] / L,
                        "reference_L": 1e-4, "within_reference": norm(d_post(R[i])) / L <= 1e-4})
    return {"verdict": verdict, "runs": rows, "supplement_uniform_drive": sup}

SERIES = ["m1-dt0.5", "m1-dt0.25", "m1-dt0.125", "m1-dt0.0625", "m2-dt0.5", "m3-dt0.5", "m2-dt0.25"]

def series(R, grp, tag):
    out = {}
    for lv in SERIES:
        k = f"{grp}-{tag}-{lv}"
        out[lv] = R.get(k)
    return out

def e2(R):
    A, B = series(R, "E2", "A"), series(R, "E2", "B")
    missing = [f"{t}:{lv}" for t, S in (("A", A), ("B", B)) for lv, e in S.items() if e is None]
    failed = [f"{t}:{lv}" for t, S in (("A", A), ("B", B)) for lv, e in S.items() if e is not None and not ok(e)]
    if missing: return {"verdict": "INCOMPLETE", "missing": missing}
    if failed: return {"verdict": "NO CLAIM", "reason": "a run in the series failed/diverged/penetrated", "failed": failed}
    dA = {lv: d_post(e) for lv, e in A.items()}; dB = {lv: d_post(e) for lv, e in B.items()}
    env = {}
    for t, d in (("A", dA), ("B", dB)):
        env[t] = max(norm(sub(d[i], d[j])) for i, j in itertools.combinations(SERIES, 2))
    R_env = max(env.values())
    D = {lv: norm(sub(dA[lv], dB[lv])) for lv in SERIES}
    verdict = "PASS" if all(D[lv] > R_env for lv in SERIES) else "NO CLAIM"
    def conv(d):
        dts = [d[f"m1-dt{x}"] for x in ("0.5", "0.25", "0.125", "0.0625")]
        ch_dt = [norm(sub(dts[i + 1], dts[i])) for i in range(3)]
        ms = [d["m1-dt0.5"], d["m2-dt0.5"], d["m3-dt0.5"]]
        ch_m = [norm(sub(ms[i + 1], ms[i])) for i in range(2)]
        return {"dt_successive_changes_L": [c / L for c in ch_dt], "dt_decreasing": all(ch_dt[i + 1] < ch_dt[i] for i in range(2)),
                "mesh_successive_changes_L": [c / L for c in ch_m], "mesh_decreasing": ch_m[1] < ch_m[0]}
    C = {}
    for lv in ["m1-dt0.5", "m1-dt0.25", "m2-dt0.5"]:
        e = R.get(f"E2s-C-{lv}")
        if e and ok(e): C[lv] = norm(d_post(e)) / L
    const = {}
    for t in ("A", "B"):
        for m in (2, 3):
            e = R.get(f"E2s-{t}-m{m}-dt0.5-constzeta")
            if e and ok(e): const[f"{t}-m{m}"] = [x / L for x in d_post(e)]
    return {"verdict": verdict, "D_L_by_level": {k: v / L for k, v in D.items()}, "R_envelope_L": R_env / L,
            "R_envelope_by_pattern_L": {k: v / L for k, v in env.items()},
            "d_A_L": {k: [x / L for x in v] for k, v in dA.items()}, "d_B_L": {k: [x / L for x in v] for k, v in dB.items()},
            "convergence_A": conv(dA), "convergence_B": conv(dB),
            "supplement_symmetric_control_C_disp_L": C, "supplement_constant_zeta_L": const}

def mirror_check(R, grp, a, b, S):
    rows, allok, missing = [], True, []
    for lv in SERIES:
        ea, eb = R.get(f"{grp}-{a}-{lv}"), R.get(f"{grp}-{b}-{lv}")
        if ea is None or eb is None: missing.append(lv); continue
        if not (ok(ea) and ok(eb)): rows.append({"level": lv, "status": "RUN_FAILED"}); allok = False; continue
        d0, d1 = d_post(ea), d_post(eb); exp = (S[0] * d0[0], S[1] * d0[1])
        e_abs = norm(sub(d1, exp)); tol = max(0.01 * norm(d0), 1e-5 * L)
        rows.append({"level": lv, "d_orig_L": [x / L for x in d0], "d_mirror_L": [x / L for x in d1],
                     "e_abs_L": e_abs / L, "e_rel": e_abs / norm(d0) if norm(d0) > 0 else None, "tol_L": tol / L, "pass": e_abs <= tol})
        allok &= e_abs <= tol
    if missing: return {"verdict": "INCOMPLETE", "missing": missing, "rows": rows}
    return {"verdict": "PASS" if allok else "FAIL", "rows": rows}

def e3(R):
    prim = mirror_check(R, "E3", "M", "My", (1, -1))
    sec = mirror_check(R, "E3", "A", "Ax", (-1, 1))   # E3-A-* series exists? no: A lives in E2; handled below
    # A series lives under E2-A-*, its x-mirror under E3-Ax-*; build a merged view
    merged = dict(R)
    for lv in SERIES:
        if f"E2-A-{lv}" in R: merged[f"E3-A-{lv}"] = R[f"E2-A-{lv}"]
    sec = mirror_check(merged, "E3", "A", "Ax", (-1, 1))
    return {"verdict": prim["verdict"], "primary_M_vs_My": prim, "secondary_A_vs_Ax": sec}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dirs", nargs="+"); ap.add_argument("--out", required=True)
    ap.add_argument("--diagnosis", help="diagnosis JSON for an E1 FAIL; E1 stays FAIL, E2/E3 read frozen + strict")
    ap.add_argument("--artifact-bound-L", type=float, default=0.0, help="passive artifact bound added to tolerances (strict variant)")
    a = ap.parse_args(); R = load(a.dirs)
    res = {"schema": "frontier.microcarrier-verdicts/1", "protocol": "artifacts/microcarrier/protocol.json", "E1": e1(R)}
    if res["E1"]["verdict"] == "PASS":
        res["E2"] = e2(R); res["E3"] = e3(R)
    elif a.diagnosis:
        dg = json.load(open(a.diagnosis)); b = a.artifact_bound_L
        res["gate"] = {"status": "E1 FAIL diagnosed as numerical; endpoints read after diagnosis (post-freeze deviation, disclosed)",
                       "diagnosis_file": a.diagnosis, "diagnosis": dg["diagnosis"], "artifact_bound_L": b}
        e2f, e3f = e2(R), e3(R)
        # strict variant (never looser than frozen): E2 needs D > R_env + 2b; E3 needs e_abs + 2b <= tol
        if "D_L_by_level" in e2f:
            e2f["strict_verdict"] = "PASS" if all(D > e2f["R_envelope_L"] + 2 * b for D in e2f["D_L_by_level"].values()) else "NO CLAIM"
        for key in ("primary_M_vs_My", "secondary_A_vs_Ax"):
            rows = e3f[key].get("rows", [])
            for r in rows:
                if "e_abs_L" in r: r["strict_pass"] = r["e_abs_L"] + 2 * b <= r["tol_L"]
            if rows and all("strict_pass" in r for r in rows):
                e3f[key]["strict_verdict"] = "PASS" if all(r["strict_pass"] for r in rows) else "FAIL"
        e3f["strict_verdict"] = e3f["primary_M_vs_My"].get("strict_verdict")
        res["E2"], res["E3"] = e2f, e3f
    else:
        res["E2"] = res["E3"] = {"verdict": "NOT READ", "reason": f"E1 is {res['E1']['verdict']}; protocol gate"}
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps({k: v["verdict"] for k, v in res.items() if isinstance(v, dict) and "verdict" in v}))
