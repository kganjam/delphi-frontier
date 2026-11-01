"""Sample-pairing audit: controls run the code used remotely; each is also broken on purpose to prove it can fail."""
import copy
import json
import re
import subprocess

import pytest

from engineering.sample_pairing import audit, controls

GIT = "/data/worktrees/delphi-frontier/foundation/.git"
REPLAY = "1b77f81"


def test_all_controls_pass():
    r = controls.run_all()
    assert r and all(r.values()), [k for k, v in r.items() if not v]


def _mut(monkeypatch, name, fn):
    monkeypatch.setattr(audit, name, fn)
    return controls.run_all()


def test_mutation_ignoring_replicate_is_caught(monkeypatch):
    orig = audit.sample_record

    def no_rep(acc, parsed, proto):
        r = orig(acc, parsed, proto)
        r["rep"] = "1"
        r["missing"] = [m for m in r["missing"] if m != "replicate_token"]
        return r
    r = _mut(monkeypatch, "sample_record", no_rep)
    assert not r["swapped_replicate_refused"] and not r["missing_replicate_unresolved"]


def test_mutation_assembly_comparison_removed_is_caught(monkeypatch):
    orig = audit.sample_record

    def same_asm(acc, parsed, proto):
        r = orig(acc, parsed, proto)
        r["assembly"] = "danrer11"
        return r
    r = _mut(monkeypatch, "sample_record", same_asm)
    assert not r["assembly_mismatch_refused"]


def test_mutation_alias_removed_is_caught(monkeypatch):
    orig = audit.load_protocol

    def no_alias(path=audit.PROTOCOL_PATH):
        p, h = orig(path)
        p = copy.deepcopy(p)
        p["assembly_aliases"] = []
        return p, h
    r = _mut(monkeypatch, "load_protocol", no_alias)
    assert not r["alias_danRer11_GRCz11_equal"]


def test_mutation_barcode_style_pairing_is_caught(monkeypatch):
    """Pair by supplementary-file (barcode) name instead of BioSample: the control must fail."""
    orig = audit.sample_record

    def by_barcode(acc, parsed, proto):
        r = orig(acc, parsed, proto)
        files = parsed["fields"].get("Sample_supplementary_file_1", [])
        if files:
            r["biosample"], r["missing"] = files[0], []
        return r
    r = _mut(monkeypatch, "sample_record", by_barcode)
    assert not r["shared_barcode_strings_do_not_pair"]


def test_mutation_ambiguity_collapse_is_caught(monkeypatch):
    orig = audit.pair

    def first_only(records):
        seen, keep = set(), []
        for x in records:
            k = (x["biosample"], x["strategy"])
            if k not in seen:
                seen.add(k)
                keep.append(x)
        return orig(keep)
    r = _mut(monkeypatch, "pair", first_only)
    assert not r["many_to_many_ambiguous"]


def test_mutation_byte_cap_ignored_is_caught(monkeypatch):
    def nocap(acc, proto, opener=None):
        with opener.open(type("R", (), {"full_url": audit.url_for(acc, proto)})(), timeout=0) as r:
            return r.read(), r.status
    r = _mut(monkeypatch, "fetch", nocap)
    assert not r["byte_bound_refused_partial_kept"]


def test_mutation_host_check_removed_is_caught(monkeypatch):
    monkeypatch.setattr(audit, "url_for", lambda acc, proto: proto["retrieval"]["url_templates"][0].format(ACC=acc))
    r = controls.run_all()
    assert not r["host_allowlist_enforced"] and not r["non_accession_url_refused"]


def test_protocol_freezes_one_budget_and_finite_retrieval():
    p, _ = audit.load_protocol()
    assert p["budget"]["hard_runtime_s"] == 600 and "withdrawn" in p["budget_note"]
    R = p["retrieval"]
    assert R["allowed_hosts"] == ["www.ncbi.nlm.nih.gov"] and R["retries"] == 0 and R["max_requests"] == R["max_gsm"] + 1
    assert R["max_total_bytes_expanded"] <= p["budget"]["max_output_bytes"]
    assert "barcode" in p["unit_of_pairing"] and p["frozen_before_new_retrieval"] is True


def _blob(path):
    try:
        return subprocess.check_output(["git", "--git-dir", GIT, "show", f"{REPLAY}:{path}"], stderr=subprocess.DEVNULL).decode()
    except Exception:
        pytest.skip("earlier audit commit not in this clone")


def test_offline_replay_of_earlier_committed_geo_bytes():
    """Replay of bytes retrieved by the EARLIER audit (not the new retrieval): same parser and pairing code."""
    base = "artifacts/regulatory-metadata/run/raw/"
    proto, _ = audit.load_protocol()
    gsms = re.findall(r"^!Series_sample_id = (GSM\d+)", _blob(base + "GSE261907.soft.txt"), flags=re.M)
    recs = [audit.sample_record(g, audit.parse_soft(_blob(base + g + ".soft.txt")), proto) for g in gsms]
    pairs, st = audit.pair(recs)
    s = audit.summarize(recs, pairs, st)
    assert s["libraries_admitted"] == 20 == len(gsms)
    assert s["pair_status_counts"] == {"matched": 10} and s["distinct_biosamples_declared"] == 10
    assert all(p["rna"] and p["atac"] for p in pairs)
    # the same replay with one library's replicate token swapped must stop being all-matched
    bad = copy.deepcopy(recs)
    bad[0]["rep"] = "2"
    p2, _ = audit.pair(bad)
    st2 = [p["status"] for p in p2]
    # the altered library no longer agrees with its partner AND reuses the other 0 dpa sample's label: both are refused
    assert st2.count("matched") == 8 and st2.count("unresolved_conflict") == 2
    reasons = " ".join(" ".join(p["reasons"]) for p in p2 if p["status"] != "matched")
    assert "rep differs: 2 vs 1" in reasons and "label reused across BioSamples" in reasons


def test_packet_is_deterministic_and_runs_from_a_fresh_directory(tmp_path):
    import tarfile
    import sys
    from engineering.sample_pairing import pack
    try:
        pk = pack.build(out=str(tmp_path / "a"))
    except SystemExit as e:
        pytest.skip(f"uncommitted: {e}")
    pk2 = pack.build(out=str(tmp_path / "b"))
    assert pk["archive"]["sha256"] == pk2["archive"]["sha256"]
    ex = tmp_path / "x"
    ex.mkdir()
    with tarfile.open(tmp_path / "a" / "packet.tar.gz") as tf:
        tf.extractall(ex, filter="data")
    r = subprocess.run([sys.executable, "-m", "engineering.sample_pairing.audit", "--preflight"], cwd=ex, capture_output=True, text=True, env={"PYTHONPATH": str(ex), "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["protocol_sha256"] == pk["protocol_sha256"] and all(out["controls"].values())
