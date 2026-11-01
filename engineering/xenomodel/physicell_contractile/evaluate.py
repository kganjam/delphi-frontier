#!/usr/bin/env python3
"""Score the frozen predictions of artifacts/xenomodel/physicell-protocol.json against runs-r1. No thresholds are set here
that are not in the protocol. usage: evaluate.py <runs dir> <out json>"""
import csv, hashlib, json, sys
from pathlib import Path
R, OUT = Path(sys.argv[1]), Path(sys.argv[2])
KAPPA = lambda xp, xm: (xm - xp) / (2 * (xp + xm))

def load(arm):
    rows = list(csv.DictReader(open(R / arm / "xm_com.csv")))
    rec = json.loads((R / arm / "receipt.json").read_text())
    X = [float(r["com_x_um"]) for r in rows]; Y = [float(r["com_y_um"]) for r in rows]
    L = [float(r["pair_dx_um"]) for r in rows] if rows[0].get("pair_dx_um") not in (None, "") else None
    ext = [float(r["extent_x_um"]) for r in rows]
    d = {"arm": arm, "exit": rec["exit"], "dX_um": X[-1] - X[0], "dY_um": Y[-1] - Y[0], "max_abs_X_excursion_um": max(abs(x - X[0]) for x in X),
         "extent_range_um": max(ext) - min(ext), "t_end_min": float(rows[-1]["t_min"]), "n_samples": len(rows), "com_csv_sha256": rec["com_csv_sha256"],
         "params": rec["params"], "dt_mechanics_min": rec["dt_mechanics_min"]}
    if L:
        tv = sum(abs(L[i + 1] - L[i]) for i in range(len(L) - 1))
        xp, xm = float(rec["params"].get("XM_XIP", 1)), float(rec["params"].get("XM_XIM", 1))
        d["TV_L_um"] = tv; d["kappa"] = KAPPA(xp, xm); d["pred_kappa_TV_um"] = KAPPA(xp, xm) * tv
        d["ratio_obs_over_pred"] = d["dX_um"] / d["pred_kappa_TV_um"] if d["pred_kappa_TV_um"] else None
    return d

A = {p.name: load(p.name) for p in sorted(R.iterdir()) if (p / "xm_com.csv").exists()}
checks = []
def chk(cid, ok, observed, prediction, endpoint=None):
    checks.append({"id": cid, "pass": bool(ok), "observed": observed, "prediction": prediction, **({"endpoint": endpoint} if endpoint else {})})

for a in ("P0-pair", "P0-strip"):
    chk(a, abs(A[a]["dX_um"]) <= 1e-9, A[a]["dX_um"], "|dX| <= 1e-9 um", "passive-control")
for a in ("I1-pair", "I2-strip-trav", "I3-strip-stand"):
    chk(a, abs(A[a]["dX_um"]) <= 1e-9, {"dX_um": A[a]["dX_um"], "max_abs_X_excursion_um": A[a]["max_abs_X_excursion_um"], "extent_range_um": A[a]["extent_range_um"]}, "|dX| <= 1e-9 um")
chk("N1-native-trav", abs(A["N1-native-trav"]["dX_um"]) <= 1e-6, {"dX_um": A["N1-native-trav"]["dX_um"], "extent_range_um": A["N1-native-trav"]["extent_range_um"]}, "|dX| <= 1e-6 um")
chk("N2-native-aniso", A["N2-native-aniso"]["dX_um"] > 0, A["N2-native-aniso"]["dX_um"], "dX > 0")
rs = []
for dt in ("0.1", "0.05", "0.025"):
    a = A[f"A1-pair-dt{dt}"]; rs.append(abs(a["ratio_obs_over_pred"] - 1))
    chk(f"A1-pair-dt{dt}", a["dX_um"] > 0 and abs(a["ratio_obs_over_pred"] - 1) <= 0.01, {"dX_um": a["dX_um"], "TV_L_um": a["TV_L_um"], "ratio": a["ratio_obs_over_pred"]}, "dX>0, |ratio-1|<=0.01")
chk("A1-dt-monotone", rs[0] >= rs[1] >= rs[2], {"abs_ratio_minus_1_by_dt": dict(zip(["0.1", "0.05", "0.025"], rs))}, "|ratio-1| non-increasing as dt halves")
for e in ("0.05", "0.2"):
    a = A[f"A1-pair-eps{e}"]
    chk(f"A1-pair-eps{e}", abs(a["ratio_obs_over_pred"] - 1) <= 0.01, {"dX_um": a["dX_um"], "TV_L_um": a["TV_L_um"], "ratio": a["ratio_obs_over_pred"]}, "|ratio-1|<=0.01")
a1, a2 = A["A1-pair-dt0.1"]["dX_um"], A["A2-pair-mirror"]["dX_um"]
chk("A2-pair-mirror", abs(a2 + a1) <= 1e-9 * abs(a1) + 1e-12, {"dX_A1": a1, "dX_A2": a2, "sum": a1 + a2}, "|dX(A2)+dX(A1)| <= 1e-9|dX(A1)| + 1e-12", "mirror-symmetry")
a4, a6 = A["A4-strip-travp-dt0.1"]["dX_um"], A["A6-strip-mirror"]["dX_um"]
chk("A6-strip-mirror", abs(a6 + a4) <= 1e-6 * abs(a4), {"dX_A4": a4, "dX_A6": a6, "sum": a4 + a6}, "|dX(A6)+dX(A4)| <= 1e-6|dX(A4)|", "mirror-symmetry")
chk("A3-strip-stand", A["A3-strip-stand-dt0.1"]["dX_um"] > 0, A["A3-strip-stand-dt0.1"]["dX_um"], "dX > 0")
ref = {k: abs(A[f"{k}-dt0.1"]["dX_um"] - A[f"{k}-dt0.05"]["dX_um"]) for k in ("A3-strip-stand", "A4-strip-travp", "A5-strip-travm")}
d34 = abs(A["A4-strip-travp-dt0.1"]["dX_um"] - A["A3-strip-stand-dt0.1"]["dX_um"]); d45 = abs(A["A4-strip-travp-dt0.1"]["dX_um"] - A["A5-strip-travm-dt0.1"]["dX_um"])
chk("pattern-dependence-A3-vs-A4", d34 > max(ref["A3-strip-stand"], ref["A4-strip-travp"]), {"diff_um": d34, "refinement_change_um": ref}, "difference > max dt-refinement change", "pattern-dependence")
chk("pattern-dependence-A4-vs-A5", d45 > max(ref["A4-strip-travp"], ref["A5-strip-travm"]), {"diff_um": d45, "refinement_change_um": ref}, "difference > max dt-refinement change", "pattern-dependence")
out = {"schema": "claude-xenomodel.physicell-results/1", "protocol": "artifacts/xenomodel/physicell-protocol.json",
       "protocol_sha256": hashlib.sha256(Path(__file__).resolve().parents[3].joinpath("artifacts/xenomodel/physicell-protocol.json").read_bytes()).hexdigest(),
       "all_exit_zero": all(v["exit"] == 0 for v in A.values()), "n_pass": sum(c["pass"] for c in checks), "n_checks": len(checks), "checks": checks, "arms": A}
OUT.write_text(json.dumps(out, indent=1) + "\n")
for c in checks: print(("PASS " if c["pass"] else "FAIL ") + c["id"], json.dumps(c["observed"])[:200])
