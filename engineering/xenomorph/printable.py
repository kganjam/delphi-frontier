"""Turn simulated cell fields into printable geometry (millimetres), using the repo's geometry conventions.

Two solids per snapshot:
  * <id>-cells.stl    cell-resolved: every cell is its own sphere (equal-volume radius x CELL_RADIUS_FACTOR) at its
                      voxel centroid, unioned with manifold3d, so the print is visibly made of cells;
  * <id>-surface.stl  aggregate surface: marching-cubes isosurface (level 0.5) of the Gaussian-smoothed occupancy field.
If a solid has more than one piece at the chosen radius, the connectivity report says so and gives the radius factor
that would join it, and PRINT-ONLY connector struts (fixed mm, never scaled from biology) are added along the
minimum spanning tree of the gaps so the part prints as one body.  The strut-free solid's piece count is reported.

Units: biological values SI (metres); prop in mm;  prop_mm = biological_m * 1000 * DISPLAY_SCALE.
The voxel length H_VOXEL_M is a declared nominal assumption (not a measured cell size, no frog parameter).

Usage: python -m engineering.xenomorph.printable --fields RUN/fields.npz --metrics RUN/metrics.json --out DIR
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import manifold3d as mf
import numpy as np
from scipy import ndimage
from scipy.sparse.csgraph import connected_components, minimum_spanning_tree
from scipy.spatial.distance import cdist
from skimage.measure import marching_cubes

from engineering.geometry import validate as VAL

HERE = Path(__file__).resolve().parent
H_VOXEL_M = 20e-6           # nominal lattice spacing, declared assumption: compact aggregate ~0.8 mm across
DISPLAY_SCALE = 75.0        # 1 m of simulated aggregate = 75 m of prop, i.e. 1 voxel = 1.5 mm
CELL_RADIUS_FACTOR = 1.0    # sphere radius = equal-volume radius of the cell's voxel set
STRUT_RADIUS_MM = 1.25      # print-only connector, fixed in mm (not biological)
SMOOTH_SIGMA_VOX = 1.0
SPHERE_SEGMENTS = 40
BOX_MM = 120.0
MIN_WALL_MM = 1.0           # repo's provisional prop wall rule (docs/printing.md), not a printer certification
RESIN_DENSITY_G_CM3 = 1.18  # stated assumption for a generic photopolymer; printer and resin are unknown
PRINTER_RESIN = {"printer": "unknown", "resin": "unknown", "layer_height": "unknown",
                 "note": "not chosen; run the docs/printing.md operator checklist in PreForm before printing"}
SCOPE = ("Physical model of a SIMULATED aggregate morphology (dimensionless Cellular Potts / differential adhesion). "
         "Not a Xenobot, not any organism, not a living construct, not a biological validation; demonstrates nothing "
         "about viability. No frog parameter is used. Published constructs move by cilia; cilia are not modelled here.")


def mm_per_voxel() -> float:
    return H_VOXEL_M * 1000.0 * DISPLAY_SCALE


def cell_table(ids: np.ndarray, types: np.ndarray):
    """Centroid (x,y,z voxel units), voxel count and type for each cell index 1..n.  ids indexed [z,y,x]."""
    n = int(ids.max())
    idx = np.arange(1, n + 1)
    zz, yy, xx = np.nonzero(ids)
    lab = ids[zz, yy, xx].astype(np.int64)
    cnt = np.bincount(lab, minlength=n + 1)[1:]
    cx = np.bincount(lab, weights=xx, minlength=n + 1)[1:] / np.maximum(cnt, 1)
    cy = np.bincount(lab, weights=yy, minlength=n + 1)[1:] / np.maximum(cnt, 1)
    cz = np.bincount(lab, weights=zz, minlength=n + 1)[1:] / np.maximum(cnt, 1)
    keep = cnt > 0
    return np.stack([cx, cy, cz], 1)[keep], cnt[keep], types[idx][keep]


def orient_cylinder(p0: np.ndarray, p1: np.ndarray, r: float) -> mf.Manifold:
    v = p1 - p0
    L = float(np.linalg.norm(v))
    c = mf.Manifold.cylinder(L, r, r, 16)
    z = np.array([0.0, 0.0, 1.0])
    u = v / L
    ax = np.cross(z, u)
    s, cth = np.linalg.norm(ax), float(np.dot(z, u))
    if s < 1e-12:
        R = np.eye(3) if cth > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        k = ax / s
        K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
        R = np.eye(3) + s * K + (1 - cth) * K @ K
    M = np.hstack([R, p0[:, None]])
    return c.transform(M.tolist())


NECK_MIN_RADIUS_MM = STRUT_RADIUS_MM  # a sphere contact counts as a join only if its neck is at least a strut


def neck_radius(D: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Analytic radius of the circle where two spheres intersect (0 if they do not overlap)."""
    Ri, Rj = R[:, None], R[None, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        a = (D ** 2 + Ri ** 2 - Rj ** 2) / (2 * D)
        h2 = Ri ** 2 - a ** 2
    h = np.where((D < Ri + Rj) & (D > 0) & (h2 > 0), np.sqrt(np.clip(h2, 0, None)), 0.0)
    return h


def components_by_overlap(C: np.ndarray, R: np.ndarray, neck_min: float = 0.0):
    """Components of the join graph. C, R in the same units; neck_min in those units."""
    D = cdist(C, C)
    h = neck_radius(D, R)
    adj = h > max(neck_min, 1e-9)
    np.fill_diagonal(adj, False)
    n, lab = connected_components(adj, directed=False)
    return n, lab, D


def connectivity(C: np.ndarray, R: np.ndarray) -> dict:
    """C, R in mm.  Pieces at the chosen radius (a join needs neck radius >= NECK_MIN_RADIUS_MM), the smallest
    uniform radius factor k that makes every MST pair at least overlap (k*R spheres), and the thinnest accepted neck."""
    n, lab, D = components_by_overlap(C, R, NECK_MIN_RADIUS_MM)
    h = neck_radius(D, R)
    acc = h[h > NECK_MIN_RADIUS_MM]
    # smallest uniform factor k so that every MST pair has neck radius >= NECK_MIN_RADIUS_MM (equal-sphere formula
    # k = sqrt((D/2)^2 + h^2) / R_mean per pair, conservative for unequal radii); argon review item 7
    Rm = (R[:, None] + R[None, :]) / 2
    kpair = np.sqrt((D / 2) ** 2 + NECK_MIN_RADIUS_MM ** 2) / Rm
    np.fill_diagonal(kpair, 0)
    mst = minimum_spanning_tree(kpair).toarray()
    k_needed = float(mst.max()) if (mst > 0).any() else 0.0
    return {"pieces_at_chosen_radius": int(n), "radius_factor_needed_to_join_all": round(k_needed * CELL_RADIUS_FACTOR, 4),
            "radius_factor_rule": "smallest uniform factor giving every minimum-spanning-tree pair a neck radius >= the join minimum",
            "chosen_radius_factor": CELL_RADIUS_FACTOR, "one_body_without_struts": n == 1,
            "join_rule": f"two cell spheres are joined iff their intersection neck radius >= {NECK_MIN_RADIUS_MM} mm",
            "thinnest_accepted_neck_diameter_mm": round(2 * float(acc.min()), 3) if len(acc) else None}


def strut_edges(C: np.ndarray, R: np.ndarray) -> list[tuple[int, int]]:
    """MST over centre distances restricted so struts are only added where spheres do not already overlap."""
    n, lab, D = components_by_overlap(C, R, NECK_MIN_RADIUS_MM)
    if n == 1:
        return []
    # MST between components: Kruskal on component-pair shortest gaps
    edges = []
    gap = D - (R[:, None] + R[None, :])
    comp_pairs = {}
    for i in range(len(C)):
        for j in range(i + 1, len(C)):
            a, b = lab[i], lab[j]
            if a == b:
                continue
            key = (min(a, b), max(a, b))
            if key not in comp_pairs or gap[i, j] < comp_pairs[key][0]:
                comp_pairs[key] = (gap[i, j], i, j)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for g, i, j in sorted(comp_pairs.values()):
        ra, rb = find(lab[i]), find(lab[j])
        if ra != rb:
            parent[ra] = rb
            edges.append((i, j))
    return edges


def cells_solid(C_mm: np.ndarray, R_mm: np.ndarray, struts: list[tuple[int, int]]) -> mf.Manifold:
    parts = [mf.Manifold.sphere(float(r), SPHERE_SEGMENTS).translate(tuple(map(float, c))) for c, r in zip(C_mm, R_mm)]
    for i, j in struts:
        parts.append(orient_cylinder(C_mm[i], C_mm[j], STRUT_RADIUS_MM))
    return mf.Manifold.batch_boolean(parts, mf.OpType.Add)


def surface_solid(ids: np.ndarray, struts_mm: list[tuple[np.ndarray, np.ndarray]]) -> mf.Manifold:
    occ = (ids > 0).astype(np.float32)
    sm = ndimage.gaussian_filter(np.pad(occ, 3), SMOOTH_SIGMA_VOX)
    verts, faces, _, _ = marching_cubes(sm, level=0.5)
    verts = (verts[:, ::-1] - 3.0) * mm_per_voxel()  # (z,y,x) -> (x,y,z), undo pad, to mm
    faces = faces.astype(np.int64)
    tri = verts[faces]
    vol = np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6
    if vol < 0:
        faces = faces[:, ::-1]
    m = mf.Manifold(mf.Mesh(vert_properties=verts.astype(np.float32), tri_verts=faces.astype(np.uint32)))
    if m.status() != mf.Error.NoError:
        raise RuntimeError(f"isosurface not a manifold: {m.status()}")
    if struts_mm:
        m = mf.Manifold.batch_boolean([m] + [orient_cylinder(a, b, STRUT_RADIUS_MM) for a, b in struts_mm], mf.OpType.Add)
    return m


def fill_cavities(m: mf.Manifold) -> tuple[mf.Manifold, dict]:
    """Drop enclosed internal void shells (negative-volume pieces of decompose()); a sealed cavity would trap resin.
    Positive pieces are kept as they are, so a multi-piece solid stays multi-piece and fails the one-body check."""
    parts = m.decompose()
    keep = [p for p in parts if p.volume() > 0]
    voids = [p for p in parts if p.volume() <= 0]
    info = {"enclosed_cavities_filled": len(voids), "cavity_volume_mm3": round(-sum(p.volume() for p in voids), 4)}
    if not voids:
        return m, info
    return (keep[0] if len(keep) == 1 else mf.Manifold.batch_boolean(keep, mf.OpType.Add)), info


def arrays(m: mf.Manifold):
    mesh = m.to_mesh()
    V = np.asarray(mesh.vert_properties)[:, :3].astype(np.float64)
    T = np.asarray(mesh.tri_verts).astype(np.int64)
    # snap to a 0.1 um grid first: vertices ~1e-5 mm apart (boolean by-products) would otherwise survive as adjacent
    # float32 values and form sub-1e-10 mm^2 slivers; validate.check re-derives closure/orientation afterwards
    V = np.round(V, 4)
    V, T, info = VAL.weld_float32(V, T)
    return V, T, info


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SIMPLIFY_MM = (1e-3, 1e-2, 5e-2)  # escalating sliver-collapse tolerances (mm), all >= 20x below the 1 mm wall rule


def export(m: mf.Manifold, path: Path, header: str, pieces_without_struts: int | None) -> dict:
    m, cav = fill_cavities(m)
    done = False
    # boolean unions and STL's float32 weld can leave sub-1e-10 mm^2 slivers: collapse short edges, and if a sliver is
    # created by float32 rounding, retry with a tiny rigid pre-shift (removed again when the part is re-zeroed)
    for off in ((0.0, 0.0, 0.0), (0.0137, 0.0291, 0.0173), (0.0211, 0.0059, 0.0263)):
        for tol in SIMPLIFY_MM:
            ms = m.simplify(tol).translate(off)
            V, T, weld = arrays(ms)
            tri = V[T]
            area = 0.5 * np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1)
            if not (area < 1e-10).any():
                done = True
                break
        if done:
            break
    weld["simplify_tolerance_mm"] = tol
    weld["pre_weld_shift_mm"] = list(off)
    V = V - V.min(axis=0)  # sit on the build plate origin
    chk = VAL.check(V, T, BOX_MM, thickness=True, min_wall_mm=MIN_WALL_MM)
    data = VAL.stl_bytes(V, T, header)
    path.write_bytes(data)
    rt = VAL.check(*VAL.read_stl(data), BOX_MM, thickness=False)
    vol_mm3 = chk["signed_volume_mm3"]
    return {"file": path.name, "bytes": len(data), "sha256": sha(path), "units": "mm",
            "weld": weld, "cavities": cav, "checks": chk, "stl_round_trip": {"closed_two_manifold": rt["closed_two_manifold"],
                                                            "consistently_oriented": rt["consistently_oriented"],
                                                            "face_connected_components": rt["face_connected_components"],
                                                            "ok": rt["ok"]},
            "watertight_and_manifold": bool(chk["closed_two_manifold"] and chk["consistently_oriented"]
                                            and rt["closed_two_manifold"] and rt["consistently_oriented"]),
            "one_connected_body": chk["face_connected_components"] == 1,
            "volume_mm3": round(vol_mm3, 2), "mass_g_at_density": round(vol_mm3 / 1000 * RESIN_DENSITY_G_CM3, 2),
            "density_g_cm3": RESIN_DENSITY_G_CM3, "density_note": "stated assumption, resin unknown",
            "biological_volume_m3": vol_mm3 * 1e-9 / DISPLAY_SCALE ** 3,
            "pieces_without_print_only_struts": pieces_without_struts}


def build_snapshot(ids: np.ndarray, types: np.ndarray, sid: str, out: Path, label: str) -> dict:
    C, cnt, ty = cell_table(ids, types)
    r_eq = (3 * cnt / (4 * math.pi)) ** (1 / 3)
    R = r_eq * CELL_RADIUS_FACTOR
    s = mm_per_voxel()
    C_mm, R_mm = C * s, R * s
    conn = connectivity(C_mm, R_mm)
    edges = strut_edges(C_mm, R_mm)
    cells = cells_solid(C_mm, R_mm, edges)
    # surface struts: connect isosurface components along the same edges (centre to centre)
    n_occ = ndimage.label(ids > 0)[1]
    surf_edges = []
    if n_occ > 1:
        lab3, _ = ndimage.label(ndimage.gaussian_filter((ids > 0).astype(np.float32), SMOOTH_SIGMA_VOX) > 0.5)
        cz = np.clip(np.round(C[:, [2, 1, 0]]).astype(int), 0, np.array(ids.shape) - 1)
        comp_of_cell = lab3[cz[:, 0], cz[:, 1], cz[:, 2]]
        # reuse cell MST edges but only those joining different isosurface pieces
        surf_edges = [(C_mm[i], C_mm[j]) for i, j in edges if comp_of_cell[i] != comp_of_cell[j]]
    surf = surface_solid(ids, surf_edges)
    out.mkdir(parents=True, exist_ok=True)
    hdr = f"xenomorph {sid} SIMULATED aggregate model, units mm, scale {DISPLAY_SCALE:g}"
    rec_cells = export(cells, out / f"{sid}-cells.stl", hdr + " cells", conn["pieces_at_chosen_radius"])
    rec_surf = export(surf, out / f"{sid}-surface.stl", hdr + " surface", int(n_occ))
    np.savez_compressed(out / f"{sid}-cells.npz", centers_mm=C_mm, radii_mm=R_mm, types=ty,
                        struts=np.array(edges, dtype=np.int32).reshape(-1, 2))
    return {"id": sid, "label": label, "n_cells": int(len(C)), "connectivity": conn,
            "print_only_struts": {"count": len(edges), "radius_mm": STRUT_RADIUS_MM,
                                  "rule": "minimum spanning tree between sphere pieces that do not overlap; print-only, not biological, not scaled"},
            "cells_solid": rec_cells, "surface_solid": rec_surf}


def choose_stages(rows: list[dict], n_cells: int) -> list[tuple[str, int]]:
    """Stage rule (declared before production fields were read): dissociated t=0; clustering = first snapshot with
    n_aggregates <= n/8; compacting = first with largest_cluster_fraction >= 0.95; compact = first with rg_norm within
    2% of the final value; sorted = final snapshot.  Duplicate times are dropped (stage is then reported merged)."""
    final = rows[-1]
    pick = [("dissociated", rows[0]["mcs"])]
    for name, cond in [("clustering", lambda r: r["n_aggregates"] <= n_cells / 8),
                       ("compacting", lambda r: r["largest_cluster_fraction"] >= 0.95),
                       ("compact", lambda r: abs(r["rg_norm"] - final["rg_norm"]) <= 0.02 * final["rg_norm"])]:
        t = next((r["mcs"] for r in rows if cond(r)), None)
        if t is not None:
            pick.append((name, t))
    pick.append(("sorted", final["mcs"]))
    seen, outl = set(), []
    for n, t in pick:
        if t not in seen:
            seen.add(t)
            outl.append((n, t))
    return outl


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fields", required=True)
    ap.add_argument("--metrics", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", default="xm")
    a = ap.parse_args(argv)
    F = np.load(a.fields)
    M = json.loads(Path(a.metrics).read_text())
    rows = M["rows"]
    avail = sorted(int(k.split("_")[1]) for k in F.files if k.startswith("ids_"))
    stages = choose_stages([r for r in rows if r["mcs"] in avail], rows[0]["n_cells_present"])
    out = Path(a.out)
    recs = []
    for i, (name, t) in enumerate(stages):
        sid = f"{a.prefix}-{i}-{name}-t{t}"
        r = build_snapshot(F[f"ids_{t}"], F[f"types_{t}"], sid, out / "stl", name)
        r["mcs"] = t
        r["metrics_at_snapshot"] = next(x for x in rows if x["mcs"] == t)
        recs.append(r)
        print(sid, "cells ok", r["cells_solid"]["checks"]["ok"], "surface ok", r["surface_solid"]["checks"]["ok"],
              "pieces", r["connectivity"]["pieces_at_chosen_radius"], "struts", r["print_only_struts"]["count"],
              "wall min", r["cells_solid"]["checks"]["wall_thickness"]["min_mm"], flush=True)
    manifest = {"schema": "frontier.xenomorph.print-manifest/1",
                "label": "Physical model of a simulated cell-aggregate morphology at display scale. Not an organism, "
                         "not a Xenobot, print preparation unvalidated (printer and resin unknown).",
                "scope": SCOPE, "printer_resin": PRINTER_RESIN,
                "run": {"command": "python -m engineering.xenomorph.printable " + " ".join(argv or []),
                        "code_sha256": sha(Path(__file__)), "fields_sha256": sha(Path(a.fields)),
                        "metrics_sha256": sha(Path(a.metrics)), "box_mm": BOX_MM, "min_wall_mm": MIN_WALL_MM,
                        "libraries": {"manifold3d": mf.__version__ if hasattr(mf, "__version__") else "3.5.4",
                                      "numpy": np.__version__}},
                "scale": {"biological_units": "m", "prop_units": "mm", "rule": "prop_mm = biological_m * 1000 * display_scale",
                          "display_scale": DISPLAY_SCALE, "voxel_length_m": H_VOXEL_M,
                          "voxel_length_note": "declared nominal assumption (no measured cell size, no frog parameter); "
                                               "the simulation itself is dimensionless",
                          "prop_mm_per_voxel": mm_per_voxel(),
                          "print_only_additions": f"connector struts r={STRUT_RADIUS_MM} mm, fixed, never scaled from biology"},
                "stage_rule": choose_stages.__doc__.strip(), "snapshots": recs,
                "files": {}}
    for r in recs:
        for k in ("cells_solid", "surface_solid"):
            manifest["files"]["stl/" + r[k]["file"]] = r[k]["sha256"]
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")


if __name__ == "__main__":
    main()
