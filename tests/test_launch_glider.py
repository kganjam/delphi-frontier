"""Launchable fish glider (SPEC-010): print requirements, controls and mutants."""
import json
import math
from pathlib import Path

import numpy as np
import pytest

from engineering.launch_glider import print_requirements as pr

ROOT = Path(__file__).resolve().parents[1]
PANELS = ROOT / "artifacts/fish3d/fish3d-v3a-fan/panels.json"
COMPS = ROOT / "artifacts/fish3d/fish3d-v3a-fan/components.json"
CARD = ROOT / "data/materials/formlabs-studio-2026-10-31.json"
MAT = {"flexural_modulus_Pa": 2.0e9, "solid_density_kg_m3": 1200.0, "ultimate_tensile_strength_Pa": 40e6}


def _rect_fin(span=0.08, chord=0.02, n=41):
    """A rectangular fin in the x-y plane: root at y = 0, chord along +x."""
    return {"fin_plane": {"origin_m": [0, 0, 0], "e_u": [0, 1, 0], "e_w": [1, 0, 0]},
            "outline_m": [[0, 0, 0], [chord, 0, 0], [chord, span, 0], [0, span, 0]],
            "area_flat_m2": span * chord}


def test_planform_matches_declared_areas_and_dihedral():
    panels = json.loads(PANELS.read_text())
    for name in ("pectoral_L", "pelvic_L"):
        pf = pr.planform(panels["fins"][name], n=401)
        assert pf["area_m2"] == pytest.approx(pf["area_declared_m2"], rel=2e-3)
    pf = pr.planform(panels["fins"]["pectoral_L"])
    assert pf["dihedral_deg"] == pytest.approx(7.0, abs=0.05)


def test_rectangle_planform_and_mac():
    pf = pr.planform(_rect_fin(), n=21)
    assert np.allclose(pf["chord_m"], 0.02) and pf["span_m"] == pytest.approx(0.08)
    m = pr.mac(pf)
    assert m["mac_m"] == pytest.approx(0.02) and m["x_ac_m"] == pytest.approx(0.005)
    assert m["span_centroid_m"] == pytest.approx(0.04)


def test_section_reduces_to_rectangle_and_parallel_axis():
    s = pr.section(0.01, 0.001, 1e-12, 1e-12)
    assert s["I_m4"] == pytest.approx(0.01 * 0.001**3 / 12, rel=1e-6)
    # membrane + spar of equal area: centroids t/2 and -h/2 -> neutral axis halfway
    c, t, ws, hs = 0.002, 0.001, 0.001, 0.002
    s = pr.section(c, t, ws, hs)
    A1, A2 = c * t, ws * hs
    yb = (A1 * t / 2 - A2 * hs / 2) / (A1 + A2)
    Iref = c * t**3 / 12 + A1 * (t / 2 - yb) ** 2 + ws * hs**3 / 12 + A2 * (hs / 2 + yb) ** 2
    assert s["I_m4"] == pytest.approx(Iref, rel=1e-12)


def test_uniform_rectangular_fin_matches_closed_form():
    """Constant chord, no spar, no inertia: tip = q L^4/(8EI), root moment = q L^2/2, sigma = M/Z."""
    pr.SCENARIO["effective_flange_over_t"]["value"] = 1e6  # full chord effective for this control
    try:
        L, c, t, p = 0.08, 0.02, 0.001, 50.0
        pf = pr.planform(_rect_fin(L, c), n=41)
        r = pr.fin_case(pf, MAT, t, 1e-9, 1e-9, p, 0.0, n_el=64)
        q, EI = p * c, MAT["flexural_modulus_Pa"] * c * t**3 / 12
        assert r["tip_m"] == pytest.approx(q * L**4 / (8 * EI), rel=1e-3)
        assert r["root_moment_N_m"] == pytest.approx(q * L * L / 2, rel=1e-4)
        assert r["sigma_root_Pa"] == pytest.approx((q * L * L / 2) / (c * t * t / 6), rel=1e-3)
    finally:
        pr.SCENARIO["effective_flange_over_t"]["value"] = 20.0


def test_inertia_load_equals_pressure_of_same_areal_weight():
    pf = pr.planform(_rect_fin(), n=41)
    t, a = 0.0005, 300.0
    r_in = pr.fin_case(pf, MAT, t, 1e-9, 1e-9, 0.0, a)
    r_p = pr.fin_case(pf, MAT, t, 1e-9, 1e-9, MAT["solid_density_kg_m3"] * t * a, 0.0)
    assert r_in["tip_m"] == pytest.approx(r_p["tip_m"], rel=1e-6)


def test_shear_lag_flange_is_conservative():
    pf = pr.planform(_rect_fin(0.08, 0.03), n=41)
    narrow = pr.fin_case(pf, MAT, 0.0005, 0.0016, 0.002, 50.0, 0.0)
    pr.SCENARIO["effective_flange_over_t"]["value"] = 1e6
    try:
        full = pr.fin_case(pf, MAT, 0.0005, 0.0016, 0.002, 50.0, 0.0)
    finally:
        pr.SCENARIO["effective_flange_over_t"]["value"] = 20.0
    assert narrow["tip_m"] > full["tip_m"] and narrow["sigma_max_Pa"] > full["sigma_max_Pa"]


def test_inplane_root_closed_form():
    pf = pr.planform(_rect_fin(0.08, 0.02), n=401)
    t, a = 0.001, 1000.0
    r = pr.inplane_root(pf, MAT, t, 1e-9, 1e-9, t, 0.0, a)
    q = MAT["solid_density_kg_m3"] * 0.02 * t * a
    M = q * 0.08**2 / 2
    assert r["moment_N_m"] == pytest.approx(M, rel=1e-4)
    assert r["sigma_Pa"] == pytest.approx(M / (t * 0.02**2 / 6), rel=1e-3)


def test_loads_and_mass_budget_arithmetic():
    ld = pr.loads(0.02)
    assert ld["V_design_m_s"] == pytest.approx(10.0)
    assert ld["a_mean_m_s2"] == pytest.approx(10.0**2 / (2 * 0.1))
    assert ld["a_peak_m_s2"] == pytest.approx(2 * ld["a_mean_m_s2"])
    assert ld["hook_force_peak_N"] == pytest.approx(0.02 * 1000.0)
    row = next(r for r in pr.mass_budget(0.00529) if r["V_m_s"] == 8.0 and r["CL_trim"] == 0.5)
    assert row["mass_max_kg"] == pytest.approx(0.5 * 1.225 * 64 * 0.5 * 0.00529 / pr.G)


def test_hook_stem_meets_allowable_exactly():
    mat = pr.load_material(CARD)
    h = pr.hook(0.02, mat, 6e-3, 4e-3)
    sig = 6 * h["design_force_N"] * 6e-3 / (4e-3 * h["min_stem_depth_m"] ** 2)
    assert sig == pytest.approx(mat["ultimate_tensile_strength_Pa"], rel=1e-9)


def test_material_card_pinned_values():
    m = pr.load_material(CARD)
    assert m["id"] == "alpha-grey-v1-default-post-cure"
    assert m["solid_density_kg_m3"] == 1220 and m["flexural_modulus_Pa"] == 2.08e9
    assert m["ultimate_tensile_strength_Pa"] == 43e6 and len(m["card_sha256"]) == 64


def test_helmbold_limits():
    assert pr.helmbold(1e6) == pytest.approx(2 * math.pi, rel=1e-5)
    assert pr.helmbold(1e-4) == pytest.approx(math.pi * 1e-4 / 2, rel=1e-3)


def test_munk_moves_np_forward_and_downwash_moves_it_forward():
    panels = json.loads(PANELS.read_text())
    pect, pelv = pr.planform(panels["fins"]["pectoral_L"]), pr.planform(panels["fins"]["pelvic_L"])
    npb = pr.neutral_point(pect, pelv, 48.7e-6, 0.0136)
    for c in npb["cases"]:
        assert c["x_np_m"] < c["x_np_fins_only_m"]
    by = {(c["downwash_deps_dalpha"], c["munk_k2_minus_k1"]): c for c in npb["cases"]}
    assert by[(0.6, 0.8)]["x_np_fins_only_m"] < by[(0.2, 0.8)]["x_np_fins_only_m"]
    assert pect["area_m2"] and npb["pectoral"]["x_ac_m"] < npb["x_np_min_m"] < npb["pelvic"]["x_ac_m"]


def test_mutant_no_pelvics_puts_np_at_pectoral_ac():
    """Removing the rear surface must collapse the fins-only NP to the pectoral a.c. (stability is lost)."""
    panels = json.loads(PANELS.read_text())
    pect = pr.planform(panels["fins"]["pectoral_L"])
    tiny = pr.planform(_rect_fin(1e-4, 1e-4), n=5)
    npb = pr.neutral_point(pect, tiny, 1e-30, 0.0136)
    assert npb["cases"][0]["x_np_fins_only_m"] == pytest.approx(npb["pectoral"]["x_ac_m"], abs=1e-6)


def test_requirements_artifact_reproduces():
    r = pr.requirements(PANELS, CARD, COMPS)
    art = json.loads((ROOT / "artifacts/launch-glider/print-requirements.json").read_text())
    assert json.loads(json.dumps(r, sort_keys=True)) == art
    pect = {s["membrane_t_m"]: s for s in r["fin_sizing"]["pectoral"]}
    assert pect[0.0005]["min_spar_h_m"] == pytest.approx(0.0012)
    rec = next(row for row in pect[0.0005]["rows"] if abs(row["spar_h_m"] - 0.002) < 1e-9)
    assert rec["pass"] and rec["worst"]["sigma_max_Pa"] < r["fin_sizing"]["pectoral"][0]["allowable_Pa"]
    bare = pect[0.0005]["rows"][0]
    assert bare["spar_h_m"] == pytest.approx(0.0004) and not bare["pass"]   # retained failing design


# ---------------------------------------------------------------- mass properties
from engineering.launch_glider import mass_props as mprops  # noqa: E402


def _box(a, b, c, o=(0.0, 0.0, 0.0)):
    """Closed, outward box [0,a]x[0,b]x[0,c] + o as 12 triangles."""
    v = np.array([[x, y, z] for x in (0, a) for y in (0, b) for z in (0, c)], float) + np.asarray(o)
    f = [(0, 1, 3), (0, 3, 2), (4, 6, 7), (4, 7, 5), (0, 4, 5), (0, 5, 1),
         (2, 3, 7), (2, 7, 6), (0, 2, 6), (0, 6, 4), (1, 5, 7), (1, 7, 3)]
    return v[np.array(f)]


def _icosphere(r, k):
    t = (1 + 5 ** 0.5) / 2
    V = [[-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0], [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
         [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
         (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10),
         (8, 6, 7), (9, 8, 1)]
    tri = np.array([[V[i] for i in f] for f in F], float)
    for _ in range(k):
        a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        tri = np.concatenate([np.stack(x, 1) for x in ((a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca))])
    return r * tri / np.linalg.norm(tri, axis=2, keepdims=True)


def test_solid_box_mass_cg_inertia_exact():
    a, b, c, rho = 0.03, 0.02, 0.01, 1220.0
    r = mprops.solid(_box(a, b, c, (0.1, -0.2, 0.05)), rho)
    m = rho * a * b * c
    assert r["mass_kg"] == pytest.approx(m, rel=1e-12)
    assert np.allclose(r["cg_m"], [0.1 + a / 2, -0.2 + b / 2, 0.05 + c / 2], atol=1e-14)
    assert np.allclose(np.diag(r["inertia_cg_kg_m2"]), [m * (b * b + c * c) / 12, m * (a * a + c * c) / 12,
                                                      m * (a * a + b * b) / 12], rtol=1e-10)


def test_sheet_box_and_sphere_shell():
    a, t, rho = 0.02, 1e-3, 1000.0
    r = mprops.sheet(_box(a, a, a), rho, t)
    m = rho * t * 6 * a * a
    assert r["mass_kg"] == pytest.approx(m) and r["area_m2"] == pytest.approx(6 * a * a)
    assert r["inertia_cg_kg_m2"][0][0] == pytest.approx(m * a * a * 5 / 18, rel=1e-10)  # thin cube shell
    R = 0.05
    s = mprops.sheet(_icosphere(R, 4), rho, t)
    assert s["inertia_cg_kg_m2"][1][1] == pytest.approx(2 / 3 * s["mass_kg"] * R * R, rel=2e-3)
    v = mprops.solid(_icosphere(R, 4), rho)
    assert v["inertia_cg_kg_m2"][2][2] == pytest.approx(0.4 * v["mass_kg"] * R * R, rel=5e-3)


def test_inverted_solid_refused_and_parallel_axis():
    with pytest.raises(ValueError):
        mprops.solid(_box(1, 1, 1)[:, ::-1], 1.0)
    c = mprops.combine([mprops.point(1.0, [1, 0, 0]), mprops.point(1.0, [-1, 0, 0])])
    assert np.allclose(np.diag(c["inertia_cg_kg_m2"]), [0, 2, 2])


# ---------------------------------------------------------------- dynamics controls and mutants
from engineering.launch_glider import dynamics as dyn  # noqa: E402
from engineering.simulation import glide  # noqa: E402

BASE = dict(m=0.012, Iyy=2.4e-5, x_cg=0.052, z_cg=0.0, S=0.005293, c=0.0265, AR=7.4, vol=48.7e-6, x_np=0.060)


def _trimmed(cl=0.5, **kw):
    p = dyn.Params(**{**BASE, **kw}).broadcast(1)
    p.Cm0 = np.array([dyn.cm0_for_trim(p, cl)])
    return p


def test_vacuum_projectile_closed_form():
    n = 4
    p = dyn.Params(**BASE, lift=0.0, drag=0.0).broadcast(n)
    V0, g0, h = np.array([4.0, 6.0, 8.0, 8.0]), np.radians([0, 20, 45, -10]), 1.35
    y0 = np.stack([np.zeros(n), np.full(n, h), g0, V0 * np.cos(g0), V0 * np.sin(g0), np.zeros(n)])
    r = dyn.fly(p, y0, dt=1e-3)
    R = V0 * np.cos(g0) * (V0 * np.sin(g0) + np.sqrt((V0 * np.sin(g0)) ** 2 + 2 * dyn.G * h)) / dyn.G
    assert np.allclose(r["range_m"], R, rtol=1e-6)


def test_lift_does_no_work_without_drag():
    p = _trimmed(drag=0.0)
    y0 = np.array([[0.0], [1.4], [0.3], [6.0], [0.5], [2.0]])
    r = dyn.fly(p, y0, dt=2e-4, record_every=1)
    h = r["history_first_draw"]
    E = 0.5 * (h[:, 4] ** 2 + h[:, 5] ** 2) + dyn.G * h[:, 2]
    assert np.ptp(E) / E[0] < 1e-6


def test_trimmed_3dof_equals_glide_point_mass():
    p = _trimmed(0.5)
    t = dyn.trim(p, 0.5)
    y = dyn.trim_state(p, 0.5, Z=1.35)
    dy, _ = dyn.rhs(p, y)
    assert np.allclose(dy[3:, 0], 0, atol=1e-9)
    r = dyn.fly(p, y, dt=1e-3)
    g = glide.integrate(0.012, 0.005293, 7.4, 1.225, t["CL"], 0.06, 0.8, 1.35, t["V_m_s"], gam0=t["gamma_rad"])
    assert r["range_m"][0] == pytest.approx(float(g["range_m"][0]), rel=1e-6)
    assert math.tan(-t["gamma_rad"]) == pytest.approx(t["CD"] / t["CL"], rel=1e-12)


def test_dt_halving_converges():
    p = _trimmed(0.5).broadcast(1)
    y0 = np.array([[0.0], [1.35], [0.25], [7.0], [1.0], [0.0]])
    r1, r2 = dyn.fly(p, y0, dt=2e-3), dyn.fly(p, y0, dt=1e-3)
    assert abs(r1["range_m"][0] / r2["range_m"][0] - 1) < 5e-3


def test_modes_stable_with_margin_and_unstable_when_cg_behind_np():
    p = _trimmed(0.5)
    md = dyn.jacobian_modes(p, dyn.trim_state(p, 0.5))
    assert md["max_real"] <= 1e-9 and md["short_period"].real < 0
    bad = _trimmed(0.5, x_cg=0.070)       # mutant: CG 10 mm behind the fins' NP
    mb = dyn.jacobian_modes(bad, dyn.trim_state(bad, 0.5))
    assert mb["max_real"] > 0.5


def test_linearisation_matches_nonlinear_small_perturbation():
    """x(t) = expm(J t) dx0 against the nonlinear run from the same small pitch-rate kick (first 1 s)."""
    from scipy.linalg import expm
    p = _trimmed(0.5)
    y_t = dyn.trim_state(p, 0.5, Z=50.0)
    md = dyn.jacobian_modes(p, y_t)
    dx0 = np.zeros((6, 1))
    dx0[5, 0] = 0.05
    r = dyn.fly(p, y_t + dx0, dt=2e-4, t_max=1.0, record_every=50)
    h = r["history_first_draw"]
    q_nl = h[:, 6]
    q_lin = np.array([(expm(md["J"] * t) @ dx0)[5, 0] for t in h[:, 0]])
    assert np.max(np.abs(q_nl - q_lin)) < 0.02 * np.max(np.abs(q_lin))
    assert md["short_period"].real < 0 and md["phugoid"].real < 0


def test_stroke_closed_form_constant_force(monkeypatch):
    monkeypatch.setattr(dyn, "G", 0.0)
    p = dyn.Params(**BASE, lift=0.0, drag=0.0).broadcast(3)
    L = dyn.Launch(V0=[4.0, 6.0, 8.0], stroke=[0.1, 0.2, 0.3], phi=0.0, profile=0, xi_h=0.025, zeta_h=0.0)
    st = dyn.stroke(p, L, 3, dt=2e-5)
    assert np.allclose(st["V_release_m_s"], [4, 6, 8], rtol=2e-3)
    assert np.allclose(st["a_mean_m_s2"], st["a_mean_formula_m_s2"], rtol=1e-3)
    assert np.allclose(st["t_release_s"], 2 * np.array([0.1, 0.2, 0.3]) / np.array([4, 6, 8]), rtol=3e-3)
    assert np.allclose(st["q_release_rad_s"], 0, atol=1e-9)        # line of action through the CG


@pytest.mark.parametrize("profile,ratio", [(0, 1.0), (1, math.pi / 2), (2, 2.0)])
def test_stroke_peak_over_mean(monkeypatch, profile, ratio):
    monkeypatch.setattr(dyn, "G", 0.0)
    p = dyn.Params(**BASE, lift=0.0, drag=0.0).broadcast(1)
    st = dyn.stroke(p, dyn.Launch(V0=6.0, stroke=0.2, phi=0.0, profile=profile), 1, dt=2e-5)
    assert st["a_peak_m_s2"][0] / st["a_mean_m_s2"][0] == pytest.approx(ratio, rel=2e-3)
    assert st["V_release_m_s"][0] == pytest.approx(6.0, rel=2e-3)


def test_hook_ahead_self_aligns_hook_behind_does_not(monkeypatch):
    """Pull from ahead of the CG restores a misalignment; the mutant hook behind the CG amplifies it."""
    monkeypatch.setattr(dyn, "G", 0.0)
    p = dyn.Params(**BASE, lift=0.0, drag=0.0).broadcast(2)
    L = dyn.Launch(V0=8.0, stroke=0.3, phi=0.0, delta=np.radians(3.0), profile=0, xi_h=[0.025, -0.025])
    st = dyn.stroke(p, L, 2, dt=2e-5)
    th = np.degrees(st["theta_release_rad"])
    assert abs(th[0]) <= 3.0 + 1e-6
    assert abs(th[1]) > 3.0


def test_hook_below_cg_sets_release_attitude(monkeypatch):
    """Under tension the CG lies on the band line, so a hook zeta below the CG holds the nose up by atan(-zeta/xi).

    Started at that attitude the body stays there (equilibrium); started level it swings about it."""
    monkeypatch.setattr(dyn, "G", 0.0)
    p = dyn.Params(**BASE, lift=0.0, drag=0.0).broadcast(2)
    th_eq = math.atan(0.002 / 0.025)
    L = dyn.Launch(V0=6.0, stroke=0.2, phi=0.0, delta=[th_eq, 0.0], profile=0, xi_h=0.025, zeta_h=-0.002)
    st = dyn.stroke(p, L, 2, dt=5e-5)
    assert st["theta_release_rad"][0] == pytest.approx(th_eq, abs=1e-6)
    assert abs(st["q_release_rad_s"][0]) < 1e-5
    assert 0.0 < st["theta_release_rad"][1] <= 2 * th_eq + 1e-6


def test_ballistic_control_has_no_rotation():
    p = dyn.Params(**BASE, lift=0.0, cd_ballistic=0.07).broadcast(1)
    y0 = np.array([[0.0], [1.35], [0.2], [8.0], [1.0], [0.0]])
    r = dyn.fly(p, y0, dt=1e-3, record_every=1)
    assert np.allclose(r["history_first_draw"][:, 3], 0.2)
    rv = dyn.fly(dyn.Params(**BASE, lift=0.0, drag=0.0).broadcast(1), y0, dt=1e-3)
    assert r["range_m"][0] < rv["range_m"][0]


# ---------------------------------------------------------------- placeholder candidate from v3a meshes
from engineering.launch_glider import candidate as cand  # noqa: E402


def test_candidate_from_v3a_meshes():
    mat = pr.load_material(CARD)
    c = cand.build(0.053, mat, root=ROOT)
    assert c["assembled"]["cg_m"][0] == pytest.approx(0.053, abs=1e-12)
    tot = sum(v["mass_kg"] for v in c["parts"].values())
    assert c["assembled"]["mass_kg"] == pytest.approx(tot, rel=1e-12)
    body = mprops.read_stl(ROOT / "artifacts/fish3d/fish3d-v3a-fan/components/body.stl")
    A = 0.5 * np.linalg.norm(np.cross(body[:, 1] - body[:, 0], body[:, 2] - body[:, 0]), axis=1).sum()
    assert c["parts"]["body_shell"]["mass_kg"] == pytest.approx(1220 * 0.8e-3 * A, rel=1e-12)
    hull = np.asarray(c["contacts_xz_m"])
    assert hull[:, 1].min() == pytest.approx(-0.029, abs=5e-4)      # caudal lower lobe is the lowest point
    assert hull[:, 0].min() == pytest.approx(0.0, abs=1e-4)         # snout
    with_ballast = cand.build(0.080, mat, root=ROOT)                # target behind the dry CG
    assert with_ballast["ballast_status"] == "NO_BALLAST_NEEDED_CG_AHEAD_OF_TARGET"


def test_munk_couple_is_destabilising_by_exactly_2_vol_k():
    a = np.radians([-1.0, 1.0])
    V, q = np.full(2, 8.0), np.zeros(2)
    with_body = dyn.aero(dyn.Params(**BASE).broadcast(2), a, V, q)[3]
    no_body = dyn.aero(dyn.Params(**{**BASE, "vol": 0.0}).broadcast(2), a, V, q)[3]
    d = (with_body - no_body)
    slope = (d[1] - d[0]) / (a[1] - a[0])
    assert slope == pytest.approx(2 * BASE["vol"] * 0.9 * math.cos(2 * a[1]) * 1.0, rel=1e-3)
    assert slope > 0


# ---------------------------------------------------------------- feasibility sweep
from engineering.launch_glider import sweep as sw  # noqa: E402

SMALL = {"x_np_m": {"values": [0.066]}, "t_body_m": {"values": [0.5e-3]}, "CL_trim": {"values": [0.45, 0.6]},
         "V0_m_s": {"values": [8.0]}, "phi_deg": {"values": [0.0]}, "hook_zeta_m": {"values": [0.0]},
         "hook_xi_m": {"values": [0.025]}}


def test_sweep_retains_failed_trim_and_runs_controls():
    r = sw.run(ROOT, CARD, grid=SMALL)
    assert [f["status"] for f in r["failed_designs"]] == ["TRIM_ABOVE_CL_PEAK"]     # retained, not dropped
    (row,) = r["rows"]
    assert row["static_margin"] == pytest.approx(sw.SM_TARGET, abs=1e-9)
    assert row["release"]["V_m_s"] == pytest.approx(8.0, rel=2e-3)
    assert row["glide_gain_m"] == pytest.approx(row["flight"]["range_m"] - row["no_lift_control"]["range_m"])
    assert row["modes"]["max_real"] <= 1e-9
    assert r["unreleased"] == 0 and r["airborne_at_t_max"] == 0


def test_sweep_dt_halving_on_one_row():
    a = sw.run(ROOT, CARD, grid={**SMALL, "CL_trim": {"values": [0.45]}})
    b = sw.run(ROOT, CARD, grid={**SMALL, "CL_trim": {"values": [0.45]}}, dt_stroke=5e-5, dt_fly=5e-4)
    assert abs(a["rows"][0]["flight"]["range_m"] / b["rows"][0]["flight"]["range_m"] - 1) < 5e-3
