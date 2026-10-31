"""Freeze the public, benign input set before any candidate is generated.

Ten well-characterised zebrafish genes, all standard benign developmental or
tissue markers routinely used as reporter drivers. For each, the 2 kb
immediately 5' of the transcription start site is split in half:

    [TSS-2000 .. TSS-1001]  distal half  -> the PROMPT the model sees
    [TSS-1000 .. TSS-1]     proximal half -> HELD OUT, never shown to the model

The held-out proximal half is the comparator a generated candidate is measured
against. Holding it out is what makes the assessment a held-out one rather than
a restatement of the prompt.

Output is committed before the GPU job runs, so the inputs cannot be chosen
after seeing an output.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import ensembl, ucsc  # noqa: E402
from connectors.bioservices.receipts import (  # noqa: E402
    RetrievalReceipt, sha256_text, utc_now, write_json,
)

# Benign, well-studied zebrafish genes. Every one is a standard developmental or
# tissue marker; several are the classic reporter drivers of the field. Nothing
# here is a pathogen, a toxin or a human-virus sequence.
TARGETS = [
    ("myod1", "skeletal muscle differentiation"),
    ("elavl3", "pan-neuronal (HuC)"),
    ("myl7", "cardiac myosin light chain (cmlc2)"),
    ("fabp10a", "liver"),
    ("gata1a", "erythroid"),
    ("sox10", "neural crest"),
    ("neurod1", "neuronal differentiation"),
    ("krt4", "periderm / epithelial keratin"),
    ("pax2a", "midbrain-hindbrain, otic, pronephros"),
    ("ins", "pancreatic beta cell (preproinsulin)"),
]

UCSC_GENOME = "danRer11"   # the same assembly as Ensembl GRCz11
UPSTREAM_BP = 2000
HALF = 1000


def main() -> int:
    ap = argparse.ArgumentParser(description="Freeze the zebrafish regulatory input set")
    ap.add_argument("--out", required=True)
    ap.add_argument("--species", default="danio_rerio")
    ap.add_argument("--lookup-cache", required=True,
                    help="gene coordinates, written as each resolves so a killed run resumes")
    args = ap.parse_args()

    # Ensembl REST has been unreliable from this host. Each resolved gene is
    # cached the moment it arrives, so a killed run resumes instead of restarting
    # and the flaky service is asked for each gene at most once, ever.
    cache = json.load(open(args.lookup_cache)) if os.path.exists(args.lookup_cache) else {}
    assembly_name = cache.get("_assembly")
    if not assembly_name:
        assembly_name = ensembl.assembly(args.species).get("assembly_name")
        cache["_assembly"] = assembly_name
        write_json(args.lookup_cache, cache)
    records, receipts, cross_checks, unresolved = [], [], [], []
    for symbol, note in TARGETS:
        if symbol in cache:
            gene = ensembl.Gene(**cache[symbol])
        else:
            try:
                gene = ensembl.lookup_symbol(symbol, args.species)
            except Exception as exc:
                # One annotation source for every target, or none. UCSC/RefSeq
                # could resolve this symbol, but RefSeq and Ensembl disagree about
                # gene ends -- measured 179 bp for neurod1 -- and on a minus-strand
                # gene the end IS the TSS, so a mixed source would define one
                # target's promoter differently from the rest. Dropping the target
                # is the smaller loss, and it is recorded rather than hidden.
                unresolved.append({"symbol": symbol, "tissue_note": note,
                                   "reason": f"{type(exc).__name__}: {str(exc)[:160]}"})
                print(f"  {symbol:9s} UNRESOLVED ({type(exc).__name__}); dropped, see input_set.json")
                continue
            cache[symbol] = dict(gene.__dict__)
            write_json(args.lookup_cache, cache)
        lo, hi = gene.upstream_region(UPSTREAM_BP)

        # UCSC is PRIMARY for sequence. Ensembl REST returned 500, 503 and read
        # timeouts from this host within minutes of each other while UCSC served
        # every request, so the reliable source carries the data and the flaky
        # one is a best-effort second opinion.
        seq = ucsc.sequence(UCSC_GENOME, gene.chromosome, lo, hi, gene.strand)
        if len(seq) != UPSTREAM_BP:
            raise SystemExit(f"{symbol}: expected {UPSTREAM_BP} bp, got {len(seq)}")
        bad = sorted(set(seq) - set("ACGT"))
        if bad:
            raise SystemExit(f"{symbol}: sequence contains non-ACGT {bad} (assembly gap?)")
        receipt = RetrievalReceipt(
            source_id=f"ucsc.sequence.{UCSC_GENOME}",
            url=f"https://api.genome.ucsc.edu/getData/sequence?genome={UCSC_GENOME}"
                f";chrom=chr{gene.chromosome};start={lo - 1};end={hi}",
            state="retrieved", retrieved_utc=utc_now(), size_bytes=len(seq),
            sha256=sha256_text(seq), media_type="application/json",
            license="UCSC Genome Browser data: free for academic and non-profit use",
            version=UCSC_GENOME, notes=[f"strand {gene.strand:+d}, oriented by the connector"],
        ).to_dict()

        # Independent second read. GRCz11 and danRer11 are the same assembly under
        # two names, but the browsers differ in coordinate convention, so agreement
        # checks that the coordinates mean what they are assumed to mean. Recorded
        # as unchecked rather than skipped silently when Ensembl is unavailable.
        try:
            ens_seq, _ = ensembl.sequence(gene.chromosome, lo, hi, gene.strand, args.species,
                                          retries=0, timeout=12)
            check = ucsc.agrees(ens_seq, seq)
            if not check["identical"]:
                raise SystemExit(f"{symbol}: Ensembl and UCSC disagree on {lo}-{hi}: {check}")
            cross_checks.append({"symbol": symbol, "checked": True,
                                 "ucsc_genome": UCSC_GENOME, **check})
        except SystemExit:
            raise
        except Exception as exc:
            cross_checks.append({"symbol": symbol, "checked": False,
                                 "reason": f"{type(exc).__name__}: {str(exc)[:120]}"})

        prompt, held_out = seq[:HALF], seq[HALF:]
        records.append({
            "symbol": symbol,
            "tissue_note": note,
            "gene_id": gene.gene_id,
            "chromosome": gene.chromosome,
            "gene_start": gene.start,
            "gene_end": gene.end,
            "strand": gene.strand,
            "tss_forward": gene.tss,
            "upstream_region_forward": [lo, hi],
            "prompt_seq": prompt,
            "prompt_sha256": sha256_text(prompt),
            "prompt_gc": round(ensembl.gc_fraction(prompt), 4),
            "held_out_seq": held_out,
            "held_out_sha256": sha256_text(held_out),
            "held_out_gc": round(ensembl.gc_fraction(held_out), 4),
            "description": gene.description,
        })
        receipts.append(receipt)
        print(f"  {symbol:9s} {gene.gene_id} chr{gene.chromosome}:{lo}-{hi} strand {gene.strand:+d} "
              f"prompt_gc={ensembl.gc_fraction(prompt):.3f} held_gc={ensembl.gc_fraction(held_out):.3f}")

    payload = {
        "input_set_id": "zebrafish-promoter-proximal-2kb/v1",
        "frozen_utc": utc_now(),
        "species": args.species,
        "assembly": assembly_name,
        "upstream_bp": UPSTREAM_BP,
        "prompt_bp": HALF,
        "held_out_bp": HALF,
        "n_targets": len(records),
        "unresolved_targets": unresolved,
        "annotation_source": "Ensembl REST gene coordinates only; never mixed with RefSeq",
        "scope": ("public reference genome only; benign model-organism developmental and tissue "
                  "markers; no pathogen, toxin or human-virus sequence"),
        "independent_cross_checks": cross_checks,
        "targets": records,
        "receipts": receipts,
    }
    digest = write_json(args.out, payload)
    all_seq = "".join(r["prompt_seq"] + r["held_out_seq"] for r in records)
    if len(records) < 9:
        raise SystemExit(f"only {len(records)} targets resolved; need at least 9 "
                         f"(8 design + 1 fully held out)")
    print(f"\nassembly: {assembly_name}  targets: {len(records)}  "
          f"unresolved: {[u['symbol'] for u in unresolved] or 'none'}")
    checked = [c for c in cross_checks if c.get("checked")]
    print(f"sequence source: UCSC {UCSC_GENOME} (primary)")
    print(f"independent Ensembl cross-check: {sum(c['identical'] for c in checked)}/{len(checked)} "
          f"identical; {len(cross_checks) - len(checked)} region(s) unchecked (Ensembl unavailable)")
    print(f"input set sha256 (file): {digest}")
    print(f"concatenated sequence sha256: {sha256_text(all_seq)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
