import time

import numpy as np
import pytest

from engineering.aeroelastic import collocation, fidelity, model, run


def test_repair_moves_only_the_collocation_point_and_not_on_a_rectangle():
    fins = model.setup(8, 2)
    repaired = collocation.repaired_setup(8, 2)
    for name, fin in fins.items():
        a, b = fin["lattice"], repaired[name]["lattice"]
        for key in ["A", "B", "N", "area", "uw"]:
            assert np.array_equal(a[key], b[key])
        assert not np.array_equal(
            a["C"], b["C"]
        )  # curved fin outlines: the inconsistency is real
        g = fin["geometry"]
        assert np.allclose(
            (a["C"] - g["O"]) @ g["eu"], (b["C"] - g["O"]) @ g["eu"], atol=1e-15
        )
        assert np.array_equal(
            fin["response"].stations, repaired[name]["response"].stations
        )
    lattice, _ = collocation.rectangle(8, 4)
    moved = collocation.repair(lattice, *collocation.PLANAR[:3])
    assert np.max(abs(moved["C"] - lattice["C"])) <= 1e-12 * 0.25


def test_repaired_setup_never_mutates_the_cached_production_lattices():
    before = model.setup(8, 2)["pectoral_L"]["lattice"]["C"].copy()
    collocation.repaired_setup(8, 2)
    collocation.repaired_setup(8, 2, one_sided=True)
    assert np.array_equal(model.setup(8, 2)["pectoral_L"]["lattice"]["C"], before)


def test_variant_installs_restores_and_refuses_nesting():
    assert run.setup is model.setup and fidelity.setup is model.setup
    with collocation.variant("repaired"):
        assert (
            run.setup is collocation.repaired_setup
            and fidelity.setup is collocation.repaired_setup
        )
        with pytest.raises(RuntimeError), collocation.variant("baseline"):
            pass
    assert run.setup is model.setup and fidelity.setup is model.setup


def test_repaired_arm_differs_and_baseline_variant_is_the_production_arm(tmp_path):
    deadline = time.monotonic() + 120
    grid = {"span": 4, "chord": 1}
    plain = run.solve_arm(
        0.2, 20.0, "tiny", "rigid", tmp_path / "plain", deadline, grid
    )
    with collocation.variant("baseline"):
        same = run.solve_arm(
            0.2, 20.0, "tiny", "rigid", tmp_path / "base", deadline, grid
        )
    with collocation.variant("repaired"):
        moved = run.solve_arm(
            0.2, 20.0, "tiny", "rigid", tmp_path / "rep", deadline, grid
        )
    CL = [r["iterations"][-1]["CL_on_fixed_source_area"] for r in (plain, same, moved)]
    assert CL[0] == CL[1] and CL[2] != CL[0]


def test_controls_can_reject_wrong_collocations():
    # chord plateau: the repair is flat, the production collocation drifts (cheap ellipse, ns 16)
    def plateau(kind, **mutant):
        return collocation.spread(
            collocation.planar_CL(collocation.ellipse, 16, nc, kind, **mutant)
            for nc in (4, 8, 16)
        )

    assert plateau("repaired") <= 1e-4 < 1e-3 < plateau("baseline")
    # quarter-chord collocation sits on the bound vortex: the law check must reject it
    quarter = collocation.law(
        collocation.planar_CL(collocation.ellipse, 32, 8, "repaired", f=0.25)
    )
    good = collocation.law(
        collocation.planar_CL(collocation.ellipse, 32, 8, "repaired")
    )
    assert good["within_3pct"] and not quarter["within_3pct"]


def test_task_layout_is_the_frozen_arm_set(tmp_path):
    cp = collocation.cprotocol()
    work = collocation.tasks(cp, tmp_path, time.monotonic() + 1)
    repaired = [
        p for f, p in work if f is collocation.in_variant and p[0] == "repaired"
    ]
    baseline = [
        p for f, p in work if f is collocation.in_variant and p[0] == "baseline"
    ]
    assert (
        len([p for p in repaired if p[1] == "arm_group"]) == 15
    )  # 3 contexts x 5 lattices, 3 arms each
    assert len([p for p in repaired if p[1] == "lattice_controls"]) == 5
    assert [(p[2][0], p[2][2]) for p in baseline] == [(0.8, "l32x8"), (0.2, "l32x8")]
    assert work[0][0] is collocation.collocation_controls
    collocation.check_inputs(cp)
