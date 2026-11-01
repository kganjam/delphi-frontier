"""Builds the deterministic self-contained packet under artifacts/rd-multiic/packet/. Computes no outcome and never opens the test-seed manifest:
infra supplies its path and sha256 as arguments, which only go into PACKET.json's argv. Without them the packet is marked pending-manifest."""
import argparse, gzip, hashlib, io, json, tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = ["engineering/__init__.py", "engineering/rd_multiic/__init__.py", "engineering/rd_multiic/multiic.py", "engineering/rd_multiic/job.sh",
         "engineering/rd_multiic/protocol.json", "engineering/rd_multiic/CLARIFICATION_1.md", "engineering/rd_inverse/__init__.py", "engineering/rd_inverse/design.py", "engineering/rd_inverse/protocol.json",
         "engineering/rd_diffusion/rd_ddpm.py", "engineering/rd_diffusion/config.json", "engineering/rd_numerics/__init__.py", "engineering/rd_numerics/audit.py"]
OUT = ROOT / "artifacts/rd-multiic/packet"
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest-path"); ap.add_argument("--manifest-sha256"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0, compresslevel=9) as gz, tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for f in sorted(FILES):
            data = (ROOT / f).read_bytes(); ti = tarfile.TarInfo(f"rd-multiic/{f}")
            ti.size, ti.mtime, ti.uid, ti.gid, ti.uname, ti.gname = len(data), 0, 0, 0, "", ""
            ti.mode = 0o755 if f.endswith(".sh") else 0o644
            tar.addfile(ti, io.BytesIO(data))
    arc = buf.getvalue(); (OUT / "rd-multiic-source.tgz").write_bytes(arc)
    proto = json.loads((ROOT / "engineering/rd_multiic/protocol.json").read_text())
    pending = not (a.manifest_path and a.manifest_sha256)
    packet = {"schema": "frontier.rd-multiic.packet/1", "status": "PENDING_MANIFEST: not admissible until infra's sealed manifest path and sha256 are filled in" if pending else "ready",
              "archive": {"name": "rd-multiic-source.tgz", "sha256": sha(arc), "bytes": len(arc)}, "files": {f: sha((ROOT / f).read_bytes()) for f in sorted(FILES)},
              "protocol_sha256": sha((ROOT / "engineering/rd_multiic/protocol.json").read_bytes()), "image": proto["bounds"]["image"],
              "manifest": {"path": a.manifest_path, "sha256": a.manifest_sha256, "note": "infra-generated; never opened by this harness; the job opens it only after barrier.json"},
              "preflight": {"cmd": "tar -xzf rd-multiic-source.tgz && PREFLIGHT=1 bash rd-multiic/engineering/rd_multiic/job.sh", "no_gpu_needed": True},
              "argv": "tar -xzf rd-multiic-source.tgz && OUT=out MANIFEST=<manifest path> MANIFEST_SHA256=<sha256> bash rd-multiic/engineering/rd_multiic/job.sh",
              "env": {"OUT": "out", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "network": "none needed", "credentials": "none"},
              "pins": proto["sources"]["pins"],
              "limits": {"gpus": 1, "hard_cap_s": 1800, "soft_deadline_s": 1500, "max_output_mib_compressed": 48, "host_ram": "< 8 GiB"},
              "requires": "CUDA; float64; TF32 flags set false and recorded AFTER setting; the job refuses on CPU.",
              "expected_outputs": ["control.json", "reference.json", "reference_fields.npz", "training_traces.json", "training_round_NN.json (x8)", "training_round_NN.npz (x8)", "selections.json", "barrier.json",
                                   "test_fields.npz", "controls.json", "endpoints.json", "sparse_controls.json", "sparse_fields.npz", "traces_partial.json", "receipt.json"],
              "estimates_unmeasured": "runtime under about 800 s (basis: the 355.13 s original run); a discarded tau=2 full-plan CPU smoke wrote about 24 MB compressed (not representative of tau=200 fields)",
              "claim_limits": "synthetic numerical model only; 5 reused targets; compute-allocation comparison, not a pure loss effect; no identifiability, no biology"}
    (OUT / "PACKET.json").write_text(json.dumps(packet, indent=1, sort_keys=True) + "\n")
    print(packet["status"], packet["archive"])


if __name__ == "__main__":
    main()
