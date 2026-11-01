"""Write artifacts/organ-sims/index.json: one card per completed run with its project scale(s), what it does NOT
establish, check tally, manifest hash and figures, so the studio page can link runs without overclaiming.

    python -m engineering.organ_sims.index
"""
import json
from engineering.organ_sims import common as C


def main():
    cards = []
    for rid, (scales, not_est) in C.SCALES.items():
        mf = C.OUT / rid / "manifest.json"
        if not mf.exists():
            cards.append({"id": rid, "scales": scales, "status": "no manifest (run not completed)"})
            continue
        m = json.loads(mf.read_text())
        ch = m.get("checks", [])
        cards.append({"id": rid, "title": m["title"], "scales": scales, "evidence_kind": m["evidence_kind"],
                      "does_not_establish": not_est, "checks_passed": sum(bool(c["pass"]) for c in ch), "checks_total": len(ch),
                      "all_checks_pass": all(bool(c["pass"]) for c in ch), "ran_utc": m["ran_utc"],
                      "manifest": f"artifacts/organ-sims/{rid}/manifest.json", "manifest_sha256": C.sha(mf),
                      "figures": m.get("figures", []), "doc": "docs/organ-sims.md",
                      "manifest_has_scale_fields": "scales" in m})
    out = {"schema": "frontier.organ-sim.index/1", "owner": "claude-organ (ff-organ)", "evidence_kind": C.SCOPE,
           "scale_note": "collective = rigid-body physics of a simultaneous release (r5); population and behaviour layers belong to ff-eco",
           "runs": cards}
    tmp = C.OUT / "index.json.tmp"
    tmp.write_text(json.dumps(out, indent=1) + "\n")
    tmp.replace(C.OUT / "index.json")
    print(json.dumps([(c["id"], c["scales"], c.get("checks_passed"), c.get("checks_total")) for c in cards]))


if __name__ == "__main__":
    main()
