"""One Gemini cross-review of each simulation's assumptions (claude-mol, 2026-11-01).
Key is read from ~/.env at call time and sent only in the x-goog-api-key header; never printed or stored.
Usage: python gemini_review.py   (reads assumptions.json beside this file, writes results/mol-sims/claude-20261101/gemini_review.json)
"""
import hashlib, json, re, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "results/mol-sims/claude-20261101"
import sys
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-3.8-flash"
ITEMS = sys.argv[2] if len(sys.argv) > 2 else "assumptions.json"   # a second round can point at another file
TAG = Path(ITEMS).stem


def key():
    m = re.search(r"^(?:export\s+)?GEMINI_API_KEY=(.*)$", (Path.home() / ".env").read_text(), re.M)
    return m.group(1).strip().strip("'\"")


def main():
    items = json.loads((HERE / ITEMS).read_text())
    prompt = ("You are a critical reviewer of computational systems-biology models. For each model below, given its "
              "stated assumptions and results, list (a) assumptions you think are unjustified or risky for the stated use, "
              "(b) any internal inconsistency in the reported results, (c) one additional control you would require. "
              "Be concise (under 150 words per model), critical, no flattery. Do not invent literature citations.\n\n"
              + json.dumps(items, indent=1))
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    req = urllib.request.Request(url, data=body, headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            status, raw = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read()
    resp = json.loads(raw)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"gemini_review_{TAG}_{MODEL}.json" if TAG != "assumptions" else f"gemini_review_{MODEL}.json").write_text(json.dumps({
        "model": MODEL, "items_file": ITEMS, "http_status": status, "seconds": round(time.time() - t0, 1), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "usage": resp.get("usageMetadata"), "response": resp.get("candidates", resp), "evidence_kind": "model review: a lead to check, not evidence"}, indent=1))
    print("http", status)


if __name__ == "__main__":
    main()
