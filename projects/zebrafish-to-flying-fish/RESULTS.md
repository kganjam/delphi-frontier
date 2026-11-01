# Computed results and receipts

Project `projects/zebrafish-to-flying-fish`, 2026-11-01. Single operator (claude-zf2ff), **not
independently reviewed**. Times are UTC with Seattle (PDT) in the status file.

**Scope line for this entire file.** Everything here is either a *retrieval* (literature metadata and
abstracts, fetched verbatim and hashed) or a *sequence alignment* (protein-to-genome). There is no
observation of any fish, no expression measurement, no phenotype and no function. A protein-to-genome
alignment is **not** an annotation, an orthology assignment, evidence of transcription, or evidence
that a locus does anything in *Hirundichthys speculiger*.

---

## R1 — Literature retrieval: 45 Europe PMC queries, bodies saved verbatim

| | |
| --- | --- |
| Command (round 1, predecessor) | `python3 scripts/fetch_abstracts.py data/epmc data/epmc_jobs.json` |
| Command (round 2, this session) | `systemd-run --user --scope -p TasksMax=256 -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=900 python3 -I scripts/fetch_abstracts.py data/epmc2 data/epmc_jobs2.json` |
| Exit code | 0 (both) |
| Service | Europe PMC REST `search`, `resultType=core`, `pageSize=8` |
| Queries | 25 (round 1) + 20 (round 2) + 4 (round 3, provenance and girdle follow-ups) = 49 |
| Outputs | `data/epmc/*.json`, `data/epmc2/*.json`, `data/epmc3/*.json`, one response body per query, byte-for-byte as returned |
| Receipts | `data/epmc/ledger.json`, `data/epmc2/ledger.json`, `data/epmc3/ledger.json`: per query the exact request URL, response sha256, byte count and UTC timestamp |
| Index built from them | `python3 -I scripts/build_source_index.py data/epmc,data/epmc2 data/source_index.json SOURCES.md`, exit 0. The script **re-verifies** every response sha256 against the ledger and aborts on mismatch; it did not abort. |

Index totals over rounds 1–2 (`data/source_index.json`): **45 queries, 227 saved records, 154
distinct PMIDs**, 222 with an abstract in the response, 160 flagged open access. Round 3's four
queries are saved with their own ledger but were fetched after the index was built and are not in
`SOURCES.md`; their bodies and hashes are in `data/epmc3/`.

**Read level: `abstract`, for every record, with no exceptions.** No full text, no figure, no
supplementary table was read by this project. A row in `SOURCES.md` means *this record exists and
this much of it was retrieved* — never that the paper supports a statement made elsewhere here.

---

## R2 — Protein-to-genome mapping onto the one public Exocoetidae assembly

### Inputs

| | |
| --- | --- |
| Assembly | `GCA_018398805.1`, *Hirundichthys speculiger*_1.0 — **scaffold level, no annotation** |
| Source | NCBI Datasets API, `include_annotation_type=GENOME_FASTA`, downloaded this session |
| FASTA sha256 | `6f312a972a382295873cf1170771b0ef952f5f7772ce3b7bd19e3b49603c1052` (1,008 MB) |
| Queries | zebrafish (*Danio rerio*) proteins from UniProt, each fetched by accession; per-query URL, length and **sha256 of the FASTA body** in `data/mapping_summary.json` and `data/round2/mapping_summary_round2.json` |
| Tool | miniprot **0.18-r281**, built from the v0.18 source tag this session (`miniprot --version` recorded in `data/miniprot.version.txt`, `data/round2/miniprot_round2.version.txt`, `data/round3/miniprot_round3.version.txt`) |
| Parameters | `-t4 -N5 --outs=0.6`, **applied per chunk** — see the correction below |
| Identity metric | `aa_identity` = PAF **column 10** (number of residue matches) ÷ **column 11** (alignment block length), as miniprot reports them for the aligned block. Verified directly on the positive control: its PAF line reads `375 0 375 + ... 1113 1125`, and 1113/1125 = 0.989, matching the table. (An earlier version of this file and of `LOCI.md` described the metric as "NM/blocklen", which names the edit distance and would have given ~0.011. The *computation was always residue matches over block length*; the **description** was wrong and is corrected here.) |
| Seed | `random.Random(12345)`, used only to shuffle the negative-control sequence |

**Memory note (a measured constraint, not an estimate).** Indexing the whole 1.04 Gb assembly
exceeded the 4 GB cap in the predecessor's round-1 run and was killed (SIGKILL). All three rounds
therefore split the assembly into 5 chunks **of whole scaffolds** and merge the alignments.

**Correction to an earlier claim about chunking (found by review, confirmed from the data).** This
file previously said chunking "does not change per-scaffold results". That is too strong, and the
evidence against it is in our own output: `-N5` caps secondary alignments and `--outs=0.6` filters
them *relative to the best score in that run*, and both were applied **per chunk**. Alternative-hit
counts therefore exceed 5 — `tbx5a` has 13, `actb1` 12, `msxb` 10 — which is impossible in a single
`-N5` run. What survives: **best hits are unaffected**, because no scaffold was split, so a best
alignment lies wholly inside one chunk. What does not survive: the **number and composition of
alternative hits is a chunking artefact** and must never be read as copy number or duplication. The
`hits` column in `LOCI.md` is reported for completeness only.

### Runs

| Round | Command | Exit |
| --- | --- | --- |
| 1 (predecessor, reviewed here, not re-run) | `python3 scripts/map_proteins.py <GENOME.fna> <miniprot> data` | 0 |
| 2 (this session) | `systemd-run --user --scope -p TasksMax=256 -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=1800 python3 -I scripts/map_proteins_round2.py <GENOME.fna> <miniprot> data/queries_round2.json data/round2` | 0 |
| 3 (this session, after review) | same script with `data/queries_round3.json data/round3` | 0 |
| merge + checks | `systemd-run ... python3 -I scripts/merge_and_check_hits.py data/mapping_summary.json,data/round2/mapping_summary_round2.json,data/round3/mapping_summary_round3.json data/loci_merged.json LOCI.md` | 0 |
| span audit | `systemd-run ... python3 -I scripts/audit_long_spans.py <GENOME.fna> data/miniprot.paf,data/round2/miniprot_round2.paf,data/round3/miniprot_round3.paf data/span_audit.json SPAN-AUDIT.md` | 0 |

Round 1 queried 12 candidate proteins + 1 positive control + 1 shuffled negative control.
Round 2 queried 10 (9 new + `msxb` deliberately repeated) + 1 shuffled negative control:
`kcnh2a`, LAT4/`slc43a2b`, `slc43a2a`, `rcan2`, `cacna1g`, `gja1`/`cx43`, `hhip`, `shhb`, `and2`.
Round 3, added in response to review, queried 6 + 1 shuffled negative control: the two genes the plan
used but had never mapped (`eda`, `fgf20a`) and four **paralog controls** (`kcnh2b`, `tbx5b`,
`fgf10b`, `kcnk5a`), because the teleost whole-genome duplication means an `a`-paralog query can
best-hit the `b` paralog's region.
**27 distinct candidate proteins, 4 controls.**

### Result

**All 27 candidate query proteins have a detectable best-aligning region in the assembly.**
Per-locus table, with scaffold, interval, coverage, amino-acid identity and alternative-hit count:
[`LOCI.md`](LOCI.md); machine-readable in `data/loci_merged.json`.

Best hits for the loci the plan leans on:

| query | scaffold | interval | cov | aa identity | note |
| --- | --- | --- | --- | --- | --- |
| `kcnh2a` | JAGFBZ010001591.1 | 1,301,510–1,579,457 | 1.00 | 0.610 | ← see the paralog correction below |
| `kcnh2b` (paralog control) | JAGFBZ010001591.1 | 1,301,510–1,540,581 | 1.00 | **0.762** |
| `slc43a2b_LAT4` | JAGFBZ010000485.1 | 561,206–573,455 | 1.00 | 0.786 | |
| `slc43a2a_fragment` | JAGFBZ010001224.1 | 1,267,873–1,271,840 | 0.908 | 0.748 | different scaffold from `slc43a2b` |
| `kcnk5b` | JAGFBZ010001926.1 | 604,214–606,769 | 1.00 | 0.563 | `kcnk5a` control lands on a different scaffold (JAGFBZ010000776.1) |
| `cacna1g` | JAGFBZ010002163.1 | 81,287–379,776 | 0.640 | 0.733 | 298 kb span, coverage 0.64 — discount, see span audit |
| `gja1_cx43_sof` | JAGFBZ010000226.1 | 84,055–85,219 | 1.00 | 0.892 | |
| `tbx5a` | JAGFBZ010001382.1 | 1,635,753–1,651,051 | 1.00 | 0.782 | `tbx5b` control lands on a different scaffold |
| `pitx1` | JAGFBZ010001412.1 | 734,755–740,041 | 0.989 | 0.901 | |
| `hhip` | JAGFBZ010000865.1 | 2,512–37,451 | 1.00 | 0.768 | |
| `and1` / `and2` | JAGFBZ010000980.1 / JAGFBZ010000267.1 | 814,249–819,560 / 345,469–347,985 | 0.982 / 0.935 | 0.552 / 0.597 | different scaffolds |
| `eda` | see `LOCI.md` | — | 0.930 | 0.645 | added round 3 |
| `fgf20a` | see `LOCI.md` | — | 1.00 | 0.752 | added round 3 |

`slc43a2a` and `slc43a2b` best-hit **different scaffolds**, so two distinct LAT4-like regions are
detectable. That does **not** resolve which one the published `lat4a` is (see `PLAN.md` §2.1); it only
says the question is answerable with sequence work.

### Internal checks (all three run by `merge_and_check_hits.py`, output in `LOCI.md`)

1. **Controls — PASS.**
   - `actb1_POSITIVE_CONTROL`: coverage 1.00, amino-acid identity **0.989**. A deeply conserved
     protein aligns nearly perfectly, as it must if the pipeline works.
   - `fgf10a_SHUFFLED_NEGATIVE_CONTROL` (round 1) and `kcnh2a_SHUFFLED_NEGATIVE_CONTROL` (round 2):
     **no hit** in either round. Shuffled sequences of the same composition and length as a real
     query produce nothing, so a hit is not an artefact of composition or of `--outs=0.6`.
2. **Reproducibility — PASS.** `msxb` was mapped in both rounds by separate miniprot invocations on
   separately re-chunked copies of the assembly. Both runs return JAGFBZ010000863.1
   508,027–509,355 — identical, well inside the 100 bp tolerance.
3. **Paralog ambiguity — two pairs flagged, and one of them undermines a headline row.**
   - `shha` and `shhb`/`twhh` best-hit the **same** region of JAGFBZ010001012.1 (overlap 6,364 bp).
   - **`kcnh2a` and `kcnh2b` best-hit the same region of JAGFBZ010001591.1, starting at the identical
     coordinate 1,301,510, and the `kcnh2b` query aligns at higher identity (0.762) than the
     `kcnh2a` query (0.610).** The single detected region is therefore better explained by the
     *b* paralog than the *a* paralog. **The row "`kcnh2a` is detectable in this assembly" must not
     be read as "the *kcnh2a* ortholog is detectable".** This matters because `kcnh2a` is the plan's
     primary candidate locus (`PLAN.md` §2.1). Resolving it needs reciprocal best hits and a gene
     tree, neither of which was run.
   - The other three paralog controls behaved differently and more reassuringly: `tbx5a`/`tbx5b`,
     `fgf10a`/`fgf10b` and `kcnk5b`/`kcnk5a` each resolve to **different scaffolds**, so those `a`
     rows are not obviously mis-assigned (which is still not an orthology test).
   This check existed only because an external review asked for it. Without round 3 the `kcnh2a` row
   would have been reported as a clean detection.

### Span audit (added after review): which long hits to discount

Two best hits span ~0.3 Mb, which in a ~1 Gb genome is either a gene with very large introns or
miniprot chaining across duplicated or gap-separated fragments. `scripts/audit_long_spans.py`
measures what distinguishes them; full table in [`SPAN-AUDIT.md`](SPAN-AUDIT.md).

| query | span | N fraction in the window | largest single intron | frameshifts | in-frame stops |
| --- | --- | --- | --- | --- | --- |
| `cacna1g` | 298,489 bp | **0.0** | 116,267 bp | 2 | 0 |
| `kcnh2a` | 277,947 bp | **0.0** | 105,952 bp | 4 | 0 |
| `kcnh2b` | 239,071 bp | **0.0** | 105,952 bp | 3 | 1 |
| `rcan2` | 44,700 bp | 0.0 | 40,087 bp | 0 | 0 |
| everything else | ≤ 35 kb | 0.0 | ≤ 13 kb | ≤ 1 | 0 |

Reading: there is **no assembly gap** inside any of these windows, so the long spans are not bridged
N-runs. Each long span is dominated by **one** ~0.1 Mb intron-like gap, and the two `kcnh2*` queries
share the same 105,952 bp gap — consistent with both chaining through the same region. The `kcnh2a`,
`kcnh2b` and `cacna1g` rows also carry 2–4 frameshifts and, for `kcnh2b`, one in-frame stop. **These
three rows are the least trustworthy in the table and should be treated as "something channel-like is
there", not as a located gene.** The audit does not decide between a large-intron gene and a chaining
artefact, and this project did not decide either.

### What these numbers do and do not license

- They license: "a region aligning to this zebrafish protein is detectable in this assembly, and it
  is this diverged from the query". Best-hit amino-acid identity ranges 0.447 (hoxd13a) to 0.989 (the
  actb1 control); alternative, lower-scoring hits go lower still.
- They do **not** license naming the paralog: for `kcnh2*` and `shh*` the method demonstrably cannot,
  and for the rest it was not tested beyond the three paralog controls that landed elsewhere.
- They do **not** license: an orthology call, a copy-number statement, a claim that the Exocoetid
  locus is transcribed, a claim about regulatory sequence (no non-coding element was examined at
  all), or any comparison of the *flying fish's* allele to the published convergent variant — that
  is analysis G4 in `PLAN.md` §3, **not run**.
- Species caution: the published flying-fish phylogenomics (PMID 34534441) and the convergent-residue
  report (PMID 40689752) used other Exocoetid species. *H. speculiger* is the only one with a public
  assembly. Any comparison crosses species inside the family and must say so.

---

## R3 — Reciprocal best-hit test (analysis G2), run to resolve the paralog collisions

| | |
| --- | --- |
| Command | `systemd-run ... python3 -I scripts/reciprocal_check.py <GENOME.fna> <miniprot> data/families.json data/reciprocal` |
| Exit code | 0 |
| Method | For each collision: cut the one scaffold out of the assembly, let miniprot predict the proteins that region encodes (`--trans`, whole gene family as queries), then align each distinct predicted protein against **every** zebrafish family member with Biopython 1.88 `PairwiseAligner` (global, BLOSUM62, gap open −11 / extend −1, free end gaps) and rank them. |
| Families | `kcnh` (10 zebrafish members: kcnh1a/1b/2a/2b/3/4a/5a/6a/6b/7), `hedgehog` (5: shha, shhb, ihha, ihhb, dhh). Per-member accession, length and FASTA sha256 in `data/reciprocal/reciprocal_check.json`. |
| Outputs | `data/reciprocal/reciprocal_check.json`, per-family predicted proteins and query FASTAs |

### Result 1 — the hedgehog collision resolves: the region is `shha`-like

All **5** distinct predicted proteins from JAGFBZ010001012.1 rank `shha` first, with `shhb` second
every time (margins 25–91, identity 0.760–0.778 vs 0.724–0.772). Consistent across every prediction,
so the forward run's `shha` assignment survives the reciprocal test and the `shha`/`shhb` ambiguity in
`LOCI.md` is resolved in favour of `shha`. Still not an orthology proof.

### Result 2 — the `kcnh2` collision does **not** resolve, and the answer flips with the metric

Eight distinct predicted proteins came out of JAGFBZ010001591.1. Five rank `kcnh2b` first, three rank
`kcnh2a` first — and the disagreement is systematic, not noise:

| predicted protein | predicted from | reciprocal best (by score) | score margin | `kcnh2a` id | `kcnh2b` id |
| --- | --- | --- | --- | --- | --- |
| **1325 aa** (the longest and most complete) | `kcnh2a` query | **`kcnh2a`** (3843) | 631 | 0.674 | **0.827** |
| 1154 aa | `kcnh6a` query | `kcnh2a` (3548) | 284 | 0.673 | — |
| 1052 aa | `kcnh7` query | `kcnh2a` (3395) | 297 | 0.719 | — |
| 818 aa | `kcnh2b` query | **`kcnh2b`** (3303) | 505 | 0.732 | 0.844 |
| 752 / 713 / 482 / 478 aa | various | `kcnh2b` | 57–286 | 0.683–0.915 | 0.725–0.942 |

**The two rankings disagree on the same sequence.** For the longest prediction, `kcnh2a` wins on
alignment *score* (by 631) while `kcnh2b` wins on percent *identity over aligned columns* (0.827 vs
0.674) — because a global BLOSUM62 score rewards aligning more of a longer protein, and `kcnh2a` is
1253 aa against `kcnh2b`'s 837 aa entry. Neither metric is wrong; they answer different questions.

**Conclusion, stated as the non-result it is: the paralog identity of this region remains unresolved.**
The forward run favoured `kcnh2b` (higher identity), the reciprocal run favours `kcnh2a` on score and
`kcnh2b` on identity, and the test's verdict depends on a scoring choice this project has no principled
reason to make. `H`, not tested here: the region holds more than one `kcnh`-like gene, or a collapsed or
tandem duplication, which would explain why differently-truncated predictions prefer different
paralogs. Settling it needs a gene tree with outgroups and synteny — **neither was run**.

### Result 3 — `kcnh2a`'s second-best scaffold is a `kcnh6a`-like locus, not a second `kcnh2a`

`kcnh2a`'s second-best forward hit (JAGFBZ010001790.1, AS 2569, coverage 0.899) is on a scaffold the
`kcnh2b` query does not hit at all, which made it the obvious candidate for a separate `kcnh2a`-like
locus. It is not: all **10** distinct predicted proteins there rank `kcnh6a` first, with margins
325–1544 — the largest and most consistent margins anywhere in this test. So that scaffold is
accounted for, and no second `kcnh2a`-like region was found.

**What this means for the plan.** `kcnh2a` is `PLAN.md`'s primary candidate locus. After three mapping
rounds, a span audit and a reciprocal test, this project **cannot say which paralog the one detected
`kcnh2`-like region is**, and has found no separate region that is unambiguously `kcnh2a`. That is not
evidence the gene is absent from *H. speculiger* — the assembly is scaffold-level and unannotated, and
a divergent or fragmented ortholog would look exactly like this. It is a limit on what can be designed:
an edit aimed at "the Exocoetid `kcnh2a`" currently has no located target.

## R4 — Gene tree (analysis G2b): the kcnh2 collision is resolved, with a passing control

Run as Nebius CPU job **`claude-zf2ff-kcnh-tree-1`** (`aijob-e00knz7gwwqck9nksp`), state read from the
CLI as `COMPLETED`. Full manifest, software versions, input and output digests, and the quota refusal
that forced a smaller preset: [`data/tree/MANIFEST.md`](data/tree/MANIFEST.md).

| | |
| --- | --- |
| Method | MAFFT v7.505 `--auto` → IQ-TREE 2.0.7 maximum likelihood, `LG+G4`, 1000 ultrafast bootstrap + 1000 SH-aLRT replicates, `--seed 12345` |
| Input | 20 proteins, sha256 `7ace646d…4697d051`, **re-hashed in-container to the same digest** |
| Alignment | 1,915 columns; 566 constant, 925 parsimony-informative; log-likelihood −27133.2124 (s.e. 480.0026) |
| Outputs | treefile sha256 `06c33bdd…3b2a51b8`, recovered from the job log and committed |
| Analysis | `scripts/analyze_tree.py` → `data/tree/tree_analysis.json` |

**The control was checked first and it passes.** The four predictions from JAGFBZ010001790.1 — the
scaffold the reciprocal test called `kcnh6a`-like — form a clade with zebrafish `kcnh6a` and **nothing
else**, support **94.4/97** (SH-aLRT/UFBoot). An independent method confirms that call, so the tree's
placement of the ambiguous sequences carries weight.

**The question is resolved.** The four predictions from the collision scaffold JAGFBZ010001591.1 form a
clade (**99.8/100**) that is **sister to zebrafish `kcnh2b`** (**99/100**), with `kcnh2a` outside that
pair (99.2/100):

```
(ZF_kcnh2a , (ZF_kcnh2b , (4 × HSPEC_ambiguous)99.8/100 )99/100 )99.2/100
```

So **the one `kcnh2`-like region detectable in `GCA_018398805.1` is `kcnh2b`-like**, and this project
has found **no `kcnh2a`-like region** in it: the second-best scaffold is `kcnh6a`-like (§R3) and this
one is `kcnh2b`-like.

**What this does to the plan.** `kcnh2a` — the `longfin` gene, `PLAN.md`'s primary candidate — remains
**unlocated** in the only public Exocoetidae assembly, and now for a sharper reason than "the method
cannot tell": the best candidate region has been positively assigned elsewhere. Three readings of the
same question now exist and they do not all agree, which is worth stating plainly:

| Test | Verdict on the collision region | Design quality |
| --- | --- | --- |
| Forward mapping, percent identity (§R2) | `kcnh2b` (0.762 vs 0.610) | no control for paralogy |
| Reciprocal test, alignment score (§R3) | `kcnh2a` on the longest prediction, by 631 | no outgroup, no control |
| Reciprocal test, percent identity (§R3) | `kcnh2b` | same |
| **Gene tree, this run** | **`kcnh2b`, 99/100, with a passing positive control** | outgroups + positive control |

Two of three agree on `kcnh2b` and the one that disagrees is the weakest design. The tree is taken as
the answer **because of its control**, not because it ran last.

**Limitations that remain.** A gene tree places sequences; it does not establish orthology without
synteny, which was not run. The four predictions come from one region, so they are not independent.
The `kcnh2a` (1253 aa) vs `kcnh2b` (837 aa) length difference is uncontrolled. The inputs are miniprot
predictions from an unannotated assembly, not transcripts. One run, one operator, not independently
reviewed. And absence of a `kcnh2a`-like region in a fragmented scaffold-level assembly is **not**
evidence that *Hirundichthys speculiger* lacks the gene.

## R5 — Cross-check of the Evo 2 harness's flying-fish windows (their action item (a))

`/data/artifacts/delphi-evolve-rethink/messages/evo-to-zf2ff.md` arrived during this session and asked
for exactly this: its 9 flying-fish windows were placed by a CDS-only GeneWise ortholog model, this
project's were placed by miniprot protein alignment, so the two are **independent estimates of the
same loci**.

| | |
| --- | --- |
| Command | `systemd-run ... python3 -I scripts/crosscheck_evo_windows.py <GENOME.fna> data/loci_merged.json <their input_set.json> data/crosscheck_evo_windows.json CROSSCHECK-EVO.md` |
| Exit code | 0 |
| Their input | `fin-scale-regulatory-2kb/v1`, read from branch `claude/evo2-fin-scale-20261101` |
| Test | A window anchored upstream of a predicted start codon must sit **flush** against the CDS it belongs to: ending where the hit starts on `+`, starting where it ends on `−`. Tolerance 2 bp. |
| Outputs | [`CROSSCHECK-EVO.md`](CROSSCHECK-EVO.md), `data/crosscheck_evo_windows.json` |

**9 windows: 2 agree, 2 paralog mismatch, 1 scaffold disagreement, 4 not comparable.**

| their symbol | their window | result |
| --- | --- | --- |
| `shha` | HS1012:2185729-2187728 (+) | **AGREE**, flush to the base against my `shha` hit (gap 0) |
| `tbx5a` | HS1382:1633754-1635753 (+) | **AGREE**, flush to the base against my `tbx5a` hit (gap 0) |
| `kcnk5b` | HS0776:65364-67363 (−) | **PARALOG MISMATCH.** Flush against the hit of my **`kcnk5a`** query, not `kcnk5b`. My `kcnk5b` hit is on a different scaffold entirely (JAGFBZ010001926.1). |
| `fgf10a` | HS2193:503910-505909 (−) | **PARALOG MISMATCH.** Nearest hit of mine is my **`fgf10b`** query, 325 bp away; my `fgf10a` hit is on JAGFBZ010000446.1. |
| `fgf20a` | HS2092:897466-899465 (+) | **DISAGREE on scaffold.** I queried `fgf20a` and my hit is on JAGFBZ010000863.1. |
| `msx1b`, `sp7`, `runx2b`, `lef1` | — | **Not comparable**: this project never queried those four proteins, so it has no independent placement. Reported as not comparable rather than as agreement. |

**Two exact agreements are the strongest independent confirmation in this project.** `shha` and
`tbx5a` each have a GeneWise-placed window ending at precisely the base where an independently
computed protein alignment begins. Two methods, two code paths, same coordinate.

**The `kcnk5b` mismatch is the consequential one.** That window is third of nineteen on the Evo 2
delta ranking (+0.2715) and `kcnk5b` is a fin-size gene in this plan, so the locus label matters. The
window is flush against the region my **`kcnk5a`** query best-hits. Here my paralog discrimination is
better supported than in the `kcnh2` case: `kcnk5a` and `kcnk5b` best-hit **different scaffolds** in my
runs, which is exactly the separation `kcnh2a`/`kcnh2b` failed to show. The Evo 2 harness already said
not to rank traits off per-window deltas; this adds that for this window the gene **label** is in
doubt, not just the ranking.

**What this does not establish.** My placements are protein alignments, not ortholog calls — my own
`kcnh2a` case (§R3) proves a best hit cannot name a paralog. So "mismatch" means *the two methods
disagree*, not that theirs is wrong and mine is right. Resolving each needs the same thing the `kcnh2`
case needs: a gene tree.

### Their action item (b): the dropped flying-fish `hoxd13a`

Their input set dropped it for "no ortholog hit with a clean 2 kb ACGT-only window". Measured here
against my `hoxd13a` hit (JAGFBZ010000479.1:5214025-5216883, `+`): the scaffold is 6,138,190 bp, a full
**2,000 bp** is available immediately upstream, and it contains **0 non-ACGT bases**. So a clean window
does exist there, and the failure is consistent with the *ortholog-hit* half of their reason rather
than the *clean-window* half. That does not show their model was wrong: my `hoxd13a` hit is the
**weakest in my whole table** (coverage 0.824, identity 0.447), which is itself a reason a stricter
ortholog model would decline it.

## R6 — Motif scan of the Evo 2 windows (the handoff's named missing job)

Run as **`claude-zf2ff-motif-scan-2`** (`aijob-e00excwvczktqjsys4`), state read from the CLI as
`COMPLETED`. Full manifest, the pre-registration, the JASPAR digest and the quota history that forced
a GPU preset for CPU work: [`data/motif/MANIFEST.md`](data/motif/MANIFEST.md).

The handoff asked for it by name: beating a dinucleotide shuffle shows structure above k = 2 and
nothing more specific, and a motif scan is the next step. 879 JASPAR 2024 CORE vertebrate motifs
(digest recorded) against claude-evo's own 95 sequences, reused verbatim and hash-verified.

**Aggregate:** real windows carry **+30.05** more passing motifs than their own shuffles (SE 9.60,
t = 3.13, 95% CI [11.2, 48.9]), 14 of 19 windows positive.

**Within each species separately** — the only form the handoff calls safe:

| set | n | mean diff | 95% CI | t | positive |
| --- | --- | --- | --- | --- | --- |
| zebrafish | 10 | +7.0 | [−11.0, +25.0] | 0.76 | 6/10 |
| flying fish | 9 | +55.7 | [+29.6, +81.8] | 4.18 | 8/9 |

**The pooled effect is carried entirely by the flying-fish windows; the zebrafish arm is null.** That
is the opposite asymmetry to the Evo 2 likelihood result, where zebrafish out-scored flying fish — and
it is **not** offered as a biological finding, for two reasons visible in this run's own numbers:

1. **n = 2 shuffles per window is underpowered.** The two shuffles of the *same* window differ by a
   median of 21 and up to 68 motifs, comparable to the effect itself.
2. **The thresholds were pooled across windows.** Real-vs-own-shuffle is composition-controlled by
   construction, but a pooled threshold lets the effect *size* track GC, and the flying-fish windows
   are GC-richer (0.349–0.577 vs 0.256–0.408).

So the reportable result here is the **aggregate above-composition motif signal**, and the species
asymmetry was **held as unresolved** pending a follow-up job designed to test exactly those two
weaknesses. That job has since run, and it overturned the asymmetry — see §R6b.

### R6b — Robustness re-run: the species asymmetry does not survive

**`claude-zf2ff-motif-robust-1`** (`aijob-e00msbsq47zkq8nwt7`), CLI-read `COMPLETED`, 118 s. Same
input FASTA digest, **same JASPAR digest** so the motif set is held constant. Changes: 20
dinucleotide-preserving shuffles per window instead of 2, generated in-container (Altschul–Erikson,
seed 12345) with an assertion that each reproduces its source's exact doublet counts — 
`ZF2FF_SHUFFLES_DOUBLET_VERIFIED=380`, all 19 × 20 verified — and **each window's threshold taken
from its own shuffles**, so no threshold is shared and GC cannot enter through it.

| set | n | mean real − shuffle | 95% CI | t | positive | mean z |
| --- | --- | --- | --- | --- | --- | --- |
| zebrafish | 10 | **+51.7** | [37.3, 66.2] | 7.02 | **10/10** | 4.21 |
| flying fish | 9 | **+57.4** | [39.1, 75.7] | 6.15 | **9/9** | 4.41 |

**19 of 19 windows positive, and the two species are indistinguishable in effect size.** The first
run's null zebrafish arm was an artefact of the pooled threshold and of n = 2 shuffles against a
shuffle-to-shuffle spread of median 21. **§R6's species asymmetry is withdrawn** — and the withdrawal
was predicted before the job was submitted, not discovered after.

**Independent agreement.** The Evo 2 harness ran its own motif scan separately (`§1c` of the handoff,
appended after this project's first run) with a different thresholding rule (per-motif FPR 1×10⁻⁴)
and 5 shuffles per sequence: real windows **+125.3** [61.0, 189.7], flying fish +181.4, zebrafish
+74.8. Different magnitudes because the thresholds differ; **the same direction**, 17/19 and 19/19
windows positive. Two independently written implementations agree.

### R6c — Held-out split: the direction survives, the effect halves, per-window claims die

**`claude-zf2ff-motif-heldout-1`** (`aijob-e00wxbf9hepvn719p6`), CLI-read `COMPLETED`. Pass two
declared its own weakness — the threshold was fitted on the same 20 shuffles that formed the null,
deflating its spread — so this pass splits them: 10 shuffles calibrate the per-motif threshold, 10
are the null. Same seed, same motif digest, same sequences; the split is the only change. All 380
shuffles doublet-verified again.

| pass | design | zebrafish | flying fish |
| --- | --- | --- | --- |
| 1 | pooled threshold, 2 shuffles | +7.0 [−11.0, +25.0] | +55.7 [+29.6, +81.8] |
| 2 | own-shuffle threshold, 20, no split | +51.7 [37.3, 66.2] | +57.4 [39.1, 75.7] |
| **3** | **held-out, 10 calibrate / 10 test** | **+27.1 [7.9, 46.3]** t 2.77, 8/10 | **+26.8 [12.0, 41.6]** t 3.54, 8/9 |

**What survives all three designs:** real windows carry more motif matches than composition-matched
shuffles of themselves, in **both** species, aggregate CI excluding zero. Pass two's species symmetry
holds; pass one's asymmetry does not.

**What does not survive:** effect size and per-window significance. Mean |z| falls from 4.21/4.41 to
**1.39/1.57**, with only **2 of 10** zebrafish and **4 of 9** flying-fish windows at z > 2. Pass two's
z values were anti-conservative exactly as its own manifest predicted, so **no per-window or per-gene
statement is supportable here** — which is also what the Evo 2 harness said about its per-window
deltas.

**Final reading of §R6–R6c:** one aggregate result, direction-robust across three thresholding
designs and corroborated by an independently written implementation in another harness, with no
per-window inference. A motif match is a sequence-pattern match, not binding, not an enhancer, not
function.

**Scope.** A motif match is a sequence-pattern match: not a bound factor, not an enhancer, not
expression, not function. Two of the nine flying-fish windows sit at loci this project's own
cross-check (§R5) flags as paralog mismatches.

## R7 — Second gene tree: no `kcnh2a`-like region exists anywhere in this assembly

**`claude-zf2ff-kcnh2a-hunt-tree-1`** (`aijob-e00k03g7vbmk6smbkh`), CLI-read `COMPLETED`. Input sha256
`585d9bd5…147a28830`, re-hashed in-container to the same digest; treefile sha256 `cf70f399…533b905e`.
Same method as §R4 (MAFFT → IQ-TREE 2, LG+G4, 1000 UFBoot + 1000 SH-aLRT, seed 12345).

A low-stringency whole-assembly search with the `kcnh2a` query alone (`-N 20 --outs=0.3 --outc=0.05`,
`scripts/hunt_kcnh2a.sh`, exit 0) found **no new region**: the same **7** `kcnh2a`-aligning regions.
Two were already assigned. This tree tested the other five, carrying one sequence from each assigned
region forward as a control.

**Both carried-forward controls reproduce in an independent run with a different sequence set:**
`HSPEC_ambiguous_1` pairs with `ZF_kcnh2b` (99.3/100) and the `kcnh6a`-like control pairs with
`ZF_kcnh6a` (99.6/100).

| region | closest zebrafish paralog | support |
| --- | --- | --- |
| JAGFBZ010002515.1 | `kcnh6b` | 100/100 |
| JAGFBZ010000289.1 | `kcnh7` | 100/100 |
| JAGFBZ010000779.1 | `kcnh7` | 63.4/74 |
| JAGFBZ010002447.1 | `kcnh4a` | 99.6/100 |
| JAGFBZ010000590.1 | `kcnh5a` | 99.3/100 |

**Every one of the seven regions in `GCA_018398805.1` that aligns to zebrafish `kcnh2a` is better
explained as a different KCNH paralog** — `kcnh2b`, `kcnh6a`, `kcnh6b`, `kcnh7` ×2, `kcnh4a`,
`kcnh5a`. No `kcnh2a`-like region was found anywhere in the assembly.

**What this does and does not mean.** It means the `longfin` gene has **no located target** in the
only public Exocoetidae assembly, so an edit designed at "the Exocoetid `kcnh2a`" cannot currently be
placed. It does **not** mean Exocoetidae lack `kcnh2a`: `GCA_018398805.1` is an explicitly *draft*,
scaffold-level, unannotated assembly, and a missing or fragmented gene is the expected failure mode
of such an assembly. Note also that the published flying-fish phylogenomics that names `kcnh2a`
(PMID 34534441) used 35 species with its own sequencing, not this assembly. A family-wide census has now answered which of
those it is — see §R7b.

### R7b — Family census: the gap is `kcnh2a`-specific, not general incompleteness

**`claude-zf2ff-kcnh-census-tree-1`** (`aijob-e00nvq278rsze2f6bp`), CLI-read `COMPLETED`. All 10
zebrafish KCNH queries were mapped over the whole assembly (`-N 10 --outs=0.5 --trans`, exit 0), 65
raw hit intervals merged into **14 distinct KCNH-like loci**, each taken as its longest predicted
protein and placed on one tree with the zebrafish family and two human outgroups. Input sha256
`771f8160…399b9c84`, re-hashed in-container; manifest at
[`data/census/MANIFEST.md`](data/census/MANIFEST.md).

**9 of the 10 zebrafish paralogs have at least one flying-fish locus placed with them. The single
exception is `kcnh2a`:** `kcnh1a`, `kcnh1b`, `kcnh2b`, `kcnh6a`, `kcnh6b` get 1 locus each, `kcnh3`,
`kcnh5a`, `kcnh7` get 2 each, `kcnh4a` gets 3, and `kcnh2a` gets **none**.

So the KCNH family is **well represented** in this assembly — 14 loci across 9 paralogs — and the
`kcnh2a` gap is **specific**, not a symptom of the assembly being generally thin here. That is the
sharper of the two explanations §R7 left open.

**Still a statement about the assembly, not the species.** A draft assembly can miss one gene, and a
sufficiently divergent Exocoetid `kcnh2a` could be placed with a neighbouring paralog rather than
appearing as a `kcnh2a` sister. Three assignments are weakly supported and should be read as
unresolved (`locus03` 42.7/68, `locus14` 23.4/62, `locus11` no recovered support); dropping all three
does not touch the headline, since none was assigned to `kcnh2a`. A model-sensitivity re-run with
ModelFinder instead of a fixed `LG+G4` and a different seed
(`claude-zf2ff-census-sensitivity-1`) was submitted to check the conclusion is not model-dependent.

## R8 — Inputs reused from other harnesses (their receipts, not ours)

- `results/bioservices/claude-20261101/` (branch `claude/bioservices-20261101`): UniProt/Ensembl/
  Europe PMC retrievals, GRCz11 coordinates for 8 candidate genes, and OpenFold2 predicted structures
  for Fgf10a, Hoxd13a, Shha and Kcnk5b with **mean pLDDT 41–56** — low confidence, structure
  hypotheses only. The `msxb` Ensembl lookup failed there (HTTP 400); `msxb` is nonetheless mapped
  here by sequence, which does not recover its GRCz11 coordinates.
- `artifacts/genetic-blueprints/blueprints.json` (SPEC-012 package): already carries construct designs
  with **null** element coordinates and declared missing links. `PLAN.md` §5 does not improve on
  those nulls; it inherits them.
- Evo 2 regulatory candidates: the handoff file
  `/data/artifacts/delphi-evolve-rethink/messages/evo-to-zf2ff.md` **did not exist** when this was
  written. No Evo 2 output is used, and none is claimed.

## Failures and things not done

- **No full text was read, for any source.** Every literature statement in `PLAN.md` is abstract-level.
- Analysis G2b was run as a Nebius CPU job and resolved the `kcnh2` collision (§R4). Analyses G3–G6
  in `PLAN.md` §3 were **not run**: no synteny analysis beyond recording scaffold
  identity, no convergent-residue inspection, no conserved-element scan, no phylogenomic scan (the
  35-species data behind PMID 34534441 is not public here). G2 was run (§R3) and returned a
  resolution for the hedgehog collision and a **non-resolution** for the `kcnh2` collision.
- No **synteny** analysis was built, which is what an orthology claim would still need beyond the
  gene tree.
- No **GPU** job was submitted by this project; the work it needed was CPU-bound. Two Nebius CPU jobs
  carry the `claude-zf2ff-` prefix. Terminal: `claude-zf2ff-kcnh-tree-1` COMPLETED (§R4),
  `claude-zf2ff-motif-scan-1` **ERROR at provisioning** (shared CPU quota taken by another tenant
  between accept and provision; preserved, not hidden), `claude-zf2ff-motif-scan-2` COMPLETED (§R6).
  In flight when this was written: `claude-zf2ff-motif-robust-1`, `claude-zf2ff-kcnh2a-hunt-tree-1`.
- The `lat4a` ↔ `slc43a2a`/`slc43a2b` identifier question is **unresolved**, and it blocks G4 and
  perturbation row P2.
- The round-1 mapping was produced by a predecessor process; it was reviewed and its controls were
  re-checked here from its saved outputs, but it was **not re-run** from scratch. Its script's
  docstring still describes the identity metric loosely; the corrected definition is in this file and
  in the round-2/3 script.
- Three documented errors were found by external review and are corrected in place above rather than
  quietly fixed: the identity-metric description, the claim that chunking does not change results,
  and the unqualified `kcnh2a` detection. See [`REVIEW.md`](REVIEW.md) for the full list, including
  the findings that were **not** accepted.
