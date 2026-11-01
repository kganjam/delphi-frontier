#!/usr/bin/env python3
"""Merge the two miniprot rounds, run three internal checks, and emit one table.

Checks (all computed, all cheap, all falsifiable):
 1. CONTROLS: every shuffled negative control must have no hit; the actb1 positive control must
    align at high identity. Printed as pass/fail, not assumed.
 2. REPRODUCIBILITY: msxb was mapped in both rounds with separate miniprot invocations. If the
    two best hits differ in scaffold or interval, the runs are not reproducible and the whole
    table is suspect.
 3. PARALOG AMBIGUITY: best hits of different query proteins that land on overlapping intervals
    cannot be treated as distinct loci. This is a limit of best-hit protein-to-genome alignment,
    not a finding about the genome.

Run: python3 merge_and_check_hits.py ROUND1.json,ROUND2.json[,...] OUT_JSON OUT_MD
"""
import json
import pathlib
import sys

ROUNDS = [json.load(open(x)) for x in sys.argv[1].split(",")]
OUT_JSON, OUT_MD = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
r2 = ROUNDS[-1]

merged = {}
for i, blk in enumerate(ROUNDS):
    rnd = f"round{i + 1}"
    why = {q["gene"]: q.get("why") for q in blk["queries"]}
    acc = {q["gene"]: q["uniprot"] for q in blk["queries"]}
    qlen = {q["gene"]: q["len"] for q in blk["queries"]}
    for g, hits in blk["hits"].items():
        merged.setdefault(g, []).append({"round": rnd, "uniprot": acc.get(g), "query_len": qlen.get(g),
                                         "why": why.get(g), "best": hits[0], "n_hits": len(hits)})
    for g in blk["no_hit"]:
        merged.setdefault(g, []).append({"round": rnd, "uniprot": acc.get(g), "query_len": qlen.get(g),
                                         "why": why.get(g), "best": None, "n_hits": 0})

checks = {"controls": [], "reproducibility": [], "paralog_ambiguity": []}

for g, recs in merged.items():
    if "NEGATIVE_CONTROL" in g:
        for r in recs:
            ok = r["best"] is None
            checks["controls"].append({"query": g, "round": r["round"], "expectation": "no hit",
                                       "observed": "no hit" if ok else r["best"], "pass": ok})
    if "POSITIVE_CONTROL" in g:
        for r in recs:
            ok = bool(r["best"]) and r["best"]["aa_identity"] >= 0.95 and r["best"]["coverage"] >= 0.95
            checks["controls"].append({"query": g, "round": r["round"],
                                       "expectation": "coverage >= 0.95 and aa_identity >= 0.95",
                                       "observed": r["best"], "pass": ok})

for g, recs in merged.items():
    if len(recs) > 1 and all(r["best"] for r in recs):
        a, b = recs[0]["best"], recs[1]["best"]
        same = (a["scaffold"] == b["scaffold"] and abs(a["t_start"] - b["t_start"]) <= 100
                and abs(a["t_end"] - b["t_end"]) <= 100)
        checks["reproducibility"].append({"query": g, "rounds": [r["round"] for r in recs],
                                          "a": a, "b": b, "same_locus_within_100bp": same})

flat = [(g, r["best"]) for g, recs in merged.items() for r in recs if r["best"]]
seen = set()
for i, (g1, h1) in enumerate(flat):
    for g2, h2 in flat[i + 1:]:
        if g1 == g2 or h1["scaffold"] != h2["scaffold"]:
            continue
        lo, hi = max(h1["t_start"], h2["t_start"]), min(h1["t_end"], h2["t_end"])
        if hi <= lo:
            continue
        key = tuple(sorted((g1, g2)))
        if key in seen:
            continue
        seen.add(key)
        checks["paralog_ambiguity"].append({
            "queries": list(key), "scaffold": h1["scaffold"], "overlap_bp": hi - lo,
            "intervals": [[h1["t_start"], h1["t_end"]], [h2["t_start"], h2["t_end"]]],
            "consequence": "These two query proteins cannot be assigned to distinct loci from "
                           "best-hit protein-to-genome alignment alone."})

summary = {
    "genome": r2["genome"],
    "genome_fasta_sha256": r2.get("genome_fasta_sha256"),
    "tool_versions": {f"round{i + 1}": b.get("tool_version", "0.18-r281 (see data/miniprot.version.txt)")
                      for i, b in enumerate(ROUNDS)},
    "scope": "Protein-to-genome alignment only. Not an annotation, not an ortholog assignment, not "
             "expression, not function. aa_identity = PAF column 10 (number of residue matches) / "
             "column 11 (alignment block length), both as miniprot reports them for the aligned "
             "block; it is not computed over the whole query. The number of ALTERNATIVE hits per "
             "query is not comparable to an unchunked run: -N5 and --outs=0.6 were applied per "
             "chunk, so secondary-hit counts can exceed 5 and are chunking artefacts. Best hits "
             "are unaffected because no scaffold was split.",
    "distinct_query_proteins": len([g for g in merged if "CONTROL" not in g]),
    "controls": len([g for g in merged if "CONTROL" in g]),
    "all_non_control_queries_have_a_hit": all(
        any(r["best"] for r in recs) for g, recs in merged.items() if "CONTROL" not in g),
    "checks": checks,
    "loci": merged,
}
OUT_JSON.write_text(json.dumps(summary, indent=1) + "\n")

rows = sorted(((g, r) for g, recs in merged.items() for r in recs if r["best"]),
              key=lambda x: -x[1]["best"]["miniprot_score_AS"])
md = ["# Candidate loci detected in GCA_018398805.1 (Hirundichthys speculiger)", "",
      f"Tool: miniprot {r2.get('tool_version', '0.18-r281')} · assembly FASTA sha256 "
      f"`{summary['genome_fasta_sha256']}`", "",
      "**Scope.** " + summary["scope"], "",
      "| zebrafish query | UniProt | round | scaffold | interval | cov | aa id | AS | hits |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for g, r in rows:
    h = r["best"]
    md.append(f"| {g} | {r['uniprot'] or '-'} | {r['round']} | {h['scaffold']} | "
              f"{h['t_start']}–{h['t_end']} | {h['coverage']} | {h['aa_identity']} | "
              f"{h['miniprot_score_AS']} | {r['n_hits']} |")
md += ["", "## Controls", ""]
for c in checks["controls"]:
    md.append(f"- `{c['query']}` ({c['round']}): expectation {c['expectation']} → "
              f"**{'PASS' if c['pass'] else 'FAIL'}**")
md += ["", "## Reproducibility across the two runs", ""]
for c in checks["reproducibility"]:
    md.append(f"- `{c['query']}` mapped in {', '.join(c['rounds'])}: same locus within 100 bp = "
              f"**{c['same_locus_within_100bp']}** ({c['a']['scaffold']} "
              f"{c['a']['t_start']}–{c['a']['t_end']} vs {c['b']['scaffold']} "
              f"{c['b']['t_start']}–{c['b']['t_end']})")
md += ["", "## Paralog ambiguity (a limit of the method, not a finding)", ""]
if not checks["paralog_ambiguity"]:
    md.append("- No two query proteins' best hits overlap.")
for c in checks["paralog_ambiguity"]:
    md.append(f"- `{c['queries'][0]}` and `{c['queries'][1]}` best-hit the same region of "
              f"{c['scaffold']} (overlap {c['overlap_bp']} bp). {c['consequence']}")
OUT_MD.write_text("\n".join(md) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k not in ("loci", "checks")}, indent=1))
print("controls:", [(c["query"], c["pass"]) for c in checks["controls"]])
print("reproducibility:", [(c["query"], c["same_locus_within_100bp"]) for c in checks["reproducibility"]])
print("ambiguous pairs:", [c["queries"] for c in checks["paralog_ambiguity"]])
