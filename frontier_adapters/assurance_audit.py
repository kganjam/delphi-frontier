"""Read-only lineage audit for the design-assurance mapping: which typed hooks exist in each direction, which LIVE records they connect to today (exact ids and versions),
and where a pin has gone stale. SPEC-008: "Lineage is bidirectional: source passage/data -> Claim -> equation/model -> Action -> Evidence/artifact -> design element, with
reverse usage queries ... The integration audit reports orphaned artifacts, unpinned equations and missing producers instead of silently displaying them as grounded."

Read-only: every query runs in a READ ONLY transaction over PUBLIC non-Event records; nothing is written, nothing is executed, no URI is fetched. No metric, probability or
ranking is produced: counts are counts of records and hooks.
"""
from __future__ import annotations

import json
import re
import typing
from collections import Counter, defaultdict

from frontier import graph
from frontier import models as M
from frontier.models import ArtifactRef, Ref

from .assurance_actions import MAP_PATH
from .common import sha_bytes

GIT_TITLE = re.compile(r"\[git:delphi-frontier@([0-9a-f]{40}):([^\]]+)\]")


# --------------------------------------------------------------------------------------------------------------------------
# 1. hooks that exist in the SCHEMA, read from the models themselves, and which of them have a reverse index
# --------------------------------------------------------------------------------------------------------------------------
def _is_ref_type(t) -> str | None:
    args = typing.get_args(t)
    if t is Ref:
        return "Ref"
    if t is ArtifactRef:
        return "ArtifactRef"
    for a in args:
        r = _is_ref_type(a)
        if r:
            return r
    return None


def _walk_models():
    seen = set()
    stack = [M.Claim, M.Problem, M.Evidence, M.Assessment, M.Action, M.Dimension, M.ActionProposal, M.Interest]
    while stack:
        cls = stack.pop()
        if cls in seen:
            continue
        seen.add(cls)
        yield cls
        for f in cls.model_fields.values():
            for a in (f.annotation, *typing.get_args(f.annotation)):
                for b in (a, *typing.get_args(a)):
                    if isinstance(b, type) and issubclass(b, M.Model) and b not in seen:
                        stack.append(b)


def schema_hooks() -> dict:
    """Forward hooks: every model field typed Ref / list[Ref] / ArtifactRef. Reverse: the relations `references()` emits into the typed-edge index (queryable backwards)."""
    forward = []
    for cls in _walk_models():
        for name, f in cls.model_fields.items():
            kind = _is_ref_type(f.annotation)
            if kind:
                forward.append({"model": cls.__name__, "field": name, "pointer": kind})
    probe_ref = {"namespace": "n", "kind": "Claim", "id": "x", "version": "0" * 64}
    indexed = {}
    for kind, payload in {
        "Evidence": {"target": probe_ref, "produced_by": {**probe_ref, "kind": "Action"}},
        "Action": {"target": probe_ref, "inputs": [probe_ref], "proposal": {"plan_steps": [{**probe_ref, "kind": "Action"}]}},
        "Problem": {"dependencies": [probe_ref]},
        "Assessment": {"target": probe_ref, "dimensions": {"d": {"evidence_links": [probe_ref]}}},
    }.items():
        indexed[kind] = sorted({rel for rel, _ in M.references({"kind": kind, "payload": payload})})
    rel_for = {("Evidence", "target"): "targets", ("Evidence", "produced_by"): "produced_by", ("Action", "target"): "targets", ("Action", "inputs"): "uses",
               ("ActionProposal", "plan_steps"): "plans_step", ("Problem", "dependencies"): "depends_on", ("Assessment", "target"): "targets",
               ("Dimension", "evidence_links"): "review_evidence", ("Interest", "target"): "targets"}
    out = []
    for h in forward:
        rel = rel_for.get((h["model"], h["field"]))
        owner = "Assessment" if h["model"] == "Dimension" else ("Action" if h["model"] == "ActionProposal" else h["model"])
        reverse = ("typed_edges relation '" + rel + "' (indexed on target_version; frontier.graph incoming edges)") if rel and rel in indexed.get(owner, []) else (
            "ArtifactIndex search by sha256/role (a separate index)" if h["pointer"] == "ArtifactRef" else "none: forward only")
        out.append({**h, "typed_edge_relation": rel, "reverse_query": reverse, "bidirectional": reverse.startswith(("typed_edges", "ArtifactIndex"))})
    untyped = ["Problem.payload.original.claim_ids (untyped ids; the graph draws them as tentative edges only)", "Evidence.payload.provenance.datasets (untyped declarations)",
               "Claim.payload.source_record_version (a string, not a Ref)", "Claim/Problem Source.locator (a git locator string, not a Ref)"]
    return {"forward_fields": sorted(out, key=lambda h: (h["model"], h["field"])), "typed_edge_relations_emitted": indexed, "untyped_lineage_text_not_queryable_backwards": untyped,
            "bidirectional_count": sum(1 for h in out if h["bidirectional"]), "forward_only_count": sum(1 for h in out if not h["bidirectional"])}


# --------------------------------------------------------------------------------------------------------------------------
# 2. live records (read-only)
# --------------------------------------------------------------------------------------------------------------------------
def _rows(store, sql: str, args: tuple) -> list:
    with store.connection() as c:
        c.execute("SET TRANSACTION READ ONLY")
        return c.execute(sql, args).fetchall()


def _pins_of(env: dict) -> set:
    p = env["payload"]
    shas = set()
    src = p.get("source")
    if isinstance(src, dict) and src.get("content_sha256"):
        shas.add(src["content_sha256"])
    for a in p.get("artifacts") or []:
        if isinstance(a, dict) and a.get("sha256"):
            shas.add(a["sha256"])
    return shas


def _record_view(row) -> dict:
    e = row["envelope"]
    return {"ref": {k: e[k] for k in ("namespace", "kind", "id", "version")}, "local_status": row["status"], "is_head": row["is_head"]}


def records_citing_path(store, path: str, limit: int = 40) -> list:
    """Public records whose payload text names this repository path (a text match, reported as such), with their pins."""
    rows = _rows(store, "SELECT v.envelope, s.status, (h.version IS NOT NULL) AS is_head FROM record_versions v LEFT JOIN local_states s ON s.version = v.version "
                        "LEFT JOIN heads h ON h.version = v.version WHERE v.visibility = 'public' AND v.kind <> 'Event' AND v.envelope::text LIKE %s "
                        "ORDER BY v.namespace, v.kind, v.record_id, v.version LIMIT %s", (f"%{path}%", limit))
    return rows


def hooks_for_item(store, item_id: str, pins: list[dict]) -> list:
    out, seen = [], set()
    for pin in pins:
        for row in records_citing_path(store, pin["path"]):
            e = row["envelope"]
            key = (e["namespace"], e["kind"], e["id"], e["version"])
            if key in seen:
                continue
            seen.add(key)
            have = _pins_of(e)
            relation = "pin_matches_map" if pin["sha256_map"] in have else ("pin_differs_from_map" if have else "no_content_pin_on_record")
            g = graph.view(store, {k: e[k] for k in ("namespace", "kind", "id", "version")}, depth=1, limit=60)
            incoming = [x for x in g["edges"] if x["to"] == graph.node_id({k: e[k] for k in ("namespace", "kind", "id", "version")})]
            out.append({**_record_view(row), "basis": f"public record text names '{pin['path']}' (a text match, not a typed reference)", "map_pin": {"path": pin["path"], "sha256": pin["sha256_map"], "selector": pin["selector"]},
                        "pin_relation": relation, "usable_as_exact_input": relation == "pin_matches_map",
                        "reverse_usage_incoming_edges": {"count": len(incoming), "by_kind": dict(Counter(x["kind"] for x in incoming)), "from": sorted({x["from"] for x in incoming})[:8]}})
    return out


def resolve_claim_refs(store, claim_refs: list) -> list:
    out = []
    for cr in claim_refs:
        r = cr["ref"]
        exact = _rows(store, "SELECT v.envelope, s.status, (h.version IS NOT NULL) AS is_head FROM record_versions v LEFT JOIN local_states s ON s.version = v.version LEFT JOIN heads h ON h.version = v.version "
                             "WHERE v.visibility = 'public' AND v.version = %s AND v.namespace = %s AND v.kind = %s AND v.record_id = %s", (r["version"], r["namespace"], r["kind"], r["id"]))
        same_id = _rows(store, "SELECT v.envelope, s.status, (h.version IS NOT NULL) AS is_head FROM record_versions v LEFT JOIN local_states s ON s.version = v.version LEFT JOIN heads h ON h.version = v.version "
                               "WHERE v.visibility = 'public' AND v.kind = %s AND v.record_id = %s ORDER BY v.namespace, v.version LIMIT 6", (r["kind"], r["id"]))
        out.append({"map_ref": r, "map_status": cr["status"], "subsystem": cr.get("subsystem"),
                    "live": "exact_version_present" if exact else ("same_kind_and_id_elsewhere" if same_id else "absent"),
                    "same_kind_and_id_in_store": [_record_view(x)["ref"] | {"local_status": x["status"]} for x in same_id]})
    return out


def stale_artifact_pins(store, repo: str, commit: str, read_blob) -> list:
    """Live artifact pins whose git locator names a file whose bytes at `commit` now hash differently: the producer re-wrote the file after the record was made."""
    rows = _rows(store, "SELECT v.envelope, s.status FROM record_versions v LEFT JOIN local_states s ON s.version = v.version WHERE v.visibility = 'public' AND v.kind = 'Evidence' "
                        "AND jsonb_array_length(coalesce(v.envelope->'payload'->'artifacts', '[]'::jsonb)) > 0 ORDER BY v.namespace, v.record_id, v.version", ())
    out = []
    for row in rows:
        e = row["envelope"]
        for a in e["payload"]["artifacts"]:
            m = GIT_TITLE.search(a.get("title", ""))
            if not m:
                continue
            try:
                now = sha_bytes(read_blob(repo, commit, m.group(2)))
            except Exception:  # noqa: BLE001 - a file that cannot be read is reported as such
                out.append({"evidence": {k: e[k] for k in ("namespace", "id", "version")}, "path": m.group(2), "pinned_sha256": a["sha256"], "state": "path_unreadable_at_commit"})
                continue
            if now != a["sha256"]:
                out.append({"evidence": {k: e[k] for k in ("namespace", "id", "version")}, "path": m.group(2), "pinned_at_commit": m.group(1), "pinned_sha256": a["sha256"],
                            "sha256_at_checked_commit": now, "checked_commit": commit, "state": "file_changed_since_pin"})
    return out


# --------------------------------------------------------------------------------------------------------------------------
# 3. orphan / unpinned audit over the map itself (SPEC-008 integration audit)
# --------------------------------------------------------------------------------------------------------------------------
def map_audit(m: dict, repo: str, commit: str, read_blob) -> dict:
    eqs = m["equation_registry"]
    no_sources = [e["id"] for e in eqs if not e.get("sources")]
    no_check = [e["id"] for e in eqs if not e.get("check_evidence")]
    unpinned = []
    for e in eqs:
        for s in e.get("sources") or []:
            if not s.get("sha256"):
                unpinned.append(e["id"])
    refs_with_ns = Counter(cr["ref"]["namespace"] for cr in m["claim_refs"])
    return {"equations": len(eqs), "equations_without_sources": no_sources, "equations_without_check_evidence": no_check, "equation_sources_without_sha256": sorted(set(unpinned)),
            "claim_refs": len(m["claim_refs"]), "claim_refs_by_namespace": dict(refs_with_ns),
            "claim_ref_status_values": dict(Counter(cr["status"] for cr in m["claim_refs"])),
            "evidence_index_pins": len(m["evidence_index"]), "map_itself_in_store": "not asserted: the map is a repository artifact; it is not a store Evidence record unless someone imports it",
            "nodes_with_no_equation_ids": sorted(n["id"] for n in m["nodes"] if n["kind"] != "model" and not n.get("equation_ids"))}


def audit(store, repo: str, commit: str, mapping: dict, m: dict, read_blob, tip_commit: str | None = None) -> dict:
    hooks_by_item = {}
    for row in mapping["rows"]:
        it = row["assurance_item"]
        hooks_by_item[it["id"]] = hooks_for_item(store, it["id"], row["evidence_pins"])
    total = _rows(store, "SELECT count(*) AS n FROM record_versions v WHERE v.visibility = 'public' AND v.kind <> 'Event'", ())[0]["n"]
    return {
        "schema": "frontier.assurance-lineage-audit/1", "read_only": True, "map": {"path": MAP_PATH, "sha256_in_mapping": mapping["source"]["map_sha256"], "commit": commit},
        "scope": {"records_visible": total, "visibility": "public, non-Event", "namespaces_read": "all", "queries": "READ ONLY transactions; text match on payload; no URI fetched"},
        "schema_hooks": schema_hooks(), "hooks_by_item": hooks_by_item, "claim_ref_resolution": resolve_claim_refs(store, m["claim_refs"]),
        "stale_artifact_pins": stale_artifact_pins(store, repo, tip_commit or commit, read_blob), "map_audit": map_audit(m, repo, commit, read_blob),
        "stale_pin_note": "file_changed_since_pin: the pin still identifies the bytes at ITS OWN commit correctly; it no longer describes the file at the checked commit. A refreshed record needs a new id (the same id would fork).",
        "no_metric_statement": "Counts are counts of records and hooks. No success probability, expected information, utility, confidence or ranking is produced.",
    }


def main(argv=None) -> int:
    """Read-only driver: audit the live store, then write the mapping with those hooks attached, plus the frozen bundle. Writes files only."""
    import argparse
    import os
    from . import assurance_actions as A
    from .artifacts import git_blob
    ap = argparse.ArgumentParser(prog="python -m frontier_adapters.assurance_audit")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--source-commit", required=True)
    ap.add_argument("--dsn", required=True, help="libpq DSN; use options='-c default_transaction_read_only=on'")
    ap.add_argument("--namespace", required=True, help="the store's own namespace (to open it); reads span all public namespaces")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    from frontier.store import Store
    commit = A.resolve_commit(a.repo, a.source_commit)
    chain, mapping = A.build(a.repo, commit)
    m = json.loads(chain.blob(A.MAP_PATH))
    au = audit(Store(a.dsn, a.namespace), a.repo, commit, mapping, m, git_blob)
    from datetime import datetime, timezone
    au["read_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    chain2, mapping2 = A.build(a.repo, commit, live_hooks=au["hooks_by_item"])
    out = A.write_frozen(a.out, chain2, mapping2)
    with open(os.path.join(a.out, "lineage_audit.json"), "w") as fh:
        fh.write(json.dumps(au, indent=1, sort_keys=True, default=str) + "\n")
    print(json.dumps({"records": len(out["bundle"]["records"]), "bundle_sha256": out["bundle"]["bundle_sha256"], "stale_pins": len(au["stale_artifact_pins"]),
                      "items_with_live_hooks": sum(1 for v in au["hooks_by_item"].values() if v), "out": a.out}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
