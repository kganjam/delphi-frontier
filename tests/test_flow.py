import math

import numpy as np
import torch

from engineering.flow import controls, obstacle
from engineering.flow.lbm import LBM


def test_poiseuille_profile_small_grid():
    r = controls.poiseuille(16)
    assert r["rel_L2_error"] < 5e-3 and r["mass_drift"] < 1e-10 and r["transverse_velocity_max"] < 1e-10


def test_poiseuille_second_order():
    e8, e16 = controls.poiseuille(8)["rel_L2_error"], controls.poiseuille(16)["rel_L2_error"]
    assert math.log(e8 / e16) / math.log(2) > 1.5


def test_taylor_green_decay_rate():
    r = controls.taylor_green(32)
    assert r["nu_rel_error"] < 1.5e-2 and r["mass_drift"] < 1e-10


def test_mass_conserved_with_force_and_walls():
    solid = torch.zeros(8, 12, dtype=torch.bool); solid[:, 0] = True; solid[:, -1] = True
    L = LBM(8, 12, 0.7, solid=solid, force=(1e-5, 0.0)); L.init(); m0 = L.total_mass()
    for _ in range(300):
        L.step()
    assert abs(L.total_mass() - m0) / m0 < 1e-12


def test_ellipse_mask_area():
    nx, ny, tau, solid = obstacle.build(40)
    area = float(solid.sum())
    assert abs(area - math.pi * (40 / 2) * (obstacle.THICK * 40 / 2)) / area < 0.06
    assert tau > 0.5 and abs((tau - 0.5) / 3 - obstacle.U * 40 / obstacle.RE) < 1e-12


def test_obstacle_short_run_finite_and_subsonic(tmp_path):
    r = obstacle.run(tmp_path, 12, max_steps=600, save_every=300, quiet=True)
    assert r["all_finite"] and r["max_speed_over_cs_Mach"] < 0.3


def test_refuses_nonphysical_tau():
    import pytest
    with pytest.raises(ValueError):
        LBM(4, 4, 0.5)
