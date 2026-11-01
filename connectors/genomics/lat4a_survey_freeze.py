"""Freeze the lat4a survey packet from a git commit: a deterministic source bundle (small enough for GCE instance metadata) and PACKET.json.

  python -m connectors.genomics.lat4a_survey_freeze COMMIT OUTDIR

The bundle is built from the blobs at COMMIT (not the working tree), with fixed times and ownership and an unnamed gzip header, so the same commit always gives the same bytes.
PACKET.json is written to OUTDIR; commit it afterwards (it names COMMIT, so it cannot be part of the bundle it describes).
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE_FILES = [
    "connectors/genomics/__init__.py",
    "connectors/genomics/lat4a_survey.py",
    "connectors/genomics/lat4a_survey_job.py",
    "data/genomics/artifacts/ensembl_protein_ENSDARP00000120945.fasta",
    "data/genomics/artifacts/ensembl_protein_ENSDARP00000156564.fasta",
    "data/genomics/lat4a_survey/accessions.json",
    "data/genomics/lat4a_survey/predictions.json",
    "data/genomics/lat4a_survey/queries.faa",
    "data/genomics/lat4a_survey/queries_shuffled.faa",
    "data/genomics/lat4a_survey/validation_slice_zebrafish_chr15_28360000_28420000.fa",
    "data/genomics/lat4a_survey/validation_slice_zebrafish_chr10_24365000_24400000.fa",
    "data/genomics/lat4a_survey/validation_slice_result.json",
    "data/genomics/lat4a_survey/validation_slice_chr10_result.json",
]
BOOTSTRAP = "data/genomics/lat4a_survey/bootstrap.sh"
METADATA_VALUE_LIMIT = 256 * 1024  # GCE: 256 KiB per instance metadata value


def blob(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
        capture_output=True,
        check=True,
    ).stdout


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build_bundle(commit: str) -> tuple[bytes, dict]:
    blobs = {p: blob(commit, p) for p in BUNDLE_FILES}
    inputs = "".join(f"{sha(b)}  {p}\n" for p, b in sorted(blobs.items())).encode()
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for name, data in [("inputs.sha256", inputs)] + sorted(blobs.items()):
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime, ti.mode, ti.uid, ti.gid, ti.uname, ti.gname = (
                len(data),
                0,
                0o644,
                0,
                0,
                "",
                "",
            )
            tar.addfile(ti, io.BytesIO(data))
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", mtime=0, filename="") as gz:
        gz.write(raw.getvalue())
    return out.getvalue(), {p: sha(b) for p, b in blobs.items()}


def main(commit: str, outdir: str) -> dict:
    full = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", commit],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    b1, hashes = build_bundle(full)
    b2, _ = build_bundle(full)
    assert b1 == b2, "the bundle must be deterministic"
    b64 = base64.b64encode(b1)
    assert len(b64) < METADATA_VALUE_LIMIT, (
        f"bundle is {len(b64)} bytes base64; the metadata value limit is {METADATA_VALUE_LIMIT}"
    )
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "lat4a-survey-bundle.tar.gz").write_bytes(b1)
    boot = blob(full, BOOTSTRAP)
    (out / "bootstrap.sh").write_bytes(boot)
    (out / "bootstrap.sh").chmod(0o755)
    pk = json.loads(
        (ROOT / "data/genomics/lat4a_survey/PACKET.template.json").read_text()
    )
    pk["frozen_source"] = {
        "repo": "kganjam/delphi-frontier (private)",
        "branch": "work/genomics",
        "commit": full,
        "bundle": {
            "file": "lat4a-survey-bundle.tar.gz",
            "sha256": sha(b1),
            "bytes": len(b1),
            "base64_bytes": len(b64),
            "metadata_attribute": "lat4a-bundle-b64",
            "metadata_value_limit_bytes": METADATA_VALUE_LIMIT,
            "deterministic": "built twice from the commit's blobs and compared",
            "contents": hashes,
        },
        "bootstrap": {
            "file": "bootstrap.sh",
            "sha256": sha(boot),
            "env_required": "BUNDLE_SHA256=<bundle sha256 above>",
            "smoke_test": "SELFCHECK_ONLY=1 verifies the environment and the byte-for-byte self-check and stops before any genome download",
        },
    }
    pk["inputs"] = hashes
    (out / "PACKET.json").write_text(json.dumps(pk, indent=1, sort_keys=True))
    return pk["frozen_source"]


if __name__ == "__main__":
    r = main(sys.argv[1], sys.argv[2])
    print(
        r["commit"][:12],
        r["bundle"]["sha256"],
        r["bundle"]["bytes"],
        "bytes gz,",
        r["bundle"]["base64_bytes"],
        "base64",
    )
