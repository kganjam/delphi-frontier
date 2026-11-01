"""One inspectable evidence-directed validation cycle (SPEC-017): candidate -> pinned checks -> changed evidence -> downstream invalidation -> proposed next Action.

The case: the exact existing assembly fish3d-v3a (its pinned files) and the END-LOADED cantilever mechanical slice (tip point load, delta = P L^3 / (3 EI)),
kept apart from the uniformly loaded beam (q L^4 / (8 EI)). Everything reuses what exists: fin_mechanics.beam (law, FEM, validity gate), the compiler's
plan/result artifacts and `evaluate_validation`/`compile_design`/`propagate`/`compile_inverse`, the DOE's typed instrument contracts, the
experimental_design planner and the Artifact/Evidence/Problem/Action Chain/bundle adapter. Nothing is built twice and nothing runs in a database or a cloud.

Phases (the pattern of cantilever_demo): `freeze` writes protocol.json, which must be committed; `run` refuses an untracked or modified protocol and writes the
cycle artifacts; `bundle --source-commit <sha>` reads those artifacts from an immutable commit and prepares the importable bundle. A proposed Action is a
record of intent, never executed. No aggregate biological probability exists anywhere in the output, and failed or unresolved dimensions are kept."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import re
import shutil
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import numpy as np

from engineering.experimental_design.cantilever_demo import _require_committed_protocol, build_cantilever_protocol
from engineering.experimental_design.planner import plan_experiments, sha256_json
from engineering.fin_mechanics import beam

from . import genotype as G

ROOT = Path(__file__).resolve().parents[2]
CYCLE = "artifacts/validation-cycle"
PROTOCOL_SCHEMA = "frontier.validation-cycle.protocol/2"
PLAN_VERSION = 2  # version 1 is retained under superseded/v1-8877fdc
V1 = {"commit": "8877fdcf09613f894f157bfa4272ba4f2dbad1a9", "protocol_sha256": "eef454f1614e67f76b0645999a352d5e15879c2870a4406322adb7ca33d5521d"}
SUMMARY_SCHEMA = "frontier.validation-cycle.summary/1"
CANDIDATE = "fish3d-v3a"
ASSEMBLY = f"artifacts/biodesign-compiler/assemblies/{CANDIDATE}.json"
FINMECH = "engineering/fin_mechanics/artifacts/result.json"
CONTROLS = "artifacts/assurance-experiments/controls.json"
ALLOM = "artifacts/observed-allometry/run/update.json"
ALLOM_RECEIPT = "artifacts/observed-allometry/run/receipt.json"
LEDGER = "artifacts/sequence-evidence/ledger.json"
VALIDATOR = {
    "role": "same-code numerical cross-check (procedural and dependent; NOT an independent validation)",
    "identity": "validation-cycle replay (this module)",
    "dependence_identity": "shares fin_mechanics.beam, the closed forms and the recorded inputs with the producer; independent of the producer's run and outputs only in that it recomputes them",
}
# The mechanical-slice context. It states what the slice is and is not; the biological fields are explicit about being unestablished.
CONTEXT = {
    "species": "not established: a design candidate, not an organism",
    "tissue": "fin ray modelled as a constant-EI cantilever (assumed)",
    "cell_state": "not applicable to the mechanical slice",
    "life_stage": "not established",
    "condition": "static end load, small deflection",
    "allele": "none: no sequence is claimed",
    "construct_context": "none: the sequence reference is unresolved",
}


def _read(rel: str, root: Path = ROOT) -> bytes:
    return (root / rel).read_bytes()


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _file_pin(rel: str, root: Path = ROOT) -> dict:
    return {"path": rel, "sha256": _sha(_read(rel, root))}


def dump(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text)
    return _sha(text.encode())


# ------------------------------------------------------------------------------------------------------------------ the frozen protocol
def operating_point(root: Path = ROOT) -> dict:
    """The declared point comes from the pinned fin_mechanics receipt (exact fractions), not from this module."""
    r = json.loads(_read(FINMECH, root))
    ex = r["load_bridge"]["exact"]
    return {"P_N": float(Fraction(ex["F_total_N"])), "L_m": float(Fraction(ex["L_ray_m"])), "P_exact": ex["F_total_N"], "L_exact": ex["L_ray_m"], "EI_crit_Nm2": float(Fraction(r["critical_stiffness"]["EI_crit_Nm2_exact"])), "EI_status": r["EI_assumed_range"]["status"], "limits": r["validity"]["policy"]}


TIP_OVER_L_MAX, SLOPE_MAX_RAD = 0.1, 0.2  # beam.check_small_deformation defaults, the declared small-deflection limits


def end_loaded_crit(P: float, L: float) -> float:
    """Smallest EI for which an END-LOADED cantilever stays inside the declared limits: tip/L <= 0.1 and slope <= 0.2 rad."""
    return max(P * L**2 / (3.0 * TIP_OVER_L_MAX), P * L**2 / (2.0 * SLOPE_MAX_RAD))


def build_protocol(root: Path = ROOT) -> dict:
    op = operating_point(root)
    reused = {k: _file_pin(v, root) for k, v in {"fin_mechanics_receipt": FINMECH, "analytic_controls": CONTROLS, "observed_allometry_update": ALLOM, "observed_allometry_receipt": ALLOM_RECEIPT}.items()}
    checks = [  # (id, kind, endpoint, executable): the endpoint is the one an acceptance must have EXECUTED
        ("c-fem-vs-analytic", "executed", True, True, "end-loaded FEM tip deflection and slope equal P L^3/(3EI) and P L^2/(2EI) at the declared point"),
        ("c-negative-controls", "executed", False, True, "numerical wrong-law mutants are rejected against independent quadrature, and wrong-unit, wrong-load-case, non-finite and domain-exit variants are each refused by the same mechanical_slice path as the positive case"),
        ("c-virtual-V1", "executed", False, True, "V1-saved-deflection-section@1 on the saved FEM section"),
        ("c-virtual-V2", "executed", False, True, "V2-saved-tip-and-slope@1 on the saved FEM summary"),
        ("c-reused-receipt", "reused", False, False, "the pinned fin_mechanics receipt and analytic controls still match their pins; positive controls only, so not an acceptance check (not_applicable with its reason, never a pass)"),
    ]
    return {
        "schema": PROTOCOL_SCHEMA,
        "version": 2,
        "supersedes": {**V1, "reason": "version 1 (retained under superseded/v1-8877fdc) tested only a local unit set, hardcoded some case counts, labelled a dependent cross-check independent and let a pin fall back to itself; acceptance is re-frozen here"},
        "candidate": {"id": CANDIDATE, "assembly": _file_pin(ASSEMBLY, root), "sequence": "unresolved: no sequence is claimed", "context": CONTEXT, "scope": "the mechanical slice of an assembly of pinned files; not a genome, not a construct and not a flyable or viable animal"},
        "slice": {
            "name": "end-loaded cantilever (tip point load)",
            "law": "delta = P L^3 / (3 EI)",
            "not_this_law": "uniformly loaded beam: delta = q L^4 / (8 EI)",
            "operating_point": {k: op[k] for k in ("P_N", "L_m", "P_exact", "L_exact")},
            "EI_crit_uniform_load_receipt_Nm2": op["EI_crit_Nm2"],
            "EI_crit_end_loaded_Nm2": end_loaded_crit(op["P_N"], op["L_m"]),
            "EI_crit_note": "the receipt's critical EI is for its UNIFORM pressure load; the end-loaded slice needs its own, derived here from P L^3/(3EI) and P L^2/(2EI) with the declared limits",
            "EI_status": op["EI_status"],
            "EI_positive_multiple_of_crit": 2.0,
            "EI_domain_exit_multiple_of_crit": 0.5,
            "n_elements": 64,
            "load_case": "end_load_at_tip",
            "refused_load_cases": ["uniform_pressure", "uniform_line_load", "distributed"],
            "units": {"P": "N", "L": "m", "EI": "N m^2", "delta": "m", "slope": "rad"},
        },
        "tolerances": {"fem_vs_analytic_rel": 1e-6, "mutant_must_exceed_rel": 1e-3, "V1_max_abs_over_L": 1e-4, "V2_tip_rel": 1e-7},
        "required_checks": [{"id": i, "kind": k, "endpoint": e, "executable": x, "what": w} for i, k, e, x, w in checks],
        "acceptance": "A mechanical-slice pass needs every required check to pass AND at least one executed required endpoint with a positive and a rejected negative case. Zero checks, all-optional checks, a missing, stale, blocked or not_run required check never earn it. A pass licenses the mechanical slice for the declared point only.",
        "reused": reused,
        "bio_bridge": {"interface": "I3", "bridge": "growth->EI (flexural rigidity)", "required_readout": "a calibrated EI of the candidate's rays in the stated tissue and stage, with unit and bounds; EI is an assumed range here"},
        "sequence_reference": {"state": "unresolved", "ledger_entry": "LEN-P2-positive", "why": "GRCz11 coordinates for the tested element are unresolved in the ledger"},
        "next_measurement": {
            "base_contract": "engineering.experimental_design.cantilever_demo.build_cantilever_protocol",
            "noise_variance_multiples": [0.25, 1.0, 4.0],
            "mixed_cost_multiples": [0.5, 1.0, 2.0],
            "assumptions": "priors, noise and costs are declared, not calibrated; selection is by expected target-variance reduction per assumed cost",
        },
        "not_claimed": [
            "a working or validated fin, ray, genome or organism",
            "that EI of any real fin ray is known (assumed range only)",
            "any biological success probability (none is computed)",
            "that the observed-allometry update validates fin mechanics or sequence-function (it is separate observed-data evidence, and it worsened held-out error)",
            "that the validator is independent: it is a same-code numerical cross-check, procedural and dependent",
            "that the input gate validates the producer receipt (it refuses offered inputs with a wrong unit or load case; a value mislabelled with an accepted unit passes it)",
        ],
    }


def freeze(root: Path = ROOT, out: Path | None = None) -> str:
    p = (out or root / CYCLE) / "protocol.json"
    return dump(p, build_protocol(root))


# ------------------------------------------------------------------------------------------------------------------ the executed checks
def _tip_slope_analytic(P, L, EI):
    return beam.tip_deflection_point_load(P, L, EI), beam.max_slope_point_load(P, L, EI)


class ContextRefused(ValueError):
    """The slice's input gate refused an offered operating context. It validates what is OFFERED to this computation (load case, units, finite positive
    values). It does not validate any producer's receipt, and it cannot catch a value mislabelled with an accepted unit."""

    def __init__(self, reasons):
        super().__init__("; ".join(reasons))
        self.reasons = list(reasons)


GATE_LIMITS = [
    "the gate compares the offered unit and load case with the slice's declared ones; a metadata mismatch refuses the offered input, it does not validate the producer's receipt",
    "no unit conversion is done and a value mislabelled with an accepted unit passes the gate; only the numerical cross-checks can catch that",
]


def declared_context(protocol: dict, EI_multiple: float | None = None) -> dict:
    s = protocol["slice"]
    op, u = s["operating_point"], s["units"]
    m = s["EI_positive_multiple_of_crit"] if EI_multiple is None else EI_multiple
    return {"load_case": s["load_case"], "P": {"value": op["P_N"], "unit": u["P"]}, "L": {"value": op["L_m"], "unit": u["L"]}, "EI": {"value": m * s["EI_crit_end_loaded_Nm2"], "unit": u["EI"]}}


def validate_context(protocol: dict, ctx: dict) -> list[str]:
    """The ONE operating-context/unit path: the positive computation calls it, and every wrong-unit or wrong-load variant goes through it."""
    s = protocol["slice"]
    why = []
    if ctx.get("load_case") != s["load_case"]:
        why.append(f"load case {ctx.get('load_case')!r} is not the slice's {s['load_case']!r} (refused: {', '.join(s['refused_load_cases'])})")
    for q in ("P", "L", "EI"):
        e = ctx.get(q)
        v = e.get("value") if isinstance(e, dict) else None
        if not (isinstance(v, (int, float)) and not isinstance(v, bool) and np.isfinite(v) and v > 0):
            why.append(f"{q}: needs a finite positive value")
        elif e.get("unit") != s["units"][q]:
            why.append(f"{q}: unit {e.get('unit')!r} is not the slice's {s['units'][q]!r} (no conversion is done)")
    return why


def mechanical_slice(protocol: dict, ctx: dict) -> dict:
    """Validate the offered context through the shared gate, then solve the end-loaded cantilever with the strict small-deflection gate and compare with the closed form."""
    why = validate_context(protocol, ctx)
    if why:
        raise ContextRefused(why)
    s, tol = protocol["slice"], protocol["tolerances"]
    P, L, EI = ctx["P"]["value"], ctx["L"]["value"], ctx["EI"]["value"]
    sol, chk = beam.solve_checked(L, EI, n_el=s["n_elements"], tip_force=P, strict=True)  # raises SmallDeformationViolation outside the declared domain
    tip_a, slope_a = _tip_slope_analytic(P, L, EI)
    tip_rel = abs(sol.tip - tip_a) / tip_a
    slope_rel = abs(sol.max_abs_slope - slope_a) / slope_a
    xs = np.linspace(0.0, L, 33)
    w_saved, _ = sol.evaluate(xs)
    w_ref = beam.w_point_load(xs, P, L, EI)
    cases = [{"case": "FEM tip vs P L^3/(3EI)", "rel_error": tip_rel, "ok": tip_rel <= tol["fem_vs_analytic_rel"]}, {"case": "FEM max slope vs P L^2/(2EI)", "rel_error": slope_rel, "ok": slope_rel <= tol["fem_vs_analytic_rel"]}]
    return {
        "EI_Nm2": EI,
        "tip_m": sol.tip,
        "tip_analytic_m": tip_a,
        "tip_over_L": chk["tip_over_L"],
        "max_slope_rad": sol.max_abs_slope,
        "validity": chk,
        "cases": cases,
        "saved_section": {"x_m": xs.tolist(), "w_saved_m": w_saved.tolist(), "w_analytic_m": w_ref.tolist(), "w_saved_sha256": _sha(np.asarray(w_saved).tobytes())},
        "passed": all(c["ok"] for c in cases),
    }


def check_mechanical(protocol: dict) -> dict:
    """Executed: the declared context through the shared gate and the strict solve."""
    return mechanical_slice(protocol, declared_context(protocol))


def _through_the_slice(protocol: dict, ctx: dict) -> dict:
    try:
        mechanical_slice(protocol, ctx)
        return {"kind": "accepted", "text": ""}
    except ContextRefused as e:
        return {"kind": "ContextRefused", "text": "; ".join(e.reasons)}
    except beam.SmallDeformationViolation as e:
        return {"kind": "SmallDeformationViolation", "text": str(e)}


def check_negative_controls(protocol: dict) -> dict:
    """Executed. Numerical wrong-law controls (against independent quadrature) are kept apart from the gate controls, whose wrong-unit and wrong-load variants are
    fed through the SAME `mechanical_slice` path as the positive case and must be refused for their intended reason. Positive controls show the same paths accept."""
    s, tol = protocol["slice"], protocol["tolerances"]
    base = declared_context(protocol)
    law = []
    for name, fn in (("uniform-load law applied to an end load", lambda P, L, EI_: beam.tip_deflection_uniform(P, L, EI_)), ("L^3 -> L^2 mutation", lambda P, L, EI_: P * L**2 / (3.0 * EI_))):
        worst = max(r["tip_load_rel_residual"] for r in beam.control_residuals(tip_fn=fn).values())
        law.append({"id": "law:" + name, "via": "beam.control_residuals", "intended_failure": "closed form disagrees with independent quadrature", "observed_rel_residual": worst, "rejected": worst > tol["mutant_must_exceed_rel"]})

    def variant(**changes):
        c = copy.deepcopy(base)
        for k, v in changes.items():
            if isinstance(v, dict):
                c[k] = {**c[k], **v}
            else:
                c[k] = v
        return c

    gate = []
    for cid, why, want_kind, want_text, ctx in (
        ("unit:EI in N mm^2", "wrong unit for EI", "ContextRefused", "EI: unit", variant(EI={"unit": "N mm^2", "value": base["EI"]["value"] * 1e6})),
        ("unit:P in kgf", "wrong unit for the load", "ContextRefused", "P: unit", variant(P={"unit": "kgf", "value": base["P"]["value"] / 9.80665})),
        ("context:uniformly loaded claim", "wrong load case for the slice", "ContextRefused", "load case", variant(load_case="uniform_pressure")),
        ("context:non-finite EI", "value not finite", "ContextRefused", "finite positive", variant(EI={"value": float("nan")})),
        ("domain:EI below the end-loaded critical", "small-deformation limit exceeded", "SmallDeformationViolation", "LINEAR_MODEL_INVALID", declared_context(protocol, s["EI_domain_exit_multiple_of_crit"])),
        ("context:uniform-load critical EI used for the end load", "wrong load case for the stiffness threshold", "SmallDeformationViolation", "LINEAR_MODEL_INVALID", variant(EI={"value": s["EI_crit_uniform_load_receipt_Nm2"] * s["EI_positive_multiple_of_crit"]})),
    ):
        got = _through_the_slice(protocol, ctx)
        gate.append({"id": cid, "via": "validation_cycle.mechanical_slice", "intended_failure": why, "expected": want_kind, "observed": got["kind"], "refusal": got["text"], "rejected": got["kind"] == want_kind and want_text in got["text"]})
    positives = [
        {"id": "declared context accepted by the same path", "via": "validation_cycle.mechanical_slice", "ok": _through_the_slice(protocol, base)["kind"] == "accepted"},
        {"id": "correct closed form passes the quadrature test", "via": "beam.control_residuals", "ok": max(r["tip_load_rel_residual"] for r in beam.control_residuals().values()) < 1e-12},
    ]
    controls = law + gate
    return {"controls": controls, "law_controls": law, "gate_controls": gate, "positive_controls": positives, "all_rejected": all(c["rejected"] for c in controls), "all_positive_ok": all(p["ok"] for p in positives), "gate_limits": GATE_LIMITS}


def _contract_number(contracts: dict, iid: str, pattern: str) -> float | None:
    """The tolerance a virtual instrument's own contract states, read from the typed contract file (not from this module)."""
    rows = json.loads(_read(G.INSTRUMENT_FILE))["contracts"]
    row = next((r for r in rows if r.get("instrument id and version", "").startswith(iid + "@")), None)
    m = re.search(pattern, (row or {}).get("acceptance", ""))
    return float(m.group(1)) if m else None


def check_virtual(protocol: dict, mech: dict, contracts: dict) -> dict:
    """Executed: V1 and V2 evaluated on the saved FEM section with the acceptance their typed contracts state. Each also gets a negative case executed here: a
    saved section or tip from the WRONG load law, which its own acceptance must reject. Case counts are what was evaluated."""
    tol = protocol["tolerances"]
    op = protocol["slice"]["operating_point"]
    L = op["L_m"]
    v1_tol = _contract_number(contracts, "V1-saved-deflection-section", r"<=\s*([0-9.e+-]+)")
    v2_tol = _contract_number(contracts, "V2-saved-tip-and-slope", r"<=\s*([0-9.e+-]+)")
    sec = mech["saved_section"]
    xs = np.array(sec["x_m"])
    ref = np.array(sec["w_analytic_m"])
    v1 = float(np.max(np.abs(np.array(sec["w_saved_m"]) - ref)) / L)
    v2 = abs(mech["tip_m"] - mech["tip_analytic_m"]) / mech["tip_analytic_m"]
    EI = mech["EI_Nm2"]
    wrong_w = beam.w_uniform(xs, 8.0 * EI * mech["tip_analytic_m"] / L**4, L, EI)  # a uniformly loaded shape with the SAME tip: right size, wrong law
    v1_neg = float(np.max(np.abs(wrong_w - ref)) / L)
    v2_neg = abs(beam.tip_deflection_uniform(op["P_N"] / L, L, EI) - mech["tip_analytic_m"]) / mech["tip_analytic_m"]
    bound = (v1_tol == tol["V1_max_abs_over_L"]) and (v2_tol == tol["V2_tip_rel"])
    return {
        "V1": {"value": v1, "tolerance": v1_tol, "ok": v1 <= (v1_tol or 0), "positive_cases": 1, "negative": {"case": "uniformly loaded shape with the same tip", "value": v1_neg, "rejected": v1_neg > (v1_tol or float("inf"))}},
        "V2": {"value": v2, "tolerance": v2_tol, "ok": v2 <= (v2_tol or 0), "positive_cases": 1, "negative": {"case": "uniform-load tip formula for an end load", "value": v2_neg, "rejected": v2_neg > (v2_tol or float("inf"))}},
        "protocol_tolerances_match_the_contracts": bound,
        "contract_refs": {k: v for k, v in {i: contracts["contracts"].get(i) for i in ("V1-saved-deflection-section", "V2-saved-tip-and-slope")}.items()},
    }


def check_reused(protocol: dict, root: Path = ROOT) -> dict:
    """Reused: the pinned fin_mechanics receipt and analytic controls. Their bytes must still match the frozen pins; nothing here reruns them. Counts are read from
    the pinned records: the receipt holds analytic POSITIVE controls only, and controls.json's mutant is the glide speed law, so no cantilever negative case is recorded."""
    pins = {k: v for k, v in protocol["reused"].items() if k in ("fin_mechanics_receipt", "analytic_controls")}
    moved = [v["path"] for v in pins.values() if not (root / v["path"]).is_file() or _sha(_read(v["path"], root)) != v["sha256"]]
    r = json.loads(_read(FINMECH, root))
    c = json.loads(_read(CONTROLS, root))
    analytic = r["controls"]["analytic_residuals_vs_independent_quadrature"]
    holding = sum(1 for case in analytic.values() if case["tip_load_rel_residual"] < 1e-12)
    ok = not moved and r.get("verdict") == "ok" and c.get("passed") is True and holding == len(analytic) > 0
    return {
        "changed_pins": moved,
        "receipt_verdict": r.get("verdict"),
        "controls_passed": c.get("passed"),
        "analytic_cases_in_receipt": len(analytic),
        "positive_cases_holding": holding,
        "negative_cases_in_receipt": None,
        "negative_case_note": "unavailable: the pinned receipt records positive analytic controls only, and controls.json's mutant is the glide speed law, not the cantilever",
        "max_rel_residual": r["controls"]["max_rel_residual"],
        "passed": ok,
        "not_rerun": True,
    }


PIN_KEYS = ("fin_mechanics_receipt", "analytic_controls", "observed_allometry_update")


def verify_pins(protocol: dict, root: Path) -> dict:
    """Which pinned inputs of the mechanical slice still match their bytes. The expected hash of beam.py comes ONLY from the producer's receipt: if the receipt
    carries none, the result is `missing_pin`, never a self-verification against the current file."""
    pins = {k: protocol["reused"][k] for k in PIN_KEYS} | {"assembly": protocol["candidate"]["assembly"]}
    out = {}
    for k, v in pins.items():
        f = root / v["path"]
        out[k] = "missing_file" if not f.is_file() else ("verified" if _sha(f.read_bytes()) == v["sha256"] else "changed")
    code = root / "engineering/fin_mechanics/beam.py"
    try:
        want = json.loads(_read(FINMECH, root))["code_files_sha256"]["beam.py"]
    except (OSError, ValueError, KeyError, TypeError):
        want = None
    out["beam_code"] = "missing_pin" if not isinstance(want, str) or len(want) != 64 else ("missing_file" if not code.is_file() else ("verified" if _sha(code.read_bytes()) == want else "changed"))
    return out


PINNED_FILES = ("engineering/fin_mechanics/beam.py", "artifacts/fish-regulatory-map/map.json", "artifacts/cfd3d/vlm/fish3d-v3a-fan/vlm.json")


def stage_pinned(tmp: Path, protocol: dict) -> Path:
    """A copy of exactly the files the slice's pins and checked layers read, so a test or the changed-input case can alter one byte of the copy."""
    for rel in [protocol["reused"][k]["path"] for k in PIN_KEYS] + [protocol["candidate"]["assembly"]["path"], *PINNED_FILES]:
        (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / rel, tmp / rel)
    return tmp


# ------------------------------------------------------------------------------------------------------------------ plan/result artifacts, then the compiler
def _write_artifacts(out: Path, protocol: dict, assembly_sha: str, results: dict) -> tuple[list, list, dict]:
    """The mechanical-slice plan and one result artifact per executed or reused check, written as compiler plan/result artifacts whose bytes bind the candidate."""
    rel = lambda name: f"{CYCLE}/{name}"  # noqa: E731
    checks = [{"id": c["id"], "interface": None, "layer": "shape_mechanics", "endpoint": c["endpoint"], "executable": c["executable"], "kind": c["kind"], "what": c["what"]} for c in protocol["required_checks"]]
    meta = {
        "id": "vp-mech-end-loaded-cantilever",
        "version": PLAN_VERSION,
        "candidate_id": CANDIDATE,
        "endpoint": "end-loaded cantilever tip deflection and slope at the declared point, small-deflection domain",
        "decision": "whether the mechanical slice of the assembly may be used as a numerical stand-in; never whether the fin or animal works",
        "required_checks": checks,
        "candidate_assembly_sha256": assembly_sha,
        "protocol_sha256": _sha((out / "protocol.json").read_bytes()),
    }
    dump(out / "plans/plan-vp-mech-end-loaded-cantilever.json", {"schema": G.PLAN_SCHEMA, **meta})
    plan = {**{k: meta[k] for k in ("id", "version", "candidate_id", "endpoint", "decision", "required_checks")}, "ref": _file_pin(rel("plans/plan-vp-mech-end-loaded-cantilever.json"), out.parent.parent)}
    res_list = []
    for cid, r in results.items():
        doc = {
            "schema": G.RESULT_SCHEMA,
            "plan_id": meta["id"],
            "plan_version": PLAN_VERSION,
            "check_id": cid,
            "status": r["status"],
            "cases": r["cases"],
            "scope": r["scope"],
            "licenses": r.get("licenses"),
            "validator": VALIDATOR,
            "candidate_assembly_sha256": assembly_sha,
            "execution": r["execution"],
            "reused_pin": r.get("reused_pin"),
            **({"reason": r["reason"]} if "reason" in r else {}),
        }
        dump(out / f"results/res-{cid}.json", doc)
        res_list.append(
            {
                "plan_id": meta["id"],
                "plan_version": PLAN_VERSION,
                "check_id": cid,
                **({"reason": r["reason"]} if "reason" in r else {}),
                "status": r["status"],
                "cases": r["cases"],
                "scope": r["scope"],
                "licenses": r.get("licenses"),
                "candidate_sequence_sha256": None,
                "ref": _file_pin(rel(f"results/res-{cid}.json"), out.parent.parent),
            }
        )
    # The two biological dimensions the cycle cannot execute are plans with NO result: the compiler reports them as missing, never as a pass or a failure.
    plans = [plan]
    for pid, cid, iface, endpoint_text, what in (
        ("vp-bio-bridge-growth-to-EI", "c-growth-to-EI", "I3", "calibrated EI of the candidate's rays in the stated tissue and stage", protocol["bio_bridge"]["required_readout"]),
        ("vp-seq-functional-readout", "c-functional-readout", "I1", "matched functional readout of the exact tested sequence in the stated context", protocol["sequence_reference"]["why"]),
    ):
        pm = {
            "id": pid,
            "version": PLAN_VERSION,
            "candidate_id": CANDIDATE,
            "endpoint": endpoint_text,
            "decision": "whether any functional claim may be made",
            "required_checks": [{"id": cid, "interface": iface, "endpoint": True, "executable": False, "kind": "not_run", "what": what}],
            "candidate_assembly_sha256": assembly_sha,
        }
        dump(out / f"plans/plan-{pid}.json", {"schema": G.PLAN_SCHEMA, **pm})
        plans.append({**{k: pm[k] for k in ("id", "version", "candidate_id", "endpoint", "decision", "required_checks")}, "ref": _file_pin(rel(f"plans/plan-{pid}.json"), out.parent.parent)})
    return plans, res_list, meta


def _results(protocol: dict, mech, neg, virt, reused) -> dict:
    """Case counts are what was executed or read from the pinned records; nothing here is a constant."""
    n = len(neg["controls"])
    pos_cases = sum(1 for c in mech["cases"] if c["ok"])
    pos_controls = sum(1 for p in neg["positive_controls"] if p["ok"])
    r = {
        "c-fem-vs-analytic": {
            "status": "pass" if mech["passed"] else "fail",
            "cases": {"positive": pos_cases, "negative": n, "negative_rejected": neg["all_rejected"]},
            "scope": "the declared point only (EI = 2 x the end-loaded critical value, assumed)",
            "licenses": "the end-loaded FEM equals the closed form at this point, inside the small-deflection domain",
            "execution": {"kind": "executed", "tip_rel_error": mech["cases"][0]["rel_error"], "tip_over_L": mech["tip_over_L"], "input_gate": "validation_cycle.mechanical_slice (units, load case, finite positive values)"},
        },
        "c-negative-controls": {
            "status": "pass" if neg["all_rejected"] and neg["all_positive_ok"] else "fail",
            "cases": {"positive": pos_controls, "negative": n, "negative_rejected": neg["all_rejected"]},
            "scope": "law, unit, load-case and domain controls for this slice; the gate refuses offered inputs, it does not validate the producer receipt",
            "licenses": "the slice refuses the wrong law, the wrong unit, the wrong load case and a domain exit",
            "execution": {"kind": "executed", "controls": neg["controls"], "positive_controls": neg["positive_controls"], "gate_limits": neg["gate_limits"]},
        },
        "c-virtual-V1": {
            "status": "pass" if virt["V1"]["ok"] and virt["protocol_tolerances_match_the_contracts"] else "fail",
            "cases": {"positive": virt["V1"]["positive_cases"], "negative": 1, "negative_rejected": virt["V1"]["negative"]["rejected"]},
            "scope": "one saved simulated case; not a biological replicate",
            "licenses": "V1-saved-deflection-section@1 on this saved section",
            "execution": {"kind": "executed", **virt["V1"]},
        },
        "c-virtual-V2": {
            "status": "pass" if virt["V2"]["ok"] and virt["protocol_tolerances_match_the_contracts"] else "fail",
            "cases": {"positive": virt["V2"]["positive_cases"], "negative": 1, "negative_rejected": virt["V2"]["negative"]["rejected"]},
            "scope": "one saved simulated case; not a biological replicate",
            "licenses": "V2-saved-tip-and-slope@1 on this saved summary",
            "execution": {"kind": "executed", **virt["V2"]},
        },
    }
    # The reused receipt holds positive analytic controls only. It cannot earn a pass (a pass needs a rejected negative case) and is not an acceptance check: not_applicable, with the reason.
    reason = f"the pinned receipt records {reused['analytic_cases_in_receipt']} analytic positive controls and no cantilever negative case; kept as pinned context for the executed checks, not as an acceptance check"
    r["c-reused-receipt"] = {
        "status": "not_applicable" if reused["passed"] else "fail",
        "reason": reason if reused["passed"] else "the pinned receipt or controls no longer hold: " + str(reused["changed_pins"]),
        "cases": {"positive": reused["positive_cases_holding"], "negative": None, "negative_rejected": None},
        "scope": "the pinned receipt only; not rerun here",
        "licenses": None,
        "execution": {"kind": "reused", **reused},
        "reused_pin": protocol["reused"]["fin_mechanics_receipt"],
    }
    return r


def _design(plans, results, protocol) -> dict:
    return {
        "schema": G.DESIGN_SCHEMA,
        "id": f"validation-cycle-{CANDIDATE}",
        "claim": "working_assembly",
        "context": copy.deepcopy(CONTEXT),
        "interface_evidence": [],
        "validation_plans": plans,
        "validation_results": results,
        "sequence_candidates": [],
        "checked_layers": [
            {"id": "regulatory-map", "node": "expression", "pins": [_file_pin("artifacts/fish-regulatory-map/map.json")]},
            {"id": "fin-mechanics-numerical", "node": "shape_mechanics", "pins": [protocol["reused"]["fin_mechanics_receipt"]]},
            {"id": "aero-numerical", "node": "performance", "pins": [_file_pin("artifacts/cfd3d/vlm/fish3d-v3a-fan/vlm.json")]},
            {"id": "observed-allometry-update", "node": "organism_context", "pins": [protocol["reused"]["observed_allometry_update"]]},
        ],
    }


def changed_input_case(protocol: dict, graph: dict, design: dict) -> dict:
    """Executed on a COPY: change one pinned mechanical input by a byte; its checks go stale, unaffected pinned checks stay verified, and the compiler's
    propagation says what the change invalidates downstream and what it retains for the original pinned model only."""
    tmp = Path(tempfile.mkdtemp(prefix="vcycle-"))
    try:
        stage_pinned(tmp, protocol)
        before = verify_pins(protocol, tmp)
        p = tmp / FINMECH  # the assumed-EI receipt: one appended byte is a changed input
        p.write_bytes(p.read_bytes() + b" ")
        after = verify_pins(protocol, tmp)
        prop = G.propagate(graph, design, {"node": "shape_mechanics"}, tmp)
        return {
            "changed_input": FINMECH,
            "bytes_changed": 1,
            "pins_before": before,
            "pins_after": after,
            "stale": [k for k in after if after[k] == "changed"],
            "retained_verified": [k for k in after if after[k] == "verified"],
            "mechanical_checks_status_after": {c["id"]: ("stale" if c["kind"] == "reused" else "needs_rerun") for c in protocol["required_checks"]},
            "propagation": prop,
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def all_optional_case(root: Path) -> dict:
    """Executed: a plan whose checks are all optional or not applicable, and a plan with no checks, must not earn acceptance."""
    out = {}
    base = {"version": 1, "candidate_id": CANDIDATE, "endpoint": "none", "decision": "none"}
    for name, checks, status in (("all_optional_not_applicable", [{"id": "o1", "endpoint": False, "executable": False}, {"id": "o2", "endpoint": False, "executable": False}], "not_applicable"), ("no_checks", [], None)):
        tmp = Path(tempfile.mkdtemp(prefix="vcycle-opt-"))
        try:
            (tmp / "p.json").write_text(json.dumps({"schema": G.PLAN_SCHEMA, "id": name, **base, "required_checks": checks}))
            plan = {"id": name, **base, "required_checks": checks, "ref": _file_pin("p.json", tmp)}
            res = []
            for c in checks:
                doc = {"schema": G.RESULT_SCHEMA, "plan_id": name, "plan_version": 1, "check_id": c["id"], "status": status, "cases": {"positive": 0, "negative": 0, "negative_rejected": False}, "validator": VALIDATOR}
                (tmp / f"r-{c['id']}.json").write_text(json.dumps(doc))
                res.append({"plan_id": name, "plan_version": 1, "check_id": c["id"], "status": status, "cases": doc["cases"], "reason": "optional", "candidate_sequence_sha256": None, "ref": _file_pin(f"r-{c['id']}.json", tmp)})
            ev = G.evaluate_validation(tmp, {"validation_plans": [plan], "validation_results": res})
            out[name] = {"all_required_pass": ev["all_required_pass"], "plans": [{"counts": p["counts"], "all_required_pass": p["all_required_pass"]} for p in ev["plans"]]}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return out


# ------------------------------------------------------------------------------------------------------------------ next measurement
def next_measurement(protocol: dict) -> dict:
    """Prospective only (no response values): the existing planner on the existing cantilever contract, with the candidate's context and a noise/cost grid."""
    spec = protocol["next_measurement"]
    base = build_cantilever_protocol()
    base["context"]["open_gaps"] = base["context"]["open_gaps"] + ["EI of the candidate's rays is an assumed range; no specimen, species bridge or sequence is pinned."]
    base["iteration"] = {"parent_versions": [], "iteration_number": 2, "rationale": "Re-run of the frozen cantilever identifiability contract for the validation cycle's missing EI bridge, with a noise and cost sensitivity grid."}
    grid = []
    for nm in spec["noise_variance_multiples"]:
        for cm in spec["mixed_cost_multiples"]:
            c = copy.deepcopy(base)
            for d in c["designs"]:
                d["noise_covariance"] = [[x * nm for x in row] for row in d["noise_covariance"]]
                if d["id"] == "mixed_load_deflection":
                    d["cost"]["value"] = d["cost"]["value"] * cm
            for r in c["readouts"]:
                r["noise_variance"] = r["noise_variance"] * nm
            res = plan_experiments(c)
            by = {d["id"]: d for d in res["designs"]}
            grid.append(
                {
                    "noise_multiple": nm,
                    "mixed_cost_multiple": cm,
                    "selected": res["selected_design_id"],
                    "reduction_per_cost": {k: v["expected_target_variance_reduction_per_cost"] for k, v in by.items()},
                    "deflection_only_identifiable": bool(by["deflection_only"]["identifiability"].get("identifiable", by["deflection_only"]["identifiability"].get("full_rank", False))),
                }
            )
    nominal = plan_experiments(base)
    sel = {g["selected"] for g in grid}
    return {
        "schema": "frontier.validation-cycle.next-measurement/1",
        "contract_sha256": nominal["normalized_contract_sha256"],
        "selected_design_id": nominal["selected_design_id"],
        "selection_objective": nominal["selection_objective"],
        "assumptions": spec["assumptions"],
        "sensitivity_grid": grid,
        "selection_flips": len(sel) > 1,
        "selected_in_every_grid_cell": sorted(sel),
        "measurement_rows": nominal["measurement_rows"],
        "executed": False,
        "status": "proposed Action only: no lab, cloud or store write; no response data was invented",
        "designs": nominal["designs"],
        "action_artifact": nominal["action_artifact"],
    }


# ------------------------------------------------------------------------------------------------------------------ the cycle
def run(root: Path = ROOT, out: Path | None = None) -> dict:
    out = out or root / CYCLE
    protocol_path = out / "protocol.json"
    if root == ROOT:
        _require_committed_protocol(protocol_path)
    protocol = json.loads(protocol_path.read_text())
    if protocol.get("schema") != PROTOCOL_SCHEMA:
        raise ValueError("unexpected protocol schema")
    stale_pins = [v["path"] for v in [protocol["candidate"]["assembly"], *protocol["reused"].values()] if _sha(_read(v["path"], root)) != v["sha256"]]
    if stale_pins:
        raise ValueError(f"frozen protocol pins changed: {stale_pins}")
    unverified = {k: v for k, v in verify_pins(protocol, root).items() if v != "verified"}
    if unverified:
        raise ValueError(f"pins not verified, refusing to run: {unverified}")
    contracts = G.instrument_contracts(root)
    graph = G.baseline_graph(root)
    mech, neg = check_mechanical(protocol), check_negative_controls(protocol)
    virt, reused = check_virtual(protocol, mech, contracts), check_reused(protocol, root)
    assembly_sha = protocol["candidate"]["assembly"]["sha256"]
    results = _results(protocol, mech, neg, virt, reused)
    plans, res_list, plan_meta = _write_artifacts(out, protocol, assembly_sha, results)
    design = _design(plans, res_list, protocol)
    dump(out / "design.json", design)
    report = G.compile_design(root, graph, design)
    inverse = G.compile_inverse(root, graph, {"schema": G.INVERSE_SCHEMA, "id": "validation-cycle-inverse", "target_node": "shape_mechanics", "candidates": [_unresolved_candidate(root)]}, design)
    changed = changed_input_case(protocol, graph, design)
    optional = all_optional_case(root)
    nxt = next_measurement(protocol)
    allom = json.loads(_read(ALLOM, root))
    ledger = json.loads(_read(LEDGER, root))
    len_entry = next(e for e in ledger["entries"] if e["id"] == "LEN-P2-positive")
    slices = G.validation_slices(graph, design, None, root)
    bridge = slices["interfaces"]["I3"]
    hist = [{"id": c["id"], "kind": c["kind"], "status": results[c["id"]]["status"], "endpoint": c["endpoint"], "what": c["what"], "pin": {"result": next(r["ref"] for r in res_list if r["check_id"] == c["id"])}} for c in protocol["required_checks"]]
    vstat = {c["id"]: c["status"] for p in report["validation"]["plans"] for c in p["checks"]}
    hist += [
        {
            "id": "c-bio-bridge-expression-to-EI",
            "kind": "not_run",
            "status": vstat["c-growth-to-EI"],
            "endpoint": True,
            "what": "growth->EI (flexural rigidity) in the candidate's rays",
            "reason": "no calibrated EI exists; EI is an assumed range; interface I3 state " + report["interface_state"]["I3"],
            "required_readout": protocol["bio_bridge"]["required_readout"],
            "recorded_bridges": bridge["recorded_bridges"],
        },
        {
            "id": "c-sequence-reference",
            "kind": "not_run",
            "status": vstat["c-functional-readout"],
            "endpoint": True,
            "what": "functional readout for the tested element",
            "reason": protocol["sequence_reference"]["why"],
            "required_readout": len_entry.get("falsifiable_validation_readout"),
            "inverse_verdict": inverse["verdict"],
            "endorsed": len(inverse.get("endorsed_candidate_set", [])),
        },
        {
            "id": "c-observed-allometry",
            "kind": "reused",
            "status": "fail",
            "endpoint": False,
            "what": "separate observed-data case: observed-subset update, held-out error",
            "reason": "held-out error worsened after the update; this is allometry evidence only, not fin mechanics and not sequence-function",
            "heldout_before": allom["heldout_before"],
            "heldout_after": allom["heldout_after"],
            "pin": protocol["reused"]["observed_allometry_update"],
        },
    ]
    dump(out / "check-history.json", {"schema": "frontier.validation-cycle.check-history/1", "candidate": CANDIDATE, "checks": hist})
    dump(out / "compile-report.json", {"compile": report, "inverse": inverse, "validation_slices_I3": bridge})
    dump(out / "changed-input.json", changed)
    dump(out / "all-optional.json", optional)
    dump(out / "next-measurement.json", nxt)
    dump(out / "mechanical-evidence.json", {"mechanical": {k: v for k, v in mech.items() if k != "saved_section"}, "saved_section": mech["saved_section"], "negative_controls": neg, "virtual": virt, "reused": reused})
    summary = _summary(protocol, report, inverse, hist, changed, optional, nxt, assembly_sha, plan_meta, res_list, protocol_path)
    dump(out / "summary.json", summary)
    files = sorted(p for p in out.rglob("*.json") if p.name not in ("manifest.json", "replay-receipt.json") and not ({"bundle", "superseded"} & set(p.relative_to(out).parts)))
    dump(
        out / "manifest.json",
        {
            "schema": "frontier.artifact-manifest/1",
            "code_sha256": {p: _sha(_read(p, root)) for p in ("engineering/biodesign_compiler/validation_cycle.py", "engineering/biodesign_compiler/genotype.py", "engineering/fin_mechanics/beam.py")},
            "environment": {"python": platform.python_version(), "numpy": np.__version__},
            "files": [{"path": str(p.relative_to(root)), "sha256": _sha(p.read_bytes()), "bytes": p.stat().st_size} for p in files],
        },
    )
    return summary


def _unresolved_candidate(root: Path) -> dict:
    return {
        "id": "len-element-unresolved",
        "sequence_unresolved": True,
        "unresolved_ref": "ledger:LEN-P2-positive (GRCz11 coordinates unresolved)",
        "evidence_kind": "measured_expression",
        "observed_context": {"species": "Danio rerio"},
        "provenance": {"proposer": "validation-cycle", "method": "ledger entry carried as an unresolved reference; no sequence generated", "source_refs": ["ledger:LEN-P2-positive"]},
    }


def _summary(protocol, report, inverse, hist, changed, optional, nxt, assembly_sha, plan_meta, res_list, protocol_path) -> dict:
    sel = nxt["selected_design_id"]
    return {
        "schema": SUMMARY_SCHEMA,
        "candidate": {"id": CANDIDATE, "assembly": protocol["candidate"]["assembly"], "sequence": "unresolved", "scope": protocol["candidate"]["scope"]},
        "verdict": {
            "working_assembly_claim": report["verdict"],
            "proposal_eligibility": report.get("proposal_eligibility"),
            "function_assurance": report.get("function_assurance"),
            "mechanical_slice": next(h["status"] for h in hist if h["id"] == "c-fem-vs-analytic"),
            "biological_success_probability": None,
            "reading": "The candidate is rejected as a working assembly; its end-loaded mechanical slice passes numerically at the declared point; the missing biological bridge and the unresolved sequence block any functional claim.",
        },
        "digest_chain": {
            "candidate_assembly_sha256": assembly_sha,
            "protocol_sha256": _sha(protocol_path.read_bytes()),
            "plan_ref": plan_meta["id"],
            "result_refs": {r["check_id"]: r["ref"]["sha256"] for r in res_list},
            "compile_design_sha256": sha256_json(report),
            "next_measurement_contract_sha256": nxt["contract_sha256"],
        },
        "reused_vs_executed": {"executed": [h["id"] for h in hist if h["kind"] == "executed"], "reused": [h["id"] for h in hist if h["kind"] == "reused"], "not_run": [h["id"] for h in hist if h["kind"] == "not_run"]},
        "dimensions": [{"id": h["id"], "status": h["status"], "kind": h["kind"], "endpoint": h["endpoint"]} for h in hist],
        "open_problems": [
            {"id": "problem-growth-to-EI", "bridge": protocol["bio_bridge"]["bridge"], "required_readout": protocol["bio_bridge"]["required_readout"]},
            {"id": "problem-sequence-reference", "state": "unresolved", "required_readout": next(h["required_readout"] for h in hist if h["id"] == "c-sequence-reference")},
        ],
        "changed_input": {
            "input": changed["changed_input"],
            "stale": changed["stale"],
            "retained_verified": changed["retained_verified"],
            "invalidated_interfaces": changed["propagation"]["invalidated_interfaces"],
            "invalidated_checked_layers": changed["propagation"]["invalidated_checked_layers"],
            "retained_checked_layers": changed["propagation"]["retained_checked_layers"],
        },
        "acceptance_guard": {k: v["all_required_pass"] for k, v in optional.items()},
        "next_action": {"status": "proposed, not executed", "design": sel, "selection_flips_in_grid": nxt["selection_flips"], "objective": nxt["selection_objective"]["name"], "assumptions": nxt["assumptions"]},
        "separate_evidence": {"observed_allometry": "held-out error worsened; context for allometry only, not fin validation"},
        "not_claimed": protocol["not_claimed"],
    }


# ------------------------------------------------------------------------------------------------------------------ the importable bundle
def prepare_bundle(source_commit: str, created_at: str, out: Path) -> dict:
    """Claim / Evidence / Problem / Action records read from the IMMUTABLE commit that holds the cycle artifacts. Documentary and proposed only: no DB submission,
    import, lease or review; the Action is a proposal and is never executed."""
    from frontier_adapters.engineering_manifest import Chain, build_bundle, link_checks, resolve_commit

    source_commit = resolve_commit(str(ROOT), source_commit)
    c = Chain(str(ROOT), source_commit, "delphi-frontier", "validation-cycle", created_at, "validation-cycle")
    protocol = c.jblob(f"{CYCLE}/protocol.json")
    summary, hist, nxt = c.jblob(f"{CYCLE}/summary.json"), c.jblob(f"{CYCLE}/check-history.json"), c.jblob(f"{CYCLE}/next-measurement.json")
    for k, v in protocol["reused"].items():
        c.same_hash("reused-pin:" + k, v["path"], v["sha256"])
    c.same_hash("candidate-assembly", protocol["candidate"]["assembly"]["path"], protocol["candidate"]["assembly"]["sha256"])
    uri = "urn:frontier:validation-cycle:documentary"

    def source(path):
        b = c.blob(path)
        return {"uri": None, "locator": f"git:delphi-frontier@{source_commit}:{path}", "source_version": source_commit, "content_sha256": _sha(b), "content_available": False, "access": "Immutable git blob read and hashed; pointers only", "license": None}

    limits = [
        "Prepared documentary records only: no DB submission, import, lease, lifecycle, acceptance or independent review.",
        "Mechanical slice only: assumed EI, small deflection, declared point; no biological calibration.",
        "The sequence reference is unresolved and no functional readout has been measured.",
        "No aggregate or biological success probability exists.",
    ]
    neg_exec = c.jblob(f"{CYCLE}/results/res-c-negative-controls.json")["execution"]  # counts come from the immutable result, not from prose
    n_ctrl = len(neg_exec["controls"])
    n_rej = sum(1 for x in neg_exec["controls"] if x["rejected"])
    st = {h["id"]: h["status"] for h in hist["checks"]}
    mech_ok, virt_ok = st["c-fem-vs-analytic"] == "pass", st["c-virtual-V1"] == "pass" and st["c-virtual-V2"] == "pass"
    claim = c.add(
        c.draft(
            "Claim",
            "validation-cycle-candidate-rejected",
            {
                "title": f"fish3d-v3a is rejected as a working assembly; its end-loaded mechanical slice {'passes' if mech_ok else 'does not pass'} at the declared point",
                "statement": f"Under the frozen protocol (version {protocol['version']}) the mechanical slice {'passes' if mech_ok else 'does not pass'} (FEM versus the closed form; {n_rej} of {n_ctrl} negative controls are refused for their intended reasons; V1 and V2 {'both hold' if virt_ok else 'do not both hold'}) while the growth-to-EI bridge and the sequence reference are missing, so the working-assembly claim is rejected.",
                "context": "A statement about the pinned assembly files and the end-loaded cantilever slice, not about an organism.",
                "assumptions": ["EI is an assumed range, not measured."],
                "limitations": limits,
                "source": source(f"{CYCLE}/summary.json"),
                "origin": "derived",
            },
            uri,
        )
    )
    action = c.add(
        c.draft(
            "Action",
            "validation-cycle-replay",
            {
                "target": claim,
                "title": "Recorded replay of the validation cycle (local, deterministic); no Store lifecycle",
                "acceptance_criteria": ["Frozen protocol pins match; every required check is reported with its status; negative controls rejected for their intended reasons."],
                "required_capabilities": ["Python, NumPy and SciPy, one CPU, no network"],
                "cost_stop_bounds": "Local deterministic replay of seconds; no provider job; dollar cost not applicable.",
                "cache_key": {
                    "target": claim["version"],
                    "input": protocol["candidate"]["assembly"]["sha256"],
                    "code": json.loads(c.blob(f"{CYCLE}/manifest.json"))["code_sha256"]["engineering/biodesign_compiler/validation_cycle.py"],
                    "model": "finmech-eb-cantilever-linear-static/1",
                    "environment": _sha(json.dumps(json.loads(c.blob(f"{CYCLE}/manifest.json"))["environment"], sort_keys=True).encode()),
                    "parameters": _sha(c.blob(f"{CYCLE}/protocol.json")),
                    "scope": "documentary already-executed local validation; not consumed before the run",
                    "acceptance_policy": "frontier-independent-review-0.1",
                },
            },
            uri,
        )
    )
    c.add(
        c.draft(
            "Evidence",
            "validation-cycle-mechanical-evidence",
            {
                "target": claim,
                "evidence_kind": "simulated",
                "source": source(f"{CYCLE}/mechanical-evidence.json"),
                "created_time": {"value": None, "basis": "unknown"},
                "retrieved_time": {"value": created_at, "basis": "declared"},
                "method": "Executed: FEM versus closed form with the strict validity gate; law, unit, context and domain negative controls; V1 and V2 on the saved section. Reused (not rerun): the pinned fin_mechanics receipt and analytic controls.",
                "context": "End-loaded cantilever, assumed EI = 2 x the end-loaded critical value, declared P and L from the pinned receipt.",
                "assumptions": ["Euler-Bernoulli, linear elastic, static, constant EI."],
                "provenance": {"adapter": "engineering.biodesign_compiler.validation_cycle", "executed": summary["reused_vs_executed"]["executed"], "reused": summary["reused_vs_executed"]["reused"], "store_execution": False},
                "source_dependence": {"group": "shares fin_mechanics.beam with the producer receipt", "independent_replication": False},
                "uncertainty": "Numerical only; EI is assumed.",
                "limitations": limits,
                "relation": "supports",
                "produced_by": action,
                "artifacts": [c.artifact("output", f"{CYCLE}/mechanical-evidence.json"), c.artifact("protocol", f"{CYCLE}/protocol.json"), c.artifact("log", f"{CYCLE}/check-history.json")],
            },
            uri,
        )
    )
    c.add(
        c.draft(
            "Evidence",
            "validation-cycle-observed-allometry-separate",
            {
                "target": claim,
                "evidence_kind": "predicted",
                "source": source(ALLOM),
                "created_time": {"value": None, "basis": "unknown"},
                "retrieved_time": {"value": created_at, "basis": "declared"},
                "method": "Reused (not rerun) observed-subset allometry update: held-out error worsened.",
                "context": "Preserved-specimen allometry only; separate from fin mechanics and sequence-function.",
                "assumptions": ["As the producer states."],
                "provenance": {"reused_receipt": protocol["reused"]["observed_allometry_receipt"], "not_fin_validation": True},
                "source_dependence": {"group": "same data and code as the observed-allometry bundle", "independent_replication": False},
                "uncertainty": "Working bands; not a calibrated population confidence.",
                "limitations": limits + ["Not fin mechanics evidence and not sequence-function evidence."],
                "relation": "context_only",
                "artifacts": [c.artifact("output", ALLOM)],
            },
            uri,
        )
    )
    prob_ei = c.add(
        c.draft(
            "Problem",
            "validation-cycle-growth-to-EI-bridge",
            {
                "title": "What is the flexural rigidity EI of this candidate's rays in the stated tissue and stage?",
                "known_state": "EI is an assumed range; no specimen, calibration or species bridge exists, so the mechanical pass licenses nothing biological.",
                "question": protocol["bio_bridge"]["required_readout"],
                "problem_kind": "project_gap",
                "novelty_status": "bridge gap, not a new biological discovery",
                "data_access": "No measurement exists; a physical readout is proposed, not executed.",
                "completeness": "actionable",
                "acceptance_criteria": ["A calibrated EI with unit and bounds for the stated tissue and stage, measured against the frozen readout."],
                "falsifiers": ["The measured EI lies outside the assumed range that the slice used, or the bound is too wide to separate the candidates."],
                "next_action": "Run the selected prospective measurement design under its stated assumptions after review.",
                "required_capabilities": ["bench mechanical testing of fin rays (proposed)"],
                "cost_stop_bounds": "Declared assumed cost units only; no dollar cost.",
                "downstream_uses": ["I3 growth-to-EI interface", "aeroelastic assumptions"],
                "dependencies": [claim],
                "source": source(f"{CYCLE}/check-history.json"),
                "approach": "measurement",
                "scales": ["organ", "tissue"],
                "context_tags": ["assumed-EI", "missing-bridge"],
            },
            uri,
        )
    )
    c.add(
        c.draft(
            "Problem",
            "validation-cycle-sequence-reference",
            {
                "title": "Which exact sequence carries the tested element, and what functional readout would validate it?",
                "known_state": "The ledger carries the tested element only as an unresolved reference (coordinates unresolved); no sequence is claimed and none is generated.",
                "question": next(h["required_readout"] for h in hist["checks"] if h["id"] == "c-sequence-reference") or "a matched functional readout",
                "problem_kind": "project_gap",
                "novelty_status": "sequence-resolution gap",
                "data_access": "Ledger entry only; no sequence read.",
                "completeness": "actionable",
                "acceptance_criteria": ["An exact sequence artifact with a pinned digest and the stated matched readout in the same context."],
                "falsifiers": ["The resolved sequence does not drive the readout in the stated context."],
                "next_action": "Resolve the reference, then request the proposed functional readout.",
                "required_capabilities": ["sequence curation", "reporter assay (proposed)"],
                "cost_stop_bounds": "Read-only curation first; assay only after review.",
                "downstream_uses": ["I1 DNA-to-expression interface"],
                "dependencies": [claim],
                "source": source(LEDGER),
                "approach": "measurement",
                "scales": ["molecular", "cellular"],
                "context_tags": ["unresolved-sequence"],
            },
            uri,
        )
    )
    nxt_alt = [{"label": d["id"].replace("_", "-"), "description": d["title"], "tradeoff": f"expected target-variance reduction per assumed cost {d['expected_target_variance_reduction_per_cost']:.4f}"} for d in nxt["designs"]]
    c.add(
        c.draft(
            "Action",
            "validation-cycle-next-measurement",
            {
                "target": prob_ei,
                "title": "PROPOSED, not executed: prospective EI measurement design selected under explicit assumptions",
                "acceptance_criteria": ["Review accepts the stated priors, noise and cost assumptions before any physical work."],
                "required_capabilities": ["bench mechanical testing of fin rays (proposed)"],
                "cost_stop_bounds": "Declared assumed cost units only; no lab or cloud job is submitted.",
                "cache_key": {
                    "target": prob_ei["version"],
                    "input": nxt["contract_sha256"],
                    "code": _sha(c.blob("engineering/experimental_design/planner.py")),
                    "model": "linear-gaussian-prospective-covariance",
                    "environment": "local deterministic linear algebra",
                    "parameters": _sha(json.dumps(nxt["assumptions"]).encode()),
                    "scope": "proposal only; no response data",
                    "acceptance_policy": "frontier-independent-review-0.1",
                },
                "inputs": [claim],
                "proposal": {
                    "intent": "experiment",
                    "method": "Prospective linear-Gaussian comparison of equal-cost readout designs for log stiffness, with a noise and cost sensitivity grid.",
                    "assumptions": [nxt["assumptions"]],
                    "alternatives": nxt_alt,
                    "expected_information": "Expected reduction in the variance of log stiffness per assumed cost unit.",
                    "decision_context": "Choose which readout design to propose to a lab after review.",
                    "expected_outputs": ["A calibrated EI with bounds if executed later; nothing now."],
                    "controls": ["Repeated-force deflections share one sensitivity row and remain rank one.", "An independent load-scale readout supplies the second direction."],
                    "analysis_plan": "Exact linear-Gaussian conditioning; compare predeclared variance reduction per cost; report the cells where the selection flips.",
                    "outcomes": [
                        {"label": "selected-design", "criterion": f"{nxt['selected_design_id']} has the greater reduction per cost across the stated grid" if not nxt["selection_flips"] else "selection depends on the assumptions; see the grid", "decision_consequence": "Propose that design for review; no execution."}
                    ],
                    "selection_basis": "declared_utility",
                    "selection_rationale": "Highest expected target-variance reduction per assumed cost under the declared priors.",
                    "limitations": limits,
                },
            },
            uri,
        )
    )
    bundle = build_bundle([c])
    if out.exists():
        raise ValueError("Fresh bundle directory required")
    dump(out / "bundle.frontier-bundle-0.1.json", bundle)
    dump(
        out / "bundle-manifest.json",
        {
            "schema": "frontier.validation-cycle.bundle/1",
            "status": "PREPARED ONLY; no DB, import, lease, review or acceptance",
            "source_commit": source_commit,
            "created_at": created_at,
            "counts": {k: sum(r["kind"] == k for r in c.records) for k in ("Claim", "Problem", "Action", "Evidence")},
            "checks": c.checks + link_checks(c.records),
            "bundle_sha256": bundle["bundle_sha256"],
            "not_claimed": limits,
        },
    )
    return bundle


def receipt(root: Path = ROOT) -> dict:
    """Execute the replay twice (bytes must be identical) and the focused test file, and record exactly what ran, its exit status and the versions. Nothing is claimed
    that was not executed here."""
    import subprocess

    import scipy

    out = root / CYCLE
    snap = lambda: {str(p.relative_to(out)): _sha(p.read_bytes()) for p in sorted(out.rglob("*.json")) if p.name != "replay-receipt.json" and not ({"bundle", "superseded"} & set(p.relative_to(out).parts))}  # noqa: E731
    run(root)
    first = snap()
    run(root)
    identical = first == snap()
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/test_validation_cycle.py"], cwd=root, capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if "passed" in ln or "failed" in ln][-1:]
    doc = {
        "schema": "frontier.validation-cycle.replay-receipt/1",
        "commands": [{"cmd": "python -m engineering.biodesign_compiler.validation_cycle run (twice)", "exit": 0, "replay_bytes_identical": identical}, {"cmd": "python -m pytest -q tests/test_validation_cycle.py", "exit": proc.returncode, "summary": tail[0] if tail else None}],
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "output_sha256": first,
        "manifest_sha256": first["manifest.json"],
        "note": "the bundle test skips until the artifacts are committed; the bundle is prepared from an immutable commit afterwards",
    }
    dump(out / "replay-receipt.json", doc)
    return doc


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("phase", choices=["freeze", "run", "receipt", "bundle"])
    ap.add_argument("--source-commit")
    ap.add_argument("--created-at")
    a = ap.parse_args(argv)
    if a.phase == "freeze":
        print({"protocol_sha256": freeze()})
    elif a.phase == "receipt":
        d = receipt()
        print(json.dumps({"replay_identical": d["commands"][0]["replay_bytes_identical"], "tests": d["commands"][1]["summary"]}))
    elif a.phase == "run":
        s = run()
        print(json.dumps({"verdict": s["verdict"]["working_assembly_claim"], "mechanical": s["verdict"]["mechanical_slice"], "next": s["next_action"]["design"]}))
    else:
        from datetime import datetime, timezone

        b = prepare_bundle(a.source_commit, a.created_at or datetime.now(timezone.utc).isoformat(), ROOT / CYCLE / "bundle")
        print({"records": len(b["records"]), "bundle_sha256": b["bundle_sha256"]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
