"""Step 1: one small probe per service. Records status; prints no secret."""
import json, subprocess, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from calls import call, load_secret, record, utc

P = "probe/"
call("uniprot", "probe", "https://rest.uniprot.org/uniprotkb/Q0KIZ7.json", save=P + "uniprot.json")
call("ncbi-eutils", "probe", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Exocoetidae&retmax=5&retmode=json", save=P + "pubmed.json")
call("europepmc", "probe", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=Exocoetidae&format=json&pageSize=2", save=P + "europepmc.json")
call("ensembl", "probe", "https://rest.ensembl.org/info/ping?content-type=application/json", save=P + "ensembl.json")
call("biomodels", "probe", "https://www.ebi.ac.uk/biomodels/search?query=zebrafish&format=json&numResults=2", save=P + "biomodels.json")
call("zfin", "probe-download-host", "https://zfin.org/downloads", save=P + "zfin.html")
key = load_secret("gemini.env", "GEMINI_API_KEY")
body = json.dumps({"contents": [{"parts": [{"text": "Reply with the single word OK."}]}]}).encode()
call("gemini", "probe", "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent",
     headers={"x-goog-api-key": key, "Content-Type": "application/json"}, data=body, method="POST", save=P + "gemini.json")
# Nebius Scientific AI MCP: initialize only
import os
url = load_secret("nebius.env", "NEBIUS_WORKBENCH_URL").rstrip("/")
tok = load_secret("nebius.env", "NEBIUS_API_KEY")
init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "claude-probe", "version": "0"}}}).encode()
import ssl
call("nebius-mcp", "probe-initialize", url + ("" if url.endswith("/mcp") else "/mcp"),
     headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
     data=init, method="POST", save=P + "nebius_mcp.txt")
for label, cmd in [("gcloud-project", ["gcloud", "projects", "describe", "scienceclaw26bos-3016", "--format=value(lifecycleState)"]),
                   ("gcloud-auth", ["gcloud", "auth", "list", "--format=value(account)"]),
                   ("brev-cli", ["bash", "-c", "command -v brev; env | grep -ci '^BREV\\|NVIDIA_API\\|NGC_API' "])]:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    record({"service": "gcp" if "gcloud" in label else "nvidia-brev", "label": label, "exit": r.returncode,
            "stdout": r.stdout.strip()[:200] if "auth" not in label else "(account omitted)", "stderr": r.stderr.strip()[:200], "t_utc": utc()})
