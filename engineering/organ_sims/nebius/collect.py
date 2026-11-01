"""Collect a finished organ-sims Nebius job: read its log, decode the ORGAN-OUT tarball, verify sha256 and bytes,
extract into the repo, and write artifacts/organ-sims/nebius/<job_name>.collect.json.

    python3 engineering/organ_sims/nebius/collect.py <job_name> <job_id>
"""
import base64, hashlib, io, json, os, re, subprocess, sys, tarfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = os.path.expanduser("~/.nebius/bin/nebius")


def main():
    name, jid = sys.argv[1], sys.argv[2]
    st = json.loads(subprocess.run([CLI, "--profile", "hackathon", "ai", "job", "get", jid, "--format", "json"], capture_output=True, text=True).stdout)
    state = st["status"]["state"]
    log = subprocess.run([CLI, "--profile", "hackathon", "ai", "job", "logs", jid], capture_output=True, text=True).stdout
    rec = {"job_name": name, "job_id": jid, "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "state": state,
           "status": st["status"], "log_bytes": len(log), "log_sha256": hashlib.sha256(log.encode()).hexdigest()}
    m = re.search(r"ORGAN-OUT-BEGIN sha256=([0-9a-f]{64}) bytes=(\d+)\n(.*?)\nORGAN-OUT-END", log, re.S)
    sci = re.search(r"ORGAN-JOB science rc=(\d+) wall_s=(\d+)", log)
    rec["science_rc"] = int(sci.group(1)) if sci else None
    rec["science_wall_s"] = int(sci.group(2)) if sci else None
    head = [l for l in log.splitlines() if l.startswith(("ORGAN-JOB", "pkgs", "Python"))][:6]
    rec["log_head"] = head
    if not m:
        rec["output"] = "no ORGAN-OUT block in log"
    else:
        lines = [l.strip() for l in m.group(3).splitlines() if re.fullmatch(r"[A-Za-z0-9+/=]+", l.strip())]
        raw = base64.b64decode("".join(lines))
        ok = hashlib.sha256(raw).hexdigest() == m.group(1) and len(raw) == int(m.group(2))
        rec["output"] = {"declared_sha256": m.group(1), "declared_bytes": int(m.group(2)), "decoded_bytes": len(raw), "sha256_match": ok}
        if ok:
            files = {}
            with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
                for mem in tf.getmembers():
                    if not mem.isfile() or mem.name.startswith("/") or ".." in mem.name or not mem.name.startswith("artifacts/organ-sims/"):
                        continue
                    b = tf.extractfile(mem).read()
                    dst = ROOT / mem.name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(b)
                    files[mem.name] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
            rec["files"] = files
            mf = [f for f in files if f.endswith("/manifest.json")]
            if mf:
                man = json.loads((ROOT / mf[0]).read_text())
                rec["manifest_checks"] = [[c["name"], bool(c["pass"])] for c in man["checks"]]
                rec["manifest_code_sha256"] = man.get("code_sha256")
                rec["manifest_git_head_at_run"] = man.get("git_head_at_run")
    out = ROOT / f"artifacts/organ-sims/nebius/{name}.collect.json"
    out.write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("state", "science_rc", "science_wall_s")}), json.dumps(rec.get("output"))[:300])


if __name__ == "__main__":
    main()
