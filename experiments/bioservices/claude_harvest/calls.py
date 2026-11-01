"""Recorded public-API calls for the 2026-11-01 harvest.

Every call appends one row to a call ledger: service, verbatim request, HTTP
status (or exception), UTC time, byte count, SHA-256 of the saved body and the
saved path. Bodies are saved verbatim. Credentials are read only for header use
and never written; ``redact`` is applied to the ledger and to saved text.
"""
from __future__ import annotations
import hashlib, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/bioservices/claude-20261101"
LEDGER = OUT / "call_ledger.jsonl"
UA = "delphi-frontier-bioservices/0.2 (public-data hackathon harvest; claude worker)"
_SECRETS: set[str] = set()


def load_secret(env_file: str, key: str) -> str:
    for line in (Path.home() / ".config/morphoswarm" / env_file).read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            if k.strip() == key:
                v = v.strip().strip("\"'")
                _SECRETS.add(v)
                return v
    raise KeyError(key)


def redact(s: str) -> str:
    for v in _SECRETS:
        s = s.replace(v, "[REDACTED]")
    s = re.sub(r"\bAIza[0-9A-Za-z_\-]{20,}", "[REDACTED]", s)
    return re.sub(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}", "Bearer [REDACTED]", s)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def record(row: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as fh:
        fh.write(redact(json.dumps(row, sort_keys=True)) + "\n")


def call(service: str, label: str, url: str, *, headers=None, data=None, method=None,
         save: str | None = None, timeout: int = 60, note: str = "") -> tuple[int | None, bytes]:
    hdr = {"User-Agent": UA, **(headers or {})}
    req = urllib.request.Request(url, headers=hdr, data=data, method=method)
    status, body, err = None, b"", None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read()
    except Exception as e:  # recorded, not hidden
        err = f"{type(e).__name__}: {e}"
    path = None
    if save and body:
        p = OUT / save
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(redact(body.decode("utf-8", "replace")))
        path = str(p.relative_to(ROOT))
    record({"service": service, "label": label, "request_url": redact(url.split("key=")[0]),
            "method": method or "GET", "http_status": status, "error": err, "t_utc": utc(),
            "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest() if body else None,
            "saved": path, "note": note, "evidence_kind": "source_retrieval"})
    time.sleep(0.4)
    return status, body
