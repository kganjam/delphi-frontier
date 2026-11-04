# Challenge 202: Daane et al. 2021 flying-fish fin phenocopy [S22]

**Claim under review (not written by me):** "[S22] Daane et al. 2021 (Curr Biol 31:5052-5061.e8, doi:10.1016/j.cub.2021.08.054) phenocopied flying-fish fin proportions in zebrafish by crossing two dominant alleles, lat4a^nr21/+ (T200K) and the longfin allele kcnh2a^lof/+, yielding double heterozygotes with elongated paired fins, a hypocercal caudal fin with elongated ventral lobe, and wild-type-sized medial fins, measured as fin length normalized to standard length only, with no measurement of fin area, aspect ratio, lift, gliding or flight."

**Verdict: WEAKENED.** The bibliographic facts, the genotypes and the phenotypes match the paper. The measurement clause does not: it presents all three phenotypes as quantified by SL-normalized fin length, but the paper quantifies only two fin lengths. The other phenotypes are qualitative or rest on one fin standing in for a class of fins.

## Sources and read-levels

| Source | Read-level | How accessed |
|---|---|---|
| Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP. "Modulation of bioelectric cues in the evolution of flying fishes." Curr Biol 31:5052-5061.e8 (2021). PMID 34534441, PMC9172250 | **full-text** (PMC author-manuscript text: main text, figure legends and STAR Methods) | NCBI BioC PMC-OA API. The Europe PMC fullTextXML endpoint returned HTTP 500. |
| Figure images, Data S1 and supplementary figures S1-S4 | **could-not-access** | I read only the legend text. I did not view any figure panel image. |

## Point-by-point check

### Bibliographic facts: confirmed
Europe PMC metadata gives the title, the author list (Daane first author), Curr Biol vol. 31, pages 5052-5061.e8, and DOI 10.1016/j.cub.2021.08.054. This is an observation from the metadata record.

### Alleles: confirmed
- nr21 came from "a small-scale dominant screen". It was mapped to "a nonsynonymous mutation (T200K) in a conserved domain of the L-type amino acid transporter, lat4a". An in-cis frameshift reverts it, which the authors read as gain-of-function (author's claim, full text).
- The longfin allele (lof^dt2) is "the dominant longfin mutant". It is an inversion on chromosome 2 between 5′ prrx1a and 5′ kcnh2a that does not touch the coding region and raises kcnh2a expression. The paper writes it as kcnh2a^lof (author's claim, full text). The claim's notation "kcnh2a^lof/+" therefore follows the paper. One nuance: lof is a cis-regulatory rearrangement, not a coding allele like T200K.
- The cross is "lat4a^nr21/+ × kcnh2a^lof/+", and the legend calls the progeny "nr21/lof trans-heterozygotes". Confirmed.

### Phenotypes: confirmed as the authors state them
Quoted from the main text: "all fins of kcnh2a^lof/+ are overgrown and all fins of lat4a^nr21/+ are shortened, the lat4a^nr21/+;kcnh2a^lof/+ fish show wild-type-sized medial fins, while the paired fins are overgrown … the caudal fin … while generally wild type in size, is hypocercal, with an elongated ventral lobe." The Fig. 4A legend also says "the nr21/lof trans-heterozygotes exhibit elongated paired fins and a hypocercal caudal fin."

### Measurement clause: this is where the claim fails
The Fig. 4 legend lists every quantified fin dimension for the double heterozygotes: "(B and C) Pectoral fin length (B) and caudal fin length (C) … In (B) and (C), length normalized by SL." Panels D and E are qRT-PCR of kcnh2a and lat4a, not fin dimensions. From this I infer the following. It is an inference from the legend, and I have not seen the images.
1. **"Elongated paired fins": only the pectoral fin was measured.** I found no pelvic-fin measurement for zebrafish. The word "pelvic" appears once in the text, in Fig. 1A, describing the flying fish *Cypselurus callopterus*. So "paired" rests on pectoral fin length plus images. **Proxy:** pectoral fins stand in for paired fins.
2. **"Hypocercal caudal fin with elongated ventral lobe": not measured at all.** Panel 4A marks it with an asterisk on a representative image. I found no lobe-length ratio or asymmetry index. Panel 4C measures total caudal fin length/SL, which cannot show asymmetry. The claim lists this phenotype alongside the others under "measured as fin length normalized to standard length", so it reads as quantified when the paper only observed it in images.
3. **"Wild-type-sized medial fins": only the caudal fin was measured.** I found no dorsal or anal fin length measurement. The text matches "anal fin" 0 times, and "dorsal fin" appears only in flying-fish descriptions and in the qRT-PCR panel 4D. **Proxy:** the caudal fin stands in for all medial fins. The caudal fin is also the fin the same paper calls hypocercal, so it is not a clean "wild-type" control.
4. **The flying-fish trait is an allometric slope, not a ratio.** Fig. 1B defines the flying-fish trait as static allometry: pectoral fin length rises steeply with SL. The zebrafish data are single length/SL ratios per genotype, and the legend text shows no slope across body sizes. So "phenocopied flying-fish fin proportions" compares one ratio in zebrafish with a scaling relationship in Beloniformes. This hidden assumption carries the phenocopy word. It is the authors' own framing ("closely phenocopies"), and the claim reports it faithfully, but it should be scoped.

### Negative statements: confirmed within the scope searched
Search scope: case-insensitive regex over the full author-manuscript text (main text, legends, STAR Methods, key resources table). Supplementary data was not searched.
- "area": 0 hits. "aspect": 0 hits.
- "lift": 1 hit, in the bioinformatics sense ("used to lift the read alignment data"), not aerodynamics.
- "glid": 51 hits, all about flying fishes, flying halfbeaks or phylogenomic foreground lineages, none about zebrafish behaviour. "swim": 0 hits.
So the claim's "no measurement of fin area, aspect ratio, lift, gliding or flight" holds for the main text. Data S1 and Figs S1-S4 are unread, so it is unverified for the supplement.

### Arithmetic
The claim has no arithmetic to redo. Its value is n/a, and I extracted no numbers from the figures because I could not view them.

### Evidence level
"literature" is the right category for what the claim cites. The defect is inside the claim: a qualitative image observation (hypocercal lobe) and two extrapolations (pectoral fins for all paired fins, caudal fin for all medial fins) are worded as if measured.

### Counter-examples or missed regimes
The paper cites "a recent paper detailing comparable analyses of kcnh2a^lof in mediating size of the fin". That is a corroborating study on longfin, not a counter-example. I did not identify or read it, so I cite no details. I found no published counter-example to the phenocopy. My search scope was this paper's text only. I did no wider literature search.

## Corrected statement
Daane et al. 2021 crossed lat4a^nr21/+ (T200K, dominant gain-of-function) with kcnh2a^lof/+ (dominant longfin inversion). The authors report that the double heterozygotes have overgrown paired fins, wild-type-sized medial fins and a hypocercal caudal fin with an elongated ventral lobe. Only pectoral fin length/SL and caudal fin length/SL were quantified (Fig. 4B, C). The hypocercal shape is shown in images only, and pelvic, dorsal and anal fin sizes are not quantified in the main text. No fin area, aspect ratio, allometric slope, lift, gliding or flight was measured, a statement verified for the main text only and not for the supplement.

```swarm-challenge
{"claim_id": 202, "outcome": "weakened", "reason": "Alleles, cross and phenotypes match the full text, but only pectoral and caudal fin length/SL were quantified (Fig 4B,C): the hypocercal ventral lobe is image-only, 'paired' rests on pectoral fins alone and 'wild-type medial fins' on the caudal fin alone, so the claim presents qualitative and proxy results as measured.", "corrected_value": null, "depends_on": ["Daane et al. 2021 Curr Biol 31:5052 PMC9172250 author-manuscript full text (main text, Fig 4 legend, STAR Methods)", "Fig 4 legend: quantified panels are pectoral fin length/SL (B) and caudal fin length/SL (C) only", "Main-text regex search: 0 hits for area, aspect, swim, anal fin; pelvic only in flying-fish Fig 1A", "Supplement (Data S1, Figs S1-S4) and figure images NOT read"]}
```
