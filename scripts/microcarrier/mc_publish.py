#!/usr/bin/env python3
"""Assemble publishable microcarrier artifacts from run directories:
 - artifacts/microcarrier/runs.csv       one row per run (receipt fields + displacement)
 - artifacts/microcarrier/receipts.jsonl all receipts verbatim
 - artifacts/microcarrier/simulation-manifest*.json  repo-format manifests with sha256 for every artifact
usage: mc_publish.py --repo REPO --runs DIR [DIR...] --media DIR"""
import argparse, csv, glob, hashlib, json, math, os
L = 1e-3
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def art(repo, path, role, mt):
    full = os.path.join(repo, path)
    return {"title": os.path.basename(path), "path": path, "sha256": sha(full), "byte_size": os.path.getsize(full), "media_type": mt, "role": role, "availability": "in-repo"}

SCOPE = ("Project scale: a 1 mm x 0.5 mm x 0.5 mm soft voxel block (organ-scale construct body in the project's scale ladder, "
         "not an organism) on a rigid frictional floor with buoyant weight only. Generic soft-body mechanics.")
NOT_EST = ["anything about Xenopus cells, tissue or xenobots", "ciliary propulsion, which is what the cited sources report; contraction here is this project's modelling choice",
           "motion in fluid (no hydrodynamics)", "a calibrated actuation-to-stress or stress-to-deformation relation (no measured modulus or contractile strain)",
           "transfer of any ranking to another engine, body or to matter"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--repo", required=True); ap.add_argument("--runs", nargs="+", required=True); ap.add_argument("--media")
    a = ap.parse_args(); od = os.path.join(a.repo, "artifacts/microcarrier"); os.makedirs(od, exist_ok=True)
    rows, recs = [], []
    for d in a.runs:
        for rp in sorted(glob.glob(os.path.join(d, "*.receipt.json"))):
            rec = json.load(open(rp)); recs.append(rec); r = rec["run"]
            o = rp.replace(".receipt.json", ".json"); out = json.load(open(o)) if os.path.exists(o) else None
            row = {"id": r["id"], "group": r["group"], "spec": r["spec"], "mesh": r["mesh"], "mirror": r["mirror"], "dtScale": r["dtScale"], "freq_Hz": r["freq"],
                   "passive": r["passive"], "zetaGlob": r["zetaGlob"], "zetaInt": r["zetaInt"], "extra": json.dumps(r.get("extra", {}), sort_keys=True),
                   "seed": rec["seed"], "exit_code": rec["exit_code"], "wall_s": rec["wall_s"], "host": rec["host"],
                   "pattern_sha256": rec["pattern_file_sha256"], "output_sha256": rec.get("output_sha256", ""), "l1_mean_abs_a": rec["pattern"]["l1_mean_abs_a"],
                   "mesh_defined": rec["pattern"]["mesh_defined"]}
            if out:
                res = out["result"]; n = max(res["post_transient_cycles"], 1)
                row.update({"diverged": out["numerics"]["diverged"], "net_dx_L": res["net_dx_m"] / L, "net_dy_L": res["net_dy_m"] / L,
                            "post_dx_per_cycle_L": res["post_transient_dx_m"] / L / n, "post_dy_per_cycle_L": res["post_transient_dy_m"] / L / n,
                            "post_disp_per_cycle_L": math.hypot(res["post_transient_dx_m"], res["post_transient_dy_m"]) / L / n,
                            "max_pen_voxel_frac": res.get("max_floor_penetration_voxel_frac")})
            rows.append(row)
    keys = sorted({k for r in rows for k in r}, key=lambda k: list(rows[0]).index(k) if k in rows[0] else 99)
    with open(os.path.join(od, "runs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); [w.writerow(r) for r in rows]
    with open(os.path.join(od, "receipts.jsonl"), "w") as f:
        for r in recs: f.write(json.dumps(r, sort_keys=True) + "\n")
    code = {p: sha(os.path.join(a.repo, p)) for p in sorted(glob.glob("scripts/microcarrier/*", root_dir=a.repo)) if os.path.isfile(os.path.join(a.repo, p))}
    base = {"evidence_kind": "simulated", "project": "tissue-microcarrier", "scale": SCOPE,
            "engine": {"name": "Voxelyze", "commit": "4287e365e11416dd108f2f361e9ec4c5a011a16c", "licence": "LGPL-3.0-or-later (source headers)"},
            "protocol": art(a.repo, "artifacts/microcarrier/protocol.json", "protocol", "application/json"), "code_files": code,
            "mechanism_note": "Sources (Kriegman 2020; Blackiston 2021, abstracts only) report ciliary locomotion. These runs model contraction as prescribed volumetric strain: a different mechanism, chosen by this project."}
    ends = dict(base, schema="frontier.microcarrier.simulation-manifest/1", id="microcarrier-endpoints-r1",
                what_it_does="Executes the three preregistered endpoints (passive control, pattern dependence, mirror symmetry) with dt and mesh refinement series.",
                artifacts=[art(a.repo, "artifacts/microcarrier/verdicts.json", "certificate", "application/json"),
                           art(a.repo, "artifacts/microcarrier/diagnostics/e1-mesh3-creep.json", "diagnosis", "application/json"),
                           art(a.repo, "artifacts/microcarrier/runs.csv", "output", "text/csv"),
                           art(a.repo, "artifacts/microcarrier/receipts.jsonl", "receipt", "application/x-ndjson")],
                does_not_establish=NOT_EST + ["spatial convergence beyond what the reported mesh series shows"])
    json.dump(ends, open(os.path.join(od, "simulation-manifest.json"), "w"), indent=1)
    if a.media:
        media = []
        for p in sorted(glob.glob(os.path.join(a.media, "*"))):
            ext = p.rsplit(".", 1)[-1]; mt = {"png": "image/png", "gif": "image/gif", "mp4": "video/mp4"}.get(ext)
            if mt: media.append(art(a.repo, os.path.relpath(p, a.repo), "render" if ext != "png" else "figure", mt))
        mm = dict(base, schema="frontier.microcarrier.media-manifest/1", id="microcarrier-media-r1",
                  what_it_does="Renders and figures from the runs above. Publication rule: show a file only if its bytes match the sha256 here.",
                  artifacts=media, does_not_establish=NOT_EST + ["a render is a picture of a simulation, never an observation"])
        json.dump(mm, open(os.path.join(od, "media-manifest.json"), "w"), indent=1)
    print(len(rows), "runs;", sum(r["exit_code"] != 0 for r in rows), "nonzero exits")
