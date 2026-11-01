"""Focused checks on cfd3d's committed packet, case artifacts and regime/grid summaries (no solver run)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/cfd3d"
PACKET = ART / "packet"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"engineering/cfd3d/{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_regime_converts_re_to_speed_in_each_medium():
    s = _load("summarize")
    r = s.regime(200)
    assert r["same_Re_in_each_medium"]["water_20C"]["U_m_s"] == pytest.approx(200 * 1.004e-6 / 0.230699)
    assert r["same_Re_in_each_medium"]["air_20C"]["U_m_s"] == pytest.approx(200 * 1.516e-5 / 0.230699)
    for v in r["intended"].values():          # intended regimes stay far above the simulated one
        assert min(v["gap_factor"]) > 100 and v["status"].startswith("assumed")
    assert "NOT" in r["label"].upper() and "flight" in r["label"]


def test_cpu_pair_is_reported_not_grid_independent():
    s = json.loads((ART / "summary-cpu.json").read_text())
    (pair,) = s["grid_pairs"]
    assert pair["rel_diff"] > 0.10 and pair["grid_rule_met"] is False
    assert "no force claim" in pair["reading"]


@pytest.mark.parametrize("case", ["fish_L24_Re200", "fish_L32_Re200"])
def test_case_artifacts_match_their_header(case):
    c = json.loads((ART / case / "case.json").read_text())
    geo = json.loads((ART / "geometry/components.json").read_text())
    assert c["candidate_sha256"] == geo["candidate_sha256"]
    assert c["resolution"]["fins_resolved"] is False and c["resolution"]["fin_thickness_cells"] < 2
    assert "body force" in c["coefficients"]["sign"] or "ON THE BODY" in c["coefficients"]["sign"].upper()
    for k, v in c["components"].items():
        assert v["stl_sha256"] == geo["components"][k]["stl_sha256"]
        n = (ART / case / "surface" / f"{k}.f32").stat().st_size
        assert n == v["rows"] * 10 * 4                        # 10 float32 columns per STL triangle
        assert v["resolved"] == (k in ("body", "eye_L", "eye_R"))
    r = json.loads((ART / case / "render/render.json").read_text())
    assert r["video"]["sha256"] == sha(ART / case / "render/flow.mp4")
    assert "FAILED" in r["caption"] and "not swimming" in r["caption"]


def test_reference_gate_failure_is_carried_by_the_packet():
    pk = json.loads((ROOT / "engineering/cfd3d/packet.json").read_text())
    ctl = json.loads((ART / "controls/cpu_controls.json").read_text())
    assert pk["reference_gate"]["C1_sphere_Re100"] == "FAIL" and ctl["C1"]["pass"] is False
    assert pk["local_cpu_pins"]["sphere_D16_Cd"] == ctl["C1"]["D16"]["Cd_mean"]


def test_packet_manifest_matches_archive_and_git():
    m = json.loads((PACKET / "packet-manifest.json").read_text())
    blob = (PACKET / m["archive"]).read_bytes()
    assert hashlib.sha256(blob).hexdigest() == m["archive_sha256"] and m["inject_total_raw"] <= 45_000
    with tarfile.open(PACKET / m["archive"]) as tf:
        for row in m["files"]:
            data = tf.extractfile(row["path"]).read()
            assert hashlib.sha256(data).hexdigest() == row["sha256"]
            src = row["path"].removeprefix("fish3d_src/")
            assert subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{row['rev']}:{src}"],
                                  capture_output=True, text=True).stdout.strip() == row["blob"]


def _launch(tmp_path, digest, extra_env=None):
    m = json.loads((PACKET / "packet-manifest.json").read_text())
    env = dict(os.environ, PREFLIGHT="1", TMPDIR=str(tmp_path), **(extra_env or {}))
    return subprocess.run([sys.executable, "-I", str(ROOT / m["launcher"]), str(PACKET / m["archive"]), digest],
                          env=env, capture_output=True, text=True, timeout=60)


def test_preflight_passes_and_wrong_hash_is_refused(tmp_path):
    m = json.loads((PACKET / "packet-manifest.json").read_text())
    ok = _launch(tmp_path, m["archive_sha256"])
    assert ok.returncode == 0 and '"preflight": true' in ok.stdout
    bad = _launch(tmp_path, "0" * 64)
    assert bad.returncode == 9 and "refused" in bad.stdout


def test_preflight_fails_on_a_missing_file(tmp_path):
    m = json.loads((PACKET / "packet-manifest.json").read_text())
    job = tmp_path / "job"
    with tarfile.open(PACKET / m["archive"]) as tf:
        tf.extractall(job, filter="data")
    (job / "engineering/cfd3d/env_gpu/pins.tsv").unlink()
    r = subprocess.run([sys.executable, "-I", "engineering/cfd3d/gpu_entry.py"], cwd=job,
                       env=dict(os.environ, PREFLIGHT="1"), capture_output=True, text=True, timeout=60)
    assert r.returncode != 0


def test_avx512_repair_is_geometry_only_and_evidenced():
    pk = json.loads((ROOT / "engineering/cfd3d/packet.json").read_text())
    env = pk["geometry"]["numpy_env"]
    assert "X86_V4" in env["NPY_DISABLE_CPU_FEATURES"]
    src = (ROOT / "engineering/cfd3d/gpu_entry.py").read_text()
    assert src.count('PK["geometry"]["numpy_env"]') == 2          # the build call and its status record only
    ev = ROOT / env["evidence"]
    pin = (ART / "geometry/candidate.json").read_bytes()
    assert (ev / "candidate.no_avx512.json").read_bytes() == pin          # disabled dispatch reproduces the pin
    assert (ev / "candidate.default.json").read_bytes() != pin            # default AVX-512 dispatch does not
    d = json.loads((ev / "diff-pin-vs-cloud-default.json").read_text())
    assert d["n_differences"] == 3 and d["max_ulps"] <= 2 and not d["non_numeric"]


VLM = ART / "vlm"
V3 = ("fish3d-v3a-fan", "fish3d-v3b-glide-pose", "fish3d-v3c-daane-length")


def test_vlm_controls_pass_and_the_mutant_fails():
    r = json.loads((VLM / "controls.json").read_text())
    g = json.loads((ROOT / "engineering/cfd3d/gates_vlm.json").read_text())["controls"]
    assert set(g) <= set(r) and r["all_pass"] is True
    assert r["V5_mutant_collocation_quarter_chord"]["rel_err"] > g["V1_elliptic_AR6"]["pass"]["rel_err_max"]


def test_vlm_seg_vel_matches_an_infinite_line_vortex():
    v = _load("vlm")
    import numpy as np
    P = np.array([[0.0, 0.0, 1.0]])
    u = v.seg_vel(P, np.array([[-1e6, 0.0, 0.0]]), np.array([[1e6, 0.0, 0.0]]))[0, 0]
    assert u == pytest.approx([0.0, -1 / (2 * 3.141592653589793), 0.0], abs=1e-9)     # Gamma/(2 pi r), right-hand


@pytest.mark.parametrize("v", V3)
def test_vlm_fish_record_carries_its_candidate_and_conserves_force(v):
    import numpy as np
    r = json.loads((VLM / v / "vlm.json").read_text())
    assert len(r["candidate_sha256"]) == 64 and r["source"].endswith(v)
    assert all(m["modelled_as"].startswith("zero-thickness") for m in r["membrane"].values())
    assert set(r["dynamic_pressure_Pa"]) == {"air_20C", "water_20C"}
    for c in r["cases"].values():
        assert c["side_force_over_lift"] < 1e-9
        for f in c["fins"].values():
            assert f["transfer_vector_residual_over_gross"] < 1e-12
            assert len(f["quad_dCp"]) == len(f["quad_area_m2"]) == len(f["quad_upper_normal"])
            assert np.isfinite(f["quad_dCp"]).all()


GPU = ART / "gpu-v1"


def test_gpu_bundle_matches_its_receipt_and_keeps_the_failed_gate():
    r = json.loads((GPU / "receipt.json").read_text())
    for row in r["files"]:
        assert sha(GPU / row["path"]) == row["sha256"]
    st = json.loads((GPU / "status.json").read_text())
    assert st["reference_gate"]["C1_sphere_Re100"] == "FAIL" and "FAILED" in st["science"]
    assert r["candidate_sha256"] == json.loads((ART / "geometry/components.json").read_text())["candidate_sha256"]
    d = json.loads((GPU / "gpu_diag.json").read_text())
    assert abs(d["sphere_D32"]["Cd_mean"]) < 0.95            # still below the frozen band at D 32


def test_gpu_grid_pairs_never_make_a_force_claim():
    s = json.loads((ART / "summary-gpu-v1.json").read_text())
    assert len(s["grid_pairs"]) == 2 and all(p["physical_force_claim"] is False for p in s["grid_pairs"])


def test_vlm_v3b_is_flagged_not_converged():
    r = json.loads((VLM / "fish3d-v3b-glide-pose" / "vlm.json").read_text())
    assert r["status"].startswith("NOT CONVERGED")
    cl0 = [v[0] for v in r["convergence_sweep"]["bilinear_surface_normal"].values()]
    assert min(cl0) < 0 < max(cl0)                     # the sign itself is lattice-dependent


def test_cyl2d_time_mean_is_exact_for_linear_data_with_partial_windows():
    e = _load("cyl2d_eval")
    t = [0.0, 0.3, 1.1, 1.15, 2.9, 4.0, 7.3]                 # non-uniform spacing
    y = [3 * x + 1 for x in t]
    for a, b in ((0.1, 6.0), (0.31, 0.32), (1.12, 3.5), (0.0, 7.3)):   # ends inside intervals, one tiny window
        assert e.time_mean(t, y, a, b) == pytest.approx(1.5 * (a + b) + 1, rel=1e-12)
    tk = [0.0, 1.0, 2.5, 5.0, 6.0, 9.0]                       # kink at a sample: piecewise linear is exact too
    yk = [abs(x - 5.0) for x in tk]
    a, b = 0.5, 7.0                                           # integral of |t - 5| over [0.5, 7] = 10.125 + 2
    assert e.time_mean(tk, yk, a, b) == pytest.approx((10.125 + 2.0) / 6.5, rel=1e-12)


def _cyl_run(cd=1.326, cdp=0.988, st=0.1660, periodic=True, surface=True, dt=0.05):
    import math
    t, k = [dt], 0
    while t[-1] < 600.0:                                      # stops like cyl2d.jl: first sample at or past t_end
        k += 1
        t.append(t[-1] + dt * (1.0 + 0.3 * math.sin(0.7 * k)))   # non-uniform steps, like the adaptive dt
    cl = [math.sin(2 * math.pi * st * s) if periodic else 1e-3 for s in t]
    run = {"t": t, "Cd": [cd] * len(t), "Cd_p": [cdp] * len(t), "Cl": cl}
    if surface:                                               # Cp = -k cos(theta) closes to Cd_p for k = 2 Cd_p / pi
        n = 720
        run["surface"] = {"Cp_wall_mean": [-2 * cdp / math.pi * math.cos(2 * math.pi * i / n) for i in range(n)]}
    return run


def _cyl_eval(tmp_path, **runs):
    e = _load("cyl2d_eval")
    paths = {}
    for k, r in runs.items():
        paths[k] = tmp_path / f"{k}.json"
        paths[k].write_text(json.dumps(r))
    return e.main(tmp_path / "eval.json", paths)


def test_cyl2d_eval_recovers_a_synthetic_pass_and_gates_pressure_coupling_on_closure(tmp_path):
    good = dict(R1=_cyl_run(cd=1.31), R2=_cyl_run(), R3_domain=_cyl_run(cd=1.315, cdp=0.979, st=0.1650),
                M1_mutant=_cyl_run(cd=2.0, periodic=False))
    r = _cyl_eval(tmp_path, **good)
    assert r["runs"]["R2"]["St"] == pytest.approx(0.1660, rel=1e-3)
    assert r["runs"]["R2"]["Cd_p_surface"] == pytest.approx(0.988, rel=1e-9)
    v = r["verdict"]
    assert v["control_passes"] and v["surface_internal"] and v["pressure_coupling_allowed"]
    bad_closure = dict(good, R2=_cyl_run())
    bad_closure["R2"]["surface"]["Cp_wall_mean"] = [c * 0.5 for c in bad_closure["R2"]["surface"]["Cp_wall_mean"]]
    v = _cyl_eval(tmp_path, **bad_closure)["verdict"]
    assert v["control_passes"] and v["surface_internal"] is False and v["pressure_coupling_allowed"] is False
    v = _cyl_eval(tmp_path, **dict(good, R2=_cyl_run(surface=False)))["verdict"]
    assert v["control_passes"] and "surface_internal" not in v and v["pressure_coupling_allowed"] is False
    v = _cyl_eval(tmp_path, **dict(good, R2=_cyl_run(cd=1.20)))["verdict"]           # 9.5 % low: outside 2 %
    assert v["R2_fidelity"] is False and v["control_passes"] is False and v["pressure_coupling_allowed"] is False


@pytest.mark.parametrize("breakage", ["nan", "inf", "length", "unsorted", "repeat", "short", "cp_nan", "missing"])
def test_cyl2d_eval_fails_closed_on_bad_series(tmp_path, breakage):
    run = _cyl_run()
    if breakage == "nan":
        run["Cd"][500] = float("nan")
    elif breakage == "inf":
        run["Cl"][-1] = float("inf")
    elif breakage == "length":
        run["Cd_p"] = run["Cd_p"][:-1]
    elif breakage == "unsorted":
        run["t"][100], run["t"][101] = run["t"][101], run["t"][100]
    elif breakage == "repeat":
        run["t"][100] = run["t"][99]
    elif breakage == "short":
        run = {k: (v[: len(v) // 2] if isinstance(v, list) else v) for k, v in run.items()}
    elif breakage == "cp_nan":
        run["surface"]["Cp_wall_mean"][3] = float("nan")
    elif breakage == "missing":
        del run["Cd_p"]
    r = _cyl_eval(tmp_path, R1=_cyl_run(), R2=run, R3_domain=_cyl_run(cd=1.315, cdp=0.979, st=0.1650),
                  M1_mutant=_cyl_run(cd=2.0, periodic=False))
    assert r["runs"]["R2"]["valid"] is False and r["runs"]["R2"]["problems"]
    assert r["verdict"]["invalid_runs"] == ["R2"]
    assert r["verdict"]["control_passes"] is False and r["verdict"]["pressure_coupling_allowed"] is False
    # an invalid mutant cannot pass the mutant rule either
    r = _cyl_eval(tmp_path, R1=_cyl_run(), R2=_cyl_run(), R3_domain=_cyl_run(cd=1.315, cdp=0.979, st=0.1650),
                  M1_mutant=run)
    assert r["verdict"]["mutant"] is False and r["verdict"]["control_passes"] is False


def test_vlm_provenance_names_the_producer_and_only_the_hand_added_keys():
    p = json.loads((VLM / "PROVENANCE.json").read_text())
    assert p["producer"]["git_blob"].startswith("cdcf1c41")
    for v, keys in p["hand_added_keys"].items():
        rec = json.loads((VLM / v / "vlm.json").read_text())
        assert set(keys) <= set(rec)
        assert sha(VLM / v / "vlm.json") == p["verification_2026_10_31"]["committed_file_sha256"][v]
        assert p["verification_2026_10_31"]["producer_rerun_equals_committed_minus_hand_added"][v]


def test_cpu_packet_runs_only_frozen_contract_cases_with_pinned_env():
    pk = json.loads((ROOT / "engineering/cfd3d/cpu_packet.json").read_text())
    contract = json.loads((ROOT / "engineering/cfd3d/cyl2d_contract.json").read_text())
    ids = [c["run_id"] for c in pk["cases"]]
    assert set(ids) <= set(contract["runs"]) and "R2" not in ids and "T_restart" not in contract["runs"]
    assert sum(c["threads"] for c in pk["cases"]) <= 16
    assert all(c["budget_s"] <= pk["outer_budget_s"] - pk["emit_margin_s"] for c in pk["cases"])
    assert sha(ROOT / "engineering/cfd3d/env/Manifest.toml") == pk["env"]["manifest_sha256"]
    assert "FAILED" in pk["reference_gate"]["C1_sphere_3d"] and "never 'passed'" in pk["science"]
    env = dict(os.environ, PREFLIGHT="1")
    r = subprocess.run([sys.executable, "-I", str(ROOT / "engineering/cfd3d/cyl2d_entry.py")], env=env,
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and json.loads(r.stdout)["preflight"] is True


def test_cpu_packet_controls_record_a_passing_check_and_a_failing_mutant():
    r = json.loads((ART / "cyl2d/cpu-packet-controls.json").read_text())
    real, mut = r["restart_check_real"]["result"], r["restart_check_mutant"]["result"]
    assert real["series_identical"] and real["final_state_identical"] and real["foreign_checkpoint_refused"]
    assert real["rc_first_segment"] == 75 and real["cp_after_split"] >= 5
    assert mut["series_identical"] is False and mut["final_state_identical"] is False
    assert r["export_resume_test"]["run2_series_identical_to_straight_run"] is True


def test_r2_packet_is_one_gpu_contract_case_behind_its_controls():
    pk = json.loads((ROOT / "engineering/cfd3d/r2_packet.json").read_text())
    contract = json.loads((ROOT / "engineering/cfd3d/cyl2d_contract.json").read_text())
    assert pk["device"] == "cuda" and [c["run_id"] for c in pk["cases"]] == ["R2"] and pk["cases"][0]["gpu"]
    assert contract["runs"]["R2"] == {"n_D": 64, "H": 60, "Re": 100}
    st = pk["stages"]
    assert st.index("env") < st.index("restart_check") < st.index("platform") < st.index("cases") < st.index("eval")
    tol = pk["same_state"]["tolerance"]
    assert tol["Cd"] <= 0.005 and tol["Cl"] <= 0.005 and pk["same_state"]["shift"] > 0
    assert pk["export_bytes_max"] == 0 and pk["max_out_bytes"] <= 12_000_000
    assert "FAILED" in pk["reference_gate"]["C1_sphere_3d"] and "never 'passed'" in pk["science"]
    env = dict(os.environ, PREFLIGHT="1")
    r = subprocess.run([sys.executable, "-I", str(ROOT / "engineering/cfd3d/cyl2d_entry.py"), "r2_packet.json"],
                       env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and json.loads(r.stdout)["preflight"] is True


def test_cyl2d_eval_reads_float32_printed_series_as_their_float32_values(tmp_path):
    np = pytest.importorskip("numpy")
    e = _load("cyl2d_eval")
    exact = _cyl_run()
    for k in ("t", "Cd", "Cd_p", "Cl"):                      # Float32-exact values, as cyl2d.jl produces them
        exact[k] = [float(np.float32(v)) for v in exact[k]]
    printed = dict(exact, series_dtype={k: "Float32" for k in ("t", "Cd", "Cd_p", "Cl")})
    for k in ("t", "Cd", "Cd_p", "Cl"):                      # what JSON carries: the shortest Float32 decimal
        printed[k] = [float(str(np.float32(v))) for v in exact[k]]
    assert printed["Cl"] != exact["Cl"]                      # the decimals alone are NOT the Float32 values
    a, b = e.evaluate(json.loads(json.dumps(exact))), e.evaluate(json.loads(json.dumps(printed)))
    assert a["valid"] and b["valid"] and all(a[k] == b[k] for k in ("Cd", "Cd_p", "Cl_rms", "St"))


def test_cyl2d_entry_hands_popen_only_strings(tmp_path, monkeypatch):
    """VM03 regression: st_scaling passed TIMING's int step count into Popen and died before any case."""
    monkeypatch.setenv("COPS_OUT", str(tmp_path / "out"))
    monkeypatch.setenv("CFD3D_WORK", str(tmp_path / "work"))
    m = _load("cyl2d_entry")
    m.OUT.mkdir(parents=True)                                 # main() makes it before any stage
    seen = []

    class FakePopen:
        def __init__(self, argv, **kw):
            seen.append(argv)
            self.pid, self.returncode = 0, 1

        def poll(self):
            return 1

    monkeypatch.setattr(m.subprocess, "Popen", FakePopen)
    monkeypatch.setattr(m, "CAP", ["systemd-run", "--scope"])
    monkeypatch.setattr(m, "left", lambda: 1e6)
    m.st_scaling()                                            # the stage that failed on VM03, ints included
    m.cyl(tmp_path / "x.json", "R2", 2, 8, 60, tmp_path / "log.txt", "TIMING", 300, gpu=True)
    assert seen and all(isinstance(a, str) for argv in seen for a in argv)
    assert any("TIMING" in argv and "40" in argv for argv in seen)


@pytest.mark.parametrize("case,go", [("fits", True), ("too_slow", False), ("not_gpu", False), ("gpu_mem", False)])
def test_r2_calibration_rule_go_and_no_go(tmp_path, monkeypatch, case, go):
    monkeypatch.setenv("COPS_OUT", str(tmp_path / "out"))
    monkeypatch.setenv("CFD3D_WORK", str(tmp_path / "work"))
    monkeypatch.setattr(sys, "argv", ["cyl2d_entry.py", "r2_packet.json"])
    m = _load("cyl2d_entry")
    m.OUT.mkdir(parents=True)
    step_s = 0.05 if case != "too_slow" else 0.5                 # 340k x 1.3 x step_s vs 30,000 s left

    class FakePopen:
        def __init__(self, argv, **kw):
            out = Path(argv[argv.index("R2") - 1])
            out.write_text(json.dumps({"wall_s": 300 * step_s, "steps": 300, "ns_per_cell_step": 1.0,
                                       "dt_grid_last": 0.18, "gpu": case != "not_gpu"}))
            self.pid, self.returncode = 0, 0

        def poll(self):
            return 0

    def fake_poll(stop, rows):
        rows.append([23000 if case == "gpu_mem" else 3000, 23034])

    monkeypatch.setattr(m.subprocess, "Popen", FakePopen)
    monkeypatch.setattr(m, "CAP", [])
    monkeypatch.setattr(m, "gpu_memory_poll", fake_poll)
    monkeypatch.setattr(m, "left", lambda: 30_000.0)
    assert m.PK_FILE == "r2_packet.json"
    assert m.st_calibration() is go
    r = json.loads((m.OUT / "calibration.json").read_text())
    assert r["go"] is go and r["projected_wall_s"][1] == round(340_000 * step_s * 1.3)


def test_r2_packet_controls_record_the_dry_run_and_its_mutant():
    r = json.loads((ART / "cyl2d/r2-packet-controls.json").read_text())
    p = r["platform_dry_run"]["result"]
    assert p["aligned_within"] and not p["shifted_within"] and p["ok"] is False and p["dry_run_would_pass"]
    assert r["cyl2d_jl_sha256"] == sha(ROOT / "engineering/cfd3d/cyl2d.jl") and r["same_files_as_the_local_run"]


def test_arms_packet_is_the_frozen_control_arms_on_cuda_with_r2s_solver_and_controls():
    pk = json.loads((ROOT / "engineering/cfd3d/arms_packet.json").read_text())
    r2 = json.loads((ROOT / "engineering/cfd3d/r2_packet.json").read_text())
    contract = json.loads((ROOT / "engineering/cfd3d/cyl2d_contract.json").read_text())
    arms = ["R1", "M1_mutant", "R3_domain"]
    assert pk["device"] == "cuda" and pk["cases_sequential"] is True
    assert [c["run_id"] for c in pk["cases"]] == arms and all(c["gpu"] for c in pk["cases"])
    assert [a["run_id"] for a in pk["calibration"]["arms"]] == arms and all(r in contract["runs"] for r in arms)
    for k in ("stages", "env", "restart_check", "same_state", "emit_margin_s", "ckpt_margin_s", "max_out_bytes"):
        assert pk[k] == r2[k], k                           # the same controls and gates as the R2 packet
    cal = pk["calibration"]
    assert (cal["run_overhead"], cal["gpu_mem_frac_max"], cal["host_rss_max_gb"]) == (1.3, 0.8, 10)
    assert "FAILED" in pk["reference_gate"]["C1_sphere_3d"] and "never 'passed'" in pk["science"]
    # the solver, contract, band and env are byte-identical to the frozen R2 archive's
    rows = {r["path"]: r["sha256"] for r in json.loads((PACKET / "cfd3d-r2-packet-manifest.json").read_text())["files"]}
    for f in ("cyl2d.jl", "cyl2d_contract.json", "cyl2d_band.json", "env_gpu/Project.toml", "env_gpu/pins.tsv"):
        assert rows["engineering/cfd3d/" + f] == sha(ROOT / "engineering/cfd3d" / f), f
    env = dict(os.environ, PREFLIGHT="1")
    r = subprocess.run([sys.executable, "-I", str(ROOT / "engineering/cfd3d/cyl2d_entry.py"), "arms_packet.json"],
                       check=False, env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and json.loads(r.stdout)["preflight"] is True


def _arms_entry(tmp_path, monkeypatch, step_s: dict, mem_mib: int = 3000, left_s: float = 6000.0):
    monkeypatch.setenv("COPS_OUT", str(tmp_path / "out"))
    monkeypatch.setenv("CFD3D_WORK", str(tmp_path / "work"))
    monkeypatch.setattr(sys, "argv", ["cyl2d_entry.py", "arms_packet.json"])
    m = _load("cyl2d_entry")
    m.OUT.mkdir(parents=True)
    calls = []

    class FakePopen:
        def __init__(self, argv, **kw):
            rid = next(r for r in step_s if r in argv)
            calls.append(rid)
            Path(argv[argv.index(rid) - 1]).write_text(json.dumps(
                {"wall_s": 300 * step_s[rid], "steps": 300, "ns_per_cell_step": 1.0, "dt_grid_last": 0.2,
                 "gpu": True}))
            self.pid, self.returncode = 0, 0 if step_s[rid] > 0 else 1

        def poll(self):
            return self.returncode

    monkeypatch.setattr(m.subprocess, "Popen", FakePopen)
    monkeypatch.setattr(m, "CAP", [])
    monkeypatch.setattr(m, "gpu_memory_poll", lambda stop, rows: rows.append([mem_mib, 81559]))
    monkeypatch.setattr(m, "left", lambda: left_s)
    return m, calls


# hi steps 112k, 205k, 115k x 1.3; 6000 s left minus the 600 s checkpoint margin = 5400 s for the arms
@pytest.mark.parametrize("case,steps,go", [
    ("fits", {"R1": 0.004, "M1_mutant": 0.004, "R3_domain": 0.013}, True),          # 582 + 1066 + 1944 s
    ("sum_too_slow", {"R1": 0.008, "M1_mutant": 0.008, "R3_domain": 0.02}, False),  # each alone fits, the sum not
    ("arm_fails", {"R1": 0.004, "M1_mutant": 0.0, "R3_domain": 0.013}, False),
])
def test_arms_calibration_rule_sums_the_arms_and_stops_at_a_failed_arm(tmp_path, monkeypatch, case, steps, go):
    m, calls = _arms_entry(tmp_path, monkeypatch, steps)
    assert m.st_calibration() is go
    r = json.loads((m.OUT / "calibration.json").read_text())
    assert r["go"] is go and set(r["arms"]) <= set(steps)
    if case == "arm_fails":
        assert calls == ["R1", "M1_mutant"] and "projected_wall_s" not in r      # R3 never timed after a failure
    else:
        hi = {"R1": 112_000, "M1_mutant": 205_000, "R3_domain": 115_000}
        assert r["projected_wall_s"][1] == sum(r["arms"][k]["projected_wall_s"][1] for k in hi)
        assert all(abs(r["arms"][k]["projected_wall_s"][1] - hi[k] * steps[k] * 1.3) <= 1 + r["arms"][k]["startup_s"]
                   for k in hi)
        assert m.CALIB.keys() == set(hi) if go else True
    if case == "sum_too_slow":
        assert all(a["projected_wall_s"][1] <= 5400 for a in r["arms"].values()) and r["fits_time"] is False


def test_arms_calibration_refuses_a_device_memory_peak_over_the_cap(tmp_path, monkeypatch):
    m, _ = _arms_entry(tmp_path, monkeypatch, {"R1": 0.004, "M1_mutant": 0.004, "R3_domain": 0.013}, mem_mib=70000)
    assert m.st_calibration() is False
    assert json.loads((m.OUT / "calibration.json").read_text())["arms"]["R1"]["fits_memory"] is False


def test_sequential_cases_do_not_start_an_arm_that_no_longer_fits(tmp_path, monkeypatch):
    m, calls = _arms_entry(tmp_path, monkeypatch, {"R1": 0.004, "M1_mutant": 0.004, "R3_domain": 0.013},
                           left_s=1500.0)
    m.CALIB.update({"R1": {"projected_wall_s": [400, 800]}, "M1_mutant": {"projected_wall_s": [900, 1100]},
                    "R3_domain": {"projected_wall_s": [1300, 2000]}})
    m.case_worker({"run_id": "M1_mutant", "gpu": True, "threads": 2, "mem_gb": 11, "budget_s": 7200})
    rec = m.status["cases"]["M1_mutant"]
    assert rec["state"].startswith("not started: calibrated projection") and calls == []
    assert rec["projected_wall_s"] == [900, 1100] and rec["left_s"] == 1500


def test_cyl2d_eval_reports_each_runs_backend_and_never_relabels(tmp_path):
    runs = {"R1": dict(_cyl_run(cd=1.31), gpu=True), "M1_mutant": dict(_cyl_run(cd=2.0, periodic=False), gpu=True),
            "R2": dict(_cyl_run(), gpu=True), "R3_domain": _cyl_run(cd=1.315, cdp=0.979, st=0.1650)}
    v = _cyl_eval(tmp_path, **runs)["verdict"]
    assert v["backends"] == {"R1": "cuda", "M1_mutant": "cuda", "R2": "cuda", "R3_domain": "cpu"}
    assert v["mixed_backends"] is True and v["control_passes"]          # reported; no criterion changed


# ---------------------------------------------------------------- VLM refinement diagnostic (vlm_diag_contract.json)
@pytest.mark.parametrize(("seq", "status"), [
    ((1.0, 0.5, 0.25), "monotone_convergent"),         # R = 0.5
    ((1.0, 0.5, 0.75), "oscillatory_convergent"),      # R = -0.5
    ((1.0, 1.5, 2.5), "divergent"),                    # R = 2: the linear-in-n drift of the core chord families
    ((0.3, 0.3, 0.3), "converged_roundoff"),
])
def test_vlm_diag_triple_classifies_by_R(seq, status):
    assert _load("vlm_diag").triple(*seq)["status"] == status


def test_vlm_diag_family_flags_a_linear_drift_and_passes_geometric_convergence():
    d = _load("vlm_diag")
    tri, dec, tail = [[16, 32, 64], [24, 48, 96]], [[16, 32, 64], [24, 48, 96]], [24, 32, 48, 64, 96]
    ns = [16, 24, 32, 48, 64, 96]
    assert d.family({n: 1 + 1 / n for n in ns}, tri, dec, tail)["verdict"] == "regular"
    assert d.family({n: 1 + 1e-4 * n for n in ns}, tri, dec, tail)["verdict"] == "irregular"
    assert d.family({n: 1 + 1 / n for n in ns if n != 96}, tri, dec, tail)["verdict"] == "incomplete"


def test_vlm_diag_repair_moves_collocation_only_where_the_outline_bends():
    d = _load("vlm_diag")
    rect = d.vlm.lattice(d.RECT, *d.PLANAR, 12, 6)
    assert np.allclose(d.repair_colloc(rect, *d.PLANAR[:3])["C"], rect["C"], rtol=0, atol=1e-15)
    ell, _ = d.vlm.elliptic(6, 12, 6)
    moved = np.abs(d.repair_colloc(ell, *d.PLANAR[:3])["C"] - ell["C"]).max()
    assert moved > 1e-6
    for k in ("A", "B", "N", "area"):
        assert d.repair_colloc(ell, *d.PLANAR[:3])[k] is ell[k]
