"""Independent return audit: clean synthetic return passes; each tampering is caught by the matching check."""
import json
import os
import shutil

import pytest

from engineering.reg_proxy import audit_return as ar
from engineering.reg_proxy import controls_synth as cs
from engineering.reg_proxy import window_count as wc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRITERIA_SHA = "1b006a519ecba7814b5107e83117c27ca75f92285d0553b0d8d4a9a3bb695402"  # frozen at 67b16d5 before the audit code; deliberately restated


@pytest.fixture(scope="module")
def good(tmp_path_factory):
    proto = json.load(open(os.path.join(cs.HERE, "protocol.json")))
    recs = cs.synth_records()
    frag, tbi, _ = cs.make_fixture(recs)
    srv = cs.Server({"/a.gz": frag, "/a.tbi.gz": tbi})
    try:
        def lib(i):
            return {"gsm": f"GSMfx{i}", "label": f"fx{i}", "dpa": 0, "replicate": i, "fragments_url": srv.url("/a.gz"), "fragments_bytes": len(frag),
                    "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)}
        ctl = {"controls": [{"name": "fxA", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400},
                            {"name": "fxB", "class": "reporter_negative", "chrom": "chr2", "start_1based": 5001, "end_1based": 5900}],
               "libraries": [lib(1), lib(2)]}
        out = str(tmp_path_factory.mktemp("ret") / "o")
        log = []
        doc, rec = wc.run(out, proto, ctl, wc.http_fetch_factory(proto, log, [srv.host], "http"))
        json.dump(log, open(os.path.join(out, "requests.json"), "w"))
        assert rec["completion_status"] == "complete", rec
        yield out, ctl, srv.url("/")
    finally:
        srv.close()


def run_audit(d, ctl, prefix):
    return ar.audit(d, ctl, host_prefix=prefix, n_expected=12)


def clone(src, tmp_path):
    d = str(tmp_path / "c")
    shutil.copytree(src, d)
    return d


def rewrite_results(d, fn):
    res = json.load(open(os.path.join(d, "results.json")))
    fn(res)
    raw = json.dumps(res, indent=1, sort_keys=True)
    open(os.path.join(d, "results.json"), "w").write(raw)
    rec = json.load(open(os.path.join(d, "receipt.json")))
    import hashlib
    rec["results_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
    json.dump(rec, open(os.path.join(d, "receipt.json"), "w"))


def failed(r):
    return {c["id"] for c in r["checks"] if not c["passed"]}


def test_criteria_bytes_are_the_frozen_ones():
    import hashlib
    assert hashlib.sha256(open(os.path.join(cs.HERE, "return_audit_criteria.json"), "rb").read()).hexdigest() == CRITERIA_SHA


def test_clean_return_passes_every_check(good):
    d, ctl, prefix = good
    r = run_audit(d, ctl, prefix)
    assert r["verdict"] == "consistent" and not failed(r) and len(r["checks"]) == 10, r["checks"]
    assert r["observations"]["fragment_rows_by_library"]["fx1"]["fxA"] > 0


def test_real_manifest_expects_330():
    ctl = json.load(open(os.path.join(cs.HERE, "controls.json")))
    assert len(ar.expected_windows(ctl)) * len(ctl["libraries"]) == 330


def mut_drop_row(d):
    rewrite_results(d, lambda r: r["windows"].pop(0))


def mut_summary(d):
    rewrite_results(d, lambda r: r["summary"][0].__setitem__("fragment_rows", r["summary"][0]["fragment_rows"] + 1))


def mut_row_count(d):
    def f(r):
        r["windows"][0]["fragment_rows"] += 1
        r["windows"][0]["dup_count_sum"] += 1
    rewrite_results(d, f)


def mut_status_unusable_but_complete(d):
    rewrite_results(d, lambda r: r["windows"][0].update(status="transport_error", detail="x"))


def mut_pvalue(d):
    rewrite_results(d, lambda r: r.__setitem__("pvalue", 0.01))


def mut_dup_row(d):
    rewrite_results(d, lambda r: r["windows"].append(dict(r["windows"][0])))


def mut_geometry(d):
    rewrite_results(d, lambda r: r["windows"][0].__setitem__("start0", r["windows"][0]["start0"] + 1))


def mut_len(d):
    rewrite_results(d, lambda r: r["windows"][0].__setitem__("window", "LEN-candidate"))


def mut_hash(d):
    rec = json.load(open(os.path.join(d, "receipt.json")))
    rec["results_sha256"] = "0" * 64
    json.dump(rec, open(os.path.join(d, "receipt.json"), "w"))


def mut_pin(d):
    rec = json.load(open(os.path.join(d, "receipt.json")))
    rec["protocol_sha256"] = "1" * 64
    json.dump(rec, open(os.path.join(d, "receipt.json"), "w"))


def mut_extra_file(d):
    open(os.path.join(d, "extra.txt"), "w").write("x")


def _reqs(d, fn):
    q = json.load(open(os.path.join(d, "requests.json")))
    fn(q)
    json.dump(q, open(os.path.join(d, "requests.json"), "w"))


def mut_drop_request(d):
    _reqs(d, lambda q: q.pop())


def mut_foreign_url(d):
    _reqs(d, lambda q: q[0].__setitem__("url", "https://example.org/x"))


def mut_range_outside(d):
    _reqs(d, lambda q: q[0].__setitem__("range", "0-999999999"))


def mut_attempt3(d):
    _reqs(d, lambda q: q.append(dict(q[0], attempt=3)))


def mut_understated_bytes(d):
    rec = json.load(open(os.path.join(d, "receipt.json")))
    rec["compressed_bytes"] -= 1
    json.dump(rec, open(os.path.join(d, "receipt.json"), "w"))


def mut_unlinked_sha(d):
    def f(r):
        for w in r["windows"]:
            if w.get("responses"):
                w["responses"][0]["sha256"] = "2" * 64
                return
    rewrite_results(d, f)


def mut_ok_without_sha(d):
    def f(q):
        for x in q:
            if x.get("ok"):
                x["sha256"] = ""
                return
    _reqs(d, f)


CASES = [("drop a row", mut_drop_row, {"C3_identities", "C5_completion"}),
         ("summary altered", mut_summary, {"C7_summary"}),
         ("row count altered", mut_row_count, {"C7_summary"}),
         ("unusable row but complete", mut_status_unusable_but_complete, {"C5_completion"}),
         ("pvalue key", mut_pvalue, {"C8_claims"}),
         ("duplicate identity", mut_dup_row, {"C3_identities"}),
         ("window geometry", mut_geometry, {"C3_identities"}),
         ("LEN identity", mut_len, {"C9_scope"}),
         ("results hash", mut_hash, {"C2_pins"}),
         ("protocol pin", mut_pin, {"C2_pins"}),
         ("extra file", mut_extra_file, {"C1_files"}),
         ("request missing", mut_drop_request, {"C6_budget"}),
         ("foreign url", mut_foreign_url, {"C6_budget"}),
         ("range outside file", mut_range_outside, {"C6_budget"}),
         ("third attempt", mut_attempt3, {"C6_budget"}),
         ("understated bytes", mut_understated_bytes, {"C6_budget"}),
         ("response sha unlinked", mut_unlinked_sha, {"C6b_linkage"}),
         ("ok request without sha", mut_ok_without_sha, {"C6_budget"})]


@pytest.mark.parametrize("label,fn,expect", CASES, ids=[c[0] for c in CASES])
def test_tampering_is_caught_by_the_matching_check(good, tmp_path, label, fn, expect):
    d, ctl, prefix = good
    c = clone(d, tmp_path)
    fn(c)
    r = run_audit(c, ctl, prefix)
    assert r["verdict"] == "inconsistent"
    assert expect <= failed(r), (label, failed(r))


def test_missing_file_is_inconsistent(good, tmp_path):
    d, ctl, prefix = good
    c = clone(d, tmp_path)
    os.remove(os.path.join(c, "requests.json"))
    assert run_audit(c, ctl, prefix)["verdict"] == "inconsistent"


def test_a_logged_retry_is_accepted_and_an_unfailed_retry_is_not(tmp_path):
    proto = json.load(open(os.path.join(cs.HERE, "protocol.json")))
    frag, tbi, _ = cs.make_fixture(cs.synth_records())
    srv = cs.Server({"/a.gz": frag, "/a.tbi.gz": tbi})
    try:
        lib = {"gsm": "GSMfx1", "label": "fx1", "dpa": 0, "replicate": 1, "fragments_url": srv.url("/a.gz"), "fragments_bytes": len(frag),
               "index_url": srv.url("/a.tbi.gz"), "index_bytes": len(tbi)}
        ctl = {"controls": [{"name": "fxA", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}], "libraries": [lib]}
        srv.fail_first = 1  # the index request fails once (IncompleteRead), then succeeds
        out = str(tmp_path / "o")
        log = []
        doc, rec = wc.run(out, proto, ctl, wc.http_fetch_factory(proto, log, [srv.host], "http"))
        json.dump(log, open(os.path.join(out, "requests.json"), "w"))
        assert [q["attempt"] for q in log[:2]] == [1, 2] and not log[0]["ok"] and log[1]["ok"]
        r = ar.audit(out, ctl, host_prefix=srv.url("/"), n_expected=3)
        assert r["verdict"] == "consistent", [c for c in r["checks"] if not c["passed"]]
        q = json.load(open(os.path.join(out, "requests.json")))
        q[0]["ok"], q[0]["http_status"], q[0]["bytes"], q[0]["sha256"] = True, 206, q[0]["range"].split("-")[1] and int(q[0]["range"].split("-")[1]) + 1, "3" * 64
        json.dump(q, open(os.path.join(out, "requests.json"), "w"))
        assert "C6_budget" in failed(ar.audit(out, ctl, host_prefix=srv.url("/"), n_expected=3))
    finally:
        srv.close()
