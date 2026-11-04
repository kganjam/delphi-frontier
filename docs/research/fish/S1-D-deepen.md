# S1-D-D: deepening the oca2 exon-21 Molino result by attacking its weakest input

**Verdict: STRENGTHENS.** The answer S1 rests on is "oca2 exon 21 is absent from the
Molino cavefish". The input it was most sensitive to was not a parameter of the k-mer
method. It was an unexamined proxy: *absent from a haploid assembly* was standing in for
*absent from the fish*. I measured the real quantity in the raw reads of the same
BioSample. Exon 21 is in **0 of 116,889,460 reads**, while single-copy flanking controls
are found at the expected depth.

---

## 0. Which answer this deepens, and one gap in the task

The task text names S1-D (organism) and says "The recorded answer:" but gives nothing
after it. The answer text was **not supplied**. I found no file in this repository named
S1, and `docs/research/fish/` did not exist before this commit (search scope: every
tracked file on branch `claude/s1-d-sensitive-input-4x930e` and `work/frontier-foundation`,
grepping for `S1`, `S1-`, `swarm-result`, `organism`). The only fish/organism answer in
the repository is

- `results/2026-10-31-oca2-exon21-molino-RESULT.md` (read-level: **full-text**, repository file).

I deepen that answer. If S1 meant something else, this document does not deepen it.

Its conclusions, in its own words:

- **C1 (preregistered, the headline).** "oca2 exon 21 is absent from the entire Molino
  assembly" (GCA_023375845.1, 1,361,196,561 bp), flanks intact, with a ~4.6 kb deletion.
  It reproduces Warren et al. 2021: "exon 21 of oca2 is absent in all Molino cavefish
  samples (n = 9)".
- **C2 (post-hoc, labelled "suggestive").** The deletion "tracks albinism rather than
  cave-dwelling", based on Tinaja (brown, per a review) carrying all 24 exons.

## 1. Which input is the answer most sensitive to? (recomputed, not asserted)

I list the candidates and recompute each one. Every probability in this section is
**calculated** under a stated model. None of them is observed.

### 1a. Per-base divergence *d* between Molino and surface: NOT the weak input

C1 reads 0/82 exact 24-mers as "deleted". The alternative explanation is that the exon is
present but so diverged that every 24-mer window carries a mismatch. S1 *asserted* that
divergence is low. It did not quantify how low *d* would have to be.

*Measured d (this work, observed):* across the Molino exon-22-to-exon-20 interval
(11,513 bp of Molino sequence, CM041831.1:19,325,244-19,336,816 region, fetched by
NCBI efetch), 53 clusters of Molino-specific 24-mers have the ≥15-k-mer signature of a
single substitution or small indel. That gives **d̂ ≈ 0.0046 per bp**. This is an
over-estimate of substitution divergence, because indel clusters are counted too. In
intron it is plausibly an over-estimate for exons as well. S1's own exon table agrees:
the lowest present-exon value in Molino is 0.793.

*Sensitivity (calculated, exact dynamic programme over a 105 bp exon, i.i.d. mismatches):*

| d (per bp) | P(0 of 82 windows survive \| exon present) | expected surviving fraction |
|---|---|---|
| 0.0046 (measured) | 2.5 × 10⁻⁶ | 0.895 |
| 0.0092 (×2) | 5.3 × 10⁻⁵ | 0.801 |
| 0.0184 (×4) | 1.1 × 10⁻³ | 0.640 |
| 0.0477 | 0.05 | 0.31 |
| 0.10 | 0.41 | 0.08 |

Doubling *d* does not move the conclusion. It takes a **~10× error** (d ≈ 0.048) before
divergence explains a zero even 5% of the time. Divergence is robust and is not the answer
to "most sensitive input".

### 1b. N-gap: not the weak input

S1 measured 0 N in the interval, and the nearest gap was 994 kb away, with a counter that
had a working positive control. This does not move under a factor of two, because 0 × 2 = 0.

### 1c. Intact-allele dosage in the source individual: THE weak input

The assembly is `assembly_type: haploid` (S1 §10). A haploid assembly emits **one**
sequence per locus. Now suppose the fish were heterozygous (one intact allele, one
deleted). The assembler can output the deleted haplotype, and the 24-mer scan of the
assembly would then return **exactly the same 0/82**.

*Recomputation:* let *f* be the fraction of the individual's chromosomes 5 that carry
exon 21. S1's observable (0/82 in the assembly) is the same for f = 0 and f = 0.5. The
measurement has **zero sensitivity** to the input that decides the biological reading.
"The Molino fish lacks exon 21" requires f = 0. At f = 0.5 the sentence is false for this
fish, and the deletion becomes a heterozygous allele in one individual. That changes the
conclusion completely (a change from 0 to 0.5, not a factor of two, but a larger move).
S1 itself flagged this ("I cannot distinguish homozygous from heterozygous from an
assembly"), and then did not act on it.

**So the most sensitive input is *f*, the intact-allele fraction in the sequenced
individual. S1 implicitly took it to be 0.**

## 2. How well was *f* established before this work?

- **Evidence level: assumption.** It was never measured on this individual. "Absent from
  the assembly" is a **proxy** for it, and the proxy cannot tell the two cases apart.
- Supporting literature: Warren et al. 2021, PMC7933363 (**read-level: full-text**, as
  recorded in S1. I did not re-open it). The authors claim exon 21 is "absent in all
  Molino cavefish samples (n = 9)" from wild-caught short-read data aligned to the surface
  reference. That is a claim about *other* fish. Its per-sample evidence (Supplementary
  Fig. 8) is **could-not-access** (per S1, not re-tried). So the homozygous call in those
  nine fish is the authors' claim and is not checked here.
- *My inference, not a sourced fact:* "recessive albinism needs homozygous loss" is
  background genetics knowledge. I have not retrieved a source for the recessivity of the
  Molino oca2 allele in this session. I list it as a dependency and do not rest the
  verdict on it.

## 3. Improving it: measure *f* directly in the raw reads

**Primary data.** ENA filereport for BioSample SAMN26927110 (**read-level: full record**)
lists three runs under the same BioSample as the assembly: SRR18578621 (PacBio, 45.5 Gb),
SRR20281239 (PacBio, 0 reads listed), and **SRR18578620 (Illumina Hi-C, paired, 58,444,730
spots, 17,533,419,000 bases)**. The BioSample record (NCBI efetch, **full record**) reads:
`isolate="ESR-SI-002"`, `ecotype="Molino cave"`, female, muscle, provider Stowers
Institute.

I chose Hi-C Illumina over PacBio subreads. With ~10-15% raw error, exact 24-mers survive
in PacBio subreads at only ~3-4% (calculated: 0.87²⁴ ≈ 0.035), so PacBio is a poor
exact-match substrate. Hi-C reads are ordinary genomic reads with chimeric junctions. A
read only has to contain one 24-mer to count.

**Access.** EBI FTP (`ftp.sra.ebi.ac.uk`) was refused by this environment's egress proxy.
NCBI `trace`/`sra-download` hosts were also refused. I downloaded the run from the AWS
open-data mirror (`sra-pub-run-odp.s3.amazonaws.com`, 7,385,190,173 bytes, matching
Content-Length) and decoded it with bioconda `sra-tools` 3.4.1 `fastq-dump --split-spot`.
fastq-dump reported "Read 58444730 spots / Written 58444730 spots". An independent awk
tally gave **116,889,460 reads, 17,533,419,000 bases, equal to ENA's `base_count` to the
base**. Every read was scanned. This is not a subsample.

**Probe sets.** All are exact 24-mers, both strands, built from the sequences named:

| label | source | 24-mers | purpose |
|---|---|---|---|
| E21 | surface exon 21, NC_064412.1:18,464,523-18,464,627 | 82 | **the test**: intact allele |
| JUNC | Molino 24-mers spanning the deletion junction (Molino window 21,060-21,130), each verified absent from the 184 kb surface oca2 locus | 22 | deleted allele |
| E20, E22 | surface exons 20 and 22 | 37, 71 | single-copy positive controls, shared by both alleles |
| FL_L | 105 bp shared by surface and Molino, ~180 bp from the junction (Molino window 20,890) | 82 | positive control, shared |
| FL_R | 105 bp shared, Molino window 21,130 | 82 | intended positive control (**failed**, see below) |
| DECOY21 | shuffled exon 21, verified absent from surface locus and Molino window | 82 | must-fail |

The junction was re-derived here independently of S1. A unique-anchor offset profile
shows a **4,588 bp** jump between surface 18,464,458 and 18,469,069. That is the same
value and interval S1 reports.

**Result (observed).** Distinct read sequences containing ≥1 probe 24-mer:

| label | reads | locus check |
|---|---|---|
| **E21** | **0** | n/a |
| **DECOY21** | **0** | n/a |
| E20 | 11 | all 11 share 43-100% of their 24-mers with the Molino locus window |
| E22 | 8 | all 8 share 34-100% |
| JUNC | 7 | all 7 share 48-99% |
| FL_L | 20 raw → **13 on-locus** | 7 reads hit by a single k-mer and share 1% with the locus, so they are off-target |
| FL_R | 8,185 | **control failed**: lies in a genomic repeat (single k-mers seen >1,000 times) |

Two things went wrong with my controls, and both are reported:

- **FL_R was a bad control.** I chose it without a genome-wide uniqueness check, and it
  falls in a repeat. It is excluded from every calculation below. It does not touch E21.
- **The FL_L on-locus filter (≥ ~0.3 of read k-mers in the locus window) was applied
  post-hoc.** It *lowers* the control count from 20 to 13, which lowers the expected E21
  count and can only weaken the test. It cannot manufacture the zero.

**Expected E21 count if an intact allele were present (calculated).** Read starts per bp
= 116,889,460 / 1,361,196,561 = 0.0859. A 105 bp target with 150 bp reads is hit by
reads starting in a (82 + 126) = 208 bp window, so uniform-coverage expectation is
17.9 reads. The single-copy controls came in at observed/expected = (11 + 8 + 13) /
(14.0 + 16.9 + 17.9) = **0.656**. Hi-C coverage is non-uniform, so I also give the most
pessimistic single control (E22: 8 / 16.9 = 0.473).

| hypothesis for *f* | λ (pooled controls) | Poisson P(0 reads) | λ (worst control) | P(0) |
|---|---|---|---|---|
| f = 1 (exon present, homozygous) | 11.7 | 8 × 10⁻⁶ | 8.5 | 2 × 10⁻⁴ |
| **f = 0.5 (heterozygous)** | **5.9** | **2.8 × 10⁻³** | **4.2** | **1.5 × 10⁻²** |
| f = 0.25 | 2.9 | 5 × 10⁻² | 2.1 | 0.12 |
| f = 0.10 | 1.2 | 0.31 | 0.85 | 0.43 |

These probabilities are **calculated** from a Poisson model. Hi-C read counts are
over-dispersed, which is why the worst-control column is there. Even so, a heterozygous
intact allele is disfavoured at P ≈ 0.003 (pooled) to 0.015 (worst case). The deleted
allele is directly **observed** in 7 junction-spanning reads (expected under homozygous
deletion: 22 + 126 = 148 bp window × 0.0859 × 0.656 ≈ 8.3; under heterozygosity ≈ 4.2).
Seven does not discriminate between those two by itself. The E21 zero is what does.

**Improved input: f = 0 observed (0 / 116,889,460 reads). The 95% upper bound on the
intact-allele fraction is ≈ 0.26 with pooled controls and ≈ 0.36 with the worst control**
(calculated as −ln 0.05 / λ(f = 1)). Heterozygosity (f = 0.5) is excluded at the levels
above. A low-level intact fraction (mosaicism, contamination, ≲ 25%) is **not** excluded
by this depth.

## 4. Recompute the original conclusion

- **C1: STRENGTHENS.** Before, it read: "exon 21 is absent from a haploid assembly of one
  Molino fish". Now it reads: "exon 21 is absent from that assembly **and** from all
  116,889,460 Illumina reads of the same BioSample, while flanking single-copy sequence and
  the deletion junction are present in those reads". The haploid-collapse alternative
  (a heterozygous fish) is now disfavoured at P ≈ 0.003-0.015 (calculated). The
  divergence alternative needs a ~10× error in *d* (calculated). The assembly-gap
  alternative was already closed by S1.
- **C2 (tracks albinism, not cave-dwelling): UNCHANGED.** This work tested nothing in
  Tinaja and nothing about phenotype. C2 still rests on a review's population-level
  description (Jeffery 2020, PMC7353729, full-text per S1), n = 1 per population, and was
  post-hoc. Its weakest input, the pigment phenotype of the specific sequenced Tinaja and
  Molino individuals, remains **unmeasured**. The BioSample records ecotype, sex and tissue
  but not pigment (Molino record checked here; Tinaja per S1). What would settle it: the
  Stowers Institute husbandry record or photographs for isolates ESR-SI-002 and the
  Tinaja isolate, at essentially zero cost if the provider will share them. Failing that,
  a melanin/L-DOPA assay on the same lab lines.

## 5. Scope of the negatives

- **"0 E21 reads"** is scoped to SRR18578620, every read of it, exact 24-mers, both
  strands. The PacBio run SRR18578621 was **not** searched. An exon-21-bearing read with a
  sequencing error in every 24-window would be missed, which is negligible at Illumina
  error rates (calculated, same DP as §1a).
- **Same individual.** The Hi-C run and the assembly share BioSample SAMN26927110 /
  isolate ESR-SI-002. I infer that they come from the same fish. That is not recorded as
  fact, and pooled tissue from several fish under one BioSample is not ruled out by the
  record.
- **FL_R** is excluded as a failed control. No genome-wide uniqueness check was run on any
  probe except E21 and DECOY21, which S1 already showed have 0 hits in the whole Molino
  assembly.
- Nothing here bears on wild Molino frequency (Warren's 9/9), on Pachón exon 24, on
  expression, or on causation.

## 6. Reproduction

Accessions: surface locus NC_064412.1:18,405,444-18,589,784 (efetch GenBank, 283,632
bytes, matching S1); Molino window CM041831.1:19,315,000-19,345,000 (efetch FASTA);
reads SRR18578620 from `https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR18578620/SRR18578620`.

```sh
fastq-dump --stdout --split-spot --skip-technical -Z SRR18578620.sra \
  | LC_ALL=C grep -F -f pats.txt > hits.txt      # pats.txt: all probe 24-mers, both strands
# then per-read labelling (distinct sequences), locus-window check, Poisson expectations
```

The scripts (`locus.py`, `junction.py`, `probes.py`, `sens.py`, `count.py`, `verify.py`)
lived in session scratch and will not persist. The accessions and the probe definitions
in §3 reconstruct them.

```swarm-result
{"subproblem": "S1-D-D", "evidence": "measured (raw reads of the same BioSample, every read scanned); significance values calculated",
  "answer": "The S1 conclusion that Molino cavefish lack oca2 exon 21 was most sensitive to the unmeasured intact-allele fraction hidden by a haploid assembly; measured directly, exon 21 occurs in 0 of 116,889,460 Hi-C reads of the same BioSample while flanking single-copy sequence and the deletion junction are present, so a heterozygous intact allele is disfavoured (calculated P(0) 0.003-0.015) and the conclusion strengthens.",
  "key_number": "intact-allele (exon-21) read count = 0 of 116,889,460 reads (expected 5.9 if heterozygous, 11.7 if intact); 95% upper bound on intact-allele fraction ~0.26 (pooled controls) to ~0.36 (worst control)",
  "verdict": "strengthens",
  "depends_on": [
    "results/2026-10-31-oca2-exon21-molino-RESULT.md: exon 21 absent from whole AstMex3_Molino assembly GCA_023375845.1 (0 hits, 1,361,196,561 bp)",
    "exon numbering: RefSeq NM_001320209.1 exon 21 = literature exon 21 (validated in S1 by Ma et al. 2015 TALEN oligos, PMC4361574)",
    "surface exon 21 sequence NC_064412.1:18,464,523-18,464,627 (105 bp)",
    "Molino deletion junction at surface 18,464,458 / 18,469,069 (4,588 bp jump, re-derived here)",
    "SRR18578620 is from BioSample SAMN26927110 (ENA filereport) and from the same individual as the assembly (inference from shared BioSample/isolate ESR-SI-002, not recorded fact)",
    "SRR18578620 read total 116,889,460 reads / 17,533,419,000 bases (matches ENA base_count)",
    "single-copy controls E20=11, E22=8, FL_L=13 on-locus reads; observed/expected 0.656",
    "post-hoc FL_L on-locus filter (only weakens the test)",
    "FL_R control excluded as repetitive",
    "Poisson coverage model for Hi-C reads (over-dispersion handled only via worst-control bound)",
    "genome size 1,361,196,561 bp used for per-bp read-start rate",
    "measured Molino-surface divergence d ~0.0046/bp over 11,513 bp of oca2 intron",
    "i.i.d. mismatch model for the divergence sensitivity calculation",
    "Warren et al. 2021 PMC7933363 claim: exon 21 absent in all Molino samples n=9 (authors' claim; Supp. Fig. 8 could-not-access)",
    "background knowledge (unsourced here): Molino albinism is recessive, so homozygous loss is the biologically relevant state",
    "C2 inputs unchanged: Jeffery 2020 PMC7353729 Tinaja brown / Molino albino (review, population-level); n=1 per population"
  ]}
```
