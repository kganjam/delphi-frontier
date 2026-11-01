"""F006 PREREG A7: for each of the team's own Nebius jobs (results/resources/hackathon-usage.json), which fields a policy comparison needs
exist anywhere in this repository? Mechanical keyword evidence only (a hit is a file that mentions the job id AND the keyword), so it
over-counts readiness (a keyword is not a verified field) and never under-counts a field written in a file that names the job.
  python3 -I experiments/f006_allocation/pool_readiness.py REPO_ROOT OUT.json"""
import collections, hashlib, json, os, re, sys

root, out_p = sys.argv[1:3]  # optional flag --specific
usage_p = os.path.join(root, "results/resources/hackathon-usage.json")
jobs = json.load(open(usage_p))["own_jobs"]
FIELDS = {  # field -> regex searched in files that mention the job id
    "ex_ante_acceptance_predicate": r"(?i)(frozen|preregister|prereg|gate|tolerance|acceptance)",
    "ex_ante_cost_declaration": r"(?i)(budget_s|timeout|RuntimeMaxSec|wall budget|budget)",
    "measured_cost_receipt": r"(?i)(container_wall_s|wall_s|seconds|started|finished|end_utc|start_utc)",
    "outcome_label": r"(?i)(PASS|FAIL|VALIDATED|NOT_VALIDATED|verdict|result)",
    "non_author_review": r"(?i)(independent review|independently reviewed|reviewed by|Codex-reviewed: yes|second reviewer)",
}
texts = {}
for dp, dn, fn in os.walk(root):
    if any(s in dp for s in ("/.git", "/node_modules", "/site/", "__pycache__")):
        continue
    for f in fn:
        if f.endswith((".json", ".md", ".jsonl", ".txt", ".log", ".csv")):
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 5_000_000:
                    continue
                texts[p] = open(p, errors="ignore").read()
            except OSError:
                pass
ids = [j["id"] for j in jobs]
nids = {p: sum(i in t for i in ids) for p, t in texts.items()}
STRICT = "--specific" in sys.argv          # variant: ignore aggregate files that name more than 3 of the jobs
rows = []
for j in jobs:
    files = [p for p, t in texts.items() if j["id"] in t and os.path.abspath(p) != os.path.abspath(usage_p) and (not STRICT or nids[p] <= 3)]
    r = {"id": j["id"], "name": j["name"], "state": j["state"], "n_files_mentioning": len(files)}
    for k, rx in FIELDS.items():
        r[k] = any(re.search(rx, texts[p]) for p in files)
    rows.append(r)
summ = {k: sum(r[k] for r in rows) for k in FIELDS}
summ["mentioned_anywhere_else"] = sum(r["n_files_mentioning"] > 0 for r in rows)
summ["all_five_fields"] = sum(all(r[k] for k in FIELDS) for r in rows)
res = {"usage_sha256": hashlib.sha256(open(usage_p, "rb").read()).hexdigest(), "n_jobs": len(jobs), "states": dict(collections.Counter(j["state"] for j in jobs)),
       "n_files_scanned": len(texts), "variant": "specific files only (<= 3 job ids per file)" if STRICT else "all files", "summary_jobs_with_field": summ, "caveat": "keyword evidence in files naming the job; an upper bound on readiness, not verified fields",
       "jobs": rows}
json.dump(res, open(out_p, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "jobs"}, indent=1))
