#!/usr/bin/env python3
"""Audit the genomic span of each best hit: how much of it is assembly gap (N), and how much of the
span is accounted for by the single largest intron in miniprot's CIGAR.

Why: a best hit spanning hundreds of kilobases can be a real gene with large introns, or it can be
miniprot chaining across duplicated or gap-separated fragments. The two look identical in a summary
table. This script does not decide between them; it reports the numbers that distinguish a plausible
large-intron gene from a suspicious chain, so the reader can discount the row.

Columns:
  span_bp        t_end - t_start of the best hit
  n_frac         fraction of N bases in that window of the assembly
  max_intron_bp  largest single intron in the CIGAR (miniprot 'N'/'U'/'V' operators)
  intron_frac    max_intron_bp / span_bp
  fs, st         frameshift and in-frame stop counts reported by miniprot (fs:i, st:i tags)

Run: python3 audit_long_spans.py GENOME.fna PAF[,PAF...] OUT_JSON OUT_MD
"""
import json
import pathlib
import re
import sys

GENOME = pathlib.Path(sys.argv[1])
PAFS = [pathlib.Path(x) for x in sys.argv[2].split(",")]
OUT_JSON, OUT_MD = pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4])

best = {}
for paf in PAFS:
    for line in paf.read_text().splitlines():
        f = line.split("\t")
        tags = {x.split(":")[0]: x.split(":")[2] for x in f[12:]}
        asv = int(tags.get("AS", 0))
        q = f[0]
        if q not in best or asv > best[q]["AS"]:
            best[q] = {"query": q, "scaffold": f[5], "t_start": int(f[7]), "t_end": int(f[8]),
                       "AS": asv, "identity": round(int(f[9]) / int(f[10]), 3),
                       "coverage": round((int(f[3]) - int(f[2])) / int(f[1]), 3),
                       "fs": int(tags.get("fs", 0)), "st": int(tags.get("st", 0)),
                       "cg": tags.get("cg", ""), "paf": paf.name}

wanted = {}
for q, h in best.items():
    wanted.setdefault(h["scaffold"], []).append(q)

# single pass over the assembly, collecting only the needed windows
seqs = {}
name, buf = None, []
with open(GENOME) as fh:
    for line in fh:
        if line.startswith(">"):
            if name in wanted:
                seqs[name] = "".join(buf)
            name = line[1:].split()[0]
            buf = []
        elif name in wanted:
            buf.append(line.strip())
if name in wanted:
    seqs[name] = "".join(buf)

rows = []
for q, h in sorted(best.items(), key=lambda kv: -(kv[1]["t_end"] - kv[1]["t_start"])):
    span = h["t_end"] - h["t_start"]
    win = seqs.get(h["scaffold"], "")[h["t_start"]:h["t_end"]].upper()
    n_frac = round(win.count("N") / len(win), 4) if win else None
    introns = [int(m.group(1)) for m in re.finditer(r"(\d+)[NUV]", h["cg"])]
    mx = max(introns) if introns else 0
    rows.append({"query": q, "scaffold": h["scaffold"], "t_start": h["t_start"], "t_end": h["t_end"],
                 "span_bp": span, "window_bases_read": len(win), "n_frac": n_frac,
                 "max_intron_bp": mx, "intron_frac": round(mx / span, 3) if span else None,
                 "n_introns": len(introns), "identity": h["identity"], "coverage": h["coverage"],
                 "frameshifts": h["fs"], "inframe_stops": h["st"], "paf": h["paf"]})

doc = {
    "scope": ("Per-best-hit span audit of a protein-to-genome alignment. It does not decide whether a "
              "hit is a real gene; it reports gap content, largest intron and frameshift/stop counts so "
              "a long span can be discounted. No orthology, expression or function is claimed."),
    "genome": GENOME.name,
    "rows": rows,
}
OUT_JSON.write_text(json.dumps(doc, indent=1) + "\n")

md = ["# Span audit of best hits", "", "**Scope.** " + doc["scope"], "",
      "| query | scaffold | span bp | N frac | largest intron bp | intron/span | introns | id | cov | fs | stops |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for r in rows:
    md.append(f"| {r['query']} | {r['scaffold']} | {r['span_bp']:,} | {r['n_frac']} | "
              f"{r['max_intron_bp']:,} | {r['intron_frac']} | {r['n_introns']} | {r['identity']} | "
              f"{r['coverage']} | {r['frameshifts']} | {r['inframe_stops']} |")
OUT_MD.write_text("\n".join(md) + "\n")
for r in rows[:12]:
    print(r["query"], r["span_bp"], "n_frac", r["n_frac"], "max_intron", r["max_intron_bp"],
          "fs", r["frameshifts"], "st", r["inframe_stops"])
