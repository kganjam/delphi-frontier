#!/usr/bin/env python3
"""Score artifacts/xenomodel/voxel-parity-protocol.json predictions. usage: evaluate.py <runs dir> <out json>"""
import hashlib, json, sys
from pathlib import Path
R, OUT = Path(sys.argv[1]), Path(sys.argv[2])
def load(i):
    d = json.loads((R / f"{i}.json").read_text()); cx = d["cycle_com_x_m"] + [d["result"]["com_end_m"][0]]
    return {"id": i, "net_dx_m": d["result"]["net_dx_m"], "net_dy_m": d["result"]["net_dy_m"], "n_cycle_marks": len(cx), "diverged": d["numerics"]["diverged"],
            "dbar_m_per_cycle": (cx[20] - cx[5]) / 15 if len(cx) >= 21 else None, "per_cycle_dx_m": [cx[k + 1] - cx[k] for k in range(len(cx) - 1)],
            "dt_s": d["numerics"]["dt_s"], "json_sha256": hashlib.sha256((R / f"{i}.json").read_bytes()).hexdigest(),
            "com_csv_sha256": hashlib.sha256((R / f"{i}-com.csv").read_bytes()).hexdigest()}
A = {p.stem: load(p.stem) for p in sorted(R.glob("*.json"))}
ck = []
def chk(cid, ok, obs, pred): ck.append({"id": cid, "pass": bool(ok), "observed": obs, "prediction": pred})
for dt in ("0.5", "0.25"):
    ref = abs(A[f"A-nx5-dt{dt}"]["dbar_m_per_cycle"])
    for nx in (4, 6, 8, 10):
        v = A[f"A-nx{nx}-dt{dt}"]["dbar_m_per_cycle"]
        chk(f"P-V1 nx{nx} dt{dt}", abs(v) < 0.1 * ref, {"dbar": v, "dbar_nx5": A[f"A-nx5-dt{dt}"]["dbar_m_per_cycle"], "ratio": abs(v) / ref}, "|dbar| < 0.1 |dbar(nx5)|")
    emax = max(abs(A[f"A-nx{nx}-dt{dt}"]["dbar_m_per_cycle"]) for nx in (4, 6, 8, 10))
    for nx in (5, 7, 9):
        v = A[f"A-nx{nx}-dt{dt}"]["dbar_m_per_cycle"]; other = A[f"A-nx{nx}-dt{'0.25' if dt == '0.5' else '0.5'}"]["dbar_m_per_cycle"]
        chk(f"P-V1b nx{nx} dt{dt}", (v > 0) == (other > 0) and abs(v) > 3 * emax, {"dbar": v, "other_dt": other, "max_even": emax}, "same sign both dt, |dbar| > 3 max even")
for nx in (5, 7):
    tol = abs(A[f"A-nx{nx}-dt0.5"]["dbar_m_per_cycle"] - A[f"A-nx{nx}-dt0.25"]["dbar_m_per_cycle"])
    for dt in ("0.5", "0.25"):
        o, m = A[f"A-nx{nx}-dt{dt}"]["dbar_m_per_cycle"], A[f"B-nx{nx}-dt{dt}"]["dbar_m_per_cycle"]
        chk(f"P-V2 nx{nx} dt{dt}", abs(o + m) <= tol, {"dbar": o, "dbar_mirror": m, "sum": o + m, "refinement_change": tol}, "|dbar_mirror + dbar| <= refinement change")
for i in ("C1-long", "C1-trav"):
    chk(f"P-V3a {i}", abs(A[i]["net_dx_m"]) <= 1e-9, A[i]["net_dx_m"], "|net_dx| <= 1e-9 m")
chk("P-V3b C2-het", abs(A["C2-het"]["net_dx_m"]) > 1e-6, A["C2-het"]["net_dx_m"], "|net_dx| > 1e-6 m")
chk("P-V3c C3-het-cte0", abs(A["C3-het-cte0"]["net_dx_m"]) <= 1e-9, A["C3-het-cte0"]["net_dx_m"], "|net_dx| <= 1e-9 m")
proto = Path(__file__).resolve().parents[3] / "artifacts/xenomodel/voxel-parity-protocol.json"
OUT.write_text(json.dumps({"schema": "claude-xenomodel.voxel-parity-results/1", "protocol_sha256": hashlib.sha256(proto.read_bytes()).hexdigest(),
                           "all_ok_runs": all(not a["diverged"] for a in A.values()), "n_pass": sum(c["pass"] for c in ck), "n_checks": len(ck), "checks": ck, "runs": A}, indent=1) + "\n")
for c in ck: print(("PASS " if c["pass"] else "FAIL ") + c["id"], json.dumps(c["observed"])[:180])
