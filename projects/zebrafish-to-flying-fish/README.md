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
| [`claims/zf2ff-claims.json`](claims/zf2ff-claims.json) | 11 Claim and 3 Problem drafts, validated against `frontier/models.py`. Validated is not true (SPEC-001). |
| `data/*/MANIFEST.md` | One manifest per Nebius job (`data/tree/`, `data/tree2/`, `data/census/`, `data/motif/`): job id, CLI-read state, preset, image, software versions, every input and output digest, the in-container re-hash of each input, and the quota refusals — including a job that failed at provisioning, kept rather than hidden. |
| [`CROSSCHECK-EVO.md`](CROSSCHECK-EVO.md) | Generated: the Evo 2 harness's 9 flying-fish windows checked against this project's independent placements. |
| `scripts/` | Everything that produced the above. |
| `data/` | Verbatim API responses, ledgers with hashes, PAF alignments, newick trees, job logs, and the machine-readable summaries. Subdirectories: `epmc*` literature, `round2`/`round3` mappings, `reciprocal`, `tree` (kcnh2 collision), `tree2` (kcnh2a hunt), `census` (family census + sensitivity), `tree5` (Beloniformes outgroups), `tree6` (Takifugu control), `motif` (three scan passes), `synteny`, `kcnh2a_hunt`. |

## Reproducing the computed results

The assembly (1,008 MB) is not committed. Fetch it, build miniprot 0.18, then:

```sh
# assembly: NCBI Datasets, accession GCA_018398805.1, GENOME_FASTA
# expected FASTA sha256: 6f312a972a382295873cf1170771b0ef952f5f7772ce3b7bd19e3b49603c1052
python3 scripts/fetch_abstracts.py       data/epmc  data/epmc_jobs.json
python3 scripts/build_source_index.py    data/epmc,data/epmc2,data/epmc3,data/epmc4 data/source_index.json SOURCES.md
python3 scripts/map_proteins_round2.py   <GENOME.fna> <miniprot> data/queries_round2.json data/round2
python3 scripts/map_proteins_round2.py   <GENOME.fna> <miniprot> data/queries_round3.json data/round3
python3 scripts/merge_and_check_hits.py  data/mapping_summary.json,data/round2/mapping_summary_round2.json,data/round3/mapping_summary_round3.json data/loci_merged.json LOCI.md
python3 scripts/audit_long_spans.py      <GENOME.fna> data/miniprot.paf,data/round2/miniprot_round2.paf,data/round3/miniprot_round3.paf data/span_audit.json SPAN-AUDIT.md
python3 scripts/reciprocal_check.py      <GENOME.fna> <miniprot> data/families.json data/reciprocal
python3 scripts/crosscheck_evo_windows.py <GENOME.fna> data/loci_merged.json <evo input_set.json> data/crosscheck_evo_windows.json CROSSCHECK-EVO.md
bash    scripts/hunt_kcnh2a.sh           # low-stringency kcnh2a-only search
python3 scripts/synteny_kcnh2a.py        <GENOME.fna> <miniprot> data/synteny
python3 scripts/build_tree_input.py      data/reciprocal/reciprocal_check.json data/tree/kcnh_tree_input.faa data/tree/kcnh_tree_input_ledger.json 4
python3 scripts/analyze_tree.py          data/tree/zf2ff_kcnh.treefile data/tree/tree_analysis.json
python3 scripts/build_motif_input.py     <evo input_set.json> <evo scores.json> data/motif/windows_all.fa data/motif/windows_ledger.json <evo controls.json>
python3 scripts/make_claims.py           claims/zf2ff-claims.json
```

The six Nebius jobs ran the scripts prefixed `job_` (`job_run_tree*.sh`, `job_motif_*.py`,
`job_run_motif.sh`, `job_run_robust.sh`, `job_run_heldout.sh`) exactly as committed; each manifest
names which script it used, and the jobs re-hash their inputs in-container so the digests in the
manifests can be checked against the files here.

Round 1 (`scripts/map_proteins.py`, `data/mapping_summary.json`) was produced by a predecessor
process; it is reviewed here, not re-run.

## The five things worth taking away

1. **Fin size has a real genetic handle; the rest of the phenotype does not.** `kcnh2a` and `lat4a`
   are named by a flying-fish phylogenomic study whose abstract reports that their interaction in
   zebrafish phenocopies flying-fish fin proportions. For caudal asymmetry, ray material properties,
   launch muscle and glide behaviour this project found **no candidate gene at all**, and says so
   rather than inventing one.
2. **The conflicts are the useful output.** Each of these is what a paper's **abstract** states, read
   at abstract level and not verified against its figures: the `hox13` edit that shifts rays toward
   spiny character also shrinks the fin fold and deletes actinotrichia; `eda` loss removes scales
   *and* fin rays; KCNH-family channels are described as having prominent cardiovascular roles with
   mutations linked to arrhythmias, which is a general family statement, not a measured `kcnh2a`
   cardiac phenotype in a long-finned fish; and most of the strongest size-control evidence is from
   adult *regeneration* while a wing must be built in *development*. One more conflict is weaker
   still: a published comparison of wildtype and longfin zebrafish **tested** jump kinematics,
   voluntary jumping and exhaustion, and this project read its design but **not its result**, so
   whether enlarged fins cost performance is unknown here — which is exactly why measuring it is the
   first thing the plan would do.
3. **The plan designed the blade and forgot the root.** The pectoral girdle and fin musculature were
   missing until review caught it. They are plausibly the binding constraint and the
   worst-sourced part of the document.
4. **Six Nebius jobs went looking for the plan's primary candidate gene and did not find it.**
   Paralog controls showed the `kcnh2b` query hitting the same region as `kcnh2a`. A gene tree with
   human outgroups and a **passing positive control** placed that region with `kcnh2b` (99/100). A
   low-stringency hunt found no new region. A second tree assigned all five remaining candidates to
   other paralogs, both carried-forward controls reproducing. A family census then placed 14
   KCNH-like loci and found **9 of 10 zebrafish paralogs have a flying-fish locus while `kcnh2a` has
   none** — so the gap is gene-specific in this assembly, not general incompleteness. `kcnh2a` is the
   `longfin` gene and this plan's primary candidate. Two further trees then settled *why*: medaka and
   the flying fish both carry the `kcnh2b` copy, while **Takifugu, a non-Beloniform, pairs with
   zebrafish `kcnh2a` at 100/100**. So `kcnh2a` is **absent from the Beloniform lineage** — a lineage
   fact, not an assembly gap — and the headline edit has **no target gene to edit**. The chain took
   five steps and three of them contradicted the step before; every reversal is kept in the repo.
5. **A robustness pass overturned one of this project's own results.** The first motif scan reported a
   null zebrafish arm and a strong flying-fish one. Its manifest named two design weaknesses *before*
   the follow-up ran; the follow-up removed them and the asymmetry vanished. A third pass with a
   held-out threshold halved the effect and killed every per-window claim. What survives is one
   aggregate result, direction-robust across three designs and matched independently by another
   harness's own implementation.

## Status

Branch `claude/zf2ff-20261101`. Single operator (`claude-zf2ff`), 2026-11-01. Not independently
reviewed. Status file: `/data/artifacts/delphi-evolve-rethink/messages/claude-zf2ff-status.md`.
The Evo 2 handoff (`messages/evo-to-zf2ff.md`) did not exist while this was written, so no Evo 2
output is used here.
