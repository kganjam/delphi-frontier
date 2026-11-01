"""Acceptance check for the F005 replay task (offered, not yet taken). Compares a participant's replay of sweep cells 240 and 1306 with the
frozen rows. Standard library only. Usage: python3 -I check_replay.py SUBMISSION.json [CELLS.json]
SUBMISSION.json: {"participant": str, "consumed": {"cells_json_sha256": str, "claim_ref": {...}}, "solver": {"name": str, "code_sha256": str,
  "independent_of": "rd_frames.py / scopedesk pde.py (state what you did NOT reuse)"}, "cells": [{"cell_id": 240, "T_tau": 800.0,
  "final_mode": int, "final_std_u": float, "refinement": {"dt_or_grid": str, "final_mode": int, "final_std_u": float}}, ...],
  "receipt": {"command": str, "exit_code": int, "wall_seconds": float, "host": str}, "cost": {"cpu_seconds": float, "participant_minutes": float}}
Exit 0 = accepted by this mechanical check (a reviewer still has to look); 1 = rejected; 2 = malformed."""
import hashlib, json, sys, urllib.request

CELLS_URL = "https://raw.githubusercontent.com/kganjam/delphi-frontier/42cbd81857b3f8c0962382cda701709326711b5a/engineering/simulation/rd/cells.json"
CELLS_SHA = "f74184cb56ba36e4face9978c96c2c00ae728a471183294c3f9d866eb066d6b6"
AMP_TOL = 0.02          # relative, between independent solvers (frozen sweep's own A-vs-B agreement was 0.5% on cell 240)


def main():
    sub = json.load(open(sys.argv[1]))
    raw = open(sys.argv[2], "rb").read() if len(sys.argv) > 2 else urllib.request.urlopen(CELLS_URL, timeout=60).read()
    if hashlib.sha256(raw).hexdigest() != CELLS_SHA:
        print("cells.json hash mismatch"); return 2
    ref = {c["cell_id"]: c["reference_row"] for c in json.loads(raw)["cells"]}
    if sub.get("consumed", {}).get("cells_json_sha256") != CELLS_SHA:
        print("REJECT: submission does not pin the consumed input version"); return 1
    for k in ("participant", "solver", "receipt", "cost", "cells"):
        if k not in sub:
            print(f"MALFORMED: missing {k}"); return 2
    if sub["receipt"].get("exit_code") != 0:
        print("REJECT: the replay run did not exit 0 (report it as a failed replay instead)"); return 1
    report, ok = [], True
    for c in sub["cells"]:
        r = ref.get(c["cell_id"])
        if r is None:
            print(f"MALFORMED: unknown cell {c['cell_id']}"); return 2
        fa = r["A"]
        mode_ok = c["final_mode"] == fa["mode"]
        amp_rel = abs(c["final_std_u"] - fa["amp"]) / fa["amp"]
        ref_ok = "refinement" in c and c["refinement"]["final_mode"] == c["final_mode"] and \
            abs(c["refinement"]["final_std_u"] - c["final_std_u"]) / c["final_std_u"] <= AMP_TOL
        report.append({"cell_id": c["cell_id"], "mode_matches_frozen": mode_ok, "amp_rel_diff": amp_rel, "amp_within_tol": amp_rel <= AMP_TOL,
                       "own_refinement_agrees": ref_ok, "frozen_linear_fastest_mode": r["linear_fastest_mode"]})
        ok &= mode_ok and amp_rel <= AMP_TOL and ref_ok
    print(json.dumps({"accepted_by_mechanical_check": ok, "cells": report,
                      "note": "A disagreement is a valid, useful outcome: it makes the cell unresolved in F003 and must be reported, not retried away."}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
