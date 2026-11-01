#!/usr/bin/env python3
"""Build a source index from the verbatim Europe PMC responses in data/epmc/.

Reads only what the saved response bodies contain. Read-level of every row is at most
`abstract`: nothing here is a full-text read, and no row asserts that the paper supports
any statement in the plan -- only that the record exists and what its own abstract says.

Run: python3 build_source_index.py DIR[,DIR...] OUT_JSON OUT_MD
"""
import hashlib
import json
import pathlib
import sys

EPMC_DIRS = [pathlib.Path(x) for x in sys.argv[1].split(",")]
OUT_JSON, OUT_MD = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])

rows, index = [], {}
files = []
ledger = {}
for d in EPMC_DIRS:
    for r in json.load(open(d / "ledger.json")):
        ledger[f"{d.name}/{r['name']}"] = r
    files += [p for p in sorted(d.glob("*.json")) if p.name != "ledger.json"]
for p in files:
    raw = p.read_bytes()
    name = f"{p.parent.name}/{p.stem}"
    body = json.loads(raw)
    led = ledger.get(name, {})
    sha = hashlib.sha256(raw).hexdigest()
    if led.get("sha256") and led["sha256"] != sha:
        raise SystemExit(f"sha256 mismatch for {p}: ledger {led['sha256']} != file {sha}")
    hits = body.get("resultList", {}).get("result", [])
    recs = []
    for h in hits:
        abstract = h.get("abstractText")
        recs.append({
            "pmid": h.get("pmid"),
            "pmcid": h.get("pmcid"),
            "doi": h.get("doi"),
            "title": (h.get("title") or "").strip(),
            "journal": (h.get("journalInfo", {}).get("journal", {}) or {}).get("title"),
            "year": h.get("pubYear"),
            "is_open_access": h.get("isOpenAccess"),
            "license": h.get("license"),
            "has_abstract_in_response": bool(abstract),
            "abstract_chars": len(abstract) if abstract else 0,
            "read_level": "abstract" if abstract else "metadata_only",
        })
    index[name] = {
        "query": led.get("query", body.get("request", {}).get("queryString")),
        "request_url": led.get("url"),
        "response_sha256": sha,
        "retrieved_utc": led.get("utc"),
        "hit_count_reported": body.get("hitCount"),
        "records_saved": len(recs),
        "records": recs,
    }
    for r in recs:
        rows.append((name, r))

summary = {
    "source": "Europe PMC REST search, resultType=core, pageSize=8",
    "read_level_ceiling": "abstract",
    "caveat": "A row means the record exists and its abstract was saved. It does not mean the paper "
              "supports any statement in this project; support requires reading the paper.",
    "queries": len(index),
    "records_saved_total": len(rows),
    "distinct_pmids": len({r["pmid"] for _, r in rows if r["pmid"]}),
    "with_abstract": sum(1 for _, r in rows if r["has_abstract_in_response"]),
    "open_access": sum(1 for _, r in rows if r["is_open_access"] == "Y"),
    "index": index,
}
OUT_JSON.write_text(json.dumps(summary, indent=1) + "\n")

lines = ["# Source index (Europe PMC, read-level = abstract)", "",
         f"{summary['queries']} queries, {summary['records_saved_total']} saved records, "
         f"{summary['distinct_pmids']} distinct PMIDs, {summary['with_abstract']} with an abstract in the response, "
         f"{summary['open_access']} flagged open access.", "",
         "A row means: this record exists and this much of it was retrieved. It does not mean the",
         "paper supports a statement made elsewhere in this project.", ""]
for name, blk in index.items():
    lines += [f"## {name}", "",
              f"- query: `{blk['query']}`",
              f"- reported hit count: {blk['hit_count_reported']}; saved: {blk['records_saved']}",
              f"- response sha256: `{blk['response_sha256']}` retrieved {blk['retrieved_utc']}", "",
              "| PMID | year | journal | OA | read | title |", "| --- | --- | --- | --- | --- | --- |"]
    for r in blk["records"]:
        t = r["title"].replace("|", "/")
        lines.append(f"| {r['pmid'] or '-'} | {r['year'] or '-'} | {(r['journal'] or '-')[:40]} | "
                     f"{r['is_open_access'] or '-'} | {r['read_level']} | {t[:110]} |")
    lines.append("")
OUT_MD.write_text("\n".join(lines) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "index"}, indent=1))
