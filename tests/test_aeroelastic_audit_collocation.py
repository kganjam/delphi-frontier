import copy
import json
import time
from hashlib import sha256

import pytest

from engineering.aeroelastic import audit_collocation as ac
from engineering.aeroelastic import audit_fidelity as af
from engineering.aeroelastic import collocation, fidelity, model, run
from engineering.aeroelastic.model import ART

TINY = {"span": 4, "chord": 1}


def ledger():
    return af.Ledger(af.frozen()["tolerance"])


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def test_audit_variant_installs_restores_and_refuses_nesting():
    assert af.setup is model.setup
    with ac.audited_variant("repaired"):
        assert af.setup is collocation.repaired_setup
        with pytest.raises(RuntimeError), ac.audited_variant("baseline"):
            pass
    assert af.setup is model.setup


def test_a_repaired_arm_audited_with_the_production_collocation_is_a_finding(tmp_path):
    folder = tmp_path / "chi0.2-u20-l32x8-rigid"
    with collocation.variant("repaired"):
        result = run.solve_arm(
            0.2, 20.0, "tiny4x1", "rigid", folder, time.monotonic() + 120, TINY
        )
    right = ledger()
    with ac.audited_variant("repaired"):
        af.audit_arm(right, folder, result, model.protocol())
    assert right.findings == []
    wrong = ledger()
    with ac.audited_variant("baseline"):
        af.audit_arm(wrong, folder, result, model.protocol())
    assert any("final_pose_fresh_VLM_force" in x["subject"] for x in wrong.findings)


def returned_like_controls():
    """A collocation-controls record with the real schema, from cfd04's reference values (no solve)."""
    refs = collocation.references()["values"]
    computed = {
        kind: {arm: dict(points) for arm, points in by_arm.items()}
        | {
            "relative_error_to_cfd04": {
                f"{a}.{p}": 0.0 for a, ps in by_arm.items() for p in ps
            }
        }
        for kind, by_arm in refs.items()
    }
    law = {"CL": 0.3, "Helmbold_CL": 0.31, "relative": -0.02, "within_3pct": True}
    bad = law | {"relative": -0.97, "within_3pct": False}
    checks = dict.fromkeys(collocation.COLLOCATION_CHECKS, True)
    return {
        "schema": "frontier.aeroelastic.collocation-controls/1",
        "computed_CL": computed,
        "rectangle": {"max_abs_C_change_m": 0.0, "CL_relative_change": 0.0},
        "law_check": {
            "repaired": {"96x8": law, "32x24": law},
            "quarter_chord_mutant": {"96x8": bad, "32x24": bad},
        },
        "chord_plateau_relative_range": {
            "repaired": {"fins": 4e-5, "ellipse": 2e-5},
            "baseline": {"fins": 7e-3, "ellipse": 9e-3},
            "one_sided_mutant": {"fins": 5.0, "ellipse": 0.5},
        },
        "K4d_one_sided_mutant_rejected_by_plateau": {"fins": True, "ellipse": True},
        "checks": checks,
        "passed": True,
        "reported_not_gating": ["K4d_one_sided_mutant_rejected_by_plateau"],
        "wall_seconds": 1.0,
    }


def test_collocation_controls_flag_a_changed_number_and_a_changed_verdict(
    tmp_path, monkeypatch
):
    local = returned_like_controls()
    monkeypatch.setattr(
        collocation, "collocation_controls", lambda out: copy.deepcopy(local)
    )
    (tmp_path / "collocation-controls.json").write_text(json.dumps(local))
    clean = ledger()
    assert all(ac.collocation_checks(clean, tmp_path)["rederived"].values())
    assert clean.findings == []
    edited = copy.deepcopy(local)
    edited["computed_CL"]["repaired"]["F3_four_fins_combined"]["32x8"] += 1e-6
    edited["chord_plateau_relative_range"]["repaired"]["fins"] = (
        2e-4  # K4c must now fail
    )
    (tmp_path / "collocation-controls.json").write_text(json.dumps(edited))
    found = ledger()
    rederived = ac.collocation_checks(found, tmp_path)["rederived"]
    kinds = {(x["kind"], x["subject"].split(".")[0]) for x in found.findings}
    assert ("reproduction", "collocation-controls") in kinds
    assert (
        "control",
        "K4c_chord_plateau_discriminates",
    ) in kinds  # returned verdict True, re-derived False
    assert not rederived["K4c_chord_plateau_discriminates"]


def test_K6_K7_catch_a_nondeterministic_rigid_arm_and_a_changed_baseline(tmp_path):
    cp, v1 = collocation.cprotocol(), fidelity.fprotocol()
    (tmp_path / "repaired/lattice-controls").mkdir(parents=True)
    for mesh in v1["lattices"]:
        (tmp_path / f"repaired/lattice-controls/{mesh}.json").write_text(
            json.dumps(
                {"passed": False, "checks": {"a": True, "upstream_force": False}}
            )
        )
    (tmp_path / "controls-original.json").write_text(json.dumps({"passed": True}))
    flight = {d: {"range_m": 30.0} for d in ["main", "half"]}
    rigid = {"iterations": [{"CL_on_fixed_source_area": 0.25}], "flight": flight}
    arms = {
        fidelity.arm_id(chi, 20.0, m, "rigid"): rigid
        for chi in (0.8, 0.2)
        for m in v1["lattices"]
    }
    baseline = {
        model.ROOT.joinpath(x["path"]).parent.name: json.loads(
            (model.ROOT / x["path"]).read_text()
        )
        for x in cp["baseline_references"]
    }
    clean = ledger()
    ok = ac.coupled_checks(clean, tmp_path, arms, baseline, cp, v1)
    assert (
        ok["K5_coupled_lattice_controls"]
        and ok["K6_determinism"]
        and ok["K7_baseline_equivalence"]
    )
    assert all(x["compared_values_exact"] for x in ok["K7"]) and clean.findings == []
    arms[fidelity.arm_id(0.2, 20.0, "fine", "rigid")] = rigid | {
        "iterations": [{"CL_on_fixed_source_area": 0.2500001}]
    }
    changed = copy.deepcopy(baseline)
    changed["chi0.8-u20-l32x8-two-way-static-feedback"]["iterations"][-1][
        "CL_on_fixed_source_area"
    ] += 1e-7
    found = ledger()
    bad = ac.coupled_checks(found, tmp_path, arms, changed, cp, v1)
    assert not bad["K6_per_lattice"]["fine"] and not bad["K7_baseline_equivalence"]
    assert any(
        x["subject"].startswith("K7.chi0.8-u20-l32x8-two-way") for x in found.findings
    )


def test_identity_flags_tampered_unlisted_and_foreign_source_bytes(tmp_path):
    raw = tmp_path / "final-x"
    science = raw / "science"
    science.mkdir(parents=True)
    (science / "summary.json").write_text("{}")
    packet = json.loads((collocation.CP / "packet.json").read_text())
    source = next(x for x in packet["files"] if x["path"].endswith("collocation.py"))
    receipt = {
        "collocation_protocol_sha256": digest(collocation.CP / "protocol.json"),
        "fidelity_v1_protocol_sha256": digest(fidelity.FID / "protocol.json"),
        "original_protocol_sha256": digest(ART / "protocol.json"),
        "sources": {source["path"]: source["sha256"]},
        "environment": {"python": "3.12.3", "numpy": "2.5.4", "scipy": "1.17.1"},
        "files": [
            {
                "path": "summary.json",
                "sha256": digest(science / "summary.json"),
                "bytes": 2,
            }
        ],
        "wall_seconds": 1.0,
        "failure": None,
        "output_bytes": 2,
        "output_cap_exceeded": False,
    }
    (science / "receipt.json").write_text(json.dumps(receipt))
    files = [science / "summary.json", science / "receipt.json"]
    collection = {
        "complete": True,
        "artifacts": [
            {
                "local_path": f"/elsewhere/{raw.name}/{p.relative_to(raw)}",
                "bytes": p.stat().st_size,
                "sha256": digest(p),
            }
            for p in files
        ],
    }
    (raw / "collection_receipt.json").write_text(json.dumps(collection))
    clean = ledger()
    ac.identity(clean, raw, science, collocation.cprotocol())
    assert clean.findings == []
    (science / "summary.json").write_text("{} ")
    (science / "stray.json").write_text("{}")
    receipt["sources"][source["path"]] = "0" * 64
    (science / "receipt.json").write_text(json.dumps(receipt))
    found = ledger()
    ac.identity(found, raw, science, collocation.cprotocol())
    details = {x["detail"] for x in found.findings}
    assert {
        "bytes differ from the collection receipt",
        "file not in the collection receipt",
        "bytes differ from the native receipt",
        "file not listed in the native receipt",
        "executed source differs from the admitted packet",
    } <= details


def test_a_changed_native_decision_is_an_analysis_disagreement(monkeypatch):
    recomputed = {
        "chi0.8-u16": {
            "assessable": True,
            "dCL_one_way_minus_rigid": "resolved",
            "dCL_two_way_minus_one_way": "resolved",
            "CL_rigid": "resolved",
            "decision": {"bending": "retain_bending", "feedback": "one_way_sufficient"},
            "series": {
                "bending": dict.fromkeys(fidelity.fprotocol()["lattices"], -0.0036),
                "feedback": dict.fromkeys(fidelity.fprotocol()["lattices"], 3e-5),
            },
        },
    }
    monkeypatch.setattr(af, "recompute_effects", lambda *a: recomputed)
    v1 = fidelity.fprotocol()
    context = {
        "compliance": 0.8,
        "speed_m_s": 16.0,
        "assessable": True,
        "effects": {
            k: {"status": "resolved"}
            for k in [
                "dCL_one_way_minus_rigid",
                "dCL_two_way_minus_one_way",
                "CL_rigid",
            ]
        },
        "decision": {
            "bending": {"decision": "retain_bending"},
            "feedback": {"decision": "one_way_sufficient"},
        },
        "descriptive_series": {
            "dCL_one_way_minus_rigid": dict.fromkeys(v1["lattices"], -0.0036),
            "dCL_two_way_minus_one_way": dict.fromkeys(v1["lattices"], 3e-5),
        },
    }
    clean = ledger()
    ac.analysis(
        clean,
        {},
        {"contexts": [context]},
        v1,
        model.protocol(),
        af.frozen()["tolerance"],
    )
    assert clean.findings == []
    changed = copy.deepcopy(context)
    changed["decision"]["bending"]["decision"] = "reject_bending"
    found = ledger()
    ac.analysis(
        found,
        {},
        {"contexts": [changed]},
        v1,
        model.protocol(),
        af.frozen()["tolerance"],
    )
    assert [x["kind"] for x in found.findings] == ["analysis_disagreement"]


def test_error_estimates_arithmetic_and_unassessable_context():
    from engineering.aeroelastic import collocation_report as cr

    lattices = cr.LADDER
    tri = {
        "T2": {
            "behaviour": "monotone",
            "p": 1.0,
            "extrapolated": -0.9,
            "GCI_abs": 0.1,
            "GCI_rel": 0.1,
        },
        "T1.5": {
            "behaviour": "monotone",
            "p": 1.0,
            "extrapolated": -0.95,
            "GCI_abs": 0.1,
            "GCI_rel": 0.1,
        },
    }
    rigid = {
        "T2": tri["T2"] | {"extrapolated": 10.0, "GCI_abs": 0.5},
        "T1.5": tri["T1.5"],
    }

    def context(series, assessable):
        effects = {
            "dCL_one_way_minus_rigid": {
                "status": "resolved",
                "floor_at_finest": 0.0,
                "triples": tri,
            },
            "dCL_two_way_minus_one_way": {
                "status": "resolved",
                "floor_at_finest": 0.0,
                "triples": tri,
            },
            "CL_rigid": {
                "status": "resolved",
                "floor_at_finest": 0.0,
                "triples": rigid,
            },
        }
        return {
            "compliance": 0.8,
            "speed_m_s": 16.0,
            "assessable": assessable,
            "descriptive_series": {k: dict(series) for k in effects},
            "floors_at_finest": dict.fromkeys(effects, 0.0),
            "effects": effects if assessable else None,
            "decision": {
                "bending": {"decision": "retain_bending", "relative": 0.09},
                "feedback": {
                    "decision": "one_way_sufficient",
                    "ratio_to_one_way": 0.01,
                },
            }
            if assessable
            else {
                "bending": {"decision": "undetermined"},
                "feedback": {"decision": "undetermined"},
            },
        }

    base = context(dict.fromkeys(lattices, -1.0), True)
    rep = context(
        dict(zip(lattices, [-1.2, -1.1, -1.05, -1.02, -1.0], strict=True)), True
    )
    row = cr.error_estimates({"contexts": [rep]}, {"contexts": [base]})[0]
    e = row["effects"]["dCL_one_way_minus_rigid"]
    assert e["five_lattice_relative_spread"]["repaired"] == pytest.approx(0.2 / 1.074)
    assert e["repaired_minus_baseline"]["main"] == pytest.approx(-0.2)
    assert e["repaired_minus_baseline_relative_at_l64x16"] == 0.0
    assert e["T2_minus_T1.5_extrapolated"] == pytest.approx(0.05)
    m = row["decision_margins_repaired"]
    assert m["bending_relative_GCI_interval"] == pytest.approx([0.8 / 10.5, 1.0 / 9.5])
    assert m["feedback_ratio_GCI_upper"] == pytest.approx(1.0 / 0.8)
    exits = context(
        dict(zip(lattices[1:], [-1.1, -1.05, -1.02, -1.0], strict=True)), False
    )
    row = cr.error_estimates({"contexts": [exits]}, {"contexts": [base]})[0]
    assert row["decision_margins_repaired"] is None
    assert row["effects"]["CL_rigid"]["status"]["repaired"] == "not_assessable"
    assert (
        row["effects"]["CL_rigid"]["five_lattice_relative_spread"]["repaired_lattices"]
        == lattices[1:]
    )
