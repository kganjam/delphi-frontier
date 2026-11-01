"""Durable lineage of the v1 partial, the missing-only recovery and their union: committed bytes match their pins and the union is reproducible."""
import hashlib
import json
import os

from engineering.reg_proxy import audit_return as ar
from engineering.reg_proxy import merge_union as mu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(ROOT, "artifacts", "reg-proxy", "lineage")
U = os.path.join(ROOT, "artifacts", "reg-proxy", "union-v1")
V1, REC = os.path.join(L, "v1"), os.path.join(L, "recovery-v1")
RECOVERY_RESULTS_SHA = "d2d60603c60bbff422c41c155225e297079fa7c7e7284d0b465b5bc420b6f540"  # reported by infra for the returned run; restated on purpose
UNION_SHA = "74441883b37c8bd1aa2c07cc499aad74d94026396d983b3348dc4fe78fe2749a"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def test_committed_raw_copies_match_their_pins():
    assert sha(os.path.join(V1, "results.json")) == mu.PARENT_RESULTS_SHA and sha(os.path.join(V1, "receipt.json")) == mu.PARENT_RECEIPT_SHA
    assert sha(os.path.join(REC, "results.json")) == RECOVERY_RESULTS_SHA


def test_recovery_run_passes_the_frozen_recovery_audit():
    r = ar.audit(REC, profile=ar.RECOVERY, n_expected=165)
    assert r["verdict"] == "consistent", [c for c in r["checks"] if not c["passed"]]


def test_union_is_reproduced_byte_for_byte_and_not_promoted(tmp_path):
    doc, rec = mu.merge(V1, REC, str(tmp_path / "u"))
    for n in ("union.json", "union_receipt.json"):
        assert sha(str(tmp_path / "u" / n)) == sha(os.path.join(U, n))
    assert rec["union_sha256"] == UNION_SHA == json.load(open(os.path.join(U, "union_receipt.json")))["union_sha256"]
    assert (rec["completion_status"], rec["usable_identities"], rec["from_v1"], rec["from_recovery"], len(rec["unresolved_identities"])) == ("partial_data", 271, 165, 165, 59)
    assert mu.verify(V1, REC, U)["union_sha256"] == UNION_SHA
    assert {tuple(x)[0] for x in rec["unresolved_identities"]} == {"1dpa2", "2dpa1"}
