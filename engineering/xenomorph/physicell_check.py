#!/usr/bin/env python3
"""Independent-engine cross-check of the xenomorph aggregation protocol in PhysiCell 1.14.2.

Off-lattice (center-based) agents, 3-D, three arms x two seeds:
  dah   : types A, B (50:50), A more cohesive than B (differential adhesion)
  equal : A and B identical (all affinities 1.0)  -> must compact, must not sort
  zero  : cell_cell_adhesion_strength = 0         -> must not compact

Generic dimensionless-in-spirit PhysiCell default-size cells; not a Xenobot, not
any organism, no frog parameter; cilia not modelled.

Usage:
  physicell_check.py gen      [--horizon MIN] [--runs-root DIR] [--only ARM-sSEED ...]
  physicell_check.py run      [--runs-root DIR] [--only ...] [--parallel 4]
  physicell_check.py analyze  [--runs-root DIR] [--results DIR]
  physicell_check.py all      (gen + run + analyze)

The PhysiCell tree is built from the 1.14.2 pristine copy with `make template && make -j4`;
the resulting ./project binary is run once per arm/seed with its own config XML, its own
cells.csv and its own output folder (<save><folder>), OMP threads = 1 per run, at most four
runs at a time (4 OpenMP threads in total).
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
PHYSICELL = Path("/data/artifacts/claude-xenomorph/physicell")
BINARY = PHYSICELL / "project"
TEMPLATE_XML = PHYSICELL / "config" / "PhysiCell_settings.xml"
DEFAULT_RUNS_ROOT = Path("/data/artifacts/claude-xenomorph/physicell-runs")
DEFAULT_RESULTS = REPO / "results" / "xenomorph" / "physicell"

SCOPE = ("Generic dimensionless-in-spirit PhysiCell default-size cells; not a Xenobot, "
         "not any organism, no frog parameter; cilia not modelled.")

# ---------------------------------------------------------------------------
# Frozen parameters (chosen before any production run; see PARAM_RATIONALE)
# ---------------------------------------------------------------------------
ARMS = ["dah", "equal", "zero"]
SEEDS = [1, 2]
N_CELLS = 250                 # 125 A + 125 B
VOLUME_FRACTION = 0.15        # sum of cell volumes / ball volume
CELL_VOLUME = 2494.0          # um^3, PhysiCell default -> radius 8.4127 um
CELL_RADIUS = (3.0 * CELL_VOLUME / (4.0 * math.pi)) ** (1.0 / 3.0)
REL_MAX_ADHESION_DIST = 1.25  # PhysiCell default
MIN_INIT_SEP = 21.5           # um, > 1.25 * 2 r = 21.03 um: nobody in adhesion range at t=0
REPULSION = 25.0              # um/min, cell_cell_repulsion_strength
ADHESION = 12.0               # um/min, cell_cell_adhesion_strength (adhesive arms)
AFFINITIES = {
    "dah":   {"AA": 1.0, "AB": 0.6, "BA": 0.6, "BB": 0.4},
    "equal": {"AA": 1.0, "AB": 1.0, "BA": 1.0, "BB": 1.0},
    "zero":  {"AA": 1.0, "AB": 1.0, "BA": 1.0, "BB": 1.0},
}
ADHESION_BY_ARM = {"dah": ADHESION, "equal": ADHESION, "zero": 0.0}
MOTILITY_SPEED = 0.5          # um/min
PERSISTENCE = 5.0             # min
MIGRATION_BIAS = 0.0
DT_MECH = 0.1
DT_PHENO = 6.0
DT_DIFF = 0.1                 # dummy substrate only; implicit solver
HORIZON = 14400.0             # min (10 d); chosen from a 240-min pilot (8 s wall); overridable with --horizon
N_SAVES = 10
DOMAIN_HALF = 200.0           # um; ball radius ~99.8 um; virtual walls at the edge
DX = 20.0
TOUCH_FACTOR = 1.05

PARAM_RATIONALE = (
    "Pre-run force-balance calculation (no simulation): PhysiCell pair potential is "
    "v = c_a*sqrt(a_ij a_ji)*(1-d/S)^2 - c_r*(1-d/R)^2 with S = 1.25 R. With the template defaults "
    "(c_a=0.4, c_r=10) the well depth is ~0.03 um^2/min, far below the effective 'temperature' of "
    "the random walk D = s^2 tau/3 = 0.42 um^2/min (s=0.5 um/min, tau=5 min), so nothing would stay "
    "bound. c_r=25, c_a=12 gives well depths AA(1.0) 3.4, AB(0.6) 1.2, BB(0.4) 0.64 um^2/min, "
    "equilibrium spacings 0.69-0.87 x sum of radii. The suggested B-B 0.2 / A-B 0.4 would give B-B "
    "depth ~0.25 (< D) and A-B ~0.64, so B cells would mostly not stay bound; B-B 0.4 / A-B 0.6 was "
    "chosen instead. DAH ordering AA > AB > BB and AB < (AA+BB)/2 = 0.7 holds (sorting with A core).")


def tag(arm, seed):
    return f"{arm}-s{seed}"


# ---------------------------------------------------------------------------
# Initial condition
# ---------------------------------------------------------------------------
def initial_cells(seed: int):
    """Random dissociated packing in a ball, min centre separation MIN_INIT_SEP.

    Uniform random draws in the ball (seeded numpy RNG), then iterative pairwise push-apart
    (random packing; pure RSA cannot reach this exclusion fraction), positions clipped back
    into the ball. Types: first half A, second half B, then shuffled.
    """
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(seed)
    R_ball = CELL_RADIUS * (N_CELLS / VOLUME_FRACTION) ** (1.0 / 3.0)
    R_c = R_ball - CELL_RADIUS
    u = rng.normal(size=(N_CELLS, 3))
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    x = u * (R_c * rng.random(N_CELLS) ** (1 / 3))[:, None]
    for it in range(20000):
        tree = cKDTree(x)
        pairs = tree.query_pairs(MIN_INIT_SEP * 1.02, output_type="ndarray")
        if len(pairs) == 0:
            break
        d = x[pairs[:, 1]] - x[pairs[:, 0]]
        dist = np.linalg.norm(d, axis=1)
        dist = np.maximum(dist, 1e-9)
        push = (0.5 * (MIN_INIT_SEP * 1.02 - dist) / dist)[:, None] * d
        dx = np.zeros_like(x)
        np.add.at(dx, pairs[:, 0], -push)
        np.add.at(dx, pairs[:, 1], push)
        x += dx + 1e-3 * rng.normal(size=x.shape)
        rr = np.linalg.norm(x, axis=1)
        out = rr > R_c
        x[out] *= (R_c / rr[out])[:, None]
    else:
        raise RuntimeError("packing did not converge")
    dmin = cKDTree(x).query(x, k=2)[0][:, 1].min()
    assert dmin > MIN_INIT_SEP, dmin
    types = np.array(["A"] * (N_CELLS // 2) + ["B"] * (N_CELLS - N_CELLS // 2))
    rng.shuffle(types)
    return x, types, {"ball_radius_um": R_ball, "centre_radius_um": R_c,
                      "min_pair_distance_um": float(dmin), "packing_iterations": it,
                      "adhesion_range_um": REL_MAX_ADHESION_DIST * 2 * CELL_RADIUS}


# ---------------------------------------------------------------------------
# Config XML from the template (tag names taken from the template, not guessed)
# ---------------------------------------------------------------------------
def _set(root, path, value):
    node = root.find(path)
    if node is None:
        raise KeyError(path)
    node.text = str(value)
    return node


def make_config(arm: str, seed: int, run_dir: Path, horizon: float):
    tree = ET.parse(TEMPLATE_XML)
    root = tree.getroot()
    for k, v in {"x_min": -DOMAIN_HALF, "x_max": DOMAIN_HALF, "y_min": -DOMAIN_HALF,
                 "y_max": DOMAIN_HALF, "z_min": -DOMAIN_HALF, "z_max": DOMAIN_HALF,
                 "dx": DX, "dy": DX, "dz": DX, "use_2D": "false"}.items():
        _set(root, f"domain/{k}", v)
    _set(root, "overall/max_time", horizon)
    _set(root, "overall/dt_diffusion", DT_DIFF)
    _set(root, "overall/dt_mechanics", DT_MECH)
    _set(root, "overall/dt_phenotype", DT_PHENO)
    _set(root, "parallel/omp_num_threads", 1)
    _set(root, "save/folder", str(run_dir / "output"))
    _set(root, "save/full_data/interval", horizon / N_SAVES)
    _set(root, "save/full_data/enable", "true")
    _set(root, "save/SVG/interval", horizon / N_SAVES)
    _set(root, "save/SVG/enable", "false")
    _set(root, "options/random_seed", seed)
    _set(root, "options/virtual_wall_at_domain_edge", "true")
    _set(root, "initial_conditions/cell_positions/folder", str(run_dir))
    _set(root, "initial_conditions/cell_positions/filename", "cells.csv")
    root.find("initial_conditions/cell_positions").set("enabled", "true")
    _set(root, "user_parameters/number_of_cells", 0)

    defs = root.find("cell_definitions")
    base = defs.find("cell_definition")
    defs.remove(base)
    aff = AFFINITIES[arm]
    for idx, name in enumerate(["A", "B"]):
        cd = copy.deepcopy(base)
        cd.set("name", name)
        cd.set("ID", str(idx))
        ph = cd.find("phenotype")
        # proliferation off: live cycle with zero transition rate
        cyc = ph.find("cycle")
        ph.remove(cyc)
        cyc = ET.Element("cycle", {"code": "5", "name": "live"})
        ptr = ET.SubElement(cyc, "phase_transition_rates", {"units": "1/min"})
        r = ET.SubElement(ptr, "rate", {"start_index": "0", "end_index": "0", "fixed_duration": "false"})
        r.text = "0.0"
        ph.insert(0, cyc)
        for m in ph.findall("death/model"):
            m.find("death_rate").text = "0.0"
        _set(ph, "volume/total", CELL_VOLUME)
        mech = ph.find("mechanics")
        _set(mech, "cell_cell_adhesion_strength", ADHESION_BY_ARM[arm])
        _set(mech, "cell_cell_repulsion_strength", REPULSION)
        _set(mech, "relative_maximum_adhesion_distance", REL_MAX_ADHESION_DIST)
        _set(mech, "attachment_rate", 0.0)
        _set(mech, "detachment_rate", 0.0)
        caa = mech.find("cell_adhesion_affinities")
        for c in list(caa):
            caa.remove(c)
        for other in ["A", "B"]:
            e = ET.SubElement(caa, "cell_adhesion_affinity", {"name": other})
            e.text = str(aff[name + other])
        mot = ph.find("motility")
        _set(mot, "speed", MOTILITY_SPEED)
        _set(mot, "persistence_time", PERSISTENCE)
        _set(mot, "migration_bias", MIGRATION_BIAS)
        _set(mot, "options/enabled", "true")
        _set(mot, "options/use_2D", "false")
        # interaction lists keyed by cell type name
        ci = ph.find("cell_interactions")
        for listtag, itemtag in [("live_phagocytosis_rates", "phagocytosis_rate"),
                                 ("attack_rates", "attack_rate"), ("fusion_rates", "fusion_rate")]:
            lst = ci.find(listtag)
            proto = lst.find(itemtag)
            for c in list(lst):
                lst.remove(c)
            for other in ["A", "B"]:
                e = copy.deepcopy(proto)
                e.set("name", other)
                e.text = "0"
                lst.append(e)
        tr = ph.find("cell_transformations/transformation_rates")
        proto = tr.find("transformation_rate")
        for c in list(tr):
            tr.remove(c)
        for other in ["A", "B"]:
            e = copy.deepcopy(proto)
            e.set("name", other)
            e.text = "0"
            tr.append(e)
        defs.append(cd)
    return tree


def cmd_gen(args):
    manifest = {}
    for arm in ARMS:
        for seed in SEEDS:
            t = tag(arm, seed)
            if args.only and t not in args.only:
                continue
            rd = args.runs_root / t
            (rd / "output").mkdir(parents=True, exist_ok=True)
            for f in (rd / "output").iterdir():
                f.unlink()
            x, types, info = initial_cells(seed)
            with open(rd / "cells.csv", "w", newline="") as fh:
                w = csv.writer(fh, lineterminator="\n")
                w.writerow(["x", "y", "z", "type"])
                for p, ty in zip(x, types):
                    w.writerow([f"{p[0]:.4f}", f"{p[1]:.4f}", f"{p[2]:.4f}", ty])
            make_config(arm, seed, rd, args.horizon).write(rd / "config.xml")
            info["horizon_min"] = args.horizon
            (rd / "init_info.json").write_text(json.dumps(info, indent=2))
            manifest[t] = info
            print(t, json.dumps(info))
    return manifest


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def run_one(rd: Path):
    cmd = ["systemd-run", "--user", "--scope", "-q", "-p", "TasksMax=256", "-p", "MemoryMax=6G",
           "-p", "MemorySwapMax=0", "-p", "RuntimeMaxSec=1800",
           "env", "OMP_NUM_THREADS=1", str(BINARY), str(rd / "config.xml")]
    t0 = time.time()
    with open(rd / "stdout.log", "w") as out:
        p = subprocess.run(cmd, cwd=PHYSICELL, stdout=out, stderr=subprocess.STDOUT)
    wall = time.time() - t0
    rec = {"command": " ".join(cmd), "cwd": str(PHYSICELL), "exit_code": p.returncode,
           "wall_time_s": round(wall, 1)}
    (rd / "run_record.json").write_text(json.dumps(rec, indent=2))
    print(rd.name, rec, flush=True)
    return rec


def cmd_run(args):
    dirs = [args.runs_root / tag(a, s) for a in ARMS for s in SEEDS
            if not args.only or tag(a, s) in args.only]
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        list(ex.map(run_one, dirs))


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def read_snapshot(xml_path: Path):
    import scipy.io
    root = ET.parse(xml_path).getroot()
    t = float(root.find("metadata/current_time").text)
    cel = root.find(".//cellular_information/cell_populations/cell_population/custom/simplified_data")
    labels = {}
    for lab in cel.find("labels"):
        labels[lab.text] = (int(lab.get("index")), int(lab.get("size")))
    fname = cel.find("filename").text
    mat = scipy.io.loadmat(xml_path.parent / fname)
    key = [k for k in mat if not k.startswith("__")][0]
    M = mat[key]
    def row(name):
        i, s = labels[name]
        return M[i:i + s]
    pos = row("position").T
    ctype = row("cell_type")[0].astype(int)
    rad = row("radius")[0] if "radius" in labels else (3 * row("total_volume")[0] / (4 * math.pi)) ** (1 / 3)
    return t, pos, ctype, rad, sorted(labels, key=lambda k: labels[k][0])


def metrics(pos, ctype, rad):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree
    N = len(pos)
    tree = cKDTree(pos)
    cand = tree.query_pairs(TOUCH_FACTOR * 2 * rad.max(), output_type="ndarray")
    if len(cand):
        d = np.linalg.norm(pos[cand[:, 0]] - pos[cand[:, 1]], axis=1)
        pairs = cand[d < TOUCH_FACTOR * (rad[cand[:, 0]] + rad[cand[:, 1]])]
    else:
        pairs = cand
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(N, N)) if len(pairs) \
        else coo_matrix((N, N))
    ncomp, lab = connected_components(g, directed=False)
    sizes = np.bincount(lab)
    c = pos.mean(axis=0)
    rel = pos - c
    rg = math.sqrt((rel ** 2).sum(axis=1).mean())
    rg_norm = float(rg / (N ** (1 / 3) * rad.mean()))
    homo = float((ctype[pairs[:, 0]] == ctype[pairs[:, 1]]).mean()) if len(pairs) else float("nan")
    rdist = np.linalg.norm(rel, axis=1)
    core_shell = (rdist[ctype == 1].mean() - rdist[ctype == 0].mean()) / rg
    G = rel.T @ rel / N
    lam = np.sort(np.linalg.eigvalsh(G))[::-1]
    asph = (lam[0] - 0.5 * (lam[1] + lam[2])) / lam.sum()
    kappa2 = 1.5 * (lam ** 2).sum() / lam.sum() ** 2 - 0.5
    # same quantities restricted to the largest cluster (diagnostic)
    big = lab == sizes.argmax()
    cb = pos[big].mean(axis=0)
    rb = np.linalg.norm(pos[big] - cb, axis=1)
    rg_big = math.sqrt((rb ** 2).mean())
    tb = ctype[big]
    cs_big = ((rb[tb == 1].mean() - rb[tb == 0].mean()) / rg_big
              if (tb == 1).any() and (tb == 0).any() and rg_big > 0 else float("nan"))
    return {"n_cells": N, "n_touching_pairs": int(len(pairs)), "n_aggregates": int(ncomp),
            "largest_cluster_fraction": float(sizes.max() / N), "rg_um": rg, "rg_norm": rg_norm,
            "sorting_index_homotypic": homo, "core_shell_index": float(core_shell),
            "asphericity": float(asph), "kappa2": float(kappa2),
            "core_shell_index_largest_cluster": float(cs_big), "mean_radius_um": float(rad.mean())}


def analyze_run(rd: Path, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    snaps = sorted((rd / "output").glob("output*.xml"))
    rows, labels = [], None
    last = None
    for s in snaps:
        t, pos, ctype, rad, labels = read_snapshot(s)
        m = {"time_min": t, "snapshot": s.name}
        m.update(metrics(pos, ctype, rad))
        rows.append(m)
        last = (pos, ctype, rad)
    with open(outdir / "metrics.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
    pos, ctype, rad = last
    with open(outdir / "final_cells.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["x", "y", "z", "type", "radius"])
        for p, ty, r in zip(pos, ctype, rad):
            w.writerow([f"{p[0]:.4f}", f"{p[1]:.4f}", f"{p[2]:.4f}", "AB"[ty], f"{r:.4f}"])
    return rows, labels


def verdicts(arm, first, last):
    out = {}
    if arm == "zero":
        out["no_compaction_rg_norm_final_ge_0.95_initial"] = bool(last["rg_norm"] >= 0.95 * first["rg_norm"])
    elif arm == "equal":
        out["no_sorting_abs_core_shell_lt_0.1"] = bool(abs(last["core_shell_index"]) < 0.1)
        out["no_sorting_homotypic_lt_0.6"] = bool(last["sorting_index_homotypic"] < 0.6)
    elif arm == "dah":
        out["compaction_largest_cluster_ge_0.9"] = bool(last["largest_cluster_fraction"] >= 0.9)
        out["compaction_rg_norm_drop_ge_20pct"] = bool(last["rg_norm"] <= 0.8 * first["rg_norm"])
        out["sorting_core_shell_gt_0.1"] = bool(last["core_shell_index"] > 0.1)
    out["PASS"] = all(out.values())
    if arm == "equal":  # brief says equal "must compact"; no numeric criterion given -> diagnostic, not in PASS
        out["diagnostic_not_scored"] = {
            "compaction_largest_cluster_ge_0.9": bool(last["largest_cluster_fraction"] >= 0.9),
            "compaction_rg_norm_drop_ge_20pct": bool(last["rg_norm"] <= 0.8 * first["rg_norm"])}
    if arm == "dah":
        out["diagnostic_not_scored"] = {
            "core_shell_index_largest_cluster": last["core_shell_index_largest_cluster"],
            "sorting_index_homotypic": last["sorting_index_homotypic"]}
    return out


def sha256(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def cmd_analyze(args):
    runs = {}
    for arm in ARMS:
        for seed in SEEDS:
            t = tag(arm, seed)
            rd = args.runs_root / t
            rec = json.loads((rd / "run_record.json").read_text()) if (rd / "run_record.json").exists() else None
            info = json.loads((rd / "init_info.json").read_text())
            rows, labels = analyze_run(rd, args.results / t)
            v = verdicts(arm, rows[0], rows[-1])
            runs[t] = {"arm": arm, "seed": seed, "run": rec, "init": info,
                       "n_snapshots": len(rows), "first": rows[0], "last": rows[-1], "verdict": v,
                       "output_labels": labels}
            print(t, v, flush=True)
    git = lambda *a: subprocess.run(["git", "-C", str(PHYSICELL), *a], capture_output=True, text=True).stdout.strip()
    pilots = []
    pj = args.runs_root / "pilots.json"
    if pj.exists():
        pilots = json.loads(pj.read_text())
    summary = {
        "scope": SCOPE,
        "engine": {"name": "PhysiCell", "version": (PHYSICELL / "VERSION.txt").read_text().strip(),
                   "license": "BSD-3-Clause",
                   "git_commit": git("rev-parse", "HEAD"), "git_describe_log": git("log", "-1", "--format=%H %s %ad"),
                   "tree": str(PHYSICELL), "build": "make template && make -j4",
                   "binary": str(BINARY), "binary_sha256": sha256(BINARY),
                   "template_config_sha256": sha256(TEMPLATE_XML)},
        "parameters": {
            "n_cells": N_CELLS, "type_ratio_A_B": "50:50", "volume_fraction_initial": VOLUME_FRACTION,
            "cell_volume_um3": CELL_VOLUME, "cell_radius_um": CELL_RADIUS,
            "relative_maximum_adhesion_distance": REL_MAX_ADHESION_DIST,
            "min_initial_center_separation_um": MIN_INIT_SEP,
            "cell_cell_repulsion_strength_um_per_min": REPULSION,
            "cell_cell_adhesion_strength_um_per_min_by_arm": ADHESION_BY_ARM,
            "cell_adhesion_affinities_by_arm": AFFINITIES,
            "attachment_rate": 0.0, "detachment_rate": 0.0,
            "motility": {"speed_um_per_min": MOTILITY_SPEED, "persistence_time_min": PERSISTENCE,
                         "migration_bias": MIGRATION_BIAS, "enabled": True, "use_2D": False},
            "cycle": "live (code 5), transition rate 0 (no proliferation)",
            "death_rates": "apoptosis 0, necrosis 0",
            "dt_mechanics_min": DT_MECH, "dt_phenotype_min": DT_PHENO, "dt_diffusion_min": DT_DIFF,
            "substrate": "template dummy 'substrate', no secretion/uptake",
            "domain_um": [-DOMAIN_HALF, DOMAIN_HALF], "voxel_um": DX, "virtual_wall_at_domain_edge": True,
            "horizon_min": runs[tag("dah", 1)]["init"]["horizon_min"], "n_saves": N_SAVES,
            "omp_threads_per_run": 1, "seeds": SEEDS,
            "physicell_random_seed": "options/random_seed = seed; numpy default_rng(seed) for placement",
            "rationale": PARAM_RATIONALE},
        "metric_definitions": {
            "touching": f"distance < {TOUCH_FACTOR} x (r_i + r_j)",
            "n_aggregates": "connected components of the touching graph (singletons count)",
            "largest_cluster_fraction": "largest component size / N",
            "rg_norm": "Rg / (N^(1/3) x mean radius), Rg about centroid of all cells",
            "sorting_index_homotypic": "fraction of touching pairs that are same-type",
            "core_shell_index": "(mean radial distance of B - mean radial distance of A) / Rg, centroid of all cells",
            "asphericity": "(l1 - (l2+l3)/2)/(l1+l2+l3), gyration-tensor eigenvalues l1>=l2>=l3",
            "kappa2": "relative shape anisotropy",
            "core_shell_index_largest_cluster": "diagnostic only: same index within the largest cluster"},
        "criteria": {
            "zero": "final rg_norm >= 0.95 x initial",
            "equal": "|core_shell_index| < 0.1 and sorting_index_homotypic < 0.6 (final)",
            "dah": "largest_cluster_fraction >= 0.9 and rg_norm drop >= 20% and core_shell_index > 0.1 (final)"},
        "pilot_runs": pilots,
        "runs": runs,
        "overall": {t: r["verdict"]["PASS"] for t, r in runs.items()},
    }
    args.results.mkdir(parents=True, exist_ok=True)
    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, list):
            return [clean(v) for v in o]
        if isinstance(o, (float, np.floating)):
            return None if math.isnan(o) else float(o)
        if isinstance(o, np.integer):
            return int(o)
        return o
    (args.results / "summary.json").write_text(json.dumps(clean(summary), indent=2, allow_nan=False))
    print("wrote", args.results / "summary.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["gen", "run", "analyze", "all"])
    ap.add_argument("--horizon", type=float, default=HORIZON)
    ap.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    ap.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--parallel", type=int, default=4)
    args = ap.parse_args()
    if args.cmd in ("gen", "all"):
        cmd_gen(args)
    if args.cmd in ("run", "all"):
        cmd_run(args)
    if args.cmd in ("analyze", "all"):
        cmd_analyze(args)


if __name__ == "__main__":
    sys.exit(main())
