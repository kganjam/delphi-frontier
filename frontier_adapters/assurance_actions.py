"""Design-assurance map -> PROPOSED Problem / Claim / Action drafts, so that a named gap becomes a pinned Problem and a proposed Action that can accept new Evidence.

Input: `artifacts/assurance/map.json` (schema frontier.design-assurance/1) read from an immutable git blob. Output: records validated with the real models and frozen as an
importable `frontier-bundle-0.1`, plus a mapping table. NOTHING is written to a store, nothing is executed, nothing is reviewed; every Action is a PROPOSAL.

Rules kept (each has a test):
  * no metric is invented: the map's expected_information_gain / expected_utility are null and stay null; the map's biological_success_probability must be null and its
    probability_calibrated false, or this adapter refuses to map it. No ranking among actions is produced (the map says ranking needs measured cost/outcome models).
  * a Problem stays `recorded`: the map supplies no falsifiers and no cost, and the store refuses an Action against a recorded Problem. The proposed Action therefore targets a
    status Claim derived from the map (origin `derived`), and the Problem depends on that Claim by exact version.
  * the five `equation_gaps` become Problems only ("missing stages remain first-class Problems"). The map does not link them to the bridges, so this adapter does not either.
  * cost and stop bound read UNKNOWN; controls and analysis plan are placeholders a reviewer must replace before the Action can become ready; none is a result.
  * pins: every Source is a git locator plus sha256 of the exact blob; the map's own evidence pins are re-hashed against the tree and a mismatch is reported, not hidden.
"""
from __future__ import annotations

import json
import os

from .artifacts import find_abs_paths
from .common import sha_bytes, sha_obj
from .engineering_manifest import ADAPTER_VERSION as _EM_VERSION, Chain, Refused, STATUS, _cache_key, _source, _time, build_bundle, link_checks, resolve_commit

ADAPTER_ID = "frontier_adapters.assurance_actions"
ADAPTER_VERSION = "0.1.0"
MAP_PATH = "artifacts/assurance/map.json"
MANIFEST_PATH = "artifacts/assurance/manifest.json"
SCHEMA = "frontier.design-assurance/1"
SRC_URI = "urn:frontier:adapter:assurance-actions"
MAX_RECORDS_HERE = 40                       # 4 x (Claim, Problem, Action) + 5 gap Problems = 17 today; a deliberate, bounded ceiling for this adapter
UNKNOWN_COST = ("UNKNOWN. The assurance map states no cost, no budget and no stop bound ('ranking among these needs measured cost/outcome models'). A reviewer must set them "
                "before this Action can be made ready; none is invented here.")
PLACEHOLDER_CONTROLS = ("To be declared by the reviewer before the Action is made ready: a positive control, a negative control and a mutation or corruption control appropriate to the "
                        "measurement or computation. The assurance map declares none.")
PLACEHOLDER_ANALYSIS = "Not declared by the assurance map. The proposer or reviewer sets the analysis plan and its predicate BEFORE any run; none is implied by this draft."
NOT_ESTABLISHED = ["that the proposed Action is the best use of resources (the map does not rank, and no expected information or utility is computed)",
                   "that the Action will succeed, or any probability of biological success",
                   "that the bridge or gap is a correct or complete description of what blocks the design",
                   "anything about biology"]
INTENT = {"resolve-cell-tissue-fin": "experiment", "resolve-fin-deformation-aerodynamic-polar": "experiment", "resolve-fin-stiffness-calibration": "experiment",
          "refine-unconverged-glide": "simulation"}


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s)[:90]


def load_map(c: Chain) -> tuple[dict, bytes]:
    data = c.blob(MAP_PATH)
    m = json.loads(data)
    c.check("map.schema", m.get("schema") == SCHEMA, f"schema {m.get('schema')!r}")
    c.check("map.no_probability", m.get("biological_success_probability") is None and m.get("probability_calibrated") is False,
            f"biological_success_probability={m.get('biological_success_probability')!r} probability_calibrated={m.get('probability_calibrated')!r}: this adapter maps only a map that makes no probability claim")
    man = c.blob(MANIFEST_PATH).decode()
    c.check("map.identity", sha_bytes(data) in man, f"sha256 {sha_bytes(data)[:16]}... is recorded in {MANIFEST_PATH}")
    for a in m["project"]["next_actions"]:
        c.check(f"action.{a['id']}.no_numbers", a.get("expected_information_gain") is None and a.get("expected_utility") is None,
                "the map carries no expected-information or utility number for this action; none is created here")
    return m, data


def check_evidence_pins(c: Chain, m: dict) -> dict:
    """Re-hash every evidence pin of the map that is present in the tree. Reported, never fatal: a stale pin is a finding."""
    ok, absent, differs = 0, [], []
    for e in m["evidence_index"]:
        try:
            got = sha_bytes(c.blob(e["path"]))
        except Refused:
            absent.append(e["path"])
            continue
        if got == e["sha256"]:
            ok += 1
        else:
            differs.append({"path": e["path"], "map_sha256": e["sha256"], "tree_sha256": got})
    return {"pins": len(m["evidence_index"]), "match": ok, "absent_in_tree": absent, "hash_differs": differs}


def _evidence_pin(c: Chain, ev: dict) -> dict:
    try:
        got = sha_bytes(c.blob(ev["path"]))
    except Refused:
        return {"path": ev["path"], "sha256_map": ev["sha256"], "selector": ev.get("selector"), "tree_check": "absent_in_tree"}
    return {"path": ev["path"], "sha256_map": ev["sha256"], "selector": ev.get("selector"), "tree_check": "match" if got == ev["sha256"] else "hash_differs"}


def _proposal(a: dict, bridge: dict | None, policy: str) -> dict:
    blocks = bridge["blocks"][0] if bridge and bridge.get("blocks") else "(not stated by the map for this item)"
    return {
        "intent": INTENT.get(a["id"], "plan"), "method": a["action"],
        "assumptions": [f"The intent '{INTENT.get(a['id'], 'plan')}' is the adapter's reading of the action wording; the map states no intent.",
                        "The action text is taken verbatim from the assurance map; no method detail is added."],
        "alternatives": [{"label": "defer", "description": "Take no action and leave the item as the map records it.",
                          "tradeoff": f"No cost; the dependent decision ({blocks}) stays blocked and the map keeps this item unsupported or failed."}],
        "expected_information": ("Qualitative only: this Action could remove the named blocker. The map's expected_information_gain is null and no probability or utility inputs are explicit, "
                                 "so no number is computed or implied."),
        "decision_context": f"Blocks: {blocks}. Priority class in the map: {a['priority_class']}. Reason in the map: {a.get('reason') or '(none stated by the map for this item)'}",
        "expected_outputs": [a["action"]], "controls": [PLACEHOLDER_CONTROLS], "analysis_plan": PLACEHOLDER_ANALYSIS,
        "outcomes": [{"label": "requirement_met", "criterion": f"Evidence that supplies: {a['action']}, with exact pins, accepted under the independent-review policy.",
                      "decision_consequence": f"The blocked decision ({blocks}) can be re-evaluated and the assurance map rebuilt from the new Evidence; the map is not edited by hand."},
                     {"label": "requirement_not_met", "criterion": "No Evidence, Evidence outside the stated scope, or Evidence that fails review.",
                      "decision_consequence": "The item stays unsupported or failed and the dependent decision stays blocked."}],
        "selection_basis": "policy", "selection_rationale": f"The map's action policy: {policy}. No ranking among actions is made.",
        "limitations": ["Proposal only: not executed, not scheduled, not leased, not reviewed.", *NOT_ESTABLISHED]}


def build(repo: str, source_commit: str, *, namespace: str = "node-a", issuer: str = "importer", created_at: str | None = None, live_hooks: dict | None = None) -> tuple[Chain, dict]:
    """Returns (chain, mapping). `live_hooks` {assurance_item_id: [ {...hook...} ]} is attached to the mapping table verbatim (it comes from a read-only audit)."""
    from .engineering_manifest import _commit_utc
    created_at = created_at or _commit_utc(repo, source_commit)
    c = Chain(repo, source_commit, namespace, issuer, created_at, "assurance_actions")
    c.limit = MAX_RECORDS_HERE
    m, mdata = load_map(c)
    pins = check_evidence_pins(c, m)
    proj = m["project"]
    bridges = {b["id"]: b for b in proj["unsupported_essential_bridges"]}
    rows = []
    for a in proj["next_actions"]:
        bridge = bridges.get((a.get("targets") or [None])[0])
        ev_pins = [_evidence_pin(c, e) for e in a["evidence"]]
        slug = _slug(a["id"])
        stmt = (f"The design-assurance map (project {m['project_id']}, sha256 {sha_bytes(mdata)}) records '{a['id']}' ({a['priority_class']}): {a['action']}. "
                + (f"Its essential-bridge entry '{bridge['id']}' has status '{bridge['status']}' and blocks: {', '.join(bridge['blocks'])}." if bridge else
                   "It is a recorded numerical failure, not an essential bridge."))
        claim_ref = c.add(c.draft("Claim", f"assure-{slug}-status", {
            "title": f"Assurance map status: {a['id']}", "statement": stmt,
            "context": "A projection by the assurance builder over recorded receipts. It states what the map lists as unsupported or failed; it is not a biological finding and not a review. "
                       "The map status for the whole design is '" + str(m["status"]) + "'.",
            "assumptions": ["The map's own scope statements apply: " + n for n in m["notices"][:2]],
            "limitations": ["Derived by an adapter from the map; single-reader, not reviewed.", "Biological success probability in the map is null and uncalibrated.", *NOT_ESTABLISHED[:1]],
            "source": _source(c, MAP_PATH, mdata, f"Selector /project/next_actions[{a['id']}]" + (f" and /project/unsupported_essential_bridges[{bridge['id']}]" if bridge else "") + "."),
            "source_record_version": None, "prior_review": {"status": "none: not reviewed by anyone"}, "origin": "derived"}, SRC_URI))
        prob_ref = c.add(c.draft("Problem", f"assure-{slug}-gap", {
            "title": a["action"][:300], "known_state": (f"Map status '{bridge['status']}'; blocks {', '.join(bridge['blocks'])}." if bridge else "Recorded numerical failure; see the cited summary."),
            "question": (f"What Evidence would resolve '{bridge['id']}' so that '{bridge['blocks'][0]}' can be decided?" if bridge else f"Why does the recorded scenario not converge, and does a refined run change any comparison that used it?"),
            "problem_kind": "project_gap", "novelty_status": "Not searched by this adapter.", "data_access": "Not established by the assurance map.", "completeness": "recorded",
            "acceptance_criteria": [], "falsifiers": [], "next_action": None, "required_capabilities": [], "cost_stop_bounds": None,
            "downstream_uses": list(bridge["blocks"]) if bridge else ["comparison of the common-launch glide scenarios"], "dependencies": [claim_ref],
            "source": _source(c, MAP_PATH, mdata, "Problem text is derived from the map's entry for this item."), "original": {"assurance_item": a["id"], "adapter": ADAPTER_ID},
            "approach": "unknown", "scales": [], "context_tags": ["flying-fish", "design-assurance", a["id"]]}, SRC_URI))
        act_draft = c.draft("Action", f"assure-{slug}-action", {
            "target": claim_ref, "title": f"PROPOSED (not executed): {a['action']}"[:300],
            "acceptance_criteria": [f"Evidence that supplies: {a['action']}, with exact pins, accepted under the independent-review policy."],
            "required_capabilities": [], "cost_stop_bounds": UNKNOWN_COST,
            "cache_key": _cache_key(claim_ref["version"], input=f"assurance map sha256 {sha_bytes(mdata)}; evidence pins " + "; ".join(f"{p['path']}#{p['selector']}:{p['sha256_map'][:16]}" for p in ev_pins),
                                    code=f"{ADAPTER_ID}@{ADAPTER_VERSION}; git:delphi-frontier@{source_commit}", model="none: a proposal", environment="NOT APPLICABLE: nothing is executed by this record",
                                    parameters="none: a proposal with no run parameters", scope="proposal to resolve one named item of the assurance map"),
            "inputs": [], "proposal": _proposal(a, bridge, proj["action_policy"])}, SRC_URI)
        act_ref = c.add(act_draft)
        rows.append({"assurance_item": {"kind": "next_action", "id": a["id"], "selector": f"/project/next_actions/{proj['next_actions'].index(a)}", "priority_class": a["priority_class"],
                                        "bridge_id": bridge["id"] if bridge else None, "bridge_status": bridge["status"] if bridge else None, "blocks": bridge["blocks"] if bridge else None},
                     "evidence_pins": ev_pins, "produces": {"claim": claim_ref, "problem": prob_ref, "action": act_ref},
                     "accepts_new_evidence_via": "Evidence with target == this Claim version and produced_by == this Action version (the store's own typed hooks)",
                     "action_inputs": [], "action_inputs_note": "empty on purpose: pinning a record whose source pin differs from the map's pin would assert a consumption that did not happen",
                     "existing_live_hooks": (live_hooks or {}).get(a["id"], "not queried (no live audit supplied)")})
    for g in m["equation_gaps"]:
        slug = _slug(g["id"])
        prob_ref = c.add(c.draft("Problem", f"assure-gap-{slug}", {
            "title": f"Missing mechanism: {g['id']}", "known_state": f"The map lists this equation gap with status '{g['status']}': {g['summary']}",
            "question": f"What calibrated equations and data would close the gap '{g['id']}' across scales {', '.join(g['scales'])}?", "problem_kind": "project_gap",
            "novelty_status": "Not searched by this adapter.", "data_access": "Not established by the assurance map.", "completeness": "recorded", "acceptance_criteria": [], "falsifiers": [],
            "next_action": None, "required_capabilities": [], "cost_stop_bounds": None, "downstream_uses": ["whole-design validation claims stay blocked while this gap is open"], "dependencies": [],
            "source": _source(c, MAP_PATH, mdata, f"Selector /equation_gaps[{g['id']}]."), "original": {"assurance_item": g["id"], "adapter": ADAPTER_ID},
            "approach": "unknown", "scales": list(g["scales"]), "context_tags": ["flying-fish", "design-assurance", g["id"]]}, SRC_URI))
        rows.append({"assurance_item": {"kind": "equation_gap", "id": g["id"], "selector": f"/equation_gaps/{m['equation_gaps'].index(g)}", "scales": g["scales"], "status": g["status"]},
                     "evidence_pins": [_evidence_pin(c, e) for e in g["evidence"]], "produces": {"problem": prob_ref},
                     "no_action": "no Action is proposed: the map supplies no action for this gap, and a recorded Problem cannot carry an Action until its actionability fields are supplied by a person",
                     "relation_to_bridges": "not declared by the map; not inferred here", "existing_live_hooks": (live_hooks or {}).get(g["id"], "not queried (no live audit supplied)")})
    mapping = {
        "status": STATUS, "adapter": {"id": ADAPTER_ID, "version": ADAPTER_VERSION}, "source": {"repo_label": "delphi-frontier", "commit": source_commit, "map_path": MAP_PATH, "map_sha256": sha_bytes(mdata)},
        "map_project": m["project_id"], "map_status": m["status"], "evidence_pin_check": pins, "rows": rows,
        "not_mapped": {"counterexamples": [{"kind": x["kind"], "reason": "a finding recorded by the map, not a gap to act on"} for x in proj["counterexamples"]],
                       "ensembles": "descriptive simulation-envelope fractions; not probabilities of biology, and not a basis for ranking here"},
        "no_metric_statement": "No expected information, utility, ranking score, success probability or calibrated figure is produced or implied. The map's own such fields are null and stay null.",
        "counts": {"next_actions": len(proj["next_actions"]), "equation_gaps": len(m["equation_gaps"]), "records": len(c.records)},
    }
    bad = find_abs_paths(mapping) + find_abs_paths(c.records)
    if bad:
        raise Refused(f"absolute local paths in output at {bad}")
    return c, mapping


def write_frozen(out_dir: str, chain: Chain, mapping: dict) -> dict:
    bundle = build_bundle([chain], limit=MAX_RECORDS_HERE)
    mapping = {**mapping, "link_checks": link_checks(bundle["records"]), "bundle_sha256": bundle["bundle_sha256"], "checks_performed": chain.checks}
    os.makedirs(out_dir, exist_ok=True)
    files = {"bundle.frontier-bundle-0.1.json": json.dumps(bundle, indent=1, sort_keys=True) + "\n", "mapping.json": json.dumps(mapping, indent=1, sort_keys=True) + "\n"}
    for n, t in files.items():
        with open(os.path.join(out_dir, n), "w") as fh:
            fh.write(t)
    manifest = {"status": STATUS, "bundle_sha256": bundle["bundle_sha256"], "file_sha256": {n: sha_bytes(t.encode()) for n, t in files.items()},
                "records": [{"kind": r["kind"], "id": r["id"], "namespace": r["namespace"], "version": r["version"]} for r in bundle["records"]], "publication": "none. Not written to any store; corpus owns imports."}
    with open(os.path.join(out_dir, "manifest.json"), "w") as fh:
        fh.write(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    return {"bundle": bundle, "mapping": mapping, "manifest": manifest}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m frontier_adapters.assurance_actions", description="Map the design-assurance map to proposed Problem/Claim/Action drafts. Writes files only; never touches a store.")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--source-commit", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--namespace", default="node-a")
    ap.add_argument("--live-hooks", default=None, help="JSON file from frontier_adapters.assurance_audit (read-only live audit), attached verbatim to the mapping")
    a = ap.parse_args(argv)
    hooks = json.load(open(a.live_hooks))["hooks_by_item"] if a.live_hooks else None
    chain, mapping = build(a.repo, resolve_commit(a.repo, a.source_commit), namespace=a.namespace, live_hooks=hooks)
    out = write_frozen(a.out, chain, mapping)
    print(json.dumps({"records": len(out["bundle"]["records"]), "bundle_sha256": out["bundle"]["bundle_sha256"], "out": a.out}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
