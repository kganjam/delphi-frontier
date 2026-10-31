"""Tests for frontier_adapters.assurance_actions and assurance_audit. Hand-worked expectations; the real committed assurance map is the input.
Run: bash scripts/test_postgres.sh frontier_adapters/tests/test_assurance_actions.py   (the PG tests skip, with that reason, outside it). Nothing here touches the live service."""
import ast
import json
import os
import subprocess
from collections import Counter
from pathlib import Path

import pytest

from frontier_adapters import assurance_actions as A, assurance_audit as U, engineering_manifest as em
from frontier_adapters.artifacts import git_blob
from frontier_adapters.common import sha_bytes, validate_draft

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "frontier_adapters" / "examples" / "assurance_actions"
MAP = "artifacts/assurance/map.json"


def have_map() -> bool:
    return (ROOT / MAP).exists() and subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True).returncode == 0


needs_map = pytest.mark.skipif(not have_map(), reason="assurance map not present in this checkout")


@pytest.fixture(scope="module")
def built():
    if not have_map():
        pytest.skip("assurance map not present")
    commit = A.resolve_commit(str(ROOT), "HEAD")
    chain, mapping = A.build(str(ROOT), commit)
    return commit, chain, mapping


def by_id(chain, rid):
    return next(r for r in chain.records if r["id"] == rid)


def ref(r):
    return {k: r[k] for k in ("namespace", "kind", "id", "version")}


# ------------------------------------------------------------------ what gets mapped
def test_four_next_actions_and_five_gaps_become_records_of_the_right_kinds(built):
    _, chain, mapping = built
    assert dict(Counter(r["kind"] for r in chain.records)) == {"Claim": 4, "Problem": 9, "Action": 4} and mapping["counts"] == {"next_actions": 4, "equation_gaps": 5, "records": 17}
    items = [(r["assurance_item"]["kind"], r["assurance_item"]["id"]) for r in mapping["rows"]]
    assert items == [("next_action", "resolve-cell-tissue-fin"), ("next_action", "resolve-fin-deformation-aerodynamic-polar"), ("next_action", "resolve-fin-stiffness-calibration"),
                     ("next_action", "refine-unconverged-glide"), ("equation_gap", "gene-to-fin-program"), ("equation_gap", "tissue-to-EI"), ("equation_gap", "deformed-fin-to-polar"),
                     ("equation_gap", "neural-caudal-control"), ("equation_gap", "whole-life-history")]
    assert [r["assurance_item"]["bridge_id"] for r in mapping["rows"][:4]] == ["cell-tissue-fin", "fin-deformation-aerodynamic-polar", "fin-stiffness-calibration", None]    # the numerical failure is not a bridge
    for r in mapping["rows"][4:]:
        assert "Action" not in json.dumps(r["produces"]) and "no Action is proposed" in r["no_action"] and "not declared by the map" in r["relation_to_bridges"]


def test_problems_stay_recorded_and_invent_no_falsifier_cost_or_next_step(built):
    _, chain, _ = built
    for p in (r for r in chain.records if r["kind"] == "Problem"):
        pl = p["payload"]
        assert pl["completeness"] == "recorded" and pl["acceptance_criteria"] == [] and pl["falsifiers"] == [] and pl["next_action"] is None and pl["cost_stop_bounds"] is None and pl["approach"] == "unknown"


def test_each_proposed_action_targets_its_status_claim_and_the_problem_depends_on_that_exact_claim(built):
    _, chain, mapping = built
    for row in mapping["rows"][:4]:
        c, p, a = (row["produces"][k] for k in ("claim", "problem", "action"))
        claim, prob, act = (by_id(chain, x["id"]) for x in (c, p, a))
        assert claim["kind"] == "Claim" and claim["payload"]["origin"] == "derived" and prob["payload"]["dependencies"] == [ref(claim)] and act["payload"]["target"] == ref(claim)
        assert act["payload"]["inputs"] == [] and "empty on purpose" in row["action_inputs_note"]
        assert act["payload"]["title"].startswith("PROPOSED (not executed):") and "not a result" not in act["payload"]["cost_stop_bounds"] and act["payload"]["cost_stop_bounds"].startswith("UNKNOWN")


def test_the_proposal_is_qualitative_policy_based_and_ranks_nothing(built):
    _, chain, _ = built
    for a in (r for r in chain.records if r["kind"] == "Action"):
        pr = a["payload"]["proposal"]
        assert pr["selection_basis"] == "policy" and "No ranking among actions is made" in pr["selection_rationale"] and "null" in pr["expected_information"] and "no number is computed" in pr["expected_information"]
        assert [x["label"] for x in pr["outcomes"]] == ["requirement_met", "requirement_not_met"] and pr["alternatives"][0]["label"] == "defer"
        assert "reviewer" in pr["controls"][0] and "BEFORE any run" in pr["analysis_plan"] and pr.get("plan_steps", []) == []
        assert any("probability of biological success" in x for x in pr["limitations"])


def test_no_metric_probability_utility_or_ranking_is_created(built):
    _, chain, mapping = built
    blob = json.dumps([chain.records, mapping], sort_keys=True)
    forbidden_keys = ("probability", "utility", "information_gain", "score", "rank", "confidence", "success_rate", "priority_score")
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if any(f in k.lower() for f in forbidden_keys) and isinstance(v, (int, float)) and not isinstance(v, bool):
                    raise AssertionError(f"numeric {k} at {path}")
                walk(v, path + "/" + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
    walk([chain.records, mapping])
    assert "No expected information, utility, ranking score, success probability or calibrated figure is produced or implied" in mapping["no_metric_statement"]
    assert '"expected_information_gain"' not in blob.replace('expected_information_gain is null', '')


# ------------------------------------------------------------------ pins and exact references
def test_map_identity_and_every_evidence_pin_are_rechecked(built):
    commit, chain, mapping = built
    data = git_blob(str(ROOT), commit, MAP)
    assert mapping["source"]["map_sha256"] == sha_bytes(data) == "737ed4004156bc32510241bcd352c5c7e352f8cb1c81ceb3959700f5862f8fd7"
    p = mapping["evidence_pin_check"]
    assert (p["pins"], p["match"], p["absent_in_tree"], p["hash_differs"]) == (32, 32, [], [])
    assert all(x["tree_check"] == "match" for r in mapping["rows"] for x in r["evidence_pins"])
    assert {"map.schema", "map.no_probability", "map.identity"} <= {c["id"] for c in chain.checks if c["ok"]}


def test_every_pointer_resolves_by_exact_version_and_new_evidence_can_attach(built):
    _, chain, mapping = built
    assert all(c["ok"] for c in em.link_checks(chain.records))
    claim, act = by_id(chain, mapping["rows"][2]["produces"]["claim"]["id"]), by_id(chain, mapping["rows"][2]["produces"]["action"]["id"])
    # a later Evidence that targets the Claim and was produced by the Action validates against the real models: the Action CAN accept new Evidence
    ev = {"namespace": claim["namespace"], "kind": "Evidence", "id": "future-evidence", "issuer": "someone", "source_uri": "urn:test", "visibility": "public", "predecessor": None,
          "payload": {"target": ref(claim), "evidence_kind": "observed", "source": claim["payload"]["source"], "created_time": {"value": None, "basis": "unknown"},
                      "retrieved_time": {"value": "2026-10-31T15:00:00+00:00", "basis": "declared"}, "method": "m", "context": "c", "assumptions": ["a"], "provenance": {"p": 1},
                      "source_dependence": {"g": 1}, "uncertainty": "u", "limitations": ["fixture"], "relation": "unspecified", "produced_by": ref(act)}}
    assert validate_draft(ev)["licence_gate_offenders"] == []
    wrong = json.loads(json.dumps(chain.records)) + [validate_draft(ev, chain.created_at)["record"]]
    other_action = by_id(chain, mapping["rows"][0]["produces"]["action"]["id"])
    wrong[-1]["payload"]["produced_by"] = ref(other_action)          # an Action aimed at a DIFFERENT Claim
    assert [c["id"] for c in em.link_checks(wrong) if not c["ok"]] == ["future-evidence.produced_by_same_target"]


def test_build_is_deterministic_and_the_frozen_bundle_is_reproduced(built):
    commit, chain, mapping = built
    again, _ = A.build(str(ROOT), commit)
    assert [r["version"] for r in chain.records] == [r["version"] for r in again.records]
    bundle = em.build_bundle([chain], limit=A.MAX_RECORDS_HERE)
    f = EXAMPLE / "bundle.frontier-bundle-0.1.json"
    if f.exists():
        frozen = json.loads(f.read_text())
        pinned = json.loads((EXAMPLE / "manifest.json").read_text())["bundle_sha256"]
        assert frozen["bundle_sha256"] == pinned == bundle["bundle_sha256"] or frozen["records"][0]["source_uri"] == "urn:frontier:adapter:assurance-actions"
        if A.resolve_commit(str(ROOT), "HEAD") == json.loads((EXAMPLE / "mapping.json").read_text())["source"]["commit"]:
            assert frozen == bundle


# ------------------------------------------------------------------ refusals on a throwaway tree
def _git(d, *a):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.org", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.org"}
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, env=env, check=True).stdout.strip()


@pytest.fixture
def tree(tmp_path):
    if not have_map():
        pytest.skip("assurance map not present")
    d = str(tmp_path)
    (tmp_path / "artifacts/assurance").mkdir(parents=True)
    (tmp_path / MAP).write_bytes((ROOT / MAP).read_bytes())
    (tmp_path / "artifacts/assurance/manifest.json").write_bytes((ROOT / "artifacts/assurance/manifest.json").read_bytes())
    _git(d, "init", "-q"); _git(d, "add", "-A"); _git(d, "commit", "-q", "-m", "base")

    def go(edit=None, rehash=True):
        if edit:
            m = json.loads((tmp_path / MAP).read_text()); edit(m)
            data = json.dumps(m).encode()
            (tmp_path / MAP).write_bytes(data)
            if rehash:                                                  # keep the identity check passing so the OTHER check is what fires
                (tmp_path / "artifacts/assurance/manifest.json").write_text(json.dumps({"output": {"map": sha_bytes(data)}}))
        _git(d, "add", "-A"); _git(d, "commit", "-q", "--allow-empty", "-m", "mutated")
        return d, _git(d, "rev-parse", "HEAD")
    return go


@pytest.mark.parametrize("name,edit,rehash,check", [
    ("a probability appears", lambda m: m.update(biological_success_probability=0.4), True, "map.no_probability"),
    ("claimed calibrated", lambda m: m.update(probability_calibrated=True), True, "map.no_probability"),
    ("wrong schema", lambda m: m.update(schema="something/else"), True, "map.schema"),
    ("expected information gain added", lambda m: m["project"]["next_actions"][0].update(expected_information_gain=1.5), True, "no_numbers"),
    ("expected utility added", lambda m: m["project"]["next_actions"][1].update(expected_utility=3), True, "no_numbers"),
    ("map changed without the manifest knowing", lambda m: m.update(status="supported"), False, "map.identity"),
])
def test_the_adapter_refuses_a_map_that_makes_a_metric_or_probability_claim_or_is_not_the_recorded_one(tree, name, edit, rehash, check):
    d, rev = tree(edit, rehash)
    with pytest.raises(em.Refused) as e:
        A.build(d, rev)
    assert check in str(e.value), (name, str(e.value))


def test_a_stale_evidence_pin_is_reported_not_hidden(tree):
    d, rev = tree()
    chain, mapping = A.build(d, rev)                                    # the throwaway tree holds only the map: every evidence file is absent
    p = mapping["evidence_pin_check"]
    assert p["match"] == 0 and len(p["absent_in_tree"]) == 32 and {x["tree_check"] for r in mapping["rows"] for x in r["evidence_pins"]} == {"absent_in_tree"}


# ------------------------------------------------------------------ the lineage audit
def test_schema_hooks_are_read_from_the_models_and_each_has_a_reverse_or_says_none():
    h = U.schema_hooks()
    f = {(x["model"], x["field"]): x for x in h["forward_fields"]}
    assert f[("Action", "inputs")]["typed_edge_relation"] == "uses" and f[("Action", "inputs")]["bidirectional"]
    assert f[("Evidence", "produced_by")]["typed_edge_relation"] == "produced_by" and f[("Problem", "dependencies")]["typed_edge_relation"] == "depends_on"
    assert f[("Evidence", "target")]["bidirectional"] and f[("Action", "target")]["bidirectional"] and f[("ActionProposal", "plan_steps")]["typed_edge_relation"] == "plans_step"
    assert f[("Evidence", "artifacts")]["pointer"] == "ArtifactRef" and "ArtifactIndex" in f[("Evidence", "artifacts")]["reverse_query"]
    assert not f[("Interest", "target")]["bidirectional"] and f[("Interest", "target")]["reverse_query"].startswith("none")          # an honest forward-only hook
    assert h["bidirectional_count"] + h["forward_only_count"] == len(h["forward_fields"]) and any("claim_ids" in u for u in h["untyped_lineage_text_not_queryable_backwards"])


def test_map_audit_counts_come_from_the_map(built):
    commit, chain, mapping = built
    m = json.loads(chain.blob(A.MAP_PATH))
    a = U.map_audit(m, str(ROOT), commit, git_blob)
    assert a["equations"] == 12 and a["equations_without_sources"] == [] and a["equation_sources_without_sha256"] == []
    assert a["claim_refs"] == 13 and a["claim_refs_by_namespace"] == {"snapshot": 13} and a["claim_ref_status_values"] == {"snapshot_pin_not_live_store_acceptance": 13}
    assert "flying-fish:molecular" in a["nodes_with_no_equation_ids"] and "map_itself_in_store" in a and "not asserted" in a["map_itself_in_store"]


def test_audit_module_only_reads(monkeypatch):
    src = (ROOT / "frontier_adapters" / "assurance_audit.py").read_text()
    tree = ast.parse(src)
    sql = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and ("SELECT" in n.value or "INSERT" in n.value or "UPDATE" in n.value or "DELETE" in n.value)]
    assert sql and all(s.lstrip().upper().startswith(("SELECT", "SET TRANSACTION READ ONLY")) or "SELECT" in s for s in sql) and not any(w in s.upper() for s in sql for w in ("INSERT ", "UPDATE ", "DELETE ", "DROP ", "ALTER "))
    imported = {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module} | {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    assert not (imported & {"urllib", "requests", "socket", "subprocess", "http"})
    assert "SET TRANSACTION READ ONLY" in src


@pytest.fixture
def pgstore():
    dsn = os.environ.get("FRONTIER_TEST_DSN")
    if not dsn:
        pytest.skip("run through scripts/test_postgres.sh (own ephemeral cluster; never the live service)")
    from uuid import uuid4
    from frontier.store import Store
    st = Store(dsn, "node-z", "test_" + uuid4().hex)
    st.initialize()
    st.provision("test-only-local-token-for-alice", "alice", "operator-a", ["contributor", "coordinator"], ["node-z"], 1000)
    return st


def _claim(store, id_, path, sha):
    src = {"uri": None, "locator": f"git:delphi-frontier@{'a' * 40}:{path}", "source_version": "x", "content_sha256": sha, "content_available": False, "access": "fixture", "license": None}
    return {"namespace": store.namespace, "kind": "Claim", "id": id_, "issuer": "alice", "source_uri": "urn:test",
            "payload": {"title": id_, "statement": "s", "context": "c", "assumptions": ["a"], "limitations": ["l"], "source": src}}


def test_hooks_pin_relation_reverse_usage_and_claim_ref_resolution_on_an_ephemeral_store(pgstore):
    from frontier.models import POLICY
    T = "test-only-local-token-for-alice"
    good, other = "1" * 64, "2" * 64
    c_match = pgstore.submit(T, "c1", _claim(pgstore, "claim-match", "engineering/x/result.json", good))["record"]
    c_diff = pgstore.submit(T, "c2", _claim(pgstore, "claim-differs", "engineering/x/result.json", other))["record"]
    pgstore.submit(T, "c3", _claim(pgstore, "claim-unrelated", "somewhere/else.json", good))
    ck = {"target": c_match["version"], "input": "i", "code": "c", "model": "m", "environment": "e", "parameters": "p", "scope": "s", "acceptance_policy": POLICY}
    ref_ = {k: c_match[k] for k in ("namespace", "kind", "id", "version")}
    pgstore.submit(T, "a1", {"namespace": "node-z", "kind": "Action", "id": "act", "issuer": "alice", "source_uri": "urn:test", "payload": {
        "target": ref_, "title": "t", "acceptance_criteria": ["x"], "required_capabilities": [], "cost_stop_bounds": "b", "cache_key": ck, "inputs": [ref_]}})
    pin = {"path": "engineering/x/result.json", "sha256_map": good, "selector": "/s"}
    hooks = {(h["ref"]["id"]): h for h in U.hooks_for_item(pgstore, "item", [pin])}
    assert set(hooks) == {"claim-match", "claim-differs"}                                        # the unrelated path is not a hook
    assert hooks["claim-match"]["pin_relation"] == "pin_matches_map" and hooks["claim-match"]["usable_as_exact_input"] is True
    assert hooks["claim-differs"]["pin_relation"] == "pin_differs_from_map" and hooks["claim-differs"]["usable_as_exact_input"] is False
    # reverse usage of the matched Claim: the Action points at it twice (as target and as input)
    ru = hooks["claim-match"]["reverse_usage_incoming_edges"]
    assert ru["count"] == 2 and ru["by_kind"] == {"targets": 1, "uses": 1} and hooks["claim-differs"]["reverse_usage_incoming_edges"]["count"] == 0
    refs = [{"ref": {"namespace": "snapshot", "kind": "Claim", "id": "claim-match", "version": "f" * 64}, "status": "snapshot_pin_not_live_store_acceptance", "subsystem": "t"},
            {"ref": {**{k: c_match[k] for k in ("namespace", "kind", "id", "version")}}, "status": "x", "subsystem": "t"},
            {"ref": {"namespace": "snapshot", "kind": "Claim", "id": "nothing-like-this", "version": "e" * 64}, "status": "x", "subsystem": "t"}]
    res = U.resolve_claim_refs(pgstore, refs)
    assert [r["live"] for r in res] == ["same_kind_and_id_elsewhere", "exact_version_present", "absent"]
    # a file that changed since its pin is reported; one that did not is not
    ev = {"namespace": "node-z", "kind": "Evidence", "id": "ev", "issuer": "alice", "source_uri": "urn:test", "payload": {
        "target": ref_, "evidence_kind": "simulated", "source": c_match["payload"]["source"], "created_time": {"value": None, "basis": "unknown"},
        "retrieved_time": {"value": "2026-10-31T15:00:00+00:00", "basis": "declared"}, "method": "m", "context": "c", "assumptions": ["a"], "provenance": {"p": 1},
        "source_dependence": {"g": 1}, "uncertainty": "u", "limitations": ["l"], "artifacts": [
            {"title": f"output: p/a.json [git:delphi-frontier@{'b' * 40}:p/a.json]", "uri": "urn:sha256:" + "3" * 64, "sha256": "3" * 64, "byte_size": 1, "media_type": "application/json", "role": "output", "availability": "referenced", "license": None},
            {"title": f"output: p/b.json [git:delphi-frontier@{'b' * 40}:p/b.json]", "uri": "urn:sha256:" + "4" * 64, "sha256": "4" * 64, "byte_size": 1, "media_type": "application/json", "role": "output", "availability": "referenced", "license": None}]}}
    pgstore.submit(T, "e1", ev)
    blobs = {"p/a.json": b"changed bytes", "p/b.json": None}
    def read(repo, commit, path):
        if blobs[path] is None:
            raise FileNotFoundError(path)
        return blobs[path]
    stale = U.stale_artifact_pins(pgstore, ".", "c" * 40, read)
    assert [(s["path"], s["state"]) for s in stale] == [("p/a.json", "file_changed_since_pin"), ("p/b.json", "path_unreadable_at_commit")]
    assert stale[0]["pinned_sha256"] == "3" * 64 and stale[0]["sha256_at_checked_commit"] == sha_bytes(b"changed bytes")


# ------------------------------------------------------------------ the committed audit, self-consistent and honest
@pytest.mark.skipif(not (EXAMPLE / "lineage_audit.json").exists(), reason="no committed audit")
def test_committed_audit_is_self_consistent_and_states_no_metric():
    au = json.loads((EXAMPLE / "lineage_audit.json").read_text())
    mp = json.loads((EXAMPLE / "mapping.json").read_text())
    assert au["read_only"] is True and "No success probability" in au["no_metric_statement"] and au["map"]["sha256_in_mapping"] == mp["source"]["map_sha256"]
    assert set(au["hooks_by_item"]) == {r["assurance_item"]["id"] for r in mp["rows"]}
    stiff = au["hooks_by_item"]["resolve-fin-stiffness-calibration"]
    assert {h["ref"]["id"] for h in stiff} >= {"eng-finmech-claim-ei-crit", "eng-finmech-evidence-sim", "eng-finmech-problem-ei-measurement"}
    assert all(h["pin_relation"] == "pin_differs_from_map" and h["usable_as_exact_input"] is False for h in stiff)       # live pins are of the older result.json bytes
    assert all(r["action_inputs"] == [] for r in mp["rows"][:4])
    cr = Counter(x["live"] for x in au["claim_ref_resolution"])
    assert cr["exact_version_present"] == 0 and sum(cr.values()) == 13 and cr["absent"] + cr["same_kind_and_id_elsewhere"] == 13
    assert all(s["state"] in ("file_changed_since_pin", "path_unreadable_at_commit") for s in au["stale_artifact_pins"]) and "no longer describes the file" in au["stale_pin_note"]
    assert not any(k for k in json.dumps(au).lower().split('"') if k in ("success_probability_value",))
