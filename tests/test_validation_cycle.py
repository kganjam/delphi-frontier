"""The validation cycle on fish3d-v3a: executed and reused checks, meaningful negatives, changed-input invalidation, missing bridges, next measurement, bundle."""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from engineering.biodesign_compiler import genotype as G
from engineering.biodesign_compiler import validation_cycle as V
from engineering.fin_mechanics import beam

ROOT = V.ROOT
OUT = ROOT / V.CYCLE


def load(name):
    return json.loads((OUT / name).read_text())


@pytest.fixture(scope="module")
def protocol():
    return load("protocol.json")


def test_the_protocol_is_frozen_derived_from_pinned_receipts_and_keeps_the_two_load_cases_apart(protocol):
    assert protocol == V.build_protocol(), "the committed protocol is what the module derives from the pinned files"
    s = protocol["slice"]
    op = s["operating_point"]
    assert op["P_exact"] == "147/6400" and op["L_exact"] == "3/20" and s["law"] == "delta = P L^3 / (3 EI)" and "q L^4" in s["not_this_law"]
    assert s["EI_crit_end_loaded_Nm2"] == pytest.approx(op["P_N"] * op["L_m"] ** 2 / (3 * 0.1)) and s["EI_crit_end_loaded_Nm2"] > 2.5 * s["EI_crit_uniform_load_receipt_Nm2"], "the receipt's critical EI is for the uniform load and is far too small for an end load"
    assert protocol["candidate"]["assembly"]["sha256"] == V._file_pin(V.ASSEMBLY)["sha256"] and all(V._file_pin(v["path"])["sha256"] == v["sha256"] for v in protocol["reused"].values())
    assert "single_genome" not in json.dumps(protocol) and "biological success probability (none is computed)" in protocol["not_claimed"][2]


def test_positive_case_the_end_loaded_fem_equals_the_closed_form_inside_the_domain(protocol):
    m = V.check_mechanical(protocol)
    assert m["passed"] and m["validity"]["valid"] and m["tip_over_L"] <= 0.1 and m["max_slope_rad"] <= 0.2
    assert m["cases"][0]["rel_error"] <= protocol["tolerances"]["fem_vs_analytic_rel"]
    op = protocol["slice"]["operating_point"]
    assert m["tip_analytic_m"] == pytest.approx(op["P_N"] * op["L_m"] ** 3 / (3 * m["EI_Nm2"]))


def test_each_negative_control_is_refused_for_its_own_intended_reason(protocol):
    neg = V.check_negative_controls(protocol)
    by = {c["id"]: c for c in neg["controls"]}
    assert neg["all_rejected"] and len(by) == 6
    assert by["law:uniform-load law applied to an end load"]["observed_rel_residual"] > 0.5 and by["law:L^3 -> L^2 mutation"]["observed_rel_residual"] > 1
    assert by["unit:EI in N mm^2"]["unit_accepted"] is False and by["unit:EI in N mm^2"]["ratio_if_misread"] == pytest.approx(1e-6)
    assert by["context:uniformly loaded claim"]["uniform_over_end_tip_ratio"] == pytest.approx(3 / 8)
    for k in ("domain:EI below critical", "context:uniform-load critical EI used for the end load"):
        assert "LINEAR_MODEL_INVALID_SMALL_DEFORMATION_VIOLATED" in by[k]["refusal"], k
    assert len({c["intended_failure"] for c in neg["controls"]}) >= 4, "different causes, not one check repeated"


def test_the_negative_controls_can_fail_the_correct_law_is_not_flagged(protocol):
    good = max(r["tip_load_rel_residual"] for r in beam.control_residuals().values())
    assert good < 1e-12 < protocol["tolerances"]["mutant_must_exceed_rel"], "a correct law passes the very test that rejects the mutants"
    ok, _ = beam.solve_checked(0.15, 2 * protocol["slice"]["EI_crit_end_loaded_Nm2"], n_el=64, tip_force=protocol["slice"]["operating_point"]["P_N"], strict=True)
    assert ok.tip > 0


def test_virtual_instruments_are_the_real_contracts_and_their_tolerances_come_from_them(protocol):
    contracts = G.instrument_contracts(ROOT)
    mech = V.check_mechanical(protocol)
    virt = V.check_virtual(protocol, mech, contracts)
    assert virt["V1"]["tolerance"] == 1e-4 == protocol["tolerances"]["V1_max_abs_over_L"] and virt["V2"]["tolerance"] == 1e-7 and virt["protocol_tolerances_match_the_contracts"]
    man = json.loads((ROOT / G.INSTRUMENT_MANIFEST).read_text())["files"]["instrument-contracts.json"]["sha256"]
    for iid in ("V1-saved-deflection-section", "V2-saved-tip-and-slope"):
        ref = virt["contract_refs"][iid]
        assert ref["sha256"] == man and ref["path"] == G.INSTRUMENT_FILE and ref["pointer"].startswith("/contracts/") and ref["interface"] == "I4" and ref["kind"] == "virtual" and ref["status"] == "computed_uncalibrated"
    broken = dict(protocol, tolerances={**protocol["tolerances"], "V1_max_abs_over_L": 1e-3})
    assert V.check_virtual(broken, mech, contracts)["protocol_tolerances_match_the_contracts"] is False, "a protocol that loosened a contract tolerance is detected"


def test_reused_and_executed_checks_are_named_and_the_reused_receipt_is_not_rerun(protocol):
    s = load("summary.json")
    assert s["reused_vs_executed"] == {"executed": ["c-fem-vs-analytic", "c-negative-controls", "c-virtual-V1", "c-virtual-V2"], "reused": ["c-reused-receipt", "c-observed-allometry"], "not_run": ["c-bio-bridge-expression-to-EI", "c-sequence-reference"]}
    r = V.check_reused(protocol)
    assert r["passed"] and r["not_rerun"] is True and r["changed_pins"] == []


def test_a_changed_input_goes_stale_unaffected_checks_stay_verified_and_downstream_is_invalidated(protocol):
    graph = G.baseline_graph(ROOT)
    design = load("design.json")
    ch = V.changed_input_case(protocol, graph, design)
    assert ch["stale"] == ["fin_mechanics_receipt"] and set(ch["retained_verified"]) == {"analytic_controls", "observed_allometry_update", "assembly", "beam_code"} and ch["bytes_changed"] == 1
    p = ch["propagation"]
    assert p["invalidated_interfaces"] == ["I4", "I5"] and p["invalidated_checked_layers"] == ["fin-mechanics-numerical"]
    assert p["retained_checked_layers"] == ["regulatory-map", "aero-numerical", "observed-allometry-update"] and "original pinned model or geometry only" in p["retained_scope"]
    assert ch == load("changed-input.json"), "the committed record is what the code produces"
    assert V.verify_pins(protocol, ROOT) == {"fin_mechanics_receipt": "verified", "analytic_controls": "verified", "observed_allometry_update": "verified", "assembly": "verified", "beam_code": "verified"}


def test_zero_or_all_optional_checks_never_earn_acceptance():
    out = V.all_optional_case(ROOT)
    assert out["all_optional_not_applicable"]["all_required_pass"] is False and out["no_checks"]["all_required_pass"] is False
    assert load("all-optional.json") == out
    r = load("compile-report.json")["compile"]["validation"]
    assert r["all_required_pass"] is False and [p["all_required_pass"] for p in r["plans"]] == [True, False, False], "one plan passing does not accept the candidate while two required plans are missing"


def test_missing_bridge_and_unresolved_sequence_are_missing_not_failed_and_nothing_is_endorsed():
    c = load("compile-report.json")
    comp = c["compile"]
    counts = {p["plan_id"]: p["counts"] for p in comp["validation"]["plans"]}
    assert counts["vp-bio-bridge-growth-to-EI"]["missing"] == 1 and counts["vp-seq-functional-readout"]["missing"] == 1 and counts["vp-bio-bridge-growth-to-EI"]["fail"] == 0
    assert comp["verdict"] == "rejected" and set(comp["interface_state"].values()) == {"unknown"} and comp["function_assurance"]["level"] == "none"
    inv = c["inverse"]
    assert inv["verdict"] == "proposals_only" and inv["endorsed_candidate_set"] == [] and inv["single_genome_guaranteed"] is False and inv["proposals"][0]["sequence_unresolved"]
    assert "sequence unresolved" in " ".join(inv["proposals"][0]["not_endorsed_because"])
    hist = {h["id"]: h for h in load("check-history.json")["checks"]}
    assert hist["c-bio-bridge-expression-to-EI"]["status"] == "missing" and hist["c-sequence-reference"]["status"] == "missing"
    assert "reporter or endogenous expression" in hist["c-sequence-reference"]["required_readout"] and "EI" in hist["c-bio-bridge-expression-to-EI"]["required_readout"]


def test_the_observed_allometry_negative_update_is_separate_evidence_not_fin_validation():
    hist = {h["id"]: h for h in load("check-history.json")["checks"]}
    a = hist["c-observed-allometry"]
    assert a["status"] == "fail" and a["endpoint"] is False and a["heldout_after"] != a["heldout_before"]
    plan = json.loads((OUT / "plans/plan-vp-mech-end-loaded-cantilever.json").read_text())
    assert "c-observed-allometry" not in [c["id"] for c in plan["required_checks"]], "it is not a check of the mechanical slice"
    assert "not fin mechanics" in a["reason"] and "not sequence-function" in a["reason"]


def test_the_digests_tie_candidate_protocol_plan_and_results_together_and_a_changed_result_goes_stale():
    s = load("summary.json")
    asm = V._file_pin(V.ASSEMBLY)["sha256"]
    plan = json.loads((OUT / "plans/plan-vp-mech-end-loaded-cantilever.json").read_text())
    assert s["digest_chain"]["candidate_assembly_sha256"] == asm == plan["candidate_assembly_sha256"] and s["digest_chain"]["protocol_sha256"] == V._file_pin(f"{V.CYCLE}/protocol.json")["sha256"]
    assert plan["protocol_sha256"] == s["digest_chain"]["protocol_sha256"]
    for cid, h in s["digest_chain"]["result_refs"].items():
        doc = json.loads((OUT / f"results/res-{cid}.json").read_text())
        assert V._sha((OUT / f"results/res-{cid}.json").read_bytes()) == h and doc["candidate_assembly_sha256"] == asm and doc["validator"]["dependence_identity"]
    design = load("design.json")
    tmp = Path(tempfile.mkdtemp(prefix="vc-test-"))
    try:
        for rel in [p["ref"]["path"] for p in design["validation_plans"]] + [r["ref"]["path"] for r in design["validation_results"]]:
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, tmp / rel)
        ok = G.evaluate_validation(tmp, design)["plans"][0]
        assert ok["all_required_pass"] and ok["counts"]["pass"] == 5
        p = tmp / f"{V.CYCLE}/results/res-c-fem-vs-analytic.json"
        p.write_bytes(p.read_bytes().replace(b'"pass"', b'"fail"'))
        bad = G.evaluate_validation(tmp, design)["plans"][0]
        assert not bad["all_required_pass"] and next(c for c in bad["checks"] if c["id"] == "c-fem-vs-analytic")["status"] == "stale", "caller-supplied status cannot override the pinned bytes"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_next_measurement_is_proposed_not_executed_under_explicit_assumptions_with_sensitivity(protocol):
    n = V.next_measurement(protocol)
    assert n["measurement_rows"] == [] and n["executed"] is False and "proposed Action only" in n["status"] and len(n["sensitivity_grid"]) == 9
    assert n["selected_design_id"] == "mixed_load_deflection" and n["selection_flips"] is False and all(not g["deflection_only_identifiable"] for g in n["sensitivity_grid"])
    cells = {(g["noise_multiple"], g["mixed_cost_multiple"]) for g in n["sensitivity_grid"]}
    assert (0.25, 0.5) in cells and (4.0, 2.0) in cells and "declared, not calibrated" in n["assumptions"]
    assert n == load("next-measurement.json"), "the committed record is what the planner produces"


def test_no_aggregate_biological_probability_exists_anywhere():
    bad = []

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if "probab" in k.lower() and v is not None and not isinstance(v, (dict, list)):
                    bad.append(path + "/" + k)
                walk(v, path + "/" + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + f"[{i}]")

    for f in sorted(OUT.rglob("*.json")):
        walk(json.loads(f.read_text()), f.name)
    assert bad == [] and load("summary.json")["verdict"]["biological_success_probability"] is None


def test_the_cycle_replays_deterministically_on_the_committed_protocol():
    before = {p: p.read_bytes() for p in sorted(OUT.rglob("*")) if p.is_file() and "bundle" not in p.parts}
    try:
        V.run()
        after = {p: p.read_bytes() for p in sorted(OUT.rglob("*")) if p.is_file() and "bundle" not in p.parts}
        assert set(after) == set(before) and all(after[p] == before[p] for p in before), [p.name for p in before if after.get(p) != before[p]]
    finally:
        for p, b in before.items():
            p.write_bytes(b)


def test_run_refuses_an_unfrozen_or_modified_protocol(tmp_path):
    p = OUT / "protocol.json"
    orig = p.read_bytes()
    try:
        p.write_bytes(orig + b" ")
        with pytest.raises(Exception):
            V.run()
    finally:
        p.write_bytes(orig)


def test_the_importable_bundle_links_records_and_keeps_the_action_a_proposal(tmp_path):
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    try:
        subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "-e", f"{head}:{V.CYCLE}/summary.json"])
    except subprocess.CalledProcessError:
        pytest.skip("the cycle artifacts are not committed yet")
    b = V.prepare_bundle(head, "2026-11-01T00:00:00+00:00", tmp_path / "b")
    kinds = [r["kind"] for r in b["records"]]
    assert sorted(kinds) == ["Action", "Action", "Claim", "Evidence", "Evidence", "Problem", "Problem"]
    man = json.loads((tmp_path / "b/bundle-manifest.json").read_text())
    assert all(c["ok"] for c in man["checks"]) and man["status"].startswith("PREPARED ONLY") and "no DB" in man["status"]
    proposal = next(r for r in b["records"] if r["id"] == "validation-cycle-next-measurement")["payload"]
    assert proposal["title"].startswith("PROPOSED, not executed") and proposal["proposal"]["intent"] == "experiment" and proposal["proposal"]["selection_basis"] == "declared_utility"
    ev = {r["id"]: r["payload"] for r in b["records"] if r["kind"] == "Evidence"}
    assert ev["validation-cycle-observed-allometry-separate"]["relation"] == "context_only" and ev["validation-cycle-mechanical-evidence"]["relation"] == "supports"
    claim = next(r for r in b["records"] if r["kind"] == "Claim")["payload"]
    assert "rejected as a working assembly" in claim["title"] and "/data/" not in json.dumps(b)
