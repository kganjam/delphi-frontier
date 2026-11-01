"""Read claude-05's `frontier.glider.flight-model/1` records, recompute their mass properties from the STL bytes,
check the as-built fin and catch sections against requirements R1-R3, and fly the result (sweep.simulate).

    python -m engineering.launch_glider.flight_model <commit> artifacts/launch-glider/r1-dynamics.json

The STLs are read from git at a pinned commit (`git show <commit>:<path>`), so the result names the exact bytes.
Every part's sha256 must match its record, and the recomputed mass and CG must agree with claude-05's within
TOLERANCE or the record is refused: the two computations are independent (claude-05's builder, this
module's signed-tetrahedron integrals), so agreement is a check on both.
Nothing here is printed, weighed or flown; the aero is the same nominal scenario set as the placeholder map.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

from . import candidate as cd
from . import mass_props as mp
from . import print_requirements as pr
from . import sweep as sw

SCHEMA = "frontier.glider.flight-model/1"
TOLERANCE = {"mass_rel": 0.005, "cg_m": 0.5e-3}
REVISIONS = ("artifacts/glider/r1-light", "artifacts/glider/r1-strong")
K_Z = {"values": [1.0, 0.5], "status": "declared strength knockdown for stress across print layers (orientation case); "
                                     "not measured for this resin or printer"}
SHOT_NOTE = "ballast from claude-05's bay fill model (packed from the front, shot density assumed by claude-05)"


def git_source(repo: Path, commit: str, base: str):
    """rel path -> bytes at `commit:base/rel`."""
    def read(rel: str) -> bytes:
        return subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{base}/{rel}"], check=True,
                              capture_output=True).stdout
    return read


def load(read) -> dict:
    rec = json.loads(read("flight_model.json"))
    if rec.get("schema") != SCHEMA:
        raise ValueError(f"schema {rec.get('schema')!r} is not {SCHEMA}")
    return rec


def _fish_triangles(read, part: dict) -> np.ndarray:
    b = read(part["stl"])
    got = hashlib.sha256(b).hexdigest()
    if got != part["stl_sha256"]:
        raise ValueError(f"{part['stl']}: sha256 {got} does not match the record's {part['stl_sha256']}")
    tri = mp.parse_stl(b, part["stl"])
    T = np.asarray(part["print_to_fish_transform_mm"], float)
    P = tri.reshape(-1, 3) @ T[:3, :3].T + T[:3, 3]
    P = P.reshape(-1, 3, 3) * 1e-3
    if np.linalg.det(T[:3, :3]) < 0:   # a mirror (the right-side fins) reverses the winding
        P = P[:, [0, 2, 1]]
    return P


def recompute(rec: dict, read, mat: dict) -> dict:
    """Independent mass, CG and inertia of every nominal part (closed solids at the card density)."""
    rho = mat["solid_density_kg_m3"]
    if abs(rec["material"]["density_kg_m3"] - rho) > 1e-9:
        raise ValueError(f"record density {rec['material']['density_kg_m3']} is not the card's {rho}")
    parts, rows, verts = [], [], []
    for p in rec["parts"]:
        tri = _fish_triangles(read, p)
        s = mp.solid(tri, rho)
        dm = s["mass_kg"] / p["mass_kg"] - 1
        dcg = float(np.linalg.norm(np.subtract(s["cg_m"], p["cg_m"])))
        rows.append({"id": p["id"], "stl_sha256": p["stl_sha256"], "mass_kg": s["mass_kg"], "cg_m": s["cg_m"],
                     "volume_m3": s["volume_m3"], "declared_mass_kg": p["mass_kg"], "mass_rel_diff": dm,
                     "cg_diff_m": dcg})
        parts.append(s)
        verts.append(tri.reshape(-1, 3))
    dry = mp.combine(parts)
    d = rec["assembled_dry"]
    dm = dry["mass_kg"] / d["mass_kg"] - 1
    dcg = float(np.linalg.norm(np.subtract(dry["cg_m"], d["cg_m"])))
    dI = float(np.max(np.abs(np.subtract(dry["inertia_cg_kg_m2"], d["inertia_cg_kg_m2"])))
               / np.max(np.abs(d["inertia_cg_kg_m2"])))
    spares = {}
    for p in rec.get("spare_parts", []):   # alternative parts (pelvic keys, catch plugs): bytes and props checked too
        s = mp.solid(_fish_triangles(read, p), rho)
        rows.append({"id": p["id"], "spare": True, "stl_sha256": p["stl_sha256"], "mass_kg": s["mass_kg"],
                     "cg_m": s["cg_m"], "volume_m3": s["volume_m3"], "declared_mass_kg": p["mass_kg"],
                     "mass_rel_diff": s["mass_kg"] / p["mass_kg"] - 1,
                     "cg_diff_m": float(np.linalg.norm(np.subtract(s["cg_m"], p["cg_m"])))})
        spares[p["id"]] = s
    worst_m = max(abs(r["mass_rel_diff"]) for r in rows + [{"mass_rel_diff": dm}])
    worst_cg = max(r["cg_diff_m"] for r in rows + [{"cg_diff_m": dcg}])
    ok = worst_m <= TOLERANCE["mass_rel"] and worst_cg <= TOLERANCE["cg_m"]
    return {"status": "AGREES" if ok else "DISAGREES", "tolerance": TOLERANCE, "parts": rows, "dry": dry,
            "_props": {p["id"]: s for p, s in zip(rec["parts"], parts)} | {k: v for k, v in spares.items()},
            "dry_mass_rel_diff": dm, "dry_cg_diff_m": dcg, "dry_inertia_max_rel_diff": dI,
            "method": "signed-tetrahedron integrals (mass_props.solid) on the STL bytes after the record's "
                      "print_to_fish transform", "_verts": np.concatenate(verts)}


def assembly(rec: dict, rc: dict, plug: str | None = "nominal") -> dict:
    """Dry assembly with the nominal catch plug swapped for `plug` (a spare plug id, or None for the bare slot top)."""
    if plug == "nominal":
        return rc["dry"]
    ids = [p["id"] for p in rec["parts"] if not p["id"].startswith("catch_plug")]
    return mp.combine([rc["_props"][i] for i in ids] + ([rc["_props"][plug]] if plug else []))


def surface(rec: dict, sid: str) -> dict:
    """A record lifting surface (left side) in print_requirements.planform's input form."""
    s = next(x for x in rec["lifting_surfaces"] if x["id"] == sid)
    f = s["frame_L"]
    o, eu, ew = (np.asarray(v, float) for v in (f["origin_mm"], f["e_u"], f["e_w"]))
    uw = np.asarray(s["outline_uw_mm"], float)
    P = (o + uw[:, :1] * eu + uw[:, 1:] * ew) * 1e-3
    x, y = uw[:, 0], uw[:, 1]
    area = 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))) * 1e-6
    return {"fin_plane": {"origin_m": (o * 1e-3).tolist(), "e_u": eu.tolist(), "e_w": ew.tolist()},
            "outline_m": P.tolist(), "area_flat_m2": area, "_record": s}


def _spar(surf: dict, pf: dict):
    """(width, hs(s)) of the leading-edge spar ridge, heights interpolated along its polyline's span coordinate."""
    r = next(x for x in surf["_record"]["ridges"] if x["role"] == "leading-edge spar")
    u = np.asarray(r["polyline_uw_mm"], float)[:, 0] * 1e-3
    h = np.asarray(r["height_mm"], float) * 1e-3
    u0 = (np.asarray(surf["outline_m"]) - surf["fin_plane"]["origin_m"]) @ np.asarray(surf["fin_plane"]["e_u"])
    s_of_u = u - float(u0.min())
    return r["width_mm"] * 1e-3, (lambda s: float(np.interp(s, s_of_u, h))), {"s_m": s_of_u.tolist(),
                                                                             "h_m": h.tolist()}


def fin_check(rec: dict, mat: dict, m_kg: float, S_paired: float) -> dict:
    """Requirement R1/R2 checks on the as-built sections (spar taper included, other ridges ignored, the
    doubler's 12-16 mm taper counted as bare membrane: both conservative)."""
    ld = pr.loads(m_kg)
    allow = mat["ultimate_tensile_strength_Pa"] / pr.SCENARIO["strength_safety_factor"]["value"]
    out = {}
    for sid in ("pectoral", "pelvic"):
        surf = surface(rec, sid)
        pf = pr.planform(surf)
        ws, hs, prof = _spar(surf, pf)
        s = surf["_record"]
        t, d = s["membrane_mm"] * 1e-3, s["root_doubler"]
        kw = dict(t_root=d["thickness_mm"] * 1e-3, root_len=d["full_to_u_mm"] * 1e-3)
        w = pr.fin_case(pf, mat, t, ws, hs, ld["p_worst_Pa"], ld["a_normal_to_fin_m_s2"], **kw)
        cr = pr.fin_case(pf, mat, t, ws, hs, m_kg * pr.G / S_paired, 0.0, **kw)
        ip = pr.inplane_root(pf, mat, t, ws, hs(0.0), kw["t_root"], kw["root_len"], ld["a_peak_m_s2"])
        lim = pr.SCENARIO["tip_deflection_over_span_cruise_max"]["value"]
        out[sid] = {"area_flat_m2": surf["area_flat_m2"], "span_m": pf["span_m"], "spar_w_m": ws,
                    "spar_h_profile": prof, "membrane_t_m": t, "root_doubler": d, "worst": w, "cruise": cr,
                    "inplane_root": ip, "allowable_Pa": allow,
                    "pass": bool(w["sigma_max_Pa"] <= allow and ip["sigma_Pa"] <= allow
                                 and w["small_deformation"]["valid"] and cr["tip_over_span"] <= lim),
                    "stress_pass_by_k_z": {str(k): bool(max(w["sigma_max_Pa"], ip["sigma_Pa"]) <= k * allow)
                                           for k in K_Z["values"]}}
    return {"mass_case_kg": m_kg, "loads": ld, "fins": out}


def catch_check(rec: dict, verts: np.ndarray, mat: dict, m_kg: float) -> dict:
    """The r1 catch is a liner wall (thickness t_x) across the body: the band force must leave it through its
    bond to the shell. Required bonded perimeter at an allowable shear of UTS/2/SF, against the body's local
    perimeter estimated as pi*(w+d)/2 from the mesh's extent within 1 mm of the seat."""
    sf = pr.SCENARIO["strength_safety_factor"]["value"]
    F = pr.loads(m_kg)["hook_force_peak_N"]
    L = rec["launch"]
    b = L["boss_section"]
    t = b.get("thickness_x_mm", b.get("thickness_mm")) * 1e-3
    xs = [L["seat_mm"][0]] if "seat_mm" in L else sorted({s["seat_mm"][0] for s in L["seats"]})

    def extent(x):
        near = verts[np.abs(verts[:, 0] - x * 1e-3) < 1e-3]
        return float(near[:, 1].max() - near[:, 1].min()), float(near[:, 2].max() - near[:, 2].min())
    x = min(xs, key=lambda v: sum(extent(v)))   # the narrowest seat station governs
    w, dpt = extent(x)
    x *= 1e-3
    tau = 0.5 * mat["ultimate_tensile_strength_Pa"] / sf
    p_need = F / (t * tau)
    p_have = math.pi * (w + dpt) / 2
    bearing = F / (2 * L["contact_radius_mm"] * 1e-3 * w)
    return {"peak_force_N": F, "design_force_N": sf * F, "wall_t_m": t, "seat_x_m": x, "body_width_at_seat_m": w,
            "body_depth_at_seat_m": dpt, "allowable_shear_Pa": tau, "bond_perimeter_needed_m": p_need,
            "bond_perimeter_estimate_m": p_have, "bearing_Pa_on_seat": bearing,
            "pass": bool(p_have >= p_need),
            "pass_by_k_z": {str(k): bool(p_have >= p_need / k) for k in K_Z["values"]},
            "rule": "tau = F / (P t) <= 0.5 UTS / SF; mesh extent is the outer body at the seat, not the liner"}


def ballast_point(rec: dict, m_b: float) -> list:
    rows = sorted((r for r in rec["ballast"]["rows"] if r["feasible"]), key=lambda r: r["ballast_g"])
    g = [r["ballast_g"] * 1e-3 for r in rows]
    return [float(np.interp(m_b, g, [r["fill_centroid_mm"][k] * 1e-3 for r in rows])) for k in range(3)]


def candidate(rec: dict, rc: dict, x_cg_target: float | None, dry: dict | None = None) -> dict:
    """A sweep candidate: the recomputed dry assembly (or `dry`, e.g. another catch plug) plus the ballast that puts
    the CG at x_cg_target (None or a target behind the dry CG: no ballast)."""
    if rc["status"] != "AGREES":
        raise ValueError("refused: recomputed mass properties disagree with the record")
    dry = dry or rc["dry"]
    mmax = rec["ballast"]["mass_range_kg"][1]
    status, mb = "ok", 0.0
    if x_cg_target is None or x_cg_target >= dry["cg_m"][0]:
        status = "NO_BALLAST_NEEDED_CG_AHEAD_OF_TARGET" if x_cg_target is not None else "DRY"
    else:
        def x_of(m):
            return mp.combine([dry, mp.point(m, ballast_point(rec, m))])["cg_m"][0]
        if x_of(mmax) > x_cg_target:
            status, mb = "BALLAST_BAY_CANNOT_REACH", mmax
        else:
            lo, hi = 0.0, mmax
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if x_of(mid) > x_cg_target else (lo, mid)
            mb = 0.5 * (lo + hi)
    tot = mp.combine([dry, mp.point(mb, ballast_point(rec, mb))]) if mb > 0 else dry
    pect, pelv = surface(rec, "pectoral"), surface(rec, "pelvic")
    S_paired = 2 * (pect["area_flat_m2"] + pelv["area_flat_m2"])
    pfp = pr.planform(pect)
    span = 2 * float(np.max(np.abs(np.asarray(pect["outline_m"])[:, 1])))
    hull = cd.hull_xz(rc["_verts"][:, [0, 2]])
    return {"evidence_kind": "derived_estimate", "source": f"claude-05 {rec['revision']} STL bytes, recomputed here",
            "revision": rec["revision"], "candidate_sha256": rec["candidate_sha256"], "dry": dry,
            "ballast_kg": mb, "ballast_status": status, "assembled": tot, "contacts_xz_m": hull.tolist(),
            "S_paired_m2": S_paired, "span_m": span, "mac_m": pr.mac(pfp)["mac_m"],
            "AR_total": span * span / S_paired}


def hand_np(rec: dict) -> dict:
    pect, pelv = pr.planform(surface(rec, "pectoral")), pr.planform(surface(rec, "pelvic"))
    b = rec["body"]
    return pr.neutral_point(pect, pelv, b["enclosed_volume_m3"], b["max_width_m"] / 2)


# ---------------------------------------------------------------- the r1 sweep
GRID_R1 = {
    "x_np_m": {"values": [0.0567, 0.060, 0.066, 0.072],
               "status": "56.7 mm = midpoint of the hand Helmbold+Munk bracket on r1's surfaces (54.5-59.0); 60 mm = "
                         "fins-only hand NP; 66 and 72 mm = aft scenarios (Park & Choi x_CG/SL 0.39-0.44); the VLM "
                         "(cfd04) replaces all four"},
    "CL_trim": {"values": [0.3, 0.45, 0.6], "status": "decalage design choice (sets Cm0)"},
    "V0_m_s": {"values": [4.0, 6.0, 8.0, 10.0, 12.0],
               "status": "4/6/8 are SPEC-010 rule 3; 10 and 12 are added beyond SPEC-010 to locate where gliding starts"},
    "phi_deg": {"values": [0.0, 15.0, 30.0], "status": "declared launch pitch (band elevation)"},
    "catch": {"values": ["r1-as-built"] + [f"r2 xi{xi:g} zeta{z:+g}" for xi in (25, 40) for z in (-1.5, 0.0, 1.5, 3.0)],
              "status": "r1-as-built = the record's seat (x, z), so its offset from the ballasted CG varies by draw; "
                        "r2 = claude-05's adjustable plugs/slots, xi mm ahead of and zeta mm above that draw's CG"},
}


def catches(rec: dict, G_: dict) -> list[tuple[str, object]]:
    """(label, plug) per catch option. A record with launch.seats[] (r2 on) has body-fixed seats, one per slot and
    offset, each with its own plug (None = bare slot top); otherwise the grid's labels with the nominal assembly."""
    seats = rec["launch"].get("seats")
    if not seats:
        return [(c, "nominal") for c in G_["catch"]["values"]]
    return [(f"slot x{s['slot_x_mm']:g} dz{s['offset_from_design_cg_z_mm']:+g}", s["plug"]) for s in seats]


def _catch(label: str, rec: dict, cg) -> tuple[float, float]:
    seat = next((s["seat_mm"] for s in rec["launch"].get("seats", [])
                 if f"slot x{s['slot_x_mm']:g} dz{s['offset_from_design_cg_z_mm']:+g}" == label), None)
    if seat is not None:   # body-fixed seat: its offset from this draw's CG
        x, z = (v * 1e-3 for v in seat)
        return cg[0] - x, z - cg[2]
    if label == "r1-as-built":
        x, z = (v * 1e-3 for v in rec["launch"]["seat_mm"])
        return cg[0] - x, z - cg[2]
    xi, z = label.split()[1:]
    return float(xi[2:]) * 1e-3, float(z[4:]) * 1e-3


def run(repo: Path, commit: str, card: Path, grid: dict | None = None, revisions=REVISIONS,
        dt_stroke=1e-4, dt_fly=1e-3) -> dict:
    G_ = grid or GRID_R1
    mat = pr.load_material(card)
    recs, rows, cands, checks = {}, [], [], {}
    for base in revisions:
        read = git_source(repo, commit, base)
        rec = load(read)
        rc = recompute(rec, read, mat)
        recs[rec["revision"]] = (rec, rc)
        np_b = hand_np(rec)
        dry = candidate(rec, rc, None)
        non_mesh = sum(nm.get("mass_kg_range", [0, 0])[1] for nm in rec["non_mesh"])
        by_np = {x_np: candidate(rec, rc, x_np - sw.SM_TARGET * dry["mac_m"]) for x_np in G_["x_np_m"]["values"]}
        m_dry = dry["dry"]["mass_kg"] + non_mesh
        m_ballasted = max(c["assembled"]["mass_kg"] for c in by_np.values()) + non_mesh
        checks[rec["revision"]] = {
            "record": {"path": f"{base}/flight_model.json", "sha256": hashlib.sha256(read("flight_model.json")).hexdigest(),
                       "commit": commit, "candidate_sha256": rec["candidate_sha256"], "label": rec["label"]},
            "recompute": {k: v for k, v in rc.items() if not k.startswith("_")},
            "hand_np": np_b,
            "structure": {case: {"mass_kg": m, "fin": fin_check(rec, mat, m, dry["S_paired_m2"]),
                                 "catch": catch_check(rec, rc["_verts"], mat, m)}
                          for case, m in (("dry_plus_non_mesh", m_dry),
                                          ("heaviest_swept_ballast_plus_non_mesh", m_ballasted))},
        }
        opts = catches(rec, G_)
        for (x_np, c0), (catch, plug) in itertools.product(by_np.items(), opts):
            c = c0 if plug == "nominal" else candidate(rec, rc, x_np - sw.SM_TARGET * dry["mac_m"],
                                                       assembly(rec, rc, plug))
            for cl, V0, phi in itertools.product(G_["CL_trim"]["values"], G_["V0_m_s"]["values"],
                                                 G_["phi_deg"]["values"]):
                cg = c["assembled"]["cg_m"]
                xi, zeta = _catch(catch, rec, cg)
                rows.append({"revision": rec["revision"], "x_np_m": x_np, "CL_trim": cl, "V0_m_s": V0,
                             "phi_deg": phi, "catch": catch, **({"plug": plug} if plug != "nominal" else {}), "hook_xi_m": xi, "hook_zeta_m": zeta,
                             "x_cg_m": cg[0], "z_cg_m": cg[2], "mass_kg": c["assembled"]["mass_kg"],
                             "ballast_kg": c["ballast_kg"], "ballast_status": c["ballast_status"],
                             "Iyy_kg_m2": c["assembled"]["inertia_cg_kg_m2"][1][1]})
                cands.append(c)
    vol = next(iter(recs.values()))[0]["body"]["enclosed_volume_m3"]
    sim = sw.simulate(rows, cands, vol, dt_stroke, dt_fly)
    return {"schema": "frontier.glider.r1-dynamics/1", "evidence_kind": "simulated_scenario",
            "inputs": {"commit": commit, "revisions": list(revisions),
                       "material": {k: mat[k] for k in ("id", "card_path", "card_sha256")}},
            "checks": checks, "grid": G_, "fixed": sw.FIXED, "sm_target": sw.SM_TARGET,
            "aero_nominal": cd.AERO_NOMINAL, "ballast_model": SHOT_NOTE,
            "dt": {"stroke_s": dt_stroke, "flight_s": dt_fly}, **sim,
            "limits": ["claude-05's r1 bytes as recorded, not a print: no printed mass, shrinkage, support scars or glue",
                       "nominal scenario coefficients; NP is a scenario axis, not a VLM result",
                       "pitch plane only: no roll, yaw, sideslip or spiral modes",
                       "launcher speed, force profile and alignment are chosen scenarios, not measurements",
                       "no ground effect, no wall/ceiling, still air"]}


def main(argv):
    commit, out = argv[1], Path(argv[2])
    r = run(Path("."), commit, Path("data/materials/formlabs-studio-2026-10-31.json"),
            revisions=tuple(argv[3:]) or REVISIONS)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=1, sort_keys=True, default=float) + "\n")
    print(out, hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main(sys.argv)
