#!/usr/bin/env python3
"""Submit up to 8 proteins to Boltz2 in ONE workbench operation.

MEASURED, not assumed: the workbench enforces a small in-flight cap PER KEY. Four concurrent native
submits all returned `429 ADMISSION_LIMIT_REACHED` with `admission: not-submitted`, so the cap
cannot be raised from the client side and a 429 creates no operation (retrying is free).

What CAN be raised is the work per slot. `boltz2_predict_native` takes `polymers` with maxItems 8
and `diffusion_samples` up to 8, so one operation can carry eight chains instead of one. We had been
submitting one sequence at a time and leaving that entirely unused.

The nesting is four levels deep and not obvious:
    polymers[] -> msa -> msa_search -> a3m -> {alignment, format}
"""
import json, os, ssl, sys, time, urllib.request

MCP = "https://89.169.99.188/mcp"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def key():
    for line in open(os.path.expanduser("~/.config/morphoswarm/nebius.env")):
        if line.startswith("NEBIUS_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no NEBIUS_API_KEY")


def polymer(chain_id, seq, a3m_path):
    return {"id": chain_id, "molecule_type": "protein", "sequence": seq,
            "msa": {"msa_search": {"a3m": {"alignment": open(a3m_path).read(), "format": "a3m"}}}}


def submit(polymers, samples=1, idem=None, wait=5):
    if not 1 <= len(polymers) <= 8:
        raise SystemExit(f"polymers must be 1-8, got {len(polymers)}")
    idem = idem or f"batch{len(polymers)}-{int(time.time())}"
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
        "name": "boltz2_predict_native",
        "arguments": {"polymers": polymers, "diffusion_samples": samples,
                      "idempotency_key": idem, "wait_seconds": wait}}}).encode()
    req = urllib.request.Request(MCP, data=body, headers={
        "Authorization": f"Bearer {key()}", "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"})
    try:
        raw = urllib.request.urlopen(req, context=CTX, timeout=240).read().decode()
    except Exception as e:
        return {"transport_error": type(e).__name__, "idempotency_key": idem}
    try:
        inner = json.loads(json.loads(raw)["result"]["content"][0]["text"])
    except Exception:
        return {"unparsed": raw[:400], "idempotency_key": idem}
    inner["idempotency_key"] = idem
    return inner


if __name__ == "__main__":
    D = "/data/scratch/designspaces/fish-proteins"
    B = os.path.dirname(os.path.abspath(__file__))
    targets = [("A", f"{B}/../results/fish-proteins/Q6PFU3.fasta", f"{D}/msa_kcnk5b/kcnk5b_pdb70.a3m"),
               ("B", f"{B}/../results/fish-proteins/E7F5V5.fasta", f"{D}/msa_and1/and1_pdb70.a3m"),
               ("C", f"{B}/../results/fish-proteins/A0ACM8QEN9.fasta", f"{D}/msa_and2/and2_pdb70.a3m")]
    pols = []
    for cid, fa, a3m in targets:
        if os.path.exists(fa) and os.path.exists(a3m):
            s = "".join(l.strip() for l in open(fa) if not l.startswith(">"))
            pols.append(polymer(cid, s, a3m))
    print(f"batching {len(pols)} proteins into one operation")
    r = submit(pols)
    e = r.get("error") or {}
    print(f"  key={r.get('idempotency_key')}  status={e.get('status_code')} {e.get('code')} "
          f"admission={e.get('admission')} op={e.get('operation_id')}")
    if e.get("code") == "ADMISSION_LIMIT_REACHED":
        print("  The slot is busy. admission=not-submitted means NO operation was created, "
              "so this is free to retry.")
