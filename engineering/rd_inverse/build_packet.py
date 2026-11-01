"""Builds the deterministic self-contained packet under artifacts/rd-inverse/packet/. No solver outcomes are computed."""
import gzip, hashlib, io, json, tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = ["engineering/__init__.py", "engineering/rd_inverse/__init__.py", "engineering/rd_inverse/design.py", "engineering/rd_inverse/job.sh",
         "engineering/rd_inverse/protocol.json", "engineering/rd_inverse/PREREG.md", "engineering/rd_diffusion/rd_ddpm.py",
         "engineering/rd_diffusion/config.json", "engineering/rd_numerics/__init__.py", "engineering/rd_numerics/audit.py"]
OUT = ROOT / "artifacts/rd-inverse/packet"
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = [f for f in FILES if (ROOT / f).exists()]
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0, compresslevel=9) as gz, tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for f in sorted(files):
            data = (ROOT / f).read_bytes(); ti = tarfile.TarInfo(f"rd-inverse/{f}")
            ti.size, ti.mtime, ti.uid, ti.gid, ti.uname, ti.gname = len(data), 0, 0, 0, "", ""
            ti.mode = 0o755 if f.endswith(".sh") else 0o644
            tar.addfile(ti, io.BytesIO(data))
    arc = buf.getvalue(); (OUT / "rd-inverse-source.tgz").write_bytes(arc)
    proto = json.loads((ROOT / "engineering/rd_inverse/protocol.json").read_text())
    packet = {"schema": "frontier.rd-inverse.packet/1", "archive": {"name": "rd-inverse-source.tgz", "sha256": sha(arc), "bytes": len(arc)},
              "files": {f: sha((ROOT / f).read_bytes()) for f in sorted(files)}, "protocol_sha256": sha((ROOT / "engineering/rd_inverse/protocol.json").read_bytes()),
              "image": proto["bounds"]["image"], "preflight": {"cmd": "tar -xzf rd-inverse-source.tgz && PREFLIGHT=1 bash rd-inverse/engineering/rd_inverse/job.sh", "no_gpu_needed": True},
              "argv": "tar -xzf rd-inverse-source.tgz && OUT=out bash rd-inverse/engineering/rd_inverse/job.sh",
              "env": {"OUT": "out", "OMP_NUM_THREADS": "unset", "network": "none needed", "credentials": "none"},
              "pins": proto["source_pins"],
              "limits": {"gpus": 1, "max_runtime_s": 900, "host_ram": "< 4 GiB", "max_output_mib_compressed": 48, "output_tarball": "out/rd_inverse_outputs.tgz"},
              "requires": "CUDA; float64; TF32 disabled; the job refuses on CPU. Image provides python3, torch, numpy.",
              "expected_outputs": ["control.json", "targets.json", "targets.npz", "traces.json", "evaluated_fields.npz", "selection.json", "validation_controls.json", "independent_checks.json", "receipt.json"],
              "claim_limits": "synthetic numerical design only, n=6, no biology, no DDPM acceleration claim"}
    (OUT / "PACKET.json").write_text(json.dumps(packet, indent=1, sort_keys=True) + "\n")
    print(packet["archive"])


if __name__ == "__main__":
    main()
