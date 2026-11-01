#!/usr/bin/env python3
"""Cross-check the Evo 2 harness's 9 flying-fish windows against this project's miniprot mapping.

The two placements are independent: claude-evo placed its windows with a CDS-only GeneWise
ortholog model, this project placed protein alignments with miniprot. Agreement makes a locus
solid by two methods; disagreement means at least one is wrong.

For each of their flying-fish windows this reports:
  - whether their scaffold (their "HS####" short name) matches the scaffold of MY best hit for
    the same gene symbol;
  - which of MY hits (over ALL query proteins, including the paralog controls) is nearest to
    their window, and the signed gap in bp;
  - whether their window lies immediately upstream of that hit on the stated strand, which is
    what an upstream-of-start-codon window should do.

The last column is the one that matters: if their window for gene X sits flush against my hit for
a DIFFERENT paralog Y, their window is labelled X but located at Y.

Also resolves their dropped hoxd13a: measures the 2 kb upstream of my hoxd13a hit for non-ACGT
characters and for running off the scaffold end, which is their stated drop reason.

Run: python3 crosscheck_evo_windows.py GENOME.fna LOCI_MERGED.json EVO_INPUT_SET.json OUT_JSON OUT_MD
"""
import json
import pathlib
import re
import sys

GENOME, LOCI, EVOSET = sys.argv[1], sys.argv[2], sys.argv[3]
OUT_JSON, OUT_MD = pathlib.Path(sys.argv[4]), pathlib.Path(sys.argv[5])

loci = json.load(open(LOCI))
evo = json.load(open(EVOSET))

# their short scaffold names are HS<4 digits>; this assembly's accessions are JAGFBZ0100<5 digits>.1
def expand(short):
    m = re.fullmatch(r"HS(\d{4})", short)
    return f"JAGFBZ0100{int(m.group(1)):05d}.1" if m else None


# every best hit of every query this project mapped, as (query, scaffold, start, end, strand)
my_hits = []
for q, recs in loci["loci"].items():
    for r in recs:
        if r["best"]:
            b = r["best"]
            my_hits.append({"query": q, "round": r["round"], "scaffold": b["scaffold"],
                            "start": b["t_start"], "end": b["t_end"], "strand": b["strand"],
                            "coverage": b["coverage"], "identity": b["aa_identity"]})

rows = []
for t in evo["targets"]:
    if not t.get("assembly", "").startswith("GCA"):
        continue
    region = t["region"]
    short, span = region.split(":")
    w_start, w_end = (int(x) for x in span.split("-"))
    scaf = expand(short)
    sym, strand = t["symbol"], t["strand"]

    same_scaffold = [h for h in my_hits if h["scaffold"] == scaf]
    # nearest hit on that scaffold by edge-to-edge distance
    def gap(h):
        if h["end"] < w_start:
            return w_start - h["end"]          # hit is before the window
        if h["start"] > w_end:
            return h["start"] - w_end          # hit is after the window
        return 0                               # overlapping

    nearest = min(same_scaffold, key=gap) if same_scaffold else None
    my_same_symbol = [h for h in my_hits if h["query"].split("_")[0] == sym]
    my_symbol_scaffolds = sorted({h["scaffold"] for h in my_same_symbol})

    flush = None
    if nearest:
        g = gap(nearest)
        # an upstream window on + strand should end where the CDS hit starts; on - strand it
        # should start where the hit ends.
        if strand == 1:
            flush = abs(w_end - nearest["start"]) <= 2
        else:
            flush = abs(w_start - nearest["end"]) <= 2

    queried_by_me = bool(my_same_symbol)
    if not queried_by_me:
        verdict = f"NOT COMPARABLE: I never queried {sym}, so I have no independent placement for it"
    elif not nearest:
        verdict = (f"DISAGREE on scaffold: I queried {sym} and my hit is on "
                   f"{', '.join(my_symbol_scaffolds)}, not on their {scaf}")
    elif nearest["query"].split("_")[0] == sym:
        verdict = ("AGREE: flush against my hit for the same gene" if flush else
                   f"same gene on the same scaffold, not flush (gap {gap(nearest)} bp)")
    else:
        other = nearest["query"].split("_")[0]
        same_family = other[:4] == sym[:4] or other.rstrip("ab") == sym.rstrip("ab")
        tag = "PARALOG MISMATCH" if same_family else "DIFFERENT GENE"
        verdict = (f"{tag}: their '{sym}' window is flush against MY '{nearest['query']}' hit"
                   if flush else
                   f"{tag}: nearest hit of mine on this scaffold is '{nearest['query']}' "
                   f"({gap(nearest)} bp away), and my own {sym} hit is on "
                   f"{', '.join(my_symbol_scaffolds)}")

    rows.append({
        "their_symbol": sym, "their_region": region, "their_strand": strand,
        "their_scaffold_expanded": scaf,
        "their_window_basis": t.get("window_basis"),
        "their_blast_best_hit": t.get("blast_best_hit"),
        "their_paralog_flag": t.get("paralog_flag"),
        "my_best_hit_scaffolds_for_this_symbol": my_symbol_scaffolds,
        "scaffold_agrees_with_my_same_symbol_hit": scaf in my_symbol_scaffolds,
        "my_nearest_hit_on_their_scaffold": None if not nearest else {
            k: nearest[k] for k in ("query", "round", "start", "end", "strand", "coverage", "identity")},
        "gap_bp": None if not nearest else gap(nearest),
        "window_is_flush_against_that_hit": flush,
        "verdict": verdict,
    })

# ---- their dropped hoxd13a: measure the stated drop reason against my hit
hox = [h for h in my_hits if h["query"] == "hoxd13a"]
hox_report = {"my_hit": hox[0] if hox else None}
if hox:
    h = hox[0]
    keep, buf = False, []
    with open(GENOME) as fh:
        for line in fh:
            if line.startswith(">"):
                if keep:
                    break
                keep = line[1:].split()[0] == h["scaffold"]
            elif keep:
                buf.append(line.strip())
    scaf_seq = "".join(buf)
    up_end = h["start"] if h["strand"] == "+" else None
    if h["strand"] == "+":
        up_start = max(0, h["start"] - 2000)
        win = scaf_seq[up_start:h["start"]]
        truncated_by_scaffold_start = h["start"] < 2000
    else:
        up_start = h["end"]
        win = scaf_seq[h["end"]:h["end"] + 2000]
        truncated_by_scaffold_start = (h["end"] + 2000) > len(scaf_seq)
    nonacgt = sum(1 for c in win.upper() if c not in "ACGT")
    hox_report.update({
        "scaffold_len": len(scaf_seq),
        "upstream_2kb_requested": 2000,
        "upstream_2kb_available": len(win),
        "non_ACGT_bases_in_window": nonacgt,
        "window_would_be_truncated": bool(truncated_by_scaffold_start),
        "their_stated_drop_reason": evo["dropped"][0]["reason"] if evo.get("dropped") else None,
        "finding": None,
    })
    if len(win) == 2000 and nonacgt == 0:
        hox_report["finding"] = ("A clean 2 kb ACGT-only window DOES exist immediately upstream of my "
                                 "hoxd13a hit on this strand. Their drop reason was 'no ortholog hit with "
                                 "a clean 2 kb ACGT-only window'; the two halves of that reason are "
                                 "separable, and this result is consistent with the ORTHOLOG-HIT half "
                                 "failing in their GeneWise model rather than the window being unclean. "
                                 "It does not show their model was wrong: my hit is a protein alignment, "
                                 "not an ortholog call, and my hoxd13a hit is the weakest in my table "
                                 "(coverage 0.824, identity 0.447).")
    else:
        hox_report["finding"] = ("The 2 kb upstream window is not clean or not available, which is "
                                 "consistent with their stated drop reason.")

doc = {
    "scope": ("Cross-check of two independent computational placements on the same unannotated "
              "assembly: claude-evo's CDS-only GeneWise ortholog windows and this project's miniprot "
              "protein-to-genome best hits. Neither is an annotation or an orthology proof, so an "
              "agreement means two methods agree, not that a locus is correct."),
    "their_input_set": evo.get("input_set_id"),
    "their_windows_checked": len(rows),
    "agree": sum(1 for r in rows if r["verdict"].startswith("AGREE")),
    "paralog_mismatch": sum(1 for r in rows if r["verdict"].startswith("PARALOG MISMATCH")),
    "different_gene": sum(1 for r in rows if r["verdict"].startswith("DIFFERENT GENE")),
    "disagree_on_scaffold": sum(1 for r in rows if r["verdict"].startswith("DISAGREE")),
    "not_comparable_i_never_queried_it": sum(1 for r in rows if r["verdict"].startswith("NOT COMPARABLE")),
    "windows": rows,
    "dropped_hoxd13a": hox_report,
}
OUT_JSON.write_text(json.dumps(doc, indent=1) + "\n")

md = ["# Cross-check: claude-evo's flying-fish windows vs this project's miniprot hits", "",
      "**Scope.** " + doc["scope"], "",
      f"{doc['their_windows_checked']} windows checked: **{doc['agree']} agree** (flush to the base), "
      f"**{doc['paralog_mismatch']} paralog mismatch**, {doc['different_gene']} land at a different "
      f"gene of mine, {doc['disagree_on_scaffold']} disagree on scaffold, "
      f"{doc['not_comparable_i_never_queried_it']} not comparable because I never queried that gene.", "",
      "A window anchored upstream of a predicted start codon should sit flush against the CDS it "
      "belongs to: ending where the hit starts on the + strand, starting where it ends on the −.", "",
      "| their symbol | their region | strand | my nearest hit there | gap bp | flush | verdict |",
      "| --- | --- | --- | --- | --- | --- | --- |"]
for r in rows:
    n = r["my_nearest_hit_on_their_scaffold"]
    md.append(f"| {r['their_symbol']} | {r['their_region']} | {r['their_strand']:+d} | "
              f"{(n['query'] + ' (' + n['round'] + ')') if n else '—'} | {r['gap_bp']} | "
              f"{r['window_is_flush_against_that_hit']} | {r['verdict']} |")
md += ["", "## Their dropped flying-fish `hoxd13a`", "",
       f"- their stated reason: {hox_report.get('their_stated_drop_reason')}",
       f"- my hoxd13a best hit: {hox_report['my_hit']['scaffold']} "
       f"{hox_report['my_hit']['start']}–{hox_report['my_hit']['end']} ({hox_report['my_hit']['strand']}), "
       f"coverage {hox_report['my_hit']['coverage']}, identity {hox_report['my_hit']['identity']}"
       if hox_report.get("my_hit") else "- no hoxd13a hit of mine",
       f"- scaffold length {hox_report.get('scaffold_len')}; 2 kb upstream available: "
       f"{hox_report.get('upstream_2kb_available')} bp; non-ACGT bases in it: "
       f"{hox_report.get('non_ACGT_bases_in_window')}", "",
       hox_report.get("finding", "")]
OUT_MD.write_text("\n".join(md) + "\n")
print(json.dumps({k: v for k, v in doc.items() if k not in ("windows", "dropped_hoxd13a")}, indent=1))
for r in rows:
    print(f"  {r['their_symbol']:10s} {r['their_region']:24s} -> {r['verdict']}")
print("hoxd13a:", hox_report.get("upstream_2kb_available"), "bp available, non-ACGT",
      hox_report.get("non_ACGT_bases_in_window"))
