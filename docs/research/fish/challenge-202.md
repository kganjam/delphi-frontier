# Challenge 202: adversarial review of claim S22 (Daane et al. 2021 fin phenocopy)

**Claim under review (not written by me):** "[S22] Daane et al. 2021 (Curr Biol 31:5052-5061.e8,
doi:10.1016/j.cub.2021.08.054) phenocopied flying-fish fin proportions in zebrafish by crossing two
dominant alleles, lat4a^nr21/+ (T200K) and the longfin allele kcnh2a^lof/+, yielding double
heterozygotes with elongated paired fins, a hypocercal caudal fin with elongated ventral lobe, and
wild-type-sized medial fins, measured as fin length normalized to standard length only, with no
measurement of fin area, aspect ratio, lift, gliding or flight."

Recorded evidence level: literature. Value: n/a. Source: harvest:s22-daane-fin-phenocopy-9l9y75.

**Verdict: SURVIVED.** I add three precision notes below. None of them contradicts the claim.

## Sources and read-levels

| Source | Read-level | Notes |
|---|---|---|
| Europe PMC REST record for doi:10.1016/j.cub.2021.08.054 | abstract (plus metadata) | Gives PMID 34534441, PMCID PMC9172250, Curr Biol 31(22):5052-5061.e8, published online 2021-09-16. Authors: Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP. |
| PMC9172250 (author manuscript HTML, pmc.ncbi.nlm.nih.gov) | full-text | Main text, Figure 3 and 4 legends, STAR Methods. I searched it as plain text. |
| NIHMS1735542-supplement-1.pdf and supplement-2.xlsx (Data S1) | could-not-access | PMC returned an HTML challenge page, not the file. |
| ZFIN ZDB-PUB-210918-31 and ZDB-FIG-221222-35 | could-not-access | HTTP 503. |
| PubMed and x-mol | could-not-access | Not reachable from this session's network policy. |
| WebSearch summary | search-summary | Used only to locate the paper. |

## 1. Check of each element against the full text

There is no arithmetic in this claim. The only numbers are the bibliographic fields and "T200K".

| Element of claim | What the paper says (full-text) | Status |
|---|---|---|
| Citation 31:5052-5061.e8, DOI | Matches the Europe PMC metadata. | confirmed |
| lat4a^nr21 is dominant, T200K | "We identified a dominant mutant, nr21 ... identified a nonsynonymous mutation (T200K) in a conserved domain of ... lat4a". In-cis frameshift revertants restore wild type, which shows a gain-of-function effect. | confirmed |
| longfin allele kcnh2a^lof is dominant | "The dominant longfin mutant (lof dt2)". It is gain-of-function: an inversion on chr 2 places the prrx1a regulatory region upstream of kcnh2a, and kcnh2a is upregulated. | confirmed. The formal allele is lof^dt2. The paper itself writes "kcnh2a lof/+". In this name "lof" means *longfin*, not loss-of-function. The allele is gain-of-function. |
| Double heterozygotes, elongated paired fins | "double mutants between kcnh2a lof/+ and lat4a nr21/+ are viable ... show wild-type-sized medial fins, while the paired fins are overgrown". Fig 4A legend: "nr21/lof trans-heterozygotes exhibit elongated paired fins and a hypocercal caudal fin". | confirmed (authors' wording) |
| Hypocercal caudal fin with elongated ventral lobe | "the caudal fin of kcnh2a lof/+; lat4a nr21/+, while generally wild type in size, is hypocercal, with an elongated ventral lobe." | confirmed |
| Wild-type-sized medial fins | Quoted above. | confirmed (authors' wording) |
| Measured as fin length / SL | Fig 4B,C: "Pectoral fin length (B) and caudal fin length (C) ... length normalized by SL". Statistics are one-way ANOVA with Tukey HSD. | confirmed |
| No area, aspect ratio, lift, gliding or flight measurement | Plain-text search of the full manuscript (main text, legends, methods) finds 0 hits for "area", "aspect", "wing loading" and "aerodyn". "flight" (2 hits) and "glid" appear only as descriptions of flying-fish behaviour or as a phylogenetic trait label. No zebrafish measurement of these quantities appears. | confirmed. Scope: main text, legends and methods only. The supplement was not read. |

## 2. Precision notes (my inference, not the authors' claim)

These notes narrow what the claim can support downstream. They do not refute it.

1. **Only two fins were quantified.** Fig 4B,C quantify pectoral fin length/SL and caudal fin
   length/SL, according to the legend. The other phenotypes rest on images and text in the main
   paper:
   - the hypocercal shape and elongated ventral lobe (an asterisk on a representative image in Fig 4A);
   - "elongated paired fins" for the pelvic fins (the word "pelvic" appears once in the paper, in a
     flying-fish figure legend);
   - "wild-type-sized" dorsal and anal fins.

   This rests on a main-text-only search. The Figure S2 panels and Data S1 could not be accessed,
   so a supplementary measurement is `unknown`, not ruled out. The claim's phrase "measured as fin
   length normalized to standard length only" is accurate about the method. It should not be read
   as saying that every listed phenotype was measured.
2. **The phenocopy is a proxy.** "Phenocopies flying-fish fin proportions" means similar length/SL
   ratios and a similar qualitative caudal shape. In the main text, the zebrafish length/SL values
   are not plotted against the flying-fish fin-length vs SL allometry (Fig 1B). So "closely
   phenocopies" is the authors' qualitative judgement. It is not a matched magnitude. Gliding
   performance depends on fin area, span and aspect ratio, wing loading, and the stiffness of the
   ventral caudal lobe. None of these was measured, as the claim itself says. I did not compute any
   zebrafish/flying-fish ratio comparison, because the Fig 4B values are in the supplement, which I
   could not access. The value is `unknown`.
3. **The allele name can be misread.** "kcnh2a^lof" is easy to read as "loss-of-function". The
   allele is a cis-regulatory gain-of-function inversion. Loss-of-function kcnh2a alleles in cis
   (lfr1 Y669N, lfr2 L739Q, WL7 Y418X) are *revertants* that remove the long-fin phenotype. The
   claim says "the longfin allele" and "dominant", so it is not wrong. Downstream users should write
   lof^dt2.

## 3. Hidden assumption, tested relaxed

The claim depends on one assumption: that "double heterozygote" denotes a single genotype class
with consistent fin proportions. The paper reports group comparisons with Tukey HSD, at p ≤ 0.0001
for the relevant contrasts according to the legend. That supports a group-level result. The
per-genotype n and the variance are in the inaccessible supplement, so I cannot test the effect size
or the penetrance. I record this as `unknown`, not as a fault.

## 4. Evidence level

"literature" is honest. The claim reports what a paper did and says. It presents no number as
measured by the claimant, and its negative statement about measurements matches the full text
within the scope I searched.

## 5. Counter-examples and missed regimes

The paper itself notes that a related independent study analysed kcnh2a and lof in fin size, but
did not identify the lesion (its ref. 21). This does not conflict with the claim. I found no
published refutation of the phenocopy result. My search was limited to one WebSearch query and the
paper's own text. That search was too narrow to show that no refutation exists.

## Why it survived

Every factual element checks out verbatim against the full text: the citation, both alleles, both
alleles being dominant, T200K, the double-heterozygote phenotypes, length/SL as the only
morphometric, and the absence of area, aspect-ratio, lift or gliding measurements. The weaknesses I
found are scope notes, and the claim already guards against them with "only" and "no measurement".
Calling them faults would be manufactured.

```swarm-challenge
{"claim_id": 202, "outcome": "survived", "reason": "Every element (citation, dominant gain-of-function alleles nr21 T200K and lof dt2, trans-heterozygote elongated paired fins, hypocercal caudal with elongated ventral lobe, wild-type-sized medial fins, length/SL-only quantification, no area/aspect/lift/gliding measures) matches the PMC9172250 full text; only caveat is that just pectoral and caudal length/SL are quantified in Fig 4B-C, other phenotypes are image/text-based in the main paper.",
  "corrected_value": null,
  "depends_on": ["Daane et al. 2021 Curr Biol 31:5052-5061.e8 author manuscript PMC9172250 (full-text: main text, Fig 3-4 legends, STAR Methods)", "Europe PMC metadata record PMID 34534441", "Supplement NIHMS1735542-supplement-1/2 NOT read (could-not-access); negative scope limited to main text"]}
```
