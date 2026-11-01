"""Step 2b: OpenFold2 (Nebius Scientific AI MCP) on unmodified zebrafish UniProt sequences.

Computed structure hypotheses, not observations: single-sequence dummy MSA, no
template, no membrane/oligomer/ligand context. Idempotency key derives from the
sequence hash; an accepted operation is polled, never resubmitted with a new key.
Credentials stay inside the gpuops NebiusMCP client (header only).
"""
import hashlib, json, sys, time
from pathlib import Path
sys.path.insert(0, "/data/worktrees/delphi-evolve/gpuops")
sys.path.insert(0, str(Path(__file__).parent))
from calls import OUT, ROOT, record, utc
from scientific_services.nebius_mcp import NebiusMCP
from scientific_services.common import redact as gredact

TARGETS = [("fgf10a", "Q8AY90"), ("hoxd13a", "Q90472"), ("shha", "Q92008"), ("kcnk5b", "Q6PFU3")]
D = OUT / "openfold2"; D.mkdir(parents=True, exist_ok=True)


def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, k)
            if r is not None: return r


c = NebiusMCP(); c.initialize()
for gene, acc in TARGETS:
    ud = json.load(open(OUT / f"uniprot/{gene}.json"))
    ent = next(e for e in ud["results"] if e["primaryAccession"] == acc)
    seq = ent["sequence"]["value"]; sh = hashlib.sha256(seq.encode()).hexdigest()
    idem = f"frontier-claude-{gene}-openfold2-{sh[:20]}"
    args = {"input_id": f"danio-{gene}-{acc}-{sh[:8]}", "sequence": seq, "selected_models": [1], "relax_prediction": False,
            "idempotency_key": idem, "wait_seconds": 30, "output_prefix": f"frontier/claude-{gene}-openfold2"}
    rec = {"tool": "infer_openfold2_native", "gene": gene, "uniprot": acc, "sequence_length": len(seq), "sequence_sha256": sh,
           "idempotency_key": idem, "submitted_utc": utc(), "polls": [], "evidence_kind": "predicted",
           "epistemic_status": "computed structure hypothesis (OpenFold2, dummy MSA); not observed, not function"}
    op = None
    try:
        res = c.call_tool("infer_openfold2_native", args); pay = c.tool_payload(res)
        rec["submit_isError"] = res.get("isError"); op = find(pay, "operation_id") or (find(pay, "operation") or {}).get("id")
        rec["submit_payload"] = gredact(pay)
    except Exception as e:
        rec["submit_exception"] = f"{type(e).__name__}: {str(e)[:300]}"
        op = find(getattr(e, "payload", None) or {}, "operation_id")
    rec["operation_id"] = op; status = None; t0 = time.time()
    while op and time.time() - t0 < 420:
        try:
            st = c.tool_payload(c.call_tool("get_operation", {"operation_id": op}))
        except Exception as e:
            rec["polls"].append({"t": utc(), "exc": str(e)[:150]}); time.sleep(10); continue
        status = find(st, "status") or find(st, "state"); rec["polls"].append({"t": utc(), "status": status})
        if isinstance(status, str) and status.upper() in {"SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED"}: break
        time.sleep(12)
    rec["final_status"] = status
    if isinstance(status, str) and status.upper() == "SUCCEEDED":
        out = c.tool_payload(c.call_tool("get_operation_result", {"operation_id": op}))
        art = out["result"]["artifact"]
        pay = c.tool_payload(c.call_tool("download_scientific_artifact", {"artifact_id": art["artifact_id"]}))
        url = next(v for v in pay.values() if isinstance(v, str) and v.startswith("http")) if any(isinstance(v, str) and v.startswith("http") for v in pay.values()) else None
        if url is None:
            def walk(o):
                if isinstance(o, dict):
                    for v in o.values():
                        r = walk(v)
                        if r: return r
                elif isinstance(o, str) and o.startswith("http"): return o
            url = walk(pay)
        import urllib.request
        data = urllib.request.urlopen(urllib.request.Request(url), timeout=120).read()
        assert hashlib.sha256(data).hexdigest() == art["sha256"], "artifact sha mismatch"
        rec["result_artifact"] = {"artifact_id": art["artifact_id"], "sha256": art["sha256"], "size_bytes": art["size_bytes"], "url_persisted": False}
        s = json.loads(data)["structures_in_ranked_order"][0]
        pdb = s["structure"]; pl = s["plddt"]
        (D / f"{gene}_{acc}_rank1.pdb").write_text(pdb)
        ca = sum(1 for l in pdb.splitlines() if l.startswith("ATOM") and l[12:16].strip() == "CA")
        rec["metrics"] = {"ranking_confidence": s.get("confidence"), "mean_plddt": sum(pl) / len(pl), "n_plddt_ge_70": sum(x >= 70 for x in pl),
                          "ptm": s.get("ptm"), "ca_residues_in_pdb": ca, "inference_seconds": s.get("inference_seconds"),
                          "pdb_sha256": hashlib.sha256(pdb.encode()).hexdigest(), "length_matches_input": ca == len(seq)}
        rec["result_keys"] = sorted(s.keys())
    rec["finished_utc"] = utc()
    (D / f"{gene}_{acc}_receipt.json").write_text(json.dumps(gredact(rec), indent=1, sort_keys=True) + "\n")
    record({"service": "nebius-openfold2", "label": f"infer:{gene}:{acc}", "http_status": None, "operation_status": status, "t_utc": utc(),
            "saved": str((D / f"{gene}_{acc}_receipt.json").relative_to(ROOT)), "evidence_kind": "predicted"})
