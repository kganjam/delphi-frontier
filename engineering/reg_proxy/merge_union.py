"""Union of the v1 partial run and the single missing-only recovery run, with immutable lineage (recovery_contract.json, frozen first).

Offline. Inputs are never modified. Every union row is a source row unchanged plus its lineage; counts from different runs are never
merged, averaged or imputed; a union is `complete` only if all 330 identities are present and usable."""
import hashlib
import json
import os
import sys

from engineering.reg_proxy import audit_return as ar

# restated from recovery_contract.json (frozen at 8543c5d) on purpose: the merger must not trust the inputs for its own pins
PARENT_RESULTS_SHA = "f2eb5178787e371cb53f58f4b725feaa8a2f26ae4df5e4c0f2b99b776a31ac8a"
PARENT_RECEIPT_SHA = "cf1e05acf581802e9c774160bc994da2870845d14851e8435c34e5d2b4dd7955"
CONTRACT_SHA = "c7edb1c59657e81bca262ad0d5206c845ed888cf22a392d7b7c9305c045bcd8e"
USABLE = ar.USABLE


class Refused(Exception):
    pass


def _read(d, name):
    raw = open(os.path.join(d, name), "rb").read()
    return raw, json.loads(raw)


def merge(parent_dir, recovery_dir, out, controls=None, n_recovery=165, host_prefix=f"https://{ar.HOST}/"):
    controls = controls or json.load(open(os.path.join(ar.HERE, "controls.json")))
    praw, pres = _read(parent_dir, "results.json")
    prcp_raw, prcp = _read(parent_dir, "receipt.json")
    rraw, rres = _read(recovery_dir, "results.json")
    rrcp_raw, rrcp = _read(recovery_dir, "receipt.json")
    if hashlib.sha256(praw).hexdigest() != PARENT_RESULTS_SHA:
        raise Refused("parent results sha256 differs from the pin")
    if hashlib.sha256(prcp_raw).hexdigest() != PARENT_RECEIPT_SHA or prcp["results_sha256"] != PARENT_RESULTS_SHA:
        raise Refused("parent receipt differs from the pin")
    if rrcp["results_sha256"] != hashlib.sha256(rraw).hexdigest():
        raise Refused("recovery receipt does not match its results")
    pins = ar.RECOVERY["pins"]
    drift = [k for k, v in pins.items() if rrcp.get(k) != v]
    if drift:
        raise Refused(f"recovery run pins differ: {drift}")
    rep = ar.audit(recovery_dir, controls, host_prefix=host_prefix, n_expected=n_recovery, profile=ar.RECOVERY)
    if rep["verdict"] != "consistent":
        raise Refused("recovery run fails the recovery audit: " + ",".join(c["id"] for c in rep["checks"] if not c["passed"]))

    prows, rrows = pres["windows"], rres["windows"]
    pid = {(r["library"], r["window"]): i for i, r in enumerate(prows)}
    rid = {(r["library"], r["window"]): i for i, r in enumerate(rrows)}
    if len(pid) != len(prows) or len(rid) != len(rrows):
        raise Refused("duplicate identity inside a run")
    p_unusable = {k for k, i in pid.items() if prows[i]["status"] not in USABLE}
    if set(rid) != p_unusable:
        raise Refused(f"recovery identities differ from the parent's unusable identities: only_recovery={len(set(rid) - p_unusable)} only_parent={len(p_unusable - set(rid))}")
    if set(rid) & {k for k in pid if k not in p_unusable}:
        raise Refused("overlap with a usable parent identity")

    union = []
    for k, i in pid.items():
        if k in rid:
            j = rid[k]
            row = dict(rrows[j]) | {"run": "recovery-v1", "source_results_sha256": hashlib.sha256(rraw).hexdigest(), "source_row_index": j,
                                    "parent_row": {"status": prows[i]["status"], "detail": prows[i].get("detail"), "source_row_index": i}}
        else:
            row = dict(prows[i]) | {"run": "v1", "source_results_sha256": PARENT_RESULTS_SHA, "source_row_index": i}
        union.append(row)
    expected = {(lib["label"], w[0]) for lib in controls["libraries"] for w in ar.expected_windows(controls)}
    if {(r["library"], r["window"]) for r in union} != expected or len(union) != len(expected):
        raise Refused("union identities differ from the 330 expected")
    mixed = [lib for lib in {r["library"] for r in union} if len({r["run"] for r in union if r["library"] == lib}) > 1]
    if mixed:
        raise Refused(f"a library mixes runs: {sorted(mixed)} (windows and their comparison windows must share a run)")
    unresolved = [[r["library"], r["window"]] for r in union if r["status"] not in USABLE]
    status = "complete" if not unresolved and len(union) == len(expected) else "partial_data"
    src_fields = ("run", "source_results_sha256", "source_row_index", "parent_row")
    for r in union:  # every union row must equal its source row unchanged
        src = (prows if r["run"] == "v1" else rrows)[r["source_row_index"]]
        if {k: v for k, v in r.items() if k not in src_fields} != src:
            raise Refused("a union row differs from its source row")
    doc = {"schema": "frontier.reg-proxy.union/1", "completion_status": status, "windows": union, "summary": ar.summary_rows(union),
           "unresolved_identities": unresolved,
           "lineage": {"parent_results_sha256": PARENT_RESULTS_SHA, "recovery_results_sha256": hashlib.sha256(rraw).hexdigest(), "contract_sha256": CONTRACT_SHA},
           "claim_limits": "descriptive library counts; accessibility is context, not function; LEN excluded; no test, threshold or rank; counts from the two runs are never merged or rescaled"}
    if os.path.exists(out):
        raise Refused(f"{out} exists: refuse to reuse an output directory")
    os.makedirs(out)
    body = json.dumps(doc, indent=1, sort_keys=True)
    open(os.path.join(out, "union.json"), "w").write(body)
    rec = {"schema": "frontier.reg-proxy.union-receipt/1", "completion_status": status, "expected_identities": len(expected), "present_identities": len(union),
           "usable_identities": len(union) - len(unresolved), "from_v1": sum(r["run"] == "v1" for r in union), "from_recovery": sum(r["run"] == "recovery-v1" for r in union),
           "unresolved_identities": unresolved, "parent_results_sha256": PARENT_RESULTS_SHA, "parent_receipt_sha256": PARENT_RECEIPT_SHA,
           "recovery_results_sha256": hashlib.sha256(rraw).hexdigest(), "recovery_receipt_sha256": hashlib.sha256(rrcp_raw).hexdigest(),
           "contract_sha256": CONTRACT_SHA, "union_sha256": hashlib.sha256(body.encode()).hexdigest(),
           "meaning": "consistent lineage, not biological validation; the v1 partial result remains the original record"}
    json.dump(rec, open(os.path.join(out, "union_receipt.json"), "w"), indent=1, sort_keys=True)
    return doc, rec


def verify(parent_dir, recovery_dir, union_dir, controls=None, n_recovery=165, host_prefix=f"https://{ar.HOST}/"):
    """Re-derive the union from the two source runs and require byte equality; also refuse any promotion."""
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(), "u")
    doc, rec = merge(parent_dir, recovery_dir, tmp, controls, n_recovery, host_prefix)
    for n in ("union.json", "union_receipt.json"):
        if open(os.path.join(tmp, n), "rb").read() != open(os.path.join(union_dir, n), "rb").read():
            raise Refused(f"{n} is not the deterministic union of its sources")
    got = json.load(open(os.path.join(union_dir, "union.json")))
    unusable = [r for r in got["windows"] if r["status"] not in USABLE]
    if got["completion_status"] == "complete" and (got["unresolved_identities"] or unusable or len(got["windows"]) != rec["expected_identities"]):
        raise Refused("completion promoted with missing or unusable identities")
    return rec


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) < 3:
        raise SystemExit("usage: merge_union PARENT_SCIENCE_DIR RECOVERY_SCIENCE_DIR OUT_DIR | --verify PARENT RECOVERY UNION")
    try:
        if a[0] == "--verify":
            print(json.dumps(verify(a[1], a[2], a[3]), indent=1, sort_keys=True))
        else:
            print(json.dumps(merge(a[0], a[1], a[2])[1], indent=1, sort_keys=True))
    except Refused as e:
        print(f"REFUSED: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
