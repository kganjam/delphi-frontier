"""Structure predictions with MSA on the Nebius Scientific AI MCP (claude-mol, 2026-11-01).

Why: the bioservices OpenFold2 monomers (dummy MSA, full-length precursors) had mean pLDDT 41-56 and no
confident stretch for MD. Here each target is trimmed to its folded domain(s), given a PDB70 MMseqs2 A3M
(msa_search_native), and predicted with Boltz-2 (boltz2_predict_native) as monomer or complex.

Targets (zebrafish UniProt sequences, trims recorded in the receipt):
  fgf_complex : Fgf10a FGF core (Q8AY90 58-201) + Fgfr2 IIIb D2-D3 (F1RBT3 150-360; IIIb chosen by alignment
                to human P21802-3 vs -1, see results/mol-sims/claude-20261101/inputs/)
  shhN        : Shha signalling domain (Q92008 24-197, mature N-terminal fragment ending at the GCF autoprocessing site)
  kcnk5b_dimer: Kcnk5b transmembrane core (Q6PFU3 1-265) x2 (K2P channels are dimers)

Every prediction is COMPUTED, not observed. Idempotency keys derive from input hashes; an accepted
operation is polled, never resubmitted with a new key. At most 2 operations outstanding.
Usage: python nebius_struct.py {msa|fold} [target ...]
"""
import hashlib, json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, "/data/worktrees/delphi-evolve/gpuops")
from scientific_services.nebius_mcp import NebiusMCP  # key read from ~/.config/morphoswarm/nebius.env, header only
from scientific_services.common import redact

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/mol-sims/claude-20261101/structures"
INP = ROOT / "results/mol-sims/claude-20261101/inputs"
BS = ROOT / "results/bioservices/claude-20261101/uniprot"


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def uni(g, a):
    d = json.loads((BS / f"{g}.json").read_text())
    return next(x for x in d["results"] if x["primaryAccession"] == a)["sequence"]["value"]


def fasta(a):
    return "".join(l.strip() for l in (INP / f"{a}.fasta").read_text().splitlines()[1:])


CHAINS = {
    "fgf10a_core": (uni("fgf10a", "Q8AY90")[57:201], "Q8AY90 58-201"),
    "fgfr2b_d2d3": (fasta("F1RBT3")[149:360], "F1RBT3 150-360"),
    "fgfr2c_d2d3": (fasta("Q8JG38")[149:362], "Q8JG38 150-362 (IIIc isoform; +2 aa insertion vs IIIb in the alternative exon)"),
    "shhN": (uni("shha", "Q92008")[23:197], "Q92008 24-197"),
    "kcnk5b_core": (uni("kcnk5b", "Q6PFU3")[0:265], "Q6PFU3 1-265"),
}
TARGETS = {"fgf_complex": ["fgf10a_core", "fgfr2b_d2d3"], "fgf_vs_fgfr2c_negctrl": ["fgf10a_core", "fgfr2c_d2d3"], "shhN": ["shhN"], "kcnk5b_dimer": ["kcnk5b_core", "kcnk5b_core"]}


def find(o, k):
    if isinstance(o, dict):
        if k in o:
            return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, k)
            if r is not None:
                return r


def poll(c, op, rec, budget=3000):
    t0, status = time.time(), None
    while time.time() - t0 < budget:
        try:
            st = c.tool_payload(c.call_tool("get_operation", {"operation_id": op}))
        except Exception as e:
            rec["polls"].append({"t": utc(), "exc": str(e)[:200]}); time.sleep(15); continue
        status = find(st, "status") or find(st, "state")
        if not rec["polls"] or rec["polls"][-1].get("status") != status:
            rec["polls"].append({"t": utc(), "status": status})
        if isinstance(status, str) and status.upper() in {"SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED"}:
            if status.upper() != "SUCCEEDED":
                rec["terminal_detail"] = redact(st)
            break
        time.sleep(15)
    return status


def fetch_result(c, op):
    """Return (result_payload, list of (artifact_meta, bytes)) with sha256 verified."""
    res = c.tool_payload(c.call_tool("get_operation_result", {"operation_id": op}))
    arts = []
    cand = []

    def walk(o):
        if isinstance(o, dict):
            if "artifact_id" in o and "sha256" in o:
                cand.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(res)
    seen = set()
    for a in cand:
        if a["artifact_id"] in seen:
            continue
        seen.add(a["artifact_id"])
        pay = c.tool_payload(c.call_tool("download_scientific_artifact", {"artifact_id": a["artifact_id"]}))
        url = None

        def wu(o):
            nonlocal url
            if url:
                return
            if isinstance(o, dict):
                for v in o.values():
                    wu(v)
            elif isinstance(o, list):
                for v in o:
                    wu(v)
            elif isinstance(o, str) and o.startswith("http"):
                url = o
        wu(pay)
        data = urllib.request.urlopen(urllib.request.Request(url), timeout=300).read()
        assert sha(data) == a["sha256"], f"sha mismatch {a['artifact_id']}"
        arts.append(({k: a.get(k) for k in ("artifact_id", "sha256", "size_bytes", "media_type", "path", "name")}, data))
    return res, arts


def run_op(c, tool, args, rec):
    res = c.call_tool(tool, args)
    pay = c.tool_payload(res)
    rec["submit_isError"] = res.get("isError")
    rec["submit_payload"] = redact(pay)
    op = find(pay, "operation_id") or ((pay or {}).get("operation") or {}).get("id")
    rec["operation_id"] = op
    if not op:
        rec["final_status"] = "NOT_ACCEPTED"
        return None
    rec["final_status"] = poll(c, op, rec)
    return op


def msa(c, name):
    seq, src = CHAINS[name]
    d = OUT / "msa"; d.mkdir(parents=True, exist_ok=True)
    if (d / f"{name}.a3m").exists():
        print(name, "a3m exists, skip"); return
    rec = {"tool": "msa_search_native", "chain": name, "source": src, "sequence": seq, "sequence_sha256": sha(seq),
           "submitted_utc": utc(), "polls": [], "database": "pdb70_220313", "evidence_kind": "computed"}
    args = {"sequence": seq, "databases": ["pdb70_220313"], "output_alignment_formats": ["a3m"], "max_msa_sequences": 2000,
            "idempotency_key": f"frontier-claude-mol-msa-{name}-{sha(seq)[:20]}", "wait_seconds": 30,
            "output_prefix": f"frontier/claude-mol/msa-{name}"}
    op = run_op(c, "msa_search_native", args, rec)
    if op and str(rec["final_status"]).upper() == "SUCCEEDED":
        res, arts = fetch_result(c, op)
        rec["result_summary"] = redact(res)
        a3m = None
        for meta, data in arts:
            txt = data.decode("utf-8", "replace")
            if txt.lstrip().startswith(">"):
                a3m = txt
            elif txt.lstrip().startswith("{"):
                j = json.loads(txt)
                a3m = a3m or find(j, "a3m") or find(j, "alignment")
                if isinstance(a3m, dict):
                    a3m = find(a3m, "alignment") or find(a3m, "content")
        rec["artifacts"] = [m for m, _ in arts]
        if a3m:
            (d / f"{name}.a3m").write_text(a3m)
            rec["a3m_sha256"] = sha(a3m); rec["a3m_n_seqs"] = a3m.count(">")
    rec["finished_utc"] = utc()
    (d / f"{name}_receipt.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(name, rec["final_status"], rec.get("a3m_n_seqs"))


def fold(c, target):
    d = OUT / target; d.mkdir(parents=True, exist_ok=True)
    if (d / "receipt.json").exists() and json.loads((d / "receipt.json").read_text()).get("final_status") == "SUCCEEDED":
        print(target, "done, skip"); return
    polys, chain_ids = [], "ABCDEFGH"
    for i, ch in enumerate(TARGETS[target]):
        seq, _ = CHAINS[ch]
        a3m = (OUT / "msa" / f"{ch}.a3m").read_text()
        polys.append({"id": chain_ids[i], "molecule_type": "protein", "sequence": seq,
                      "msa": {"msa_search": {"a3m": {"alignment": a3m, "format": "a3m"}}}})
    key = sha(json.dumps(polys, sort_keys=True))
    rec = {"tool": "boltz2_predict_native", "target": target, "chains": {chain_ids[i]: {"name": ch, "source": CHAINS[ch][1], "sequence_sha256": sha(CHAINS[ch][0]),
           "a3m_sha256": sha((OUT / 'msa' / f'{ch}.a3m').read_text())} for i, ch in enumerate(TARGETS[target])},
           "params": {"diffusion_samples": 3, "recycling_steps": 3, "sampling_steps": 200}, "seed_note": "runtime accepts no seed; nondeterministic",
           "submitted_utc": utc(), "polls": [], "evidence_kind": "predicted",
           "epistemic_status": "computed structure hypothesis (Boltz-2 + PDB70 MSA); not observed, not function"}
    args = {"polymers": polys, **rec["params"], "output_format": "mmcif", "wait_seconds": 30,
            "idempotency_key": f"frontier-claude-mol-boltz2-{target}-{key[:20]}", "output_prefix": f"frontier/claude-mol/boltz2-{target}"}
    rec["idempotency_key"] = args["idempotency_key"]
    op = run_op(c, "boltz2_predict_native", args, rec)
    if op and str(rec["final_status"]).upper() == "SUCCEEDED":
        res, arts = fetch_result(c, op)
        rec["result_summary"] = redact(res) if len(json.dumps(res)) < 200000 else {"keys": list(res)}
        rec["artifacts"] = [m for m, _ in arts]
        for i, (meta, data) in enumerate(arts):
            nm = (meta.get("name") or meta.get("path") or f"artifact_{i}").split("/")[-1]
            (d / nm).write_bytes(data)
    rec["finished_utc"] = utc()
    (d / "receipt.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(target, rec["final_status"])


def fold_of3(c, target):
    """OpenFold3 (fixed seed 42, one sample) for targets Boltz-2 rejected (homodimer MSA identity check)."""
    d = OUT / f"{target}_openfold3"; d.mkdir(parents=True, exist_ok=True)
    if (d / "receipt.json").exists() and json.loads((d / "receipt.json").read_text()).get("final_status") == "SUCCEEDED":
        print(target, "done, skip"); return
    mols = []
    for i, ch in enumerate(TARGETS[target]):
        seq, _ = CHAINS[ch]
        a3m = (OUT / "msa" / f"{ch}.a3m").read_text()
        mols.append({"type": "protein", "id": "ABCDEFGH"[i], "sequence": seq, "msa": {"main": {"a3m": {"alignment": a3m, "format": "a3m"}}}})
    key = sha(json.dumps(mols, sort_keys=True))
    rec = {"tool": "infer_openfold3_native", "target": target, "seed": 42, "seed_note": "runtime-fixed seed 42, one sample",
           "chains": {"ABCDEFGH"[i]: {"name": ch, "source": CHAINS[ch][1], "sequence_sha256": sha(CHAINS[ch][0])} for i, ch in enumerate(TARGETS[target])},
           "submitted_utc": utc(), "polls": [], "evidence_kind": "predicted",
           "epistemic_status": "computed structure hypothesis (OpenFold3 preview2 + PDB70 MSA); not observed, not function"}
    args = {"request_id": f"claude-mol-{target.replace('_', '-')}-{key[:8]}", "inputs": [{"input_id": target.replace("_", "-"), "molecules": mols, "output_format": "cif"}], "wait_seconds": 30,
            "idempotency_key": f"frontier-claude-mol-of3-{target}-{key[:20]}", "output_prefix": f"frontier/claude-mol/of3-{target}"}
    op = run_op(c, "infer_openfold3_native", args, rec)
    if op and str(rec["final_status"]).upper() == "SUCCEEDED":
        res, arts = fetch_result(c, op)
        rec["result_summary"] = redact(res) if len(json.dumps(res)) < 200000 else {"keys": list(res)}
        rec["artifacts"] = [m for m, _ in arts]
        for i, (meta, data) in enumerate(arts):
            (d / f"artifact_{i}").write_bytes(data)
    rec["finished_utc"] = utc()
    (d / "receipt.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    print(target, rec["final_status"])


def main():
    stage, names = sys.argv[1], sys.argv[2:]
    c = NebiusMCP(); c.initialize()
    if stage == "schema":
        print(json.dumps(c.tool_payload(c.call_tool("get_model_schema", {"model_id": names[0], "summary_only": False}))[:1] if False else
              c.tool_payload(c.call_tool("get_model_schema", {"model_id": names[0]})), indent=1)[:6000])
        return
    for n in names or (CHAINS if stage == "msa" else TARGETS):
        {"msa": msa, "fold": fold, "of3": fold_of3}[stage](c, n)


if __name__ == "__main__":
    main()
