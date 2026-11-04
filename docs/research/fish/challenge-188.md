# Challenge 188 — adversarial review of the S1-D-D Hi-C intact-allele claim

**Verdict: SURVIVED, with one stated fragility.** The arithmetic reproduces. The read
count, the individual and the BioSample all check out. The *direction* of the result
("strengthens") holds under every relaxation I tried. The *quantitative* bounds (P(0)
0.003-0.015, intact fraction ≤ 0.26-0.36) hold only if coverage is Poisson. I could not
measure overdispersion, so I record that as a fragility rather than a refutation.

## The claim under review (the author's, not mine)

> Exon 21 occurs in 0 of 116,889,460 Hi-C reads of the same BioSample, while the flanking
> single-copy sequence and the deletion junction are present. Expected 5.9 reads if
> heterozygous, 11.7 if intact. Calculated P(0) 0.003-0.015. 95% upper bound on the
> intact-allele fraction ~0.26 (pooled controls) to ~0.36 (worst control). Strengthens.

Source `harvest:s1-d-sensitive-input-4x930e`. **Read-level: could-not-access.** That
harvest's working is not in this repository on any branch (I ran `git grep` for "hi-c",
"116889460" and "s1-d" across all refs: no hits). So I could not see the author's control
windows, their counts, or their exact matching method. Everything below is checked against
public records and my own arithmetic.

## 1. Inputs I verified independently (observed, from public records)

- **The read count is right.** The ENA `filereport` for BioSample SAMN26927110 (read-level:
  full record) lists `SRR18578620`: Hi-C, Illumina NovaSeq 6000, PAIRED, 58,444,730 spots,
  17,533,419,000 bases. 2 × 58,444,730 = **116,889,460 reads**, and 17,533,419,000 /
  116,889,460 = **150 bp per read**. "Reads" here means mates, not pairs.
- **The sample is the same fish.** The Hi-C run and the HiFi run `SRR18578621`
  (Sequel II, 2,625,605 reads, 45,492,493,992 bases) share BioSample SAMN26927110, with
  sample alias `AstMex_cave_lab_molino_female`. The EBI BioSamples record (read-level:
  full record) gives `isolate: ESR-SI-002`, `ecotype: Molino cave`, `sex: female`,
  `tissue: muscle`, and `biomaterial provider: Stowers Institute`. One isolate means the
  claim's "same BioSample" is also the same individual, as far as metadata can say.
- **There is no alternate-haplotype assembly to check instead.** An NCBI Assembly esearch
  for SAMN26927110 returns one assembly, GCA_023375845.1 `AstMex3_Molino`,
  `assemblytype: haploid`. So the reads are the only way to test heterozygosity, as the
  claim says.
- **The exon is the right one.** I fetched NC_064412.1:18,464,523-18,464,627 with NCBI
  efetch. It is 105 bp, and its plus-strand sequence ends `…CCGCCTCTGGCACAGC`, which
  contains the TALEN1-right oligo that the S1 result (`results/2026-10-31-oca2-exon21-molino-RESULT.md`
  line 236) places inside exon 21.

**Not verified: the zero itself.** I tried to recount the reads myself, and every route
failed:

- ENA FTP: DNS failure over HTTP, and HTTPS was refused by the proxy.
- NCBI `trace` and `ftp-trace`: refused by the proxy.
- The AWS copy (`sra-pub-run-odp`, 7,385,190,173 bytes) downloads at about 20 MB/s, but
  it is in SRA format, and sra-tools is not installed and cannot be fetched.

So the count of 0 is the author's measurement, and I have not reproduced it.

## 2. Arithmetic, redone from the stated inputs (calculated)

- **P(0) for a heterozygote, Poisson:** e^-5.85 = **0.0029**. For the worst control (an
  intact expectation of 8.32, so 4.16 for a heterozygote), e^-4.16 = **0.0156**. Both
  match the stated 0.003-0.015.
- **95% upper bound on the intact fraction, given 0 reads:** the Poisson bound is
  −ln 0.05 = 2.996 reads. 2.996 / 11.7 = **0.256**, and 2.996 / 8.32 = **0.360**. Both
  match the stated 0.26 and 0.36.
- **A cross-check from first principles.** I assumed reads start uniformly over a diploid
  1,361,196,561 bp genome, and counted reads of 150 bp that hold at least one complete
  24-mer of the 105 bp exon (150 + 105 − 48 + 1 = 208 start positions). That gives
  116,889,460 / (2 × 1.361e9) × 208 = **8.9 reads per allele**, which means 17.9 if
  intact and 8.9 if heterozygous. The author's empirical 11.7 and 5.9 are lower than
  this. Calibrating against flanking controls rather than uniform theory therefore
  *understates* the expected count, which makes the claim conservative here, not
  inflated.

The arithmetic survives.

## 3. Proxy check

The question is whether this fish carries an intact exon-21 allele. Hi-C reads are a
legitimate proxy for that, because they are a whole-genome library from the same isolate.
But **a better direct measurement exists and was not used**: the HiFi run from the same
BioSample. It has about 45.5 Gb, roughly 33× haploid coverage at ~17 kb mean read length
(both calculated from the ENA listing). A HiFi read spans the whole ~4.6 kb deletion, so
it would type each allele directly, as deleted or intact. That would remove the
coverage-model dependence described in section 4.

This is a missed opportunity, not a defect. The Hi-C proxy measures the right quantity.

## 4. The hidden assumption that carries the numbers: Poisson coverage

P(0) and the upper bounds assume the count at exon 21 is Poisson with a mean taken from
the controls. Hi-C coverage is known to be uneven at the scale of a few hundred bp,
because of restriction-site proximity and GC/PCR bias. Here is what I could check
(observed, from the efetch sequence):

- **GC content.** Exon 21 is **61% GC**. The ±1 kb around it is **39% GC**. If the
  author's flanking controls are typical of the locus, the test window is GC-richer than
  its controls. Illumina PCR-amplified libraries often under-cover GC-rich windows. That
  would push the true expectation below 5.9, which inflates the stated significance. I
  cannot quantify this without the reads or the controls' sequences: **unknown**.
- **Restriction sites.** GATC sites lie 142 bp and 60 bp upstream of the exon. If the
  library used a GATC-cutting enzyme (DpnII/MboI/Arima), reads are enriched near those
  sites, which would favour coverage of exon 21. The enzyme is not stated in the ENA
  fields I retrieved: **unknown**. These two biases may partly offset.

**Relaxing the assumption (calculated, negative binomial with dispersion k):**

| k (lower = more overdispersed) | P(0 \| het, mean 5.85) | P(0 \| het, mean 4.16) | 95% bound on intact fraction (pooled / worst) |
|---|---|---|---|
| Poisson (∞) | 0.003 | 0.016 | 0.26 / 0.36 |
| 10 | 0.010 | 0.031 | 0.30 / 0.42 |
| 5 | 0.021 | 0.048 | 0.35 / 0.49 |
| 2 | 0.065 | 0.105 | 0.59 / 0.83 |

My inference from the table:

- At moderate overdispersion (k ≥ 5), a heterozygote is still disfavoured at about the
  5% level.
- At strong overdispersion (k ≈ 2), the 95% bound no longer excludes a fraction of 0.5.
- Even at k = 2, 0 reads against an expected 5.85 is a likelihood ratio of about 15:1
  for "no intact allele" over "heterozygous". So the claim's verdict word,
  "strengthens", survives every k I tried. What does not survive strong overdispersion is
  the precision of "0.003-0.015" and "0.26-0.36".

I have no measurement of k for this library. The author's own pooled-versus-worst spread
(11.7 vs 8.32, a factor of 1.4) shows that control-to-control variation exists. But with
the number of controls unknown, it does not pin k down. **I do not claim k is small.** I
claim that the quoted bounds are conditional on Poisson, and that the claim does not say
so.

## 5. Is the evidence level honest?

The claim records "measured". In my reading:

- **Measured:** the read total (verified above), and the zero (not reproduced by me).
- **Calculated:** the expectations 5.9 and 11.7, P(0), and the 0.26/0.36 bounds.

The claim labels P(0) as "calculated" in its own sentence, and the recorded value is
"n/a". The bounds are not labelled. That is a minor labelling gap, not a misrepresented
number.

## 6. Missed regimes or counter-examples

- **Scope.** This tests one lab-reared female, isolate ESR-SI-002, from Stowers. It says
  nothing new about wild Molino fish. The wild-population claim rests on Warren et al.
  2021, which reports n = 9 with all lacking exon 21, as quoted in the S1 result. The
  claim does not overstate this; it speaks of "the same BioSample".
- **Diverged intact allele.** Exact 24-mer matching would miss an intact allele carrying
  a substitution every <24 bp across all 105 bp. No such allele is reported in the
  sources the S1 result quotes. Warren 2021 reports *smaller deletions* in exon 21 in
  Pachón, Río Choy and Tinaja, not diverged copies. **Scope of that negative:** only the
  passages quoted in the S1 result. I did not do a fresh literature search.
- I found no published counter-example of a heterozygous intact exon-21 allele in a
  Molino laboratory fish. **Scope:** I did not run a literature search. This rests only
  on the sources already quoted in the S1 result.

## Bottom line

I could not break the claim's arithmetic, its sample identity or its direction. Its
quantitative bounds rest on an unstated Poisson assumption. That assumption is
untested, and it may be biased by the exon's 61% GC against a 39% GC neighbourhood.
Under strong overdispersion, the bounds widen enough to admit a heterozygote, though the
likelihood still favours absence. The cheapest decisive fix is to type the ~4.6 kb
deletion in the 33× HiFi reads from the same BioSample.

```swarm-challenge
{"claim_id": 188, "outcome": "survived", "reason": "Read total (2x58,444,730 = 116,889,460, SRR18578620), same isolate ESR-SI-002, and the P(0)/upper-bound arithmetic all reproduce, and the 'strengthens' direction holds under negative-binomial relaxation, though the quoted bounds are Poisson-conditional (at dispersion k=2 the 95% bound widens to 0.59-0.83) and the zero count itself could not be re-measured here.", "corrected_value": null, "depends_on": ["author-reported exon-21 read count = 0 in SRR18578620 (not reproduced; harvest s1-d-sensitive-input-4x930e not accessible)", "author-reported control-derived expectations 11.7 (pooled) and 8.32 (worst) intact-allele reads", "ENA filereport SRR18578620: 58,444,730 spots, 17,533,419,000 bases, BioSample SAMN26927110", "EBI BioSamples SAMN26927110: isolate ESR-SI-002, Molino cave, female", "NC_064412.1:18,464,523-18,464,627 as oca2 exon 21 (105 bp, 61% GC) per results/2026-10-31-oca2-exon21-molino-RESULT.md", "Poisson coverage model (relaxed via negative binomial in section 4)"]}
```
