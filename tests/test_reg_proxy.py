"""GSE261907 validated-control window count: same-parser controls, mutation checks, frozen protocol, packet."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "engineering", "reg_proxy")
PROTOCOL_SHA = "7a2ec7be0132fe77140ad3647e229400affe74698f53d4b059954e35dc723dc5"  # frozen at 306a603 before code; deliberately restated


def run_controls(cwd):
    p = subprocess.run([sys.executable, "-m", "engineering.reg_proxy.controls_synth"], cwd=cwd, capture_output=True, text=True, timeout=240)
    try:
        return p.returncode, json.loads(p.stdout)["controls"]
    except ValueError:
        return p.returncode, []


def test_controls_pass_on_the_committed_code():
    rc, ctl = run_controls(ROOT)
    failed = [c for c in ctl if not c["passed"]]
    assert rc == 0 and len(ctl) == 29 and not failed, failed


AMENDMENT_SHA = "048e4745f78462a43bf6790a8d7d8a528f4b9c81cb10c0cfbd41d037e5657637"  # frozen at c713181 before the reader repair; deliberately restated


def test_amendment_bytes_are_the_frozen_ones():
    assert hashlib.sha256(open(os.path.join(PKG, "transport_amendment.json"), "rb").read()).hexdigest() == AMENDMENT_SHA


def test_protocol_bytes_are_the_frozen_ones():
    assert hashlib.sha256(open(os.path.join(PKG, "protocol.json"), "rb").read()).hexdigest() == PROTOCOL_SHA


MUTATIONS = [
    ("window_count.py", "if e > w0:", "if e >= w0:", "half-open start"),
    ("window_count.py", "if s >= w1:", "if s > w1:", "half-open end"),
    ("window_count.py", 'if r.status != 206:', 'if False:', "range status"),
    ("window_count.py", 'if r.headers.get("Content-Range") != f"bytes {start}-{end}/{total}":', "if False:", "content-range"),
    ("window_count.py", "if s < prev:", "if False:", "sortedness"),
    ("window_count.py", 'if out["compressed_bytes_read"] >= cap:', "if False:", "window cap"),
    ("window_count.py", 'if a["chrom"] == b["chrom"] and a["start0"] < b["end0"] and b["start0"] < a["end0"]:', "if False:", "overlap"),
    ("window_count.py", "if len(data) != isize or zlib.crc32(data) != crc:", "if False:", "crc"),
    ("window_count.py", "if coff >= total:", "if False:", "index/file mismatch"),
    ("window_count.py", 'if len(body) != expected:', "if False:", "short read"),
    ("window_count.py", "self.budget.precheck(expected)  # cap refusals are final: never retried", "pass", "caps checked before send"),
    ("window_count.py", "self.budget.charge(len(c))", "pass", "bytes read are charged"),
    ("window_count.py", "self.budget.charge(len(e.partial))", "pass", "partial IncompleteRead bytes are charged"),
    ("window_count.py", "self._bounded_read(r, expected + 1, rec)", "self._bounded_read(r, expected + 1000000, rec)", "read bound"),
    ("window_count.py", 'if r.status != 206:', 'if False:', "status checked before body"),
    ("window_count.py", 'error = type(e).__name__', 'error = None', "unexpected error status"),
    ("window_count.py", 'present == set(expected) else "partial_data")', 'present == set(expected) or True else "partial_data")', "complete needs all usable"),
    ("window_count.py", 'if self.lib_bytes + n > self.b["per_library_compressed_max_bytes"]:', "if False:", "library cap"),
]


@pytest.mark.parametrize("fname,old,new,label", MUTATIONS, ids=[m[3] for m in MUTATIONS])
def test_mutated_code_fails_a_control(tmp_path, fname, old, new, label):
    dst = tmp_path / "m"
    (dst / "engineering").mkdir(parents=True)
    shutil.copy(ROOT + "/engineering/__init__.py", dst / "engineering" / "__init__.py")
    shutil.copytree(PKG, dst / "engineering" / "reg_proxy", ignore=shutil.ignore_patterns("__pycache__"))
    f = dst / "engineering" / "reg_proxy" / fname
    src = f.read_text()
    assert src.count(old) == 1, f"mutation target for {label!r} not found exactly once"
    f.write_text(src.replace(old, new))
    rc, ctl = run_controls(dst)
    assert rc != 0 or any(not c["passed"] for c in ctl), f"mutation {label!r} survived all controls"
    assert ctl or rc != 0


def test_packet_is_built_from_head_and_preflights(tmp_path):
    import tarfile
    from engineering.reg_proxy import pack
    pk = json.load(open(os.path.join(ROOT, "artifacts", "reg-proxy", "packet.json")))
    arc = open(os.path.join(ROOT, "artifacts", "reg-proxy", "packet.tar.gz"), "rb").read()
    assert hashlib.sha256(arc).hexdigest() == pk["archive"]["sha256"] and len(arc) == pk["archive"]["bytes"]
    d = tmp_path / "x"
    d.mkdir()
    with tarfile.open(os.path.join(ROOT, "artifacts", "reg-proxy", "packet.tar.gz")) as tf:
        tf.extractall(d, filter="data")
    for m in pk["members"]:
        assert hashlib.sha256((d / m["path"]).read_bytes()).hexdigest() == m["sha256"]
    assert [m["path"] for m in pk["members"]] == pack.MEMBERS
    rc, ctl = run_controls(d)
    assert rc == 0 and all(c["passed"] for c in ctl)
