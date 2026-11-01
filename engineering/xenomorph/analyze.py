"""Measure morphogenesis per snapshot from Morpheus cell.id / cell.type TIFF fields.

Usage: python -m engineering.xenomorph.analyze RUN_DIR [RUN_DIR ...]
Writes RUN_DIR/metrics.csv and RUN_DIR/metrics.json (definitions in protocol.json).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import tifffile
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from skimage.measure import marching_cubes, mesh_surface_area

FIELDS = ["mcs", "n_cells_present", "n_aggregates", "largest_cluster_fraction", "sphericity_largest",
          "contact_area_cell_cell", "contact_area_cell_medium", "rg_all", "rg_norm",
          "sorting_index_homotypic", "core_shell_index", "min_cell_volume", "max_cell_volume"]


def load_snapshot(path: Path) -> tuple[np.ndarray, np.ndarray]:
    a = tifffile.imread(path)
    # Morpheus writes (z, channel, y, x) for 3-D with 2 channels; normalise to (2, z, y, x)
    a = np.asarray(a)
    if a.ndim == 3 and a.shape[0] % 2 == 0:
        # Morpheus 2.3.9 (OME-header off) writes pages interleaved as z0c0, z0c1, z1c0, ...
        a = np.stack([a[0::2], a[1::2]])
    elif a.ndim == 4 and a.shape[1] == 2:
        a = np.moveaxis(a, 1, 0)
    else:
        raise ValueError(f"unexpected TIFF shape {a.shape} in {path}")
    return a[0].astype(np.int64), a[1].astype(np.int64)


def face_pairs(ids: np.ndarray):
    """Yield (a, b) arrays of voxel values across every face, all three axes."""
    for ax in range(3):
        sl1 = [slice(None)] * 3
        sl2 = [slice(None)] * 3
        sl1[ax] = slice(0, -1)
        sl2[ax] = slice(1, None)
        yield ids[tuple(sl1)].ravel(), ids[tuple(sl2)].ravel()


def measure(ids: np.ndarray, types: np.ndarray, type_a: int, n_expected: int) -> dict:
    occ = ids > 0
    labels = np.unique(ids[occ])
    n = len(labels)
    remap = np.zeros(int(ids.max()) + 1, dtype=np.int64)
    remap[labels] = np.arange(n)
    # per-cell type: mode of type channel inside the cell
    flat_ids = remap[ids[occ]]
    cell_type = np.zeros(n, dtype=np.int64)
    np.maximum.at(cell_type, flat_ids, types[occ])
    vols = np.bincount(flat_ids, minlength=n)

    cc = 0
    cm = 0
    homo = 0
    rows, cols = [], []
    for a, b in face_pairs(ids):
        diff = a != b
        a2, b2 = a[diff], b[diff]
        both = (a2 > 0) & (b2 > 0)
        one = (a2 > 0) ^ (b2 > 0)
        cm += int(one.sum())
        ia, ib = remap[a2[both]], remap[b2[both]]
        cc += int(both.sum())
        homo += int((cell_type[ia] == cell_type[ib]).sum())
        rows.append(ia)
        cols.append(ib)
    rows = np.concatenate(rows) if rows else np.zeros(0, int)
    cols = np.concatenate(cols) if cols else np.zeros(0, int)
    g = sparse.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n)).tocsr()
    ncomp, comp = connected_components(g, directed=False)
    comp_cells = np.bincount(comp, minlength=ncomp)
    big = int(np.argmax(comp_cells))
    lcf = comp_cells[big] / n_expected

    # sphericity of largest component from marching cubes
    big_mask = np.zeros(n + 1, bool)
    big_mask[1:][comp == big] = True
    full = np.zeros(ids.shape, bool)
    full[occ] = big_mask[1:][flat_ids]
    pad = np.pad(full, 1).astype(np.float32)
    verts, faces, _, _ = marching_cubes(pad, level=0.5)
    area = float(mesh_surface_area(verts, faces))
    V = float(full.sum())
    spher = math.pi ** (1 / 3) * (6 * V) ** (2 / 3) / area if area > 0 else float("nan")

    coords = np.argwhere(occ).astype(np.float64)
    c0 = coords.mean(0)
    d2 = ((coords - c0) ** 2).sum(1)
    rg = math.sqrt(d2.mean())
    rg_norm = rg / (float(occ.sum())) ** (1 / 3)
    r = np.sqrt(d2)
    tA = cell_type[flat_ids] == type_a
    core_shell = (r[~tA].mean() - r[tA].mean()) / rg if tA.any() and (~tA).any() else float("nan")
    return {"n_cells_present": n, "n_aggregates": int(ncomp), "largest_cluster_fraction": round(float(lcf), 6),
            "sphericity_largest": round(spher, 6), "contact_area_cell_cell": cc, "contact_area_cell_medium": cm,
            "rg_all": round(rg, 4), "rg_norm": round(rg_norm, 6),
            "sorting_index_homotypic": round(homo / cc, 6) if cc else float("nan"),
            "core_shell_index": round(float(core_shell), 6),
            "min_cell_volume": int(vols.min()), "max_cell_volume": int(vols.max())}


def analyze(run: Path) -> dict:
    meta = json.loads((run / "init_cells.json").read_text())
    tiffs = sorted(run.glob("cell.id_cell.type_*.tif"), key=lambda p: int(re.findall(r"(\d+)\.tif$", p.name)[0]))
    rows = []
    # Morpheus numbers cell types by declaration order; medium=0? determine A id from t=0 snapshot vs init types
    ids0, types0 = load_snapshot(tiffs[0])
    type_vals = sorted(set(np.unique(types0[ids0 > 0]).tolist()))
    type_a = type_vals[0]  # A is declared before B in the XML
    for t in tiffs:
        mcs = int(re.findall(r"(\d+)\.tif$", t.name)[0])
        ids, types = load_snapshot(t)
        m = measure(ids, types, type_a, meta["n_cells"])
        rows.append({"mcs": mcs, **m})
    with open(run / "metrics.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    out = {"schema": "frontier.xenomorph.metrics/1", "arm": meta["arm"], "seed": meta["seed"], "scale": meta["scale"],
           "type_ids": {"A": type_a, "all": type_vals},
           "t0_all_cells_separate": rows[0]["n_aggregates"] == meta["n_cells"],
           "inputs": {t.name: hashlib.sha256(t.read_bytes()).hexdigest() for t in tiffs},
           "analyzer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "rows": rows}
    (run / "metrics.json").write_text(json.dumps(out, indent=1) + "\n")
    return out


if __name__ == "__main__":
    for d in sys.argv[1:]:
        o = analyze(Path(d))
        r0, r1 = o["rows"][0], o["rows"][-1]
        print(d, "t0sep", o["t0_all_cells_separate"], "first", r0, "\nlast", r1)
