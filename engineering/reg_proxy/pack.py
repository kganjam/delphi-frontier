"""Build the portable packet for the GSE261907 validated-control window count: deterministic tar.gz, per-member sha256/size
manifest, exact source commit, entry argv. Refuses members that differ from HEAD."""
import gzip
import hashlib
import io
import json
import os
import subprocess
import tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMBERS = ["engineering/__init__.py", "engineering/reg_proxy/__init__.py", "engineering/reg_proxy/window_count.py",
           "engineering/reg_proxy/controls_synth.py", "engineering/reg_proxy/protocol.json", "engineering/reg_proxy/controls.json",
           "engineering/reg_proxy/transport_amendment.json", "engineering/reg_proxy/transport_amendment_2.json", "engineering/reg_proxy/fixtures/GSM8153942_0dpa1_atac_fragments.tsv.gz.tbi.gz",
           "engineering/reg_proxy/fixtures/htslib_fixture.tsv.gz", "engineering/reg_proxy/fixtures/htslib_fixture.tsv.gz.tbi",
           "engineering/reg_proxy/fixtures/htslib_expected.json"]
OUT = os.path.join(ROOT, "artifacts", "reg-proxy")


def _tar(members):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz, tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for name, data in members:
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime, ti.mode, ti.uid, ti.gid, ti.uname, ti.gname = len(data), 0, 0o644, 0, 0, "", ""
            tf.addfile(ti, io.BytesIO(data))
    return buf.getvalue()


def _committed_members(names):
    commit = git("rev-parse", "HEAD")
    members = []
    for m in names:
        disk = open(os.path.join(ROOT, m), "rb").read()
        try:
            committed = git("show", f"{commit}:{m}", raw=True)
        except subprocess.CalledProcessError:
            raise SystemExit(f"{m} is not in HEAD {commit[:10]}: commit it first") from None
        if disk != committed:
            raise SystemExit(f"{m} differs from HEAD {commit[:10]}: commit it first")
        members.append((m, disk))
    return commit, members


def git(*a, raw=False):
    r = subprocess.check_output(["git", "-C", ROOT, *a], stderr=subprocess.DEVNULL)
    return r if raw else r.decode().strip()


def build(out=OUT):
    commit = git("rev-parse", "HEAD")
    members = []
    for m in MEMBERS:
        disk = open(os.path.join(ROOT, m), "rb").read()
        try:
            committed = git("show", f"{commit}:{m}", raw=True)
        except subprocess.CalledProcessError:
            raise SystemExit(f"{m} is not in HEAD {commit[:10]}: commit it first") from None
        if disk != committed:
            raise SystemExit(f"{m} differs from HEAD {commit[:10]}: commit it first")
        members.append((m, disk))
    os.makedirs(out, exist_ok=True)
    arc = _tar(members)
    open(os.path.join(out, "packet.tar.gz"), "wb").write(arc)
    d = dict(members)
    packet = {"schema": "frontier.reg-proxy.packet/1", "source_commit": commit,
              "archive": {"path": "artifacts/reg-proxy/packet.tar.gz", "sha256": hashlib.sha256(arc).hexdigest(), "bytes": len(arc)},
              "members": [{"path": n, "sha256": hashlib.sha256(x).hexdigest(), "bytes": len(x)} for n, x in members],
              "python": ">=3.10", "dependencies": "none (standard library only)",
              "extract": "into a NEW empty directory; run every command with that directory as cwd",
              "preflight_argv": ["python3", "-m", "engineering.reg_proxy.window_count", "--preflight"],
              "entry_argv": ["python3", "-m", "engineering.reg_proxy.window_count", "--run", "--out", "$COPS_OUT"],
              "contract": {"COPS_OUT": "exact fresh output directory (must not exist)", "workers": 1, "numeric_threads": 1,
                           "memory_bytes": 4294967296, "tasks_max": 128, "hard_runtime_s": 1200, "max_output_bytes": 52428800,
                           "network": "ftp.ncbi.nlm.nih.gov over https, HTTP byte ranges only; bounds in protocol.json",
                           "retries": "declared max 2 attempts per request, each logged and charged; no other retry"},
              "outputs": ["results.json", "receipt.json", "requests.json"],
              "exit_codes": {"0": "complete (330/330 usable)", "2": "stopped_on_bound", "3": "partial_data", "4": "stopped_on_error", "1": "preflight failed"},
              "amendment_sha256": hashlib.sha256(d["engineering/reg_proxy/transport_amendment.json"]).hexdigest(),
              "amendment2_sha256": hashlib.sha256(d["engineering/reg_proxy/transport_amendment_2.json"]).hexdigest(),
              "protocol_sha256": hashlib.sha256(d["engineering/reg_proxy/protocol.json"]).hexdigest(),
              "controls_sha256": hashlib.sha256(d["engineering/reg_proxy/controls.json"]).hexdigest()}
    json.dump(packet, open(os.path.join(out, "packet.json"), "w"), indent=1, sort_keys=True)
    return packet


RECOVERY_MEMBERS = ["engineering/__init__.py", "engineering/reg_proxy/__init__.py", "engineering/reg_proxy/window_count.py",
                    "engineering/reg_proxy/controls_synth.py", "engineering/reg_proxy/controls_recovery.py", "engineering/reg_proxy/recovery.py",
                    "engineering/reg_proxy/protocol.json", "engineering/reg_proxy/controls.json", "engineering/reg_proxy/transport_amendment.json",
                    "engineering/reg_proxy/transport_amendment_2.json", "engineering/reg_proxy/recovery_contract.json",
                    "engineering/reg_proxy/fixtures/GSM8153942_0dpa1_atac_fragments.tsv.gz.tbi.gz", "engineering/reg_proxy/fixtures/htslib_fixture.tsv.gz",
                    "engineering/reg_proxy/fixtures/htslib_fixture.tsv.gz.tbi", "engineering/reg_proxy/fixtures/htslib_expected.json"]
RECOVERY_OUT = os.path.join(ROOT, "artifacts", "reg-proxy", "recovery-packet")


def build_recovery(out=RECOVERY_OUT):
    """Portable packet for the single missing-only recovery run (recovery_contract.json)."""
    commit, members = _committed_members(RECOVERY_MEMBERS)
    os.makedirs(out, exist_ok=True)
    arc = _tar(members)
    open(os.path.join(out, "packet.tar.gz"), "wb").write(arc)
    d = dict(members)
    c = json.load(open(os.path.join(ROOT, "engineering/reg_proxy/recovery_contract.json")))
    packet = {"schema": "frontier.reg-proxy.recovery-packet/1", "source_commit": commit,
              "archive": {"path": "artifacts/reg-proxy/recovery-packet/packet.tar.gz", "sha256": hashlib.sha256(arc).hexdigest(), "bytes": len(arc)},
              "members": [{"path": n, "sha256": hashlib.sha256(x).hexdigest(), "bytes": len(x)} for n, x in members],
              "python": ">=3.10", "dependencies": "none (standard library only)",
              "extract": "into a NEW empty directory; run every command with that directory as cwd",
              "preflight_argv": ["python3", "-m", "engineering.reg_proxy.recovery", "--preflight"],
              "entry_argv": ["python3", "-m", "engineering.reg_proxy.recovery", "--run", "--out", "$COPS_OUT"],
              "contract": {"COPS_OUT": "exact fresh output directory (must not exist)", "workers": 1, "numeric_threads": 1, "memory_bytes": c["bounds"]["memory_bytes"],
                           "tasks_max": c["bounds"]["tasks_max"], "hard_runtime_s": c["bounds"]["runtime_hard_s"], "max_output_bytes": c["bounds"]["output_max_bytes"],
                           "requests_max": c["bounds"]["requests_max"], "charged_bytes_max": c["bounds"]["charged_bytes_max"],
                           "network": c["bounds"]["network"], "index_schedule_s": c["transport"]["index_schedule"]["wait_before_attempt_s"],
                           "scope_libraries": c["scope"]["libraries"]},
              "outputs": ["results.json", "receipt.json", "requests.json"],
              "exit_codes": {"0": "complete (165/165 usable)", "2": "stopped_on_bound", "3": "partial_data", "4": "stopped_on_error", "1": "preflight failed"},
              "contract_sha256": hashlib.sha256(d["engineering/reg_proxy/recovery_contract.json"]).hexdigest(),
              "protocol_sha256": hashlib.sha256(d["engineering/reg_proxy/protocol.json"]).hexdigest(),
              "controls_sha256": hashlib.sha256(d["engineering/reg_proxy/controls.json"]).hexdigest(),
              "parent_results_sha256": c["parent"]["results_sha256"],
              "offline_tools_not_in_packet": ["audit_return (--recovery)", "merge_union"]}
    json.dump(packet, open(os.path.join(out, "packet.json"), "w"), indent=1, sort_keys=True)
    return packet


if __name__ == "__main__":
    print(json.dumps(build_recovery() if "--recovery" in __import__("sys").argv else build(), indent=1))
