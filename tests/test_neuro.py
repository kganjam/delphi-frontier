"""Fast checks for the neural-scale models (engineering.neuro) and their gallery cards. Simulated models; these test code, not biology."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pytest

from engineering.neuro import caudal_cpg as M2, common as C, glide_stab as M3

ROOT = Path(__file__).resolve().parents[1]


def test_body_length_from_condition_factor():
    assert C.L_BODY == pytest.approx(0.171, abs=1e-3)


def test_ebt_closed_form_matches_phase_average():
    for U in (0.0, 1.5, 4.0):
        assert M2.ebt_thrust(U, 20.0, 0.017, 0.171, 0.043) == pytest.approx(M2.ebt_thrust_numeric(U, 20.0, 0.017, 0.171, 0.043), rel=1e-9, abs=1e-12)


@pytest.mark.parametrize("c,dw,locked", [(40.0, 0.5, True), (20.0, 1.0, False)])
def test_chain_locking_condition_against_integration(c, dw, locked):
    an = M2.lock_analytic(c, dw, 2 * math.pi / 7)
    num = M2.cpg_steady(30.0, c, 2 * math.pi / 7, dw, T=0.8)
    assert an["locked"] is locked and num["locked"] is locked


def test_delay_chain_matrix_equals_explicit_buffer():
    g = M3.geometry(); d = M3.derivs(g); A, B, Bg, Lo = M3.long_ss(d); Ad, Bd, _ = M3.disc(A, B, Bg)
    rows = [Lo["theta_vis"], Lo["q_canal"]]; K = M3.gains(B[2], M3.W_PITCH)
    M = M3.closed_loop(Ad, Bd, rows, K, [0.02, 0.006]); z = np.zeros(M.shape[0]); z[1] = 0.01
    for _ in range(200):
        z = M @ z
    x = np.zeros(4); x[1] = 0.01; act = 0.0; hist = [np.r_[x, act]]; a = math.exp(-M3.DT / M3.TAU_ACT)
    for k in range(200):
        y0 = rows[0] @ (hist[k - 10] if k >= 10 else np.zeros(5)); y1 = rows[1] @ (hist[k - 3] if k >= 3 else np.zeros(5))
        x = Ad @ x + Bd * act; act = a * act + (1 - a) * (-(K[0] * y0 + K[1] * y1)); hist.append(np.r_[x, act])
    assert np.allclose(z[:5], hist[-1], atol=1e-12)


def test_neutral_point_inside_repo_bracket():
    g = M3.geometry(); d = M3.derivs(g)
    assert g["np_bracket_m"][0] - 0.003 <= d["x_np"] <= g["np_bracket_m"][1] + 0.003


def test_gallery_cards_for_completed_runs():
    spec = importlib.util.spec_from_file_location("neuro_site_builder", ROOT / "scripts/build_site.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    out = {}
    cards = {x["id"]: x for x in module.engineering_cards(module.Inputs(), out)}
    done = [r for r in ("m1-fast-start", "m2-caudal-cpg", "m3-glide-stabilizer")
            if (ROOT / f"artifacts/neuro/{r}/run_receipt.json").is_file() and json.loads((ROOT / f"artifacts/neuro/{r}/run_receipt.json").read_text())["exit_code"] == 0]
    assert done, "no completed neural-scale run"
    for r in done:
        card = cards["neuro-" + r]
        assert card["scales"][0] == "neural" and card["evidence_kind"] == "simulated, not observed"
        assert card["experiment_design"] and card["perturbation_sweep"] and card["does_not_establish"]
        m = json.loads((ROOT / card["manifest"]).read_text())
        published = out[f"@artifacts/simulations/neuro-{r}/figure.png"]
        assert hashlib.sha256(published).hexdigest() == m["outputs"]["figure.png"]
        assert all(c["result"] == "passed" for c in card["numerical_checks"] if c["name"].startswith("control") or c["name"].startswith("EBT"))
