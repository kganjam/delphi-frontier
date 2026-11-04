# Replication of claim 281: flying-fish fin proportions in zebrafish ("enlarger plus suppressor")

**Type of result:** independent re-derivation. **What it rests on:** reading the primary paper's allele descriptions. No new experiment or simulation was run. Every count below is something I **inferred** by tallying the alleles the authors describe. None is a measurement I made.

## 0. Scope and honesty notes

- **The question was truncated.** It reached me as: *"MECHANISTICALLY THIS IS ENLARGER PLUS SUPPRESSOR, not uniform enlargement. That is why the published result is about fin PROPORTIONS rather than fin size, and i…"*, with the number removed. I could not see what quantity was being asked for. I took it to be **the minimal genetic recipe**: how many loci, how many mutant allele copies, and of what kind (gain- or loss-of-function), are needed to turn zebrafish fin proportions into flying-fish proportions. That fits the hint "inference from the allele descriptions". If the original claim asked for a different quantity, this replication may not address it.
- **No prior working seen.** I searched the repository on every local and remote branch for `enlarger`, `fin proportion`, `flying fish`, `kcnh2a`, `kcnk5b` and `longfin`. There were no hits apart from unrelated triage text in `findings/gemini-triage-267-problems.json`, which I did not use. I did not search GitHub issues or PRs.
- **Identifying the paper.** I matched the paper from the question's wording (enlarger, suppressor, proportions rather than size). The match is my inference, but the paper's own abstract uses "fin proportion" and its Figure 4 legend uses "suppressor of overgrowth".

## 1. Sources

| # | Source | Read-level |
|---|---|---|
| S1 | Daane JM, … Harris MP. *Modulation of bioelectric cues in the evolution of flying fishes.* Curr Biol 31(22):5052–5061.e8 (2021). PMID 34534441, PMC9172250 | **full-text** (author manuscript XML via NCBI E-utilities `efetch db=pmc id=9172250`) |
| S2 | Europe PMC record for PMID 34534441 | abstract |
| S3 | ZFIN pages ZDB-PUB-210918-31 and ZDB-FIG-221222-35 | search-summary only. zfin.org returned HTTP 503 and crick.zfin.org did not resolve, so I **could not access** them. NOAA repository: could-not-access (DNS) |

## 2. Inputs, with the allele descriptions quoted from S1 (full text)

**Enlarger: `kcnh2a` *lof^dt2^* ("longfin")**
- S1: *"The dominant longfin mutant (lof dt2) … coordinated overgrowth of all fins … dose sensitive such that homozygous fish have larger fins."*
- Lesion: *"an inversion on chromosome 2 in lof with break points between 5′ prrx1a and 5′ kcnh2a without affecting the coding region of either gene."* kcnh2a is upregulated in fins. Ectopic hKCNH2 is sufficient to cause local ray overgrowth.
- Type: **gain-of-function** (regulatory/cis-ectopic). The authors infer this from the fact that loss-of-function kcnh2a alleles in cis revert the phenotype: lfr1 Y669N, lfr2 L739Q, WL4, WL7 Y418X, and the γ-ray deletion j6g1.

**Suppressor: `lat4a` *nr21* (allele designation dmh26)**
- S1: *"We identified a dominant mutant, nr21, as having small adult fins."* The lesion is the missense *"T200K in a conserved domain"* of the L-type amino acid transporter Lat4a.
- Type: **gain-of-function**. Frameshifts in cis revert nr21 to wild type. *"zebrafish lacking lat4a have no fin phenotype"* (null allele lat4a^del^, mh152).

**The interaction (authors' claim, S1):**
> "double mutants between kcnh2a lof/+ and lat4a nr21/+ are viable and show specific, non-additive variation in proportion among fins: while all fins of kcnh2a lof/+ are overgrown and all fins of lat4a nr21/+ are shortened, the lat4a nr21/+; kcnh2a lof/+ fish show wild-type-sized medial fins, while the paired fins are overgrown … Thus, lat4a nr21/+ is a medial fin suppressor of kcnh2a lof/+ … the caudal fin … is hypocercal, with an elongated ventral lobe."

The authors also report that, by qRT-PCR, nr21 does **not** change kcnh2a expression in pectoral or dorsal fins. They conclude that the suppression acts *"downstream of bioelectric signaling."*

## 3. Derivation (counting is my inference)

| Quantity | Tally | Value |
|---|---|---|
| Loci | kcnh2a + lat4a | **2** |
| Mutant allele copies in the phenocopy genotype | lof/+ (1 copy) + nr21/+ (1 copy) | **2** (a double heterozygote, "trans-heterozygote" in the Figure 4 legend) |
| Gain-of-function alleles among them | lof (cis-ectopic expression, GOF) + nr21 (T200K, GOF) | **2 of 2** |
| Loss-of-function alleles needed | lat4a null has no fin phenotype; kcnh2a LOF reverts lof | **0** |
| Homozygosity needed | both heterozygous | **0** loci |
| Fin-type outcome | paired fins: enlarger wins (overgrown). Medial fins: suppressor cancels enlarger (about wild-type size). Caudal fin: about wild-type size but hypocercal | no single size change. What changes is the **ratio** of paired-fin to medial-fin size |

**Result:** the flying-fish proportion phenocopy is **1 dominant gain-of-function enlarger plus 1 dominant gain-of-function suppressor at 2 loci, each heterozygous: 2 mutant allele copies, 0 loss-of-function**.

Why this explains "proportions rather than size": the enlarger alone (lof/+) grows **all** fins, which is uniform enlargement. The suppressor alone (nr21/+) shrinks **all** fins. Only in combination does suppression act on the medial fins while the paired fins stay overgrown. So the published phenotype is a change in relative size between fin types, not an absolute size change. This interpretation is mine, but it follows the authors' own wording ("non-additive", "fin-type-specific regulation of size").

**Uncertainty and caveats**
- The counts (2 loci, 2 copies, both GOF) are exact **given S1's allele descriptions**. The main uncertainty is whether I picked the quantity the truncated question asked for.
- **Quantitative fin lengths are `unknown`.** The pectoral and caudal fin length / SL values in Figure 4B–C are plotted, not given in the text. I could not open the figure source data or ZFIN.
- **The zebrafish alleles are not flying-fish alleles.** The convergent flying-fish Lat4a change is **F326L**, while the zebrafish suppressor is **T200K**. No kcnh2a coding change is reported in flying fishes; the paper reports signatures in bioelectric genes (kcnk9, kcnk5a) and in CNEs. The phenocopy shows the mechanism is sufficient. It does not show that flying fishes carry these alleles. The authors' word is "phenocopies".
- **Sources partly disagree on who is called the suppressor.** S1's main text says nr21 is a *medial-fin* suppressor. The Figure 4 legend says more broadly that lat4a is *"a fin suppressor of overgrowth"*. I keep the narrower, main-text reading because paired fins remain overgrown.
- The *lof* dt2 revertant lines are stated to be *"no longer maintained nor frozen"*. *lof* dt2 itself is at ZIRC (ZL86), but S1 does not give ZIRC IDs for lat4a nr21/dmh26.

## 4. Comparison with the recorded value

I could not find any recorded value for claim 281 in this repository: all branches checked, no `docs/research/fish/` directory existed before this file. Without the recorded number, or the full question text, I **CANNOT TELL** whether my value agrees.

```swarm-replication
{"claim_id": 281, "my_value": "2 loci, 2 mutant allele copies (kcnh2a lof/+ enlarger + lat4a nr21/+ suppressor), both dominant gain-of-function, 0 loss-of-function, 0 homozygous", "agrees": null, "note": "Re-derived from the Daane et al. 2021 Curr Biol full text, but the question was truncated and no recorded value was found, so agreement cannot be judged."}
```
