import hashlib, json, shutil
from pathlib import Path
import numpy as np, pytest
from engineering.rd_multiic import multiic as m

SMALL = dict(targets=(0, 1), reps=1, rounds=2, arms={"A_single_IC_matched": (1, 8), "B_multi_IC_matched": (4, 2), "C_single_IC_candidate_matched": (1, 2)},
             tau=2.0, test_count=4, sparse_configs=((64, 0.02),))


def manifest(tmp_path, plan, seeds=None, **over):
    body = {"schema": m.MANIFEST_SCHEMA, "protocol_sha256": m.sha(m.PROTOCOL), "count": plan.test_count,
            "seeds": seeds or [2000001 + 7 * k for k in range(plan.test_count)], "excluded": "test", "generation_rule": "test", "generator_id": "test"}
    body.update(over)
    path = tmp_path / "manifest.json"; path.write_text(json.dumps(body))
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


def test_plan_matches_protocol_and_budgets_matched():
    p = m.Plan.from_protocol(); pr = m.protocol()
    assert (p.budget("A_single_IC_matched"), p.budget("B_multi_IC_matched"), p.budget("C_single_IC_candidate_matched")) == (512, 512, 128)
    assert pr["replication"]["replicates"] == 4 and p.test_count == 16
    assert (m.ELITES, m.SD_FLOOR, m.GATE_A_PTP, m.GATE_B_RMS) == (4, 0.03, 0.10, 0.02)
    assert pr["bounds"]["scientific_tree_hard_cap_s"] == 1800 and pr["bounds"]["soft_deadline_s"] == 1500


def test_seed_rules_disjoint_and_paired_initialisation():
    p = m.Plan.from_protocol(); tr = m.all_training_seeds(p)
    assert len(tr) == 80 and min(tr) >= 930000 and max(tr) < 933404 and all(s > 920052 for s in tr)
    a, b, c = (m.initial_points(1, 2, n) for n in (64, 16, 16))
    assert np.array_equal(a[:16], b) and np.array_equal(b, c)


def test_ledger_and_loss_rules():
    l = m.Ledger({"k": 8}); l.charge("k", 8)
    with pytest.raises(RuntimeError):
        l.charge("k", 1)
    assert m.loss_of([0.1, 0.3]) == pytest.approx(0.2) and m.loss_of([0.1, None]) is None


def test_propose_is_blind_deterministic():
    pts = m.initial_points(0, 0, 16); loss = [float(i) for i in range(16)]
    assert np.array_equal(m.propose(7, pts, loss, 16), m.propose(7, pts, loss, 16))
    assert not np.array_equal(m.propose(7, pts, loss, 16), m.propose(8, pts, loss, 16))
    loss2 = list(loss); loss2[0] = None
    assert not np.array_equal(m.propose(7, pts, loss2, 16), m.propose(7, pts, loss, 16))


def test_support_verdict_cases():
    ok = {"all": True}
    D = {(t, r): 0.1 for t in range(5) for r in range(4)}; adm = {t: 16 for t in range(5)}
    assert m.support_verdict(D, adm, ok)["verdict"] == "supported_descriptively"
    D2 = dict(D); D2.update({(t, r): -0.1 for t in range(5) for r in range(2)})  # 10 of 20 positive
    assert m.support_verdict(D2, adm, ok)["verdict"] == "not_supported"
    bad = {"all": False, "wrong_IC": False, "positive_oracle": True}
    v = m.support_verdict(D, adm, bad)
    assert v["verdict"] == "blocked" and v["failed_controls"] == ["wrong_IC"]
    assert m.support_verdict(D, {**adm, 0: 3}, ok)["targets_excluded_insufficient_admissible_seeds"] == [0]


def test_early_read_refused_and_barrier_order(tmp_path):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan)
    g = m.SealedManifest(path, sha)
    with pytest.raises(m.EarlyReadError):
        g.read(plan, set())
    sel, tr = tmp_path / "s.json", tmp_path / "t.json"; sel.write_text("{}"); tr.write_text("{}")
    g.seal(tmp_path / "barrier.json", sel, tr)
    assert (tmp_path / "barrier.json").exists() and len(g.read(plan, set())) == plan.test_count


@pytest.mark.parametrize("bad", [dict(seeds=[5, 6, 7, 8]), dict(seeds=[2000001] * 4), dict(schema="x"), dict(protocol_sha256="0" * 64), dict(count=3)])
def test_invalid_manifests_refused(tmp_path, bad):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan, **bad)
    g = m.SealedManifest(path, sha); g._sealed = True
    with pytest.raises(ValueError):
        g.read(plan, set())


def test_manifest_overlapping_training_and_wrong_hash(tmp_path):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan)
    g = m.SealedManifest(path, sha); g._sealed = True
    with pytest.raises(ValueError):
        g.read(plan, {2000001})
    g2 = m.SealedManifest(path, "0" * 64); g2._sealed = True
    with pytest.raises(ValueError):
        g2.read(plan, set())


def test_preflight_ok_and_flip_refused(tmp_path, monkeypatch):
    assert m.preflight()["preflight"] == "ok"
    fake = tmp_path / "r"
    for pin in m.protocol()["sources"]["pins"].values():
        (fake / pin["path"]).parent.mkdir(parents=True, exist_ok=True); shutil.copy(m.ROOT / pin["path"], fake / pin["path"])
    p = fake / "engineering/rd_numerics/audit.py"; b = bytearray(p.read_bytes()); b[50] ^= 1; p.write_bytes(bytes(b))
    monkeypatch.setattr(m, "ROOT", fake)
    with pytest.raises(SystemExit):
        m.preflight()


def test_small_run_orders_barrier_before_manifest_open_and_counts_exact(tmp_path, monkeypatch):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan)
    log = []
    real = Path.read_bytes
    def spy(self):
        log.append(("manifest" if self == path else "other", (tmp_path / "out" / "barrier.json").exists()))
        return real(self)
    monkeypatch.setattr(Path, "read_bytes", spy)
    r = m.run(tmp_path / "out", "cpu", False, path, sha, plan)
    assert [e for e in log if e[0] == "manifest"] == [("manifest", True)]  # opened once, after the barrier existed
    tr = json.loads((tmp_path / "out/training_traces.json").read_text())
    assert all(tr["evaluation_counts"][k] == tr["budgets"][k] for k in tr["budgets"])
    assert {tr["budgets"][k] for k in tr["budgets"] if k.endswith("A_single_IC_matched")} == {16} == {tr["budgets"][k] for k in tr["budgets"] if k.endswith("B_multi_IC_matched")}
    e = json.loads((tmp_path / "out/endpoints.json").read_text())
    assert e["verdict"]["verdict"] == "blocked"  # tau=2: no amplitude-admissible test seeds, so controls cannot support a claim
    assert r["complete"] and (tmp_path / "out/sparse_controls.json").exists()


def test_bad_manifest_fails_closed_keeping_training(tmp_path):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan, seeds=[1, 2, 3, 4])
    with pytest.raises(SystemExit):
        m.run(tmp_path / "out", "cpu", False, path, sha, plan)
    assert (tmp_path / "out/selections.json").exists() and not (tmp_path / "out/endpoints.json").exists()
    assert "manifest_unusable" in json.loads((tmp_path / "out/receipt.json").read_text())["status"]


def test_soft_deadline_voids_matched_comparison(tmp_path):
    plan = m.Plan(**{**SMALL, "soft_s": -1.0}); path, sha = manifest(tmp_path, plan)
    r = m.run(tmp_path / "out", "cpu", False, path, sha, plan)
    assert r["status"].startswith("training_incomplete") and not r["complete"] and not (tmp_path / "out/barrier.json").exists()


def test_completed_round_survives_a_later_round_failure(tmp_path, monkeypatch):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan)
    real = m.base.solve_batch
    calls = {"n": 0}
    def boom(*a, **k):
        calls["n"] += 1
        if calls["n"] == 6:  # control 3 + reference 1 + round 1 = 5 calls; the 6th is round 2
            raise RuntimeError("simulated hard stop during round 2")
        return real(*a, **k)
    monkeypatch.setattr(m.base, "solve_batch", boom)
    with pytest.raises(RuntimeError):
        m.run(tmp_path / "out", "cpu", False, path, sha, plan)
    out = tmp_path / "out"
    assert (out / "training_round_01.json").exists() and (out / "training_round_01.npz").exists() and not (out / "training_round_02.json").exists()
    st = m.load_training(out)
    ref = np.load(out / "reference_fields.npz")
    assert set(st) and all(len(v["fields"]) == len(v["loss"]) for v in st.values())
    r, i, a = next(k for k in st if k[2] == "B_multi_IC_matched")
    v = st[(r, i, a)]
    # recovered actual fields and scores, not only counts: recompute round-1 per-IC RMS from the saved fields
    for c in range(len(v["loss"])):
        got = [m.base.rms(v["fields"][c][k], ref[f"r{r}_t{i}_k{k}"]) for k in range(4)]
        assert got == pytest.approx(v["per_ic"][c], abs=1e-12)
    part = json.loads((out / "traces_partial.json").read_text())
    assert part["after_round"] == 1 and part["rounds_saved"][0]["json_sha256"] == m.sha(out / "training_round_01.json")
    assert not (out / "selections.json").exists() and not (out / "barrier.json").exists()


def test_no_cumulative_duplication_and_receipt_scope(tmp_path):
    plan = m.Plan(**SMALL); path, sha = manifest(tmp_path, plan)
    r = m.run(tmp_path / "out", "cpu", False, path, sha, plan)
    out = tmp_path / "out"
    assert not (out / "training_fields.npz").exists() and sorted(p.name for p in out.glob("training_round_*.npz")) == ["training_round_01.npz", "training_round_02.npz"]
    idx = json.loads((out / "training_traces.json").read_text())
    assert "runs" not in idx and len(idx["rounds"]) == 2
    # chunk fields cover every evaluated trajectory exactly once: candidates per run * rounds
    st = m.load_training(out)
    assert {k[2]: len(v["loss"]) for k, v in st.items() if k[:2] == (0, 0)} == {"A_single_IC_matched": 16, "B_multi_IC_matched": 4, "C_single_IC_candidate_matched": 4}
    assert "not numerical validation" in r["complete_means"] and r["optional_sparse_checks"]["status"] == "complete" and "controls_ok_summary" in r


def test_incomplete_sparse_checks_reported(tmp_path):
    plan = m.Plan(**{**SMALL, "sparse_configs": ((64, 0.02), (64, 0.005))}); path, sha = manifest(tmp_path, plan)
    import time
    real = m.time.time
    t0 = real()
    # soft deadline crossed only after the test phase: patch the clock so soft_passed() flips once endpoints are written
    state = {"flip": False}
    orig_finish_dump = m.dump
    def dump(p, v):
        orig_finish_dump(p, v)
        if Path(p).name == "endpoints.json":
            state["flip"] = True
    m.dump = dump
    m.time.time = lambda: real() + (1_600 if state["flip"] else 0)
    try:
        r = m.run(tmp_path / "out", "cpu", False, path, sha, plan)
    finally:
        m.dump = orig_finish_dump; m.time.time = real
    assert r["optional_sparse_checks"]["status"].startswith("INCOMPLETE") and len(r["optional_sparse_checks"]["configs_not_run"]) == 2
