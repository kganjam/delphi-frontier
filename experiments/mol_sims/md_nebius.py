"""s6: explicit-solvent OpenMM MD of the Boltz-2 ShhN model on the Nebius Scientific AI MCP (claude-mol, 2026-11-01).

Start: structures/shhN/model_0.cif (Boltz-2 + PDB70 MSA, mean pLDDT 85; OpenFold2 dummy-MSA was 40 on the same
residues). Converted to heavy-atom PDB; the hosted OpenMM App adds hydrogens at pH 7, solvates (TIP3P, 1.0 nm,
0.15 M NaCl), minimises, equilibrates NVT then NPT, and runs production at 301 K (28 C).
Known omission: Hedgehog-N binds Zn2+ and Ca2+; the apo prediction has no ions, so metal-site loops may move more
than in the holo protein. SIMULATED, not observed.
Usage: python md_nebius.py submit | poll
"""
import gzip, hashlib, io, json, sys, tarfile, time, urllib.request
from pathlib import Path

sys.path.insert(0, "/data/worktrees/delphi-evolve/gpuops")
from scientific_services.nebius_mcp import NebiusMCP
from scientific_services.common import redact

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "results/mol-sims/claude-20261101/md_shhN"
CIF = ROOT / "results/mol-sims/claude-20261101/structures/shhN/model_0.cif"
PROD_STEPS = 5_000_000      # 10 ns at 2 fs
SEED = 20261101


def sha(b):
    return hashlib.sha256(b).hexdigest()


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def pdb_bytes():
    from openmm.app import PDBxFile, PDBFile
    x = PDBxFile(str(CIF))
    buf = io.StringIO()
    PDBFile.writeFile(x.topology, x.positions, buf, keepIds=False)
    return buf.getvalue().encode()


def bundle(pdb):
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode="w") as tf:
        ti = tarfile.TarInfo("shhN_model0.pdb"); ti.size = len(pdb); ti.mtime = 0; ti.uid = ti.gid = 0; ti.uname = ti.gname = ""
        tf.addfile(ti, io.BytesIO(pdb))
    return gzip.compress(bio.getvalue(), mtime=0)


def upload(c, data, media, key, rec):
    up = c.tool_payload(c.call_tool("begin_scientific_artifact_upload", {"model_id": "openmm", "sha256": sha(data), "size_bytes": len(data),
                                                                         "media_type": media, "idempotency_key": key}))
    rec.setdefault("uploads", []).append({"begin": redact(up)})
    h = up.get("handle") or {}
    url = h.get("url") or up.get("direct_upload_url") or up.get("upload_url")
    if url:
        req = urllib.request.Request(url, data=data, method=h.get("method", "PUT"),
                                     headers={"Content-Type": media, **{k: v for k, v in (h.get("headers") or {}).items() if isinstance(v, str)}})
        with urllib.request.urlopen(req, timeout=120) as r:
            rec["uploads"][-1]["put_status"] = r.status
    uid = up.get("upload_id") or (up.get("upload") or {}).get("upload_id")
    fin = c.tool_payload(c.call_tool("finalize_scientific_artifact_upload", {"upload_id": uid}))
    rec["uploads"][-1]["finalize"] = redact(fin)
    ref = fin.get("artifact") or fin
    return {k: ref[k] for k in ("artifact_id", "sha256", "size_bytes", "media_type") if k in ref}


def submit():
    D.mkdir(parents=True, exist_ok=True)
    pdb = pdb_bytes(); (D / "start_heavy.pdb").write_bytes(pdb)
    tgz = bundle(pdb)
    rec = {"sim": "s6", "start_cif_sha256": sha(CIF.read_bytes()), "start_pdb_sha256": sha(pdb), "bundle_sha256": sha(tgz), "submitted_utc": utc(), "polls": []}
    c = NebiusMCP(); c.initialize()
    art = upload(c, tgz, "application/gzip", f"frontier-claude-mol-md-bundle-{sha(tgz)[:20]}", rec)
    manifest = {"schema": "fs2-serve.nebius.ai/scientific-artifact-manifest/v1",
                "artifacts": [{"role": "openmm-inputs", "name": "openmm-inputs", **art, "compression": "none"}]}
    mb = json.dumps(manifest, sort_keys=True).encode()
    rec["manifest"] = manifest
    mart = upload(c, mb, "application/vnd.fs2.scientific-manifest+json", f"frontier-claude-mol-md-manifest-{sha(mb)[:20]}", rec)
    T = 301.0
    params = {"schema": "fs2-serve.nebius.ai/openmm-workflow-request/v1", "backend": "cuda", "precision": "mixed", "random_seed": SEED,
              "max_wall_seconds": 7200, "output_prefix": "frontier/claude-mol/openmm-shhN",
              "jobs": [{"id": "shhn-apo", "system": {"format": "pdb", "coordinates": "shhN_model0.pdb",
                                                      "forcefields": ["amber14-all.xml", "amber14/tip3pfb.xml"], "add_hydrogens": True, "ph": 7.0,
                                                      "solvent": {"model": "tip3p", "padding_nm": 1.0, "ionic_strength_molar": 0.15, "neutralize": True},
                                                      "nonbonded_method": "PME", "nonbonded_cutoff_nm": 1.0, "constraints": "HBonds"},
                        "steps": [{"id": "min", "kind": "minimize", "tolerance_kj_mol_nm": 10.0},
                                  {"id": "nvt", "kind": "equilibrate", "steps": 50000, "temperature_k": T, "report_interval": 5000},
                                  {"id": "npt", "kind": "equilibrate", "steps": 100000, "temperature_k": T, "pressure_bar": 1.0, "report_interval": 5000},
                                  {"id": "prod", "kind": "production", "steps": PROD_STEPS, "temperature_k": T, "pressure_bar": 1.0,
                                   "report_interval": 5000, "checkpoint_interval_steps": 500000}]}]}
    args = {"request": {"input_manifest": {**mart, "compression": "none"}, "parameters": params,
                        "client_context": {"display_name": "claude-mol ShhN apo 10 ns"}},
            "idempotency_key": f"frontier-claude-mol-openmm-shhN-{sha(json.dumps(params, sort_keys=True).encode() + tgz)[:20]}"}
    rec["submit_arguments"] = redact(args)
    res = c.call_tool("submit_openmm_workflow", args)
    pay = c.tool_payload(res)
    rec["submit_isError"] = res.get("isError"); rec["submit_payload"] = redact(pay)
    s = json.dumps(pay)
    import re
    m = re.search(r'"(?:operation_id|id)": "(op-[0-9a-f]+)"', s)
    rec["operation_id"] = m.group(1) if m else None
    (D / "receipt.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(rec["operation_id"], rec["submit_isError"], s[:1500])


if __name__ == "__main__":
    {"submit": submit}[sys.argv[1]]()
