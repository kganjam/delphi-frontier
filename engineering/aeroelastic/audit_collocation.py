"""Independent return audit of the paired collocation study (collocation-paired-v1).

Per arm it is the frozen fidelity-v1 return audit (audit_fidelity.py, bytes unchanged): closed-form beam shapes,
saved-load and CL reproduction, domain-exit reproduction and one fresh VLM solve on each stored final pose, run
with the variant that produced the arm installed in that module's setup name. Around it, and written after the
return arrived and after its native summary was read (the report says so), are the checks specific to this
study: the collector's and the native receipt's bytes against the admitted packet, cardinality, K1-K4c
recomputed locally and compared value by value, K5-K7 and the original controls re-derived from raw files, and
the frozen classification recomputed by the audit's separate three-grid implementation. It never reruns an arm,
never edits a returned file and never replaces a native status or domain exit.

    python -m engineering.aeroelastic.audit_collocation --raw RAW_RETURN_DIR --report REPORT.json
"""

import argparse
import contextlib
import json
import tempfile
from pathlib import Path


from . import audit_fidelity as af
from . import collocation, fidelity, model
from .model import ART, dump

BLOCKING = {"identity", "reproduction", "analysis_disagreement", "missing", "control"}
NATIVE_PREFIXES = ("model-domain", "unconverged", "partial", "not-started")


@contextlib.contextmanager
def audited_variant(name):
    """audit_fidelity rebuilds lattices with its module name setup; give it the arm's own variant."""
    if af.setup is not model.setup:
        raise RuntimeError("An audit variant is already installed")
    af.setup = collocation.VARIANTS[name]
    try:
        yield
    finally:
        af.setup = model.setup


def identity(ledger, raw, science, cp):
    record = {}
    collection = af.read(raw / "collection_receipt.json")
    listed = set()
    for ref in collection["artifacts"]:
        parts = Path(ref["local_path"]).parts
        local = raw.joinpath(*parts[parts.index(raw.name) + 1 :])
        listed.add(local)
        if (
            not local.is_file()
            or local.stat().st_size != ref["bytes"]
            or af.digest(local) != ref["sha256"]
        ):
            ledger.find(
                "identity", str(local), "bytes differ from the collection receipt"
            )
    for extra in sorted(p for p in raw.rglob("*") if p.is_file() and p not in listed):
        if extra.name != "collection_receipt.json":
            ledger.find("identity", str(extra), "file not in the collection receipt")
    record |= {
        "collection_receipt_sha256": af.digest(raw / "collection_receipt.json"),
        "collection_artifacts": len(collection["artifacts"]),
        "collection_bytes": sum(x["bytes"] for x in collection["artifacts"]),
        "collection_complete": collection["complete"],
    }
    receipt = af.read(science / "receipt.json")
    for key, path in [
        ("collocation_protocol_sha256", collocation.CP / "protocol.json"),
        ("fidelity_v1_protocol_sha256", fidelity.FID / "protocol.json"),
        ("original_protocol_sha256", ART / "protocol.json"),
    ]:
        if receipt[key] != af.digest(path):
            ledger.find(
                "identity", key, "executed protocol differs from the frozen one"
            )
    packet = json.loads((collocation.CP / "packet.json").read_text())
    members = {x["path"]: x["sha256"] for x in packet["files"]}
    for name, value in receipt["sources"].items():
        if members.get(name) != value:
            ledger.find(
                "identity", name, "executed source differs from the admitted packet"
            )
    if (receipt["environment"]["numpy"], receipt["environment"]["scipy"]) != (
        "2.5.4",
        "1.17.1",
    ):
        ledger.find("identity", "environment", "pinned versions not used")
    names = {x["path"] for x in receipt["files"]}
    for ref in receipt["files"]:
        target = science / ref["path"]
        if (
            not target.is_file()
            or target.stat().st_size != ref["bytes"]
            or af.digest(target) != ref["sha256"]
        ):
            ledger.find("identity", ref["path"], "bytes differ from the native receipt")
    for extra in sorted(
        str(p.relative_to(science)) for p in science.rglob("*") if p.is_file()
    ):
        if extra != "receipt.json" and extra not in names:
            ledger.find("identity", extra, "file not listed in the native receipt")
    return record | {
        "admitted_archive_sha256": packet["archive_sha256"],
        "source_commit": packet["source_commit"],
        "receipt_sha256": af.digest(science / "receipt.json"),
        "executed_sources": len(receipt["sources"]),
        "environment": receipt["environment"],
        "native_failure": receipt["failure"],
        "wall_seconds": receipt["wall_seconds"],
        "output_bytes": receipt["output_bytes"],
        "output_cap_exceeded": receipt["output_cap_exceeded"],
    }


def audit_arms(ledger, folder, declared, kind, p):
    """audit_fidelity.audit's per-arm loop (that function is monolithic and frozen, so it is restated here)."""
    progress = {
        row["id"]: row
        for path in sorted((folder / "progress").glob("*.json"))
        for row in af.read(path)
    }
    arms, records, statuses = {}, [], {}
    for name in declared:
        case, row = folder / "arms" / name, progress.get(name)
        if (case / "result.json").is_file():
            result = af.read(case / "result.json")
            statuses[name] = result["status"]
            if row is not None and (
                row["status"] != result["status"]
                or row.get("iterations") != result["iterations"]
            ):
                ledger.find(
                    "reproduction", name, "progress row differs from result.json"
                )
            try:
                with audited_variant(kind):
                    records.append(af.audit_arm(ledger, case, result, p))
            except (
                Exception
            ) as exc:  # an unreadable arm is a finding, the audit goes on
                ledger.find("reproduction", name, f"{type(exc).__name__}: {exc}")
                records.append(
                    {"id": name, "status": result["status"], "audit_error": str(exc)}
                )
            arms[name] = result
        elif (case / "failure.json").is_file():
            failure = af.read(case / "failure.json")
            statuses[name] = failure["status"]
            records.append(
                {"id": name, "status": failure["status"], "error": failure.get("error")}
            )
            ledger.find("native_failure", name, failure.get("error", failure["status"]))
        elif row is not None:
            statuses[name] = row["status"]
            records.append({"id": name, "status": row["status"]})
            ledger.find("native_incomplete", name, row["status"])
        else:
            statuses[name] = "missing"
            ledger.find("missing", name, "no result, failure or progress row")
    for name, status in statuses.items():
        if status.startswith(NATIVE_PREFIXES):
            ledger.find(
                "native_" + status.split(":")[0].replace(" ", "_"), name, status
            )
    extra = sorted(
        p.name for p in (folder / "arms").iterdir() if p.name not in set(declared)
    )
    if extra:
        ledger.find("identity", str(folder / "arms"), f"undeclared arms {extra}")
    return arms, records, statuses


def leaves(value, prefix=""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(value, bool) or value is None:
        yield prefix, value
    elif isinstance(value, (int, float)):
        yield prefix, float(value)


def collocation_checks(ledger, science):
    """K1-K4c: every returned number recomputed locally (rigid unit solves only) and every verdict re-derived."""
    returned = af.read(science / "collocation-controls.json")
    with tempfile.TemporaryDirectory() as scratch:
        mine = collocation.collocation_controls(scratch)
    theirs = dict(leaves({k: v for k, v in returned.items() if k != "wall_seconds"}))
    ours = dict(leaves({k: v for k, v in mine.items() if k != "wall_seconds"}))
    if set(theirs) != set(ours):
        ledger.find(
            "control",
            "collocation-controls",
            "returned fields differ from a local recompute",
        )
    for key in sorted(set(theirs) & set(ours)):
        a, b = ours[key], theirs[key]
        if isinstance(a, float) and isinstance(b, float):
            ledger.compare(f"collocation-controls.{key}", a, b)
        elif a != b:
            ledger.find(
                "control", f"collocation-controls.{key}", {"local": a, "returned": b}
            )
    plateau = returned["chord_plateau_relative_range"]
    rederived = {
        "K1_exact_repair": max(
            returned["computed_CL"]["repaired"]["relative_error_to_cfd04"].values()
        )
        <= collocation.TIGHT,
        "K2_baseline_unchanged": max(
            returned["computed_CL"]["baseline"]["relative_error_to_cfd04"].values()
        )
        <= collocation.TIGHT,
        "K3_rectangle_invariance": returned["rectangle"]["max_abs_C_change_m"]
        <= collocation.TIGHT * 0.25
        and returned["rectangle"]["CL_relative_change"] <= collocation.TIGHT,
        "K4a_law_repaired": all(
            x["within_3pct"] for x in returned["law_check"]["repaired"].values()
        ),
        "K4b_quarter_chord_mutant_rejected": not all(
            x["within_3pct"]
            for x in returned["law_check"]["quarter_chord_mutant"].values()
        ),
        "K4c_chord_plateau_discriminates": max(plateau["repaired"].values()) <= 1e-4
        and min(plateau["baseline"].values()) > 1e-3,
    }
    # the cfd04 reference values themselves, not only the stored errors
    refs = collocation.references()["values"]
    for kind, by_arm in refs.items():
        for arm, points in by_arm.items():
            for point, value in points.items():
                ledger.compare(
                    f"cfd04.{kind}.{arm}.{point}",
                    mine["computed_CL"][kind][arm][point],
                    value,
                )
    for key, value in rederived.items():
        if returned["checks"].get(key) != value:
            ledger.find(
                "control",
                key,
                {"returned": returned["checks"].get(key), "rederived": value},
            )
    return {
        "rederived": rederived,
        "K4d_reported": returned["K4d_one_sided_mutant_rejected_by_plateau"],
        "chord_plateau_relative_range": plateau,
        "law_check": returned["law_check"],
        "local_recompute_wall_seconds": mine["wall_seconds"],
        "returned_wall_seconds": returned["wall_seconds"],
    }


def coupled_checks(ledger, science, arms, baseline, cp, v1):
    lattice = {}
    for mesh in v1["lattices"]:
        path = science / "repaired/lattice-controls" / f"{mesh}.json"
        if not path.is_file():
            ledger.find("missing", f"lattice-controls/{mesh}", "not returned")
            continue
        c = af.read(path)
        if c["passed"] != all(c["checks"].values()):
            ledger.find(
                "reproduction",
                f"lattice-controls/{mesh}",
                "passed flag inconsistent with checks",
            )
        lattice[mesh] = {
            "K5": all(v for k, v in c["checks"].items() if k != "upstream_force"),
            "upstream_force_reported": c["checks"].get("upstream_force"),
            "failed_checks": sorted(k for k, v in c["checks"].items() if not v),
        }
    K6 = {}
    for mesh in v1["lattices"]:
        a, b = (
            arms.get(fidelity.arm_id(chi, 20.0, mesh, "rigid")) for chi in (0.8, 0.2)
        )
        same = a is not None and b is not None
        same = same and [x["CL_on_fixed_source_area"] for x in a["iterations"]] == [
            x["CL_on_fixed_source_area"] for x in b["iterations"]
        ]
        same = same and all(
            a["flight"][d]["range_m"] == b["flight"][d]["range_m"]
            for d in ["main", "half"]
        )
        K6[mesh] = bool(same)
    K7 = []
    for item in cp["baseline_references"]:
        name = Path(item["path"]).parent.name
        ref_path = model.ROOT / item["path"]
        if af.digest(ref_path) != item["sha256"]:
            ledger.find("identity", item["path"], "baseline reference bytes changed")
        ref, new = af.read(ref_path), baseline.get(name)
        if new is None:
            K7.append({"id": name, "present": False, "within_roundoff": False})
            continue
        same = ref["status"] == new["status"] and len(ref["iterations"]) == len(
            new["iterations"]
        )
        ok, start = same, len(ledger.comparisons)
        if same:
            ok &= ledger.compare(
                f"K7.{name}.CL_history",
                [x["CL_on_fixed_source_area"] for x in new["iterations"]],
                [x["CL_on_fixed_source_area"] for x in ref["iterations"]],
            )
            tips = lambda r: [  # noqa: E731
                [
                    x["shape_validity"][f]["tip_over_L"]
                    for f in sorted(x["shape_validity"])
                ]
                for x in r["iterations"]
                if x.get("shape_validity")
            ]
            ok &= ledger.compare(f"K7.{name}.tip_over_L", tips(new), tips(ref))
            if ref["flight"] or new["flight"]:
                ok &= bool(ref["flight"] and new["flight"]) and ledger.compare(
                    f"K7.{name}.range",
                    [new["flight"][d]["range_m"] for d in ["main", "half"]],
                    [ref["flight"][d]["range_m"] for d in ["main", "half"]],
                )
        exact = same and all(x["exact"] for x in ledger.comparisons[start:])
        K7.append(
            {
                "id": name,
                "present": True,
                "status_and_counts_equal": same,
                "within_roundoff": bool(ok),
                "compared_values_exact": exact,
            }
        )
    original = af.read(science / "controls-original.json")
    return {
        "lattice_controls": lattice,
        "K5_coupled_lattice_controls": len(lattice) == len(v1["lattices"])
        and all(x["K5"] for x in lattice.values()),
        "K6_per_lattice": K6,
        "K6_determinism": all(K6.values()),
        "K7": K7,
        "K7_baseline_equivalence": len(K7) == 6
        and all(x["within_roundoff"] for x in K7),
        "original_controls": bool(original["passed"]),
    }


def analysis(ledger, arms, native, v1, p, tolerance):
    recomputed = af.recompute_effects(arms, v1, p, tolerance)
    rows = []
    for context in native["contexts"]:
        key = f"chi{context['compliance']}-u{context['speed_m_s']:g}"
        mine = recomputed[key]
        row = {
            "context": key,
            "assessable": (mine["assessable"], context["assessable"]),
        }
        if mine["assessable"] != context["assessable"]:
            ledger.find("analysis_disagreement", key, row)
        if mine["assessable"] and context["assessable"]:
            for effect in [
                "dCL_one_way_minus_rigid",
                "dCL_two_way_minus_one_way",
                "CL_rigid",
            ]:
                row[effect] = (mine[effect], context["effects"][effect]["status"])
            row["decision"] = (
                mine["decision"],
                {k: v["decision"] for k, v in context["decision"].items()},
            )
            if (
                any(
                    a != b
                    for a, b in (
                        row[e]
                        for e in [
                            "dCL_one_way_minus_rigid",
                            "dCL_two_way_minus_one_way",
                            "CL_rigid",
                        ]
                    )
                )
                or row["decision"][0] != row["decision"][1]
            ):
                ledger.find("analysis_disagreement", key, row)
            for label, effect in [
                ("bending", "dCL_one_way_minus_rigid"),
                ("feedback", "dCL_two_way_minus_one_way"),
            ]:
                series = context["descriptive_series"][effect]
                ledger.compare(
                    f"series.{key}.{effect}",
                    [mine["series"][label][m] for m in v1["lattices"]],
                    [series[m] for m in v1["lattices"]],
                )
        elif not context["assessable"]:
            for decision in context["decision"].values():
                if decision["decision"] != "undetermined":
                    ledger.find(
                        "analysis_disagreement", key, "unassessable context decided"
                    )
        rows.append(row)
    return recomputed, rows


def audit(raw, report):
    raw = Path(raw)
    science = raw / "science"
    cp, v1, fa, p = (
        collocation.cprotocol(),
        fidelity.fprotocol(),
        af.frozen(),
        model.protocol(),
    )
    ledger = af.Ledger(fa["tolerance"])
    ident = identity(ledger, raw, science, cp)
    names = p["parameters"]["arms"]
    declared = [
        fidelity.arm_id(c["compliance"], c["speed_m_s"], m, a)
        for c in cp["contexts"]
        for m in v1["lattices"]
        for a in names
    ]
    arms, records, statuses = audit_arms(
        ledger, science / "repaired", declared, "repaired", p
    )
    base_declared = [Path(x["path"]).parent.name for x in cp["baseline_references"]]
    baseline, base_records, base_statuses = audit_arms(
        ledger, science / "baseline-equivalence", base_declared, "baseline", p
    )
    if (science / "task-failures.json").is_file():
        for row in af.read(science / "task-failures.json"):
            ledger.find("native_task_crash", row["task"], row["error"])
    colloc = collocation_checks(ledger, science)
    coupled = coupled_checks(ledger, science, arms, baseline, cp, v1)
    gating = {
        **colloc["rederived"],
        **{
            k: coupled[k]
            for k in [
                "K5_coupled_lattice_controls",
                "K6_determinism",
                "K7_baseline_equivalence",
                "original_controls",
            ]
        },
    }
    native = af.read(science / "summary.json")
    if native["gating_controls"] != gating or native["study_valid"] != all(
        gating.values()
    ):
        ledger.find(
            "analysis_disagreement",
            "gating",
            {"native": native["gating_controls"], "audit": gating},
        )
    for key, value in [
        ("declared_arms", len(declared)),
        ("returned_arms", len(arms)),
        (
            "valid_arms",
            sum(bool(x["valid_for_declared_transfer"]) for x in arms.values()),
        ),
    ]:
        if native[key] != value:
            ledger.find(
                "analysis_disagreement", key, {"native": native[key], "audit": value}
            )
    recomputed, agreement = analysis(ledger, arms, native, v1, p, fa["tolerance"])
    result = {
        "schema": "frontier.aeroelastic.collocation-return-audit/1",
        "basis": "Per-arm checks are the frozen fidelity-v1 return audit (audit_fidelity.py, sha256 "
        f"{af.digest(Path(af.__file__))}, protocol {af.digest(af.FID / 'return-audit-protocol.json')}), "
        "unchanged, with the arm's own variant installed. The study-specific checks here were written after "
        "the return arrived and after its native summary.json had been read; they apply the frozen "
        "collocation-paired-v1 protocol's thresholds and change none.",
        "collocation_protocol_sha256": af.digest(collocation.CP / "protocol.json"),
        "audit_code_sha256": af.digest(Path(__file__)),
        "raw_return": str(raw),
        "identity": ident,
        "declared_arms": {
            "repaired": len(declared),
            "baseline_equivalence": len(base_declared),
        },
        "native_statuses": statuses,
        "baseline_equivalence_statuses": base_statuses,
        "arms": records,
        "baseline_equivalence_arms": base_records,
        "collocation_controls": colloc,
        "coupled_controls": coupled,
        "gating_rederived": gating,
        "study_valid_rederived": all(gating.values()),
        "recomputed_effects_and_decisions": recomputed,
        "agreement_with_native_summary": agreement,
        "findings": ledger.findings,
        "finding_counts": {
            k: sum(x["kind"] == k for x in ledger.findings)
            for k in sorted({x["kind"] for x in ledger.findings})
        },
        "comparisons": {
            "count": len(ledger.comparisons),
            "exact": sum(x["exact"] for x in ledger.comparisons),
            "within_roundoff": sum(x["within_roundoff"] for x in ledger.comparisons),
            "worst": sorted(ledger.comparisons, key=lambda x: -x["max_abs_difference"])[
                :20
            ],
        },
        "blocking_kinds": sorted(BLOCKING),
        "audit_passed": not any(x["kind"] in BLOCKING for x in ledger.findings),
        "scope": "Offline reproduction and consistency of the returned bytes and saved states, local rigid "
        "unit-solve recompute of the collocation controls, and an independent recomputation of the frozen "
        "classification. No arm is rerun; not empirical validation, not fish performance.",
    }
    dump(Path(report), result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    r = audit(args.raw, args.report)
    print(
        {k: r[k] for k in ["audit_passed", "study_valid_rederived", "finding_counts"]}
        | {"comparisons": r["comparisons"]["count"], "exact": r["comparisons"]["exact"]}
    )
    raise SystemExit(0 if r["audit_passed"] else 1)
