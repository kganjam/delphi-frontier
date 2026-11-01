"""Missing-only recovery: frozen contract, controls (same code as the remote run), mutation checks, union lineage and recovery audit."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

import pytest

from engineering.reg_proxy import audit_return as ar
from engineering.reg_proxy import controls_recovery as cr
from engineering.reg_proxy import controls_synth as cs
from engineering.reg_proxy import merge_union as mu
from engineering.reg_proxy import recovery as rc
from engineering.reg_proxy import window_count as wc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "engineering", "reg_proxy")
HP = "http://127.0.0.1"  # the local Range server used for the synthetic runs
CONTRACT_SHA = "c7edb1c59657e81bca262ad0d5206c845ed888cf22a392d7b7c9305c045bcd8e"  # frozen at 8543c5d before any recovery code; deliberately restated


def sha(n):
    return hashlib.sha256(open(os.path.join(PKG, n), "rb").read()).hexdigest()


def test_contract_and_pins_are_the_frozen_ones():
    assert sha("recovery_contract.json") == CONTRACT_SHA == mu.CONTRACT_SHA == ar.RECOVERY["pins"]["contract_sha256"]
    assert sha("protocol.json") == ar.PIN["protocol_sha256"] and sha("transport_amendment.json") == ar.PIN["amendment_sha256"] and sha("transport_amendment_2.json") == ar.PIN["amendment2_sha256"]
    c = json.load(open(os.path.join(PKG, "recovery_contract.json")))
    assert c["parent"]["results_sha256"] == rc.PARENT_RESULTS_SHA == mu.PARENT_RESULTS_SHA == ar.RECOVERY["pins"]["parent_results_sha256"]
    assert c["parent"]["receipt_sha256"] == mu.PARENT_RECEIPT_SHA


def run_recovery_controls(cwd):
    p = subprocess.run([sys.executable, "-m", "engineering.reg_proxy.controls_recovery"], cwd=cwd, capture_output=True, text=True, timeout=240)
    try:
        return p.returncode, json.loads(p.stdout)["controls"]
    except ValueError:
        return p.returncode, []


def test_recovery_controls_pass_on_the_committed_code():
    rc_, ctl = run_recovery_controls(ROOT)
    assert rc_ == 0 and len(ctl) == 11 and all(c["passed"] for c in ctl), [c for c in ctl if not c["passed"]]


MUTATIONS = [
    ('if self.recovery and not body:', 'if False:', "empty_206 classification"),
    ('self.sleep(wait)', 'pass', "schedule waits taken"),
    ('if self.budget.clock() - self.budget.t0 + wait > self.budget.b["runtime_hard_s"]:', 'if False:', "no sleeping past the bound"),
    ('rec["headers"] = {h: r.headers.get(h) for h in ALLOWED_HEADERS if r.headers.get(h) is not None}', 'rec["headers"] = {h: r.headers.get(h) for h in r.headers.keys()}', "header allow-list"),
    ('waits = list(schedule) if schedule else [0] * self.attempts', 'waits = [0] * self.attempts', "index schedule used"),
    ('self.budget.precheck(expected + 1)', 'self.budget.precheck(expected)', "reservation"),
    ('rec["wait_before_s"], rec["t_clock"] = wait, t_attempt', 'pass', "wait and clock logged"),
]


@pytest.mark.parametrize("old,new,label", MUTATIONS, ids=[m[2] for m in MUTATIONS])
def test_mutated_transport_fails_a_recovery_control(tmp_path, old, new, label):
    dst = tmp_path / "m"
    (dst / "engineering").mkdir(parents=True)
    shutil.copy(ROOT + "/engineering/__init__.py", dst / "engineering" / "__init__.py")
    shutil.copytree(PKG, dst / "engineering" / "reg_proxy", ignore=shutil.ignore_patterns("__pycache__"))
    f = dst / "engineering" / "reg_proxy" / "window_count.py"
    src = f.read_text()
    assert src.count(old) == 1, f"mutation target {label!r} not found exactly once"
    f.write_text(src.replace(old, new))
    rc_, ctl = run_recovery_controls(dst)
    assert rc_ != 0 or any(not c["passed"] for c in ctl), f"mutation {label!r} survived"
    assert ctl or rc_ != 0


# ---------- union lineage on a synthetic parent + recovery ----------

@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    mp = None
    proto_r, _, contract = rc.load()
    proto = json.load(open(os.path.join(PKG, "protocol.json")))
    recs = cs.synth_records()
    frag, tbi, _ = cs.make_fixture(recs)
    srv = cs.Server({"/a.gz": frag, "/a.tbi.gz": tbi, "/c.tbi.gz": tbi})
    try:
        def lib(label, ok_index):
            return {"gsm": "GSM" + label, "label": label, "dpa": 0, "replicate": 1, "fragments_url": srv.url("/a.gz"), "fragments_bytes": len(frag),
                    "index_url": srv.url("/a.tbi.gz" if ok_index else "/c.tbi.gz"), "index_bytes": len(tbi)}
        controls = {"controls": [{"name": "fx", "class": "reporter_positive", "chrom": "chr1", "start_1based": 1001, "end_1based": 2400}],
                    "libraries": [lib("lA", True), lib("lB", True), lib("lC", False)]}
        base = tmp_path_factory.mktemp("u")
        # parent: lA good; lB and lC fail their index (empty 206 for the first 4 index requests: 2 attempts x 2 libraries)
        srv.empty_first = 0
        plog = []
        pf = wc.http_fetch_factory(proto, plog, [srv.host], "http")
        n = {"i": 0}

        def pmake(url, total, b):
            f = pf(url, total, b)
            if url.endswith(".tbi.gz"):
                n["i"] += 1
                srv.empty_first = 2 if n["i"] in (2, 3) else 0
            return f
        pdoc, prec = wc.run(str(base / "parent"), proto, controls, pmake)
        srv.empty_first = 0
        mp = pytest.MonkeyPatch()
        mp.setattr(rc, "PARENT_RESULTS_SHA", hashlib.sha256((base / "parent" / "results.json").read_bytes()).hexdigest())
        assert prec["completion_status"] == "partial_data" and prec["usable_identities"] == 3, prec
        json.dump(plog, open(base / "parent" / "requests.json", "w"))
        # recovery: only lB and lC
        sub = controls | {"libraries": controls["libraries"][1:]}
        ck = cr.FakeClock()
        rlog = []
        bud = wc.Budget(proto_r["bounds"], ck.now)
        base_f = wc.http_fetch_factory(proto_r, rlog, [srv.host], "http", sleep=ck.sleep, recovery=True)
        rdoc, rrec = rc.run_recovery(str(base / "recovery"), proto_r, sub, contract, base_f, clock=ck.now, budget=bud)
        json.dump(rlog, open(base / "recovery" / "requests.json", "w"), indent=1)
        # a second recovery in which library lC's index keeps failing (the C index server mode is switched per URL)
        ck2 = cr.FakeClock()
        bud2 = wc.Budget(proto_r["bounds"], ck2.now)
        b2 = wc.http_fetch_factory(proto_r, [], [srv.host], "http", sleep=ck2.sleep, recovery=True)
        log2 = []
        b2 = wc.http_fetch_factory(proto_r, log2, [srv.host], "http", sleep=ck2.sleep, recovery=True)

        def make2(url, total, b):
            srv.mode = "empty_206" if url.endswith("/c.tbi.gz") else "ok"
            return b2(url, total, b)
        r2doc, r2rec = rc.run_recovery(str(base / "recovery2"), proto_r, sub, contract, make2, clock=ck2.now, budget=bud2)
        srv.mode = "ok"
        json.dump(log2, open(base / "recovery2" / "requests.json", "w"), indent=1)
        assert r2rec["completion_status"] == "partial_data" and r2rec["usable_identities"] == 3, r2rec
        yield {"base": base, "controls": controls, "sub": sub, "prec": prec, "rrec": rrec}
    finally:
        srv.close()
        mp.undo()


@pytest.fixture
def pinned(runs, monkeypatch):
    b = runs["base"]
    prec = json.load(open(b / "parent" / "receipt.json"))
    pr = hashlib.sha256((b / "parent" / "results.json").read_bytes()).hexdigest()
    monkeypatch.setattr(mu, "PARENT_RESULTS_SHA", pr)
    monkeypatch.setattr(mu, "PARENT_RECEIPT_SHA", hashlib.sha256((b / "parent" / "receipt.json").read_bytes()).hexdigest())
    monkeypatch.setattr(rc, "PARENT_RESULTS_SHA", pr)
    prof = ar.RECOVERY | {"libraries": ["lB", "lC"], "pins": ar.RECOVERY["pins"] | {"parent_results_sha256": pr}}
    monkeypatch.setattr(ar, "RECOVERY", prof)
    return runs | {"parent_receipt": prec, "pr": pr}


def test_recovery_run_is_consistent_under_the_recovery_audit(pinned):
    r = ar.audit(str(pinned["base"] / "recovery"), pinned["sub"], host_prefix="http://127.0.0.1", n_expected=6, profile=ar.RECOVERY)
    assert r["verdict"] == "consistent", [c for c in r["checks"] if not c["passed"]]


def test_union_keeps_lineage_and_does_not_promote(pinned, tmp_path):
    out = str(tmp_path / "u")
    ctl = pinned["controls"]
    doc, rec = mu.merge(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery"), out, ctl, n_recovery=6, host_prefix=HP)
    assert rec["expected_identities"] == 9 and rec["from_v1"] == 3 and rec["from_recovery"] == 6, rec
    src_p = json.load(open(pinned["base"] / "parent" / "results.json"))["windows"]
    src_r = json.load(open(pinned["base"] / "recovery" / "results.json"))["windows"]
    for r in doc["windows"]:
        src = (src_p if r["run"] == "v1" else src_r)[r["source_row_index"]]
        assert {k: v for k, v in r.items() if k not in ("run", "source_results_sha256", "source_row_index", "parent_row")} == src
    assert all(r["parent_row"]["status"] == "library_unavailable" for r in doc["windows"] if r["run"] == "recovery-v1")
    assert (rec["completion_status"] == "complete") == (not rec["unresolved_identities"])
    assert mu.verify(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery"), out, ctl, n_recovery=6, host_prefix=HP)["union_sha256"] == rec["union_sha256"]
    # inputs are untouched
    assert hashlib.sha256((pinned["base"] / "parent" / "results.json").read_bytes()).hexdigest() == pinned["pr"]


def _copy(pinned, tmp_path):
    d = tmp_path / "x"
    shutil.copytree(pinned["base"], d)
    return d


def test_a_still_failing_library_stays_unresolved_in_the_union(pinned, tmp_path):
    ctl = pinned["controls"]
    doc, rec = mu.merge(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery2"), str(tmp_path / "u"), ctl, n_recovery=6, host_prefix=HP)
    assert rec["completion_status"] == "partial_data" and rec["usable_identities"] == 6 and len(rec["unresolved_identities"]) == 3, rec
    assert {tuple(x)[0] for x in rec["unresolved_identities"]} == {"lC"}
    assert all(r["status"] == "library_unavailable" and r["run"] == "recovery-v1" and r["parent_row"]["status"] == "library_unavailable" for r in doc["windows"] if r["library"] == "lC")
    assert not any(s["library"] == "lC" and "fragment_rows" in s for s in doc["summary"])


def test_merger_refusals(pinned, tmp_path, monkeypatch):
    ctl = pinned["controls"]

    def merge(d, **kw):
        return mu.merge(str(d / "parent"), str(d / "recovery"), str(tmp_path / f"o{len(os.listdir(tmp_path))}"), ctl, n_recovery=6, host_prefix=HP)

    # parent drift
    (tmp_path / "a").mkdir()
    d = _copy(pinned, tmp_path / "a")
    res = json.load(open(d / "parent" / "results.json"))
    res["windows"][0]["fragment_rows"] += 1
    json.dump(res, open(d / "parent" / "results.json", "w"))
    with pytest.raises(mu.Refused, match="parent results"):
        merge(d)
    # recovery drift: results altered after the receipt hash
    (tmp_path / "b").mkdir()
    d = _copy(pinned, tmp_path / "b")
    res = json.load(open(d / "recovery" / "results.json"))
    res["windows"][0]["fragment_rows"] = 1
    json.dump(res, open(d / "recovery" / "results.json", "w"))
    with pytest.raises(mu.Refused, match="recovery receipt"):
        merge(d)
    # pin drift in the recovery receipt
    (tmp_path / "c").mkdir()
    d = _copy(pinned, tmp_path / "c")
    rcp = json.load(open(d / "recovery" / "receipt.json"))
    rcp["contract_sha256"] = "0" * 64
    json.dump(rcp, open(d / "recovery" / "receipt.json", "w"))
    with pytest.raises(mu.Refused, match="pins differ"):
        merge(d)
    # overlap: a recovery row for an identity the parent already has usable
    (tmp_path / "d").mkdir()
    d = _copy(pinned, tmp_path / "d")
    rres = json.load(open(d / "recovery" / "results.json"))
    prow = [r for r in json.load(open(d / "parent" / "results.json"))["windows"] if r["status"] == "ok"][0]
    rres["windows"][0] = dict(prow)
    raw = json.dumps(rres)
    open(d / "recovery" / "results.json", "w").write(raw)
    rcp = json.load(open(d / "recovery" / "receipt.json"))
    rcp["results_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
    json.dump(rcp, open(d / "recovery" / "receipt.json", "w"))
    with pytest.raises(mu.Refused):
        merge(d)
    # output reuse
    (tmp_path / "e").mkdir()
    out = tmp_path / "e" / "o"
    mu.merge(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery"), str(out), ctl, n_recovery=6, host_prefix=HP)
    with pytest.raises(mu.Refused, match="exists"):
        mu.merge(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery"), str(out), ctl, n_recovery=6, host_prefix=HP)


def test_verify_refuses_a_promoted_or_edited_union(pinned, tmp_path):
    ctl = pinned["controls"]
    out = tmp_path / "u"
    doc, rec = mu.merge(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery"), str(out), ctl, n_recovery=6, host_prefix=HP)
    u = json.load(open(out / "union.json"))
    u["completion_status"] = "complete"
    u["unresolved_identities"] = [["lB", "fx"]] if not u["unresolved_identities"] else u["unresolved_identities"]
    json.dump(u, open(out / "union.json", "w"), indent=1, sort_keys=True)
    with pytest.raises(mu.Refused):
        mu.verify(str(pinned["base"] / "parent"), str(pinned["base"] / "recovery"), str(out), ctl, n_recovery=6, host_prefix=HP)


def _aud(d, pinned):
    return ar.audit(str(d / "recovery2"), pinned["sub"], host_prefix=HP, n_expected=6, profile=ar.RECOVERY)


def _failed(r):
    return {c["id"] for c in r["checks"] if not c["passed"]}


def _edit_reqs(d, fn):
    q = json.load(open(d / "recovery2" / "requests.json"))
    fn(q)
    json.dump(q, open(d / "recovery2" / "requests.json", "w"))


def _idx(q):
    return [x for x in q if x["url"].endswith("/c.tbi.gz")]


def test_recovery_audit_clean_and_tampered(pinned, tmp_path):
    assert _failed(_aud(pinned["base"], pinned)) == set(), _aud(pinned["base"], pinned)
    cases = {
        "secret header": lambda q: q[0].__setitem__("headers", dict(q[0]["headers"], **{"Set-Cookie": "x"})),
        "schedule not honoured": lambda q: _idx(q)[1].__setitem__("t_clock", _idx(q)[0]["t_clock"] + 1),
        "wrong wait recorded": lambda q: _idx(q)[1].__setitem__("wait_before_s", 5),
        "fourth index attempt": lambda q: q.insert(q.index(_idx(q)[2]) + 1, dict(_idx(q)[2], attempt=4)),
        "timing field missing": lambda q: q[0].pop("elapsed_s"),
    }
    for label, fn in cases.items():
        d = tmp_path / label.replace(" ", "_")
        d.mkdir()
        shutil.copytree(pinned["base"], d / "b")
        _edit_reqs(d / "b", fn)
        r = ar.audit(str(d / "b" / "recovery2"), pinned["sub"], host_prefix=HP, n_expected=6, profile=ar.RECOVERY)
        assert "C6_budget" in _failed(r), (label, _failed(r))


def test_recovery_packet_matches_its_manifest_and_preflights(tmp_path):
    import tarfile
    from engineering.reg_proxy import pack
    base = os.path.join(ROOT, "artifacts", "reg-proxy", "recovery-packet")
    pk = json.load(open(os.path.join(base, "packet.json")))
    arc = open(os.path.join(base, "packet.tar.gz"), "rb").read()
    assert hashlib.sha256(arc).hexdigest() == pk["archive"]["sha256"] and len(arc) == pk["archive"]["bytes"]
    assert [m["path"] for m in pk["members"]] == pack.RECOVERY_MEMBERS and pk["contract_sha256"] == CONTRACT_SHA
    d = tmp_path / "x"
    d.mkdir()
    with tarfile.open(os.path.join(base, "packet.tar.gz")) as tf:
        tf.extractall(d, filter="data")
    for m in pk["members"]:
        assert hashlib.sha256((d / m["path"]).read_bytes()).hexdigest() == m["sha256"]
    p = subprocess.run([sys.executable, "-m", "engineering.reg_proxy.recovery", "--preflight"], cwd=d, capture_output=True, text=True, timeout=300)
    r = json.loads(p.stdout)
    assert p.returncode == 0 and all(c["passed"] for k in r.values() for c in k["controls"])
    assert len(r["v1_controls"]["controls"]) == 30 and len(r["recovery_controls"]["controls"]) == 11
