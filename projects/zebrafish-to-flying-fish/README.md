# Zebrafish to flying fish

**The question:** what would it actually take to get from *Danio rerio* to an Exocoetid-like gliding
fish? **The answer this project produced:** a sourced decomposition of the problem, a candidate-gene
table with explicit evidence levels, four comparative-genomics analyses that can be reproduced from this
directory, a perturbation table whose most useful output is the conflicts it exposes, and twelve
record drafts in the repo's own format.

**A plan is not a result.** Read [`PLAN.md`](PLAN.md) as a plan. The only results are in
[`RESULTS.md`](RESULTS.md), and they are retrievals and sequence alignments — nothing more.

**No fish was observed.** No Exocoetid and no zebrafish was handled, imaged, sequenced or perturbed
by this project. No full text was read for any source; every literature statement is abstract-level.
Nothing here demonstrates that a flying fish can be built.

## Files

| File | What it is |
| --- | --- |
| [`PLAN.md`](PLAN.md) | The plan: trait decomposition by scale (T1–T12), candidate genes and regulatory regions with evidence levels, runnable comparative genomics (G1–G7), the perturbation table (P1–P15) and its conflicts, engineering methods and feasibility, and the known / abstract-stated / unknown split. |
| [`RESULTS.md`](RESULTS.md) | Every computed result with its receipt: command, exit code, input sha256, tool version, seed, and a scope line saying what it does not license. Includes three corrections made after review. |
| [`LOCI.md`](LOCI.md) | Generated: the per-locus hit table plus the control, reproducibility and paralog-ambiguity checks. |
| [`SPAN-AUDIT.md`](SPAN-AUDIT.md) | Generated: assembly-gap fraction, largest intron and frameshift counts per best hit, so long spans can be discounted. |
| [`SOURCES.md`](SOURCES.md) | Generated: 45 Europe PMC queries, 227 saved records, 154 distinct PMIDs, each with the request URL and response sha256. Read-level is `abstract` for every row. |
| [`REVIEW.md`](REVIEW.md) | What an LLM critique found, which findings were verified and acted on, and which were rejected and why. |
| [`claims/zf2ff-claims.json`](claims/zf2ff-claims.json) | 9 Claim and 3 Problem drafts, validated against `frontier/models.py`. Validated is not true (SPEC-001). |
| `scripts/` | Everything that produced the above. |
| `data/` | Verbatim API responses, ledgers with hashes, PAF alignments, and the machine-readable summaries. |

## Reproducing the computed results

The assembly (1,008 MB) is not committed. Fetch it, build miniprot 0.18, then:

```sh
# assembly: NCBI Datasets, accession GCA_018398805.1, GENOME_FASTA
# expected FASTA sha256: 6f312a972a382295873cf1170771b0ef952f5f7772ce3b7bd19e3b49603c1052
python3 scripts/fetch_abstracts.py       data/epmc  data/epmc_jobs.json
python3 scripts/build_source_index.py    data/epmc,data/epmc2 data/source_index.json SOURCES.md
python3 scripts/map_proteins_round2.py   <GENOME.fna> <miniprot> data/queries_round2.json data/round2
python3 scripts/map_proteins_round2.py   <GENOME.fna> <miniprot> data/queries_round3.json data/round3
python3 scripts/merge_and_check_hits.py  data/mapping_summary.json,data/round2/mapping_summary_round2.json,data/round3/mapping_summary_round3.json data/loci_merged.json LOCI.md
python3 scripts/audit_long_spans.py      <GENOME.fna> data/miniprot.paf,data/round2/miniprot_round2.paf,data/round3/miniprot_round3.paf data/span_audit.json SPAN-AUDIT.md
python3 scripts/reciprocal_check.py      <GENOME.fna> <miniprot> data/families.json data/reciprocal
python3 scripts/make_claims.py           claims/zf2ff-claims.json
```

Round 1 (`scripts/map_proteins.py`, `data/mapping_summary.json`) was produced by a predecessor
process; it is reviewed here, not re-run.

## The four things worth taking away

1. **Fin size has a real genetic handle; the rest of the phenotype does not.** `kcnh2a` and `lat4a`
   are named by a flying-fish phylogenomic study whose abstract reports that their interaction in
   zebrafish phenocopies flying-fish fin proportions. For caudal asymmetry, ray material properties,
   launch muscle and glide behaviour this project found **no candidate gene at all**, and says so
   rather than inventing one.
2. **The conflicts are the useful output.** The edit that stiffens rays shrinks the fin; the edit that
   adds a keel removes fin rays; `kcnh2a` is a cardiac channel; most of the strongest evidence is
   from adult *regeneration* while a wing must be built in *development*; and an enlarged fin has a
   measured locomotor cost in the only organism in play.
3. **The plan designed the blade and forgot the root.** The pectoral girdle and fin musculature were
   missing until review caught it. They are plausibly the binding constraint and the
   worst-sourced part of the document.
4. **A computed check killed a headline row, and the follow-up check could not revive it.** Paralog
   controls run after review show the `kcnh2b` query aligning to the same region as `kcnh2a` at higher
   identity. A reciprocal best-hit test then **resolved** the parallel `shha`/`shhb` collision cleanly
   (5 of 5 predictions) but **failed to resolve** the `kcnh2` one: alignment score and percent identity
   rank the same predicted sequence differently. So after three mapping rounds, a span audit and a
   reciprocal test, the plan's primary candidate locus has no located target — reported as the
   non-result it is, not rounded to a conclusion.

## Status

Branch `claude/zf2ff-20261101`. Single operator (`claude-zf2ff`), 2026-11-01. Not independently
reviewed. Status file: `/data/artifacts/delphi-evolve-rethink/messages/claude-zf2ff-status.md`.
The Evo 2 handoff (`messages/evo-to-zf2ff.md`) did not exist while this was written, so no Evo 2
output is used here.
