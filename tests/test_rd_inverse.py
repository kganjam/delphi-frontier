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


def _short(monkeypatch):
    monkeypatch.setattr(d.solve_batch, "__defaults__", (d.N, d.DT, 2.0, "cpu"))


def test_select_none_when_all_failed():
    assert d.select([None, None]) is None and d.select([None, 0.5, 0.2]) == 2 and d.select([0.2, 0.2]) == 0


def test_all_failed_candidates_named_status_not_crash(tmp_path, monkeypatch):
    _short(monkeypatch)
    real = d.rms
    state = {"on": False}
    monkeypatch.setattr(d, "rms", lambda f, t: None if state["on"] else real(f, t))
    orig_ic = d.solve_batch
    # candidates fail only after the targets are built: flip on at the first search-phase solve
    calls = {"n": 0}
    def wrapped(*a, **k):
        calls["n"] += 1
        if calls["n"] > 2:
            state["on"] = True
        return orig_ic(*a, **k)
    monkeypatch.setattr(d, "solve_batch", wrapped)
    r = d.run(tmp_path, "cpu", False)
    sel = json.loads((tmp_path / "selection.json").read_text())
    assert r["complete"] and all(x["status"] == "no_valid_candidate" for x in sel["selection"]["optimizer"])
    assert all(x["near_optimal_count"] == 0 for x in sel["near_optimal"]) and (tmp_path / "traces.json").exists()
    assert json.loads((tmp_path / "independent_checks.json").read_text())["methods_without_selection"] == ["optimizer", "baseline"]


def test_nan_target_fails_closed_with_native_fields(tmp_path, monkeypatch):
    _short(monkeypatch)
    orig = d.solve_batch
    seen = {"n": 0}
    def nan_first(*a, **k):
        seen["n"] += 1
        out = orig(*a, **k)
        if seen["n"] == 2:  # first call is the in-job control; second builds the targets
            out = out.copy(); out[0, 0, 0] = np.nan
        return out
    monkeypatch.setattr(d, "solve_batch", nan_first)
    with pytest.raises(SystemExit):
        d.run(tmp_path, "cpu", False)
    rec = json.loads((tmp_path / "receipt.json").read_text())
    assert rec["status"].startswith("invalid_target") and not rec["complete"]
    assert (tmp_path / "targets.npz").exists() and not (tmp_path / "traces.json").exists()


def test_clean_and_concentration_stats():
    assert d.clean({"a": [float("nan"), 1.0]}) == {"a": [None, 1.0]}
    c = d.conc(np.array([[[1.0, -0.5], [2.0, 3.0]]]))
    assert c["negative_cells_u"] == 1 and c["negative_cells_v"] == 0 and c["min_u"] == -0.5


def test_full_run_retains_raw_fields(tmp_path, monkeypatch):
    _short(monkeypatch)
    d.run(tmp_path, "cpu", False)
    for f in ("independent_fields.npz", "validation_fields.npz", "concentration_stats.json", "traces_partial.json"):
        assert (tmp_path / f).exists()
    z = np.load(tmp_path / "independent_fields.npz")
    assert {"seed0_true", "seed2_optimizer", "N256_dt0.005_true", "N64_dt0.005_baseline"} <= set(z.files)
