"""Checks of the xenomorph measurement and print code on synthetic fields with known answers (no simulation run)."""
import numpy as np
import pytest

mf = pytest.importorskip("manifold3d")
pytest.importorskip("skimage")

from engineering.xenomorph import analyze as A  # noqa: E402
from engineering.xenomorph import cpm_model as CM  # noqa: E402
from engineering.xenomorph import printable as P  # noqa: E402


def two_blocks(gap: int):
    ids = np.zeros((20, 20, 30), np.int64)
    ids[5:15, 5:15, 3:13] = 1
    ids[5:15, 5:15, 13 + gap:23 + gap] = 2
    types = np.where(ids > 0, 1, 0)
    return ids, types


def test_touching_cells_are_one_aggregate_and_separate_are_two():
    m = A.measure(*two_blocks(0), type_a=1, n_expected=2)
    assert m["n_aggregates"] == 1 and m["largest_cluster_fraction"] == 1.0
    assert m["contact_area_cell_cell"] == 100  # 10 x 10 shared faces
    m2 = A.measure(*two_blocks(2), type_a=1, n_expected=2)  # negative control
    assert m2["n_aggregates"] == 2 and m2["contact_area_cell_cell"] == 0


def test_core_shell_sign():
    ids = np.zeros((31, 31, 31), np.int64)
    z, y, x = np.indices(ids.shape) - 15
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    ids[r <= 6] = 1
    ids[(r > 6) & (r <= 10)] = 2
    types = ids.copy()
    assert A.measure(ids, types, type_a=1, n_expected=2)["core_shell_index"] > 0.3
    assert A.measure(ids, types, type_a=2, n_expected=2)["core_shell_index"] < -0.3  # swapped labels flip sign


def test_lattice_placement_has_no_contacts_at_t0():
    P_, t = CM.place_cells_lattice(128, 4.0, 1.0, 0.5, 50.0, seed=3, frac_a=0.5)
    d = np.linalg.norm(P_[:, None] - P_[None], axis=2) + np.eye(128) * 1e9
    assert d.min() >= 2 * 4.0 + 1.0 - 1e-9
    assert (t == "A").sum() == 64


def test_neck_rule_and_struts_make_one_body():
    C = np.array([[0.0, 0, 0], [10.0, 0, 0], [30.0, 0, 0]])  # third sphere far away
    R = np.array([6.0, 6.0, 6.0])
    conn = P.connectivity(C, R)
    assert conn["pieces_at_chosen_radius"] == 2 and not conn["one_body_without_struts"]
    edges = P.strut_edges(C, R)
    assert len(edges) == 1
    m, _ = P.fill_cavities(P.cells_solid(C, R, edges))
    assert len(m.decompose()) == 1
    m0 = P.cells_solid(C, R, [])  # negative control: without struts it is two pieces
    assert len(m0.decompose()) == 2


def test_radius_factor_needed_gives_required_neck():
    C = np.array([[0.0, 0, 0], [14.0, 0, 0]])
    R = np.array([6.0, 6.0])
    k = P.connectivity(C, R)["radius_factor_needed_to_join_all"]
    h = P.neck_radius(np.array([[0, 14.0], [14.0, 0]]), R * k)[0, 1]
    assert h == pytest.approx(P.NECK_MIN_RADIUS_MM, rel=2e-3)  # k is reported to 4 decimals
