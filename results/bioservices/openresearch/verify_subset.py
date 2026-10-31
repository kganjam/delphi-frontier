"""Replayable check: the committed 256-variant subset IS what the frozen rule selects.

Deterministic and standard-library only, so a replay either reproduces the output
hash exactly or the code changed. No network, no randomness, no environment
dependence beyond the hash function.

The claim under test, from the frozen protocol:
    subset = first 256 matched variants sorted by (sha256(f"{salt}|{mutant}"), mutant)
"""
import csv, hashlib, json

SALT = "delphi-frontier/kir21-esm2-assay-agreement/v1"
SIZE = 256

def key(m): return hashlib.sha256(f"{SALT}|{m}".encode()).hexdigest()

matched = [r["mutant"] for r in csv.DictReader(open("full_matched.csv"))]
committed = [r["mutant"] for r in csv.DictReader(open("subset_256.csv"))]
selected = sorted(matched, key=lambda m: (key(m), m))[:SIZE]

out = {
    "n_matched": len(matched),
    "n_committed_subset": len(committed),
    "n_selected_by_rule": len(selected),
    "rule_reproduces_committed_subset": sorted(selected) == sorted(committed),
    "selected_sha256": hashlib.sha256("\n".join(sorted(selected)).encode()).hexdigest(),
    "committed_sha256": hashlib.sha256("\n".join(sorted(committed)).encode()).hexdigest(),
}
out["verdict"] = "REPRODUCED" if out["rule_reproduces_committed_subset"] else "MISMATCH"
text = json.dumps(out, indent=2, sort_keys=True)
open("results.json", "w").write(text + "\n")
print(text)
print("results_sha256", hashlib.sha256((text + "\n").encode()).hexdigest())
