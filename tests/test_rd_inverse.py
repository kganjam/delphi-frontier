import json, shutil, numpy as np, pytest
from engineering.rd_inverse import design as d


def test_protocol_constants_match_implementation():
    p = d.protocol()
    assert (p["fixed"]["a"], p["fixed"]["b"], p["fixed"]["tau"], p["fixed"]["dt"], p["fixed"]["N"]) == (d.A, d.B_PAR, d.TAU, d.DT, d.N)
    assert p["methods"]["budget_per_target_per_method"] == d.BUDGET == d.ROUNDS * d.PER_ROUND
    assert p["gates"]["B_design_success"].count("0.02") and d.GATE_B_RMS == 0.02 and d.GATE_A_PTP == 0.10
    assert p["bounds"]["hard_cap_s"] == 900 and len(p["targets"]["list"]) == 6


def test_targets_reproducible_from_seed():
    rng = np.random.default_rng(20261101)
    dv, lv = rng.uniform(*d.D_RANGE, 6), rng.uniform(*d.L_RANGE, 6)
    for t, a, b in zip(d.protocol()["targets"]["list"], dv, lv):
        assert abs(t["d_true"] - a) < 1e-5 and abs(t["L_true"] - b) < 1e-5


def test_methods_deterministic_and_blind():
    assert np.array_equal(d.baseline_points(2), d.baseline_points(2)) and d.baseline_points(2).shape == (64, 2)
    pts = d.initial_points(1); sc = [float(i) for i in range(16)]
    a, b = d.next_points(1, 2, pts, sc), d.next_points(1, 2, pts, sc)
    assert np.array_equal(a, b) and a.min() >= 0 and a.max() <= 1
    sc2 = list(sc); sc2[0] = None  # a failed candidate ranks last
    assert not np.array_equal(d.next_points(1, 2, pts, sc2), a)


def test_ledger_refuses_overspend():
    l = d.Ledger(); l.charge(0, "x", 64)
    with pytest.raises(RuntimeError):
        l.charge(0, "x", 1)


def test_oracle_zero_negatives_large_and_cpu_control():
    dl = np.array([[27.7, 50.7], [10.0, 42.0]]); seeds = np.array([910000, 910005])
    f = d.solve_batch(dl, seeds, tau=10.0)
    assert d.rms(f[0], f[0]) == 0.0
    assert d.rms(d.solve_batch(dl * [1.0, 0.7], seeds, tau=10.0)[0], f[0]) > 1e-6
    assert d.rms(np.full_like(f[0], np.nan), f[0]) is None
    assert d.control("cpu", False)["passed"]


def test_preflight_ok_and_one_byte_flip_refused(tmp_path, monkeypatch):
    assert d.preflight()["preflight"] == "ok"
    fake = tmp_path / "r"; (fake / "engineering/rd_diffusion").mkdir(parents=True); (fake / "engineering/rd_numerics").mkdir(parents=True)
    for pin in d.protocol()["source_pins"].values():
        shutil.copy(d.ROOT / pin["path"], fake / pin["path"])
    p = fake / "engineering/rd_diffusion/rd_ddpm.py"; b = bytearray(p.read_bytes()); b[100] ^= 1; p.write_bytes(bytes(b))
    monkeypatch.setattr(d, "ROOT", fake)
    with pytest.raises(SystemExit):
        d.preflight()
