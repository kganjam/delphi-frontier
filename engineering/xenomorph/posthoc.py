"""POST-HOC supplementary metrics (added after the protocol freeze, in response to the gemini-4-argon review).
They do not replace any frozen gate; they are reported beside it, labelled post-hoc.

Per returned snapshot in RUN/fields.npz:
  core_shell_index_largest   core-shell index computed on the largest contact cluster only (its own centroid)
  A_medium_exposure_fraction share of type-A cell surface (voxel faces) that faces medium; ~0 = A fully engulfed
  B_medium_exposure_fraction same for B
  n_aggregates_26            aggregate count with 26-neighbourhood contact (faces, edges, corners: Morpheus order 2)
  fragmented_cells           cells whose voxels form more than one 6-connected piece

Usage: python -m engineering.xenomorph.posthoc RUN_DIR [...]  -> RUN_DIR/posthoc.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.csgraph import connected_components


def contact_graph(ids: np.ndarray, n: int, full: bool):
    rows, cols = [], []
    offs = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    if full:
        offs = [(a, b, c) for a in (0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) > (0, 0, 0)]
    L = ids.shape
    for o in offs:
        s1 = tuple(slice(max(0, -d), L[i] - max(0, d)) for i, d in enumerate(o))
        s2 = tuple(slice(max(0, d), L[i] - max(0, -d)) for i, d in enumerate(o))
        a, b = ids[s1].ravel(), ids[s2].ravel()
        m = (a != b) & (a > 0) & (b > 0)
        rows.append(a[m]); cols.append(b[m])
    r = np.concatenate(rows).astype(np.int64); c = np.concatenate(cols).astype(np.int64)
    g = sparse.coo_matrix((np.ones(len(r)), (r, c)), shape=(n + 1, n + 1)).tocsr()
    return g


def one(ids: np.ndarray, ty: np.ndarray) -> dict:
    ids = ids.astype(np.int64)
    n = int(ids.max())
    present = np.unique(ids[ids > 0])
    out = {}
    for full, key in ((False, "n_aggregates_6"), (True, "n_aggregates_26")):
        g = contact_graph(ids, n, full)
        nc, lab = connected_components(g, directed=False)
        lab_p = lab[present]
        out[key] = int(len(np.unique(lab_p)))
        if not full:
            vals, cnts = np.unique(lab_p, return_counts=True)
            big = vals[np.argmax(cnts)]
            big_cells = present[lab_p == big]
    mask = np.isin(ids, big_cells)
    coords = np.argwhere(mask).astype(float)
    c0 = coords.mean(0)
    r = np.sqrt(((coords - c0) ** 2).sum(1))
    rg = np.sqrt((r ** 2).mean())
    tvox = ty[ids[mask]]
    out["core_shell_index_largest"] = round(float((r[tvox == 2].mean() - r[tvox == 1].mean()) / rg), 6) \
        if (tvox == 1).any() and (tvox == 2).any() else None
    # exposure: faces of type-k voxels that touch medium / all boundary faces of type-k cells
    tfield = np.where(ids > 0, ty[ids], 0)
    exp_med = {1: 0, 2: 0}; exp_all = {1: 0, 2: 0}
    for ax in range(3):
        for a, b in ((np.take(ids, range(0, ids.shape[ax] - 1), ax), np.take(ids, range(1, ids.shape[ax]), ax)),):
            ta = np.take(tfield, range(0, ids.shape[ax] - 1), ax); tb = np.take(tfield, range(1, ids.shape[ax]), ax)
            diff = a != b
            for k in (1, 2):
                for x, y, tx in ((a, b, ta), (b, a, tb)):
                    sel = diff & (tx == k)
                    exp_all[k] += int(sel.sum())
                    exp_med[k] += int((sel & (y == 0)).sum())
    out["A_medium_exposure_fraction"] = round(exp_med[1] / max(exp_all[1], 1), 6)
    out["B_medium_exposure_fraction"] = round(exp_med[2] / max(exp_all[2], 1), 6)
    frag = 0
    objs = ndimage.find_objects(ids)
    for k, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        if ndimage.label(ids[sl] == k)[1] > 1:
            frag += 1
    out["fragmented_cells"] = frag
    return out


def run(d: Path) -> dict:
    F = np.load(d / "fields.npz")
    times = sorted(int(k.split("_")[1]) for k in F.files if k.startswith("ids_"))
    rows = [{"mcs": t, **one(F[f"ids_{t}"], F[f"types_{t}"])} for t in times]
    res = {"schema": "frontier.xenomorph.posthoc/1", "label": "POST-HOC supplementary metrics; not frozen gates",
           "rows": rows}
    (d / "posthoc.json").write_text(json.dumps(res, indent=1) + "\n")
    return res


if __name__ == "__main__":
    for a in sys.argv[1:]:
        r = run(Path(a))
        print(a, r["rows"][0], r["rows"][-1])
