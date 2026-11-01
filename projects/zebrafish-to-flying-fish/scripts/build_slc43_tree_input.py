#!/usr/bin/env python3
"""Build the SLC43 (LAT3/LAT4) family tree input, mirroring the KCNH census that settled kcnh2.

Why: the flying-fish phylogenomic study names two loci, `kcnh2a` and `lat4a`. The first is now
settled (absent from the Beloniform lineage, `data/tree6/MANIFEST.md`). The second is still an open
Problem record in this project — `zf2ff-problem-lat4a-identifier` — because the papers say "lat4a"
while UniProt offers zebrafish `slc43a2a` (a 153 aa FRAGMENT entry) and `slc43a2b` (592 aa,
full-length "L-type amino acid transporter 4"). Mapping the whole family and placing every locus on
one tree turns the unanswerable naming question into an answerable one: which SLC43 loci does this
assembly carry, and which zebrafish paralog is each closest to?

Overlapping hits on the same scaffold are merged into one locus, so a locus is a genomic region, not
a query. Medaka proteins are included as Beloniformes context and are a labelled PROXY.

Run: python3 build_slc43_tree_input.py CENSUS_PAF REFS_FAA OUT_FAA OUT_LEDGER
"""
import collections
import hashlib
import json
import pathlib
import re
import sys

PAF, REFS, OUT_FA, OUT_LED = (pathlib.Path(x) for x in sys.argv[1:5])
OUT_FA.parent.mkdir(parents=True, exist_ok=True)

cur, per, meta = None, collections.defaultdict(list), {}
for line in PAF.read_text().splitlines():
    if line.startswith("##STA"):
        per[cur].append(line.split("\t", 1)[1].strip().replace("*", ""))
    elif not line.startswith("##"):
        f = line.split("\t")
        cur = (f[5], int(f[7]), int(f[8]))
        tags = {x.split(":")[0]: x.split(":")[2] for x in f[12:]}
        a = int(tags.get("AS", 0))
        m = meta.get(cur)
        if m is None or a > m["AS"]:
            meta[cur] = {"AS": a, "query": f[0],
                         "coverage": round((int(f[3]) - int(f[2])) / int(f[1]), 3),
                         "identity": round(int(f[9]) / int(f[10]), 3)}

byscaf = collections.defaultdict(list)
for (sc, s, e) in per:
    byscaf[sc].append((s, e))
merged = {}
for sc, iv in byscaf.items():
    iv.sort()
    cs, ce = iv[0]
    out = []
    for s, e in iv[1:]:
        if s <= ce:
            ce = max(ce, e)
        else:
            out.append((cs, ce))
            cs, ce = s, e
    out.append((cs, ce))
    merged[sc] = out

loci = []
for sc, ivs in merged.items():
    for ms, me in ivs:
        prots, best = [], None
        for (s2, st, en), ps in per.items():
            if s2 == sc and not (en <= ms or st >= me):
                prots += ps
                m = meta[(s2, st, en)]
                if best is None or m["AS"] > best["AS"]:
                    best = dict(m, start=st, end=en)
        if prots:
            loci.append({"scaffold": sc, "start": ms, "end": me,
                         "protein": max(prots, key=len), "best": best})
loci.sort(key=lambda L: -len(L["protein"]))

refs, cur = [], None
for line in REFS.read_text().splitlines():
    if line.startswith(">"):
        cur = line[1:]
        refs.append([cur, ""])
    else:
        refs[-1][1] += line

recs, led = [], []
for i, L in enumerate(loci, 1):
    short = re.sub(r"JAGFBZ0100|\.1$", lambda m: "HS" if m.group(0).startswith("JAG") else "", L["scaffold"])
    name = f"HSPEC_slc43locus{i:02d}_{short}_len{len(L['protein'])}"
    recs.append((name, L["protein"]))
    led.append({"name": name, "scaffold": L["scaffold"], "start": L["start"], "end": L["end"],
                "top_query": L["best"]["query"], "top_AS": L["best"]["AS"],
                "coverage": L["best"]["coverage"], "identity": L["best"]["identity"],
                "protein_len": len(L["protein"]),
                "sha256": hashlib.sha256(L["protein"].encode()).hexdigest()})

out = [(n, s) for n, s in refs] + recs
OUT_FA.write_text("".join(f">{n}\n{s}\n" for n, s in out))
blob = OUT_FA.read_bytes()
doc = {
    "scope": ("Family-wide SLC43 census of GCA_018398805.1 placed with the zebrafish family and two "
              "medaka proteins. Medaka is a labelled PROXY. A gene tree places sequences; it does not "
              "prove orthology and is not evidence of expression or function."),
    "question": ("Which SLC43 loci does the flying-fish assembly carry, and which zebrafish paralog is "
                 "each closest to? This is the answerable form of the open Problem "
                 "zf2ff-problem-lat4a-identifier."),
    "prior_signal_worth_checking": ("Neither medaka nor Takifugu has an annotated slc43a2a in Ensembl, "
                                    "and the zebrafish slc43a2a UniProt entry is a 153 aa fragment, so "
                                    "the 'lat4a' symbol may carry the same naming problem kcnh2a did."),
    "search": "miniprot 0.18-r281 -N 10 --outs=0.5 --trans, 6 zebrafish SLC43 queries, 5 whole-scaffold chunks",
    "n_merged_loci": len(loci), "n_sequences": len(out), "fasta_bytes": len(blob),
    "fasta_sha256": hashlib.sha256(blob).hexdigest(), "loci": led,
}
OUT_LED.write_text(json.dumps(doc, indent=1) + "\n")
print(f"{len(loci)} merged SLC43 loci; {len(out)} sequences, {len(blob)} bytes, sha256 {doc['fasta_sha256']}")
for e in led:
    print(f"  {e['name']:42s} top_query={e['top_query']:22s} cov={e['coverage']} id={e['identity']}")
